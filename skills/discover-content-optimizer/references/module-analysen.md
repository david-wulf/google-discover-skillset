# Module 1–5: Anweisungen und Ausgabeverträge

---

## Metrik-Referenz: was `textstats.py` liefert

Diese Werte sind berechnet. Sie werden zitiert, nicht geschätzt.

| Feld | Bedeutung | Bewertung |
|------|-----------|-----------|
| `document.avg_sentence_words` | Ø Satzlänge in Wörtern | Discover-Feed wird mobil gelesen. 12–18 ist gut, über 22 wird zäh |
| `document.long_sentence_ratio` | Anteil Sätze > 25 Wörter | über 0,25 = Struktur-Abzug |
| `document.avg_paragraph_words` | Ø Absatzlänge | 35–70 gut. `paragraphs_over_120w` > 0 = Mobil-Problem |
| `document.subheadings_detected` | erkannte Zwischenüberschriften | < 1 pro 250 Wörter = Abzug |
| `readability.score` / `.band` | Flesch (EN) bzw. Flesch-Amstad (DE) | DE-Zielband 50–70. Unter 40 = zu schwer für einen Feed-Kanal |
| `headline.characters` | Headline-Länge | > 65 Zeichen wird im Feed abgeschnitten |
| `lead.answer_first_hint` | Erster Satz kurz **und** enthält Zahl/Aussageverb | `false` = Lead liefert die Antwort nicht sofort |
| `fact_density.specific_facts_per_100_words` | Prozent-, Währungs-, Datums-, Einheitenangaben je 100 Wörter | < 1,0 = vage. 2–6 = faktendicht |
| `topical_core_terms` | häufig **und** über viele Absätze verteilt | Das ist die thematische Klammer — als was Google den Text klassifiziert |
| `tfidf_peak_terms` | lokal dichte Terme (echte IDF über Absätze) | Unterthemen. Wenn die Kernentität hier fehlt, aber in Core steht: gut. Wenn sie in beiden fehlt: Fokusproblem |
| `entities.<x>.integration_score` | 0–1, siehe Formel unten | < 0,4 = `isoliert`: Entität wird genannt, aber nicht eingebunden |
| `entity_cooccurrence` | Jaccard über Sätze, paarweise | Zeigt, welche Entitäten der Text tatsächlich miteinander verknüpft |

**Integrations-Score, Formel** (im Skript implementiert, hier zur Erklärung im Bericht):

```
0,25 · min(1, Häufigkeit/3)
+ 0,20 · min(1, Absatz-Spread/0,4)
+ 0,25 · min(1, Ø-Top3-Kookkurrenz/0,35)
+ 0,20 · (Anteil vorhandener Marker aus {Definition, Vergleich, Kausalität})
+ 0,10 · min(1, Zahlen im Kontext/2)
```

Bänder: ≥ 0,65 `stark` · 0,40–0,64 `mittel` · < 0,40 `isoliert`.

> **Warum kein Embedding-Heatmap wie im Referenztool.** Ein Cosine-Heatmap über
> Entitäts-Embeddings misst, wie ähnlich zwei Begriffe *im Modell* sind — „CPU" und „GPU" sind
> immer ähnlich, unabhängig vom Artikel. Deshalb liegen solche Matrizen praktisch immer im
> Band 0,8–1,0 und diskriminieren nicht. Der Integrations-Score misst stattdessen, ob **dieser
> Text** die Entität eingebunden hat: Häufigkeit, Verteilung, Ko-Vorkommen mit anderen
> Entitäten, Definitions-/Vergleichs-/Kausalmarker, Faktendichte im Umfeld. Das ist die Frage,
> die für Discover zählt, und sie ist ohne API und ohne Kosten reproduzierbar berechenbar.
> Diese Begründung gehört in den Methodik-Abschnitt.

---

## Modul 1 — Entitätenanalyse

Fundament. Alle anderen Module bauen darauf auf.

### 1.1 Identifizierte Entitäten

Extrahiere alle Entitäten aus dem Text, gruppiert nach Typ:

`Organisationen` · `Personen` · `Orte` · `Produkte` · `Ereignisse` · `Konzepte/Fachbegriffe`

Regeln:
- Nur was wirklich im Text steht. Keine Ergänzungen aus Weltwissen (die kommen in 1.3).
- Konzepte sind Fachbegriffe und Sachverhalte, keine Allerweltswörter. „Speicherbandbreite" ja,
  „Leistung" nein.
