# CLAUDE.md — Web personal de Rafel Cirer-Sastre

Context permanent del projecte per a Claude Code. Llegeix-lo sencer abans de fer res.

Aquest fitxer és el **document mestre** de decisions i preferències del projecte. No en
facis còpies: si cal canviar una regla, canvia-la aquí.

`cv-extracte-web.md` és la **font factual única**. Qualsevol dada de carrera, publicació,
projecte o mètrica surt d'aquí. No inventis res que no hi sigui i no arrodoneixis xifres.

Si aquests dos fitxers i el que has escrit tu es contradiuen, manen ells.

---

## 1. Persona i perfil tècnic

Rafel Cirer-Sastre. Professor Titular de Cinesiologia a l'INEFC Lleida (UdL), plaça
obtinguda el 2026. Doctor internacional per la UdL (2020). Cap de Projecte de Suport a la
Recerca i Transferència del Coneixement a l'INEFC Lleida des del 2022.

ORCID: 0000-0001-6687-8201 · Scopus: 57194537687 · Researcher ID: G-4163-2015

**Forma canònica de signatura: Rafel Cirer-Sastre.** Usa-la sempre, a tot arreu.

Perfil tècnic: estadístic. Treballa amb R i Python. **No és desenvolupador web**: no
coneix JavaScript, CSS ni les convencions del front-end. Escriu i explica en conseqüència.

---

## 2. Objectiu del lloc

Web personal acadèmica amb dos objectius:

1. Marca personal i visibilitat com a investigador — captar doctorands, col·laboradors
   i lectors.
2. Recollir recursos docents i material metodològic obert.

Serà l'adreça canònica a la qual apuntarà la fitxa institucional de gencat.

---

## 3. Stack i restriccions tècniques

- **Quarto** com a generador del lloc (fitxers `.qmd`).
- **GitHub Pages** com a allotjament. Fase inicial: `quarto publish gh-pages` des de
  local. GitHub Actions més endavant.
- **cdmon** només com a registrador i gestor de DNS. Dominis registrats:
  **rafelcirer.com** i **rafelcirer.cat**. Encara no s'ha decidit quin serà el canònic;
  l'altre haurà de redirigir-hi.
- Compte de GitHub: **rcirer** (github.com/rcirer). Autenticació per clau SSH ed25519.
- Scripts auxiliars en **R o Python**, indistintament.

Restriccions sense excepció:

- Cap dependència de JavaScript, framework o eina de build que ell no pugui mantenir.
  Si una solució requereix npm, justifica-ho **abans** de proposar-la.
- Res de WordPress, Hugo, Jekyll ni cap CMS.
- Davant de dues solucions, guanya sempre la que ell pugui entendre i reparar sol
  d'aquí a un any, encara que sigui més pobra.

---

## 4. Marc estratègic — el fil conductor

El lloc no documenta el passat; construeix la línia que ara lidera.

Idea unificadora: **com mesurem el que l'exercici fa al cos i què en podem concloure de
veritat.** Tres línies:

- **Com respon** — troponina cardíaca i biomarcadors després de l'exercici, amb èmfasi en
  poblacions joves. Línia consolidada, derivada de la tesi.
- **Com el mesurem** — validació de tests de camp en resistència: FTP, VO2max, potència en
  ciclisme. La línia amb més lectures i més audiència aplicada.
- **Com s'adapta** — força, mecànica muscular i rang d'excursió. Projecte **EXCURSE**
  (2025–2028), del qual és IP. Línia de futur, i la que encaixa amb la plaça.

Transversal a les tres: **bioestadística aplicada** — modelatge del curs temporal,
regressió bayesiana, revisió sistemàtica i meta-anàlisi. No és una quarta línia: és el
mètode, i és el que explica la col·laboració amb l'IRBLleida en assaigs clínics.

Qualsevol text de presentació parteix d'aquest marc.

---

## 5. Arquitectura del lloc

