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
4. **Karte, nicht Bild.** Bild und Headline werden gemeinsam bewertet. Ein Bild, das die Headline
   wortwörtlich wiederholt, verschenkt die Hälfte der Fläche.
5. **Keine erfundenen Maße.** Bildbreite, Format und Dateigröße kommen aus dem Skript.

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
  ogImageW: document.querySelector('meta[property="og:image:width"]')?.content,
  ogImageH: document.querySelector('meta[property="og:image:height"]')?.content,
  robots: document.querySelector('meta[name="robots"]')?.content,
  siteName: document.querySelector('meta[property="og:site_name"]')?.content,
  heroSrcset: document.querySelector('article img, .entry-content img, .post-thumbnail img')?.srcset,
  jsonldImage: [...document.querySelectorAll('script[type="application/ld+json"]')]
    .map(s => s.textContent).join('\n').match(/"image"[\s\S]{0,300}/)?.[0]
})
```

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

## Grenzen

- Die Kartenmaße 340 × 190 und 80 × 80 sind Größenordnungen der ausgelieferten Karten, keine von
  Google dokumentierten Spezifikationen. Die Aussage „bei dieser Größe verschwindet X" ist
  belastbar; „genau so sieht die Karte bei jedem Nutzer aus" nicht.
- Der Score ist kein CTR-Wert. Er misst, ob die Karte die bekannten Schwächen vermeidet.
- Ob Google überhaupt dieses Bild wählt, entscheidet die Fallback-Kette aus `og:image`,
  JSON-LD-`image` und Seitenbild. Weichen die Quellen ab, wird das im Bericht benannt — welche
  Variante Google nimmt, ist von außen nicht feststellbar.
- Gesichtserkennung findet nicht automatisiert statt. Menschliche Präsenz wird visuell beurteilt.
