# Discover-Analyse: „Balkonkraftwerk: Was Sie wissen sollten"

Beispielausgabe des Skills auf `tests/sample_de_schwach.txt` — ein bewusst inhaltsleerer
Ratgebertext. Zeigt, wie der Bericht aussieht, wenn ein Text die Erwartungen nicht erfüllt.

**Domain-Profil:** E-Commerce (Kaufberatung) · **Sprache:** de · **207 Wörter** ·
**Analyse:** 2026-08-06

## Discover Content Score: 32 / 100 — Nicht Discover-fähig

Der Text nennt sein Thema, aber er beantwortet keine einzige Frage prüfbar: keine Zahl, keine
benannte Quelle, kein Preis, kein Rechtsstand. Der größte Hebel ist nicht die Headline, sondern
die Faktenbasis — ohne mindestens drei belegte Zahlen bleibt jede Headline-Variante schwach.
Aufwand für die Top-3-Maßnahmen: rund 90 Minuten Recherche und Ergänzung.

| Dimension | Punkte | Befund |
|-----------|-------:|--------|
| Entitäten-Abdeckung und -Tiefe | 6 / 25 | 4 von 12 erwarteten Kernentitäten vorhanden; nur eine kontextualisiert |
| Headline und Einstieg | 7,6 / 20 | Headline ohne Fakt (Rubrik 4,0/10), Lead liefert die Antwort nicht |
| Semantische Vollständigkeit | 6 / 20 | Vier Konzepte mit Relevanz ≥ 7 fehlen vollständig |
| Struktur und Lesbarkeit | 8 / 15 | Satz- und Absatzlängen gut, Zwischenüberschriften ohne Substanz |
| Vertrauen und Maschinenlesbarkeit | 4 / 20 | Faktendichte 0,00 je 100 Wörter, keine benannte Quelle |

Der Deckel „D1 < 12 Punkte → maximal 65 gesamt" greift, ist hier aber nicht bindend.

## Top-3-Maßnahmen

**1. Ertragszahlen mit Ausrichtungsbezug ergänzen** — 40 Min · +11 Punkte (D5 5a: 0→3, D1 1a/1b, D3 3a)
Der Satz „nur so lässt sich ein guter Ertrag erzielen" ist die zentrale Leerstelle. Ersetzen durch
eine Spanne mit Bedingung. Vorschlag:
> „Ein 800-Watt-Balkonkraftwerk liefert bei Südausrichtung und 30 Grad Neigung rund 900 kWh im
> Jahr. Senkrecht am Balkongeländer sind es nach Angaben der Verbraucherzentrale NRW etwa
> 25 bis 30 Prozent weniger."

**2. Rechtsstand konkret benennen** — 25 Min · +7 Punkte (D1 1a, D5 5b/5c, D3 3a)
„Auch die Anmeldung sollte man nicht vergessen" nennt weder wo noch wie. Vorschlag:
> „Die Anmeldung beim Netzbetreiber ist seit dem Solarpaket I vom Mai 2024 entfallen. Bleibt die
> Registrierung im Marktstammdatenregister der Bundesnetzagentur — online, kostenlos, etwa
> zehn Minuten."

**3. Abschnitt „Wann es sich nicht lohnt" ergänzen und „Fazit" ersetzen** — 25 Min · +6 Punkte (D3 3a, D4 4a/4d)
Der Fazit-Absatz wiederholt nur die Einleitung und enthält keinen eigenen Fakt. Er wird durch das
Ausschlusskriterium ersetzt — das ist im Profil E-Commerce fast immer das fehlende Konzept mit der
höchsten Relevanz.