- **Inici** — qui sóc en tres frases, la frase unificadora, enllaços.
- **Recerca** — les tres línies explicades per a humans, no la llista de papers.
- **Publicacions** — generada automàticament, amb filtre per any.
- **Blog** — posts metodològics i *behind the paper*.
- **Docència** — recursos oberts per assignatura o tema. Navegació pròpia, separada del
  blog: qui ve a buscar apunts no és qui ve a veure qui sóc.
- **Doctorat** — què busca en un doctorand i sobre què es pot treballar. Penja d'EXCURSE,
  que és on hi ha projecte, calendari i infraestructura.
- **CV / Contacte.**

### Idiomes

Sense duplicar contingut i sense maquinària multilingüe:

- **Anglès per defecte**, navegació inclosa. El públic objectiu són doctorands i
  col·laboradors internacionals.
- **Docència (`teaching.qmd`) és l'única excepció i va en català**, perquè el seu públic
  són els estudiants d'aquí. Duu un avís en anglès al capdamunt que ho explica.

Els noms de fitxer són URL públiques i han de ser en anglès i estables
(`phd.qmd`, `teaching.qmd`...). Renombrar-los un cop publicats trenca enllaços externs.

---

## 6. Pipeline de publicacions

Decisions preses. No les replantegis si ell no te les qüestiona.

- **Font de veritat: ORCID**, amb auto-updates de Crossref i DataCite activades.
- **Lectura tècnica: OpenAlex**, filtrant per ORCID, sense token.
- **Recuperació sempre per ORCID, mai per nom.** Signa de formes diferents
  (`Cirer-Sastre, R.`, `Cirer Sastre, R.`) i en almenys un article publicat hi apareix com
  a "Rafael" per error tipogràfic. La cerca per nom fallarà.
- **Capa manual d'excepcions**: `extres.yml` per al que les API no veuen, `exclusions.yml`
  per a duplicats i falsos positius.
- **Automatisme**: GitHub Action mensual que, si detecta canvis, obre un *Pull Request*.
  Mai commit directe.

Volum actual (2026-01-11): 40 publicacions indexades, 331 citacions, h-index 10.

El CV original conté errors coneguts (títols, anys, DOI absents, camps intercanviats);
són a l'apartat final de `cv-extracte-web.md` i són un argument a favor d'alimentar la web
des d'ORCID en comptes de mantenir la llista a mà. No els repropaguis.

---

## 7. Regles de contingut

### Blog

- **No generis un post per article.** Un resum d'IA de cada paper sona buit i no aporta res
  que el DOI no doni ja. Objectiu: 8–12 posts sobre els articles que importen, més posts
  metodològics de manera continuada.
- El contingut valuós és el que no surt publicat: per què es va fer l'estudi, què va
  sorprendre, quina decisió metodològica va costar, què faria diferent avui.
- Els **posts metodològics** tenen més abast que els posts sobre articles propis. Serveixen
  alhora la marca personal i el material docent.
- El teu paper és estructurar, retallar i polir esborranys **seus**. No escriure'ls de zero.
- Extensió orientativa: 600–900 paraules.

### Veu

- Primera persona del singular. És un lloc personal.
- Directe, concret, sense hipèrbole. És metodòleg: les afirmacions van calibrades i la
  incertesa es diu.
- Res de prosa d'IA: sense frases de farciment, sense entusiasme genèric, sense tricolons
  decoratius.

### Llicències i drets

- **No pengis mai PDFs d'editorial.** Enllaça el DOI; si cal text complet, la versió
  acceptada al repositori institucional (repositori.udl.cat) o la versió en accés obert.
- Material docent amb llicència explícita (CC BY-NC-SA per defecte).

---

## 8. Prohibicions

No admeten excepció.

- **Cap dada personal identificativa al repositori ni al lloc**: DNI, adreça postal, data
  de naixement, telèfon privat.
- El **CV normalitzat d'AQU no pot entrar mai al repositori**, ni tan sols temporalment:
  git en conserva l'historial per sempre. `cv-extracte-web.md` sí que hi pot ser — és
  l'extracte ja depurat d'aquestes dades.
