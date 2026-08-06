---
name: discover-feedkarte
description: >
  Bewertet die Google-Discover-Feed-Karte als Einheit: Titelbild und Headline zusammen, so wie
  der Nutzer sie im Feed sieht. Misst das Bild technisch (Breite, Seitenverhältnis, Format,
  Kontrast, Farbigkeit, Informationsverlust), rendert es auf echte Kartengrößen (340 × 190 und
  80 × 80) und beurteilt es dort visuell: Ist die Kern-Entität erkennbar, übersteht die Bildaussage
  den Beschnitt, bleibt Schrift lesbar, doppelt das Bild die Headline oder ergänzt es sie.
  Liefert einen Feed-Karten-Score 0–100 und konkrete Bildaufträge.
  Verwende diesen Skill immer, wenn es um das Titelbild oder die Feed-Darstellung eines Artikels
  geht — auch bei: "Titelbild prüfen", "og:image bewerten", "welches Bild für Discover",
  "Bild-Check", "Feed-Karte", "Thumbnail", "warum klickt keiner", "CTR Bild verbessern",
  "Bildausschnitt Discover", "Discover Vorschaubild", "Karte im Feed bewerten".
  Auch auslösen, wenn ein Screenshot einer Discover-Karte oder eines Artikels eingereicht wird,
  oder wenn nur ein Bild plus Headline zur Beurteilung kommt.
  Für die semantische Textanalyse ist discover-content-optimizer zuständig, für die technische
  Prüfung der veröffentlichten Seite (News-Sitemap, Startseiten-Prominenz) der
  discover-artikel-optimierer.
---

# Discover Feed-Karte

Im Feed konkurriert kein Artikel, sondern eine **Karte**: Bild, Headline, Publisher-Name. Sie ist
rund 340 × 190 Punkte groß und wird im Scrollen wahrgenommen. Ein Titelbild, das in
Originalgröße überzeugt, kann dort vollständig versagen — und umgekehrt.

Der Kern dieses Skills ist deshalb kein Prompt, sondern ein Wechsel der Betrachtungsgröße:
Das Bild wird auf die echten Kartenmaße gerendert und **in dieser Größe angesehen**.

## Grundregeln

1. **Erst rendern, dann urteilen.** Nie ein Titelbild allein in Originalgröße bewerten. Die
   Bewertung erfolgt an `ansicht_feedkarte_340x190.png` und `ansicht_kompakt_80x80.png`.
2. **Messwerte sind Prüfaufträge, keine Urteile.** Der Informationsverlust-Wert unterscheidet
   nicht zwischen verschwindender Schrift und verschwindender Textur. Nur das Auge entscheidet,
   ob die Bildaussage betroffen ist.
3. **Belegpflicht.** Jeder Befund benennt, was in welcher Ansicht sichtbar oder verschwunden ist.
   „Bild zu unruhig" ist kein Befund. „In der 80 × 80-Ansicht sind Logo und Markenname
   weggeschnitten, lesbar bleibt nur ‚000 WATT'" ist einer.
4. **Karte, nicht Bild.** Bild und Headline werden gemeinsam bewertet. Ein Bild, das den
   `og:title` wiederholt, verschenkt eine der zwei Flächen der Karte.
5. **Keine erfundenen Maße.** Bildbreite, Fläche, Format, Dateigröße und Auslieferung kommen aus
   dem Skript.
6. **Evidenzstufe mitführen.** Jedes Kriterium ist als **[Doku]**, **[SDK]**, **[Richtlinie]** oder
   **[Praxis]** markiert (`references/kartenrubrik.md`). Im Bericht wird die Stufe genannt: eine
   Spezifikation aus der Google-Doku ist nicht verhandelbar, eine SDK-Erkenntnis ist ein starkes
   Indiz aus Client-Sicht, eine Praxis-Heuristik braucht eine Begründung. Nie eine
   Praxis-Empfehlung als „Google verlangt" verkaufen — und SDK-Zahlen nicht als Spezifikation
   zitieren.

## Die harte Spezifikation

Diese vier Punkte sind Zulassungsbedingung, kein Feinschliff **[Doku]**:

| Anforderung | Prüfung |
|-------------|---------|
| **≥ 1200 px Breite** | `dimensions.meets_min_width_1200` |
| **> 300.000 px Gesamtfläche** | `dimensions.meets_min_area_300k` — eigenständig, nicht von der Breite abgedeckt |
| **16:9** | `dimensions.aspect_ratio` |
| **Wichtige Details bleiben im beschnittenen Ausschnitt erhalten** | nur visuell prüfbar, an `ansicht_crop_16zu9.png` |
| **`max-image-preview:large`** im robots-Meta oder AMP | der einzige harte technische Blocker der ganzen Doku |

