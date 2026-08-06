# Discover Content Optimizer

Claude-Code-Plugin für die semantische Analyse von Artikeltexten mit Blick auf **Google
Discover** und **AI-Sichtbarkeit**. Prüft nicht, ob ein Text gut geschrieben ist, sondern ob
Google ihn einem Thema, einer Entität und einem Nutzerinteresse zweifelsfrei zuordnen kann.

Ergebnis: ein **Discover Content Score 0–100** nach dokumentierter Rubrik, ein priorisierter
Maßnahmenplan mit Aufwand und erwarteter Score-Wirkung, und fertige Textbausteine zum Einsetzen.

## Installation

```bash
/plugin marketplace add https://<git-host>/<pfad>/discover-content-optimizer
```

Danach in der Plugin-Übersicht `discover-content-optimizer` installieren.

Alternativ ohne Git: den Ordner `skills/discover-content-optimizer` nach
`~/.claude/skills/` kopieren.

**Voraussetzung:** Python 3.8+ im PATH für das Rechen-Backend (nur Standardbibliothek, keine
Pakete). Ohne Python läuft die Analyse weiter, aber Struktur- und Integrationswerte werden
geschätzt statt berechnet — der Bericht weist das dann aus.

## Nutzung

Text einfügen und eine Analyse anfordern:

```
Prüf diesen Artikel auf Discover-Tauglichkeit:
<Text, erste Zeile = Headline>
```

Auch möglich: URL statt Text, plus optional ein Wettbewerbertext für die Gap-Analyse.

Der Skill fragt nach dem Domain-Profil, wenn es nicht aus dem Text hervorgeht:
Technologie · Gesundheit · Finanzen · Bildung · E-Commerce · News · Flash News · Allgemein.
Das Profil steuert, welche Entitäten erwartet und welche Vertrauenssignale gewichtet werden.

Am Ende wird gefragt, ob zusätzlich ein Word-Bericht, eine Excel-Maßnahmenliste oder ein
HTML-Einseiter erzeugt werden soll. Ohne Auswahl bleibt es beim Bericht im Chat.

## Was analysiert wird

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

## Was der Skill bewusst anders macht

Der Skill orientiert sich am Funktionsumfang des *Advanced Google Discover Optimizer* von
metehan.ai, weicht aber an drei Stellen ab:

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

## Grenzen

- Analysiert **Text**. Bildwirkung, `og:image`-Maße, `max-image-preview`, News-Sitemap und
  Startseiten-Prominenz sind nicht Teil davon.
- „Fehlende Entitäten" sind ohne SERP-Daten eine begründete Vermutung, keine Messung. Sind
  SERP-MCPs verfügbar (DataForSEO, Ahrefs, SurferSEO), wird der Erwartungsraum aus real
  rankenden Seiten gebildet und das im Bericht ausgewiesen.
- Headline-Scores sind Rubrik-Werte, keine CTR-Prognose.
- Der Score sagt nichts über Domain-Autorität, Site-Trust oder Publisher-Status — die
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
tests/                              Beispieltexte für Kalibrierungsprüfungen
```

## Rechen-Backend direkt aufrufen

```bash
python skills/discover-content-optimizer/scripts/textstats.py \
  --text-file artikel.txt --entities "Entität A,Entität B"
```

Liefert JSON: Dokumentstatistik, Lesbarkeit (Flesch bzw. Flesch-Amstad), Headline- und
Lead-Metriken, Faktendichte, thematische Kernbegriffe und TF-IDF-Spitzen, Trust-Marker,
pro Entität Integrations-Score, Kookkurrenzmatrix.
