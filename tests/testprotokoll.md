# Testprotokoll — Nachbau vs. Original

Datum: 2026-08-06 · Original: <https://googlediscoveroptimizer.replit.app/> (metehan.ai)

## Testfälle

| # | Datei | Sprache | Charakter |
|---|-------|---------|-----------|
| A | `sample_en.txt` | EN | Hands-on-Test MacBook M5, faktendicht, eigene Messung. **Identischer Text auch im Original gelaufen.** |
| B | `sample_de_schwach.txt` | DE | Ratgeber Balkonkraftwerk, bewusst inhaltsleer: keine Zahl, keine benannte Quelle. **Identischer Text auch im Original gelaufen.** |
| C | `sample_de_stark.txt` | DE | Gleiches Thema wie B, stark: Messwerte, benannte Quellen, Rechtsstand, Gegenposition. |

## Ergebnis Discover Content Score

| Dimension | A (EN, gut) | B (DE, schwach) | C (DE, stark) |
|-----------|------------:|----------------:|--------------:|
| D1 Entitäten (25) | 17 | 6 | 25 |
| D2 Headline + Einstieg (20) | 15,8 | 7,6 | 16,2 |
| D3 Semantische Vollständigkeit (20) | 11 | 6 | 17 |
| D4 Struktur (15) | 13 | 8 | 12 |
| D5 Vertrauen + Maschinenlesbarkeit (20) | 16 | 4 | 17 |
| **Gesamt** | **73** | **32** | **87** |
| Band | Solide | Nicht Discover-fähig | Discover-ready |

**Spreizung B → C: 55 Punkte.** Abnahmekriterium war ≥ 25. Bestanden.

Gemessene Grundlage der Spreizung (nicht geschätzt):

