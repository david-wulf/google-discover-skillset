# Headline-Analyse: Kalibrierungslauf über fünf Titel

Beispielausgabe des Skills `discover-headline`. Der Satz enthält absichtlich Extreme — einen
inhaltsleeren Rahmen, zwei starke Titel und einen reinen Clickbait-Titel als Kontrolle —, damit
sichtbar wird, ob das Modell spreizt.

**Baseline:** „Balkonkraftwerk: Was Sie wissen sollten" · **Kernentität:** Balkonkraftwerk ·
**Analyse:** 2026-08-06

## Urteil

Die Baseline landet bei 4,9 % im Band „niedrig" — sie nennt ihr Thema und verspricht nichts.
Die stärkste Variante gewinnt **+9,6 Prozentpunkte**, und zwar allein über
`informational_value` und `engagement_depth`: eine konkrete Spanne plus die Ankündigung, sie zu
erklären. Der Clickbait-Kontrolltitel fällt auf 1,5 % — richtig, aber nicht wegen β, sondern weil
seine Qualität nahe null liegt.

## Vergleich

| Titel | Z. | quality | β | raw | pCTR | Band | Δ Baseline |
|---|---:|---:|---:|---:|---:|---|---:|
| Balkonkraftwerk: Was Sie wissen sollten | 39 | 3,60 | 94,8 % | 3,41 | **4,9 %** | niedrig | Baseline |
| Balkonkraftwerk: 1,5 bis 10 kWh am Tag – daran liegt es | 55 | 6,69 | 96,5 % | 6,46 | **14,5 %** | top | **+9,6 pp** |
| KI Team erstellen mit Claude (für Anfänger) | 43 | 6,35 | 98,2 % | 6,24 | **13,8 %** | hoch | +8,9 pp |
| Das Geldsystem kippt gerade – und keiner merkt es | 49 | 4,89 | 79,0 % | 3,86 | **6,0 %** | mittel | +1,1 pp |
| Du wirst nicht glauben, was dann passierte | 42 | 1,31 | 66,8 % | 0,87 | **1,5 %** | niedrig | −3,4 pp |

Spannweite 13,0 Prozentpunkte. Entscheidungsspalte ist Δ, nicht der Absolutwert — siehe Methodik.

## Dimensionsprofil: Baseline gegen Sieger

| Dimension | Gewicht | Baseline | Sieger | Differenz im Beitrag |
|---|---:|---:|---:|---:|
| `entity_density` | 22 % | 4,0 | 6,5 | +0,55 |
| `topic_clarity` | 18 % | 6,0 | 8,5 | +0,45 |
| `informational_value` | 16 % | 2,0 | 8,5 | **+1,04** |
| `freshness_signal` | 12 % | 1,0 | 2,0 | +0,12 |
| `engagement_depth` | 10 % | 3,0 | 7,5 | +0,45 |
| `title_formatting` | 8 % | 4,0 | 6,0 | +0,16 |
| `natural_authority` | 8 % | 5,0 | 7,5 | +0,20 |
| `visual_promise` | 6 % | 3,0 | 5,0 | +0,12 |

Der Unterschied entsteht fast vollständig bei `informational_value`: „Was Sie wissen sollten"
verspricht, dass es Information gäbe. „1,5 bis 10 kWh am Tag – daran liegt es" nennt sie und
kündigt die Erklärung an. Das ist ein Anker-Sprung von 2 auf 8,5.

## Der größte Hebel

