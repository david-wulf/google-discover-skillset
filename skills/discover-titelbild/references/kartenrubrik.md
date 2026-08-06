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
Begründung beide. Was nicht zulässig ist: einen Zwischenwert wählen, um eine unangenehme
Einordnung zu vermeiden.

## Evidenzstufen — im Bericht mitführen

Die Kriterien haben unterschiedliche Verbindlichkeit. Diese Trennung gehört in den Kundenbericht,
weil sie darüber entscheidet, was verhandelbar ist:

| Marke | Bedeutung |
|-------|-----------|
| **[Doku]** | Google-Discover-Dokumentation. Harte Spezifikation, nicht verhandelbar. |
| **[SDK]** | Aus dem Reverse Engineering des Google-App-SDK. Starkes Indiz, keine bestätigte Spezifikation — Client-Sicht zu einem Zeitpunkt. Nicht als Google-Vorgabe zitieren. |
| **[Richtlinie]** | Discover-Inhaltsrichtlinien. Verstöße erscheinen als manuelle Maßnahme in der GSC. |
| **[Praxis]** | Bewährte Heuristik ohne Google-Beleg. Begründungspflicht beim Kunden, kein „Google verlangt". |

---

## K1 — Technische Auslieferbarkeit (25)

**1a Breite (0–7)** — aus `dimensions.width` · **[Doku]** ≥ 1200 px

| Breite | Punkte |
|--------|-------:|
| ≥ 1600 px | 7 |
| 1200–1599 px | 5 |
| 1000–1199 px | 2 |
| < 1000 px | 0 |

Nur 5 von 7 bei erfüllter Spezifikation ist Absicht: das SDK kennt einen ausdrücklichen
Negativmarker `LOW_QUALITY_IMAGE` **[SDK]**. Es gibt also nicht nur „gut genug", sondern eine
benannte Abwertung — bei Grenzfällen deutlich über die Mindestmaße gehen statt knapp darüber.
Googles eigenes Beispielbild ist 1280 × 720, also selbst ein Grenzfall.

**1b Gesamtfläche (0–3)** — aus `dimensions.total_pixels` · **[Doku]** > 300.000 px
- 3 = über 300.000 px
- 0 = darunter

Eigenständiges Kriterium, nicht durch die Breite abgedeckt: ein 1200 × 200 px Banner erfüllt die
Breite und fällt trotzdem durch.

**1c Seitenverhältnis und Detailerhalt (0–5)** — **[Doku]** 16:9, und: *beim Zuschnitt müssen die
wichtigen Details im beschnittenen Ausschnitt erhalten bleiben*

| Zustand | Punkte |
|---------|-------:|
| 16:9, Abweichung ≤ 3 % | 5 |
| Abweichung ≤ 10 %, tragende Elemente überstehen den Beschnitt | 3 |
| Beschnitt kostet tragende Elemente (an `ansicht_crop_16zu9.png` geprüft) | 1 |
| Hochformat (Verhältnis < 1,0) | 0 |

Der Detailerhalt ist damit **Spezifikationskonformität, nicht Feinschliff** — der einzige Weg ihn
zu prüfen ist der Blick auf die beschnittene Ansicht.

**1d Format (0–3)** — **[Praxis]**
- 3 = WebP oder AVIF
- 2 = JPEG
- 0 = PNG oder untypisches Material

Google äußert sich zum Dateiformat nicht, rät aber von **textlastigen** Bildern ab. Gemeint sind
vollgeschriebene Grafiken, nicht ein kurzer Schriftzug — der ist ausdrücklich Teil der
Thumbnail-Formel in K2.

**1e `max-image-preview:large` (0–4)** — **[Doku]**, der einzige harte technische Blocker
- 4 = im robots-Meta gesetzt (oder AMP)
- 0 = fehlt
- 2 = nicht prüfbar (Bild-only- oder Screenshot-Eingabe) — im Bericht als geschätzt markieren

Fehlt es, erscheint nur ein Mini-Thumbnail und die gesamte Titelbildarbeit läuft ins Leere. Beim
Lesen aus rohem HTML **beide Anführungszeichen-Varianten** prüfen und zusätzlich den HTTP-Header
`X-Robots-Tag`, der das Meta-Tag überstimmt.

**1f Auslieferung (0–3)** — aus `delivery` · **[SDK]**

Drei der fünf im SDK nachweisbaren Bild-Signale betreffen nicht das Motiv, sondern die Zustellung:
Bildmaße, Download-Erfolg (`EMBER_FEED_THUMBNAILS_DOWNLOADED`) und Fehlerrate
(`image_load_failure_count`). Volle 3 Punkte, je Mangel einen Punkt Abzug:

