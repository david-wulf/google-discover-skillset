---
name: discover-content-optimizer
description: >
  Semantische Tiefenanalyse eines Artikeltexts für Google Discover und AI-Sichtbarkeit —
  fünf Module: Entitäten (vorhanden, Beziehungen, fehlend), Content-Optimierung (Headline-Varianten
  mit kalibriertem Score, semantische Anreicherung, Struktur, interne Verlinkung, Wettbewerbs-Gap),
  Schema-Markup (JSON-LD generieren + validieren), Keyword-Analyse (TF-IDF, Cluster, Platzierung,
  Long-Tail) und semantische Abdeckung (Entitäten-Integrationsmatrix, fehlende Konzepte).
  Liefert einen Discover-Readiness-Score 0–100 mit dokumentierter Rubrik und einen Maßnahmenplan.
  Verwende diesen Skill immer, wenn ein Artikeltext, Entwurf oder Manuskript auf Discover-Tauglichkeit,
  Entitäten-Vollständigkeit oder semantische Tiefe geprüft werden soll — auch bei: "Discover-Optimierung",
  "Entitäten prüfen", "welche Entitäten fehlen", "Headline-Varianten", "semantische Lücken",
  "Content-Gap zum Wettbewerber", "Schema für den Artikel", "Discover Content Score",
  "Artikel vor Veröffentlichung prüfen", "Text semantisch optimieren", "Themenabdeckung prüfen",
  "warum wird der Artikel nicht ausgespielt", "entity analysis", "content gap analysis".
  Auch auslösen, wenn nur ein Text mit der Bitte um Discover- oder Semantik-Bewertung eingereicht wird.
  Nicht verwenden für rein technische Prüfungen einer veröffentlichten URL (OG-Tags, Bildgröße,
  News-Sitemap, Startseiten-Prominenz) — dafür ist der Skill discover-artikel-optimierer zuständig.
---

# Discover Content Optimizer

Analysiert den **Text** eines Artikels auf semantische Discover-Tauglichkeit. Die Leitfrage
ist nicht „ist der Text gut geschrieben", sondern: **Kann Google diesen Text einem Thema,
einer Entität und einem Nutzerinteresse zweifelsfrei zuordnen — und ihn dann auch ausspielen?**

## Grundregeln

Diese Regeln gelten in jedem Modul. Sie sind der Unterschied zwischen einem verwertbaren
Bericht und einer Liste generischer Ratschläge.

1. **Belegpflicht.** Jeder Befund zitiert die konkrete Stelle aus dem Text (wörtlich, in
   Anführungszeichen). Ein Befund ohne Zitat wird nicht in den Bericht aufgenommen.