- Jede Entität in der Schreibweise des Textes, damit das Skript sie findet.
- Danach zweiten `textstats.py`-Lauf mit dieser Liste starten.

### 1.2 Entitäten-Beziehungen

Aus der Kookkurrenzmatrix plus Lektüre: welche Entitäten verknüpft der Text explizit,
und **wie** (Hersteller-von, Nachfolger-von, Voraussetzung-für, Alternative-zu, Ursache-von …).

Ausgabe als Liste `A —[Beziehung]→ B`, plus:
- **Nicht verknüpfte Paare, die verknüpft sein müssten** — das sind die wertvollsten Befunde.
  Beispiel: Text nennt Produkt und Anwendungsfall, verbindet sie aber nie in einem Satz.
- Bei mehr als 8 Entitäten: die 10 wichtigsten Beziehungen, nicht alle.

Wenn ein Diagramm hilft, ein Mermaid-Graph (`graph LR`). Nicht bei weniger als 5 Entitäten.

### 1.3 Fehlende Entitäten

Der Kern des Moduls. Welche Entitäten erwartet Google bei diesem Thema, die der Text nicht hat?

Vorgehen:
1. Kernthema und Suchintention bestimmen.
2. Erwartungsraum aufstellen — nach Domain-Profil (`references/domains.md`). Wenn SERP-Daten
   verfügbar sind: aus den Top-10 der real rankenden Seiten. Sonst aus Modellwissen, **und das
   im Bericht kennzeichnen**.
3. Abgleich mit 1.1.
4. Jede fehlende Entität bewerten.

Ausgabevertrag pro Eintrag:

| Feld | Inhalt |
|------|--------|
| Entität | Name |
| Typ | Organisation / Person / Produkt / Konzept / … |
| Warum relevant | Ein Satz, thema-spezifisch. Nicht „für Vollständigkeit" |
| Priorität | **Hoch** = Text ist ohne sie unvollständig; Leser fragt sich das zwangsläufig · **Mittel** = stärkt Autorität · **Niedrig** = nice-to-have |
| Einbau | Wo im Text, in welcher Form (Satz, Absatz, Tabellenzeile, interner Link) |

Maximal 8 Einträge, nach Priorität sortiert. Kein Vollständigkeits-Dumping: eine Liste mit
15 Entitäten ohne Priorisierung ist für den Kunden wertlos.

**Häufigster Fehler, den es zu vermeiden gilt:** Entitäten fordern, die in einem *anderen*
Artikel gehören. Bei einem Hands-on-Test gehören Preisstaffeln und Zubehör-Ökosystem nicht
zwingend in den Text — bei einem Kaufberater schon. Prüfe die Textsorte, bevor du Lücken meldest.

---

## Modul 2 — Content-Optimierung

### 2.1 Original-Headline bewerten

**Zuerst**, vor allen Alternativen. Rubrik in `references/scoring.md`, Abschnitt
„Headline-Rubrik". Ausgabe: Punkte pro Kriterium, Summe, ein Satz Begründung, plus die vom
Skript gemessene Zeichenzahl.

### 2.2 Headline-Varianten

Genau 5 Varianten. Jede nutzt eine **andere** Formel (Formelkatalog in
`references/discover-mechanik.md`). Pro Variante:

- Die Headline (≤ 65 Zeichen, gezählt — nicht geschätzt)
- Formel
- Rubrik-Score mit derselben Rubrik wie das Original
- Ein Satz: welcher Fakt aus dem Text sie trägt

Harte Regeln:
- Der stärkste Fakt des Textes muss in mindestens zwei Varianten vorkommen.
- Höchstens eine Variante darf ≥ 9,0 bekommen.
- Wenn keine Variante das Original um ≥ 1,5 Punkte übertrifft: das ausdrücklich sagen —
  „Original ist stark, Varianten bringen keinen Gewinn." Das ist ein legitimes Ergebnis.
