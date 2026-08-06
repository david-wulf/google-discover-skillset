---
name: discover-readiness-domain
description: "Analysiert eine Domain auf Google Discover-Optimierung: Discover-Traffic, Content-Qualität, technische Signale und E-E-A-T. Verwende diesen Skill immer, wenn der User nach Google Discover fragt, Discover-Traffic analysieren will, wissen möchte ob seine Seite Discover-ready ist, oder die Discover-Performance einer Domain bewerten will. Auch auslösen bei: 'Discover Check', 'Discover Audit', 'Discover optimieren', 'Discover Traffic', 'warum bin ich nicht in Discover', 'Discover-Potenzial', 'wie performe ich in Discover', 'Discover-Analyse'. Selbst wenn der User nur beiläufig Google Discover erwähnt — diesen Skill nutzen."
---

# Google Discover Audit

Dieser Skill führt eine umfassende Analyse durch, ob eine Domain gut für Google Discover optimiert ist. Der Fokus liegt auf Content-Qualität, E-E-A-T-Signalen und technischen Discover-Voraussetzungen.

Google Discover ist ein personalisierter Content-Feed, den Google auf Mobilgeräten und der Google-Startseite anzeigt. Im Gegensatz zur klassischen Suche braucht der Nutzer keine Query — Google wählt Inhalte basierend auf Nutzerinteressen, Content-Qualität und Aktualität aus. Discover kann massiven Traffic liefern, ist aber unberechenbar und belohnt vor allem hochwertige, visuell ansprechende, aktuelle Inhalte.

## Diagnoserahmen: an welcher Station hängt es?

Discover ist eine Pipeline aus acht Stationen, und ein Artikel kann an **jeder einzelnen**
hängenbleiben. Deshalb ist „schlechter Discover-Traffic" nie eine Diagnose, sondern eine Frage:
**an welcher Station?** Das Audit muss diese Frage beantworten, nicht eine Mängelliste liefern.

| Symptom in den Daten | Station | Wo geprüft |
|---|---|---|
| **Gar keine Impressionen** | 01 Eligibility | Phase 3: Indexierung, `max-image-preview:large`, Blocker-Tags, manuelle Maßnahmen, Richtlinien |
| **Impressionen bei der falschen Zielgruppe** | 02/03 Klassifikation und Matching | Phase 2: Entitäten und Themenschärfe |
| **Impressionen, aber kaum Klicks** | 04 Initial Exposure | Phase 2: Headline und Titelbild |
| **Klicks, dann schneller Rücksprung** | 05 Klickqualität | Phase 2: löst der Artikel ein, was die Karte verspricht |
| **Guter Start, dann Abflachen** | 06/08 Engagement und Decay | Phase 1: Lebenszyklus, Aktualisierungspraxis |

**Die wichtigste Konsequenz:** Der Eligibility-Check läuft **pro Verzeichnis und pro Entität**,
nicht auf Domain-Ebene. Eine Domain kann in einem Themenordner discover-fähig sein und im nächsten
überhaupt nicht — Discover-Erfolg ist **nicht von Thema zu Thema übertragbar**. Deshalb wird der
Traffic in Phase 1 **nach Verzeichnis aufgeschlüsselt**. Ein Domain-Score allein verdeckt genau
den Befund, der handlungsleitend ist.

Mechanik, belegte Signale, Kennzahlen und Evidenzstufen: `references/discover-mechanik.md`. Dort
steht auch, welche verbreiteten Empfehlungen **nicht** in Googles Doku stehen und deshalb im
Kundenbericht als Praxis-Heuristik gekennzeichnet werden müssen.

## Abgrenzung zu den Artikel-Skills

Dieses Audit arbeitet auf **Domain-Ebene**. Für die Einzelartikel-Analyse sind vier Skills
zuständig, auf die am Ende verwiesen wird statt deren Arbeit hier grob nachzuahmen:

| Skill | Ebene |
|-------|-------|
| `discover-readiness-artikel` | veröffentlichte URL: OG-Vollständigkeit, News-Sitemap, Startseiten-Prominenz |
| `discover-content-optimizer` | Artikeltext: Entitäten, semantische Tiefe, Schema, Keywords |
| `discover-headline` | `og:title`: pCTR-Modell, Varianten, Clickbait |
| `discover-titelbild` | Titelbild bei echter Kartengröße |

Wenn in Phase 2 auffällt, dass die Schwäche an einem einzelnen Hebel hängt (etwa durchgehend
schwache Titel oder Bilder unter der Spezifikation), gehört in die Empfehlung der Verweis auf den
zuständigen Skill — nicht eine oberflächliche Zweitanalyse.

