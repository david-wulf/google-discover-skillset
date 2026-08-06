---
name: discover-ctr-optimierung
description: >
  Optimiert die Discover-CTR einer Karte aus Headline und Titelbild gemeinsam — ausgehend von
  gemessenen Daten statt von einer Rubrik. Holt sich, wenn Search Console per MCP angebunden ist,
  den tatsächlichen CTR-Verlauf pro URL, prüft statistisch ob die Lücke zum Benchmark echt ist,
  bestimmt den Engpass (Headline oder Bild), und baut einen Messplan mit belastbarem Zeitfenster.
  Verwende diesen Skill, wenn es um die Klickrate im Discover-Feed geht — auch bei:
  "CTR verbessern", "Discover-CTR optimieren", "warum klickt niemand", "CTR zu niedrig",
  "Klickrate steigern", "Headline und Bild zusammen optimieren", "CTR-Verlauf", "CTR-Analyse
  Discover", "Karte optimieren", "hat die Änderung was gebracht", "Titeländerung messen",
  "A/B-Test Discover", "welche Karte performt besser".
  Auch auslösen, wenn Klick- und Impressionszahlen zur Bewertung eingereicht werden oder gefragt
  wird, ob eine CTR-Veränderung signifikant ist.
  Für die reine Titelbewertung ohne Messdaten ist discover-headline zuständig, für das Bild allein
  discover-titelbild.
---

# Discover CTR-Optimierung

Die anderen Skills bewerten **prognostisch**: sie sagen anhand einer Rubrik, wie gut Titel oder
Bild sein dürften. Dieser Skill geht den umgekehrten Weg — er startet bei der **gemessenen** CTR
und arbeitet zurück auf die Ursache.

Damit kommt eine Frage ins Spiel, die in CTR-Diskussionen fast immer übersprungen wird: **Ist die
beobachtete Differenz überhaupt echt?** Eine CTR von 6,2 % auf 6,8 % bei 800 Impressionen ist
nicht von Zufall unterscheidbar. Wer daraus eine Maßnahme ableitet, optimiert auf Rauschen.

## Grundregeln

1. **Erst Volumen prüfen, dann interpretieren.** Vor jeder Aussage über CTR-Unterschiede wird das
   Konfidenzintervall gerechnet. Kein Befund auf Zehntel-Prozentpunkte, die das Intervall nicht
   trägt.
2. **Signifikanz ist keine Kausalität.** Discover erlaubt keinen echten A/B-Test. Zwei Zeiträume
   sind nicht randomisiert — Freshness-Verfall, andere Kohorten, Saisonalität und Wettbewerb wirken
   mit. Ein belegter Unterschied zeigt eine Veränderung, nicht deren Ursache. Das steht in jedem
   Bericht.
3. **Eine Variable pro Messung.** Wer Titel und Bild gleichzeitig tauscht, weiß hinterher nichts.
4. **Kein Ergebnis ist auch ein Ergebnis.** „Bei diesem Volumen nicht nachweisbar" ist eine
   verwertbare Aussage — sie verhindert Folgeaufwand auf falscher Grundlage.
5. **Die CTR-Historie hängt an der URL.** Vor jeder Optimierungsempfehlung wird geprüft, ob die
   URL überhaupt noch zu retten ist.

## Ablauf

### Schritt 0 — Eingabe klären

| Was | Wozu |
|-----|------|
| **URL(s)** | für die GSC-Abfrage. Am aussagekräftigsten: eine Top-URL und eine schwache zum Vergleich |
| **Headline** (`og:title`) und **Titelbild** | die zwei Bestandteile der Karte. Bei URL-Eingabe aus dem HTML holen |
| **Domain-Typ** | `news` oder `non-news` — bestimmt den Referenzwert (rund 11 % gegen rund 6 %) |
| **Gab es eine Änderung, und wann?** | entscheidet, ob ein Vorher-Nachher-Vergleich möglich ist |

Ohne GSC-Anbindung läuft der Skill weiter, aber ohne Messdaten: dann werden Headline und Bild
prognostisch bewertet und der Bericht sagt ausdrücklich, dass die Diagnose auf Rubrikwerten statt
auf gemessener CTR beruht.

### Schritt 1 — Messdaten holen

Wenn ein GSC-MCP verfügbar ist, in dieser Reihenfolge:

1. **Ist die Domain als Property vorhanden?** Erst prüfen, dann abfragen. Wenn nicht: kein
   GSC-Teil, und das im Bericht benennen statt zu schätzen.
2. **CTR pro Seite**, Suchtyp `discover`, Dimension `page`, letzte 28 Tage. Liefert Klicks,
   Impressionen und CTR je URL.
3. **Tagesverlauf** für die betroffene URL, Dimension `date`. Damit ist der Verlauf sichtbar —
   und ein Änderungszeitpunkt lässt sich als Schnitt setzen.
4. **Vorperiode und Vorjahreszeitraum** für dieselbe URL, wenn vorhanden. Discover ist saisonal;
   ein Vormonatsvergleich allein kann täuschen.

