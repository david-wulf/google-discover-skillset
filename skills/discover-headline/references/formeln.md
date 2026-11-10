# Headline-Formeln und Technik

## Drei Titel, drei Aufgaben

Der Discover-Titel ist der **`og:title`**. Er darf und soll sich vom Meta-Title und von der H1
unterscheiden:

| Feld | Aufgabe | Optimiert auf |
|------|---------|---------------|
| `<title>` | Google-Suche | Keyword, Klarheit, Ranking |
| `<h1>` | die Seite selbst | Leseführung im Artikel |
| **`og:title`** | **Discover-Feed** | Emotion plus Versprechen, als ganzer Satz |

Eine Titeländerung nur an der H1 kommt im Feed **nicht** an. Das ist der häufigste stille Fehler:
Redaktionen ändern die Überschrift und wundern sich, dass die Karte gleich bleibt.

Abweichen ja — **widersprüchlich nein**. Bei Widersprüchen ersetzt Google den Titel durch eine
eigene Ableitung aus dem Seiteninhalt, und dann ist die ganze Arbeit weg.

Laut SDK-Befunden ist `og:title` **direkter Input in Googles pCTR-Modell**, nicht nur ein
Anzeigetext. Deshalb lohnt der Vortest hier mehr als an jeder anderen Stelle.

## Länge

Eine Zeichenzahl-Vorgabe für den `og:title` ist **nicht bestätigt**. Titel mit deutlich mehr als
65 Zeichen funktionieren im Feed problemlos. `pctr.py` zählt die Zeichen, bewertet sie aber nicht;
ein Titel wird nicht wegen seiner Länge abgewertet oder gekürzt.

Die Kernentität gehört trotzdem nach vorn, in die **ersten 40 Zeichen**: Dort liest jeder, auch
wer nur anscrollt.

## Die Formeln

Nicht die Formel befüllen, sondern den stärksten Fakt des Artikels suchen und in die passende
Formel einbauen. Bei fünf Varianten: fünf verschiedene Formeln, sonst testet man dieselbe Idee
fünfmal. **Jede Formel wird als ganzer Satz ausformuliert** (siehe nächster Abschnitt) — die
Formel bestimmt den Aufhänger, nicht die Satzform.

| Formel | Muster (Satzform) | Wirkt über |
|--------|--------|-----------|
| **How-to** | „Wie [Zielgruppe] [Ergebnis] erreicht — ohne [Hindernis]" | Nutzen plus entkräftete Angst |
| **Nummerierte Liste** | „[Zahl] [Dinge], die [Zielgruppe] [Ergebnis] bringen" | Abschätzbarer Aufwand |
| **Konträrer Ansatz** | „Warum [verbreitete Annahme] falsch ist — und was stattdessen gilt" | Widerspruch zur Erwartung |
| **Trend-Hook** | „Was [Änderung] ab [Zeitpunkt] für [Zielgruppe] bedeutet" | Aktualität plus Betroffenheit |
| **Experten-Zitat** | „[Experten/Institution] sagen es seit Jahren, und trotzdem [verbreiteter Fehler]" | Fremdautorität als Bürge |
| **Zahlen-Kontrast** | „[Gegenstand] schwankt zwischen [niedrig] und [hoch], und [was den Unterschied macht]" | Überraschung durch Spanne |
| **Konkretes Ergebnis** | „[Ergebnis mit Zahl] — [unter welcher Bedingung]" | Prüfbarkeit erzeugt Vertrauen |
| **Entscheidungshilfe** | „[Option A] oder [Option B]? [Das Kriterium] entscheidet" | Direkte Betroffenheit |
| **Kosten-Hook** | „So viel [sparst/kostet] dich [Thema] wirklich — [Zeitraum]" | Geld ist universell |

Die ersten fünf sind die Kernformeln des Playbooks, die übrigen vier Ergänzungen. Ältere Muster
mit Doppelpunkt („Laut [Institution]: …", „[Thema] 2026: was das für … bedeutet", „Von X bis Y:
…") sind **gegen die Ganzer-Satz-Regel nicht getestet** und werden nicht mehr als Standard
vorgeschlagen. Wer sie trotzdem verwendet, kennzeichnet die Variante als ungetestet.

Zwei Formeln haben einen Zulieferer im Prozess: der **Trend-Hook** kommt aus Trends-Daten, das
**Experten-Zitat** aus den Personen, die bei der Entitäten-Recherche ohnehin auffallen.

## Ganzer Satz statt Keyword-Stapel

Läuft derselbe Artikel mit beiden Titelformen im Feed, gewinnt der **ganze Satz** — in den
Titeltests derselben Artikel ausnahmslos und mit deutlichem Abstand (Stand: 2026-10). Beispiele
der getesteten Paare:

| Thema | Ganzer Satz (gewann) | Keyword-Titel |
|-------|-------------|---------------|
| Fenster putzen | „Fensterputzer sagen es seit Jahren, und trotzdem macht es fast jeder falsch" | „Fenster putzen ohne Streifen 4 Fehler" · „Schlieren Fenster Sonne Reiniger Zeitung" |
| Kondenswasser | „Beschlagene Fensterscheiben am Morgen sind ein Warnsignal" | „Kondenswasser innen Fenster Ursachen Grenzwerte" |
| Fugen im Bad | „Die Fugen im Bad vergrauen schneller, wenn du diesen Fehler machst" | „Essig Bad Zementfugen Schäden grau" · „Schimmel Fugen Silikon erneuern wann" |
| Standby | „Diese 7 Geräte ziehen Strom, obwohl ausgeschaltet" | „Stromfresser Ruhemodus 7 Geräte Tipps" |

**Faustregel:** ganzer Satz, zweite Person, ein sichtbares Alltagsproblem, die Ursache
zurückhalten. **Nicht:** Keyword-Stapel, Doppelpunkt, Produkt vorn. Discover ist ein Feed, keine
Suche — die Keyword-Form verliert dort ihren Vorteil.

„Die Ursache zurückhalten" ist keine Clickbait-Lizenz: Der Gegenstand steht im Titel (Fugen,
Fensterscheiben, Geräte), nur die Erklärung kommt im Artikel. Verschwiegen wird die Antwort,
nie das Thema — siehe Clickbait-Grenze unten.

