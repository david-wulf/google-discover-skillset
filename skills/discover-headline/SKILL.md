---
name: discover-headline
description: >
  Bewertet und optimiert Discover-Headlines (og:title) mit einem pCTR-Modell: acht gewichtete
  Qualitätsdimensionen, Clickbait-Abzug (β) und Umrechnung in einen Prozentwert. Misst zuerst die
  Titelmerkmale (Länge, Zahlen, Ansprache, Clickbait-Lexikon, erkannte Formel, Position der
  Kernentität), bewertet dann nach dokumentierten Ankern und vergleicht bis zu fünf Varianten
  gegen die Original-Headline mit Delta in Prozentpunkten.
  Verwende diesen Skill immer, wenn es um Überschriften, Titel oder deren Klickwirkung geht —
  auch bei: "Headline prüfen", "Titel bewerten", "og:title optimieren", "pCTR", "CTR-Prognose
  Headline", "Headline-Varianten", "Überschrift testen", "welcher Titel ist besser",
  "Titel A/B vergleichen", "ist das Clickbait", "Titel zu lang", "Überschrift für Discover".
  Auch auslösen, wenn nur eine Liste von Titeln zur Bewertung eingereicht wird, oder wenn ein
  Artikel vorliegt und Titelvorschläge gewünscht sind.
  Für den Artikeltext ist discover-content-optimizer zuständig, für Titelbild und Feed-Karte
  discover-feedkarte.
---

# Discover Headline

Der Titel ist das wichtigste Einzelelement in Discover — laut SDK-Befunden **direkter Input in
Googles pCTR-Modell**, nicht bloß ein Anzeigetext. Dieser Skill bewertet ihn nach einem
nachgebauten, offen dokumentierten Modell und vergleicht Varianten gegeneinander.

## Grundregeln

1. **Erst messen, dann bewerten.** `pctr.py features` liefert Länge, Zahlen, Ansprache,
   Clickbait-Lexikon, erkannte Formeln und die Position der Kernentität. Diese Werte werden
   zitiert, nicht geschätzt.
2. **Anker statt Gefühl.** Jede der acht Dimensionen wird nach den Ankern in
   `references/dimensionen.md` bewertet, mit einem Satz Begründung pro Dimension, der sich auf den
   Titeltext oder einen gemessenen Wert bezieht.
3. **Die Original-Headline ist die Baseline.** Sie wird zuerst bewertet und mit
   `"baseline": true` markiert. Ohne Baseline ist keine Aussage darüber möglich, ob eine Variante
   besser ist.
4. **Der absolute pCTR-Wert ist keine CTR-Prognose.** Entscheidungsgrundlage ist der **Abstand
   zwischen den Varianten** in Prozentpunkten. Begründung in `references/dimensionen.md`,
   Abschnitt „Kalibrierungsschwächen".
5. **Clickbait-Veto.** Bei `clickbait_score` ≥ 6 wird die Variante nicht empfohlen, auch wenn ihr
   pCTR-Wert der höchste ist. Das Veto wird ausgewiesen, nicht versteckt.
6. **Maximal fünf Titel pro Durchlauf.** So verhält sich das Original, und mehr sind auch
   inhaltlich nicht vergleichbar.

## Ablauf

### Schritt 0 — Eingabe klären

| Was | Wie |
|-----|-----|
| **Titel** | Ein bis fünf. Bei einer URL: `og:title` aus dem HTML holen — **nicht** die H1, die kann abweichen. Weichen `og:title`, `<title>` und H1 voneinander ab, alle drei im Bericht nennen: das ist selbst ein Befund. |
| **Kernentität** | Für die Positionsprüfung. Aus dem Thema ableiten und die Annahme benennen. |
| **Artikeltext** | Optional, aber entscheidend für den `clickbait_score`: nur mit Text ist prüfbar, ob der Titel einlöst. Ohne Text wird der Wert als geschätzt markiert. |

Wenn nur ein Titel vorliegt und Varianten gewünscht sind: Original zuerst bewerten, dann vier
Varianten mit **je unterschiedlicher Formel** aus `references/formeln.md` erzeugen und alle fünf
gemeinsam durchrechnen.

