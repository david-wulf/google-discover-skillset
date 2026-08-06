# Feed-Karten-Score — Rubrik

100 Punkte über vier Dimensionen. Punkte werden pro Unterkriterium vergeben, jeweils mit einem
Messwert aus `feedcard.py` oder einer benannten Beobachtung in einer der gerenderten Ansichten.

| Dimension | Punkte |
|-----------|-------:|
| K1 Technische Auslieferbarkeit | 25 |
| K2 Bildaussage | 30 |
| K3 Tauglichkeit bei Kartengröße | 25 |
| K4 Zusammenspiel mit der Headline | 20 |

**Zwischenwerte** sind zulässig, wenn zwei Anker gleichzeitig zutreffen — dann nennt die
Begründung beide. Beispiel: ein Bild, das drei von vier Headline-Elementen wiederholt, aber einen
Fakt ergänzt, liegt bei 4a zwischen „wiederholt" (2) und „illustriert ohne zu ergänzen" (5).
Was nicht zulässig ist: einen Zwischenwert wählen, um eine unangenehme Einordnung zu vermeiden.

---

## K1 — Technische Auslieferbarkeit (25)

**1a Breite (0–10)** — aus `dimensions.width`

| Breite | Punkte |
|--------|-------:|
| ≥ 1600 px | 10 |
| 1200–1599 px | 9 |
| 1000–1199 px | 4 |
| 700–999 px | 2 |
| < 700 px | 0 |

Unter 1200 px zeigt Discover statt der großen Karte nur ein kleines Vorschaubild. Das ist kein
Schönheitsfehler, sondern der Verlust der Fläche, über die geklickt wird.

**1b Seitenverhältnis (0–6)** — aus `dimensions.aspect_ratio` und `crop_loss_16x9`

| Zustand | Punkte |
|---------|-------:|
| 16:9, Abweichung ≤ 3 % | 6 |
| Abweichung ≤ 10 %, Beschnittverlust < 10 % der Fläche | 5 |
| Beschnittverlust 10–20 % ohne Verlust tragender Elemente | 3 |
| Beschnittverlust > 20 %, oder tragende Elemente fallen weg | 1 |
| Hochformat (Verhältnis < 1,0) | 0 |

**1c Format und Dateigröße (0–4)**
- 4 = WebP oder AVIF, unter 250 KB
- 3 = JPEG unter 300 KB
- 2 = JPEG über 300 KB
- 1 = PNG (ohne Transparenzbedarf) oder über 600 KB
- 0 = animiertes Format, oder über 1,5 MB

**1d `max-image-preview:large` (0–5)**
- 5 = gesetzt
- 0 = fehlt oder `<meta name="robots">` ist nicht vorhanden
- 3 = nicht prüfbar (Bild-only- oder Screenshot-Eingabe) — im Bericht als geschätzt markieren

Ohne dieses Signal darf Google das Bild nicht groß darstellen. Ein 1600-px-Bild ohne
`max-image-preview:large` verhält sich wie ein 600-px-Bild.

---

## K2 — Bildaussage (30)

Rein visuell, aus der 340 × 190-Ansicht. Jedes Urteil nennt, was zu sehen ist.

**2a Kern-Entität erkennbar (0–10)**
- 10 = Die Kern-Entität des Artikels ist auf den ersten Blick identifizierbar und dominiert das Bild
- 7 = erkennbar, aber nicht dominant
- 4 = nur mit Vorwissen oder erst nach genauem Hinsehen erkennbar
- 2 = thematisch verwandt, aber eine andere Sache als der Artikelgegenstand
- 0 = nicht erkennbar oder thematisch beliebig

**2b Bildsprache (0–8)**
- 8 = Close-up oder klar dominantes Einzelmotiv; ein Blickanker
- 6 = mittlere Distanz, Motiv klar abgegrenzt
- 3 = Weitwinkel oder Übersichtsaufnahme mit mehreren konkurrierenden Elementen
- 0 = überfüllte Collage, Screenshot einer Oberfläche oder Infografik ohne Blickanker

