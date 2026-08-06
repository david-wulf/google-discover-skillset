# Discover-Bewertungskriterien

## 1. Headline & OG:Title

Google Discover zeigt den `og:title` als Headline im Feed — dieser kann sich vom `<title>` (für die Google-Suche) und der `<h1>` (für den Artikel selbst) unterscheiden. Das ist ein wichtiger Hebel: Man kann den Discover-Titel separat optimieren, ohne SEO-Rankings zu gefährden.

### Bewährte Headline-Formeln für Discover

Jede Formel hat einen psychologischen Mechanismus, der sie im Feed wirksam macht. Beim Schreiben von Alternativen: Nicht einfach die Formel befüllen, sondern den stärksten Aspekt des Artikels finden und in die Formel einbauen.

| Formel | Mechanismus | Muster | Beispiel |
|--------|-------------|--------|----------|
| Zahlen-Kontrast | Überraschung durch unerwartete Spanne oder Vergleich | „Von [niedrig] bis [hoch]: [was den Unterschied macht]" | „Von 1,5 bis 10 kWh am Tag: So stark schwankt der Ertrag eines Balkonkraftwerks" |
| How-to + Hindernis | Nutzenversprechen + typische Angst entkräften | „Wie [Zielgruppe] [Ergebnis] erreicht – ohne [typisches Hindernis]" | „Wie Mieter ihre Heizkosten halbieren – ohne teure Sanierung" |
| Konträrer Ansatz | Widerspruch zu Erwartung = Klick-Impuls | „Warum [verbreiteter Glaube] falsch ist – und was [Autorität] stattdessen empfiehlt" | „Warum tägliches Joggen deinen Knien schadet – und was Orthopäden empfehlen" |
| Experten + Überraschung | Autorität + unerwartetes Ergebnis | „Laut [Experte/Institution]: [überraschende Erkenntnis oder Zahl]" | „Laut Stiftung Warentest: Diese Zahnpasta ist die beste – und kostet nur 65 Cent" |
| Trend-Hook + Relevanz | Aktualität + persönliche Betroffenheit | „[Aktuelles Thema] [Jahr]: Was das für [Zielgruppe] bedeutet" | „Neues Solargesetz 2026: Was das für Balkonkraftwerk-Besitzer bedeutet" |
| Kosten/Spar-Hook | Geld sparen = universeller Klick-Trigger | „[Produkt/Thema]: So viel sparst du wirklich – [konkreter Zeitraum]" | „Balkonkraftwerk: So viel sparst du wirklich im ersten Jahr" |

### Prinzipien für starke Discover-Headlines

1. **Der stärkste Fakt gehört in die Headline** — Wenn der Artikel eine überraschende Zahl, einen Vergleich oder ein konkretes Ergebnis enthält, muss das in die Headline. Nicht verstecken.
2. **Neugier-Lücke ohne Clickbait** — Der Leser muss wissen, worum es geht (kein Rätsel), aber noch nicht die Antwort kennen (kein Spoiler). Beispiel gut: „Von 1,5 bis 10 kWh am Tag" (Spanne ist klar, aber welche Faktoren?). Beispiel schlecht: „Du wirst nicht glauben, wie viel Strom..." (reines Clickbait).
3. **Persönliche Relevanz** — „du", „dein", direkte Ansprache. Discover-Nutzer scrollen durch einen Feed — sie klicken nur, wenn es sie persönlich betrifft.
4. **Konkretheit schlägt Abstraktion** — „389 Euro Ersparnis pro Jahr" ist stärker als „viel Geld sparen".
5. **Richtwert 70–95 Zeichen** für den `og:title`. Darunter bleibt Platz für den Haken ungenutzt,
   über 95 wird im Feed abgeschnitten. Die Kernentität gehört in die ersten 40 Zeichen.

### Headline-Validierung

Der Skill `discover-headline` bewertet den `og:title` über acht gewichtete Dimensionen
(Entitätsdichte, Themenklarheit, Informationswert, Aktualitätssignal, Engagement-Tiefe,
Formatierung, Autorität, Bildversprechen) mit Clickbait-Abzug und rechnet das in einen
pCTR-Wert um. Vorgehen:

1. Original als Baseline bewerten lassen
2. Bis zu vier Varianten mit je anderer Formel dagegen stellen
3. Im Bericht das **Delta in Prozentpunkten** angeben, nicht den Absolutwert — der
   Modell-Mittelpunkt liegt bei 11,3 % und damit über dem Arbeitsziel

Ziel-CTR zur Einordnung: **7–9 %**, News-Seiten liegen im Schnitt bei rund 11 %, Non-News bei
rund 6 %; unter 5 % ist Handlungsbedarf. *(GSC-Auswertung über 11.000 URLs von 62 Domains.)*

Das frühere externe Web-Tool (pctr-discover.pages.dev) ist damit nicht mehr nötig und war beim
letzten Test nicht funktionsfähig.

### Rote Flaggen bei Headlines:
- Rein informativ ohne Anreiz ("Bericht über Heizkostenentwicklung 2025")
- Clickbait ohne Substanz ("Du wirst nicht glauben, was...")
- Zu lang (über 95 Zeichen werden im Feed abgeschnitten) oder zu kurz (unter 50 Zeichen trägt
  kaum einen Haken)
- Kein Bezug zu einer aktuellen Relevanz oder einem Nutzerbedürfnis
- Identisch mit `<title>` und `<h1>` — dann wird die Chance verpasst, für Discover separat zu optimieren

---

## 2. Titelbild

