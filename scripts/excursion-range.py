#!/usr/bin/env python3
"""Genera images/excursion-range.svg, la figura dels quatre rangs d'excursió.

Executa'l des d'on vulguis:  python3 scripts/excursion-range.py

Es genera perquè les molles tenen fins a 143 punts i editar-les a mà és
inviable. El pas de les molles el fixa PITCH: cada fila rep el nombre de
bucles que cal perquè, amb el múscul allargat (inici del recorregut), totes
quatre tinguin la mateixa distància entre bucles.
"""

import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "images", "excursion-range.svg")

WALL = 884.0   # ancoratge de les gomes
LEAD = 6.0     # tram recte a cada punta de la molla
AMP = 6.0      # amplitud del bucle
PITCH = 2.58   # distància entre bucles amb el múscul allargat
EASE = ('calcMode="spline" keyTimes="0;0.75;1" '
        'keySplines="0.45 0 0.55 1;0.45 0 0.55 1"')
TIME = 'dur="6s" begin="0s" repeatCount="indefinite"'

ORIGIN = 150.0
BELLY_X = 168.0
TENDON = 18.0
K = 470.0      # gruix de la panxa = K / sqrt(amplada)


def zig(x0, cy, n):
    """Molla de n bucles entre x0 i WALL, centrada a cy. n+3 punts."""
    pts = [(x0, cy), (x0 + LEAD, cy)]
    a, b = x0 + LEAD, WALL - LEAD
    seg = (b - a) / n
    for i in range(1, n):
        pts.append((a + i * seg, cy + (AMP if i % 2 else -AMP)))
    pts += [(b, cy), (WALL, cy)]
    return "M" + " L".join("%.1f,%.1f" % p for p in pts)


def belly(ins):
    """Amplada, gruix i y de la panxa per a una inserció donada."""
    w = ins - ORIGIN - 2 * TENDON
    h = K / (w ** 0.5)
    return w, h


ROWS = [
    ("Inner MER",    "concentric end",  128.0, 330.0, 510.0),
    ("Mid MER",      "neither extreme", 196.0, 450.0, 670.0),
    ("Outer MER",    "eccentric end",   264.0, 630.0, 810.0),
    ("Complete MER", "limit to limit",  330.0, 330.0, 810.0),
]

blocks = []
for name, gloss, cy, lo, hi in ROWS:
    n = max(6, round(((WALL - LEAD) - (hi + LEAD)) / PITCH))
    w0, h0 = belly(lo)
    w1, h1 = belly(hi)
    y0, y1 = cy - h0 / 2, cy - h1 / 2
    pa, pb = zig(lo, cy, n), zig(hi, cy, n)
    blocks.append(f"""
  <!-- {'=' * 26} {name} {'=' * 26} -->
  <text class="acr" x="128" y="{cy - 4:.0f}" text-anchor="end">{name}</text>
  <text class="glo" x="128" y="{cy + 13:.0f}" text-anchor="end">{gloss}</text>

  <path class="elas" d="{pa}">
    <animate attributeName="d" {TIME} {EASE}
      values="{pa};
              {pb};
              {pa}"/>
    <animate attributeName="stroke-width" values="1.6;2.4;1.6" {TIME} {EASE}/>
  </path>

  <line class="tend" x1="{ORIGIN:.0f}" y1="{cy:.0f}" x2="{BELLY_X:.0f}" y2="{cy:.0f}"/>
  <circle class="ins" cx="{ORIGIN:.0f}" cy="{cy:.0f}" r="4.5"/>
  <rect class="belly" x="{BELLY_X:.0f}" y="{y0:.1f}" width="{w0:.0f}" height="{h0:.1f}" rx="9">
    <animate attributeName="width"  values="{w0:.0f};{w1:.0f};{w0:.0f}" {TIME} {EASE}/>
    <animate attributeName="height" values="{h0:.1f};{h1:.1f};{h0:.1f}" {TIME} {EASE}/>
    <animate attributeName="y"      values="{y0:.1f};{y1:.1f};{y0:.1f}" {TIME} {EASE}/>
  </rect>
  <line class="tend" x1="{lo - TENDON:.0f}" y1="{cy:.0f}" x2="{lo:.0f}" y2="{cy:.0f}">
    <animate attributeName="x1" values="{lo - TENDON:.0f};{hi - TENDON:.0f};{lo - TENDON:.0f}" {TIME} {EASE}/>
    <animate attributeName="x2" values="{lo:.0f};{hi:.0f};{lo:.0f}" {TIME} {EASE}/>
  </line>
  <circle class="ins" cx="{lo:.0f}" cy="{cy:.0f}" r="4.5">
    <animate attributeName="cx" values="{lo:.0f};{hi:.0f};{lo:.0f}" {TIME} {EASE}/>
  </circle>
  <path class="trav" d="M{lo:.0f} {cy + 24:.0f} v12 M{lo:.0f} {cy + 30:.0f} H{hi:.0f} M{hi:.0f} {cy + 24:.0f} v12"/>""")
    print(f"{name}: {n} bucles, pas en repòs {((WALL - LEAD) - (hi + LEAD)) / n:.2f}")

