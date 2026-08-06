# Feed-Karten-Analyse: „Wow! Top-Deal bei Kleines Kraftwerk mit Anker SOLIX 3"

Beispielausgabe des Skills `discover-feedkarte` an einem echten, professionell produzierten
Titelbild von homeandsmart.de. Zeigt, dass ein technisch einwandfreies Bild an der Kartengröße
und am Zusammenspiel mit der Headline verlieren kann.

**Bild:** `2000-watt-kleines-kraftwerk.jpg` · 1600 × 900 px · JPEG 242,5 KB ·
**Motiv:** zwei Solarmodule auf einem Balkon, überlagert von Textbalken „2.000 WATT
BALKONKRAFTWERK", Störer „TOP DEAL! KLEINER PREIS", Logo „kleines kraftwerk" oben links,
Markenblock „ANKER SOLIX SOLARBANK 3" oben rechts · **Analyse:** 2026-08-06

## Feed-Karten-Score: 64 / 100 — Mittel

Technisch ist die Karte tadellos, sie verliert aber an drei Stellen: das Bild zeigt Module,
während der Artikel vom Speicher handelt; der quadratische Beschnitt zerstört Logo und
Markenblock vollständig; und Bild und Headline sagen dreimal dasselbe. Der größte Hebel ist
kostenlos — ein anderer Ausschnitt und eine Headline, die einen anderen Fakt trägt als das Bild.
Aufwand: rund 20 Minuten, kein neues Bildmaterial nötig.

| Dimension | Punkte | Befund |
|-----------|-------:|--------|
| K1 Technische Auslieferbarkeit | 24 / 25 | 1600 px, exakt 16:9, `max-image-preview:large` gesetzt — nur das Format ließe sich verbessern |
| K2 Bildaussage | 14 / 30 | Gezeigt werden Module, Artikelgegenstand ist der 2-kWh-Speicher; keine menschliche Präsenz |
| K3 Tauglichkeit bei Kartengröße | 16 / 25 | Große Karte trägt; die 80 × 80-Ansicht zerstört Logo und Marke |
| K4 Zusammenspiel mit der Headline | 10 / 20 | Dreifache Doppelung, Fremdmarken dominieren die Fläche |

## Was in welcher Größe verschwindet

Die zentrale Tabelle. Grundlage: `ansicht_feedkarte_340x190.png` und `ansicht_kompakt_80x80.png`.

| Element | Original 1600 × 900 | Feed-Karte 340 × 190 | Kompakt 80 × 80 |
|---|---|---|---|
| „2.000 WATT BALKONKRAFTWERK" | vollständig | **vollständig lesbar** | zu „000 WATT" / „…KRAFTWERK" zerschnitten |
| Störer „TOP DEAL! KLEINER PREIS" | vollständig | lesbar | angeschnitten, Text unleserlich |
| Logo „kleines kraftwerk" | vollständig | an der Lesbarkeitsgrenze | **komplett weggeschnitten** |
| Markenblock „ANKER SOLIX" | vollständig | „ANKER" lesbar | **komplett weggeschnitten** |
| „SOLARBANK 3" | vollständig | nur mit Mühe entzifferbar | weggeschnitten |
| Solarmodule | dominant | klar erkennbar | erkennbar, aber ohne Kontext |
| Balkon, Pflanze, Stadtkulisse | detailreich | zu Farbflächen reduziert | nicht mehr deutbar |

Der gemessene Informationsverlust bei Feed-Größe beträgt 6,69 % — über der Prüfschwelle von 6 %.
Die Prüfung an der Kartenansicht zeigt: **betroffen ist nur Textur** (Zellstruktur der Module,
Blattwerk, Himmel), nicht die Bildaussage. Deshalb kein Abzug bei K3 3a über den Nebendetails
hinaus. Genau dafür ist der Messwert ein Prüfauftrag und kein Urteil.

Die Kompaktansicht ist der eigentliche Befund: Beide Markenelemente liegen im äußeren Fünftel
und fallen im quadratischen Beschnitt weg. Übrig bleiben Schriftfragmente, die wie ein
Darstellungsfehler wirken.

## Karten-Zusammenspiel

Headline: „Wow! Top-Deal bei Kleines Kraftwerk mit Anker SOLIX 3" (52 Zeichen)

| Information | in der Headline | im Bild |
|---|---|---|
| Top-Deal | ✅ | ✅ „TOP DEAL! KLEINER PREIS" |
| Kleines Kraftwerk | ✅ | ✅ Logo |
| Anker SOLIX | ✅ | ✅ Markenblock |
| 2.000 Watt | ❌ | ✅ Textbalken |
| 2 kWh Speicher (Artikelthema) | ❌ | ❌ |
| Preis oder Ersparnis | ❌ | ❌ |

Drei von vier Elementen sind doppelt belegt. Die Karte hat rund 340 × 190 Punkte plus eine
Textzeile — und nutzt davon drei Slots für dieselbe Aussage. Der Artikelgegenstand, der 2-kWh-
Speicher als Testsieger, kommt in keinem der beiden Kanäle vor.