**Grenzen der Messung:** vier Themen, alle Haushalts-Ratgeber. Für News mit harter
Tagesaktualität ist die Regel nicht belegt.

`pctr.py features` misst die Satzform heuristisch (`structure.sentence_form`: `satz`,
`keyword_stapel` oder `unklar`, nur für Deutsch). Das Feld ist ein Hinweis für die Bewertung von
`title_formatting`, kein Urteil.

## Suchtitel gegen Discover-Titel

Der Unterschied ist nicht Stil, sondern Funktion. In der Suche hat der Nutzer eine Absicht, im
Feed hat er keine — der Titel muss sie erzeugen.

- Suchtitel: „Die schönsten Wanderwege im Schwarzwald"
- Discover-Titel: „Ich habe 10 versteckte Schwarzwald-Pfade gefunden, die Touristen nicht kennen"

Die Zutaten der zweiten Variante: ganzer Satz, Ich-Perspektive, konkrete Zahl, benannte
Zielgruppe, angesprochener Wunsch. Alle fünf fehlen der ersten.

## Die Clickbait-Grenze

**Magnetisch ≠ Clickbait.** Beide versprechen viel. Der Unterschied ist, ob der Artikel liefert.

Zwei harte Anker, warum das keine Geschmacksfrage ist:

1. **Richtlinie:** Untersagt sind Vorschauinhalte, die zur Interaktion verleiten, indem **Details
   vorgetäuscht** werden. Die Regel greift am Vorschauelement — `og:title` und `og:image` — nicht
   am Artikeltext. Verstöße erscheinen als manuelle Maßnahme in der Search Console.
2. **Mechanik:** Die Klickqualität wird nach dem Navboost-Modell bewertet. Ein Titel, der klickt
   aber nicht einlöst, verliert dort. Clickbait ist rechnerisch schlecht, nicht moralisch.

Erschwerend: die historische CTR wird **pro URL** geführt. Eine URL nimmt ihre Feed-Reputation in
künftige Ausspielungen mit. Ein schwacher oder verbrannter Start belastet **diese URL** dauerhaft —
ein späterer Titelwechsel wirkt nur begrenzt. Bei grundlegend neuem Aufhänger ist eine neue URL die
ehrlichere Option.

### Rote Flaggen

- Kategoriesprache ohne Substanz: „Alles über X", „Was Sie wissen sollten"
- Gegenstand bewusst verschwiegen: „was dann passierte", „dieser eine Trick"
- Insiderwissen suggeriert, das der Artikel nicht hat: „keiner merkt es", „niemand spricht darüber"
- Reißerische Methoden über morbide Neugier, Nervenkitzel oder Empörung — ausdrücklich in den
  Richtlinien genannt
- Versalien und mehrere Ausrufezeichen
- Jahreszahl ohne Anlass im Artikel: eine ungedeckte Aktualitätsbehauptung

## Was ein Titel nicht reparieren kann

Der Titel ist der wichtigste Einzelhebel im Feed — aber er wirkt erst, wenn die Stufen davor
passen. Wenn ein Artikel gar keine Impressionen bekommt, liegt es nicht am Titel, sondern an
Trust und thematischer Autorität im Verzeichnis oder an der technischen Basis. Der Titel greift
an der Stelle, an der es Impressionen, aber kaum Klicks gibt.

Diagnose vor Titelarbeit:

| Symptom | Ansatzpunkt |
|---------|-------------|
| keine Impressionen | Eligibility: Trust, Indexierung, `max-image-preview:large` |
| Impressionen bei der falschen Zielgruppe | Klassifikation: Entitäten und Themenschärfe |
| Impressionen, kaum Klicks | **Titel und Bild** — hier greift dieser Skill |
| Klicks, dann sofortiger Rücksprung | Einlösung: der Artikel hält nicht, was der Titel verspricht |
| guter Start, dann Abflachen | Substanz und Aktualisierung |
