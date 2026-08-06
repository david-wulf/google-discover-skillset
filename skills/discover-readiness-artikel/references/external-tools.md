# Vertiefungs-Skills und externe Tools

Stand: 2026-08-06. Drei der fünf früher hier gelisteten externen Web-Tools sind inzwischen als
lokale Skills nachgebaut. Der Grund ist nicht Bequemlichkeit: beim letzten Test war der
pCTR Predictor **nicht funktionsfähig** (Anthropic-Guthaben erschöpft, OpenAI-Fallback mit
veraltetem Parameter), und der Discover Optimizer liefert unkalibrierte Bewertungen — alle
Headline-Varianten landeten zwischen 8,4 und 9,5 von 10. Ein Kundenbericht darf nicht davon
abhängen, ob ein fremdes Deployment gerade läuft.

## Lokale Skills — erste Wahl

| Hebel | Skill | Ersetzt |
|-------|-------|---------|
| **Headline** (`og:title`) | `discover-headline` | pCTR Predictor (pctr-discover.pages.dev) |
| **Titelbild** | `discover-titelbild` | Image-to-Google-Discover (HF Space metehan777) |
| **Artikeltext, Entitäten** | `discover-content-optimizer` | Advanced Google Discover Optimizer (Replit) |
| **Textqualität, kanalunabhängig** | `content-checker` | — |

### discover-headline

Acht gewichtete Dimensionen, Clickbait-Abzug, Umrechnung in pCTR, Variantenvergleich mit Delta.
Formel und Gewichte sind aus dem Original übernommen, damit die Werte vergleichbar bleiben; die
Bewertungsanker der Dimensionen sind ergänzt, weil das Original sie nicht veröffentlicht.

**Im Bericht das Delta in Prozentpunkten angeben, nicht den Absolutwert.** Der Modell-Mittelpunkt
liegt bei 11,3 % und damit über dem Arbeitsziel von 7–9 % — ein mittelmäßiger Titel bekommt sonst
eine zu freundliche Zahl.

### discover-titelbild

Misst die Google-Spezifikation (Breite ≥ 1200 px, Fläche > 300.000 px, 16:9, Format) und die
Auslieferung (HTTPS, Content-Type, Weiterleitung, Downloadzeit), rendert das Bild dann auf die
echten Kartengrößen **340 × 190** und **80 × 80** und beurteilt es dort. Der wichtigste
Ausgabeteil ist die Tabelle „was in welcher Größe verschwindet".

### discover-content-optimizer

Entitäten nach Typ, Beziehungen, fehlende Entitäten mit Priorität, Integrations-Score je Entität,
semantische Lücken, JSON-LD samt Validierung, thematische Kernbegriffe gegen TF-IDF-Spitzen.
Liefert einen Discover Content Score 0–100 mit dokumentierter Rubrik.

## Extern, weiterhin nützlich

### Teaser-Optimizer für die og:description

**URL:** https://huggingface.co/spaces/metehan777/neuralseo

Bewertet den Teaser-Text unter dem Titel in der Feed-Karte. Regel unabhängig vom Tool: Die
Description **löst das Titel-Versprechen weiter auf, sie wiederholt es nicht.** Ein doppelter Titel
in Titel und Description verschenkt die zweite Zeile der Karte.

Optional, kein Blocker. Wenn nicht erreichbar: im Bericht vermerken und die Description nach der
Regel oben selbst bewerten.

### Newsifier Publisher Insights

**URL:** https://www.newsifier.com/publisher-insights/

Benchmark-Kontext für Publisher im Discover-Ökosystem. Nur als Einordnung nutzen, nicht als
Zielwert. Belastbarere Zahlen liegen im Skill selbst vor: News-Seiten rund 11 % CTR, Non-News rund
6 %, Arbeitsziel 7–9 %, unter 5 % Handlungssignal — aus einer GSC-Auswertung über 11.000 URLs von
62 Domains über 12 Monate. Wenn Newsifier abweicht, gilt die Auswertung mit der größeren Datenbasis.

### Google Search Console

Keine Alternative, sondern die Datenbasis: Discover-Bericht mit Impressionen, Klicks und CTR über
16 Monate. Erscheint erst ab einer nicht bezifferten Mindest-Impressionszahl und enthält **auch
Chrome-Zugriffe** — das gehört in jede Erläuterung beim Kunden.

Richtlinienverstöße stehen unter **„Sicherheit & manuelle Maßnahmen" → „Manuelle Maßnahmen für
Discover"**. Immer zuerst dort nachsehen, bevor über Content spekuliert wird: liegt ein Eintrag vor,
ist das die Antwort und alles andere zweitrangig.

## Wenn ein Skill nicht verfügbar ist

Kein Grund, den Prozess anzuhalten. Dann nach den Kriterien in `discover-kriterien.md` selbst
bewerten und im Bericht unter Methodik vermerken, dass die Bewertung ohne das jeweilige
Rechen-Backend erfolgt ist — also geschätzt statt gemessen.