## Grundregel: Keine Halluzinationen

Führe im Audit ausschließlich Befunde auf, die du mit konkreten Daten belegen kannst. Jede Aussage muss sich auf ein tatsächlich abgerufenes Ergebnis beziehen — sei es ein GSC-Datenpunkt, ein HTML-Element im Quellcode oder ein Inspection-Ergebnis.

Wenn du einen Aspekt nicht prüfen konntest (z.B. weil kein Seitenabruf möglich war, oder weil die GSC-Daten keine Aussage dazu enthalten), dann schreibe explizit **"⚠ Zu prüfen:"** gefolgt von einer Beschreibung, was der User manuell verifizieren sollte. Stelle niemals Vermutungen als Fakten dar.

## Vorab-Check: GSC-Zugang prüfen

Bevor du GSC-Tools nutzt, prüfe mit `gsc_list_sites`, ob die angefragte Domain dort als Property registriert ist. Vergleiche die vom User genannte Domain mit den verfügbaren `siteUrl`-Einträgen (z.B. `sc-domain:example.de` oder `https://www.example.de/`).

- **Domain stimmt überein:** Nutze die passende `siteUrl` für alle GSC-Abfragen. Bevorzuge die `sc-domain:`-Variante, da sie alle Subdomains und Protokolle abdeckt.
- **Domain stimmt NICHT überein:** Nutze keine GSC-Tools für diese Domain. Teile dem User mit, dass für die angefragte Domain kein GSC-Zugang besteht. Führe in diesem Fall nur Phase 2 (Content-Analyse per Seitenabruf) durch und gib Empfehlungen basierend auf den technischen Befunden. Weise den User darauf hin, dass ohne GSC-Daten keine Aussagen über tatsächlichen Discover-Traffic möglich sind.

## Analyse-Ablauf

Der Audit besteht aus vier Phasen. Führe sie in dieser Reihenfolge durch und präsentiere die Ergebnisse als zusammenhängende Analyse im Chat.

### Phase 1: Discover-Traffic-Daten abrufen

Nutze die GSC Search Analytics API mit `type: "discover"`, um echte Discover-Daten zu ziehen. Das ist der wichtigste erste Schritt, weil er zeigt, ob die Domain überhaupt in Discover präsent ist.

**Abfragen (alle parallel absetzbar):**

1. **Discover-Tagesverlauf aktuelle Periode** (letzte 28 Tage):
   - `gsc_search_analytics` mit `type: "discover"`, `dimensions: ["date"]`
   - Berechne: Gesamt-Clicks, Impressions, CTR

2. **Discover-Tagesverlauf Vorperiode** (die 28 Tage davor):
   - `gsc_search_analytics` mit `type: "discover"`, `dimensions: ["date"]` — mit den Datumsangaben der Vorperiode
   - Damit lässt sich der Monats-Trend berechnen (Wachstum/Rückgang in %)

3. **Discover-Tagesverlauf Vorjahreszeitraum** (gleiche 28 Tage, ein Jahr zuvor):
   - `gsc_search_analytics` mit `type: "discover"`, `dimensions: ["date"]` — mit den Datumsangaben des Vorjahres
   - Damit lässt sich die YoY-Entwicklung berechnen. Das ist besonders wichtig, weil Discover-Traffic saisonalen Schwankungen unterliegt — ein Vergleich nur mit dem Vormonat kann saisonale Effekte verschleiern.
   - Falls keine Vorjahresdaten vorhanden sind (GSC liefert leere Ergebnisse), vermerke dies als "Vorjahresdaten nicht verfügbar" und überspringe den YoY-Vergleich.

4. **Top Discover-Seiten** (aktuelle Periode):
   - `gsc_search_analytics` mit `type: "discover"`, `dimensions: ["page"]`, `rowLimit: 25`
   - Identifiziere die Top-Seiten, die in Discover performen

5. **Web-Traffic zum Vergleich** (aktuelle Periode):
   - `gsc_search_analytics` mit `type: "web"`, `dimensions: ["date"]`
   - Berechne den Discover-Anteil am Gesamttraffic (Discover-Clicks / (Discover + Web-Clicks))

