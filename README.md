# Discover Content Optimizer

Claude-Code-Plugin mit zwei Skills für **Google Discover** und **AI-Sichtbarkeit**. Zusammen
decken sie die beiden Hebel ab, die im Feed über den Klick entscheiden: den Text und die Karte.

| Skill | Prüft | Ergebnis |
|-------|-------|----------|
| **discover-content-optimizer** | den **Artikeltext**: kann Google ihn einem Thema, einer Entität und einem Nutzerinteresse zweifelsfrei zuordnen? | Discover Content Score 0–100, Maßnahmenplan, fertige Textbausteine, JSON-LD |
| **discover-feedkarte** | die **Feed-Karte**: Titelbild und Headline als Einheit, gerendert auf echte Kartengröße | Feed-Karten-Score 0–100, Tabelle „was in welcher Größe verschwindet", Bildaufträge |

Beide arbeiten mit dokumentierter Rubrik, Punkten pro Unterkriterium und Belegpflicht: jeder
Befund zitiert die Textstelle oder benennt, was in welcher Bildansicht sichtbar ist.

## Installation

```bash
/plugin marketplace add https://<git-host>/<pfad>/discover-content-optimizer
```

Danach in der Plugin-Übersicht `discover-content-optimizer` installieren.

Alternativ ohne Git: die Ordner unter `skills/` nach `~/.claude/skills/` kopieren.

**Voraussetzungen**

| Skill | Braucht |
|-------|---------|
| discover-content-optimizer | Python 3.8+ (nur Standardbibliothek). Fehlt Python, werden Struktur- und Integrationswerte geschätzt statt berechnet — der Bericht weist das aus |
| discover-feedkarte | Python 3.8+ **und Pillow** (`pip install pillow`). Ohne Pillow entfällt der Kartengrößen-Test; der Score wird entsprechend gedeckelt statt geschätzt |

## Nutzung

**Text prüfen:**

```
Prüf diesen Artikel auf Discover-Tauglichkeit:
<Text, erste Zeile = Headline>
```

Auch möglich: URL statt Text, plus optional ein Wettbewerbertext für die Gap-Analyse. Der Skill
fragt nach dem Domain-Profil, wenn es nicht aus dem Text hervorgeht: Technologie · Gesundheit ·
Finanzen · Bildung · E-Commerce · News · Flash News · Allgemein. Das Profil steuert, welche
Entitäten erwartet und welche Vertrauenssignale gewichtet werden.

**Feed-Karte prüfen:**

```
Prüf das Titelbild dieser URL für Discover: <url>
```

Ebenfalls möglich: Bilddatei plus Headline, oder ein Screenshot einer Discover-Karte — dann
braucht es keinen Seitenzugriff und keine Paywall-Umgehung.

In beiden Fällen wird am Ende gefragt, ob zusätzlich ein Word-Bericht, eine Excel-Maßnahmenliste
oder ein HTML-Einseiter erzeugt werden soll. Ohne Auswahl bleibt es beim Bericht im Chat.

## Skill 1: discover-content-optimizer — was analysiert wird

| Modul | Inhalt |
|-------|--------|
| 1 Entitäten | Entitäten nach Typ, explizite Beziehungen, fehlende Entitäten mit Priorität und Einbauort |
| 2 Content | Original-Headline bewertet, 5 Varianten mit je eigener Formel, semantische Anreicherung, Topic-Cluster, Struktur, interne Verlinkung, Wettbewerbs-Gap |
| 3 Schema | JSON-LD generiert (inkl. `about[]`/`mentions`/`sameAs`) und in vier Blöcken validiert |
| 4 Keywords | thematische Kernbegriffe vs. TF-IDF-Spitzen, primär/sekundär, Cluster, Platzierung, Long-Tail |
| 5 Semantik | Entitäten-Integrationsmatrix, Kookkurrenz, fehlende semantische Konzepte mit Relevanz |

### Score