**2c Menschliche Präsenz (0–6)**
- 6 = Gesicht mit erkennbarem Ausdruck, groß im Bild
- 4 = Person handelnd sichtbar, Gesicht klein oder abgewandt
- 2 = Hände oder Körperteile im Einsatz
- 0 = keine menschliche Präsenz

Kein Abzug, wenn das Thema Menschen inhaltlich ausschließt — dann wird 2c mit 3 Punkten neutral
bewertet und das im Bericht begründet.

**2d Spezifik statt Generik (0–6)**
- 6 = erkennbar spezifisch zu diesem Artikel: das konkrete Produkt, der konkrete Ort, die
  konkrete Person
- 4 = passendes, aber austauschbares Motiv
- 2 = erkennbares Stockfoto-Muster (glatte Studio-Optik, generische Szene, Symbolbild)
- 0 = Symbolbild ohne Bezug, oder ein Motiv, das für Dutzende Artikel passen würde

---

## K3 — Tauglichkeit bei Kartengröße (25)

**3a Bildaussage in der 340 × 190-Ansicht (0–10)**
- 10 = Aussage trägt vollständig; nichts Tragendes verloren
- 7 = Aussage trägt, Nebendetails verloren
- 4 = Aussage nur noch angedeutet
- 0 = in Kartengröße nicht mehr lesbar oder verwechselbar

Der Messwert `detail.loss_pct_of_range` ist hier **Prüfauslöser, nicht Urteil**: Er unterscheidet
nicht zwischen verschwindender Schrift und verschwindender Textur. Bei einem Wert über 6 % wird
die Kartenansicht gezielt daraufhin geprüft, ob die Bildaussage betroffen ist. Ist nur Textur
betroffen (Materialstruktur, Blattwerk, Himmel), gibt es keinen Abzug.

**3b Schriftlesbarkeit (0–6)**
- 6 = keine Schrift im Bild, oder alle Schrift bleibt lesbar
- 4 = die tragende Aussage bleibt lesbar, Beiwerk nicht
- 2 = nur Fragmente lesbar
- 0 = Schrift wird zu Grafikrauschen

Immer wörtlich zitieren, was noch entzifferbar ist. Fragmente sind schlimmer als keine Schrift:
ein angeschnittenes „000 WATT" wirkt wie ein Fehler.

**3c Kompaktansicht 80 × 80 (0–5)**
- 5 = Motiv bleibt im quadratischen Beschnitt intakt und verständlich
- 3 = Motiv erkennbar, Marke oder Logo fällt weg
- 1 = Beschnitt zerstört die Aussage, Schriftfragmente bleiben stehen
- 0 = im Quadrat nicht mehr deutbar

Randständige Logos und Markennamen sind hier der Regelfall des Scheiterns. Konsequenz für die
Bildproduktion: alles Tragende in das mittlere Quadrat legen.

**3d Kontrast und Auffälligkeit (0–4)** — aus `luminance.rms_contrast` und `colorfulness`
- 4 = RMS-Kontrast ≥ 60 und Farbigkeit ≥ 40
- 3 = eines von beiden erfüllt
- 2 = RMS-Kontrast 40–59
- 0 = RMS-Kontrast < 40 und Farbigkeit < 20

Zusätzlich prüfen: `clipped_white_pct` über 15 % bedeutet ausgebrannte Flächen — in einem
hellen Feed verschwimmt die Karte mit dem Hintergrund. Ein Punkt Abzug, unabhängig vom Kontrastwert.

---

## K4 — Zusammenspiel mit der Headline (20)

Entfällt bei Bild-only-Eingabe. Dann wird der Score auf 80 Punkte normiert und das im Bericht
ausgewiesen — nicht hochgerechnet und nicht geschätzt.