`google_spec.all_met` im Skript-Output fasst die messbaren drei zusammen. Ist der Wert `false`,
greift der Score-Deckel bei 55 — vor jeder inhaltlichen Diskussion.

Ausdrücklich untauglich laut Doku: das **Websitelogo** und generische Motive. Ebenso „Bilder mit
viel Text" — gemeint sind vollgeschriebene Grafiken, **nicht** ein kurzer Schriftzug aus drei bis
fünf Wörtern. Der ist Teil der Thumbnail-Formel und wird in K2 belohnt.

Ohne abrufbares Thumbnail entsteht laut SDK **keine Karte**, es gibt keinen Textfallback **[SDK]**.
Die Bildquelle läuft über eine fünfstufige Fallback-Kette (`og:image` → `twitter:image` →
`og:image:secure_url` → `twitter:image:src` → generisches `image`), wobei **Schema.org-JSON-LD
Vorrang vor allen OG-Tags hat**. Nennen mehrere Quellen unterschiedliche Motive, wählt Google —
und nicht zwingend das gute Bild. Abweichungen deshalb immer im Bericht benennen.

## Ablauf

### Schritt 0 — Eingabe klären

Drei Wege, je nachdem was vorliegt:

| Eingabe | Vorgehen |
|---------|----------|
| **URL eines Artikels** | `og:image`, `og:title`, JSON-LD-`image`, `srcset` und `<meta name="robots">` aus dem HTML holen (WebFetch, sonst Browser + `javascript_tool`). Die **größte** verfügbare Variante nehmen — oft steckt im `srcset` eine breitere Fassung als im `og:image`. Beide Werte im Bericht nennen, wenn sie abweichen. |
| **Bild plus Headline** | Direkt weiter zu Schritt 1. Headline separat erfragen, wenn nicht geliefert — ohne sie fällt Dimension K4 weg. |
| **Screenshot** | Screenshot einer Discover-Karte oder eines Artikels mit dem Read-Tool ansehen. Headline, Publisher und Bildmotiv daraus ablesen. Technische Maße sind dann **nicht** bekannt: Dimension K1 wird als nicht messbar gekennzeichnet, nicht geschätzt. |

Zusätzlich klären: Was ist die **Kern-Entität** des Artikels? Ohne sie ist nicht bewertbar, ob
das Bild sie zeigt. Und: Gibt es Konkurrenzkarten zum Vergleich (Screenshot des eigenen Feeds)?
Der Feed ist ein Wettbewerbsumfeld, nicht eine Einzelbetrachtung.

Wenn die Meta-Tags per Regex aus rohem HTML gelesen werden (WebFetch-Weg), **beide
Anführungszeichen-Varianten** abdecken. WordPress schreibt `name='robots'` mit einfachen
Anführungszeichen; ein Muster mit `"` allein meldet fälschlich, `max-image-preview:large` fehle —
und das führt direkt in einen falschen Score-Deckel. Der DOM-Weg über `querySelector` hat das
Problem nicht. Zusätzlich immer den HTTP-Header `X-Robots-Tag` prüfen, der das Meta-Tag überstimmt.

JavaScript-Schnipsel für den URL-Weg:

```js
JSON.stringify({
  ogTitle: document.querySelector('meta[property="og:title"]')?.content,
  ogImage: document.querySelector('meta[property="og:image"]')?.content,
  ogImageSecure: document.querySelector('meta[property="og:image:secure_url"]')?.content,
  ogImageW: document.querySelector('meta[property="og:image:width"]')?.content,
  ogImageH: document.querySelector('meta[property="og:image:height"]')?.content,
  ogImageAlt: document.querySelector('meta[property="og:image:alt"]')?.content,
  twitterImage: document.querySelector('meta[name="twitter:image"]')?.content,
  robots: document.querySelector('meta[name="robots"]')?.content,
  siteName: document.querySelector('meta[property="og:site_name"]')?.content,
  locale: document.querySelector('meta[property="og:locale"]')?.content,
  heroSrcset: document.querySelector('article img, .entry-content img, .post-thumbnail img')?.srcset,
  jsonldImage: [...document.querySelectorAll('script[type="application/ld+json"]')]
    .map(s => s.textContent).join('\n').match(/"(?:image|primaryImageOfPage)"[\s\S]{0,300}/g)
})
```

Aus diesem Satz drei Dinge ableiten, bevor gemessen wird:

1. **Welche Variante ist die größte?** Im `srcset` steckt oft eine breitere Fassung als im
   `og:image`. Gemessen wird die größte verfügbare; beide Werte im Bericht nennen, wenn sie
   abweichen — denn Discover nimmt die deklarierte, nicht die vorhandene.
