#!/usr/bin/env python3
"""
Construeix la llista de publicacions del web a partir d'ORCID.

    python3 scripts/publications.py

Escriu `publications.yml` a l'arrel. No toca cap altre fitxer.

COM FUNCIONA, i per què així
----------------------------
1. ORCID és la FONT DE VERITAT. És la llista que tu controles.
2. OpenAlex només ENRIQUEIX: citacions, accés obert, autors. No decideix
   què surt a la llista.

   El motiu està comprovat amb dades: filtrant OpenAlex pel teu ORCID es
   perden set articles teus, perquè OpenAlex només te'ls atribueix si el
   teu ORCID consta en aquell registre concret, cosa que sovint no passa
   quan ets autor intermedi. Si algun dia algú proposa "simplificar-ho"
   llegint només OpenAlex, aquesta és la raó per no fer-ho.

3. Crossref cobreix els que OpenAlex no té, per als autors.
4. `exclusions.yml` treu entrades; `extres.yml` n'afegeix a mà.

Dependències: PyYAML. La resta és biblioteca estàndard.
"""

import base64
import collections
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ORCID_ID = "0000-0001-6687-8201"
MAILTO = "rcirer@gencat.cat"          # entra al "polite pool" d'OpenAlex i Crossref
ARREL = Path(__file__).resolve().parent.parent
SORTIDA = ARREL / "publications.yml"
UA = f"rafelcirer-web/1.0 (mailto:{MAILTO})"


# --------------------------------------------------------------------------
# Utilitats de xarxa
# --------------------------------------------------------------------------

def demana(url, capcaleres=None, intents=3):
    """GET amb reintents. Retorna JSON, o None si no s'ha pogut."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(capcaleres or {})})
    for i in range(intents):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            if i == intents - 1:
                print(f"  ! ha fallat {url[:70]}: {e}", file=sys.stderr)
                return None
            time.sleep(2 * (i + 1))
    return None


def normalitza_doi(valor):
    """Un DOI en minúscules i sense prefixos d'URL, per poder comparar-los."""
    if not valor:
        return None
    d = valor.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d or None


# --------------------------------------------------------------------------
# 1. ORCID: la font de veritat
# --------------------------------------------------------------------------

def llegeix_orcid():
    """Retorna la llista d'obres del perfil ORCID públic."""
    dades = demana(
        f"https://pub.orcid.org/v3.0/{ORCID_ID}/works",
        capcaleres={"Accept": "application/json"},
    )
    if not dades:
        sys.exit("No s'ha pogut llegir ORCID. Atura't: sense la font de veritat "
                 "no s'ha de generar cap llista.")

    obres = []
    for grup in dades.get("group", []):
        # ORCID agrupa el mateix treball declarat per fonts diferents.
        # El primer resum del grup ja porta les dades bones.
        s = grup["work-summary"][0]

        doi = None
        for ident in grup.get("external-ids", {}).get("external-id", []):
            if ident.get("external-id-type") == "doi":
                doi = normalitza_doi(ident.get("external-id-value"))
                break

        titol = (s.get("title") or {}).get("title", {}).get("value")
        data = s.get("publication-date") or {}
        any_ = (data.get("year") or {}).get("value")

        obres.append({
            "doi": doi,
            "titol": (titol or "").strip(),
            "any": int(any_) if any_ and str(any_).isdigit() else None,
            "revista": ((s.get("journal-title") or {}) or {}).get("value"),
            "tipus": s.get("type"),
            "url_orcid": (s.get("url") or {}).get("value"),
        })
    return obres


# --------------------------------------------------------------------------
# 2. OpenAlex: enriquiment
# --------------------------------------------------------------------------

