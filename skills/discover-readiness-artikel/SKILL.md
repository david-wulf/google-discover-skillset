---
name: discover-readiness-artikel
description: >
  Analysiert veröffentlichte Artikel anhand ihrer URL auf Google-Discover-Tauglichkeit.
  Prüft Headlines, OG-Tags, Titelbild, Entitäten-Vollständigkeit, News-Sitemap, Startseiten-Prominenz,
  strukturierte Daten und E-E-A-T-Signale. Verwende diesen Skill immer, wenn jemand einen Artikel
  für Google Discover optimieren, prüfen oder bewerten will — auch bei Begriffen wie "Discover-Check",
  "Discover-Analyse", "Artikel für Discover optimieren", "Discover-Audit", "CTR verbessern für Discover",
  oder wenn eine URL mit der Bitte um Discover-Optimierung eingereicht wird. Auch auslösen, wenn jemand
  fragt, warum ein Artikel in Discover nicht performt oder wie man Discover-Traffic steigern kann.
---

# Google Discover Optimizer

Dieser Skill analysiert einen veröffentlichten Artikel anhand seiner URL und gibt konkrete, priorisierte Empfehlungen zur Steigerung der Discover-Sichtbarkeit und CTR.

## Ablauf

Der Skill arbeitet in drei Phasen. Die zentrale Regel: Jede Phase muss echte, konkrete Ergebnisse liefern — niemals leere Platzhalter oder "Ausstehend"-Felder im finalen Bericht.

### Phase 1: Daten sammeln

Ziel ist es, den vollständigen HTML-Quellcode der Seite zu bekommen. Probiere die folgenden Methoden in dieser Reihenfolge, bis eine funktioniert:

**Methode A — web_fetch**: Versuche die URL mit `web_fetch` abzurufen. Das ist der schnellste Weg.

**Methode B — Claude in Chrome**: Falls web_fetch fehlschlägt (Proxy-Fehler, Provenance-Check, Timeout), öffne die URL mit Claude in Chrome (`navigate`-Tool). Lies dann den Seiteninhalt mit `get_page_text` und den HTML-Quellcode mit `javascript_tool` (z.B. `document.head.innerHTML` für Meta-Tags und `document.querySelector('script[type="application/ld+json"]')?.textContent` für strukturierte Daten).

**Methode C — User fragen**: Nur als letzter Ausweg, wenn weder web_fetch noch Chrome verfügbar sind, bitte den User, den HTML-Quellcode zu liefern. Aber: Gib trotzdem schon eine Analyse auf Basis der URL-Struktur und des Domain-Kontexts — der Bericht darf nie leer sein.

Sobald du Zugriff auf die Seite hast, extrahiere folgende Daten:

#### 1.1 Meta-Tags & OG-Tags
Extrahiere diese Werte direkt aus dem HTML-Quellcode (via `javascript_tool` oder im Seitenquelltext). Gib die tatsächlich gefundenen Werte im Bericht an — nicht raten, nicht annehmen.

- `<title>`, `<h1>`, `<meta name="description">`
- `og:title`, `og:image` (die volle URL!), `og:description`, `og:type`
- `<meta name="robots">` — prüfe explizit ob `max-image-preview:large` gesetzt ist. Falls kein robots-Meta-Tag vorhanden ist oder der Wert fehlt, ist das ein gelbes Signal.

JavaScript-Snippet für Chrome:
```js
JSON.stringify({
  title: document.title,
  h1: document.querySelector('h1')?.textContent,
  metaDesc: document.querySelector('meta[name="description"]')?.content,
  ogTitle: document.querySelector('meta[property="og:title"]')?.content,
  ogImage: document.querySelector('meta[property="og:image"]')?.content,
  ogDesc: document.querySelector('meta[property="og:description"]')?.content,
  ogType: document.querySelector('meta[property="og:type"]')?.content,
  robots: document.querySelector('meta[name="robots"]')?.content,
  maxImagePreview: document.querySelector('meta[name="robots"]')?.content?.includes('max-image-preview:large')
})
```

#### 1.2 Strukturierte Daten (JSON-LD)
Extrahiere den vollständigen JSON-LD-Block aus dem Quellcode. Daraus lesen:
- `@type`: Article / NewsArticle / BlogPosting
- `headline`
- `author` (Name + Bild)
- `datePublished`, `dateModified`
- `image` — welche Bild-URL und Bildgröße ist hier hinterlegt? Das ist relevant, weil Google diese neben `og:image` als Bildquelle nutzt.
- `mainEntityOfPage`, `primaryImageOfPage`