- El repositori porta un `.gitignore` amb `*.pdf` des del primer commit.
- **L'adreça de contacte s'escriu desglossada** (`rcirer *at* gencat *dot* cat`), mai com
  a `mailto:` ni en text pla. És deliberat, per dificultar els recol·lectors de correu.
  No ho «arreglis» convertint-ho en un enllaç clicable.
- El CV públic del web serà un document diferent, sense dades identificatives.

---

## 9. Com treballar amb ell

- **Explica què fa cada comanda** abans que l'executi. No dona per fet res del flux de git
  ni de desplegament.
- **Fitxers complets, no fragments.** Si canvia un fitxer, dóna'l sencer o digues
  exactament quina línia substituir.
- **Una decisió tècnica alhora.** Si una tasca en requereix diverses, llista-les i comenceu
  per la primera.
- **Digues-li quan una idea seva és dolenta.** Vol mentoratge, no aprovació. Si el que
  demana li costarà manteniment o farà mal efecte, digues-ho abans de fer-ho.
- Si una cosa depèn d'una decisió que encara no ha pres, atura't i pregunta.

---

## 9 bis. Condicions del doctorat (EXCURSE)

Fets confirmats per en Rafel. Són la base de `phd.qmd`; no els suavitzis ni els ampliïs.

- **No hi ha contracte predoctoral atorgat.** EXCURSE té finançament de despeses de
  recerca, però la beca l'ha de demanar i guanyar el candidat en convocatòria competitiva
  (AGAUR/FI, FPU, o equivalent del seu país). Dir-ho clar: és una plaça per la qual competir,
  no una plaça concedida.
- Hi caben **2 o 3 doctorands**.
- Inici previst: **finals del 2026**.
- Requisit: **màster oficial** (accés al programa de doctorat de la UdL).
- **Presencialitat obligatòria** a la facultat de Lleida.
- Hi ha **docència associada**.
- Procés: **primer parlar amb en Rafel**, abans de cap tràmit formal.

Pendent: qui codirigeix les tesis. EXCURSE el co-lidera Xavier Peirau Terès, però no està
confirmat que codirigeixi.

## 9 ter. Decisions tancades

Descartades per en Rafel el 3 d'agost de 2026, després d'una auditoria externa que les
recomanava. **No les tornis a proposar** si no és ell qui les replanteja.

- **Cap secció «Collaborate»** ni recorreguts de navegació per públic (estudiants /
  col·laboradors). L'arquitectura es queda temàtica.
- **El correu no es fa clicable.** Es queda desglossat (`rcirer *at* gencat *dot* cat`).
  L'argument que l'ofuscació afegeix fricció és cert i ell l'ha sospesat: prefereix la
  fricció abans que el correu brossa.
- **Cap llista de «publicacions seleccionades»** ni categories temàtiques. Surten totes,
  amb filtre per any i prou. Trair-ne unes quantes a mà xoca amb la secció 6.
- **Cap CV en PDF**, ni curt ni llarg. La regla `*.pdf` del `.gitignore` es manté.

## 9 quater. Infografies docents

Projecte obert el 3 d'agost de 2026. Idea d'en Rafel: **diagrames i infografies docents,
cadascun a la seva pàgina, a pantalla completa i sense menú**, oberts en finestra nova i
llistats des de Docència. Serveixen per a les seves classes i com a recurs obert.

Primera: el diagrama del rang d'excursió muscular (MER), que ja existeix a
`images/excursion-range.svg`. Servirà per fixar el motlle.

Temes previstos: cadenes cinètiques, rols musculars (agonista, antagonista, sinergista,
estabilitzador).

**Referència que el va inspirar**: <https://rpsychologist.com/cohend/>, de Kristoffer
Magnusson. Visualització interactiva de la d de Cohen amb control lliscant, distribucions
que es recalculen en directe, mode fosc i preferències desades al navegador. **És una
aplicació de JavaScript**, no un SVG. Val la pena fixar-se també en com separa les
llicències: codi amb MIT, visualització amb CC0, text amb CC BY 4.0.

**Conseqüència que no s'ha de perdre de vista:** aquell nivell d'interactivitat entra en
conflicte amb la secció 3 (res de dependències de JavaScript ni eines de build). Abans de
construir res interactiu, cal decidir la via i justificar-la amb ell.