Das Titelbild ist neben der Headline der wichtigste CTR-Treiber im Discover-Feed. Google verwendet für die Bildauswahl:
1. `og:image` Meta-Tag
2. Strukturierte Daten: `WebPage` → `primaryImageOfPage`
3. Strukturierte Daten: `mainEntity` / `mainEntityOfPage` → `BlogPosting` → `image`

### Technische Anforderungen
- **Mindestbreite**: 1200px (darunter wird das Bild im Feed klein dargestellt oder gar nicht verwendet)
- **Seitenverhältnis**: 16:9 ideal
- **Format**: WebP oder JPEG bevorzugt — kein PNG (zu groß, keine Vorteile im Feed)
- **Meta-Robots**: `max-image-preview:large` muss gesetzt sein, sonst darf Google das Bild nicht groß anzeigen

### Inhaltliche Empfehlungen
- **Close-ups** funktionieren besser als Weitwinkel-Aufnahmen
- **Gesichter und Emotionen** steigern die CTR
- **Collagen** können mehrere Aspekte eines Themas zeigen
- **Personen/Charaktere** stärken Autorität und Vertrauen
- **Die Entität kreativ darstellen** — nicht nur ein generisches Stockfoto, sondern das Kernthema visuell greifbar machen
- **Standort des Nutzers** bei der Bildwahl berücksichtigen (regionale Relevanz)
- **Schrift auf dem Bild** ist erlaubt und kann als zusätzlicher Hook funktionieren

### Rote Flaggen bei Bildern:
- Generisches Stockfoto ohne Bezug zum Thema
- Bild unter 1200px Breite
- PNG-Format
- `max-image-preview:large` fehlt
- Bild zeigt nicht die Kern-Entität des Artikels

---

## 3. Entitäten-Vollständigkeit

Entitäten sind das Herzstück der Discover-Optimierung. Google bewertet thematische Autorität auf Entitäts-Ebene. Es reicht nicht, Keywords zu verwenden — Google will sehen, dass der Autor das Thema wirklich durchdrungen hat.

### So identifiziert man Kern-Entitäten eines Themas:
1. Top-10-Rankings für das Hauptkeyword öffnen
2. Wiederkehrende Begriffe sammeln: Personen, Marken, Tools, Orte, Fachbegriffe
3. Das sind die Kern-Entitäten, die Google erwartet

### Entitäten nicht nur nennen, sondern kontextualisieren:
- **Definieren**: Was ist es genau?
- **Vergleichen**: Wie unterscheidet es sich von Alternativen?
- **Beziehungen erklären**: Wie hängt es mit anderen Entitäten zusammen?
- **Intern verlinken**: Auf eigene Inhalte verweisen, die die Entität vertiefen

So erkennt Google echte thematische Autorität statt Keyword-Stuffing. Jede Kern-Entität sollte idealerweise mindestens 2 dieser 4 Kontextualisierungen erhalten.

### Bewertungslogik:
- **Grün**: >80% der erwarteten Kern-Entitäten sind vorhanden UND mindestens die Hälfte davon kontextualisiert
- **Gelb**: >60% vorhanden ODER Entitäten vorhanden aber nicht kontextualisiert
- **Rot**: <60% der erwarteten Kern-Entitäten fehlen

---

## 4. E-E-A-T Signale

Discover bevorzugt Inhalte mit starken Trust-Signalen.

### Was geprüft wird:
- **Strukturierte Daten**: Article/NewsArticle mit Autor-Objekt (Name + Bild)
- **Veröffentlichungsdatum**: Sichtbar im Artikel mit Autorennennung
- **Autorenseite**: Existiert eine Seite mit Bio, Qualifikation, Erfahrung, publizierten Artikeln?
- **Über-uns-Seite**: Existiert, ist verlinkt, zeigt Expertise der Redaktion
- **Quellenangaben**: Werden seriöse externe Quellen verlinkt?

---

## 5. Technische Discover-Readiness

### OG-Tags (Pflicht)
- `og:title` — vorhanden und optimiert (nicht identisch mit `<title>` wenn möglich)
- `og:image` — vorhanden, URL erreichbar, Bild erfüllt technische Anforderungen
- `og:description` — vorhanden, ansprechend formuliert
- `og:type` — `article` gesetzt

### Meta-Robots
- `max-image-preview:large` muss gesetzt sein
- Seite darf nicht auf `noindex` stehen

### News-Sitemap
- Eine News-Sitemap sollte existieren unter `/news-sitemap.xml` oder als Teil des Sitemap-Index
- Der analysierte Artikel sollte darin enthalten sein
- Fehlende News-Sitemap ist ein gelbes Signal — nicht zwingend nötig, aber stark empfohlen für Publisher

### Startseiten-Verlinkung
- Der Artikel sollte von der Startseite verlinkt sein
- Je prominenter (weiter oben, größerer Teaser), desto besser
- Discover gibt frischen Inhalten einen Boost — Startseiten-Prominenz signalisiert Google die Wichtigkeit

---

## 6. Content-Freshness

| Zeitraum | Freshness-Gewichtung |
|----------|----------------------|
| 1–7 Tage alt | Höchste Gewichtung |
| 8–14 Tage alt | Mittlere Gewichtung |
| 15–30 Tage alt | Niedrige Gewichtung |
| über 30 Tage | Kontinuierlicher Verlust |

Wenn ein Artikel älter als 7 Tage ist und Discover-Traffic gewünscht ist, empfehle eine Aktualisierung (Inhalt erweitern, Bild tauschen, Headline anpassen).