JavaScript-Snippet:
```js
document.querySelector('script[type="application/ld+json"]')?.textContent
```
Falls mehrere JSON-LD-Blöcke vorhanden sind:
```js
[...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent)
```

#### 1.3 Artikelinhalt
- Fließtext, Zwischenüberschriften (H2, H3)
- Interne und externe Links
- Genannte Entitäten (Personen, Marken, Produkte, Fachbegriffe, Orte)

#### 1.4 Titelbild — Alle Varianten prüfen

**Wichtig zur Rangfolge:** Die Parsing-Priorität ist hart codiert
**Schema.org JSON-LD → Open Graph → Twitter Cards → HTML-Meta**. `og:image` ist also **nicht** die
primäre Quelle, sondern die zweite Ebene — JSON-LD gewinnt bei Konflikt. Wer nur OG-Tags pflegt,
arbeitet an der falschen Stelle. *(Quelle: Reverse Engineering des Google-App-SDK — starkes Indiz
aus Client-Sicht, keine bestätigte Google-Spezifikation.)*

Prüfe deshalb alle Quellen und vergleiche:

1. **Strukturierte Daten** — `image` im `Article`/`NewsArticle`-JSON-LD, außerdem
   `WebPage` → `primaryImageOfPage` und `mainEntity`/`mainEntityOfPage` → `BlogPosting` → `image`.
   **Höchste Priorität.**
2. **`og:image`** (plus `og:image:secure_url`) — zweite Ebene. Dazu prüfen, ob
   `og:image:width`/`:height` gesetzt sind: sie verhindern Fehl-Skalierung und falschen Zuschnitt.
   Und `og:image:alt`.
3. **`twitter:image`** — dritte Ebene der Fallback-Kette
   (`og:image` → `twitter:image` → `og:image:secure_url` → `twitter:image:src` → generisches `image`).
4. **HTML `<img>`-Tag des Artikelbilds** — `srcset` prüfen, dort listet WordPress oft mehrere Größen
   (720px, 1024px, 1600px). Die größte verfügbare Variante sollte in den deklarierten Quellen stehen.

**Nennen alle Quellen dasselbe Motiv?** Widersprüchliche Angaben sind schlimmer als eine fehlende,
weil Google dann wählt — und die Wahl fällt nicht zwingend auf das gute Bild. Abweichungen im
Bericht benennen.

Ohne abrufbares Thumbnail entsteht **keine Karte** — es gibt keinen Textfallback. Deshalb zusätzlich
prüfen: ist die Bild-URL anonym abrufbar (kein Login, kein Hotlink-Schutz, kein 404), läuft sie über
HTTPS, ist der `Content-Type` ein `image/*`, und wie schnell antwortet das CDN? Download-Erfolg und
Fehlerrate sind eigene Ranking-Signale (`EMBER_FEED_THUMBNAILS_DOWNLOADED`,
`image_load_failure_count`).

JavaScript-Snippet für alle Bild-Varianten:
```js
JSON.stringify({
  ogImage: document.querySelector('meta[property="og:image"]')?.content,
  heroImg: document.querySelector('article img, .entry-content img, .post-thumbnail img')?.src,
  heroSrcset: document.querySelector('article img, .entry-content img, .post-thumbnail img')?.srcset,
  maxImagePreview: document.querySelector('meta[name="robots"]')?.content?.includes('max-image-preview:large')
})
```

**Bewertungskriterien** (Google-Doku, harte Spezifikation):
- **Breite ≥ 1.200 px** — Pflicht. Bei Grenzfällen deutlich darüber gehen: das SDK kennt einen
  ausdrücklichen Negativmarker `LOW_QUALITY_IMAGE`, es gibt also nicht nur „gut genug". Ab 1.600 px
  ist man auf der sicheren Seite
- **Gesamtfläche > 300.000 px** — eigenständige Anforderung, nicht von der Breite abgedeckt. Ein
  1200 × 200-Banner erfüllt die Breite und fällt trotzdem durch. Googles Beispiel: 1280 × 720
- **Seitenverhältnis 16:9**, und beim Zuschnitt müssen die **wichtigen Details im beschnittenen
  Ausschnitt erhalten bleiben** — das verlangt Google ausdrücklich