2. **Nennen alle Quellen dasselbe Motiv?** `og:image`, `twitter:image`, JSON-LD-`image` und
   `primaryImageOfPage` vergleichen. JSON-LD gewinnt bei Konflikt **[SDK]**.
3. **Sind `og:image:width`/`:height` gesetzt?** Fehlen sie, riskiert man Fehl-Skalierung und
   falschen Zuschnitt. Kein Punktabzug, aber eine Zeile im Bericht.

### Schritt 1 — Messen und rendern

```bash
python scripts/feedcard.py --image <url-oder-pfad> --out <ausgabeverzeichnis>
```

Liefert JSON mit Maßen, Seitenverhältnis samt Beschnittverlust, Helligkeit, RMS-Kontrast,
Farbigkeit, Informationsverlust bei Feed-Größe, automatischen Hinweisen — und den Pfaden zu
drei Ansichten:

| Ansicht | Wofür |
|---------|-------|
| `ansicht_feedkarte_340x190.png` | die große Feed-Karte. Hauptbewertungsgrundlage |
| `ansicht_kompakt_80x80.png` | kompakte Listenansicht. Zeigt, was ein quadratischer Beschnitt zerstört |
| `ansicht_crop_16zu9.png` | 16:9-Beschnitt des Originals. Zeigt, was bei abweichendem Seitenverhältnis wegfällt |

Braucht Pillow. Fehlt es (`pip install pillow`), entfällt der Rendering-Schritt: dann das Original
ansehen, Dimension K3 als nicht messbar kennzeichnen und den Score entsprechend deckeln —
nicht schätzen.

### Schritt 2 — Ansehen

**Alle drei Ansichten mit dem Read-Tool öffnen.** Das ist der Kern des Skills und wird nicht
übersprungen. Pro Ansicht notieren:

- Was ist auf den ersten Blick erkennbar — in einer halben Sekunde, so wie beim Scrollen?
- Ist die Kern-Entität des Artikels sichtbar und identifizierbar?
- Welche Schrift bleibt lesbar, welche nicht? Wörtlich zitieren, was noch entzifferbar ist.
- Was schneidet der Beschnitt weg? Besonders in der 80 × 80-Ansicht: Logos, Marken und
  Randmotive verschwinden dort regelmäßig.
- Wirkt es wie ein generisches Stockfoto oder wie eine spezifische Aufnahme zu diesem Thema?

Dann das Original ansehen und vergleichen: Was ging verloren, und war es tragend?

**Die Thumbnail-Formel abhaken** — Gesicht, Schriftzug, Beweis-Element. Sie wirken nur zusammen,
deshalb wird jede Komponente einzeln festgestellt und nicht im Gesamteindruck verrechnet:

| Komponente | Konkret zu prüfen |
|------------|-------------------|
| **Gesicht** | Ist es die **eigene** Person (Autor, Experte) oder ein Model? Blick in die Kamera oder auf das gezeigte Objekt — oder ins Leere? Haltung passend zur Aussage oder Grimasse? Augen in der Kartengröße noch erkennbar? |
| **Schriftzug** | Wörter zählen — 3 bis 5 ist die Erfassbarkeitsgrenze. Behauptung oder Frage, oder nur eine Beschreibung? Ist **ein** Wort hervorgehoben (Farbfläche, Unterstreichung, Farbwechsel)? |
| **Beweis-Element** | Gibt es einen sichtbaren Beleg für die Behauptung: Screenshot, UI-Ausschnitt, Produkt, Tool-Logos, eine Zahl als Badge? Bei abstraktem Thema: ersetzt eine sprechende Geste das Objekt? |

Zusätzlich die **Bildordnung**: klare Zweiteilung (etwa halbe Fläche Gesicht, halbe Text) oder
liegt der Text über dem Gesicht? Bewährte Muster sind Gesicht rechts / Text links mit einem farbig
hinterlegten Wort, oder Gesicht links / UI-Screenshot rechts mit Zahlen-Badge.

### Schritt 3 — Bewerten

Score nach `references/kartenrubrik.md`. Punkte pro Unterkriterium mit Begründung, entweder
aus einem Messwert oder aus einer benannten Beobachtung in einer der Ansichten.

### Schritt 4 — Bericht

Markdown in der Antwort, zusätzlich als Datei. Aufbau:

1. **Kopf** — Motiv in einem Satz, Maße, Format, Score mit Band
2. **Urteil in drei Sätzen** — Zustand, größter Hebel, Aufwand
3. **Score-Tabelle** — vier Dimensionen mit Punkten und Einzeiler-Befund
4. **Was in welcher Größe verschwindet** — die zentrale Tabelle: Element × sichtbar in 340×190 ×
   sichtbar in 80×80. Das ist der Teil, der beim Kunden hängen bleibt