6. **Aufschlüsselung nach Verzeichnis** (aktuelle Periode) — **der wichtigste Schnitt**:
   - Die Ergebnisse aus Abfrage 4 nach dem ersten Pfadsegment gruppieren (`/ratgeber/`, `/news/`,
     `/tests/` …) und Clicks, Impressionen und CTR je Verzeichnis aufsummieren
   - Der Eligibility-Check läuft pro Verzeichnis und pro Entität, nicht auf Domain-Ebene. Diese
     Tabelle zeigt, **wo** die Domain discover-fähig ist und wo nicht
   - Verzeichnisse mit Publikationsvolumen aber null Discover-Impressionen sind der stärkste
     Einzelbefund des ganzen Audits: dort greift Station 01

**Bewertungskriterien:**
- Hat die Domain überhaupt Discover-Traffic? Wenn ja, wie viel — und **in welchen Verzeichnissen**?
- Monats-Trend gegen die Vorperiode, YoY-Trend gegen das Vorjahr. Saisonale Muster?
- Welche Content-Typen und Themen performen? Gibt es ein dominantes Themencluster?
- Discover-CTR gegen die Benchmarks: **News-Seiten rund 11 %, Non-News rund 6 %, Arbeitsziel
  7–9 %, unter 5 % ist ein Handlungssignal.** Quelle: GSC-Auswertung über 11.000 URLs von
  62 Domains über 12 Monate. Diese Zahlen im Bericht mit Quelle nennen, nicht als eigene Erfahrung
- Einzelne Top-URLs dauerhaft unter 5 % CTR: die historische CTR wird **pro URL** geführt
  (`click_count`/`show_count`). Eine URL trägt ihre Feed-Reputation mit — Titel- und Bildwechsel
  wirken dort begrenzt, bei grundlegend neuem Aufhänger ist eine **neue URL** die ehrlichere Option

**Beim Verhältnis Discover zu Web unbedingt dazuschreiben:** Der Vergleich der beiden CTR-Werte
ist **nicht zulässig**. Discover zählt eine Impression erst, wenn eine Karte **sichtbar** wird;
die Suche zählt sie, sobald die Ergebnisseite ausgeliefert wird. Die Discover-CTR ist strukturell
höher, ohne dass etwas besser läuft. Das Klick-Verhältnis ist vergleichbar, das CTR-Verhältnis nicht.

**Volatilität nicht überinterpretieren:** Volatilität ist laut Google Konstruktionsmerkmal, nicht
Fehlerbild. Ein Teil der Schwankung ist zudem Test-Design (Counterfactual-Experimente, retroaktives
Entfernen bereits ausgespielter Inhalte). Deshalb über 28 Tage plus Vorjahresvergleich arbeiten und
einzelne Einbrüche nicht als Qualitätsurteil lesen.

**Kontext für die Erwartungssteuerung:** Discover-Traffic ist ein **Impuls, keine Basis**. Ein
Artikel, der monatlich liefern soll, braucht Search-Rankings; Discover addiert Spitzen darauf. Der
GSC-Discover-Bericht enthält außerdem **auch Chrome-Zugriffe** und erscheint erst ab einer nicht
bezifferten Mindest-Impressionszahl — beides gehört in die Erläuterung.

Falls die Domain keinen Discover-Traffic hat, ist das ein wichtiger Befund — die weiteren Phasen helfen dann zu verstehen, warum.

### Phase 2: Content-Qualität & E-E-A-T prüfen

Wähle 5-8 repräsentative Seiten aus: die Top-Discover-Seiten (falls vorhanden) plus einige aktuelle Artikel, die noch nicht in Discover aufgetaucht sind.

**Seitenabruf — so gehst du vor:**

Die Seiten müssen im HTML-Quellcode analysiert werden. Dafür gibt es mehrere Wege, die du in dieser Reihenfolge probieren solltest:

1. **Chrome-Browser-Tools** (bevorzugt, wenn verfügbar): Nutze `navigate` + `get_page_text` oder `read_page` um Seiten zu laden und den Quellcode zu lesen. Das funktioniert immer, wenn Chrome verbunden ist.
2. **web_fetch**: Funktioniert nur mit URLs, die der User direkt im Chat genannt hat. URLs aus Tool-Ergebnissen (z.B. aus gsc_search_analytics) werden blockiert. Wenn du diesen Weg nutzen willst, bitte den User, 2-3 Beispiel-URLs seiner Artikelseiten in den Chat zu schicken.
3. **Fallback ohne Seitenabruf**: Wenn weder Chrome noch web_fetch verfügbar sind, teile dem User mit, dass die Content-Qualitätsprüfung in dieser Session nicht vollständig durchgeführt werden kann. Führe Phase 1 (Discover-Daten) und Phase 3 (URL-Inspection, Sitemaps) durch und markiere alle Content-Qualitätspunkte als **"⚠ Zu prüfen"**. Bitte den User, beim nächsten Mal 2-3 Artikel-URLs direkt im Chat zu senden.

