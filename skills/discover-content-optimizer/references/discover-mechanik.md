# Discover-Mechanik: warum die Kriterien gelten

Grundlage für die Begründungen im Bericht. Wer eine Empfehlung ausspricht, soll sagen können,
gegen welchen Mechanismus sie wirkt.

## Discover ist ein Push-Kanal ohne Query

Es gibt keine Suchanfrage, gegen die der Text matchen könnte. Google muss aus dem Dokument
selbst ableiten, **worum es geht** und **wen es interessiert**. Das erklärt, warum in diesem
Skill Entitäten und Themenfokus schwerer wiegen als klassische Keyword-Optimierung:
Die Zuordnung passiert über Entitäten, nicht über Query-Matching.

Der Ablauf in Stufen:

1. **Eligibility** — Prüfung auf Ebene der Domain und des Verzeichnisses, nicht des Artikels.
   Eine Sperre hier greift **vor** jedem Ranking. Content-Qualität kann sie nicht kompensieren.
2. **Klassifikation** — Zuordnung zu Themen-Clustern. Ein Text mit zwei konkurrierenden
   Themen wird unschärfer zugeordnet; das ist der Grund für D3 3b (Themenfokus).
3. **Personalisierung über Entitäten** — Abgleich der Dokument-Entitäten mit dem
   Interessenprofil des Nutzers. Entitäten sind hier der Match-Schlüssel. Eine Entität, die
   nur einmal isoliert genannt wird, trägt diesen Abgleich nicht — daher der Integrations-Score.
4. **Initial Exposure** — Test an einer kleinen Nutzergruppe. Hier entscheiden Headline und
   Bild fast allein. Deshalb ist die Headline ein Fünftel des Scores.
5. **Engagement-Feedback** — Fortschreibung anhand von Klickqualität, nicht nur Klickrate.
   Ein Klick, der schnell zurückspringt, schadet. Deshalb zählen Answer-First-Lead und
   Faktendichte: sie erfüllen das Versprechen der Headline.
6. **Decay** — Sichtbarkeit fällt mit dem Alter. Bewährte Buckets: 0–1 Tag, 1–7 Tage,
   8–14 Tage, 15–30 Tage, danach kontinuierlicher Verlust.

### Was das für strukturierte Daten heißt

Beim Auslesen von Titel, Autor und Publisher wird **Schema.org-JSON-LD zuerst** geprüft,
Open-Graph erst als Rückfallebene. Das widerspricht der verbreiteten Annahme, `og:title` sei
für Discover die einzige relevante Titelquelle. Praktische Folge: `headline` im JSON-LD und
`og:title` sollten bewusst gesetzt und konsistent sein — und `about[]` mit `sameAs` ist der
stärkste Hebel zur Entitäts-Disambiguierung, den ein Publisher selbst in der Hand hat.

Für Bilder gilt eine Mindestbreite von 1200 px für die große Feed-Karte. Das ist ein
technischer Check am veröffentlichten Dokument und damit Sache des Skills
`discover-readiness-artikel`, nicht dieses Skills.

*Quellen für diesen Abschnitt: metehan.ai, „Google Discover Architecture: Clusters,
Classifiers, OG Tags, NAIADES". Serverseitige Gewichtungen sind von außen nicht messbar —
die Stufenlogik ist ein belastbares Modell, keine offengelegte Spezifikation. Diese
Einschränkung gehört in den Methodik-Abschnitt, wenn im Bericht darauf Bezug genommen wird.*

---

## Headline-Formeln

Beim Erzeugen der fünf Varianten: nicht die Formel befüllen, sondern den stärksten Fakt
des Textes suchen und in die passende Formel einbauen. Jede Variante nutzt eine andere Formel.