2. **Keine Platzhalter.** Kein „ausstehend", kein „hier könnte …", keine leeren Tabellenzeilen.
   Wenn ein Modul nichts findet, steht das als Ergebnis da („keine isolierten Entitäten").
3. **Kalibrierung vor Freundlichkeit.** Scores müssen diskriminieren. Wenn alle
   Headline-Varianten 8,5+ bekommen, ist die Bewertung wertlos. Siehe `references/scoring.md`,
   Abschnitt „Anti-Inflation".
4. **Der Ist-Zustand wird zuerst bewertet.** Die Original-Headline bekommt einen Score, bevor
   Alternativen entstehen. Sonst ist nicht messbar, ob eine Alternative überhaupt besser ist.
5. **Empfehlungen sind umsetzbar.** „Mehr Kontext ergänzen" ist keine Empfehlung.
   „Nach Absatz 3 zwei Sätze ergänzen, die den Neural Accelerator erklären — Vorschlag: …" ist eine.
6. **Rechnen statt schätzen.** Alles, was `scripts/textstats.py` berechnet, wird nicht geschätzt.

## Ablauf

### Schritt 0 — Eingabe klären

Der Skill braucht drei Dinge. Was nicht geliefert wurde, wird bestimmt oder erfragt:

| Was | Wie |
|-----|-----|
| **Text** | Direkt eingefügt, als Datei, oder aus einer URL extrahiert (WebFetch, sonst Browser + `get_page_text`). Bei URL: nur den Artikelkörper verwenden, keine Navigation/Footer. |
| **Domain** | Aus dem Text ableiten und die Annahme benennen. Profile: Technologie, Gesundheit, Finanzen, Bildung, E-Commerce, News, Flash News, Allgemein — siehe `references/domains.md`. Bei echter Ambiguität einmal fragen. |
| **Zielkeyword / Kernentität** | Aus dem Text ableiten. Wird für Modul 1 und 4 gebraucht. |

Die erste Zeile des Textes wird als Headline behandelt. Wenn unklar ist, ob eine Headline
enthalten ist, nachfragen — die Headline-Bewertung ist ein Fünftel des Scores.

Optional, wenn geliefert: Wettbewerbertext für die Gap-Analyse, Autor/Publisher für das Schema,
URL für `mainEntityOfPage`.

### Schritt 1 — Metriken berechnen (immer zuerst)

```bash
python scripts/textstats.py --text-file <pfad> --entities "Entität A,Entität B,..."
```

Alternativ JSON auf stdin: `{"text": "...", "entities": [...], "lang": "de"}`.

Vorgehen: Skript **zweimal** laufen lassen. Erster Lauf ohne `--entities`, um Dokument-,
Lesbarkeits-, Headline-, Faktendichte- und Keyword-Metriken zu bekommen. Danach Modul 1
(Entitäten extrahieren), dann zweiter Lauf mit der Entitätenliste für Integrations-Score und
Kookkurrenzmatrix.

Wenn Python fehlt: Modul für Modul weiterarbeiten, aber im Bericht unter „Methodik" vermerken,
dass die Struktur- und Integrationswerte geschätzt statt berechnet sind. Nie berechnete Werte
erfinden.

Was das Skript liefert und wie es zu lesen ist, steht in `references/module-analysen.md`,
Abschnitt „Metrik-Referenz".

### Schritt 2 — Die fünf Analysemodule

Alle fünf laufen, in dieser Reihenfolge. Detaillierte Anweisungen und Ausgabeverträge:
`references/module-analysen.md`.

1. **Entitäten** — identifizierte Entitäten nach Typ, Beziehungen, fehlende Entitäten mit
   Begründung und Priorität. Fundament für alles Weitere.
2. **Content-Optimierung** — Original-Headline scoren, 5 Varianten mit unterschiedlichen
   Formeln, semantische Anreicherung, Topic-Cluster, Struktur, interne Verlinkung,
   optional Wettbewerbs-Gap.
3. **Schema-Markup** — JSON-LD für den Artikel generieren (inkl. `about`/`mentions` aus Modul 1)
   und gegen die Discover-relevanten Anforderungen validieren.
4. **Keyword-Analyse** — thematische Kernbegriffe vs. TF-IDF-Spitzen, primäre/sekundäre
   Keywords, semantische Cluster, Platzierungsstrategie, Long-Tail-Varianten.
5. **Semantische Abdeckung** — Entitäten-Integrationsmatrix (welche Entität hängt im Text in
   der Luft), fehlende semantische Konzepte mit Relevanz-Score und Umsetzungsvorschlag.

### Schritt 3 — Score

Der Discover Content Score (0–100) wird nach der Rubrik in `references/scoring.md` gebildet.
Die Rubrik ist verbindlich: Punkte werden pro Kriterium mit Begründung vergeben, nicht
pauschal geschätzt. Im Bericht steht die Punkteverteilung, nicht nur die Summe.

### Schritt 4 — Bericht

Standardformat ist Markdown, direkt in der Antwort und zusätzlich als Datei
`discover-analyse-<slug>-<datum>.md` im Arbeitsverzeichnis.

Aufbau:

1. **Kopf** — Titel, Domain-Profil, Sprache, Wortzahl, Analysedatum, **Score mit Band**.
2. **Urteil in drei Sätzen** — Was ist der Zustand, was ist der größte Hebel, was kostet es.
3. **Score-Tabelle** — fünf Dimensionen mit Punkten, Maximum und Einzeiler-Befund.
4. **Top-3-Maßnahmen** — nach Impact sortiert, jede mit Aufwand (in Minuten) und erwarteter
   Score-Wirkung. Das ist der Teil, den der Kunde umsetzt.
5. **Modul 1–5 im Detail** — pro Modul die Befunde mit Zitaten. Grüne Bereiche kurz.
6. **Textbausteine zum Einsetzen** — die konkreten Sätze/Absätze, die fehlen, fertig formuliert.
   Nicht „ergänze eine Definition", sondern die Definition.
7. **JSON-LD-Block** — kopierfertig.
8. **Methodik** — welche Werte berechnet, welche bewertet, welche Datenquellen genutzt wurden,
   und was der Skill nicht messen kann. Dieser Abschnitt ist Pflicht.

### Schritt 5 — Kundendokument anbieten, nicht aufdrängen

Nachdem der Bericht im Chat steht: **einmal** fragen, ob ein Dokument zur Weitergabe erzeugt
werden soll. Per AskUserQuestion, mehrfach wählbar, plus die Möglichkeit, nichts zu wählen:

| Option | Umsetzung |
|--------|-----------|
| **Word-Bericht** | Über den Skill `docx`. Aufbau wie der Markdown-Bericht, aber ohne Rohdaten-Dumps: Kopf mit Score, Urteil, Score-Tabelle, Top-3-Maßnahmen, Module 1–5, Textbausteine, JSON-LD im Anhang, Methodik. |
| **Excel-Maßnahmenliste** | Über den Skill `xlsx`. Eine Zeile pro Maßnahme, Spalten: Nr · Maßnahme · Modul · Priorität · Aufwand (Min) · Score-Wirkung · betroffene Textstelle · Status (leer zum Abarbeiten). |
| **HTML-Einseiter** | `assets/report-template.html` als Basis, Platzhalter ersetzen. Für Kunden ohne Office und ohne Claude-Zugang; druckbar. |

Ohne Auswahl bleibt es beim Chat-Bericht und der `.md`-Datei. Nie ungefragt ein Dokument
erzeugen — und nie ein Dokument mit unausgefüllten Platzhaltern ausliefern.

## Optionale Datenanreicherung

Der Skill funktioniert vollständig ohne externe Tools — er analysiert den Text. Wenn im
Kontext MCP-Server verfügbar sind, wird die Analyse belastbarer statt nur plausibler:

| Verfügbar | Nutzen | Einsatz in |
|-----------|--------|-----------|
| SERP-Daten (DataForSEO, Ahrefs, SurferSEO) | Erwartete Entitäten und Terme aus den real rankenden Seiten statt aus Modellwissen | Modul 1 (fehlende Entitäten), Modul 4 (Keywords) |
| Search Console (GSC) | Tatsächliche Discover-Impressionen/CTR der Domain als Benchmark | Score-Kontext, Modul 2 (Headline) |
| Trends (trends-local) | Aktuelles Interesse an der Kernentität — relevant für Freshness-Bewertung | Domain-Profil News/Flash News |

Regel: Wenn eine externe Quelle genutzt wurde, wird sie im Bericht benannt. Wenn nicht, steht
dort, dass die erwarteten Entitäten aus Modellwissen abgeleitet sind — das ist ein schwächerer
Beleg und der Kunde muss das wissen.

## Grenzen — ehrlich benennen

Diese Punkte gehören in den Methodik-Abschnitt jedes Berichts, wenn sie zutreffen:

- Der Skill bewertet **Text**. Bildwirkung, `og:image`-Größe, `max-image-preview`, News-Sitemap
  und Startseiten-Prominenz sind nicht Teil dieser Analyse → Skill `discover-artikel-optimierer`.
- „Fehlende Entitäten" ohne SERP-Daten sind eine begründete Vermutung, keine Messung.
- Headline-Scores sind Rubrik-Werte, keine CTR-Prognose. Eine echte CTR-Schätzung liefert nur
  ein Test am Live-Feed oder ein trainiertes Modell.
- Der Score sagt nichts über Site-Trust, Domain-Autorität oder Publisher-Status — die
  entscheiden vor der Content-Qualität über Discover-Eligibility.

## Referenzen

- `references/module-analysen.md` — Anweisungen und Ausgabeverträge für alle fünf Module,
  plus Metrik-Referenz für `textstats.py`.
- `references/scoring.md` — Rubrik für den Discover Content Score, Headline-Rubrik,
  Anti-Inflation-Regeln, Bänder.
- `references/domains.md` — acht Domain-Profile: erwartete Entitätstypen, Trust-Signale,
  Freshness-Erwartung, typische Fehler.
- `references/discover-mechanik.md` — warum die Kriterien gelten: Discover-Architektur,
  Entitäts-Personalisierung, Headline-Formeln, Freshness-Buckets.