**2a. Bilder-Check (kritisch für Discover)**

Drei der fünf im SDK belegbaren Bild-Signale betreffen nicht das Motiv, sondern die **Zustellung**.
Deshalb wird beides geprüft.

**Harte Spezifikation** (Google-Doku), pro Seite abhaken:
- **≥ 1200 px Breite**
- **> 300.000 px Gesamtfläche** — eigenständige Anforderung. Ein 1200 × 200-Banner erfüllt die
  Breite und fällt trotzdem durch. Googles Beispiel: 1280 × 720 = 921.600 px
- **16:9**
- Beim Zuschnitt müssen die **wichtigen Details im beschnittenen Ausschnitt erhalten bleiben**
- **`max-image-preview:large`** im robots-Meta oder AMP — **der einzige harte technische Blocker
  der ganzen Doku**. Fehlt er, erscheint nur ein Mini-Thumbnail und die gesamte Bildarbeit läuft
  ins Leere. Beim Lesen aus rohem HTML **beide Anführungszeichen-Varianten** prüfen (WordPress
  schreibt `name='robots'` mit einfachen) und zusätzlich den HTTP-Header `X-Robots-Tag`, der das
  Meta-Tag überstimmt
- Untauglich: generische Motive, ausdrücklich das **Websitelogo**, und vollgeschriebene Grafiken

**Bildquelle und Priorität:**
- Die Parsing-Priorität ist hart codiert: **Schema.org JSON-LD → Open Graph → Twitter Cards →
  HTML-Meta**. Wer nur OG-Tags pflegt, arbeitet auf der zweiten Ebene
- Nennen `og:image`, JSON-LD `image` und `primaryImageOfPage` **dasselbe Motiv**? Widersprüchliche
  Quellen sind schlimmer als eine fehlende, weil Google dann wählt — und nicht zwingend das gute Bild
- Sind `og:image:width` und `og:image:height` gesetzt? Sie verhindern Fehl-Skalierung und falschen
  Zuschnitt

**Zustellung** (eigene Ranking-Signale, `EMBER_FEED_THUMBNAILS_DOWNLOADED` und
`image_load_failure_count`):
- Ist die Bild-URL **anonym abrufbar** — kein Login, kein Hotlink-Schutz, kein 404?
- Läuft sie über HTTPS? Leitet sie weiter (dann in `og:image` die Ziel-URL direkt angeben)?
- Ist der `Content-Type` ein `image/*`?
- Wie schnell antwortet das Bild-CDN? Ein gutes Thumbnail hinter einem langsamen CDN verliert an
  einer Stelle, die in keinem Content-Briefing auftaucht

**Formatwahl:** WebP oder JPEG. Bei Grenzfällen bei den Maßen nicht knapp über die Schwelle gehen —
das SDK kennt einen ausdrücklichen Negativmarker `LOW_QUALITY_IMAGE`, es gibt also nicht nur „gut
genug", sondern eine benannte Abwertung. Ab 1600 px Breite ist man auf der sicheren Seite.

Für die **Bildwirkung** bei echter Kartengröße ist der Skill `discover-titelbild` zuständig — er
rendert das Bild auf 340 × 190 und 80 × 80 und beurteilt es dort. Wenn die Bilder technisch in
Ordnung sind und die CTR trotzdem unter 5 % liegt, dorthin verweisen.

**2b. Artikel-Struktur & Content-Qualität**

- **Headline-Qualität**: Ist der Title-Tag ansprechend, klar und nicht clickbaity? Discover belohnt Titel, die neugierig machen ohne zu manipulieren.
- **Meta-Description**: Vorhanden und aussagekräftig?
- **Artikellänge**: Wie umfangreich ist der Content? (Discover bevorzugt tendenziell substantiellere Inhalte, aber es gibt keine Mindestlänge)
- **Struktur**: Gibt es H2/H3-Zwischenüberschriften? Ist der Content scanbar?
- **Publikationsdatum**: Ist ein Datum erkennbar? Discover bevorzugt aktuelle Inhalte.
- **Update-Datum**: Wird ein Aktualisierungsdatum angezeigt?

**2c. E-E-A-T-Signale**