| Dimension | Punkte |
|-----------|--------|
| Entitäten-Abdeckung und -Tiefe | 25 |
| Headline und Einstieg | 20 |
| Semantische Vollständigkeit | 20 |
| Struktur und Lesbarkeit | 15 |
| Vertrauen und Maschinenlesbarkeit | 20 |

Bänder: 85–100 Discover-ready · 70–84 solide · 55–69 mittel · 40–54 schwach · <40 nicht
Discover-fähig. Deckel verhindern Schönfärberei: ohne Entitätenabdeckung ist bei 65 Schluss,
ohne benannte Quelle und ohne Faktendichte bei 55.

Die vollständige Rubrik steht in `skills/discover-content-optimizer/references/scoring.md`
und wird im Bericht mit Punkten pro Unterkriterium offengelegt.

## Skill 2: discover-feedkarte — das Bild dort prüfen, wo es wirkt

Im Feed konkurriert kein Artikel, sondern eine Karte von rund 340 × 190 Punkten, wahrgenommen im
Scrollen. Ein Titelbild, das in Originalgröße überzeugt, kann dort vollständig versagen. Der Skill
misst das Bild und **rendert es auf die echten Kartengrößen**, bevor er urteilt:

| Ansicht | Wofür |
|---------|-------|
| 340 × 190 | die große Feed-Karte — Hauptbewertungsgrundlage |
| 80 × 80 | kompakte Listenansicht — zeigt, was ein quadratischer Beschnitt zerstört |
| 16:9-Beschnitt | zeigt bei abweichendem Seitenverhältnis, was wegfällt |

Gemessen werden Breite, Seitenverhältnis samt Beschnittverlust, Format und Dateigröße,
Helligkeit, RMS-Kontrast, ausgebrannte Flächen, Farbigkeit nach Hasler-Süsstrunk und der
Informationsverlust bei Feed-Größe. Visuell beurteilt werden Erkennbarkeit der Kern-Entität,
Bildsprache, Schriftlesbarkeit, Wirkung des Beschnitts und das Markenverhältnis.

| Dimension | Punkte |
|-----------|-------:|
| Technische Auslieferbarkeit | 25 |
| Bildaussage | 30 |
| Tauglichkeit bei Kartengröße | 25 |
| Zusammenspiel mit der Headline | 20 |

Deckel: unter 1200 px Breite ist bei 55 Schluss, ohne `max-image-preview:large` bei 60, und wenn
die Kern-Entität im Bild nicht erkennbar ist bei 50.

Der wichtigste Ausgabeteil ist die Tabelle **„was in welcher Größe verschwindet"** — Element für
Element, in welcher Ansicht es noch sichtbar ist. Beispiel aus
[examples/beispielbericht-feedkarte.md](examples/beispielbericht-feedkarte.md): bei einem
technisch einwandfreien 1600 × 900-Bild fallen im quadratischen Beschnitt Logo und Markenblock
komplett weg, übrig bleibt das Fragment „000 WATT".

## Was die Skills bewusst anders machen

Sie orientieren sich am Funktionsumfang des *Advanced Google Discover Optimizer* von
metehan.ai, weichen aber an vier Stellen ab:

1. **Der Ist-Zustand wird bewertet.** Die Original-Headline bekommt einen Score, bevor
   Alternativen entstehen. Sonst ist nicht messbar, ob eine Alternative besser ist.
2. **Kalibrierte Scores.** Anti-Inflations-Regeln erzwingen Spreizung: höchstens eine
   Headline-Variante darf ≥ 9,0 erreichen, eine Headline ohne Zahl oder Eigennamen kommt nie
   über 6,0. Ein Score, bei dem alles gut ist, ist wertlos.
3. **Integrations-Score statt Embedding-Heatmap.** Eine Cosine-Matrix über
   Entitäts-Embeddings misst Modellähnlichkeit — „CPU" und „GPU" sind sich immer ähnlich,
   unabhängig vom Artikel; solche Matrizen liegen praktisch immer im Band 0,8–1,0 und
   unterscheiden nichts. Stattdessen wird berechnet, ob *dieser Text* die Entität einbindet:
   Häufigkeit, Absatz-Spread, Ko-Vorkommen mit anderen Entitäten, Definitions-, Vergleichs-
   und Kausalmarker, Faktendichte im Umfeld. Reproduzierbar, ohne API und ohne Kosten.