5. **Karten-Zusammenspiel** — Bild gegen Headline: Doppelung oder Ergänzung
6. **Bildaufträge** — konkret, was ein Fotograf oder Grafiker tun soll. Nicht „aussagekräftigeres
   Bild", sondern „Ausschnitt so wählen, dass die Module die untere Bildhälfte füllen und der
   Markenname aus dem äußeren Fünftel in die Mitte rückt"
7. **Technische Fixes** — Breite, Format, `max-image-preview:large`, Dateigröße
8. **Methodik** — was gemessen, was visuell beurteilt, was nicht prüfbar war

Die gerenderten Ansichten mit dem SendUserFile-Tool mitschicken — der visuelle Beleg wirkt beim
Kunden stärker als jede Beschreibung.

Auf Wunsch zusätzlich Word oder Excel über die Skills `docx` bzw. `xlsx`. Einmal fragen, nicht
ungefragt erzeugen.

## Abgrenzung

| Skill | Zuständig für |
|-------|---------------|
| **discover-feedkarte** | Titelbild und Feed-Karte: Bild, Beschnitt, Lesbarkeit, Bild-Headline-Zusammenspiel |
| discover-content-optimizer | Artikeltext: Entitäten, semantische Tiefe, Schema, Keywords |
| discover-artikel-optimierer | veröffentlichte Seite: OG-Vollständigkeit, News-Sitemap, Startseiten-Prominenz, E-E-A-T-Signale im HTML |

Überschneidung ist gewollt bei `max-image-preview:large` und der Bildbreite — beide Skills
prüfen das, weil beide es brauchen. Die Bildwirkung prüft nur dieser Skill.

## Herkunft der Kriterien

Die Rubrik trennt vier Evidenzstufen, weil sie unterschiedlich verbindlich sind:

- **[Doku]** — Googles Discover-Dokumentation: Mindestbreite 1200 px, Gesamtfläche über
  300.000 px, 16:9, Detailerhalt beim Zuschnitt, `max-image-preview:large`, Websitelogo und
  generische Motive untauglich.
- **[Richtlinie]** — Discover-Inhaltsrichtlinien: Werbeanteil darf den Anteil der
  Nachrichteninhalte nicht überschreiten, gesponserte Inhalte deutlich kennzeichnen, keine
  Vorschauinhalte mit vorgetäuschten Details, Transparenz über Autor und Datum.
- **[SDK]** — Reverse Engineering des Google-App-SDK (Metehan Yeşilyurt): `LOW_QUALITY_IMAGE` als
  Negativmarker, `EMBER_FEED_THUMBNAILS_DOWNLOADED` und `image_load_failure_count` als eigene
  Signale, JSON-LD vor OG-Tags, historische CTR pro URL. **Client-Sicht zu einem Zeitpunkt** — der
  Autor hat frühere Behauptungen selbst korrigiert. Als starkes Indiz führen, nie als Spezifikation
  zitieren.
- **[Praxis]** — Thumbnail-Formel Gesicht + 3–5 Wörter + Beweis-Element, Zweiteilung der Fläche,
  Formatwahl webp/jpg, Schriftzug ≠ `og:title`. Bewährt, aber ohne Google-Beleg.

## Grenzen

- Die Kartenmaße 340 × 190 und 80 × 80 sind Größenordnungen der ausgelieferten Karten, keine von
  Google dokumentierten Spezifikationen. Die Aussage „bei dieser Größe verschwindet X" ist
  belastbar; „genau so sieht die Karte bei jedem Nutzer aus" nicht.
- Der Score ist kein CTR-Wert. Er misst, ob die Karte die bekannten Schwächen vermeidet.
  Zur Einordnung der Zielgröße: Discover-CTR liegt bei News-Seiten um 11 %, bei Non-News um 6 %;
  Arbeitsziel 7–9 %, unter 5 % ist ein Handlungssignal. Diese Werte sind **nicht** aus dem Score
  ableitbar und dürfen nicht als Prognose ausgegeben werden.
- Ob Google überhaupt dieses Bild wählt, entscheidet die Fallback-Kette. Weichen die Quellen ab,
  wird das im Bericht benannt — welche Variante Google nimmt, ist von außen nicht feststellbar.
- Gesichtserkennung findet nicht automatisiert statt. Menschliche Präsenz wird visuell beurteilt.
- Bei einer bereits ausgespielten URL mit schwacher Historie ist die Wirkung eines Bildwechsels
  begrenzt: die CTR-Historie hängt an der URL **[SDK]**. Das gehört in die Empfehlung, nicht in den
  Score.
