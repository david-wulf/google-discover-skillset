# Domain-Profile

Das Domain-Profil steuert drei Dinge: welche Entitätstypen im Erwartungsraum (Modul 1.3)
stehen, welche Vertrauenssignale in D5 zählen, und wie streng Aktualität gewichtet wird.
Das Profil wird im Bericht genannt, damit der Kunde die Bewertungsgrundlage kennt.

Bei Mischthemen: Hauptprofil wählen, Zusatzkriterien des Nebenprofils ergänzen und das
im Bericht vermerken.

---

## Technologie

**Erwartete Entitäten:** Hersteller · Produkt- und Modellbezeichnung (exakt, inkl. Generation) ·
Vorgänger- und Konkurrenzmodell · Kernkomponenten · Preis und Verfügbarkeitsdatum ·
Software-/Plattform-Voraussetzung · Benchmark oder Messmethode

**Vertrauen:** Eigene Messung schlägt Herstellerangabe. Wer Herstellerzahlen ungeprüft
übernimmt, verliert bei 5b. Benchmark-Namen (Geekbench, Cinebench) sind Entitäten, nicht Deko.

**Aktualität:** Hoch. Ohne Datums- oder Generationsbezug ist der Text für Discover schwer
einzuordnen.

**Typischer Fehler:** Spezifikationen ohne Alltagsübersetzung. „45 % mehr GPU-Leistung" ohne
„das heißt: Export in 2:11 statt 3:40" kostet Punkte bei 3a und K1.

---

## Gesundheit

**Erwartete Entitäten:** Krankheit/Zustand mit Fachbegriff **und** Alltagsbezeichnung ·
Wirkstoff oder Verfahren · Fachgesellschaft, Leitlinie oder Studie · Facharztgruppe ·
Risikogruppe · Nebenwirkung/Kontraindikation

**Vertrauen:** Höchste Anforderung. Ohne benannte medizinische Quelle (Leitlinie, Fachgesellschaft,
peer-reviewte Studie mit Jahr) ist 5b auf 1 Punkt begrenzt. Ein Arzt-Zitat mit Namen und
Fachrichtung ist hier doppelt wert.

**Aktualität:** Mittel — aber Leitlinienstand muss benannt sein.

**Typischer Fehler:** Handlungsempfehlung ohne Einschränkung und ohne Arztverweis. Fehlende
Risiko-/Nebenwirkungsperspektive ist in Modul 5.3 fast immer ein Konzept mit Relevanz ≥ 8.

---

## Finanzen

**Erwartete Entitäten:** Produkt- oder Anlageklasse · Anbieter/Institut · Regulierungsrahmen ·
Kosten und Gebühren mit Zahl · Zeithorizont · Steuerbehandlung · Risikoklasse

**Vertrauen:** Zahlen brauchen Stichtag. „4,2 % Zinsen" ohne Datum ist wertlos und kostet bei
5c (Widersprüche/Aktualität). Anbietervergleich ohne Gebührenangabe ist unvollständig.

**Aktualität:** Hoch, mit Stichtagspflicht.

**Typischer Fehler:** Ertragschance ohne Risiko und ohne Kosten. Beides ist in 5.3
regelmäßig Relevanz 9.

---

## Bildung

**Erwartete Entitäten:** Bildungsgang/Abschluss · Institution · Zulassungsvoraussetzung ·
Dauer und Kosten · Fördermöglichkeit · Bundesland oder Rechtsraum (bei DE zwingend) ·
Berufsperspektive

**Vertrauen:** Amtliche Quellen (Ministerium, Kammer, Hochschule) sind hier die stärksten
Signale. Erfahrungsberichte ergänzen, ersetzen sie nicht.

**Aktualität:** Mittel, aber Bewerbungsfristen und Studienjahr müssen stimmen.

**Typischer Fehler:** Bundesland-Unterschiede ignorieren. Fehlender Rechtsraum ist ein
Konzept mit Relevanz ≥ 8.

---

## E-Commerce

**Erwartete Entitäten:** Produkt mit exakter Bezeichnung · Marke · Preis mit Stand ·
mindestens zwei Alternativen · Zielgruppe/Anwendungsfall · Kaufkriterien · Händler/Verfügbarkeit ·
Garantie oder Rückgabe

**Vertrauen:** Eigener Test oder klar gekennzeichnete Sekundärrecherche. Affiliate-Kontext
verlangt Transparenz — fehlende Kennzeichnung ist ein Trust-Risiko, auch wenn sie den Score
nicht direkt senkt.

**Aktualität:** Hoch bei Preisen, mittel bei Kaufkriterien.

**Typischer Fehler:** Nur Vorteile. Ohne genannte Nachteile oder Ausschlusskriterium fehlt
das Konzept „für wen es nicht passt" — Relevanz meist 8.

---

## News

**Erwartete Entitäten:** Handelnde Personen mit Funktion · Organisationen · Ort · Zeitpunkt ·
Anlass · betroffene Gruppen · Vorgeschichte

**Vertrauen:** Quellenattribution pro Kernaussage. Wer, wann, wo gesagt. Konjunktiv bei
Unbestätigtem.

**Aktualität:** Sehr hoch. Ohne Datum und Ortsangabe im Text kein voller 5c-Punkt.

**Typischer Fehler:** Ereignis ohne Einordnung. Das Konzept „warum das jetzt passiert /
was folgt" ist bei News fast immer Relevanz 9.

---

## Flash News

Wie News, aber auf Geschwindigkeit und Feed-Eignung optimiert.

**Zusätzliche Erwartung:** Die Kernaussage steht im ersten Satz — `lead.answer_first_hint`
muss `true` sein, sonst 2b = 0. Kein Aufwärmabsatz.

**Länge:** 150–400 Wörter sind hier kein Mangel. Die Struktur-Deckel für
Zwischenüberschriften (4a) werden bei unter 300 Wörtern auf „vorhanden = volle Punkte"
gelockert; das im Bericht vermerken.

**Aktualität:** Maximal. Zeitstempel im Text ist Pflicht.

**Typischer Fehler:** Nachrichtenkern erst in Absatz 3. Bei Flash News ist das der
teuerste einzelne Fehler.

---

## Allgemein

Wenn kein Profil trägt. Erwartungsraum aus Suchintention und Textsorte ableiten und die
Ableitung im Bericht offenlegen. Vertrauenssignale nach Standard: benannte Quelle,
Erstautorschaft, prüfbare Zahl. Aktualität mittel.

Regel: „Allgemein" nur wählen, wenn wirklich kein Profil passt. Ein falsch spezifisches
Profil ist besser als gar keins, weil der Erwartungsraum sonst beliebig wird.