def enriqueix_openalex(dois, mida_lot=45):
    """Consulta OpenAlex per DOI, en lots. Retorna {doi: dades}."""
    resultat = {}
    dois = [d for d in dois if d]
    for i in range(0, len(dois), mida_lot):
        lot = dois[i:i + mida_lot]
        filtre = "doi:" + "|".join(lot)
        url = ("https://api.openalex.org/works?per-page=200"
               f"&filter={urllib.parse.quote(filtre, safe=':|/.')}"
               f"&mailto={MAILTO}")
        dades = demana(url)
        if not dades:
            continue
        for w in dades.get("results", []):
            d = normalitza_doi(w.get("doi"))
            if not d:
                continue
            loc = w.get("primary_location") or {}
            font = loc.get("source") or {}

            # OpenAlex pot tenir DOS registres amb el mateix DOI, i un ser
            # erroni. Cas real detectat: 10.1016/j.jsams.2020.06.019 retorna
            # l'article bo i, a més, "Aristotle and Bertolt Brecht" (1972).
            # Ens quedem el registre que el té a ell com a autor.
            autories = w.get("authorships") or []
            es_seu = any(
                (((a.get("author") or {}).get("orcid")) or "").endswith(ORCID_ID)
                for a in autories
            )
            if d in resultat and resultat[d].get("_seu") and not es_seu:
                continue

            resultat[d] = {
                "_seu": es_seu,
                "titol": w.get("title") or w.get("display_name"),
                "citacions": w.get("cited_by_count", 0),
                "revista": font.get("display_name"),
                "obert": bool((w.get("open_access") or {}).get("is_oa")),
                "tipus": w.get("type"),
                "any": w.get("publication_year"),
                "autors": [
                    (a.get("author") or {}).get("display_name")
                    for a in (w.get("authorships") or [])
                ],
            }
        time.sleep(0.2)   # cortesia amb l'API
    return resultat


# --------------------------------------------------------------------------
# 3. Crossref: els que OpenAlex no té
# --------------------------------------------------------------------------

def enriqueix_crossref(dois):
    """Només per als DOI que OpenAlex desconeix. Una crida per DOI."""
    resultat = {}
    for d in dois:
        dades = demana(f"https://api.crossref.org/works/{urllib.parse.quote(d)}"
                       f"?mailto={MAILTO}")
        if not dades:
            continue
        m = dades.get("message", {})
        autors = []
        for a in m.get("author", []) or []:
            nom = " ".join(x for x in (a.get("given"), a.get("family")) if x)
            if nom:
                autors.append(nom)
        resultat[d] = {
            "titol": (m.get("title") or [None])[0],
            "citacions": m.get("is-referenced-by-count", 0),
            "revista": (m.get("container-title") or [None])[0],
            "obert": False,
            "tipus": m.get("type"),
            "any": (m.get("issued", {}).get("date-parts", [[None]])[0] or [None])[0],
            "autors": autors,
        }
        time.sleep(0.2)
    return resultat


# --------------------------------------------------------------------------
# 4. Capa manual
# --------------------------------------------------------------------------

def llegeix_yaml(nom):
    ruta = ARREL / nom
    if not ruta.exists():
        return []
    contingut = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    return contingut or []


MENUDES = {"a", "an", "and", "for", "in", "of", "on", "the", "to", "y", "e",
           "de", "del", "la", "el", "i", "per", "en"}


def titula(nom):
    """'INTERNATIONAL JOURNAL OF...' -> 'International Journal of...'"""
    paraules = nom.split()
    sortida = []
    for i, p in enumerate(paraules):
        b = p.lower()
        sortida.append(b if (i and b in MENUDES) else b.capitalize())
    return " ".join(sortida)


# Revistes que les bases de dades escriuen amb la majúscula equivocada.
# La clau és en minúscules i sense espais; el valor, la grafia correcta.
# Afegeix-n'hi quan en detectis una: és més honest que intentar endevinar-ho.
GRAFIES = {
    "eclinicalmedicine": "eClinicalMedicine",
}