| Metrik | B | C |
|--------|--:|--:|
| Faktendichte (spezifische Angaben je 100 Wörter) | 0,00 | 4,42 |
| Benannte Quellen | 0 (nur „Studien zeigen") | 4 (HTW Berlin, Verbraucherzentrale NRW, Bundesnetzagentur, VDE V 0126-95) |
| Erstautorschaft belegt | nein | ja („Ich habe zwei Anlagen über zwölf Monate … protokolliert") |
| `lead.answer_first_hint` | false | true |
| Integrations-Mittelwert Kernentitäten | 0,354 | 0,671 |
| Zwischenüberschriften faktentragend | 0 von 3 | 5 von 5 |

## Headline-Kalibrierung — der Kernunterschied

Gleicher Text B, beide Systeme:

| System | Varianten-Scores | Spanne | Original-Headline bewertet? |
|--------|------------------|-------:|----------------------------|
| Original | 87 · 88 · 89 · 90 · **92** | 5 Punkte | nein |
| Nachbau | 4,0 · 5,0 · 6,0 · 6,0 · 6,0 (von 10) · Original-Headline **4,0** | 2,0 Punkte, alle im unteren Drittel | ja |

Die niedrigste Nachbau-Variante (4,0) ist die mit dem Kosten-Hook „so viel Strom sparst du im
Jahr" — sie verspricht eine Sparsumme, die der Text nicht einlöst, und wird über K2 abgestraft.
Das Original hätte genau diese Variante hoch bewertet.

Die höchste Bewertung des Originals (92) ging an
„Alles, was Sie über Balkonkraftwerke wissen müssen: Nutzen, Kosten und Installation" —
83 Zeichen, im Feed abgeschnitten, ohne einen einzigen Fakt.

Der Nachbau deckelt hier über K1 (Konkretheit) und K4 (stärkster Fakt): Ein Text ohne Zahlen
kann keine Headline mit Zahlen tragen. Statt fünf Scheinlösungen liefert er den Befund:
**Das Headline-Problem ist ein Inhaltsproblem.** Erst Fakten in den Text, dann Headline.

Nebenbefund: Das Original nutzt keine feste Skala. Im englischen Lauf lagen die Headline-Scores
bei 8,4–9,5, im deutschen bei 87–92; die Relevanz-Scores fehlender Konzepte bei 7–9 bzw. 3–5.
Dieselbe Bewertungsdimension, zwei Skalen — die Werte sind zwischen Läufen nicht vergleichbar.

## Fehlende Entitäten — Vergleich Text B

| Original (8 Einträge, unpriorisiert, englisch) | Nachbau (priorisiert, deutschsprachig, rechtsraumkonkret) |
|---|---|
| Regulatory Bodies · Technical Specifications · Installation Requirements · Financial Incentives · Grid Connectivity · Maintenance and Upkeep · Safety Standards · Battery Storage Options | **Hoch:** Marktstammdatenregister der Bundesnetzagentur · 800-Watt-Einspeisegrenze / Solarpaket I · Ertrag in kWh mit Ausrichtungsbezug · Anschaffungspreis und Amortisation · **Mittel:** Wechselrichter · Eigenverbrauchsquote · Schuko-Stecker / VDE V 0126-95 · **Niedrig:** Speicheroption |

Das Original bleibt auf Kategorieebene („Regulatory Bodies") und antwortet auf einen deutschen
Text auf Englisch. Der Nachbau benennt die tatsächlich erwarteten Entitäten des deutschen
Rechtsraums, weil das Domain-Profil den Erwartungsraum vorgibt.

## Embedding-Heatmap — belegte Nichtaussage

| Lauf | Legendenband der Matrix |
|------|------------------------|
| Original, Text A (EN) | 0,80 – 1,00 |
| Original, Text B (DE) | 0,85 – 1,00 |

Alle Entitätspaare liegen im obersten Fünftel bzw. Siebtel. Die Matrix trennt nichts.

Der Integrations-Score des Nachbaus auf denselben Texten: 0,17 bis 0,82, mit inhaltlich
nachvollziehbarer Zuordnung — „Anmeldung" in Text B bei 0,17 (einmal genannt, ohne Kontext,
ohne Zahl), „Wechselrichter" in Text C bei 0,82 (vier Nennungen, drei Absätze, Vergleich
600/800 W, Kausalkette zur Abregelung).

## Deckung mit dem Original bei Text A (identischer Input)

Die inhaltlich tragfähigen Lücken des Originals werden alle gefunden. Gegenprobe:

| Original meldete | Nachbau |
|---|---|
| Benchmarks (Geekbench/Cinebench) | ✅ Priorität hoch |
| CPU-/GPU-Kernzahl | ✅ Priorität hoch |
| Wettbewerbsvergleich außerhalb Apple | ✅ Priorität hoch |
| Ports / Konnektivität | ✅ Priorität mittel |
| Thermik / Kühlung | ✅ Priorität mittel |
| Speicheroptionen, macOS-Version, Verfügbarkeitsregionen | ✅ Priorität niedrig |
| Audio-System, Gewicht und Maße, Upgradeability, Nachhaltigkeit, Security, Display | ⚠️ verworfen — Textsorte ist ein fokussierter Upgrade-Test, kein Datenblatt. Begründung steht im Bericht. |

Das Original liefert 9 bis 15 Lücken ohne Priorität und ohne Rücksicht auf die Textsorte.
Der Nachbau priorisiert auf maximal 8 und begründet Verwerfungen.

## Während der Tests gefundene und behobene Fehler im eigenen Code

| Fehler | Wirkung | Fix |
|--------|---------|-----|
| Stoppwortlisten ASCII-notiert | „für", „über", „möchten" wurden als Kernbegriffe gelistet | `fold()`-Vergleichsform |
| `\bStudie\b` | „Studien zeigen" — der häufigste vage Quellenverweis — blieb unerkannt | Beugungsformen ergänzt |
| „selbst" als Erfahrungsmarker | „selbst Strom erzeugen" galt als Erstautorschaft | nur `selbst getestet/gemessen/…` |
| stdout-Kodierung Windows | Umlaute als Ersatzzeichen | `reconfigure(encoding="utf-8")` |
| Belegentitäten im Integrations-Mittelwert | gut belegter Text 0,40 vs. leerer Text 0,33 — keine Trennschärfe | `--core` / `--entities` getrennt, Kontext höher gewichtet → 0,67 vs. 0,35 |
| `is_heading_line()` verwarf Fragezeichen | „Should you upgrade?" wurde nicht als Zwischenüberschrift gezählt, obwohl die Rubrik Fragen belohnt | Fragezeichen zugelassen, `question_subheadings` ergänzt |
| Höflichkeitsform nicht erkannt | deutsche Headlines mit „Sie" verloren bei K3 einen Punkt | groß geschriebenes `Sie`/`Ihr…` ergänzt |

## Nicht abgeschlossen

Der Direktvergleich für Text C wurde nicht gefahren — für die Kalibrierungsprüfung reichen
A und B, weil dort identischer Input in beiden Systemen vorliegt.

Die Bewertung im Original erfolgte über die Browser-Automatisierung bei nicht gerendertem
Viewport (`window.innerWidth === 0`); Screenshots waren deshalb nicht möglich. Alle
Original-Werte stammen aus dem DOM-Text der Tab-Panels, nicht aus Bildschirmfotos.