**Decisió d'arquitectura ja presa**: aquestes pàgines **no seran pàgines del lloc Quarto**.
Seran fitxers autònoms dins `diagrames/`, per no dependre de la plantilla del web ni haver
d'amagar-li el menú amb CSS, cosa que es trencaria a la primera actualització de Quarto.

**Analítica**: pendent. L'opció recomanada és GoatCounter (gratuït, sense galetes, sense
retenir IP ni User-Agent, només agregats). No s'instal·la fins que en Rafel ho consulti amb
el delegat de protecció de dades de la UdL. Per distingir canals, enllaços amb paràmetre
(`?d=cinesiologia`) en comptes de dades demogràfiques.

## 10. Decisions obertes

Pendents. Recorda-les-hi quan siguin rellevants per a la tasca en curs.

- Quin dels dos dominis serà el canònic: rafelcirer.com o rafelcirer.cat. GitHub Pages
  només admet un domini personalitzat per repositori; el segon ha de redirigir des del
  DNS o des del registrador.
- Si té o no perfil de Google Scholar (cal crear-lo si no).
- Si val la pena moure el DNS a Cloudflare per resoldre la redirecció del segon domini.
- Text definitiu de la fitxa de gencat i verificació que l'enllaç al domini hi és a les
  tres versions (ca/es/en).

---

## 11. Estat actual del projecte

Fet:

- Repositori git local a `/Users/rcirer/Projects/rafelcirer`, branca `main`.
- Remot `origin` → `git@github.com:rcirer/rcirer.github.io.git` (públic), per SSH.
- `.gitignore` amb `*.pdf` present des del primer commit.

- Lloc Quarto amb set pàgines, **publicat i viu a https://rcirer.github.io**.
- Publicació amb `quarto publish gh-pages`. La branca `gh-pages` conté només l'HTML;
  `main` conté el codi font. GitHub Pages serveix des de `gh-pages`, arrel.

- Capa de disseny pròpia a `theme.scss`. Un sol fitxer, sense npm ni build.
- Esquema d'EXCURSE a `images/excursion-range.svg`, generat per
  `scripts/excursion-range.py`. No l'editis a mà.
- Pipeline de publicacions: `scripts/publications.py` llegeix ORCID, enriqueix amb
  OpenAlex i Crossref, aplica `exclusions.yml` i `extres.yml`, i escriu
  `publications.yml`. 40 publicacions. Executa'l amb `python3 scripts/publications.py`.

Pendent, en aquest ordre:

1. GitHub Action mensual que executi l'script i obri un *pull request* si hi ha canvis.
2. Retrat d'en Rafel per a la portada. Mentrestant hi ha una foto d'estoc d'una aula.
3. Primer post del blog, a partir de `blog/posts/_llavor-troponina.qmd`.
4. Traducció al català sota `/ca/`, quan el text anglès estigui tancat.
5. Domini personalitzat (secció 10).

**Sobre ORCID i `extres.yml`.** Les entrades d'ORCID importades automàticament de Web of
Science pertanyen a aquella font i en Rafel **no les pot editar**. Si a WoS hi falta el
DOI, a ORCID hi faltarà sempre. Per tant `extres.yml` no és una llista de coses pendents
d'arreglar: per a aquests casos és la solució definitiva. No li proposis "arreglar-ho a
l'origen" quan l'origen és WoS.

Tres entrades permanents: la meta-anàlisi contralateral de 2017 (J Sports Sci Med no
diposita DOI, i a ORCID hi consta cinc vegades sense poder-se fusionar), l'article d'IL-6
i el de water polo.

No facis cap d'aquests passos sense demanar-ho: van d'una decisió en una.

**Avís après per experiència:** no facis `git add -A` sense mirar abans què s'hi afegeix.
L'editor d'en Rafel pot re-desar fitxers que acabes de renombrar, i un `add -A` cec els
reintrodueix. Va passar amb `doctorat.qmd`, que hauria publicat text ja retirat.