- **Autor-Information**: Gibt es einen sichtbaren Autorennamen? Verlinkt er auf eine Autorenseite?
- **Autorenbox**: Gibt es eine Bio/Beschreibung des Autors?
- **Organisation**: Ist das Impressum / die "Über uns"-Seite leicht auffindbar?
- **Quellen & Verlinkungen**: Werden Aussagen mit Quellen belegt?

**2d. Schema Markup**

Prüfe im HTML-Quellcode auf structured data:
- `Article` oder `NewsArticle` Schema vorhanden?
- Enthält das Schema: `headline`, `image`, `datePublished`, `dateModified`, `author`?
- Ist der `author` als `Person` oder `Organization` ausgezeichnet mit `name` und idealerweise `url`?
- Gibt es `WebPage` oder `BreadcrumbList` Schema?

**2e. Startseiten-Verlinkung**

Rufe die Startseite der Domain ab und prüfe:
- Sind die aktuellen Discover-Top-Artikel prominent auf der Startseite verlinkt? Discover bewertet interne Verlinkung — Artikel, die weit oben auf der Startseite verlinkt sind, haben bessere Chancen, von Google als relevant eingestuft zu werden.
- Wo auf der Startseite tauchen die Artikel auf? (Above the fold, in einem Slider/Karussell, weiter unten, gar nicht?)
- Gibt es einen klar erkennbaren "Aktuelle Artikel"- oder "Neueste Beiträge"-Bereich?
- Wie viele Klicks sind es von der Startseite zum Artikel? (Idealerweise 1 Klick)

### Phase 3: Technische Discover-Signale

**3a. URL-Inspection & Redirect-Check** (für 3-5 der Beispielseiten)

Nutze `gsc_inspect_url` (nur wenn GSC-Zugang für die Domain besteht) um zu prüfen:
- Ist die Seite indexiert? (`verdict: "PASS"` und `coverageState: "Submitted and indexed"`)
- Mobile Usability — gibt es Probleme?
- Rich Results — welche sind aktiviert?
- Crawl-Status — wann wurde zuletzt gecrawlt?
- **Crawl-Typ**: Wird als MOBILE gecrawlt? (Sollte bei allen Seiten so sein)
- **Redirect-Check**: Das ist ein zentraler Prüfpunkt. Vergleiche die angefragte URL mit der `googleCanonical`-URL im Ergebnis:
  - Stimmen sie überein? → Kein Redirect-Problem.
  - Weichen sie ab? → Die angefragte URL leitet auf eine andere kanonische URL weiter. Prüfe:
    - Ist der `coverageState` = `"Page with redirect"`? Dann läuft der Discover-Traffic über eine Redirect-Kette.
    - Welche URL ist die kanonische? Sind interne Links und Sitemaps bereits auf die kanonische URL aktualisiert?
    - Wie viele der Top-Discover-URLs haben dieses Problem? (Prüfe mehrere)
  - Redirects sind nicht per se schlimm, aber sie kosten Crawl-Budget und können dazu führen, dass Google die Seite weniger effizient verarbeitet. Bei Top-Discover-Seiten sollten Redirects aufgelöst werden.

**3b. News-Sitemap-Check**

Die News-Sitemap ist für Discover besonders relevant, weil sie Google signalisiert, welche Inhalte aktuell und nachrichtenwertig sind. Nutze `gsc_list_sitemaps` um gezielt zu prüfen:

- **Existiert eine News-Sitemap?** Suche in den Ergebnissen nach einer Sitemap mit `type: "news"` in den `contents`. Typische Pfade sind `/news-sitemap.xml` oder als Teil eines Sitemap-Index.
- **Ist die News-Sitemap im Sitemap-Index referenziert?** Prüfe, ob die News-Sitemap als eigenständige Sitemap UND als Teil des `sitemap_index.xml` auftaucht. Idealerweise ist sie in beiden vorhanden.
- **Fehlerfrei?** Prüfe `errors` und `warnings` — beide sollten "0" sein.
- **Aktualität:** Wann wurde die News-Sitemap zuletzt von Google heruntergeladen (`lastDownloaded`)? Wenn der letzte Download mehr als 24 Stunden her ist, wird sie möglicherweise nicht regelmäßig abgerufen.
- **Umfang:** Wie viele URLs enthält die News-Sitemap (`submitted`)? News-Sitemaps sollten nur Artikel der letzten 48 Stunden enthalten (Google-Richtlinie). Wenn sie sehr viele URLs enthält (>200), könnte sie zu viele alte Artikel beinhalten.
- **Keine News-Sitemap vorhanden?** Das ist ein relevanter Befund. Empfehle die Einrichtung einer News-Sitemap, die automatisch die neuesten Artikel der letzten 48h enthält.