Manche GSC-MCPs bringen fertige Auswertungen mit (`discover_analysis`, `ctr_opportunities`,
`ctr_vs_benchmark`, `search_appearance`). Wenn vorhanden, nutzen — aber die Rohwerte Klicks und
Impressionen trotzdem mitnehmen, weil Schritt 2 sie braucht.

**Zwei Dinge zur Auslegung**, die in den Bericht gehören: Der GSC-Discover-Bericht enthält **auch
Chrome-Zugriffe** und erscheint erst ab einer nicht bezifferten Mindest-Impressionszahl. Und die
Discover-CTR ist **nicht** mit der Search-CTR vergleichbar — Discover zählt eine Impression erst,
wenn die Karte sichtbar wird.

### Schritt 2 — Der statistische Realitätscheck

Das ist der Schritt, der diesen Skill von einer Meinung unterscheidet.

```bash
# Wie genau ist diese CTR?
python scripts/ctrstats.py ci --clicks 412 --impressions 8300

# Wo stehen wir gegen den Referenzwert — und ist der Abstand belegt?
python scripts/ctrstats.py benchmark --clicks 412 --impressions 8300 --typ non-news

# Was ist bei diesem Volumen überhaupt nachweisbar?
python scripts/ctrstats.py mde --impressions 8300 --baseline-ctr 0.05
```

Und wenn eine Änderung vorliegt:

```bash
python scripts/ctrstats.py compare --before 412/8300 --after 388/6900
```

Was die Werte bedeuten:

| Ausgabe | Bedeutung für den Bericht |
|---------|---------------------------|
| `ci95_pct` | Die CTR ist ein Intervall, kein Punkt. Bei 12 Klicks auf 190 Impressionen liegt sie zwischen 3,7 % und 10,7 % — daraus lässt sich nichts ableiten |
| `belastbar` | `false` heißt: keine Maßnahme auf Zehntel-Prozentpunkte stützen |
| `abstand_belegt` | Ob der Abstand zum Referenzwert bei diesem Volumen überhaupt nachweisbar ist |
| `mde_relativ_pct` | Der kleinste Effekt, den man hier je messen könnte. Bei 8.300 Impressionen sind das rund 18 % relativ — alles darunter bleibt unsichtbar |
| `p_wert` / `signifikant_alpha_5pct` | Ob die beobachtete Veränderung belegbar ist |

**Der ernüchternde Normalfall:** Selbst bei 16.000 Impressionen ist eine Verbesserung von 6,25 %
auf 6,75 % noch nicht signifikant (p ≈ 0,07). Wer bei 800 Impressionen über Zehntel diskutiert,
diskutiert über nichts. Das offen zu sagen ist Teil der Leistung.

### Schritt 3 — Den Engpass bestimmen

Erst wenn Schritt 2 zeigt, dass es überhaupt eine belegbare Lücke gibt, wird nach der Ursache
gesucht. Die Karte hat zwei Flächen, und beide werden von den zuständigen Skills geprüft:

| Symptom | Vermuteter Engpass | Skill |
|---------|-------------------|-------|
| Viele Impressionen, CTR unter 5 %, Titel ohne Fakt oder Zahl | **Headline** | `discover-headline` |
| Titel stark bewertet, CTR trotzdem niedrig | **Bild** | `discover-titelbild` |
| Titel und Bild sagen dasselbe | **Doppelung** — eine Fläche verschenkt | `discover-titelbild`, Dimension K4 |
| Gute CTR, aber schneller Rücksprung danach | **Einlösung**, nicht CTR | `discover-content-optimizer` |
| Kaum Impressionen | **nicht CTR** — Eligibility | `discover-readiness-domain` |

Die letzte Zeile ist die häufigste Fehldiagnose: Wer bei 200 Impressionen die CTR optimiert,
arbeitet an der falschen Station. Dann wird hier abgebrochen und dorthin verwiesen.

**Reihenfolge einhalten:** `discover-headline` liefert den empfohlenen Titel; `discover-titelbild`
braucht ihn, um die Doppelung gegen den **neuen** Titel zu prüfen.

### Schritt 4 — Messplan bauen

Das ist der Teil, den die reinen Bewertungsskills nicht leisten können.

```bash
python scripts/ctrstats.py power --baseline-ctr 0.062 --uplift-rel 0.15 --impressions-per-day 1200
```

Daraus fällt in der Praxis fast immer derselbe Konflikt: Um +15 % relativ nachzuweisen, braucht man
bei 1.200 Impressionen pro Tag rund **10 Tage pro Variante**. Das Freshness-Fenster mit hoher
Gewichtung ist aber **7 Tage**. Sequenzielles Messen an einem einzelnen Artikel ist damit
strukturell nicht saubermachbar — der Freshness-Verfall überlagert den Effekt.

**Der Ausweg ist ein Portfolio-Test statt eines Artikel-Tests:**

- Die Änderung auf **eine Gruppe vergleichbarer Artikel** anwenden (gleiches Verzeichnis, ähnliche
  Themen, ähnliches Impressionsvolumen) und eine zweite Gruppe unverändert lassen.
