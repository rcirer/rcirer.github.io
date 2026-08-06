#!/usr/bin/env python3
"""Baixa les fonts del lloc i les desa al repositori.

Per què existeix aquest script
------------------------------
El lloc no pot demanar les fonts a Google Fonts en temps real: seria una
petició del navegador del lector a un tercer, i això és un problema de
protecció de dades (i una dependència externa que un dia pot caure). Les
fonts, doncs, viuen al repositori i les serveix el mateix domini.

Baixar-les a mà és feina de precisió: cal quedar-se només amb el subconjunt
de caràcters llatí, en format woff2 i en versió variable. Això ho fa aquest
script, i deixa escrit d'on ha sortit cada fitxer.

Com funciona
------------
Google Fonts publica les fonts amb llicència oberta (SIL Open Font License).
La seva API de CSS retorna, per a cada família, una llista de blocs
@font-face partida per subconjunts d'alfabet (llatí, ciríl·lic, grec...).
Nosaltres agafem només el bloc marcat `/* latin */` i en baixem el fitxer.

  - Subconjunt llatí: cobreix tot el que fa servir el lloc (anglès i català,
    inclòs el punt volat de la ela geminada). Comprovat sobre el text real.
  - Format woff2: el format comprimit estàndard del web des del 2018.
  - Versió variable: un sol fitxer conté tots els gruixos de 400 a 700, en
    comptes d'un fitxer per gruix. Menys pes i menys peces.

Ús
--
    python3 scripts/fonts.py                  # baixa a fonts/
    python3 scripts/fonts.py _temes/fonts     # baixa a un altre lloc

Les famílies a baixar són a la llista FAMILIES, aquí sota. Per canviar la
tipografia del lloc: canvia la llista, executa l'script, i actualitza els
noms de família a `theme.scss`. Els fitxers antics s'han d'esborrar a mà.
"""

import pathlib
import re
import sys
import urllib.parse
import urllib.request

# Famílies que fa servir el lloc. `italic` a False per a les que només
# s'usen en títols: un títol no va mai en cursiva i el fitxer seria pes mort.
#
# Schibsted Grotesk fa de tot: text, títols i navegació. Triada el 6 d'agost
# de 2026 després de comparar vuit lletres sobre el lloc renderitzat sencer.
# La cursiva sí que cal: la porten els noms de revista de publications.qmd.
FAMILIES = [
    ("Schibsted Grotesk", True),
]

# Gruixos que necessitem. El text va a 400, la negreta a 700, i els títols
# del lloc a 650 (theme.scss). Amb una font variable, demanar el rang sencer
# surt de franc: és el mateix fitxer.
PES = "400..700"

# Google serveix fitxers diferents segons el navegador que els demana. Sense
# aquesta capçalera ens donaria el format antic (ttf), que pesa el triple.
NAVEGADOR = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def descarrega(url: str) -> bytes:
    peticio = urllib.request.Request(url, headers={"User-Agent": NAVEGADOR})
    with urllib.request.urlopen(peticio, timeout=30) as resposta:
        return resposta.read()


def css_de_la_familia(familia: str, italica: bool) -> str:
    """Demana a Google el full d'estils de la família, en versió variable."""
    if italica:
        eixos = f"ital,wght@0,{PES};1,{PES}"
    else:
        eixos = f"wght@{PES}"
    consulta = urllib.parse.urlencode(
        {"family": f"{familia}:{eixos}", "display": "swap"}, safe=":;,@."
    )
    return descarrega(f"https://fonts.googleapis.com/css2?{consulta}").decode("utf-8")


def blocs_llatins(css: str):
    """Retorna (estil, url) de cada bloc @font-face del subconjunt llatí.

    El CSS ve amb un comentari davant de cada bloc que en diu el subconjunt
    (`/* latin */`, `/* cyrillic */`...). Tallem pel comentari i ens quedem
    amb el que porta l'etiqueta exacta `latin`.
    """
    parts = re.split(r"/\*\s*([a-z-]+)\s*\*/", css)[1:]
    for etiqueta, cos in zip(parts[0::2], parts[1::2]):
        if etiqueta != "latin":
            continue
        url = re.search(r"src:\s*url\(([^)]+)\)", cos)
        estil = re.search(r"font-style:\s*(\w+)", cos)
        if url:
            yield (estil.group(1) if estil else "normal"), url.group(1)


def nom_de_fitxer(familia: str, estil: str) -> str:
    base = familia.lower().replace(" ", "-")
    return f"{base}{'-italic' if estil == 'italic' else ''}.woff2"


def main() -> None:
    desti = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "fonts")
    desti.mkdir(parents=True, exist_ok=True)

    total = 0
    for familia, italica in FAMILIES:
        css = css_de_la_familia(familia, italica)
        trobats = list(blocs_llatins(css))
        if not trobats:
            print(f"  !! {familia}: cap subconjunt llatí. Nom mal escrit?")
            continue
        for estil, url in trobats:
            dades = descarrega(url)
            fitxer = desti / nom_de_fitxer(familia, estil)
            fitxer.write_bytes(dades)
            total += len(dades)
            print(f"  {fitxer}  {len(dades) / 1024:.0f} KB")

    print(f"\nTotal: {total / 1024:.0f} KB a {desti}/")
    print("Llicència de totes: SIL Open Font License 1.1")


if __name__ == "__main__":
    main()