**3c. Allgemeine Sitemap-Infos**

Aus den Sitemap-Daten kannst du folgende Fakten ablesen und berichten — aber nur das, was die API tatsächlich zurückgibt:
- Anzahl der eingereichten URLs (aus `submitted`)
- Anzahl der indexierten URLs (aus `indexed`) — falls die API diesen Wert liefert. Achtung: Bei Sitemap-Index-Dateien zeigt `indexed` oft "0", weil der Index selbst keine URLs enthält. Nutze für die Index-Rate nur die Werte aus einzelnen Sitemaps (nicht aus dem Index).
- Bild-Einträge in der Sitemap (aus `type: "image"`)

**3d. Blocker-Tags — der stille Totalausfall**

Zwei Meta-Tags halten die Verarbeitung **komplett** an: **`notranslate`** und
**`nopagereadaloud`**. Beide werden gern von CMS- oder Übersetzungs-Plugins automatisch injiziert
und tauchen in **keinem** SEO-Tool als Fehler auf.

```js
JSON.stringify({
  notranslate: !!document.querySelector('meta[name="google"][content*="notranslate"], meta[name="notranslate"]'),
  nopagereadaloud: document.documentElement.innerHTML.includes('nopagereadaloud'),
  robots: document.querySelector('meta[name="robots"]')?.content,
  locale: document.querySelector('meta[property="og:locale"]')?.content,
  siteName: document.querySelector('meta[property="og:site_name"]')?.content,
  contentTier: [...document.querySelectorAll('meta[property="article:content_tier"]')].map(m => m.content),
  accessibleForFree: document.documentElement.innerHTML.match(/"isAccessibleForFree"\s*:\s*\w+/)?.[0]
})
```

Wenn eine Domain plötzlich keine Impressionen mehr hat und technisch alles in Ordnung wirkt, ist
das der **erste** Prüfpunkt — vor jeder Content-Spekulation.

**3e. Weitere eligibility-relevante Tags**

- **`og:locale`** beeinflusst die Eligibility, nicht nur die Darstellung: der Wert wird gegen die
  Nutzer-Locale gematcht. Bei deutschsprachigen Seiten konsequent `de_DE`, konsistent mit
  `hreflang` und `<html lang>`. Fehlt oder widerspricht es, kann das Ausspielung kosten, ohne
  irgendwo als Fehler aufzutauchen
- **`article:content_tier`** kennt **genau drei** Werte: `free`, `metered`, `locked`. Mehrere Werte
  gleichzeitig erzeugen einen Log-Eintrag — genau einen setzen. Bei Paywall wahrheitsgemäß, weil
  eine als frei ausgegebene Locked-Seite die enttäuschte Erwartung erzeugt, die Station 05 als
  schlechten Klick liest
- **`og:site_name`** — Publisher-Name im Karten-Header. Fehlt er, rät Google aus der Domain

**3f. Manuelle Maßnahmen und Richtlinien — vor jeder Content-Spekulation**

Die beiden **einzigen** echten Zulassungsbedingungen sind: indexiert und Inhaltsrichtlinien
eingehalten. Deshalb zuerst nachsehen, bevor über Content geredet wird:

- **GSC → „Sicherheit & manuelle Maßnahmen" → „Manuelle Maßnahmen für Discover"**. Liegt dort ein
  Eintrag, ist das die Antwort und alles andere zweitrangig. Kann der Skill das nicht selbst
  abrufen: als **„⚠ Zu prüfen"** mit genau diesem Klickpfad ausgeben
- **Werbeanteil** (nur bei werbefinanzierten Domains, dort aber zentral): Werbung und Werbemittel
  sollen den Anteil der Nachrichteninhalte **nicht überschreiten**. Auf den geprüften Artikelseiten
  abschätzen: wie viel Fläche above the fold ist Werbung, wie viele Anzeigenblöcke unterbrechen den
  Text? Das ist die einzige Discover-Regel, die direkt ins Geschäftsmodell greift
- **Gesponserte Inhalte deutlich gekennzeichnet?** Getarnte Sponsorings sind ein Richtlinienverstoß.
  Für ein Publisher-Portal mit Sponsoring-Modell der wichtigste Einzelpunkt dieses Abschnitts
- **Transparenz** ist Zulassungsvoraussetzung, nicht Optimierung: eindeutige Datumsangaben und
  Verfasserzeilen, Angaben zu Redaktion, Publikation und Herausgeber, Unternehmensangaben und
  **Kontaktdaten**. Fehlt davon etwas, ist es ein Zulassungsrisiko und keine Feinjustierung

