# Discover Content Score — Rubrik

Verbindlich. Punkte werden pro Unterkriterium vergeben, jeweils mit dem gemessenen Wert oder
dem Textzitat als Begründung. Eine Dimension ohne Begründung pro Unterkriterium gilt als nicht
bewertet.

Summe: **100 Punkte** über fünf Dimensionen.

| Dimension | Punkte |
|-----------|--------|
| D1 Entitäten-Abdeckung und -Tiefe | 25 |
| D2 Headline und Einstieg | 20 |
| D3 Semantische Vollständigkeit | 20 |
| D4 Struktur und Lesbarkeit | 15 |
| D5 Vertrauen und Maschinenlesbarkeit | 20 |

---

## D1 — Entitäten-Abdeckung und -Tiefe (25)

**1a Abdeckung der erwarteten Kernentitäten (0–10)**

Anteil der in Modul 1.3 aufgestellten erwarteten Kernentitäten, die im Text vorkommen.

| Anteil | Punkte |
|--------|--------|
| ≥ 90 % | 10 |
| 75–89 % | 8 |
| 60–74 % | 6 |
| 45–59 % | 4 |
| 30–44 % | 2 |
| < 30 % | 0 |

**1b Kontextualisierungstiefe (0–8)**

Anteil der vorhandenen Kernentitäten, die mindestens **zwei** von vier Kontextualisierungen
haben: definiert · verglichen · in Beziehung zu einer anderen Entität gesetzt · intern verlinkt
bzw. mit vertiefender Erklärung versehen.

| Anteil | Punkte |
|--------|--------|
| ≥ 60 % | 8 |
| 45–59 % | 6 |
| 30–44 % | 4 |
| 15–29 % | 2 |
| < 15 % | 0 |

**1c Textuelle Integration (0–7)** — aus `entity_summary.mean_integration`

| Wert | Punkte |
|------|--------|
| ≥ 0,60 | 7 |
| 0,50–0,59 | 5 |
| 0,42–0,49 | 4 |
| 0,33–0,41 | 2 |
| < 0,33 | 0 |

Deckel: Wenn mehr als 40 % der Entitäten im Band `isoliert` liegen, sind für 1c maximal
3 Punkte möglich, unabhängig vom Mittelwert.

---

## D2 — Headline und Einstieg (20)

**2a Headline (0–14)** = Headline-Rubrik-Score (0–10) × 1,4

**2b Einstieg / Lead (0–6)** — je erfülltes Kriterium 1 Punkt, außer wo anders angegeben

| Kriterium | Punkte |
|-----------|--------|
| `lead.answer_first_hint` = true — erster Satz kurz und aussagetragend | 2 |
| Lead enthält eine konkrete Zahl oder einen prüfbaren Fakt | 2 |
| Kernentität steht im ersten Satz | 1 |
| Lead ≤ 40 Wörter | 1 |

---

## Headline-Rubrik (0–10)

Fünf Kriterien, je 0–2 Punkte. Wird identisch auf Original und alle Varianten angewendet.

