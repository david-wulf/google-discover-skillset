# Google Discover Skillset

Claude-Code-Plugin mit acht Skills. Sieben davon decken Google Discover über alle Ebenen ab, einer
prüft Textqualität kanalunabhängig. Alle arbeiten mit dokumentierter Rubrik, Punkten pro
Unterkriterium und Belegpflicht: jeder Befund zitiert die Textstelle oder benennt einen gemessenen
Wert.

## Die acht Skills

| Skill | Ebene | Ergebnis |
|-------|-------|----------|
| **discover-gesamtaudit** | Orchestrierung | Ruft die fünf Discover-Skills in der richtigen Reihenfolge auf, bricht bei Zulassungs-Blockern früh ab und fasst alles zu **einem** Bericht mit Stationsdiagnose zusammen |
| **discover-readiness-domain** | Domain | Zulassung, Discover-Traffic **nach Verzeichnis**, Bild-Config, E-E-A-T, technische Signale · Readiness Score 0–100 |
| **discover-readiness-artikel** | veröffentlichte URL | OG-Vollständigkeit, Schema und Parsing-Priorität, News-Sitemap, Startseiten-Prominenz, Blocker-Tags |
| **discover-content-optimizer** | Artikeltext | Entitäten-Abdeckung und -Integration, semantische Lücken, JSON-LD, Keywords · Content Score 0–100 |
| **discover-headline** | `og:title` | pCTR-Modell aus acht gewichteten Dimensionen, Clickbait-Abzug, Variantenvergleich mit Delta |
| **discover-titelbild** | Titelbild | Spezifikationsprüfung plus Rendering auf echte Kartengröße 340 × 190 und 80 × 80 · Karten-Score 0–100 |
| **discover-ctr-optimierung** | gemessene CTR | Holt den CTR-Verlauf aus der GSC, prüft **statistisch** ob die Lücke echt ist, bestimmt den Engpass und baut einen belastbaren Messplan |
| **content-checker** | Textqualität | 12 Qualitätskriterien: KI-Muster, fehlende Tiefe, Answer-First, Überschriften. **Kanalunabhängig** — sagt nichts über Discover |

### Warum die Reihenfolge zählt

Es ist sinnlos, Headline und Bild zu optimieren, wenn die Domain im betroffenen Verzeichnis gar
nicht discover-fähig ist. Genau das passiert in der Praxis regelmäßig. Deshalb prüft
`discover-gesamtaudit` von unten nach oben und bricht ab, wenn eine Vorstufe blockiert:

```
Zulassung  →  Domain-Traffic  →  URL-Technik  →  Artikeltext  →  Headline  →  Titelbild
   ▲                                                  │             │
   └── manuelle Maßnahme, notranslate,                 │             └── liefert den Titel,
       max-image-preview → Abbruch                     └── liefert den      gegen den die Karte
                                                           stärksten Fakt   auf Doppelung prüft
```

Die Einzelscores werden **nicht** zu einer Gesamtnote verrechnet — sie messen Verschiedenes auf
verschiedenen Ebenen. Der Bericht führt sie nebeneinander und benennt den Engpass.

## Installation

```bash
/plugin marketplace add https://github.com/david-wulf/google-discover-skillset
```

Danach in der Plugin-Übersicht `google-discover-skillset` installieren.

Alternativ ohne Git: die Ordner unter `skills/` nach `~/.claude/skills/` kopieren.

**Voraussetzungen**

| Skill | Braucht |
|-------|---------|
| discover-content-optimizer, discover-headline, discover-ctr-optimierung | Python 3.8+ (nur Standardbibliothek) |
| discover-titelbild | Python 3.8+ **und Pillow** (`pip install pillow`) |
| discover-readiness-domain, discover-ctr-optimierung | Search-Console-Zugang per MCP für Messdaten; ohne GSC läuft der Rest, arbeitet dann aber prognostisch statt messend |
| alle übrigen | nichts |

Fehlt Python, werden berechnete Werte geschätzt statt gemessen — der Bericht weist das aus.

