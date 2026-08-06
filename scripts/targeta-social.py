#!/usr/bin/env python3
"""Fabrica la imatge que surt quan algú comparteix un enllaç del lloc.

Què és això
-----------
Quan enganxes una adreça a LinkedIn, a Bluesky o a un xat, aquestes webs
llegeixen la pàgina i n'ensenyen una previsualització amb una imatge. Fins
ara aquella imatge era la foto d'estoc d'una aula. Aquest script en fabrica
una de tipogràfica: el nom, el càrrec i la frase del lloc, amb la lletra i
els colors del web.

IMPORTANT: això NO és una eina de construcció del lloc.
--------------------------------------------------------
S'executa a mà, quan canviï el text de la targeta, i prou. El que es publica
és el PNG que en surt, que viu al repositori com qualsevol altra imatge. El
lloc no necessita ni Chrome ni aquest script per funcionar; ni tan sols per
tornar-se a renderitzar. És el mateix plantejament que `excursion-range.py`.

Com funciona
------------
1. Escriu una pàgina HTML de 1200x630 píxels (la mida que demanen les xarxes)
   amb la lletra del lloc, agafada de `fonts/`.
2. Obre aquella pàgina amb el Chrome que ja tens instal·lat, sense finestra,
   i li demana una captura.
3. Desa la captura a `images/social-card.png`.

Ús
--
    python3 scripts/targeta-social.py

Si un dia no tens Chrome, l'script t'ho dirà i no passarà res més: la
targeta que ja hi ha al repositori segueix servint.
"""

import pathlib
import shutil
import subprocess
import sys
import tempfile

ARREL = pathlib.Path(__file__).resolve().parent.parent
DESTI = ARREL / "images" / "social-card.png"

# El text de la targeta. És l'únic que has de tocar per canviar-la.
NOM = "Rafel Cirer-Sastre"
CARREC = "Associate Professor of Kinesiology · INEFC Lleida"
FRASE = "Many measurements strike me as more convincing than reliable."
ADRECA = "rafelcirer.com"

# Els mateixos colors que theme.scss. Si allà en canvies un, canvia'l aquí.
INK = "#15181b"
INK_MUTED = "#5c6670"
ACCENT = "#0e6b5e"
PAPER = "#ffffff"

# Mida que demanen totes les xarxes per a la previsualització d'un enllaç.
AMPLE, ALT = 1200, 630

# Perfil de Chrome reaprofitat entre execucions. Si es crea de nou cada
# vegada, la captura triga minuts en comptes de segons. Es pot esborrar
# sense conseqüències: només és memòria cau del navegador.
PERFIL = pathlib.Path(tempfile.gettempdir()) / "targeta-social-chrome"

CHROME = pathlib.Path(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)


def html() -> str:
    fonts = (ARREL / "fonts").as_uri()
    return f"""<!doctype html><meta charset="utf-8">
<style>
  @font-face {{
    font-family: "Schibsted Grotesk";
    font-weight: 400 700;
    src: url("{fonts}/schibsted-grotesk.woff2") format("woff2");
  }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    width: {AMPLE}px; height: {ALT}px;
    background: {PAPER};
    font-family: "Schibsted Grotesk", sans-serif;
    color: {INK};
    display: flex; flex-direction: column; justify-content: center;
    padding: 0 84px;
    box-sizing: border-box;
  }}
  /* Una franja del color de marca a l'esquerra: identifica la targeta
     d'un cop d'ull encara que surti petita al costat d'altres enllaços. */
  .franja {{
    position: absolute; left: 0; top: 0; bottom: 0; width: 14px;
    background: {ACCENT};
  }}
  .nom {{
    font-size: 94px; font-weight: 600;
    letter-spacing: -0.042em; line-height: 1.02;
    margin: 0 0 18px;
  }}
  .carrec {{
    font-size: 29px; color: {INK_MUTED};
    margin: 0 0 46px;
  }}
  .frase {{
    font-size: 43px; line-height: 1.3; font-weight: 400;
    border-left: 5px solid {ACCENT};
    padding-left: 26px;
    margin: 0 0 52px;
    max-width: 27ch;
  }}
  .adreca {{
    font-size: 26px; font-weight: 600; color: {ACCENT};
    letter-spacing: -0.01em; margin: 0;
  }}
</style>
<div class="franja"></div>
<p class="nom">{NOM}</p>
<p class="carrec">{CARREC}</p>
<p class="frase">{FRASE}</p>
<p class="adreca">{ADRECA}</p>
"""


def main() -> None:
    if not CHROME.exists():
        sys.exit(
            "No hi ha Google Chrome a /Applications.\n"
            "La targeta que ja hi ha a images/social-card.png segueix servint;\n"
            "només cal Chrome per tornar-la a fabricar."
        )

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        pagina = tmp / "targeta.html"
        pagina.write_text(html(), encoding="utf-8")
        sortida = tmp / "targeta.png"

        subprocess.run(
            [
                str(CHROME),
                "--headless",
                "--disable-gpu",
                # Cal per llegir la font des de fonts/, que és un altre fitxer
                # local: sense això Chrome ho bloqueja i la targeta surt amb
                # la lletra del sistema.
                "--allow-file-access-from-files",
                f"--window-size={AMPLE},{ALT}",
                f"--screenshot={sortida}",
                # Perquè no li apliqui la mida de pantalla del Mac.
                "--force-device-scale-factor=1",
                "--hide-scrollbars",
                # Sense aquestes, Chrome es passa minuts fent la posada en
                # marxa d'un navegador de debò (comprovar si és el navegador
                # per defecte, sincronitzar, carregar extensions...) abans de
                # fer la captura. Aquí no en volem res.
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
                "--disable-background-networking",
                "--disable-sync",
                "--disable-component-update",
                # Li diu: fes córrer el rellotge de la pàgina 3 segons de
                # cop i captura. Sense això pot quedar-se esperant.
                "--virtual-time-budget=3000",
                f"--user-data-dir={PERFIL}",
                pagina.as_uri(),
            ],
            check=True,
            capture_output=True,
        )

        if not sortida.exists():
            sys.exit("Chrome no ha arribat a escriure la captura.")
        DESTI.parent.mkdir(exist_ok=True)
        shutil.copy(sortida, DESTI)

    print(f"{DESTI.relative_to(ARREL)}  {DESTI.stat().st_size / 1024:.0f} KB")
    print("Recorda tornar a renderitzar el lloc perquè se la copiï.")


if __name__ == "__main__":
    main()
