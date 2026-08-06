# Headline-Formeln und Technik

## Drei Titel, drei Aufgaben

Der Discover-Titel ist der **`og:title`**. Er darf und soll sich vom Meta-Title und von der H1
unterscheiden:

| Feld | Aufgabe | Optimiert auf |
|------|---------|---------------|
| `<title>` | Google-Suche | Keyword, Klarheit, Ranking |
| `<h1>` | die Seite selbst | Leseführung im Artikel |
| **`og:title`** | **Discover-Feed** | Emotion plus Versprechen, ~70–95 Zeichen |

Eine Titeländerung nur an der H1 kommt im Feed **nicht** an. Das ist der häufigste stille Fehler:
Redaktionen ändern die Überschrift und wundern sich, dass die Karte gleich bleibt.

Abweichen ja — **widersprüchlich nein**. Bei Widersprüchen ersetzt Google den Titel durch eine
eigene Ableitung aus dem Seiteninhalt, und dann ist die ganze Arbeit weg.

Laut SDK-Befunden ist `og:title` **direkter Input in Googles pCTR-Modell**, nicht nur ein
Anzeigetext. Deshalb lohnt der Vortest hier mehr als an jeder anderen Stelle.

## Länge

Richtwert **70–95 Zeichen**. Darunter bleibt Platz für den Haken ungenutzt, darüber wird im Feed
abgeschnitten. Praktische Bänder:

| Zeichen | Bewertung |
|---------|-----------|
| 70–95 | optimal |
| 50–69 | kurz — der Titel könnte mehr tragen |
| 96–110 | lang — Abschneiden möglich |
| < 50 oder > 110 | außerhalb |

Die Kernentität gehört in die **ersten 40 Zeichen**, weil dort auf jedem Gerät gelesen wird.

## Die Formeln

Nicht die Formel befüllen, sondern den stärksten Fakt des Artikels suchen und in die passende
Formel einbauen. Bei fünf Varianten: fünf verschiedene Formeln, sonst testet man dieselbe Idee
fünfmal.

| Formel | Muster | Wirkt über |
|--------|--------|-----------|
| **How-to** | „Wie [Zielgruppe] [Ergebnis] erreicht — ohne [Hindernis]" | Nutzen plus entkräftete Angst |
| **Nummerierte Liste** | „[Zahl] [Adjektiv] Wege zu [Nutzen]" | Abschätzbarer Aufwand |
| **Konträrer Ansatz** | „Warum [verbreitete Annahme] falsch ist — und was stattdessen gilt" | Widerspruch zur Erwartung |
| **Trend-Hook** | „[Änderung/Jahr]: was das für [Zielgruppe] bedeutet" | Aktualität plus Betroffenheit |
| **Experten-Zitat** | „Laut [Institution]: [überraschende Erkenntnis]" | Fremdautorität als Bürge |
| **Zahlen-Kontrast** | „Von [niedrig] bis [hoch]: [was den Unterschied macht]" | Überraschung durch Spanne |
| **Konkretes Ergebnis** | „[Ergebnis mit Zahl] — [unter welcher Bedingung]" | Prüfbarkeit erzeugt Vertrauen |
| **Entscheidungshilfe** | „[Option A] oder [Option B]? [Das Kriterium]" | Direkte Betroffenheit |
| **Kosten-Hook** | „[Thema]: so viel [sparst/kostet] du wirklich — [Zeitraum]" | Geld ist universell |

Zwei Formeln haben einen Zulieferer im Prozess: der **Trend-Hook** kommt aus Trends-Daten, das
**Experten-Zitat** aus den Personen, die bei der Entitäten-Recherche ohnehin auffallen.

## Suchtitel gegen Discover-Titel

Der Unterschied ist nicht Stil, sondern Funktion. In der Suche hat der Nutzer eine Absicht, im
Feed hat er keine — der Titel muss sie erzeugen.

- Suchtitel: „Die schönsten Wanderwege im Schwarzwald"
- Discover-Titel: „Ich habe 10 versteckte Schwarzwald-Pfade gefunden, die Touristen nicht kennen"

Die Zutaten der zweiten Variante: Ich-Perspektive, konkrete Zahl, benannte Zielgruppe, angesprochener
Wunsch. Alle vier fehlen der ersten.

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