- Beide Gruppen im **gleichen Zeitfenster** messen. Damit wirkt der Freshness-Verfall auf beide
  gleich und fällt aus dem Vergleich heraus.
- Impressionen über die Gruppe summieren. Das Volumenproblem löst sich über die Anzahl der Artikel
  statt über die Zeit.
- Gruppengröße aus `power` ableiten: benötigte Impressionen pro Variante geteilt durch die
  durchschnittlichen Impressionen pro Artikel.

Wenn der Kunde das nicht leisten kann oder will: das sagen, statt ein sequenzielles Vorher-Nachher
zu verkaufen, das methodisch nichts belegt. Eine Änderung ohne Messmöglichkeit ist trotzdem
zulässig — sie wird dann als **begründete Verbesserung** ausgewiesen, nicht als messbarer Test.

### Schritt 5 — Die URL-Entscheidung

Die historische CTR wird **pro URL** geführt (`click_count`/`show_count`). Eine URL trägt ihre
Feed-Reputation in künftige Ausspielungen mit. Daraus folgt eine Entscheidung, die vor jeder
Textarbeit fällt:

| Befund | Empfehlung |
|--------|-----------|
| URL hatte nie viel Traffic, CTR schwach | Karte optimieren, URL behalten |
| URL hatte guten Start, CTR seit Wochen fallend | Karte optimieren plus Content aktualisieren — Decay, nicht Kartenproblem |
| URL dauerhaft deutlich unter 5 % bei relevanten Impressionen | **Neue URL** mit neuem Aufhänger erwägen. Titel- und Bildwechsel auf einer verbrannten URL wirken begrenzt |
| URL wurde von Nutzern häufig weggewischt | Tombstoning ist permanent — neue URL, nicht Reparatur |

Diese Empfehlung gehört ausdrücklich in den Bericht, weil sie den Aufwand steuert: Eine neue URL
ist teurer als eine neue Headline, aber billiger als drei erfolglose Iterationen.

### Schritt 6 — Bericht

1. **Urteil in drei Sätzen** — wo die CTR steht, ob die Lücke belegt ist, was der Engpass ist
2. **Datenlage** — Klicks, Impressionen, CTR mit Konfidenzintervall, Zeitraum. Plus: was bei
   diesem Volumen überhaupt nachweisbar wäre (MDE)
3. **Einordnung** — gegen Referenzwert und Arbeitsziel, mit dem Hinweis ob der Abstand belegt ist
4. **Verlauf** — Tagesverlauf, Vorperiode, Vorjahr. Bei vorliegender Änderung: der
   Signifikanztest mit p-Wert und der Kausalitäts-Vorbehalt
5. **Engpass-Diagnose** — Headline oder Bild, mit dem Ergebnis des jeweiligen Skills
6. **Maßnahme** — die konkrete neue Headline bzw. der Bildauftrag, ausgeschrieben
7. **Messplan** — Portfolio oder Einzelartikel, Gruppengröße, Zeitfenster, was gemessen wird und
   was nicht belegbar sein wird
8. **URL-Entscheidung** — optimieren oder neu aufsetzen
9. **Methodik und Grenzen** — Pflicht, siehe unten

## Grenzen — gehören in jeden Bericht

- **Discover kennt keinen A/B-Test.** Es gibt keine Variantenauslieferung. Alles, was möglich ist:
  ändern und beobachten, oder Gruppen vergleichen. Beides ist nicht randomisiert.
- **Ein signifikanter Unterschied belegt eine Veränderung, nicht deren Ursache.** Freshness-Verfall,
  Kohortenwechsel, Saisonalität, Wettbewerb und Googles eigene Counterfactual-Experimente wirken
  mit. Ein Teil der beobachteten Volatilität ist Test-Design von Google, kein Qualitätsurteil.
- **Kein Skill prognostiziert CTR.** Die pCTR-Werte aus `discover-headline` sind Rubrikwerte für den
  Variantenvergleich, keine Vorhersage. Der Modell-Mittelpunkt liegt bei 11,3 % und damit über dem
  Arbeitsziel von 7–9 %.
- **Referenzwerte sind Beobachtungen**, keine Google-Vorgaben: News rund 11 %, Non-News rund 6 %,
  Arbeitsziel 7–9 %, unter 5 % Handlungssignal — aus einer GSC-Auswertung über 11.000 URLs von
  62 Domains über 12 Monate.
- **Der GSC-Discover-Bericht enthält auch Chrome-Zugriffe.** Er ist nicht rein Feed-Traffic.
- **Ohne GSC keine Messdiagnose.** Dann arbeitet der Skill prognostisch, und das wird ausgewiesen.

## Abgrenzung

| Frage | Skill |
|-------|-------|
| Ist dieser Titel gut? | `discover-headline` |
| Ist dieses Bild gut? | `discover-titelbild` |
| **Warum ist die gemessene CTR niedrig, und ist die Änderung belegbar?** | **dieser Skill** |
| Bekommt der Artikel überhaupt Impressionen? | `discover-readiness-domain` |
| Hält der Artikel, was die Karte verspricht? | `discover-content-optimizer` |
| Alles zusammen als Kundenbericht | `discover-gesamtaudit` |
