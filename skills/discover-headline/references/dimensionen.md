# Die acht Dimensionen — Bewertungsanker

Jede Dimension wird von 0 bis 10 bewertet. Die Gewichte stammen aus dem pCTR-Modell und sind
fest; die Anker hier sind der Teil, den das Originaltool **nicht** veröffentlicht — ohne sie wäre
die Bewertung beliebig und zwei Durchläufe kämen zu verschiedenen Ergebnissen.

Vorgehen pro Dimension: Anker suchen, der zutrifft, Zwischenwerte nur wenn zwei Anker gleichzeitig
greifen. Jede Vergabe wird im Bericht mit einem Satz begründet, der sich auf den Titeltext oder
einen gemessenen Wert aus `pctr.py features` bezieht.

| Dimension | Gewicht |
|-----------|--------:|
| `entity_density` | 22 % |
| `topic_clarity` | 18 % |
| `informational_value` | 16 % |
| `freshness_signal` | 12 % |
| `engagement_depth` | 10 % |
| `title_formatting` | 8 % |
| `natural_authority` | 8 % |
| `visual_promise` | 6 % |

---

## entity_density (22 %) — die schwerste Dimension

Wie viele benennbare Entitäten trägt der Titel, und wie spezifisch sind sie? Entitäten sind der
Match-Schlüssel der Personalisierung: der Titel wird gegen Interessenprofile abgeglichen.

- **10** — zwei oder mehr spezifische, disambiguierbare Entitäten (Marke, Produkt mit
  Modellbezeichnung, benannte Person, Institution, Norm), plus ein Fachbegriff
- **7** — eine starke spezifische Entität plus ein Fachbegriff oder eine Zahl mit Einheit
- **5** — eine klare, aber gattungshafte Entität („Balkonkraftwerk", „E-Auto")
- **3** — nur eine abstrakte Kategorie („Geldsystem", „Künstliche Intelligenz")
- **0** — keine Entität, rein sprachliche Konstruktion

Nicht auf Großschreibung verlassen: im Deutschen sind alle Substantive groß. `capitalized_tokens`
aus dem Feature-Output ist eine Rohbeobachtung, kein Entitätennachweis.

## topic_clarity (18 %)

Ist nach einem Blick klar, **worum es geht** — nicht ob es interessant ist. Diese Dimension
entscheidet über die Klassifikation, und ein falsch klassifizierter Artikel kann nicht schlecht
ranken, er wird der falschen Kohorte gezeigt.