def tria_revista(orcid_val, api_val):
    """
    ORCID mana, però Web of Science diposita els noms en MAJÚSCULES i això
    fa lleig i incoherent (la mateixa revista surt de dues maneres). Quan
    ORCID crida, provem amb el nom de l'API, que ve de l'editor.
    """
    if orcid_val and not orcid_val.isupper():
        nom = orcid_val
    elif api_val:
        nom = api_val
    elif orcid_val:
        nom = titula(orcid_val)
    else:
        return None
    return GRAFIES.get(nom.lower().replace(" ", ""), nom)


def escriu_histograma(publicacions):
    """
    Escriu `histograma.css` amb l'amplada de la barra de cada any.

    Quarto pinta el filtre de categories com a <div class="category"
    data-category="BASE64"> i nosaltres només hi afegim una variable CSS.
    Els elements segueixen sent els seus i el filtre continua funcionant;
    si algun dia Quarto canvia aquesta estructura, les barres deixaran de
    sortir però la llista i el filtre continuaran igual.
    """
    compte = collections.Counter(
        str(p["year"]) for p in publicacions if p.get("year")
    )
    if not compte:
        return
    maxim = max(compte.values())

    linies = [
        "/* GENERAT per scripts/publications.py — no l'editis a mà. */",
        "/* Amplada de la barra de cada any, proporcional al màxim. */",
    ]
    for any_, n in sorted(compte.items()):
        clau = base64.b64encode(any_.encode()).decode()
        linies.append(
            f'.quarto-listing-category .category[data-category="{clau}"]'
            f" {{ --barra: {round(100 * n / maxim)}%; }}"
        )
    (ARREL / "histograma.css").write_text("\n".join(linies) + "\n", encoding="utf-8")
    print(f"Escrit histograma.css: {len(compte)} anys, màxim {maxim}")


def formata_autors(noms, maxim=8):
    if not noms:
        return None
    if len(noms) > maxim:
        return ", ".join(noms[:maxim]) + " et al."
    return ", ".join(noms)


# --------------------------------------------------------------------------
# Programa principal
# --------------------------------------------------------------------------