- Format WebP oder JPEG, kein PNG
- **`max-image-preview:large`** im robots-Meta oder AMP — der einzige harte technische Blocker der
  ganzen Doku. Beim Regex-Lesen aus rohem HTML **beide Anführungszeichen-Varianten** abdecken
  (WordPress schreibt `name='robots'` einfach) und zusätzlich den HTTP-Header `X-Robots-Tag` prüfen,
  der das Meta-Tag überstimmt
- Untauglich laut Doku: generische Motive, ausdrücklich das **Websitelogo**, vollgeschriebene Grafiken

Für die **Bildwirkung** bei echter Kartengröße gibt es den Skill `discover-titelbild` — er rendert
das Bild auf 340 × 190 und 80 × 80 und beurteilt es dort. Ist er verfügbar, dort prüfen statt hier
zu schätzen.

**Im Bericht angeben:**
- Die exakte og:image-URL und ihre Pixelmaße
- Die Bild-URL aus den strukturierten Daten und ihre Pixelmaße (falls abweichend)
- Welche weiteren Größen im srcset verfügbar sind
- Ob `max-image-preview:large` gesetzt ist (ja/nein)

#### 1.5 News-Sitemap prüfen
Rufe `[domain]/news-sitemap.xml` ab. Falls 404, prüfe `/sitemap.xml` und `/sitemap_index.xml` nach News-Sitemap-Referenzen. Prüfe, ob die analysierte URL enthalten ist.

#### 1.6 Startseiten-Prominenz prüfen
Rufe die Startseite der Domain ab. Suche nach einem Link zur analysierten URL. Bewerte die Position: ganz oben (Hero/Header), Mitte, oder nur im Footer/Archiv.

#### 1.7 Vertiefung an die Spezial-Skills abgeben

Drei Hebel werden nicht hier grob mitbeurteilt, sondern von den zuständigen Skills geprüft. Sie
laufen lokal, ohne externe Tools und ohne Ausfallrisiko:

| Hebel | Skill | Was er liefert |
|-------|-------|----------------|
| **Headline** (`og:title`) | `discover-headline` | pCTR-Modell mit acht gewichteten Dimensionen, Clickbait-Abzug, Variantenvergleich mit Delta |
| **Titelbild** | `discover-titelbild` | Spezifikationsprüfung plus Rendering auf echte Kartengröße 340 × 190 und 80 × 80 |
| **Artikeltext** | `discover-content-optimizer` | Entitäten-Abdeckung und -Integration, semantische Lücken, JSON-LD, Keywords |

Für den Hebel mit dem größten sichtbaren Defizit den passenden Skill aufrufen und dessen Ergebnis
übernehmen. Nicht alle drei pauschal — der Bericht soll priorisieren, nicht addieren.

**Historische Notiz:** Frühere Fassungen verwiesen auf drei externe Web-Tools von metehan.ai
(pCTR Predictor, Image-Analyzer, Discover Optimizer). Deren Funktion ist in den Skills oben
nachgebaut, und mindestens zwei waren beim letzten Test nicht funktionsfähig (fehlendes
API-Guthaben bzw. defekter Fallback). Extern bleibt optional der Teaser-Optimizer
(`huggingface.co/spaces/metehan777/neuralseo`) für die `og:description` — kein Blocker.

Falls ein Tool nicht erreichbar ist, überspringe es und vermerke das kurz im Bericht — aber halte deswegen nicht den ganzen Prozess auf. Die Tools liefern zusätzliche Datenpunkte, die Kern-Analyse funktioniert auch ohne sie.

### Phase 2: Analyse

Bewerte den Artikel in sechs Kategorien. Lies `references/discover-kriterien.md` für die detaillierten Bewertungskriterien.

Jede Bewertung muss auf echten, gefundenen Daten basieren. Zitiere konkret, was du gefunden hast (z.B. "Der og:title lautet: '...' — das sind 58 Zeichen").

#### 2.1 Headline & OG:Title
Die Headline ist der wichtigste CTR-Hebel im Discover-Feed. Analysiere sie gründlich:

- Wie lautet der aktuelle `og:title`? Unterscheidet er sich von `<title>` und `<h1>`? (Falls alle drei identisch sind: verpasste Chance — der og:title kann und sollte für Discover separat optimiert werden, ohne die SEO-Rankings zu gefährden)
- CTR-Potenzial bewerten: Klarheit, emotionale Ansprache, Neugier-Balance, Spezifität
- Länge: Richtwert **70–95 Zeichen** für den `og:title`. Darunter bleibt Platz für den Haken
  ungenutzt, über 95 wird im Feed abgeschnitten. Kernentität in die ersten 40 Zeichen
