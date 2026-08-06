# Discover-Mechanik: Diagnoserahmen und belegte Signale

Grundlage für die Stationsdiagnose im Audit. Jede Aussage trägt ihre Evidenzstufe, weil davon
abhängt, wie verbindlich sie beim Kunden vertreten werden kann.

| Marke | Bedeutung |
|-------|-----------|
| **[Doku]** | Google-Discover-Dokumentation. Harte Anforderung. |
| **[Richtlinie]** | Discover-Inhaltsrichtlinien. Verstöße erscheinen als manuelle Maßnahme in der GSC. |
| **[SDK]** | Reverse Engineering des Google-App-SDK (Metehan Yeşilyurt). Client-Sicht zu einem Zeitpunkt, starkes Indiz — **nicht** als Spezifikation zitieren. Der Autor hat frühere Behauptungen selbst korrigiert. |
| **[Daten]** | Auswertung echter GSC-Daten (11.000 URLs / 62 Domains / 12 Monate). |
| **[Praxis]** | Bewährte Heuristik ohne Google-Beleg. |

---

## Die Pipeline — der Diagnoserahmen

Discover ist **Push, nicht Pull**: niemand stellt eine Anfrage. Jeder Artikel läuft eine Pipeline
durch und kann an **jeder einzelnen Station** hängenbleiben. Deshalb ist „schlechter
Discover-Traffic" nie eine Diagnose, sondern eine Frage: **an welcher Station?**

Kurzform: **Eligible → Classified → Matched → Ranked → Decays.**