**3g. Technische Basis** (wenn Seitenabruf möglich)

Prüfe anhand des HTML-Quellcodes:
- Viewport Meta-Tag vorhanden? (`<meta name="viewport" ...>`)
- HTTPS aktiv?
- Offensichtliche Performance-Probleme (exzessiv viele Scripts, keine Lazy-Loading-Hinweise)

### Phase 4: Bewertung & Empfehlungen

Fasse die Ergebnisse in einer strukturierten Bewertung zusammen. Verwende dieses Schema:

**Zuerst: die Stationsdiagnose.** Vor dem Score wird in zwei bis drei Sätzen gesagt, **an welcher
Station** es hängt — nach dem Raster oben. Ohne diese Aussage ist der Score eine Zahl ohne Richtung.

**Discover-Readiness Score** (0-100):
- **Zulassung** (0-15 Punkte): indexiert, keine manuelle Maßnahme, keine Blocker-Tags
  (`notranslate`/`nopagereadaloud`), Transparenz-Angaben vorhanden, Werbeanteil im Rahmen. Das ist
  Station 01 — ohne diese Punkte ist alles andere zweitrangig
- **Discover-Traffic-Status** (0-15 Punkte): Hat die Domain Discover-Traffic? Trend MoM und YoY —
  **und in welchen Verzeichnissen**? Ein Verzeichnis mit Publikationsvolumen und null Impressionen
  kostet hier Punkte, auch wenn die Domain-Summe gut aussieht
- **Bild-Optimierung** (0-25 Punkte): Spezifikation (Breite, Fläche, 16:9),
  `max-image-preview:large`, Quellen-Konsistenz und **Zustellung** (abrufbar, HTTPS, Content-Type,
  Ladezeit). Der wichtigste technische Faktor — ohne richtige Bild-Config passiert gar nichts
- **Content-Qualität** (0-20 Punkte): Artikelstruktur, Headline-Qualität, Tiefe, Aktualität,
  Startseiten-Verlinkung
- **E-E-A-T** (0-12 Punkte): Autoreninfos, Quellenangaben
- **Technische Basis** (0-13 Punkte): Schema Markup und Parsing-Priorität, `og:locale`,
  `article:content_tier`, Mobile UX, News-Sitemap, Redirects

**Deckel:** Liegt eine manuelle Maßnahme vor oder ist ein Blocker-Tag gesetzt, ist der Gesamtscore
auf **40** begrenzt — unabhängig von allem anderen. Fehlt `max-image-preview:large` domainweit,
maximal **60**. Beides im Bericht mit dem Grund ausweisen.

Wenn einzelne Bereiche nicht geprüft werden konnten, vergib keine Punkte für diesen Bereich, sondern markiere ihn als **"⚠ Nicht geprüft"** und passe den Gesamtscore entsprechend an (z.B. "33/35 geprüfte Punkte"). Stelle klar, welche Punkte auf Daten basieren und welche offen sind.

**Bewertungsstufen** (bezogen auf den geprüften Anteil):
- 80-100%: Sehr gut optimiert — Discover-Traffic sollte fließen wenn die Themen passen
- 60-79%: Gute Basis, aber es gibt konkrete Verbesserungsmöglichkeiten
- 40-59%: Deutliche Lücken — mehrere wichtige Faktoren fehlen
- 0-39%: Grundlegende Discover-Voraussetzungen nicht erfüllt

**Empfehlungen:**
Gib maximal 5-7 priorisierte, konkrete Empfehlungen. Jede Empfehlung muss sich auf einen konkreten Befund aus dem Audit beziehen — keine generischen Tipps ohne Datenbasis. Jede Empfehlung sollte enthalten:
- Was genau zu tun ist (nicht vage "verbessern Sie Ihre Bilder", sondern konkret "Fügen Sie `<meta name="robots" content="max-image-preview:large">` in den Head aller Artikelseiten ein")
- Auf welchen Befund sich die Empfehlung stützt (z.B. "In 3 von 5 geprüften Seiten fehlt dieses Tag")
- Geschätzter Impact (hoch/mittel/niedrig)

Sortiere Empfehlungen nach Impact — die wichtigsten zuerst.

## Wichtige Hinweise