- Keine Clickbait-Varianten („Du wirst nicht glauben …"). Sie scoren in der Rubrik ohnehin schlecht.

### 2.3 Semantische Anreicherung

Wo braucht der Text mehr semantische Substanz? Pro Empfehlung: Position im Text (Absatznummer),
was fehlt, **fertig formulierter Vorschlagstext** (1–3 Sätze). Maximal 4 Empfehlungen.

Typische Hebel: unerklärte Fachbegriffe, fehlende Vergleichsgröße zu einer Zahl, fehlende
Kausalkette („warum ist das so"), fehlende Einordnung („was heißt das für mich").

### 2.4 Topic-Cluster

In welche 3–5 Teilthemen zerfällt der Text? Pro Cluster: Name, welche Absätze dazugehören,
Anteil am Text. Dann: ist die Gewichtung sinnvoll für die Suchintention, oder ist ein
Nebenthema überproportional groß? Ein Cluster, der über den ganzen Text verstreut ist statt
gebündelt, ist ein Strukturbefund.

### 2.5 Struktur

Auf Basis der Skript-Metriken: Zwischenüberschriften-Dichte, Absatzlängen, Satzlängen,
Listen/Tabellen, Answer-First im Lead. Bei Zwischenüberschriften auch die Qualität prüfen —
„Was sich geändert hat" ist schwächer als „153 GB/s: was sich technisch geändert hat", weil
die zweite Variante eine Entität und einen Fakt trägt.

Konkrete Vorschläge, keine Prinzipien: welche Überschrift wie umformulieren, welcher Absatz
wo geteilt werden soll.

### 2.6 Interne Verlinkung

3–5 Vorschläge. Pro Vorschlag: Ankertext (aus dem Textfluss heraus, keine „hier klicken"),
Zielthema, Begründung über Entitätsvertiefung. Wenn die Domain bekannt ist und eine Suche
möglich ist: nach real existierenden Zielseiten suchen statt Themen zu erfinden.

### 2.7 Wettbewerbs-Gap (nur mit Wettbewerbertext)

Ohne gelieferten Vergleichstext: Abschnitt weglassen und einen Satz notieren, dass er ohne
Vergleichstext nicht möglich ist. **Nicht** raten, was Wettbewerber schreiben.

Mit Vergleichstext: Entitäten und Kernbegriffe beider Texte gegenüberstellen. Drei Listen —
nur beim Wettbewerber (= Lücke), nur im eigenen Text (= Differenzierung, bewusst behalten),
bei beiden (= Pflichtthemen, prüfen wer es besser macht).

---

## Modul 3 — Schema-Markup

### 3.1 JSON-LD generieren

Typ nach Textsorte: `NewsArticle` (nachrichtlich, datiert), `Article` (Standard),
`BlogPosting` (persönlich/meinungsstark), zusätzlich `HowTo`/`FAQPage`/`Review` wenn die
Struktur es hergibt.

Pflichtfelder: `@context`, `@type`, `headline` (≤ 110 Zeichen), `description`, `datePublished`,
`dateModified`, `author` (als `Person` mit `name` **und** `url`), `publisher` (als `Organization`
mit `logo` als `ImageObject`), `image` (als `ImageObject` mit `width`/`height`),
`mainEntityOfPage`.

Discover-relevante Zusatzfelder, die den Unterschied machen:
- `about[]` — die 3–6 **Kernentitäten** aus Modul 1, jeweils als `Thing` mit `name` und, wenn
  bekannt, `sameAs` (Wikipedia/Wikidata). `sameAs` ist der stärkste Entitäts-Disambiguierer.
- `mentions[]` — die übrigen Entitäten, nach Typ (`Organization`, `Product`, `Person`).
- `articleSection` — passend zum Domain-Profil.
- `inLanguage`, `isAccessibleForFree`, bei Paywall `hasPart` mit `cssSelector`.
- `speakable` bei nachrichtlichem Content.

Regeln:
- Unbekannte Werte als klar markierte Platzhalter (`"{{AUTOR_NAME}}"`), nie erfunden. Im Bericht
  eine Liste, welche Platzhalter der Kunde füllen muss.
- `articleBody` **nicht** einfügen — bläht das Markup auf, ohne Nutzen für Discover.
- `about` nicht mit 15 Einträgen füllen. Wer alles als Hauptthema markiert, markiert nichts.

### 3.2 Validierung

Prüfe und protokolliere in vier Blöcken:

1. **Syntax** — valides JSON, `@context` korrekt, keine doppelten Keys.
2. **Pflichtfelder** — pro Feld: vorhanden / fehlt / Platzhalter.
3. **Google-Richtlinien** — `headline`-Länge, `image` mit Maßen und ≥ 1200 px Breite,
   `author` als Objekt statt String, `datePublished` in ISO 8601 mit Zeitzone,
   `publisher.logo` vorhanden.
4. **Discover-Spezifika** — `about[]` gesetzt und mit `sameAs` angereichert; Schema-Titel
   konsistent mit geplantem `og:title`; `dateModified` ≥ `datePublished`.

Jeder Block: Status, konkreter Befund, Fix. Ein „alles valide" ohne Prüfliste ist kein
Validierungsergebnis.

---

## Modul 4 — Keyword-Analyse

### 4.1 Berechnete Basis

`topical_core_terms` und `tfidf_peak_terms` aus dem Skript darstellen (je Top 10, mit Werten).
Dann interpretieren:

- Steht die Kernentität in den Core-Terms? Wenn nein: Fokusproblem, der Text redet über etwas
  anderes als beabsichtigt.
- Gibt es Peak-Terme, die zum Thema nichts beitragen? Wenn ja: Nebenthema frisst Substanz.
- Sind die Core-Terme thematisch homogen? Wenn sie in zwei unverbundene Gruppen fallen,
  behandelt der Text zwei Themen — für Discover fast immer ein Nachteil, weil die
  Themen-Klassifikation unschärfer wird.

### 4.2 Primäre und sekundäre Keywords

Primär: 5–8 Terme, die das Thema tragen. Sekundär: 8–12, die den Themenraum aufspannen.
Jeweils mit Begründung aus den berechneten Werten oder — bei ergänzten Termen, die noch nicht
im Text sind — mit dem Hinweis „noch nicht im Text".

### 4.3 Semantische Cluster und Wichtigkeit

3–5 Cluster mit Zuordnung der Keywords. Wichtigkeits-Score 0–10 pro primäres Keyword,
begründet aus: Position in Headline/Lead, TF, Absatz-Spread, Rolle in der Suchintention.
Nicht alle Keywords bei 8–9 — spreize den Bereich.

### 4.4 Platzierung

Wo konkret fehlt welcher Term: Headline, Lead (erste 100 Wörter), Zwischenüberschriften,
Schlussabsatz, Bild-Alt-Text, Meta-Description. Tabelle Term × Position × Status
(vorhanden / fehlt / überrepräsentiert).

### 4.5 Long-Tail

4–6 Varianten, jede mit der Nutzerfrage dahinter und dem Ort im Text, an dem sie beantwortet
werden kann. Nur Varianten, die der Text plausibel abdecken kann — nicht Themen für weitere
Artikel (die gehören in Modul 2.6 als interne Verlinkung).

---

## Modul 5 — Semantische Abdeckung

### 5.1 Entitäten-Integration

Tabelle aus dem Skript: Entität, Anzahl, Absatz-Spread, Integrations-Score, Band, gefundene
Marker. Sortiert nach Score aufsteigend — die Problemfälle stehen oben.

Dann pro isolierter Entität (Score < 0,4) ein Befund: Zitat der einzigen Nennung, warum das
Discover schadet, und der fertige Satz, der sie einbindet.

Nennenswert ist auch der Gegenfall: eine Entität mit sehr hoher Frequenz und niedrigem Spread
steht geballt an einer Stelle — Hinweis auf einen Absatz, der als Fremdkörper wirkt.

Kennzahl für den Score: `entity_summary.mean_integration` und die Verteilung der Bänder.

### 5.2 Kookkurrenz lesen

Aus `entity_cooccurrence`: die 3 stärksten und die 3 auffällig schwachen Paare (Paare, die
thematisch zusammengehören, aber Jaccard 0 haben). Letztere sind konkrete Schreibaufträge.

### 5.3 Fehlende semantische Konzepte

Anders als Modul 1.3: dort fehlen **benennbare Entitäten**, hier fehlen **Denkschritte und
Perspektiven** — Einordnung, Gegenposition, Risiko, Kosten, Zeithorizont, Zielgruppendifferenzierung,
rechtlicher Rahmen, was-wäre-wenn.

Pro Konzept:

| Feld | Inhalt |
|------|--------|
| Konzept | z. B. „Langfristige Softwareunterstützung" |
| Relevanz | 0–10, begründet aus Suchintention und Domain-Profil |
| Warum es fehlt ins Gewicht fällt | Ein Satz: welche Nutzerfrage unbeantwortet bleibt |
| Umsetzung | Wo und wie, mit Formulierungsvorschlag |

4–6 Konzepte, nach Relevanz sortiert. Relevanz-Werte müssen spreizen — wenn alle 8–9 haben,
ist nicht priorisiert.