def main():
    print("Llegint ORCID...")
    obres = llegeix_orcid()
    print(f"  {len(obres)} obres al perfil")

    exclosos = {normalitza_doi(x) for x in llegeix_yaml("exclusions.yml")}
    if exclosos:
        print(f"  {len(exclosos)} exclusions declarades")

    dois = [o["doi"] for o in obres if o["doi"] and o["doi"] not in exclosos]

    print("Consultant OpenAlex...")
    oa = enriqueix_openalex(dois)
    print(f"  {len(oa)} de {len(dois)} enriquits")

    pendents = [d for d in dois if d not in oa]
    if pendents:
        print(f"Consultant Crossref per als {len(pendents)} restants...")
        oa.update(enriqueix_crossref(pendents))

    sortida, sense_doi, sense_dades = [], [], []
    for o in obres:
        d = o["doi"]
        if not d:
            sense_doi.append(o["titol"])
            continue
        if d in exclosos:
            continue
        e = oa.get(d, {})
        if not e:
            sense_dades.append(d)

        # ORCID és la font de veritat també per a les dades bibliogràfiques:
        # l'enriquiment només omple el que ORCID no té. A l'inrevés, un sol
        # registre corrupte d'una base de dades externa et canvia l'any o la
        # revista d'un article teu sense que te n'adonis.
        if o["any"] and e.get("any") and abs(int(e["any"]) - int(o["any"])) > 1:
            print(f"  avís: {d} — ORCID diu {o['any']} i l'enriquiment {e['any']}. "
                  f"Fem cas d'ORCID.")

        sortida.append({
            "doi": d,
            "title": o["titol"],
            "year": o["any"] or e.get("any"),
            "journal": tria_revista(o["revista"], e.get("revista")),
            "authors": formata_autors(e.get("autors")),
            "citations": e.get("citacions", 0),
            "open_access": e.get("obert", False),
            "type": e.get("tipus") or o["tipus"],
            "href": f"https://doi.org/{d}",
            "source": "orcid",
        })

    # Els extres que ja hagin aparegut a ORCID no es dupliquen. Passa quan
    # afegeixes a extres.yml una publicació que li faltava el DOI a ORCID i
    # més endavant l'arregles al perfil: aleshores ja arriba per la via bona.
    ja_hi_son = {x["doi"] for x in sortida if x.get("doi")}
    extres = []
    for extra in llegeix_yaml("extres.yml"):
        extra = dict(extra)
        d = normalitza_doi(extra.get("doi"))
        if d and d in ja_hi_son:
            print(f"  extres.yml: {d} ja arriba per ORCID, no el dupliquem.\n"
                  f"    Ja el pots esborrar d'extres.yml.")
            continue
        extra["doi"] = d
        extres.append(extra)

    # Els extres amb DOI s'enriqueixen igual que la resta. Així a extres.yml
    # només cal escriure el DOI: ni autors, ni citacions, ni revista a mà.
    nous = [x["doi"] for x in extres if x.get("doi") and x["doi"] not in oa]
    if nous:
        print(f"Enriquint {len(nous)} entrades d'extres.yml...")
        oa.update(enriqueix_openalex(nous))
        falten = [d for d in nous if d not in oa]
        if falten:
            oa.update(enriqueix_crossref(falten))

    for extra in extres:
        e = oa.get(extra.get("doi") or "", {})
        # El que escriguis a mà mana sempre; l'API només omple els buits.
        for clau, valor in (
            ("title", e.get("titol")),
            ("year", e.get("any")),
            ("journal", e.get("revista")),
            ("authors", formata_autors(e.get("autors"))),
            ("citations", e.get("citacions")),
            ("open_access", e.get("obert")),
            ("type", e.get("tipus")),
        ):
            if valor is not None and extra.get(clau) in (None, ""):
                extra[clau] = valor
        extra.setdefault("source", "extres")
        extra.setdefault("citations", 0)
        if extra.get("doi") and not extra.get("href"):
            extra["href"] = f"https://doi.org/{extra['doi']}"
        if not extra.get("title"):
            print(f"  ! extres.yml: una entrada sense títol i sense dades "
                  f"({extra.get('doi') or 'sense DOI'}). Cal posar-hi title.",
                  file=sys.stderr)
            continue
        sortida.append(extra)

    sortida.sort(key=lambda x: (-(x.get("year") or 0), -(x.get("citations") or 0)))

    # Camps que espera el llistat de Quarto:
    #   path       -> on porta l'enllaç del títol
    #   categories -> l'any, que és el que dona el filtre de la pàgina
    #   oa         -> text curt, perquè una casella buida es llegeix millor
    #                 que un "false" repetit quaranta vegades
    for x in sortida:
        x["path"] = x.pop("href", None) or x.get("path")
        if x.get("year"):
            x.setdefault("categories", [str(x["year"])])
        x["oa"] = "Open access" if x.get("open_access") else ""

    SORTIDA.write_text(
        "# GENERAT AUTOMÀTICAMENT — no editis aquest fitxer a mà.\n"
        "# Prové d'ORCID; per canviar-ne el contingut, edita el teu perfil\n"
        "# d'ORCID, o bé exclusions.yml / extres.yml, i torna a executar:\n"
        "#   python3 scripts/publications.py\n"
        + yaml.safe_dump(sortida, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )

    escriu_histograma(sortida)

    print(f"\nEscrit {SORTIDA.name}: {len(sortida)} publicacions")
    if sense_doi:
        print(f"\n{len(sense_doi)} obres d'ORCID sense DOI, fora de la llista:")
        for t in sense_doi:
            print(f"   - {t[:72]}")
        print("  Si n'hi ha alguna que ha de sortir, posa-la a extres.yml.")
    if sense_dades:
        print(f"\n{len(sense_dades)} sense dades ni d'OpenAlex ni de Crossref:")
        for d in sense_dades:
            print(f"   - {d}")


if __name__ == "__main__":
    main()