- Stütze dich ausschließlich auf die tatsächlich abgerufenen Daten. Spekuliere nicht über Discover-Algorithmus-Details, die nicht belegt sind.
- Wenn GSC keinen Discover-Traffic zeigt, kann das verschiedene Gründe haben: Die Domain ist zu klein, die Themen passen nicht zum Discover-Profil, oder die technischen Voraussetzungen fehlen. Benenne alle möglichen Ursachen.
- Discover-Traffic ist von Natur aus volatil. Ein Rückgang ist nicht automatisch ein Problem — erkläre dem User diesen Kontext.
- Wenn der User nach einem Export als Dokument oder Präsentation fragt, erstelle die Ergebnisse im gewünschten Format. Nutze dafür die entsprechenden Skills (docx, pptx).
- Wenn Teilbereiche nicht geprüft werden konnten, markiere sie als **"⚠ Zu prüfen"** mit konkreter Anleitung, was der User manuell verifizieren sollte.

## Beispiel-Ausgabestruktur

Die Ausgabe im Chat sollte ungefähr so aufgebaut sein (als Fließtext mit Zwischenüberschriften):

```
## Google Discover Audit: [domain.de]

### Diagnose in drei Sätzen
[An welcher Station hängt es — mit dem Symptom aus den Daten belegt]
[Was der größte Hebel ist]
[Was er kostet]

### Zulassung (Station 01)
[Manuelle Maßnahmen: Eintrag vorhanden? Oder "⚠ Zu prüfen" mit Klickpfad]
[Blocker-Tags notranslate / nopagereadaloud: gesetzt?]
[Transparenz: Autor, Datum, Redaktion, Kontakt vorhanden?]
[Werbeanteil, falls werbefinanziert]

### Discover-Traffic-Status
[Clicks, Impressions, CTR der aktuellen Periode]
[Vergleich mit Vorperiode: +/-X% MoM]
[Vergleich mit Vorjahr: +/-X% YoY — oder "Vorjahresdaten nicht verfügbar"]
[CTR gegen Benchmark: News ~11%, Non-News ~6%, Ziel 7-9%, <5% Handlungssignal]
[Klick-Verhältnis Discover vs. Web — mit dem Hinweis, dass die CTR-Werte nicht vergleichbar sind]

### Traffic nach Verzeichnis
[Tabelle: Verzeichnis | Clicks | Impressionen | CTR]
[Welche Verzeichnisse sind discover-fähig, welche nicht — und publizieren sie trotzdem?]

### Top-Discover-Inhalte
[Welche Seiten performen, welche Themencluster erkennbar sind, CTR-Spitzen]

### Content-Qualität & E-E-A-T
[Befunde aus der Seitenanalyse: Bilder, Struktur, Autoreninfos, Schema]
[Startseiten-Verlinkung: Sind Top-Artikel prominent verlinkt?]
[Falls nicht prüfbar: "⚠ Zu prüfen:" mit konkreten Hinweisen]

### Technische Bewertung
[URL-Inspection: Indexierung, Redirect-Befunde, Crawl-Typ]
[News-Sitemap: Vorhanden? Im Index? Fehlerfrei? Aktuell?]
[Allgemeine Sitemap-Infos — nur belegbare Fakten]

### Discover-Readiness Score: XX/YY geprüfte Punkte
[Aufschlüsselung der Teilscores — nur bewertbare Bereiche bewertet]

### Empfehlungen
[Priorisierte, konkrete Maßnahmen — jede mit Bezug zu einem Befund]
[Bei Praxis-Heuristiken (News-Sitemap, Startseiten-Prominenz, Schema, Republishing) kennzeichnen,
 dass sie nicht in Googles Doku stehen]

### Vertiefung auf Artikelebene
[Welcher der vier Artikel-Skills adressiert den größten gefundenen Hebel — mit Begründung]
```

## Benötigte Tools

- `gsc_list_sites` — Vorab-Check ob GSC-Zugang für die Domain besteht
- `gsc_search_analytics` (mit type: "discover" und type: "web") — für Traffic-Daten (nur bei GSC-Zugang)
- `gsc_inspect_url` — für Indexierungs-, Redirect- und Mobile-Usability-Check (nur bei GSC-Zugang)
- `gsc_list_sitemaps` — für News-Sitemap- und allgemeine Sitemap-Prüfung (nur bei GSC-Zugang)
- Chrome-Browser-Tools (`navigate`, `get_page_text`, `read_page`) — für HTML-Quellcode-Analyse und Startseiten-Check (bevorzugt)
- `web_fetch` — Alternative für HTML-Analyse, wenn Chrome nicht verfügbar (nur mit User-bereitgestellten URLs)