Für die Baseline meldet das Skript `entity_density` mit **1,32 offenen Qualitätspunkten** — die
schwerste Dimension bei nur 4 von 10. Konkret fehlt: eine zweite Entität neben
„Balkonkraftwerk". Ein Fachbegriff mit Zahl („800 Watt", „Wechselrichter") oder eine Institution
(„Marktstammdatenregister") hebt die Dimension und trägt gleichzeitig `informational_value`.

Die drei schwächsten Beiträge der Baseline: `freshness_signal`, `visual_promise`,
`engagement_depth`.

## Empfehlung

**„Balkonkraftwerk: 1,5 bis 10 kWh am Tag – daran liegt es"** — Formel Zahlen-Kontrast, vom
Skript in den Merkmalen als solche erkannt.

Mit einer Einschränkung: 55 Zeichen liegen unter dem Richtwert von 70–95, der Titel lässt also
Platz ungenutzt. Ausgebaut, ohne die Aussage zu verwässern:
**„Balkonkraftwerk-Ertrag: 1,5 bis 10 kWh am Tag – an diesen drei Faktoren liegt es"** (79 Zeichen,
im optimalen Band, plus eine Zahl mehr).

**Kein Veto ausgesprochen** — der höchste pCTR-Wert und der `clickbait_score` von 1,0 fallen hier
zusammen. Wäre der Sieger bei ≥ 6 gelandet, würde er nicht empfohlen.

## Was der Clickbait-Kontrolltitel zeigt

„Du wirst nicht glauben, was dann passierte" bekommt `clickbait_score` 9,5 und β = 66,8 %. Der
Absturz auf 1,5 % kommt aber überwiegend aus der Qualität (1,31), nicht aus β — der maximale
β-Abzug beträgt nur 35 %.

Gegenprobe mit konstruierten Werten:

| Fall | quality | β | raw | pCTR | Band |
|---|---:|---:|---:|---:|---|
| alle Dimensionen 8,0 · kein Clickbait | 8,00 | 100 % | 8,00 | 18,5 % | top |
| alle Dimensionen 8,0 · **Clickbait 10** | 8,00 | 65 % | 5,20 | 10,2 % | hoch |
| alle Dimensionen 10,0 · **Clickbait 10** | 10,00 | 65 % | 6,50 | 14,6 % | **top** |

Ein maximal manipulativer Titel kann im Modell also „top" erreichen. Genau dafür existiert das
Veto außerhalb der Formel.

## Methodik

**Gemessen** mit `pctr.py features`: Zeichenzahl und Längenband, Zahlen, Einheiten, Jahresangaben,
Ansprache, Versalien, Autoritäts-, Frische- und Superlativ-Marker, Clickbait-Lexikon, erkannte
Formeln, Struktur, Position der Kernentität.

**Bewertet** nach den Ankern in `references/dimensionen.md`, alle fünf Titel in einem Durchgang,
damit die Werte untereinander konsistent sind.

**Gerechnet** mit `pctr.py score` nach der Formel des pCTR Predictors von metehan.ai, unverändert
übernommen. Handrechnung gegengeprüft: Baseline quality 3,60 · β 0,9475 · raw 3,41 · pCTR 4,89 %.

**Warum der Absolutwert nicht als CTR-Prognose gilt:** Der Sigmoid-Mittelpunkt raw = 5,5 ergibt
11,25 % — das ist der beobachtete CTR-Durchschnitt von News-Seiten in Discover. Ein
durchschnittlicher Titel bekommt dadurch einen Wert am oberen Ende der realen Bandbreite
(News rund 11 %, Non-News rund 6 %, Arbeitsziel 7–9 %). Der systematische Versatz wirkt auf alle
Varianten gleich, deshalb ist das **Delta** belastbar und der Absolutwert nicht.

**Geschätzt statt geprüft:** Die `clickbait_score`-Werte, weil zu keinem der fünf Titel der
Artikeltext vorlag. Nur mit Text ist prüfbar, ob ein Titel einlöst.

**Nicht Teil dieser Analyse:** Titelbild und Feed-Karte (→ `discover-feedkarte`), Artikeltext und
Entitätenabdeckung (→ `discover-content-optimizer`). Und: ob der Artikel überhaupt Impressionen
bekommt, entscheidet die Eligibility-Stufe vor dem Titel.