### Schritt 1 — Merkmale messen

```bash
python scripts/pctr.py features --titles-file titel.txt --entity "Kernentität"
```

Auch möglich: `--title "..."` mehrfach. Ausgabe ist JSON pro Titel mit Länge und Längenband,
Konkretheit (Zahl, Einheit, Währung, Jahr), Ansprache (Frage, Du/Sie, Ich-Perspektive, Versalien,
Ausrufezeichen), Autoritäts-, Frische- und Superlativ-Markern, Clickbait-Lexikontreffern,
erkannten Formeln, Struktur und der Position der Kernentität.

Zwei Dinge zur Auslegung:

- `capitalized_tokens` ist **kein** Entitätennachweis. Im Deutschen sind alle Substantive groß.
- Clickbait-Lexikontreffer sind Verdachtsmomente. „keiner merkt es" kann in einem Text, der genau
  das belegt, gedeckt sein — ein Treffer verlangt eine Entscheidung mit Begründung, keinen
  Automatismus.

### Schritt 2 — Acht Dimensionen bewerten

Nach den Ankern in `references/dimensionen.md`. Ergebnis ist eine JSON-Datei:

```json
{"titles":[
  {"title":"...","baseline":true,
   "scores":{"entity_density":6.5,"topic_clarity":8.5,"informational_value":8.5,
             "freshness_signal":2,"engagement_depth":7.5,"title_formatting":6,
             "natural_authority":7.5,"visual_promise":5},
   "clickbait_score":1.0}
]}
```

Alle acht Schlüssel sind Pflicht, Werte 0–10; das Skript weist Unvollständiges und
Ausreißer zurück. Bewertungen für alle Titel in **einem** Durchgang vergeben, damit sie
untereinander konsistent sind — nicht Titel für Titel nacheinander.

### Schritt 3 — Rechnen

```bash
python scripts/pctr.py score --input bewertung.json
```

Liefert pro Titel `quality_score`, `beta_penalty`, `raw_score`, `pctr_pct`, Band, die
Beitragsverteilung, die drei schwächsten Beiträge, den Kopfraum je Dimension und den größten
Hebel — plus das Delta zur Baseline und eine Zusammenfassung mit Spannweite.

Die Formel wird unverändert aus dem Original übernommen, damit die Werte vergleichbar bleiben:

```
quality = Σ(wᵢ × fᵢ)              Gewichte: entity_density 22 %, topic_clarity 18 %,
β       = 1 − 0,35 × (cb / 10)    informational_value 16 %, freshness_signal 12 %,
raw     = quality × β             engagement_depth 10 %, title_formatting 8 %,
pCTR    = 0,5 % + 21,5 % × σ(0,65 × (raw − 5,5))    natural_authority 8 %, visual_promise 6 %
```

### Schritt 4 — Bericht

1. **Kopf** — Baseline-Titel, Anzahl Varianten, Kernentität, Analysedatum
2. **Urteil in drei Sätzen** — trägt das Original, welche Variante gewinnt um wie viel, was kostet
   die Umstellung
3. **Vergleichstabelle** — Titel, Zeichen, quality, β, pCTR, Band, **Delta zur Baseline in
   Prozentpunkten**. Das Delta ist die Entscheidungsspalte, nicht der Absolutwert
4. **Dimensionsprofil der Baseline und der besten Variante** — acht Werte gegenübergestellt, mit
   Begründung dort, wo der Unterschied entsteht
5. **Der größte Hebel** — aus `biggest_lever`: welche Dimension lässt die meisten Qualitätspunkte
   liegen, und was konkret im Titel dafür fehlt
6. **Empfehlung** — ein Titel, ausgeschrieben, mit Formel und Begründung. Bei Clickbait-Veto:
   welche Variante rechnerisch vorne lag, warum sie nicht empfohlen wird, und die gedeckte
   Alternative
7. **Methodik** — Formel und Gewichte, Herkunft, die zwei Kalibrierungsschwächen, und was
   geschätzt statt gemessen wurde

