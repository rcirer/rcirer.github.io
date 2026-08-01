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

Pendent, en aquest ordre:

1. Esquelet del projecte Quarto (`_quarto.yml` i pàgines mínimes).
2. Primera publicació a GitHub Pages i comprovació a `https://rcirer.github.io`.
3. Pipeline de publicacions des d'ORCID/OpenAlex (secció 6).
4. Domini personalitzat (secció 10).

No facis cap d'aquests passos sense demanar-ho: van d'una decisió en una.