| # | Station | Was dort passiert |
|---|---------|-------------------|
| 01 | **Eligibility** | Prüfung von Site-Trust und thematischer Autorität — **nicht** auf Domain-Ebene, sondern **pro Verzeichnis und pro Entität**. Besteht der Check, *kann* der Inhalt erscheinen. Mehr sagt er nicht. |
| 02 | **Klassifikation** | Google liest Entitäten und Thema und entscheidet, in welche Interessens-Schublade der Artikel fällt. |
| 03 | **Matching auf Kohorten** | Zuweisung an Nutzer-Kohorten mit passendem Interesse. Kohorten sind die Viralitäts-Maschine: wird eine gut bedient, trägt Google die Story in die nächste. |
| 04 | **Initial Exposure** | Startschub, gemessen an früher CTR. Getragen von **Headline, Bild und Markenwiedererkennung**. |
| 05 | **User Quality Assessment** | Gemessen wird Klick**qualität** nach dem Navboost-Modell, nicht Klickmenge. |
| 06 | **Engagement-Loop** | Laufendes Scoring über Impressionen, CTR und explizites Nutzerfeedback („weniger davon"). |
| 07 | **Personalisierung** | Abgleich mit Interessen und Historie des einzelnen Nutzers. Ab hier gibt es keine „Discover-Position" mehr, nur Verteilungen. |
| 08 | **Decay & Renewal** | Sichtbarkeit älterer Stories fällt; erfolgreicher Evergreen kann **re-promoted** werden. |

### Das Diagnose-Raster — die zentrale Tabelle des Audits

| Symptom in den Daten | Station | Wo im Audit geprüft |
|---|---|---|
| **Gar keine Impressionen** | 01 | Trust und Autorität im Verzeichnis, Indexierung, `max-image-preview:large`, Blocker-Tags, Richtlinienkonformität |
| **Impressionen bei der falschen Zielgruppe** | 02/03 | Entitäten und Themenschärfe der Top-Seiten |
| **Impressionen, aber kaum Klicks** | 04 | Headline und Titelbild |
| **Klicks, dann schneller Rücksprung** | 05 | Einlösung: hält der Artikel, was die Karte verspricht |
| **Guter Start, dann Abflachen** | 06/08 | Substanz, Aktualisierung, Re-Promotion |

Ein Audit, das diese Zuordnung nicht trifft, liefert eine Liste statt einer Diagnose.

### Eligibility ist nicht übertragbar — die wichtigste Konsequenz

Der Check läuft **pro Verzeichnis und pro Entität**. Eine Domain kann in einem Themenordner
discover-fähig sein und im nächsten überhaupt nicht. **Discover-Erfolg ist nicht von Thema zu
Thema übertragbar** — er wird pro Themenfeld erarbeitet.

Für das Audit heißt das: Traffic **nach Verzeichnis aufschlüsseln**, nicht nur als Domain-Summe
betrachten. Ein Domain-Score verdeckt genau den Befund, der handlungsleitend ist.

Zweistufige Filterung **vor** dem Ranking: `filter_collection_status` auf Domain-Ebene,
`filter_entity_status` auf URL-Ebene **[SDK]**. Ein auf Collection-Ebene blockierter Publisher
erreicht das Ranking gar nicht.

---

## Die fünf belegten Bild- und Aktualitätssignale **[SDK]**

Im SDK als Eingaben nachweisbar — die konkreteste Zielliste, die es für Discover gibt:

| Signal | SDK-Belegstelle | Optimierungsziel |
|--------|-----------------|------------------|
| Bildqualität | `LOW_QUALITY_IMAGE`, `image_width`, `image_height` | Maße deutlich über der Schwelle, nie knapp darüber |
| Aktualität | `freshness_delta_in_seconds` | Publish- und Update-Zeitpunkt bewusst setzen |
| Historische CTR **pro URL** | `click_count` / `show_count` | CTR-Historie als Asset behandeln |
| Thumbnail-Download | `EMBER_FEED_THUMBNAILS_DOWNLOADED` | Bild-URL schnell, öffentlich, unblockiert |
| Bild-Ladefehler | `image_load_failure_count` | Fehlerrate 0 — CDN, Hotlink-Schutz, 404 prüfen |

Drei der fünf betreffen **Bild-Infrastruktur**, nicht Bildmotiv. Discover misst nicht nur, *was*
auf dem Bild ist, sondern **ob und wie zuverlässig es ankommt**. Ein gutes Thumbnail hinter einem
langsamen Bild-CDN verliert an einer Stelle, die in keinem Content-Briefing auftaucht.

`LOW_QUALITY_IMAGE` ist ein **expliziter Negativ-Marker**: es gibt nicht nur „gut genug", sondern
eine benannte Abwertung. Bei Grenzfällen deutlich über die Mindestmaße gehen.

**Historische CTR hängt pro URL**, nicht pro Domain. Eine URL hat eine eigene Reputation im Feed,
die sie in künftige Ausspielungen mitnimmt. Zwei Folgen für Empfehlungen:

- Ein schwacher Start belastet **diese URL** dauerhaft. Titel- und Bildwechsel auf einer
  verbrannten URL wirken begrenzt.
- Ein bewährter Evergreen startet bei Re-Promotion mit Vorsprung.
- Bei grundlegend neuem Aufhänger ist eine **neue URL** die ehrlichere Option als die Reparatur
  der alten. Das gehört in die Empfehlung, wenn eine Top-URL dauerhaft unter 5 % CTR liegt.

---

## Bild-Spezifikation **[Doku]**

- **≥ 1200 px Breite**
- **> 300.000 Pixel Gesamtfläche** — eigenständige Anforderung; ein 1200 × 200-Banner erfüllt die
  Breite und fällt trotzdem durch. Googles Beispiel: 1280 × 720 = 921.600 px
- **16:9**
- **Beim Zuschnitt müssen die wichtigen Details im beschnittenen Ausschnitt erhalten bleiben**
- **`max-image-preview:large`** im robots-Meta oder AMP — **der einzige harte technische Blocker
  der ganzen Doku**. Fehlt er, erscheint nur ein Mini-Thumbnail
- Untauglich: generische Motive, ausdrücklich das **Websitelogo**, und Bilder mit *viel* Text
  (gemeint sind vollgeschriebene Grafiken, nicht ein kurzer Schriftzug)
- Bildquelle: `og:image` **oder** `WebPage` → `primaryImageOfPage` **oder** `mainEntity`/
  `mainEntityOfPage` → `BlogPosting` (`image`). Mehrere Quellen müssen **dasselbe Motiv** nennen

---

## Zwei Tags, die die Verarbeitung komplett stoppen **[SDK]**

`notranslate` und `nopagereadaloud` halten das Parsing an. Beide werden gern von **CMS- oder
Übersetzungs-Plugins automatisch injiziert** — ein stiller Totalausfall, der in keinem SEO-Tool
als Fehler auftaucht.

**Gehört in jede technische Abnahme.** Wenn eine Domain plötzlich keine Impressionen mehr hat und
technisch alles in Ordnung wirkt, ist das der erste Prüfpunkt.

## Parsing-Priorität, hart codiert **[SDK]**

**Schema.org JSON-LD → Open Graph → Twitter Cards → HTML-Meta.**

Wer nur OG-Tags pflegt, arbeitet auf der zweiten Ebene. Für Titel, Autor, Publisher und Bild gibt
es je eine eigene Fallback-Kette. Widersprüchliche Angaben zwischen Schema und OG sind schlimmer
als eine fehlende — Google muss dann wählen, und die Wahl fällt nicht zwingend auf das gute Bild.

Bild-Fallback-Kette: `og:image` → `twitter:image` → `og:image:secure_url` → `twitter:image:src` →
generisches `image`. Ohne verfügbares Thumbnail entsteht **keine Karte**, es gibt keinen
Textfallback.

`og:locale` beeinflusst die **Eligibility**, nicht nur die Darstellung: es wird gegen die
Nutzer-Locale gematcht. Bei deutschsprachigen Seiten konsequent `de_DE`, konsistent mit
`hreflang` und `<html lang>`.

`article:content_tier` kennt **genau drei** Werte: `free`, `metered`, `locked`. Mehrere Werte
erzeugen einen Log-Eintrag — also genau einen setzen. Vorher wird `isAccessibleForFree` geprüft
(Schema, Default `true`).

---

## Kennzahlen **[Daten]**

Aus einer GSC-Auswertung über 11.000 URLs von 62 Domains über 12 Monate:

| Kennzahl | Wert |
|----------|------|
| CTR News-Seiten | ~11 % |
| CTR Non-News | ~6 % |
| CTR klassische Suche zum Vergleich | ~4 % |
| **Arbeitsziel** | **7–9 %** |
| Handlungssignal | unter 5 % |

**Der Vergleich mit der Search-CTR ist nicht zulässig** — und das ist der wichtigere Punkt:
Discover zählt eine Impression erst, wenn eine **Karte sichtbar** wird; die Suche zählt sie,
sobald die Ergebnisseite ausgeliefert wird, auch ohne Sichtbarkeit der Position. Die
Discover-CTR ist strukturell höher, ohne dass etwas besser läuft. Wer beides im Report
nebeneinanderstellt, vergleicht zwei verschiedene Nenner — das muss dabeistehen.

Virale Ausreißer von 20–30 % werden berichtet, sind aber **unbelegt** (nur Sekundärquellen ohne
Datenbasis). Als Größenordnung nutzbar, nicht als Benchmark zitieren.

## Freshness und Lebenszyklus

Aktualität geht als `freshness_delta_in_seconds` ein — **in Sekunden**, nicht in Tagen **[SDK]**.

| Alter | Gewichtung |
|-------|-----------|
| 1–7 Tage | höchste |
| 8–14 Tage | mittlere |
| 15–30 Tage | niedrigste |
| über 30 Tage | kontinuierlicher Verlust |

*Belastbarkeit:* Die Staffelung stammt aus der SDK-Analyse; derselbe Autor hat später relativiert,
dass die Werte aus einem Gesture-Settings-Kontext stammen und nicht sicher Discover-Klassen
zuzuordnen sind. Als **Arbeitsmodell** nutzen, nicht als Google-Spezifikation zitieren.

Merksatz: **erste Stunden = Höhe, erste Woche = Dauer, ab Tag 15 = Republishing.**

**Kein Freshness-Zwang [Doku]:** Ältere Inhalte werden ausgespielt, wenn sie zu den
Nutzerinteressen passen. Evergreen-Re-Promotion ist von Google gedeckt, nicht bloß ein Trick.

**Planerische Konsequenz:** Discover-Traffic ist ein **Impuls**, keine Basis. Ein Artikel, der
monatlich liefern soll, braucht Search-Rankings; Discover addiert Spitzen darauf. Das gehört in
jede Erwartungssteuerung beim Kunden.

---

## Volatilität richtig einordnen

**Volatilität ist laut Google Konstruktionsmerkmal**, nicht Fehlerbild **[Doku]** — Ursachen sind
sich ändernde Nutzerinteressen, veränderte Inhaltstypen im Feed und Such-Updates.

Dazu aus dem SDK: `SHOW_SKIPPED_DUE_TO_COUNTERFACTUAL`, `VISIBILITY_REPRESSED_COUNTERFACTUAL` und
ein Zähler `background_refresh_rug_pull_count` für Inhalte, die **schon im Feed waren und
retroaktiv entfernt wurden**. Ein Teil der beobachteten Volatilität ist also **Test-Design, nicht
Qualitätsurteil**. Einzelne Einbrüche nicht überinterpretieren — im Audit über mindestens 28 Tage
plus Vorjahresvergleich arbeiten.

**Tombstoning:** Von Nutzern weggewischte oder mit „nicht mehr anzeigen" markierte Inhalte werden
permanent markiert und kommen nicht zurück. Negative Nutzersignale sind endgültig, nicht abklingend.

**13 Cluster-Typen** bestimmen, in welcher Feed-Sorte eine Karte landet — u. a. `neoncluster`
(Haupt-Content), `geotargetingstories`, `deeptrends`, `freshvideos`, `mustntmiss`,
`newsstoriesheadlines`, `trendingugc`. Erklärt, warum dasselbe Thema mit anderem Zuschnitt völlig
anders läuft: es landet in einem anderen Cluster.

**WPAS** („Web Publisher Articles Signal") ist ein eigener Personalisierungs-Subtyp, der
wahrscheinlich mit der **Registrierung im Google Publisher Center** zusammenhängt. Das nuanciert
Googles Aussage, es brauche keine Anmeldung: nötig ist sie nicht, aber sie führt offenbar zu einer
**anderen Klassifizierung**. Für ein Publisher-Portal ein prüfenswerter Hebel.

---

## Audience-Signale — die „Backlinks" von Discover

Der am häufigsten übersehene Faktor. Discover bewertet, ob der Content **bereits bei einem echten
Publikum resoniert**:

- In der Suche sagen **Backlinks** „dieser Seite kann man trauen".
- In Discover sagen **Audience-Signale** „das ist es wert, weiter verteilt zu werden".

Ohne initiale Traktion keine Distribution — auch bei objektiv starkem Artikel. Publisher mit
engagiertem, wiederkehrendem Publikum starten strukturell im Vorteil: ihre frühen Signale
entstehen von allein.

Für das Audit: eigene Kanäle (Newsletter, Social, Stammpublikum) sind kein Nebenschauplatz,
sondern **Zulieferer des Discover-Signals**. Wenn eine Domain technisch sauber ist und trotzdem
keine Traktion bekommt, ist das der Prüfpunkt.

## Sniper statt Volumen **[Praxis]**

Redaktionen halten Discover meist für ein Volumenspiel — es ist das Gegenteil. Mehr Artikel
verwässern die durchschnittlichen Engagement-Signale der **ganzen** Site; der Algorithmus sieht
schwächere Signale über die gesamte Domain, und selbst die besten Artikel werden mitgezogen.

Beobachtet: Publisher mit 100+ Artikeln pro Tag liegen im Discover-Traffic unter Sites mit unter
10 pro Tag. *(Praxisbeobachtung ohne öffentliche Quelle — nicht als Kennzahl zitieren.)*

Im Audit relevant, wenn die Domain hohe Publikationsfrequenz bei schwacher Discover-CTR zeigt:
dann ist Frequenzreduktion eine legitime Empfehlung.

---

## Richtlinien als zweite Zulassungsbedingung **[Richtlinie]**

Nur zwei echte Zulassungsbedingungen: **indexiert** und **Inhaltsrichtlinien eingehalten**. Keine
Anmeldung, keine speziellen Tags, keine strukturierten Daten erforderlich.

Aus den Richtlinien, was im Audit tatsächlich prüfbar ist:

- **Werbeanteil:** Werbung und Werbemittel sollen den Anteil der Nachrichteninhalte **nicht
  überschreiten**. Gesponserte Inhalte **deutlich kennzeichnen**, keine getarnten Sponsorings.
  Die einzige Discover-Regel, die direkt ins Geschäftsmodell und Seitenlayout greift — für
  werbefinanzierte Sites die härteste. **Gehört in jedes Audit einer Publisher-Domain.**
- **Irreführende Vorschauinhalte:** verboten sind Vorschauinhalte, die zur Interaktion verleiten,
  indem **Details vorgetäuscht** werden. Die Regel greift am **Vorschau**-Element — `og:title` und
  `og:image` — nicht am Artikeltext.
- **Transparenz ist Pflicht, nicht Kür:** eindeutige Datumsangaben und Verfasserzeilen,
  Informationen zu Redaktion, Publikation und Herausgeber, Angaben zum Unternehmen sowie
  Kontaktdaten. Fehlt das, ist es kein Optimierungsdefizit, sondern ein Zulassungsrisiko.
- Zehn Verbotskategorien aus der Suche; medizinische Inhalte sind beschränkt, nicht verboten.

Verstöße erscheinen in der GSC unter **„Sicherheit & manuelle Maßnahmen" → „Manuelle Maßnahmen
für Discover"**. Im Audit immer nachsehen, bevor über Content spekuliert wird.

## Was in Googles Doku ausdrücklich *nicht* steht

Wichtig gegen Mythenbildung — diese Punkte sind **Praxis-Heuristik**, nicht Google-Anforderung:
Startseiten-Prominenz, News-Sitemap, `Article`-Schema, Autorenseiten als eigene URLs, Republishing,
Follow-Funktion, Web Stories, Google-News-Anmeldung, Interstitial-Regeln, interne Verlinkung.

Sie können trotzdem wirken — aber im Kundenbericht als Praxis-Empfehlung kennzeichnen, nicht als
„Google verlangt". Autoren- und Datumsangaben gehören **nicht** in diese Liste: sie sind über die
Transparenz-Regel Zulassungsvoraussetzung.

## Messung

GSC-Discover-Bericht: Impressionen, Klicks, CTR über **16 Monate**, erscheint erst ab einer
**nicht bezifferten** Mindestanzahl an Impressionen und enthält **auch Chrome-Zugriffe** **[Doku]**.

Der Chrome-Anteil ist ein häufiger Erklärungsbedarf beim Kunden: der Bericht ist nicht rein
Discover-App-Traffic.