## Nutzung

```
Mach ein komplettes Discover-Audit für example.de
```

Einzelne Ebenen direkt:

| Anliegen | Formulierung |
|----------|--------------|
| Domain-Check | „Ist example.de Discover-ready?" |
| URL-Technik | „Prüf diesen Artikel für Discover: <url>" |
| Artikeltext | „Prüf diesen Text auf Discover-Tauglichkeit: <Text>" |
| Headline | „Bewerte diese Headline" · „Was wäre eine gute Überschrift für X?" |
| Titelbild | „Prüf das Titelbild dieser URL" · Screenshot einer Feed-Karte |
| CTR | „Warum klickt niemand auf diesen Artikel?“ · „Ist die CTR-Verbesserung signifikant?“ |
| Textqualität | „Content-Check für diesen Artikel“ |

Am Ende wird gefragt, ob zusätzlich ein Word-Bericht, eine Excel-Maßnahmenliste oder ein
HTML-Einseiter erzeugt werden soll. Ohne Auswahl bleibt es beim Bericht im Chat.

## Rechen-Backends

Drei Skills rechnen statt zu schätzen. Direkt aufrufbar:

```bash
python skills/discover-content-optimizer/scripts/textstats.py \
  --text-file artikel.txt --core "Kernentität" --entities "Quelle"
```

Dokumentstatistik, Lesbarkeit (Flesch bzw. Flesch-Amstad), Headline- und Lead-Metriken,
Faktendichte, thematische Kernbegriffe gegen TF-IDF-Spitzen, Trust-Marker, Integrations-Score je
Entität, Kookkurrenzmatrix.

```bash
python skills/discover-headline/scripts/pctr.py features --titles-file titel.txt --entity "Marke"
python skills/discover-headline/scripts/pctr.py score --input bewertung.json
```

`features` misst Länge und Längenband, Zahlen, Ansprache, Autoritäts-, Frische- und
Superlativ-Marker, Clickbait-Lexikon, erkannte Formeln, Position der Kernentität. `score` rechnet
die bewerteten Dimensionen in pCTR um und vergleicht gegen die Baseline.

```bash
python skills/discover-titelbild/scripts/feedcard.py --image <url> --out ansichten
```

Maße, Gesamtfläche, Seitenverhältnis samt Beschnittverlust, Format, Kontrast, Farbigkeit,
Informationsverlust bei Feed-Größe, Auslieferung (HTTPS, Content-Type, Weiterleitung, Ladezeit) —
plus drei gerenderte Ansichten.

```bash
python skills/discover-ctr-optimierung/scripts/ctrstats.py ci --clicks 412 --impressions 8300
python skills/discover-ctr-optimierung/scripts/ctrstats.py compare --before 412/8300 --after 388/6900
python skills/discover-ctr-optimierung/scripts/ctrstats.py power --baseline-ctr 0.062 --uplift-rel 0.15 --impressions-per-day 1200
python skills/discover-ctr-optimierung/scripts/ctrstats.py mde --impressions 8300 --baseline-ctr 0.062
```

Wilson-Konfidenzintervall für die CTR, Zwei-Stichproben-z-Test für Vorher-Nachher,
benötigte Impressionen für einen angestrebten Uplift und der kleinste bei gegebenem
Volumen überhaupt nachweisbare Effekt.

**Warum das nötig ist:** Eine CTR-Änderung von 6,25 % auf 6,75 % ist selbst bei 16.000
Impressionen noch nicht signifikant (p ≈ 0,07). Bei 8.300 Impressionen sind nur Verbesserungen
ab rund 18 % relativ nachweisbar. Und um +15 % zu belegen, braucht man bei 1.200 Impressionen pro
Tag zehn Tage pro Variante — das Freshness-Fenster ist aber sieben Tage lang. Sequenzielles
Messen an einem einzelnen Artikel ist damit strukturell nicht saubermachbar; der Skill schlägt
deshalb einen Portfolio-Test über eine Artikelgruppe im gleichen Zeitfenster vor.