- **10** — Thema und Aussage sind beide eindeutig; ein Leser könnte den Artikelinhalt vorhersagen
- **8** — Thema eindeutig, Aussage angedeutet
- **6** — Thema klar, Aussage offen („Was Sie wissen sollten")
- **4** — Thema nur erschließbar, mehrere Lesarten möglich
- **1** — kein erkennbares Thema

## informational_value (16 %)

Verspricht der Titel eine **prüfbare** Information — oder nur, dass es welche gäbe?

- **10** — konkrete Zahl, Ergebnis oder Vergleich im Titel, dazu die Bedingung
  („1,5 bis 10 kWh am Tag – daran liegt es")
- **7** — konkretes Versprechen ohne Zahl („so bucht Claude direkt in DATEV")
- **5** — Nutzen benannt, aber unbestimmt („so sparst du Stromkosten")
- **2** — Rahmen ohne Inhalt („Was Sie wissen sollten", „Alles über X")
- **0** — verspricht nichts, oder verspricht Sensation statt Information

## freshness_signal (12 %)

Aktualität geht in Sekunden ins Modell ein. Diese Dimension bewertet nur, was der **Titel**
signalisiert — nicht das tatsächliche Alter des Artikels.

- **10** — datierter Anlass oder Rechtsstand („seit Mai 2024", „ab Januar", „neue Pflicht")
- **7** — Jahreszahl oder klare Zeitmarke („2026", „jetzt", „gerade")
- **4** — impliziter Aktualitätsbezug („neu", „kommt")
- **1** — zeitlos formuliert

Wichtig: eine Jahreszahl, die im Artikel keinen Anlass hat, ist kein Freshness-Signal, sondern
eine ungedeckte Behauptung. Dann höchstens 4, und im Bericht vermerken.

## engagement_depth (10 %)

Lädt der Titel dazu ein, **nach** dem Klick weiterzulesen? Diese Dimension trennt Neugier von
Reiz: gemessen wird an Station 05 die Klickqualität, nicht die Klickmenge.

- **10** — Neugier-Lücke mit klarem Gegenstand: der Leser weiß, worum es geht, aber nicht die
  Antwort, und die Antwort ist substanziell
- **7** — Neugier vorhanden, Substanz erwartbar
- **5** — informativ, aber ohne Zugkraft
- **3** — Reiz ohne Gegenstand
- **0** — reiner Klickanreiz, nach dem Klick bleibt nichts

## title_formatting (8 %)

- **10** — 70–95 Zeichen, klare Zweiteilung (Doppelpunkt oder Gedankenstrich), Kernentität in
  den ersten 40 Zeichen, keine Versalien, kein Ausrufezeichen
- **7** — Länge im Rahmen 50–110, saubere Struktur
- **5** — zu kurz (unter 50) und damit ungenutzter Platz, oder leicht über 95
- **3** — über 110 Zeichen, Abschneiden im Feed
- **0** — Versalien-Wörter, mehrere Ausrufezeichen, oder unleserliche Struktur

Werte aus `pctr.py features` übernehmen, nicht schätzen.

## natural_authority (8 %)

Glaubwürdigkeit **ohne** Lautstärke. Autorität entsteht aus benannten Quellen und prüfbaren
Angaben, nicht aus Superlativen.

- **10** — benannte Institution, Studie oder Experte im Titel („Laut Stiftung Warentest")
- **7** — prüfbare Zahlen oder eigene Messung erkennbar, nüchterner Ton
- **5** — sachlich, aber ohne Beleg
- **3** — Superlative oder unbelegte Behauptungen
- **0** — Autoritätsanspruch ohne jede Deckung

## visual_promise (6 %)

Legt der Titel ein starkes Titelbild nahe? Die Karte ist Bild **plus** Titel — ein Titel, der
kein Bildmotiv anbietet, erschwert die Bildarbeit.

- **10** — der Titel nennt etwas Zeigbares: ein Produkt, eine Person, einen Ort, eine Zahl als Badge
- **7** — Bildmotiv naheliegend, aber nicht benannt
- **4** — abstraktes Thema, Bildmotiv muss erfunden werden
- **1** — rein begrifflich, kein Anknüpfungspunkt

---

## clickbait_score (0–10) — separat, kein Qualitätsmerkmal

Die Grenze verläuft am **Einlösen**, nicht an der Emotionalität. Magnetisch heißt: verspricht
viel und liefert. Clickbait heißt: verspricht und liefert nicht.

- **0–1** — nüchtern, kein überschüssiges Versprechen
- **2–3** — emotional, aber vollständig gedeckt
- **4–5** — Zuspitzung, die der Artikel nur teilweise einlöst
- **6–7** — Insiderwissen suggeriert („keiner merkt es", „niemand spricht darüber"), Details
  angedeutet statt genannt
- **8–10** — Vorschauinhalt täuscht Details vor; der Gegenstand wird bewusst verschwiegen
  („Du wirst nicht glauben, was dann passierte")

Das Lexikon in `pctr.py features` liefert Verdachtsmomente, keine Urteile: „keiner merkt es"
kann in einem Text, der genau das belegt, gedeckt sein. Ein Lexikontreffer verlangt eine
Entscheidung mit Begründung, keinen Automatismus.

**Prüffrage:** Kann der Artikel das Versprechen einlösen? Wenn der Artikeltext vorliegt, wird das
geprüft und nicht vermutet. Liegt er nicht vor, wird der Wert als geschätzt markiert.

---

## Das Modell und seine zwei Kalibrierungsschwächen

```
quality = Σ(wᵢ × fᵢ)
β       = 1 − 0,35 × (clickbait / 10)
raw     = quality × β
pCTR    = 0,5 % + (22 % − 0,5 %) × σ(0,65 × (raw − 5,5))
```

Die Formel wird **unverändert** übernommen, damit die Werte mit dem Originaltool vergleichbar
bleiben. Zwei Eigenschaften muss man dabei kennen und im Bericht benennen:

**1. Der Mittelpunkt liegt zu hoch.** raw = 5,5 ergibt 11,3 % pCTR. Das ist der beobachtete
CTR-Durchschnitt von News-Seiten in Discover — also bekommt ein durchschnittlicher Titel eine
Vorhersage am oberen Ende der realen Bandbreite und das Band „hoch". Beobachtete Werte zum
Vergleich: News-Seiten rund 11 %, Non-News rund 6 %, Arbeitsziel 7–9 %, unter 5 % Handlungssignal.

**Konsequenz für den Bericht:** Der absolute pCTR-Wert wird **nicht** als erwartete CTR
ausgegeben. Verwendet wird der **Abstand zwischen den Varianten** in Prozentpunkten — dafür ist
das Modell brauchbar, weil derselbe systematische Versatz auf alle Varianten wirkt.

**2. Der Clickbait-Abzug ist zu schwach.** β kappt maximal 35 % der Qualität. Gemessen:

| Fall | quality | β | raw | pCTR | Band |
|------|--------:|--:|----:|-----:|------|
| alle Dimensionen 5,5 · kein Clickbait | 5,50 | 100 % | 5,50 | 11,3 % | hoch |
| alle 8,0 · kein Clickbait | 8,00 | 100 % | 8,00 | 18,5 % | top |
| alle 8,0 · **Clickbait 10** | 8,00 | 65 % | 5,20 | 10,2 % | hoch |
| alle 10,0 · **Clickbait 10** | 10,00 | 65 % | 6,50 | 14,6 % | **top** |

Ein maximal manipulativer Titel kann also das Band „top" erreichen. Das widerspricht der
Mechanik, die das β modellieren soll: Klickqualität wird nach dem Navboost-Modell bewertet, und
die historische CTR hängt **pro URL** — ein Titel, der klickt aber nicht einlöst, belastet diese
URL dauerhaft.

**Deshalb gilt außerhalb der Formel ein Veto:** Bei `clickbait_score` ≥ 6 wird die Variante
**nicht** als Empfehlung ausgesprochen, unabhängig vom pCTR-Wert. Die Begründung steht im Bericht,
und es wird eine gedeckte Alternative vorgeschlagen. Das Veto wird ausgewiesen, nicht versteckt —
der Kunde soll sehen, dass die Zahl höher war und warum sie nicht gilt.