- HTTPS (`og:image:secure_url` wird gegenüber HTTP bevorzugt)
- `Content-Type` beginnt mit `image/`
- keine Weiterleitung — in `og:image` die Ziel-URL direkt angeben
- Download unter 400 ms, anonym abrufbar (kein Login, kein Hotlink-Schutz)

Zusätzlich prüfen, ohne Punktwirkung: sind `og:image:width` und `og:image:height` gesetzt? Sie
verhindern Fehl-Skalierung und falschen Zuschnitt. Und: nennen `og:image`, `WebPage` →
`primaryImageOfPage` und `mainEntityOfPage` → `image` **dasselbe Motiv**? Widersprüchliche Quellen
sind schlimmer als eine fehlende, weil Google dann wählt — und **Schema.org JSON-LD hat Vorrang
vor allen OG-Tags** **[SDK]**. Abweichungen im Bericht benennen.

---

## K2 — Bildaussage (30)

Struktur folgt der Thumbnail-Formel **Gesicht + 3–5 Wörter + Beweis-Element** **[Praxis]**. Die
drei Komponenten wirken nur zusammen: das Gesicht erzeugt Blickkontakt, der Schriftzug liefert den
Grund weiterzulesen, das Beweis-Element macht das Versprechen glaubhaft. Bewertung rein visuell an
`ansicht_feedkarte_340x190.png`; jedes Urteil nennt, was zu sehen ist.

**2a Kern-Entität (0–8)**
- 8 = Entität auf den ersten Blick identifizierbar, dominant, und **kreativ gezeigt** statt als
  erwartbares Katalogfoto — Wiedererkennung plus Überraschung
- 6 = klar erkennbar, aber erwartbare Abbildung
- 4 = nur mit Vorwissen oder erst nach genauem Hinsehen erkennbar
- 2 = thematisch verwandt, aber eine andere Sache als der Artikelgegenstand
- 0 = nicht erkennbar, oder Websitelogo bzw. generisches Motiv (**[Doku]** nennt das Websitelogo
  ausdrücklich als untauglich)

**2b Gesicht (0–8)** — je Teilkriterium
- Die **eigene** Person, Autor oder Experte, nicht ein Model (0–3). Stock-Menschen erfüllen die
  Aufmerksamkeitsfunktion, aber nicht die Absender-Funktion — und die ist der Grund, warum es
  wirkt: das Bild zahlt gleichzeitig auf E-E-A-T und die Transparenz-Anforderung ein **[Richtlinie]**
- Blick in die Kamera **oder** auf das gezeigte Objekt, nie ins Leere (0–2)
- Ausdruck ist Haltung, nicht Grimasse — ernst-alarmiert, erklärend-zugewandt oder
  selbstbewusst-präsentierend, passend zur Aussage. Übertriebene Mimik ist die Clickbait-Variante
  des Bildes (0–2)
- Gesicht groß genug, dass die Augen in der Kartenansicht erkennbar bleiben (0–1)

Schließt das Thema Menschen inhaltlich aus, wird 2b mit 4 Punkten neutral bewertet und das
begründet. Der Regelfall ist das nicht: Discover bewegt sich Richtung Creator- und Absenderlogik,
ein Artikel ohne erkennbaren Menschen verschenkt genau das Signal, das die Plattform aufwertet.

**2c Schriftzug (0–7)**
- **3–5 Wörter** (0–3): 3 = drei bis fünf · 2 = sechs bis sieben · 1 = acht bis zehn · 0 = mehr
  oder kein Schriftzug. Die Obergrenze ist Erfassbarkeit im Scroll, keine Stilfrage — bei mehr
  Wörtern wird überflogen, und überfliegen heißt weiterscrollen
- **Behauptung oder Frage statt Beschreibung** (0–2): „Die Uhr tickt!", „DATEV per Chat
  bebuchen?", „Mein KI-Team" sind ein Gedanke. Eine Zusammenfassung ist 0
- **Ein Wort hervorgehoben** (0–2): Farbfläche hinter dem Schlüsselwort, Unterstreichung oder
  Farbwechsel. Der Akzent führt das Auge und macht aus der Zeile eine Aussage mit Betonung