K4 4a liegt deshalb bei 3 von 8: zwischen „wiederholt die Headline" (2) und „illustriert ohne zu
ergänzen" (5) — das Bild ergänzt genau einen Fakt, die 2.000 Watt.

Zusätzlich dominieren zwei Fremdmarken die Fläche, ohne dass ein redaktionelles Motiv dagegen
steht. K4 4b: 2 von 4. In einem redaktionellen Feed erhöht das die Rücksprungwahrscheinlichkeit
bei Nutzern, die eine Einordnung erwarten und eine Werbefläche bekommen.

## Maßnahmen

**1. Ausschnitt umbauen: Tragendes in das mittlere Quadrat** — 15 Min, aus dem vorhandenen Bild ·
+4 Punkte (K3 3c: 1 → 5)
Logo und Markenblock aus den äußeren Fünfteln in Richtung Bildmitte rücken, sodass der 80 × 80-
Beschnitt sie nicht verliert. Faustregel für die Bildproduktion: alles, was tragen soll, liegt im
mittleren Quadrat des 16:9-Rahmens.

**2. Headline auf einen anderen Fakt umstellen** — 5 Min · +5 Punkte (K4 4a: 3 → 8)
Das Bild sagt bereits „Top-Deal", „Kleines Kraftwerk", „Anker SOLIX". Die Headline soll deshalb
den Fakt tragen, den das Bild nicht hat — den Speicher und seine Zahl. Vorschlag:
„2 kWh Speicher im Test: Anker Solarbank 3 jetzt 300 Euro günstiger" (65 Zeichen, wenn der Preis
stimmt). Damit trägt die Karte zwei Aussagen statt einer.

**3. Speicher ins Bild holen** — Auftrag, neues Bildmaterial · +6 Punkte (K2 2a: 4 → 10)
Der Artikel handelt vom 2-kWh-Speicher als Testsieger; gezeigt werden Module. Ein Motiv, in dem
die Solarbank selbst dominiert, würde die Kern-Entität sichtbar machen. Zweitbeste Lösung ohne
neues Material: den Markenblock „SOLARBANK 3" so vergrößern, dass er in der Feed-Karte klar
lesbar ist.

**Erreichbarer Score: 79 / 100** (Band „Solide") mit Maßnahmen 1 und 2 allein — beide kosten
zusammen 20 Minuten und kein Bildbudget. Mit Maßnahme 3: 85.

Weiteres Potenzial, nicht in den Top 3: menschliche Präsenz (K2 2c steht bei 0 von 6). Eine Person,
die die Solarbank anschließt, würde sowohl 2a als auch 2c heben — das ist aber ein Shooting, kein
Ausschnitt.

## Technische Fixes

| Punkt | Status | Fix |
|---|---|---|
| Breite 1600 px | ✅ | über der 1200-px-Schwelle für die große Karte |
| Seitenverhältnis 16:9 exakt | ✅ | kein Beschnittverlust |
| `max-image-preview:large` | ✅ | gesetzt: `<meta name='robots' content='index, follow, max-image-preview:large, …'>` |
| Format JPEG, 242,5 KB | ⚠️ | als WebP rund 40 % kleiner bei gleicher Qualität — K1 1c: 3 → 4 |
| Ausgebrannte Flächen 12,6 % | ⚠️ | unter der 15-%-Schwelle, kein Abzug. Der helle Himmel im oberen Drittel reduziert aber die Abgrenzung gegen einen hellen Feed-Hintergrund |
| RMS-Kontrast 88,0 · Farbigkeit 80,8 | ✅ | deutlich über den Schwellen; die Karte fällt im Feed auf |

## Methodik

**Gemessen** mit `feedcard.py`: Maße, Seitenverhältnis und Beschnittverlust, Format und
Dateigröße, Helligkeit, RMS-Kontrast, ausgebrannte Flächenanteile, Farbigkeit nach
Hasler-Süsstrunk (80,8), Informationsverlust bei Feed-Größe (RMS-Abweichung nach Rundreise über
340 × 190: 6,69 % des Wertebereichs).

**Visuell beurteilt** an den drei gerenderten Ansichten: Erkennbarkeit der Kern-Entität,
Bildsprache, Schriftlesbarkeit, Wirkung des quadratischen Beschnitts, Markenverhältnis.

**Nicht prüfbar:** Welche Bildquelle Google tatsächlich wählt — `og:image`, JSON-LD-`image` oder
Seitenbild. Hier stimmen `og:image` und Artikelbild überein, was das Risiko ausschließt. Ob die
Karte beim Nutzer exakt 340 × 190 groß ist, ist nicht dokumentiert; die Größenordnung ist
belastbar, die exakte Pixelzahl nicht. Der Score ist kein CTR-Wert.

**Nicht Teil dieser Analyse:** Artikeltext, Entitätenabdeckung, Schema-Markup
(→ `discover-content-optimizer`), News-Sitemap und Startseiten-Prominenz
(→ `discover-artikel-optimierer`).