## Was bewusst anders ist als bei den Vorlagen

Die drei neu gebauten Skills orientieren sich an den Tools von metehan.ai, weichen aber ab:

1. **Der Ist-Zustand wird bewertet.** Original-Headline und vorhandenes Bild bekommen einen Score,
   bevor Alternativen entstehen. Sonst ist nicht messbar, ob eine Alternative besser ist.
2. **Kalibrierte Scores.** Anti-Inflations-Regeln erzwingen Spreizung. Im Test des Originals lagen
   alle Headline-Varianten eines inhaltsleeren Textes bei 87–92 von 100, die höchste Note ging an
   die generischste Variante.
3. **Integrations-Score statt Embedding-Heatmap.** Cosine-Ähnlichkeit von Entitäts-Embeddings misst
   Modellähnlichkeit, nicht Textqualität — solche Matrizen liegen praktisch immer im Band 0,8–1,0.
   Stattdessen wird berechnet, ob *dieser Text* die Entität einbindet.
4. **Das Bild wird in Kartengröße geprüft**, nicht in Originalgröße.
5. **Clickbait-Veto außerhalb der Formel.** Der β-Abzug des pCTR-Modells kappt maximal 35 %; ein
   maximal manipulativer Titel erreicht damit noch das Band „top". Ab `clickbait_score` 6 wird eine
   Variante deshalb nicht empfohlen, und das wird ausgewiesen.

Zwei der drei Vorlagen waren beim Nachbau nicht funktionsfähig. Details in
`skills/discover-readiness-artikel/references/external-tools.md`.

## Grenzen

- **Keine Keyword- oder Themenrecherche.** Die Skills prüfen vorhandene Artikel.
- **Keine CTR-Prognose.** Kein Score sagt, welche CTR erreicht wird. Zur Einordnung: News-Seiten
  rund 11 %, Non-News rund 6 %, Arbeitsziel 7–9 %, unter 5 % Handlungssignal *(GSC-Auswertung über
  11.000 URLs von 62 Domains)*.
- **Keine Lösung für fehlenden Site-Trust.** Ein Verzeichnis ohne thematische Autorität erkennt das
  Audit, löst es aber nicht.
- **Discover ist ein Impuls, keine Basis.** Wer Discover als Grundlast plant, plant falsch.
- **Kein A/B-Test möglich.** Discover liefert keine Varianten aus. Man kann nur ändern
  und beobachten oder Artikelgruppen vergleichen — beides ist nicht randomisiert. Ein
  signifikanter Unterschied belegt eine Veränderung, nicht deren Ursache.
- **Evidenzstufen mitführen:** Kriterien sind als [Doku], [Richtlinie], [SDK] oder [Praxis]
  markiert. SDK-Erkenntnisse sind Client-Sicht zu einem Zeitpunkt — starkes Indiz, keine
  Spezifikation. Praxis-Heuristiken (News-Sitemap, Startseiten-Prominenz, Article-Schema,
  Republishing) stehen **nicht** in Googles Doku und dürfen im Kundenbericht nicht als
  „Google verlangt" auftreten.

## Aufbau

```
.claude-plugin/plugin.json          Plugin-Manifest
.claude-plugin/marketplace.json     Marketplace-Eintrag
skills/discover-gesamtaudit/        Orchestrierung über alle Ebenen
skills/discover-readiness-domain/       + references/discover-mechanik.md
skills/discover-readiness-artikel/ + references/discover-kriterien.md, external-tools.md
skills/discover-content-optimizer/  + scripts/textstats.py, 4 references, HTML-Template
skills/discover-headline/           + scripts/pctr.py, references/dimensionen.md, formeln.md
skills/discover-titelbild/          + scripts/feedcard.py, references/kartenrubrik.md
skills/discover-ctr-optimierung/    + scripts/ctrstats.py
skills/content-checker/             Textqualität, kanalunabhängig
examples/                           drei vollständige Beispielberichte
tests/                              Beispieltexte und Testprotokoll
```