**2d Beweis-Element (0–4)**
- 4 = sichtbarer Beleg für die Behauptung des Schriftzugs: Screenshot, UI-Ausschnitt, Produkt,
  Logos der beteiligten Tools, eine Zahl als Badge („5 Agenten")
- 2 = sprechende Geste als Ersatz bei abstraktem Thema (offene Hand, Zeigen)
- 0 = keins, oder reine Dekoration ohne Belegfunktion

**2e Herkunft des Motivs (0–3)**
- 3 = eigenes oder erkennbar spezifisches Material; bei regionalem Thema die Zielregion erkennbar
  (der Feed ist auch regional personalisiert)
- 1 = passend, aber austauschbar
- 0 = generisches Stockmaterial. Prüffrage ist nicht „erfüllt es die Specs", sondern „würde **die**
  Zielgruppe dafür den Scroll stoppen"

---

## K3 — Tauglichkeit bei Kartengröße (25)

**3a Bildaussage bei 340 × 190 (0–8)**
- 8 = Aussage trägt vollständig, nichts Tragendes verloren
- 6 = Aussage trägt, Nebendetails verloren
- 3 = Aussage nur noch angedeutet
- 0 = nicht mehr lesbar oder verwechselbar

`detail.loss_pct_of_range` ist hier **Prüfauslöser, nicht Urteil**: Der Wert unterscheidet nicht
zwischen verschwindender Schrift und verschwindender Textur. Über 6 % gezielt prüfen, ob die
Bildaussage betroffen ist. Nur Textur betroffen (Materialstruktur, Blattwerk, Himmel) → kein Abzug.

**3b Schriftlesbarkeit bei 340 × 190 (0–6)**
- 6 = kein Schriftzug, oder alle Schrift bleibt lesbar
- 4 = die tragende Aussage bleibt lesbar, Beiwerk nicht
- 2 = nur Fragmente lesbar
- 0 = Schrift wird zu Grafikrauschen

Immer wörtlich zitieren, was noch entzifferbar ist. Fragmente sind schlimmer als keine Schrift.
Voraussetzung für die oberen Stufen ist fette Sans mit hohem Kontrast auf dunklem oder
abgedunkeltem Grund — der Feed wird auf dem Smartphone im Daumenkino gelesen.

**3c Zweiteilung Gesicht und Text (0–4)** — **[Praxis]**
- 4 = klare Zweiteilung, etwa halbe Fläche Gesicht, halbe Text; beide unbeeinträchtigt
- 2 = Aufteilung erkennbar, aber Text überlappt das Gesicht oder drängt es an den Rand
- 0 = Text liegt über dem Gesicht, oder es gibt keine erkennbare Bildordnung

Bewährte Muster zum Abgleich: Gesicht rechts, Text links, ein Wort farbig hinterlegt · Gesicht
links, UI-Screenshot rechts, Zahlen-Badge.

**3d Kompaktansicht 80 × 80 (0–4)**
- 4 = Motiv bleibt im quadratischen Beschnitt intakt und verständlich
- 2 = Motiv erkennbar, Marke oder Logo fällt weg
- 1 = Beschnitt zerstört die Aussage, Schriftfragmente bleiben stehen
- 0 = im Quadrat nicht mehr deutbar

Randständige Logos und Markennamen sind hier der Regelfall des Scheiterns. Konsequenz für die
Produktion: alles Tragende in das mittlere Quadrat legen.

**3e Kontrast und Auffälligkeit (0–3)** — aus `luminance.rms_contrast` und `colorfulness`
- 3 = RMS-Kontrast ≥ 60 **und** Farbigkeit ≥ 40
- 2 = eines von beiden erfüllt
- 1 = RMS-Kontrast 40–59
- 0 = Kontrast < 40 und Farbigkeit < 20

Zusätzlich: `clipped_white_pct` über 15 % bedeutet ausgebrannte Flächen — in einem hellen Feed
verschwimmt die Karte mit dem Hintergrund. Ein Punkt Abzug, unabhängig vom Kontrastwert.

---

## K4 — Zusammenspiel mit der Headline (20)

Entfällt bei Bild-only-Eingabe. Dann wird der Score auf 80 Punkte normiert und das ausgewiesen —
nicht hochgerechnet und nicht geschätzt.

Zur Erinnerung, was hier bewertet wird: Der Discover-Titel ist der **`og:title`** und darf sich von
Meta-Title und H1 unterscheiden — drei Titel, drei Aufgaben. Verglichen wird der Bildschriftzug
gegen den `og:title`, nicht gegen die H1.

**4a Schriftzug ergänzt den `og:title` (0–8)** — **[Praxis]**
- 8 = Schriftzug liefert einen **zweiten Haken**: eine andere Ebene als der Titel (Emotion,
  Dringlichkeit, Zahl, Perspektive), nicht dasselbe in anderen Worten
- 5 = illustriert den Titel, ohne zu ergänzen
- 2 = wiederholt die Kernbegriffe des Titels
- 0 = Schriftzug und Titel widersprechen sich

Die Karte hat zwei Flächen. Doppeln beide, verschenkt sie eine davon. Das ist der häufigste
Einzelfehler bei ansonsten gut gemachten Karten — insbesondere bei aus YouTube übernommenen
Thumbnails, wo der Titel klein und grau unter dem Bild steht und das Bild den Hook allein tragen
muss. In Discover steht die Headline prominent daneben.

**4b Werbeanteil und Kennzeichnung (0–4)** — **[Richtlinie]**

Die Richtlinien verlangen, dass Werbung und Werbemittel den Anteil der Nachrichteninhalte nicht
überschreiten, und dass gesponserte Inhalte deutlich gekennzeichnet werden.

- 4 = liest sich als redaktioneller Beitrag; Fremdmarken nur, soweit inhaltlich nötig
- 3 = Fremdmarke sichtbar, dem Bildmotiv untergeordnet
- 2 = Fremdmarken dominieren die Fläche; die Karte wirkt werblich
- 1 = von einer Anzeige nicht unterscheidbar, ohne Kennzeichnung
- 0 = irreführend hinsichtlich des Absenders, oder getarntes Sponsoring

Discover zeigt den Publisher-Namen ohnehin als Text unter der Karte (`og:site_name`) — es geht
also nicht darum, ob die eigene Marke im Bild steht, sondern ob die Karte redaktionell wirkt.

**4c Einlösung (0–8)** — **[Richtlinie]** + **[SDK]**
- 8 = Die Karte verspricht exakt, was der Artikel liefert
- 5 = Versprechen leicht überzogen
- 2 = Karte verspricht mehr als der Artikel hält
- 0 = irreführend

Zwei unabhängige Gründe, warum das kein Stilkriterium ist: Die Richtlinien untersagen
Vorschauinhalte, die zur Interaktion verleiten, indem **Details vorgetäuscht** werden — und die
Regel greift ausdrücklich am Vorschauelement, also an `og:title` und `og:image`, nicht am
Artikeltext. Und die Klickqualität wird nach dem Navboost-Modell bewertet: ein Titel, der klickt,
aber nicht einlöst, verliert dort. Clickbait ist rechnerisch schlecht, nicht moralisch.

Erschwerend: die historische CTR wird **pro URL** geführt (`click_count`/`show_count`) **[SDK]**.
Eine URL trägt ihre Feed-Reputation in künftige Ausspielungen mit. Ein schwacher Start belastet
diese URL dauerhaft — Titel- und Bildwechsel auf einer verbrannten URL wirken begrenzt. Bei
grundlegend neuem Aufhänger ist eine neue URL die ehrlichere Option. Gehört in die Empfehlung,
wenn 4c bei 2 oder darunter liegt.

---

## Bänder und Deckel

| Score | Band | Bedeutung |
|-------|------|-----------|
| 85–100 | **Feed-stark** | Karte funktioniert. Nur Feinschliff. |
| 70–84 | **Solide** | Ein klarer Hebel offen, meist Beschnitt, Doppelung oder Kontrast. |
| 55–69 | **Mittel** | Karte verliert im Wettbewerb mit Nachbarkarten. |
| 40–54 | **Schwach** | Bild trägt die Karte nicht. Neues Motiv oder neuer Ausschnitt. |
| < 40 | **Nicht feed-tauglich** | Technisch oder inhaltlich unbrauchbar. |

Deckel:

- **Google-Spezifikation nicht erfüllt** (`google_spec.all_met` = false: Breite, Fläche oder 16:9)
  → maximal **55**. Das ist die Untergrenze der Zulässigkeit, kein Feinschliff.
- **Bild nicht anonym abrufbar oder `Content-Type` nicht `image/*`** → maximal **40**. Ohne
  erfolgreichen Thumbnail-Download entsteht laut SDK **keine Karte** — kein Textfallback.
- **`max-image-preview:large` fehlt nachweislich** → maximal **60**.
- **K2 2a ≤ 2** (Kern-Entität nicht erkennbar) → maximal **50**.
- Score > 85 nur, wenn jede Dimension mindestens 80 % ihres Maximums erreicht.
- Nicht messbare Unterkriterien neutral bewerten und als geschätzt markieren. Bei mehr als zwei
  geschätzten Unterkriterien den Score als Bereich angeben, nicht als Zahl.

## Score-Delta

Nach den Maßnahmen den erreichbaren Score angeben, mit Zuordnung: welche Maßnahme hebt welches
Unterkriterium um wie viele Punkte. Dabei nach Kosten unterscheiden — **Ausschnitt ändern**
(Minuten, aus dem vorhandenen Bild) · **Schriftzug oder Badge ergänzen** (Grafik, unter einer
Stunde) · **Bild ersetzen** (Stunden oder Lizenzkosten) · **Bild neu produzieren** (Shooting).