- Folgt die Headline einer bewährten Discover-Formel? (How-to, Nummerierte Liste, Konträrer Ansatz, Trend-Hook, Experten-Zitat — Details in `references/discover-kriterien.md`)

**Headline-Bewertung abgeben:** Der Skill `discover-headline` bewertet den `og:title` über acht
gewichtete Dimensionen mit Clickbait-Abzug und vergleicht bis zu fünf Varianten gegen das
Original — inklusive Delta in Prozentpunkten und dem größten offenen Hebel. Ist er verfügbar,
dort bewerten und das Ergebnis hier übernehmen, statt die Headline zweimal zu beurteilen.

Nur wenn er nicht verfügbar ist: nach den Formeln in `references/discover-kriterien.md` selbst
bewerten und die drei Alternativen begründen.

#### 2.2 Titelbild
- Technische Werte: Breite, Format, Seitenverhältnis
- `max-image-preview:large` gesetzt?
- Inhaltliche Eignung: Zeigt es die Kern-Entität? Emotionen, Close-ups, Gesichter?

#### 2.3 Entitäten-Vollständigkeit
Das ist der wichtigste inhaltliche Check. So gehst du vor:
1. Bestimme das Kernthema des Artikels
2. Identifiziere die erwarteten Kern-Entitäten (Personen, Marken, Produkte, Fachbegriffe, die zum Thema gehören — orientiere dich daran, was in den Top-10-Rankings typischerweise vorkommt)
3. Prüfe für jede Entität: Wird sie nur erwähnt oder auch kontextualisiert?
   - **Definiert**: Was ist es?
   - **Verglichen**: Wie unterscheidet es sich von Alternativen?
   - **In Beziehung gesetzt**: Wie hängt es mit anderen Entitäten zusammen?
   - **Intern verlinkt**: Gibt es einen Link zu vertiefendem eigenem Content?
4. Liste fehlende Entitäten konkret auf

#### 2.4 E-E-A-T Signale
- Autor mit Name und Bild in strukturierten Daten?
- Veröffentlichungsdatum sichtbar?
- Autorenseite mit Bio/Qualifikation vorhanden?
- Externe Quellen verlinkt (seriöse Autoritäten)?

#### 2.5 Technische Discover-Readiness

**Zuerst die zwei Blocker-Tags** — sie halten die Verarbeitung komplett an und tauchen in keinem
SEO-Tool als Fehler auf, weil sie von CMS- oder Übersetzungs-Plugins automatisch injiziert werden:
- **`notranslate`** gesetzt?
- **`nopagereadaloud`** gesetzt?

Wenn ein Artikel gar nicht ausgespielt wird und technisch alles in Ordnung wirkt, ist das der erste
Prüfpunkt.

Dann:
- OG-Tags vollständig und korrekt? Insbesondere `og:image:width`/`:height`, `og:image:alt`,
  `og:site_name` (sonst rät Google den Publisher-Namen aus der Domain)
- **`og:locale`** gesetzt und konsistent mit `hreflang` und `<html lang>`? Der Wert wird gegen die
  Nutzer-Locale gematcht und ist damit **eligibility-relevant**, nicht bloß Darstellung
- **`article:content_tier`** — genau **einer** von `free`, `metered`, `locked`. Mehrere Werte
  erzeugen einen Log-Eintrag. Bei Paywall wahrheitsgemäß setzen: eine als frei ausgegebene
  Locked-Seite erzeugt die enttäuschte Erwartung, die als schlechter Klick gewertet wird
- `max-image-preview:large` gesetzt? Auch den HTTP-Header `X-Robots-Tag` prüfen, er überstimmt das
  Meta-Tag
- Widersprechen sich Schema und OG-Tags? JSON-LD hat Vorrang — Abweichungen benennen
- News-Sitemap: Vorhanden? Artikel enthalten?
- Startseite: Artikel verlinkt? Wie prominent?

**Kennzeichnung:** News-Sitemap, Startseiten-Prominenz und `Article`-Schema stehen **nicht** in
Googles Discover-Doku. Sie können wirken, sind aber Praxis-Heuristik — im Kundenbericht so
kennzeichnen, nicht als „Google verlangt".

#### 2.6 Content-Freshness und URL-Historie
- Veröffentlichungsdatum und letztes Update — beide **sichtbar** am Artikel und konsistent mit
  `datePublished`/`dateModified` im Schema