| Formel | Mechanismus | Muster (Satzform) |
|--------|-------------|--------|
| **Zahlen-Kontrast** | Überraschung durch unerwartete Spanne | „[Gegenstand] schwankt zwischen [niedrig] und [hoch], und [was den Unterschied macht]" |
| **Konkretes Ergebnis** | Prüfbarkeit erzeugt Vertrauen | „[Ergebnis mit Zahl] — [unter welcher Bedingung]" |
| **How-to plus Hindernis** | Nutzen und entkräftete Angst | „Wie [Zielgruppe] [Ergebnis] erreicht — ohne [Hindernis]" |
| **Konträrer Ansatz** | Widerspruch zur Erwartung | „Warum [verbreitete Annahme] nicht stimmt — und was [Autorität] empfiehlt" |
| **Autorität plus Überraschung** | Fremdautorität als Bürge | „[Experten/Institution] sagen es seit Jahren, und trotzdem [verbreiteter Fehler]" |
| **Entscheidungshilfe** | Direkte Betroffenheit | „[Option A] oder [Option B]? [Kriterium] entscheidet" |
| **Trend-Hook** | Aktualität und persönliche Folge | „Was [Änderung] ab [Zeitpunkt] für [Zielgruppe] bedeutet" |
| **Kosten-Hook** | Geld ist der universelle Trigger | „So viel [sparst/kostet] dich [Thema] wirklich — [Zeitraum]" |

Ältere Muster mit Doppelpunkt („Laut [Institution]: …", „Von X bis Y: …") sind gegen die
Ganzer-Satz-Regel (Prinzip 6) nicht getestet und werden nicht mehr als Standard vorgeschlagen.

### Prinzipien

1. Der stärkste Fakt gehört in die Headline, nicht in Absatz 4.
2. Neugier-Lücke: Der Leser weiß, worum es geht, aber nicht die Antwort. Weder Rätsel noch Spoiler.
3. Konkret schlägt abstrakt. „389 Euro im Jahr" schlägt „viel Geld".
4. **Keine Längenvorgabe** für den `og:title`: Eine Zeichenzahl-Grenze ist nicht bestätigt, Titel
   über 65 Zeichen funktionieren im Feed problemlos. Bewertet wird der `og:title`, nicht die H1 — eine Titeländerung nur
   an der H1 kommt im Feed nicht an.
5. Die Kernentität steht in den ersten 40 Zeichen, nicht am Ende.
6. **Ganzer Satz statt Keyword-Stapel.** In Titeltests derselben Artikel gewann der ganze Satz
   ausnahmslos und deutlich gegen die Keyword-Varianten (Stand: 2026-10; Beispielpaare und
   Grenzen der Messung im Skill `discover-headline`, `references/formeln.md`). Faustregel: ganzer
   Satz, zweite Person, sichtbares Alltagsproblem, Ursache zurückhalten. Nicht: Keyword-Stapel,
   Doppelpunkt, Produkt vorn.

Eine vollständige Bewertung der Headline über acht gewichtete Dimensionen samt Clickbait-Abzug
leistet der Skill `discover-headline`. Ist er verfügbar, wird die Headline dort bewertet und das
Ergebnis hier übernommen.

### Rote Flaggen

- Kategoriesprache ohne Substanz („Neue Entwicklungen bei …")
- Clickbait ohne Einlösung im Text — kostet doppelt, weil Stufe 5 (Klickqualität) es bestraft
- Über 70 Zeichen
- Kein benannter Adressat
- Headline verspricht etwas, das der Text nicht liefert

---

## Warum Entitäten und nicht Keywords

Ein Keyword ist eine Zeichenfolge, eine Entität ein Ding mit Eigenschaften und Beziehungen.
Google bewertet thematische Autorität auf Entitätsebene. Deshalb reicht Nennung nicht —
es braucht Kontextualisierung. Vier Formen, von denen eine Kernentität mindestens zwei
haben sollte:

- **Definieren** — was ist es
- **Vergleichen** — wie unterscheidet es sich von der Alternative
- **In Beziehung setzen** — wie hängt es mit den anderen Entitäten des Textes zusammen
- **Vertiefen** — interner Link oder eigener Absatz

Der Integrations-Score in `textstats.py` operationalisiert genau das: Häufigkeit, Verteilung
über den Text, Ko-Vorkommen mit anderen Entitäten, Definitions-/Vergleichs-/Kausalmarker und
Faktendichte im Umfeld der Nennung.

---

## Der Zusammenhang mit AI-Sichtbarkeit

Was Discover als eindeutig klassifizierbaren, faktendichten, entitätsreichen Text bevorzugt,
ist auch das, was Antwortmaschinen zitieren: eine klare Kernaussage früh im Text, prüfbare
Zahlen mit Bezugsgröße, benannte Quellen, saubere Entitäts-Disambiguierung. Die Maßnahmen aus
diesem Skill wirken deshalb auf beide Kanäle. Das ist ein legitimes Argument im Kundenbericht —
aber als Plausibilität formulieren, nicht als gemessenen Effekt.