Wenn keine Variante die Baseline um mindestens **1,5 Prozentpunkte** übertrifft: das ausdrücklich
sagen — „Original behalten". Das ist ein Ergebnis, kein Versagen.

## Zusammenspiel mit den anderen beiden Skills

Die drei Skills decken die drei Hebel der Feed-Karte ab und greifen an definierten Stellen
ineinander:

| Skill | Hebel | Übergabe |
|-------|-------|----------|
| **discover-headline** | Titel | liefert den bewerteten `og:title` |
| discover-feedkarte | Titelbild und Karte | braucht den `og:title`, um zu prüfen, ob der Bildschriftzug ihn doppelt (K4 4a) |
| discover-content-optimizer | Artikeltext | braucht den Titel für die Headline-Dimension (D2) und liefert umgekehrt den stärksten Fakt für die Titelarbeit |

Praktisch heißt das:

- Wird dieser Skill nach `discover-content-optimizer` aufgerufen, den dort ermittelten
  **stärksten Fakt** des Artikels als Rohmaterial für die Varianten verwenden. Ein Titel kann
  keinen Fakt tragen, den der Text nicht hat — dann ist die Titelarbeit nachrangig und das gehört
  in den Bericht.
- Wird `discover-feedkarte` danach aufgerufen, den empfohlenen Titel dorthin übergeben, damit die
  Doppelungsprüfung gegen den **neuen** Titel läuft.
- Ist einer der anderen Skills verfügbar und passt zur Frage, darauf hinweisen statt die fremde
  Dimension mitzubeurteilen. Es gibt keine harte Abhängigkeit: jeder Skill funktioniert allein.

## Grenzen

- **Der absolute pCTR-Wert ist kein CTR-Versprechen.** Der Sigmoid-Mittelpunkt des Modells liegt
  bei 11,3 %, also am beobachteten Durchschnitt von News-Seiten — ein mittelmäßiger Titel bekommt
  dadurch einen Wert am oberen Ende der realen Bandbreite. Beobachtete Werte zum Vergleich:
  News rund 11 %, Non-News rund 6 %, Arbeitsziel 7–9 %, unter 5 % Handlungssignal. Diese Zahlen
  stammen aus einer GSC-Auswertung über 11.000 URLs und sind **nicht** aus dem Modell ableitbar.
- **Der Clickbait-Abzug des Modells ist zu schwach.** Deshalb das Veto außerhalb der Formel.
- Die acht Dimensionswerte sind eine begründete Bewertung, keine Messung. Reproduzierbar werden
  sie nur durch die Anker — deshalb sind sie verbindlich.
- Der Skill bewertet den Titel. Ob der Artikel überhaupt Impressionen bekommt, entscheidet die
  Eligibility-Stufe davor: Trust und thematische Autorität im Verzeichnis, Indexierung,
  `max-image-preview:large`. Diagnose-Raster in `references/formeln.md`.
- Ein Titelwechsel auf einer URL mit schwacher CTR-Historie wirkt begrenzt, weil die historische
  CTR pro URL geführt wird. Bei grundlegend neuem Aufhänger ist eine neue URL die ehrlichere Option.

## Herkunft

Formel, Gewichte und Bandgrenzen sind aus dem **pCTR Predictor** von metehan.ai
(`pctr-discover.pages.dev`) übernommen, wo Formel und Gewichte offen auf der Seite dokumentiert
und die Bandgrenzen im Client-Code hinterlegt sind. Die Bewertungsanker der acht Dimensionen
veröffentlicht das Original **nicht** — sie sind in `references/dimensionen.md` ergänzt, weil die
Bewertung ohne sie nicht reproduzierbar wäre.

Zum Stand der Prüfung: das Original war zum Zeitpunkt des Nachbaus nicht funktionsfähig (beide
Backends antworteten mit Fehlern). Ein direkter Ergebnisvergleich war deshalb nicht möglich; die
Rechnung wurde stattdessen gegen die veröffentlichte Formel verifiziert.