**K1 Konkretheit (0–2)**
- 2 = enthält eine Zahl, einen Eigennamen oder ein prüfbares Ergebnis („153 GB/s", „1.599 Dollar", „Stiftung Warentest")
- 1 = konkretes Thema, aber keine harte Angabe
- 0 = abstrakt oder Kategoriesprache („Neue Entwicklungen bei Notebooks")

**K2 Neugier-Lücke (0–2)**
- 2 = Leser weiß, worum es geht, aber nicht die Antwort
- 1 = entweder komplett gespoilert oder zu rätselhaft
- 0 = Clickbait ohne Substanz, oder rein deskriptiv ohne jeden Anreiz

**K3 Persönliche Relevanz (0–2)**
- 2 = benennt explizit, wen es betrifft, oder spricht direkt an („für Mieter", „wenn du noch ein M1 nutzt")
- 1 = Relevanz erschließbar, aber nicht benannt
- 0 = reine Sachmeldung ohne Adressat

**K4 Stärkster Fakt (0–2)**

Bestimme zuerst den stärksten Fakt des Textes (überraschendste Zahl, größter Kontrast,
konkretestes Ergebnis). Dann:
- 2 = dieser Fakt steht in der Headline
- 1 = ein schwächerer Fakt aus dem Text steht in der Headline
- 0 = kein Fakt aus dem Text in der Headline

**K5 Feed-Tauglichkeit (0–2)**
- 2 = ≤ 65 Zeichen **und** Kernentität in den ersten 40 Zeichen
- 1 = eines von beiden erfüllt
- 0 = keines von beiden

### Anti-Inflation

Diese Regeln sind der Grund, dass der Score überhaupt aussagekräftig ist:

- **Höchstens eine** Variante pro Analyse darf ≥ 9,0 erreichen. Wenn zwei Varianten so gut
  wirken, ist eine davon zu senken — mit Begründung, welches Kriterium sie schlechter erfüllt.
- Eine Headline ohne Zahl, Eigennamen oder prüfbares Ergebnis kann **nie** über 6,0 kommen
  (K1 = 0 oder 1 begrenzt automatisch).
- Über 65 Zeichen: K5 ≤ 1, und im Bericht wird die gemessene Zeichenzahl genannt.
- Wenn keine Variante das Original um ≥ 1,5 Punkte übertrifft, lautet die Empfehlung
  „Original behalten". Das ist ein Ergebnis, kein Versagen.
- Typische reale Publisher-Headlines liegen bei 4–7. Ein 9er ist die Ausnahme.

---

## D3 — Semantische Vollständigkeit (20)

**3a Fehlende Konzepte, gewichtet (0–12)** — auf Basis von Modul 5.3

| Situation | Punkte |
|-----------|--------|
| Kein fehlendes Konzept mit Relevanz ≥ 7 | 12 |
| Ein Konzept mit Relevanz ≥ 7 fehlt | 9 |
| Zwei | 6 |
| Drei | 3 |
| Vier oder mehr | 0 |

**3b Themenfokus (0–8)**

| Zustand | Punkte |
|---------|--------|
| Ein klares Thema; Core-Terme homogen; Cluster jeweils gebündelt in zusammenhängenden Absätzen | 8 |
| Klares Thema, leichte Streuung eines Clusters | 6 |
| Ein Nebenthema überproportional groß, oder ein Cluster über den Text verstreut | 4 |
| Zwei konkurrierende Themen im selben Text | 2 |
| Kein erkennbarer thematischer Schwerpunkt | 0 |

---

## D4 — Struktur und Lesbarkeit (15)

**4a Zwischenüberschriften (0–4)**

| Zustand | Punkte |
|---------|--------|
| ≥ 1 je 200 Wörter **und** tragen Entitäten oder Fakten | 4 |
| ≥ 1 je 250 Wörter, inhaltlich brauchbar | 3 |
| ≥ 1 je 400 Wörter | 2 |
| Vorhanden, aber generisch („Fazit", „Hintergrund") | 1 |
| Keine | 0 |

**4b Absatz- und Satzlänge (0–4)**
- 2 Punkte: `avg_paragraph_words` ≤ 80 **und** `paragraphs_over_120w` = 0
- 2 Punkte: `avg_sentence_words` ≤ 19 **und** `long_sentence_ratio` ≤ 0,20

**4c Lesbarkeit (0–4)** — aus `readability.score`

| DE (Amstad) / EN (Flesch) | Punkte |
|---------------------------|--------|
| 60–75 | 4 |
| 50–59 oder 76–85 | 3 |
| 45–49 | 2 |
| 30–44 oder > 85 | 1 |
| < 30 | 0 |

**4d Scanbarkeit (0–3)** — je 1 Punkt
- Mindestens eine Liste, Tabelle oder Aufzählung vorhanden
- Mindestens eine Zwischenüberschrift formuliert eine Nutzerfrage
- Kein Absatz ohne eigenen Fakt oder eigene Aussage (reine Übergangsabsätze zählen negativ)

---

## D5 — Vertrauen und Maschinenlesbarkeit (20)

**5a Faktendichte (0–6)** — aus `fact_density.specific_facts_per_100_words`

| Wert | Punkte |
|------|--------|
| ≥ 3,0 | 6 |
| 2,0–2,9 | 5 |
| 1,5–1,9 | 4 |
| 1,0–1,4 | 3 |
| 0,5–0,9 | 1 |
| < 0,5 | 0 |

**5b Quellen und Erfahrung (0–7)**

| Kriterium | Punkte |
|-----------|--------|
| Benannte externe Quellen (Institution, Studie, Unternehmen mit Namen): ≥ 2 → 3 · genau 1 → 2 · nur vage („Studien zeigen") → 1 · keine → 0 | 0–3 |
| Erstautorschaft belegt: eigener Test, eigene Messung, Vor-Ort-Beobachtung | 0–2 |
| Namentlich zugeordnetes Zitat oder Experteneinschätzung | 0–2 |

**5c Maschinenlesbarkeit des Textes (0–7)**

Bewertet, ob der **Text** die Grundlage für saubere strukturierte Daten liefert — nicht das
selbst erzeugte Schema.

| Kriterium | Punkte |
|-----------|--------|
| Kernentität eindeutig disambiguierbar (Vollname, Hersteller, Modellbezeichnung — `sameAs` wäre auflösbar) | 0–2 |
| Aktualitätsbezug im Text (Datum, Zeitangabe, „seit", „ab") | 0–1 |
| Headline und Zwischenüberschriften tragen Entitäten statt Allgemeinplätze | 0–2 |
| Text liefert Belege für ein `author`-Objekt (Erfahrung, Rolle, Perspektive) | 0–1 |
| Keine widersprüchlichen Angaben (Zahlen, Daten, Bezeichnungen konsistent) | 0–1 |

---

## Bänder und Deckel

| Score | Band | Bedeutung |
|-------|------|-----------|
| 85–100 | **Discover-ready** | Kein struktureller Mangel. Nur Feinschliff. |
| 70–84 | **Solide** | Funktionsfähig, aber die Top-3-Maßnahmen heben spürbar. |
| 55–69 | **Mittel** | Deutliche Lücken bei Entitäten oder Vertrauen. Überarbeitung lohnt. |
| 40–54 | **Schwach** | Text erfüllt Discover-Erwartungen nicht. Substanzielle Ergänzung nötig. |
| < 40 | **Nicht Discover-fähig** | Neu ansetzen — der Text trägt das Thema nicht. |

Deckel, die vor Schönfärberei schützen:

- D1 < 12 Punkte → Gesamtscore maximal **65**. Ohne Entitätenabdeckung gibt es keine
  thematische Autorität, egal wie gut der Text geschrieben ist.
- Keine einzige benannte Quelle **und** `specific_facts_per_100_words` < 1,0 → maximal **55**.
- Score > 85 nur, wenn **jede** Dimension mindestens 80 % ihres Maximums erreicht.
- Wenn ein Wert nicht berechnet werden konnte (Python fehlt, Textsorte unklar), wird das
  Unterkriterium mit dem konservativen Mittelwert bewertet und im Bericht als geschätzt markiert.

## Score-Delta ausweisen

Nach den Top-3-Maßnahmen wird der **erreichbare Score** angegeben: aktueller Score plus die
Punkte, die die drei Maßnahmen nach Rubrik freischalten. Pro Maßnahme wird benannt, welches
Unterkriterium sie hebt und um wie viele Punkte. Das macht die Empfehlung überprüfbar und ist
für den Kunden der Unterschied zwischen einer Meinung und einem Plan.