- Freshness-Gewichtung nach Alter: 1–7 Tage höchste, 8–14 mittlere, 15–30 niedrigste, über 30
  kontinuierlicher Verlust. Merksatz: **erste Stunden = Höhe, erste Woche = Dauer, ab Tag 15 =
  Republishing.** *(Arbeitsmodell aus der SDK-Analyse; der Autor hat die Zuordnung später
  relativiert — nicht als Google-Spezifikation zitieren.)*
- **Kein Freshness-Zwang:** Ältere Inhalte werden laut Google ausgespielt, wenn sie zu den
  Nutzerinteressen passen. Evergreen-Re-Promotion ist gedeckt, nicht bloß ein Trick
- **`dateModified` nie ohne echte inhaltliche Änderung hochsetzen** — das ist die Datums-Variante
  von Clickbait und fällt in dieselbe Richtlinien-Kategorie irreführender Vorschauinhalte

**URL-Historie mitbedenken:** Die historische CTR wird **pro URL** geführt
(`click_count`/`show_count`). Eine URL trägt ihre Feed-Reputation in künftige Ausspielungen mit.
Wenn dieser Artikel schon einmal mit schwacher CTR ausgespielt wurde, wirken Titel- und Bildwechsel
begrenzt — bei grundlegend neuem Aufhänger ist eine **neue URL** die ehrlichere Option. Das gehört
in die Empfehlung, nicht in den Score.

### Phase 3: Ausgabe

Der Bericht muss kompakt und aktionsorientiert sein — kein Template-Filler, keine leeren Tabellen, keine "Ausstehend"-Felder. Jede Zeile muss einen konkreten Befund enthalten.

Struktur:

**Kopf**: URL, Analysedatum, Gesamtscore (1-10)

**Ampel-Übersicht**: Eine kompakte Tabelle mit allen 6 Kategorien, ihrer Ampelfarbe und einem Einzeiler-Befund.

**Detail pro Kategorie** (nur wo Handlungsbedarf besteht — grüne Kategorien kurz abhandeln):
- Was wurde gefunden (konkretes Zitat/Wert)
- Ampel + Begründung
- Konkrete Empfehlung (was genau ändern, mit Beispiel)

**Top-3-Prioritäten**: Die drei Maßnahmen mit dem größten erwarteten Impact auf Discover-CTR, mit geschätztem Aufwand.

**3 alternative Headlines**: Jede Headline muss eine klar andere Discover-Formel nutzen (z.B. eine How-to, eine mit Zahlen/Kontrast, eine mit Experten-Zitat oder Trend-Hook). Für jede:
- Die Headline selbst
- Welche Formel sie nutzt und warum diese zum Thema passt
- Falls PCTR-Tool genutzt wurde: den CTR-Score im Vergleich zum Original
Qualität geht vor Quantität — 3 starke Vorschläge sind besser als 5 mittelmäßige.

**Externe Tools — Ergebnisse**: Falls die Tools aufgerufen wurden, integriere die Scores und Empfehlungen in die jeweiligen Kategorien. Falls nicht aufgerufen, liste die Tool-URLs mit kurzer Anleitung, damit der User sie selbst nutzen kann.

## Wichtige Hintergründe

Google Discover ist mittlerweile die größte Traffic-Quelle für Publisher — der Anteil ist von 37% (2023) auf knapp 68% (2025) gestiegen. Gleichzeitig sinkt der klassische Such-Traffic. Aber: ein starkes organisches Ranking bleibt die Grundlage für stabile Discover-Sichtbarkeit. Die beiden Kanäle hängen zusammen.

Discover funktioniert als personalisierter Push-Kanal. Der Algorithmus durchläuft mehrere Stufen:
1. **Eligibility Check** — Prüft Site-Trust und thematische Autorität auf Subfolder- und Entitäts-Ebene
2. **Initial Exposure** — Testet frische Inhalte anhand der frühen CTR (getrieben von Headline, Bild, Markenbekanntheit)
3. **User Quality Assessment** — Misst Klick-Qualität (Navboost: gute vs. schlechte Klicks)
4. **Engagement Feedback Loop** — Fortlaufendes Scoring basierend auf Impressionen, CTR und User-Feedback
5. **Personalisierung** — Abgleich mit Nutzer-Interessen und -Historie
6. **Decay & Renewal** — Ältere Inhalte verlieren Sichtbarkeit, erfolgreicher Evergreen kann re-promoted werden

CTR-Zielwert für Discover liegt bei 7-9%. Unter 5% deutet auf Optimierungsbedarf bei Headline oder Bild hin.