**Erreichbarer Score nach Umsetzung: 56 / 100** (Band „Mittel"). Für „Solide" wären zusätzlich
Wechselrichter, Eigenverbrauchsquote und Anschaffungspreis nötig.

## Modul 1 — Entitäten

**Vorhanden:** Konzepte: Balkonkraftwerk, Solaranlage, Strompreise, Stromkosten, Ausrichtung,
Ertrag, Anmeldung, Strombedarf, Versorger. Organisationen, Personen, Orte, Produkte, Ereignisse:
**keine.** Für eine Kaufberatung ist das ein Befund, kein Zufall — ohne Institution, Norm oder
Anbieter fehlt jeder Ankerpunkt für Entitäts-Disambiguierung.

**Erwartungsraum** (aus Modellwissen abgeleitet, nicht aus SERP-Daten — schwächerer Beleg):

| Fehlende Entität | Typ | Priorität | Warum relevant | Einbau |
|---|---|---|---|---|
| Marktstammdatenregister / Bundesnetzagentur | Organisation | **Hoch** | Die einzige verbleibende Pflicht; der Text warnt vor „Problemen", ohne zu sagen wovor | Abschnitt „Worauf man achten sollte", 2 Sätze |
| 800-Watt-Einspeisegrenze / Solarpaket I | Konzept / Ereignis | **Hoch** | Bestimmt, welche Anlage überhaupt zulässig ist; Rechtsstand seit Mai 2024 geändert | neuer Absatz nach Absatz 2 |
| Ertrag in kWh | Konzept | **Hoch** | „guter Ertrag" ist ohne Zahl unprüfbar — Kernfrage der Kaufentscheidung | Abschnitt „Worauf man achten sollte" |
| Anschaffungspreis und Amortisation | Konzept | **Hoch** | „langfristig Stromkosten sparen" ohne Preis und Zeitraum trägt keine Entscheidung | neuer Absatz vor dem Schluss |
| Wechselrichter | Produkt | Mittel | Das bauteilbestimmende Element; ohne ihn ist „800 Watt" nicht erklärbar | Definitionssatz in Absatz 2 |
| Eigenverbrauchsquote | Konzept | Mittel | Entscheidet über die Ersparnis stärker als der Ertrag | im Ertragsabsatz |
| Schuko-Stecker / VDE V 0126-95 | Produkt / Norm | Mittel | Beantwortet die häufigste Laienfrage: darf ich das selbst einstecken | Abschnitt Installation |
| Speicheroption | Produkt | Niedrig | Steigert die Eigenverbrauchsquote, ist aber kein Einstiegsthema | ein Satz mit interner Verlinkung |

**Beziehungen, die der Text herstellt:** Balkonkraftwerk —[ist ein]→ Solaranlage ·
Balkonkraftwerk —[reduziert]→ Strombedarf vom Versorger.

**Nicht verknüpfte Paare, die verknüpft sein müssten** — die wertvollsten Befunde:
Ausrichtung ↔ Ertrag (Jaccard 0,33, aber ohne Kausalaussage: der Text sagt, dass die Ausrichtung
wichtig ist, nie warum) · Strompreise ↔ Stromkosten (Jaccard 0,00 — Preis und Ersparnis werden
nie im selben Satz verbunden) · Anmeldung ↔ Netzbetreiber (Jaccard 0,00, Netzbetreiber fehlt ganz).

## Modul 2 — Content-Optimierung

### Headline

Original: **„Balkonkraftwerk: Was Sie wissen sollten"** — 39 Zeichen, **Rubrik 4,0 / 10**
K1 Konkretheit 0 (keine Zahl, kein Eigenname, kein Ergebnis) · K2 Neugier-Lücke 1 (Kategorierahmen
ohne definierte Lücke) · K3 Relevanz 1 („Sie", aber keine benannte Zielgruppe) · K4 stärkster Fakt 0
(der Text enthält keinen) · K5 Feed-Tauglichkeit 2 (39 Zeichen, Kernentität vorn).

| Variante | Zeichen | Score | Formel |
|---|---:|---:|---|
| Balkonkraftwerk: Lohnt sich das auf deinem Balkon? | 49 | **6,0** | Entscheidungshilfe |
| Balkonkraftwerk montieren: was Laien selbst schaffen | 51 | **6,0** | How-to + Hindernis |
| Balkonkraftwerk: die Ausrichtung entscheidet über den Ertrag | 59 | **6,0** | Konträrer Ansatz |
| Balkonkraftwerk 2026: was vor dem Kauf zu klären ist | 51 | **5,0** | Trend-Hook |
| Balkonkraftwerk: so viel Strom sparst du im Jahr | 47 | **4,0** | Kosten-Hook |

Die beste Variante liegt 2,0 Punkte über dem Original — die Empfehlungsschwelle von 1,5 ist
überschritten, aber alle Varianten bleiben im unteren Drittel. **Grund: keine Variante kann über
6,0 kommen, weil K1 und K4 einen Fakt aus dem Text verlangen und der Text keinen hat.** Das
Headline-Problem ist ein Inhaltsproblem. Nach Umsetzung von Maßnahme 1 sind Varianten im Bereich
8,0 möglich, etwa „Balkonkraftwerk: 900 kWh im Jahr — wenn die Ausrichtung stimmt" (K1 2, K4 2).

Der Kosten-Hook bekommt bewusst nur 4,0: er verspricht eine Sparsumme, die der Text nicht
einlöst. Uneingelöste Versprechen kosten in Discover doppelt, weil die Klickqualität in die
Bewertung zurückfließt.

Die Jahreszahl im Trend-Hook ist nur zulässig, wenn der Text einen echten Aktualitätsbezug
bekommt (Maßnahme 2 liefert ihn mit „seit Mai 2024").

### Semantische Anreicherung

1. **Absatz 2** — „Solaranlage" wird als Definition benutzt, ist selbst aber undefiniert.
   > „Ein Balkonkraftwerk besteht aus einem oder zwei Solarmodulen und einem Wechselrichter, der
   > den Gleichstrom der Module in haushaltsüblichen Wechselstrom umwandelt und über eine
   > Steckdose ins Hausnetz einspeist."
2. **Absatz 3** — „Studien zeigen, dass sich die Anschaffung lohnt" ist eine Quellenbehauptung
   ohne Quelle. Entweder Studie benennen oder den Satz ersetzen; als vager Verweis schadet er
   der Vertrauensbewertung mehr, als er nützt.
3. **Absatz 4** — „da sonst Probleme entstehen können" nennt keine Folge. Konkretisieren:
   welche Pflicht, welche Konsequenz.

### Topic-Cluster

| Cluster | Absätze | Anteil | Bewertung |
|---|---|---:|---|
| Motivation / Marktlage | 1 | 21 % | angemessen, aber ohne Zahl |
| Funktionsweise | 2 | 20 % | zu dünn für die Kaufintention |
| Nutzenversprechen | 3 | 19 % | reine Behauptungen |
| Kaufkriterien | 4 | 23 % | der wichtigste Cluster, inhaltlich der leerste |
| Zusammenfassung | 5 | 17 % | ohne eigenen Beitrag |

Ein einzelnes Thema, sauber gebündelt — die Gewichtung ist aber falsch: 36 % des Textes gehen
für Motivation und Zusammenfassung weg, während der entscheidungsrelevante Cluster keine
Substanz hat.

### Struktur

Satz- und Absatzlängen sind gut (Ø 12,2 bzw. 34,5 Wörter, kein Satz über 25 Wörter, kein Absatz
über 120 Wörter). Lesbarkeit 57,9 (Flesch-Amstad, Band „mittel") liegt im Zielbereich.

Die drei Zwischenüberschriften tragen keine Entität und keinen Fakt. Konkret:
„Die Vorteile" → „Was ein Balkonkraftwerk im Jahr einspart" ·
„Worauf man achten sollte" → „Ausrichtung, Anmeldung, Wechselrichter: die drei Stellschrauben" ·
„Fazit" ersetzen durch „Wann sich ein Balkonkraftwerk nicht lohnt".

Keine Liste und keine Tabelle im Text. Die drei Stellschrauben aus Absatz 4 sind der natürliche
Kandidat für eine Aufzählung.

### Interne Verlinkung

| Ankertext | Zielthema | Begründung |
|---|---|---|
| Registrierung im Marktstammdatenregister | Anleitung Marktstammdatenregister | vertieft eine Hoch-Prioritäts-Entität, die im Text nur gestreift wird |
| optimale Ausrichtung und Neigung | Ertragsvergleich nach Ausrichtung | Ausrichtung ist die zentrale Kaufentscheidung und bleibt hier unbelegt |
| Balkonkraftwerk mit Speicher | Speicher-Ratgeber | fängt die Anschlussfrage nach der Eigenverbrauchsquote auf |

Die Zielseiten sind Themenvorschläge — ob sie auf der Domain existieren, wurde nicht geprüft.

### Wettbewerbs-Gap

Nicht durchgeführt: kein Vergleichstext geliefert. Ohne Vergleichstext wird nicht geraten, was
Wettbewerber schreiben.

## Modul 3 — Schema-Markup

Typ: `Article`. `NewsArticle` ist nicht angebracht — der Text ist zeitlos formuliert und hat
keinen Anlass. Sobald Maßnahme 2 umgesetzt ist (Rechtsstand mit Datum), wird `dateModified`
zum tragenden Feld.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Balkonkraftwerk: Lohnt sich das auf deinem Balkon?",
  "description": "Was ein Balkonkraftwerk im Jahr einspart, welche Ausrichtung sich lohnt und welche Anmeldung noch nötig ist.",
  "datePublished": "{{DATUM_ISO_MIT_ZEITZONE}}",
  "dateModified": "{{DATUM_ISO_MIT_ZEITZONE}}",
  "inLanguage": "de-DE",
  "isAccessibleForFree": true,
  "articleSection": "Energie",
  "author": {
    "@type": "Person",
    "name": "{{AUTOR_NAME}}",
    "url": "{{AUTOR_PROFIL_URL}}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{{PUBLISHER_NAME}}",
    "logo": { "@type": "ImageObject", "url": "{{LOGO_URL}}" }
  },
  "image": {
    "@type": "ImageObject",
    "url": "{{BILD_URL}}",
    "width": 1200,
    "height": 675
  },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "{{ARTIKEL_URL}}" },
  "about": [
    { "@type": "Thing", "name": "Balkonkraftwerk",
      "sameAs": "https://de.wikipedia.org/wiki/Steckersolarger%C3%A4t" },
    { "@type": "Thing", "name": "Photovoltaik",
      "sameAs": "https://de.wikipedia.org/wiki/Photovoltaik" },
    { "@type": "Thing", "name": "Eigenverbrauch" }
  ],
  "mentions": [
    { "@type": "Organization", "name": "Bundesnetzagentur",
      "sameAs": "https://de.wikipedia.org/wiki/Bundesnetzagentur" }
  ]
}
```

**Vom Kunden zu füllen:** `{{DATUM_ISO_MIT_ZEITZONE}}`, `{{AUTOR_NAME}}`, `{{AUTOR_PROFIL_URL}}`,
`{{PUBLISHER_NAME}}`, `{{LOGO_URL}}`, `{{BILD_URL}}`, `{{ARTIKEL_URL}}`.

**Validierung**

| Block | Status | Befund |
|---|---|---|
| Syntax | ✅ | valides JSON-LD, `@context` korrekt, keine doppelten Keys |
| Pflichtfelder | ⚠️ | alle vorhanden, sieben als Platzhalter — vor Veröffentlichung füllen |
| Google-Richtlinien | ⚠️ | `headline` 49 Zeichen ✅ · `author` als Objekt ✅ · `image` mit Maßen und 1200 px ✅, URL fehlt · `datePublished` muss ISO 8601 mit Zeitzone sein |
| Discover-Spezifika | ⚠️ | `about[]` gesetzt, zwei von drei mit `sameAs` ✅ · `mentions` nur ein Eintrag, weil der Text keine weiteren Institutionen nennt — wächst mit Maßnahme 2 · `headline` weicht bewusst vom H1 ab, muss mit dem geplanten `og:title` übereinstimmen |

## Modul 4 — Keyword-Analyse

**Thematische Kernbegriffe** (häufig und über viele Absätze verteilt — die Klammer des Textes):
balkonkraftwerke · anschaffung · balkon · balkonkraftwerk · erzeugen · lohnt · sparen · strom ·
verbraucher · installation

**TF-IDF-Spitzen** (lokal dichte Terme): vorteile · balkonkraftwerke · anschaffung · balkon ·
erzeugen · lohnt

Die beiden Listen sind fast identisch. Das klingt nach Fokus, ist aber ein Substanzbefund: Es
gibt keine lokal verdichteten Unterthemen, weil kein Absatz ein Thema fachlich ausführt. Ein
Text mit Substanz zeigt hier Spitzen wie „Wechselrichter", „Eigenverbrauchsquote" oder
„Marktstammdatenregister". Zum Vergleich der starke Text zum gleichen Thema: dort stehen
kwh · jahresertrag · watt · neigung in den Kernbegriffen.

**Primäre Keywords:** Balkonkraftwerk · Ertrag kWh *(noch nicht im Text)* · Ausrichtung ·
Anmeldung Marktstammdatenregister *(noch nicht im Text)* · Kosten und Amortisation *(noch nicht
im Text)* · Wechselrichter *(noch nicht im Text)*

**Sekundäre Keywords:** Eigenverbrauch · 800 Watt · Solarpaket I · Neigungswinkel · Schuko ·
Verschattung · Speicher · Netzbetreiber · Modulleistung Wp · Stromkosten sparen

**Wichtigkeit** (aus Position, TF, Absatz-Spread, Rolle in der Suchintention):
Balkonkraftwerk 9,5 · Ertrag kWh 8,8 · Kosten/Amortisation 8,5 · Ausrichtung 7,9 ·
Anmeldung MaStR 7,4 · Wechselrichter 6,8 · Eigenverbrauch 6,2 · Speicher 4,5

**Cluster:** Technik (Wechselrichter, Modulleistung, 800 Watt) · Ertrag (kWh, Ausrichtung,
Neigung, Verschattung) · Wirtschaftlichkeit (Preis, Amortisation, Eigenverbrauch, Stromkosten) ·
Recht (MaStR, Solarpaket I, Netzbetreiber, Schuko/VDE)

Von vier Clustern ist einer schwach belegt und drei fehlen praktisch ganz.

**Platzierung**

| Term | Headline | Lead | H2 | Schluss | Status |
|---|---|---|---|---|---|
| Balkonkraftwerk | ✅ | ✅ | ❌ | ✅ | vorhanden, in H2 fehlend |
| Ertrag kWh | ❌ | ❌ | ❌ | ❌ | fehlt vollständig |
| Kosten / Amortisation | ❌ | ❌ | ❌ | ❌ | fehlt vollständig |
| Ausrichtung | ❌ | ❌ | ❌ | ❌ | nur im Fließtext, ohne Zahl |
| Anmeldung MaStR | ❌ | ❌ | ❌ | ❌ | nur „Anmeldung", unbestimmt |

**Long-Tail**, jeweils mit der Nutzerfrage und der Stelle, an der sie beantwortbar ist:
„wie viel kWh Balkonkraftwerk im Jahr" (Ertragsabsatz) · „Balkonkraftwerk anmelden 2026 Pflicht"
(Abschnitt Kaufkriterien) · „Balkonkraftwerk senkrecht am Geländer Ertrag" (Ertragsabsatz) ·
„lohnt sich Balkonkraftwerk bei Nordbalkon" (neuer Ausschluss-Abschnitt) ·
„Balkonkraftwerk 800 Watt oder 600 Watt" (Technikabsatz)

## Modul 5 — Semantische Abdeckung

**Entitäten-Integration** (Kernentitäten, Mittelwert 0,354)

| Entität | Nennungen | Absatz-Spread | Score | Band |
|---|---:|---:|---:|---|
| Anmeldung | 1 | 0,17 | 0,17 | isoliert |
| Solaranlage | 1 | 0,17 | 0,30 | isoliert |
| Ausrichtung | 1 | 0,17 | 0,41 | mittel |
| Ertrag | 1 | 0,17 | 0,41 | mittel |
| Balkonkraftwerk | 5 | 0,83 | 0,48 | mittel |

Belegentitäten (Strompreise 0,17, Stromkosten 0,17) sind aus dem Mittelwert ausgenommen — sie
werden in einem gut recherchierten Text zu Recht nur einmal genannt. Hier ist ihr Wert allerdings
selbst ein Befund: es gibt gar keine Institutionen oder Normen als Belegentitäten.

**Auffällig:** „Balkonkraftwerk" hat mit 5 Nennungen und einem Absatz-Spread von 0,83 die
höchste Präsenz, kommt aber nur auf 0,48 — weil im Umfeld der Nennungen keine Zahl und keine
Vergleichsaussage steht. Das ist das Muster eines Textes, der sein Thema oft nennt und nie
ausführt.

**„Anmeldung", Score 0,17** — einzige Nennung:
> „Auch die Anmeldung sollte man nicht vergessen, da sonst Probleme entstehen können."
Kein Adressat, keine Frist, keine Folge. Für Discover heißt das: Der Text trägt die Entität
„Anmeldepflicht Balkonkraftwerk" nicht, obwohl er sie erwähnt — er kann für diese Nutzerabsicht
nicht ausgespielt werden. Ersatz siehe Maßnahme 2.

**Fehlende semantische Konzepte**

| Konzept | Relevanz | Unbeantwortete Nutzerfrage | Umsetzung |
|---|---:|---|---|
| Konkreter Jahresertrag | 10 | „Wie viel Strom bekomme ich tatsächlich?" | Maßnahme 1, Ertragsabsatz |
| Anschaffungspreis und Amortisation | 9 | „Wann habe ich das Geld zurück?" | neuer Absatz mit Preisspanne und Rechnung |
| Ausschlusskriterium | 8 | „Für wen lohnt es sich nicht?" | Maßnahme 3, ersetzt das Fazit |
| Rechtsstand und Anmeldeweg | 8 | „Muss ich das anmelden und wo?" | Maßnahme 2 |
| Mietrecht / Zustimmung von Vermieter oder WEG | 7 | „Darf ich das als Mieter überhaupt?" | zwei Sätze im Abschnitt Kaufkriterien |
| Wartung und Lebensdauer | 5 | „Was kommt später an Kosten?" | ein Satz, oder interner Link |

## Methodik

**Berechnet** mit `textstats.py`: Dokument-, Satz- und Absatzstatistik, Lesbarkeit
(Flesch-Amstad, 57,9), Headline-Zeichenzahl, Answer-First-Heuristik des Leads, Faktendichte
(0,00 spezifische Angaben je 100 Wörter), thematische Kernbegriffe und TF-IDF-Spitzen,
Trust-Marker, Integrations-Score und Kookkurrenzmatrix der Entitäten.

**Bewertet** nach der Rubrik in `references/scoring.md`: Entitäten-Abdeckung und
Kontextualisierung, Headline-Rubrik, Relevanz fehlender Konzepte, Themenfokus, Qualität der
Zwischenüberschriften, benannte Quellen.

**Nicht gemessen, sondern abgeleitet:** Der Erwartungsraum der Kernentitäten stammt aus
Modellwissen, nicht aus SERP-Daten. Mit angebundenen SERP-Daten wäre er belastbarer. Die Liste
ist damit eine begründete Vermutung.

**Nicht Teil dieser Analyse:** Titelbild und dessen Maße, `og:image`, `max-image-preview`,
News-Sitemap, Startseiten-Prominenz, Domain-Autorität und Publisher-Status. Die Bildwirkung ist
neben der Headline der stärkste CTR-Hebel im Feed — dafür ist der Skill
`discover-artikel-optimierer` an der veröffentlichten URL zuständig. Die Headline-Scores sind
Rubrik-Werte, keine CTR-Prognose.