**4a Ergänzung statt Doppelung (0–8)**
- 8 = Bild liefert eine Information, die die Headline nicht hat, und umgekehrt
- 5 = Bild illustriert die Headline, ohne zu ergänzen
- 2 = Bild wiederholt die Headline wörtlich (Headline-Text als Bildtext)
- 0 = Bild und Headline widersprechen sich

Die Fläche im Feed ist begrenzt. Wer die Headline im Bild wiederholt, verschenkt die Hälfte der
Karte — und hat die Aussage doppelt, wo zwei Aussagen möglich wären.

**4b Markenverhältnis (0–4)**

Discover zeigt den Publisher-Namen ohnehin als Text unter der Karte. Entscheidend ist deshalb
nicht, ob die eigene Marke im Bild steht, sondern ob die Karte redaktionell oder werblich wirkt.

- 4 = liest sich als redaktioneller Beitrag; Fremdmarken nur, soweit inhaltlich nötig
- 3 = Fremdmarke sichtbar, aber dem Bildmotiv untergeordnet
- 2 = Fremdmarken dominieren die Fläche; die Karte wirkt werblich
- 1 = von einer Anzeige nicht unterscheidbar, ohne Kennzeichnung
- 0 = irreführend hinsichtlich des Absenders

Werblich wirkende Karten in einem redaktionellen Feed kosten Klickqualität: Wer eine Einordnung
erwartet und eine Werbefläche bekommt, springt zurück.

**4c Einlösung (0–8)**
- 8 = Die Karte verspricht exakt, was der Artikel liefert
- 5 = Versprechen leicht überzogen
- 2 = Karte verspricht mehr als der Artikel hält
- 0 = irreführend

Die Klickqualität fließt in die Discover-Bewertung zurück. Eine Karte, die überverkauft, schadet
zweimal: beim Rücksprung und in der Fortschreibung.

---

## Bänder und Deckel

| Score | Band | Bedeutung |
|-------|------|-----------|
| 85–100 | **Feed-stark** | Karte funktioniert. Nur Feinschliff. |
| 70–84 | **Solide** | Ein klarer Hebel offen, meist Beschnitt oder Kontrast. |
| 55–69 | **Mittel** | Karte verliert im Wettbewerb mit Nachbarkarten. |
| 40–54 | **Schwach** | Bild trägt die Karte nicht. Neues Motiv oder neuer Ausschnitt. |
| < 40 | **Nicht feed-tauglich** | Technisch oder inhaltlich unbrauchbar. |

Deckel:

- Breite < 1200 px → Gesamtscore maximal **55**. Ohne große Karte ist alles andere zweitrangig.
- `max-image-preview:large` fehlt nachweislich → maximal **60**, aus demselben Grund.
- K2 2a ≤ 2 Punkte (Kern-Entität nicht erkennbar) → maximal **50**. Ein Bild, das nicht zeigt,
  worum es geht, kann seine Aufgabe nicht erfüllen.
- Score > 85 nur, wenn jede Dimension mindestens 80 % ihres Maximums erreicht.
- Nicht messbare Unterkriterien (Screenshot-Eingabe, fehlendes Pillow) werden neutral bewertet
  und im Bericht als geschätzt markiert. Ein Score mit mehr als zwei geschätzten Unterkriterien
  wird als Bereich angegeben, nicht als Zahl.

## Score-Delta

Nach den Maßnahmen den erreichbaren Score angeben, mit Zuordnung: welche Maßnahme hebt welches
Unterkriterium um wie viele Punkte. Bildaufträge sind teuer — ein neues Motiv kostet mehr als ein
neuer Ausschnitt. Deshalb bei jeder Maßnahme unterscheiden zwischen **Ausschnitt ändern**
(Minuten, aus dem vorhandenen Bild), **Bild ersetzen** (Stunden oder Kosten) und
**Bild neu produzieren** (Auftrag).