hatch = " ".join("M884 %d l10 -9" % y for y in range(116, 381, 24))

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 520" width="900" height="520" role="img" aria-labelledby="exc-t exc-d">
  <title id="exc-t">The four muscle excursion ranges compared in EXCURSE</title>
  <desc id="exc-d">Four muscles are drawn one above another on a horizontal muscle length axis, all fixed at the same origin on the left. Each is a rounded rectangle standing for the muscle belly, joined by a short tendon at either end to two marked attachment points: a fixed proximal one at the origin and a distal one that moves. From that distal attachment an elastic band runs to a fixed anchor on the right, so every muscle works against a resistance. All four bands are at rest, with the same spacing between coils, when their muscle is at its longest; each then stretches by the length of its own excursion as the muscle shortens. Two vertical lines mark the shortening limit, the shortest length the muscle reaches voluntarily, and the lengthening limit, the longest; a dashed line between them marks the resting length. Each muscle shortens and lengthens only within its own excursion range: Inner MER works against the shortening limit and stays shorter than resting length, Outer MER works against the lengthening limit and stays longer than resting length, Mid MER straddles resting length without reaching either limit, and Complete MER travels the whole distance from one limit to the other. The belly thickens as it shortens and thins as it lengthens, while the tendons keep their length. A bar under each muscle marks the travel of its distal attachment, which is that muscle excursion range.</desc>

  <style>
    .lim  {{ font: 600 14px system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: #0e6b5e; }}
    .sub  {{ font: 400 13px system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: #5c6670; }}
    .acr  {{ font: 700 15px system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: #15181b; }}
    .glo  {{ font: 400 12.5px system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: #5c6670; }}
    .axn  {{ font: 700 12px system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: #5c6670; letter-spacing: 0.1em; }}
    .note {{ font: 400 13px system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: #5c6670; }}
    .leg  {{ font: 400 13px system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: #15181b; }}
    .belly {{ fill: #c9825f; fill-opacity: 0.78; stroke: #a2603f; stroke-width: 1.2; }}
    .tend  {{ stroke: #a2603f; stroke-width: 3; stroke-linecap: round; }}
    .ins   {{ fill: #a2603f; }}
    .trav  {{ stroke: #a2603f; stroke-width: 1.4; fill: none; }}
    .elas  {{ stroke: #5c6670; stroke-width: 2; fill: none; stroke-linejoin: round; }}
    .wall  {{ stroke: #5c6670; stroke-width: 1.6; fill: none; }}
  </style>

  <!-- =====================================================================
       AQUEST FITXER ES GENERA. No l'editis a mà: els camins de les molles
       tenen fins a 143 punts. Canvia els números a scripts/excursion-range.py
       i torna a executar:  python3 scripts/excursion-range.py

       Tots els músculs neixen a l'origen x=150. Límit d'escurçament x=330,
       longitud de repòs x=530, límit d'allargament x=810, ancoratge de les
       gomes x=884. Cada fila té tendó fix, panxa, tendó mòbil, inserció
       distal i goma. La panxa engreixa en escurçar-se (gruix = 470/√amplada,
       el volum es manté); els tendons no canvien de llarg.

       Recorregut de la inserció distal, per fila:
         Inner 330→510 · Mid 450→670 · Outer 630→810 · Complete 330→810

       LES MOLLES tenen un nombre de bucles diferent a cada fila, calculat
       perquè totes quatre tinguin el mateix pas (PITCH) amb el múscul
       allargat, que és l'inici del recorregut. Llegit físicament: són la
       mateixa goma de llargades diferents, totes en repòs a l'inici, i cada
       una s'estira exactament el que val la seva excursió.

       Les quatre files van totes alhora (begin="0s"): així, en qualsevol
       instant, les insercions són al mateix punt de la mateixa repetició i
       la diferència que es veu és la condició, no la fase.

       RITME 1:3. keyTimes="0;0.75;1" parteix el cicle de 6 s en excèntrica
       (4,5 s) i concèntrica (1,5 s).
       ===================================================================== -->

  <!-- fites -->
  <text class="sub" x="150" y="82" text-anchor="middle">origin</text>

  <text class="lim" x="330" y="64" text-anchor="middle">shortening limit</text>
  <text class="sub" x="330" y="82" text-anchor="middle">shortest voluntary length</text>

  <text class="sub" x="530" y="82" text-anchor="middle">resting length</text>

  <text class="lim" x="810" y="64" text-anchor="middle">lengthening limit</text>
  <text class="sub" x="810" y="82" text-anchor="middle">longest voluntary length</text>

  <line x1="150" y1="96" x2="150" y2="376" stroke="#c3cacd" stroke-width="1.5"/>
  <line x1="330" y1="96" x2="330" y2="376" stroke="#0e6b5e" stroke-width="1.6"/>
  <line x1="530" y1="96" x2="530" y2="376" stroke="#c3cacd" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="810" y1="96" x2="810" y2="376" stroke="#0e6b5e" stroke-width="1.6"/>

  <!-- ancoratge de les gomes -->
  <path class="wall" d="M884 104 V376"/>
  <path class="wall" d="{hatch}"/>
{"".join(blocks)}

  <!-- eix -->
  <line x1="150" y1="392" x2="872" y2="392" stroke="#5c6670" stroke-width="1.5"/>
  <path d="M870 386 L884 392 L870 398 Z" fill="#5c6670"/>
  <text class="axn" x="150" y="414">MUSCLE LENGTH</text>

  <!-- llegenda -->
  <path class="elas" d="M150 443 L153 443 L156 447 L159 439 L162 447 L165 439 L168 447 L171 439 L174 447 L177 439 L180 447 L183 439 L186 443 L190 443"/>
  <text class="leg" x="200" y="447">elastic resistance</text>

  <path class="wall" d="M330 435 V451 M330 439 l8 -7 M330 447 l8 -7"/>
  <text class="leg" x="346" y="447">fixed anchor</text>

  <text class="note" x="150" y="480">MER, muscle excursion range: how far the distal attachment travels — the bar under each muscle.</text>
  <text class="note" x="150" y="500">The four ranges are anchored to the two limits and individualised per participant, muscle and exercise.</text>
</svg>
"""

with open(OUT, "w") as f:
    f.write(svg)
print("escrit:", OUT, len(svg), "bytes")