4. **Das Bild wird in Kartengröße geprüft.** Das metehan-Tool
   *image-to-google-discover* trägt „image" im Namen, nimmt einen Screenshot aber nur als
   Eingabeformat und prüft nirgends Bildbreite, Beschnitt, Kontrast oder Lesbarkeit als
   Thumbnail. `discover-feedkarte` rendert das Bild auf 340 × 190 und 80 × 80 und beurteilt es
   dort — die Größe, in der es tatsächlich wahrgenommen wird.

## Grenzen

- Der Textskill analysiert **Text**, der Kartenskill **Bild und Headline**. News-Sitemap,
  OG-Vollständigkeit und Startseiten-Prominenz sind in keinem von beiden.
- „Fehlende Entitäten" sind ohne SERP-Daten eine begründete Vermutung, keine Messung. Sind
  SERP-MCPs verfügbar (DataForSEO, Ahrefs, SurferSEO), wird der Erwartungsraum aus real
  rankenden Seiten gebildet und das im Bericht ausgewiesen.
- Beide Scores sind Rubrik-Werte, keine CTR-Prognose.
- Die Kartenmaße 340 × 190 und 80 × 80 sind Größenordnungen der ausgelieferten Karten, keine von
  Google dokumentierten Spezifikationen. „Bei dieser Größe verschwindet X" ist belastbar; „genau
  so sieht die Karte bei jedem Nutzer aus" nicht.
- Kein Score sagt etwas über Domain-Autorität, Site-Trust oder Publisher-Status — die
  entscheiden vor jeder Content-Qualität über Discover-Eligibility.

## Aufbau

```
.claude-plugin/plugin.json          Plugin-Manifest
.claude-plugin/marketplace.json     Marketplace-Eintrag
skills/discover-content-optimizer/
  SKILL.md                          Ablauf, Grundregeln, Ausgabeformat
  scripts/textstats.py              Rechen-Backend (stdlib-only)
  references/module-analysen.md     Module 1–5, Ausgabeverträge, Metrik-Referenz
  references/scoring.md             Score- und Headline-Rubrik, Anti-Inflation
  references/domains.md             8 Domain-Profile
  references/discover-mechanik.md   Begründungsbasis, Headline-Formeln
  assets/report-template.html       HTML-Einseiter
skills/discover-feedkarte/
  SKILL.md                          Ablauf, drei Eingabewege, Bewertung an den Ansichten
  scripts/feedcard.py               Mess- und Render-Backend (braucht Pillow)
  references/kartenrubrik.md        Feed-Karten-Rubrik, Deckel, Bänder
examples/                           zwei vollständige Beispielberichte
tests/                              Beispieltexte und Testprotokoll
```

## Backends direkt aufrufen

```bash
python skills/discover-content-optimizer/scripts/textstats.py \
  --text-file artikel.txt --core "Kernentität A" --entities "Quelle B"
```

Liefert JSON: Dokumentstatistik, Lesbarkeit (Flesch bzw. Flesch-Amstad), Headline- und
Lead-Metriken, Faktendichte, thematische Kernbegriffe und TF-IDF-Spitzen, Trust-Marker,
pro Entität Integrations-Score, Kookkurrenzmatrix.

```bash
python skills/discover-feedkarte/scripts/feedcard.py \
  --image https://example.com/titelbild.jpg --out ansichten
```

Liefert JSON mit Maßen, Seitenverhältnis und Beschnittverlust, Format, Helligkeit, RMS-Kontrast,
Farbigkeit, Informationsverlust bei Feed-Größe und automatischen Hinweisen — plus die drei
gerenderten Ansichten im angegebenen Verzeichnis.
