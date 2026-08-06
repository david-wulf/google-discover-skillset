---
name: content-checker
description: "Prüft fertige SEO-Artikel auf Qualitätsprobleme: KI-Muster, oberflächliche Sätze, fehlende inhaltliche Tiefe, atmosphärisch-poetischen Stil, fehlende Answer-First-Struktur, Überschriften-Qualität und mehr. Verwende diesen Skill immer, wenn ein fertiger Artikel, Blogpost oder Content-Stück zur Qualitätsprüfung eingereicht wird. Auch auslösen bei: 'prüfe diesen Text', 'Content-Check', 'Artikel bewerten', 'QA für Content', 'KI-Check', 'Text checken', 'Qualitätssicherung'. Der Skill geht den Artikel Abschnitt für Abschnitt durch und gibt pro Check eine strukturierte Bewertung mit konkreten Fundstellen und Verbesserungsvorschlägen. Dieser Skill ist kanalunabhängig — er prüft Textqualität, nicht Discover-Tauglichkeit. Für Google Discover sind discover-content-optimizer (Entitäten, Semantik), discover-headline (og:title) und discover-feedkarte (Titelbild) zuständig."
---

# Content Quality Checker

## Zweck

Dieser Skill prüft fertige SEO-Artikel systematisch auf 12 Qualitätskriterien. Er geht den Artikel **sequentiell** durch — jeder Check wird nacheinander auf den gesamten Text angewendet. Das Ergebnis ist ein strukturierter Report mit konkreten Fundstellen, Bewertungen und Verbesserungsvorschlägen.

## Schritt 0 — Ordner-Scan (vor den Checks)

Bevor du mit den eigentlichen Checks startest, prüfe den Arbeitsordner des Nutzers auf vorhandene Kontextdateien. Das ist wichtig, weil dort oft kundenspezifische Briefings, Style Guides oder Guidelines liegen, die die Checks deutlich relevanter machen.

**Vorgehen:**
1. Liste alle Dateien im aktuellen Arbeitsordner (und Unterordnern, max. 2 Ebenen tief).
2. Lies alle Dateien, die nach Briefing, Guideline, Style Guide, Kundeninfo oder ähnlichem aussehen — typische Namen: `briefing.md`, `guidelines.md`, `style-guide.md`, `kunde.md`, `brand-voice.md`, `SKILL.md` (von Kunden-Skills), `.txt`- oder `.md`-Dateien mit relevantem Namen.
3. Extrahiere daraus:
   - **Kundenname / Domain** (falls nicht vom Nutzer angegeben)
   - **Brand Voice / Tonalität** (z.B. Du vs. Sie, formell vs. locker)
   - **Spezifische Do's und Don'ts** für den Content
   - **Keyword-Vorgaben oder Themen-Fokus**
   - **Jede andere kundenspezifische Anforderung**, die für die Qualitätsprüfung relevant ist
4. Wenn du kundenspezifische Regeln findest, die über die Standard-12-Checks hinausgehen, nimm sie als **zusätzliche personalisierte Checks** am Ende der Checkliste auf. Benenne sie klar als "Kunden-Check" und referenziere die Quelle (z.B. "Laut briefing.md: ...").

Falls kein Ordner ausgewählt ist oder keine relevanten Dateien vorhanden sind, überspringe diesen Schritt und arbeite mit den Infos, die der Nutzer direkt mitliefert.

## Anwendung

Der Nutzer schickt einen fertigen Artikel (als Text, HTML oder Datei). Optional kann er angeben:
- **Kunde / Domain** (für Kontext zum Kunden-Einbau und Brand Voice)
- **Keyword** (für Suchintentions-Check)
- **Ansprache** (Du oder Sie — falls bekannt)

Falls diese Infos nicht mitgeliefert werden, prüfe zuerst den Ordner-Scan (Schritt 0). Dann führe die Checks durch, die mit den vorhandenen Infos möglich sind, und überspringe kundenspezifische Punkte nur, wenn wirklich kein Kontext vorhanden ist.

## Ausgabeformat

Gib für jeden Check aus:

```
## Check [Nr] — [Name]
**Status:** ✅ Bestanden / ⚠️ Verbesserungswürdig / ❌ Nicht bestanden
**Fundstellen:** [Anzahl Probleme gefunden]

### Probleme
- **[Zitat/Stelle im Text]** → [Was das Problem ist] → [Verbesserungsvorschlag]

### Zusammenfassung
[1–2 Sätze Gesamtbewertung für diesen Check]
```

Am Ende aller Checks: Eine **Gesamtbewertung** mit Prioritätsliste.

---

## Die 12 Checks

Führe jeden Check in dieser Reihenfolge durch. Gehe dabei den gesamten Artikel Abschnitt für Abschnitt durch.

---

### Check 1 — Inhaltliche Tiefe & Redundanz

**Regel:** Jeder Abschnitt muss mindestens eine Information enthalten, die über Allgemeinwissen hinausgeht: eine konkrete Zahl, einen spezifischen Tipp, eine Insider-Empfehlung, eine unbekannte Tatsache, eine Einschränkung oder eine erfahrungsbasierte Einschätzung. Abschnitte, die nur das Offensichtliche beschreiben, sind austauschbar. Gleichzeitig darf kein Satz oder Absatz eine Information wiederholen, die bereits an anderer Stelle im Artikel steht — auch nicht in anderer Formulierung.

**Prüfmethode:** Prüfe pro Abschnitt zwei Dimensionen:

**A) Tiefe — Hat der Abschnitt Substanz?**
- Enthält er mindestens eine konkrete Zahl/Fakt (Preis, Entfernung, Zeit, Öffnungszeit)?
- Enthält er einen spezifischen, nicht-offensichtlichen Tipp?
- Würde ein anderer LLM-generierter Artikel zum gleichen Thema exakt das Gleiche sagen?

**Wenn alle drei Antworten Nein/Ja(letzte) sind → Abschnitt ist oberflächlich.**

**B) Redundanz — Wiederholt sich der Text?**
- Gehe den Artikel absatzweise durch. Frage dich bei jedem Satz: "Steht diese Information (oder eine Variante davon) schon woanders im Artikel?"
- Prüfe auch: Sätze, die nur "schön klingen" ohne neuen Informationswert — atmosphärische Füller, emotionale Abschlüsse, die nichts Neues sagen, Überleitungssätze ohne Inhalt.
- Faustregel: Wenn man einen Satz streicht und dem Leser danach keine Information und keine Handlungsanweisung fehlt → der Satz ist redundant.

**Typische Fundstellen für Redundanz:**
- Wiederholungen in anderer Formulierung ("Der Markt ist belebt" → drei Absätze später "Hier herrscht reges Treiben")
- Füllsätze als Überleitung ("Und so geht es weiter zum nächsten Highlight.")
- Emotionale Abschlüsse am Absatzende, die nichts Neues sagen
- Atmosphärische Sätze ohne Fakten ("Die Stimmung kippt, es wird kühler, gedämpfter.")

**Output:** Liste der oberflächlichen Abschnitte mit Vorschlag, welche konkrete Information fehlt. Liste jeden redundanten oder überflüssigen Satz mit Zitat und begründe, warum er keine neue Info liefert.

**Beispiel Oberflächlichkeit:**
- ❌ Abschnitt "Marienplatz": Beschreibt nur, dass der Platz belebt ist und Touristen anzieht — kein konkreter Tipp, keine Zahl, keine Insider-Info.
- ✅ Besser: Öffnungszeiten Glockenspiel, bester Fotospot, Hinweis auf U-Bahn-Zugang.

**Beispiel Redundanz:**
- ❌ "Und so geht es weiter zum nächsten Highlight." → Reiner Übergangssatz ohne Information — streichen.
- ❌ "München ist eine lebendige Stadt" (Einleitung) + "Die Stadt zeigt sich hier von ihrer lebendigen Seite" (Absatz 5) → Gleiche Aussage, zweites Vorkommen streichen oder mit konkretem Detail ersetzen.

---

### Check 2 — Atmosphärisch-poetischer Stil

**Regel:** SEO-Content ist praktisch, informativ und direkt. Er darf eine eigene Stimme haben, aber die Basis ist immer: Information zuerst, Atmosphäre maximal als Nebensatz. Keine Feuilleton-Sprache, keine literarischen Metaphern, keine poetischen Schlussakkorde.

**Prüfmethode:** Suche gezielt nach:
- Literarischen Metaphern ("wie eine Theaterkulisse, die zufällig Verwaltung ist")
- Poetischen Beschreibungen ohne Informationswert ("Es ist dieselbe Stadt, nur mit anderem Tonfall")
- Stimmungsmalerei ("Unter den Arkaden verändert sich das Licht")
- Dramaturgischen Begriffen im Kontext von Reise/SEO ("Schlussakkord", "Dramaturgie", "Bühne")

**Output:** Zitiere jede Fundstelle. Schlage für jede eine praktisch-informative Alternative vor.

**Beispiel:**
- ❌ "Die Perspektive wirkt plötzlich wie ein gerahmtes Bild."
- ✅ "Vom Isartor hast du einen schönen Rückblick auf die Altstadt — guter Fotospot."

---

### Check 3 — KI-Dreierkaskaden

**Regel:** Drei aufgereihte Adjektive, Eigenschaften oder Beschreibungen in der Form "X, Y und Z" sind ein häufiges KI-Muster. Sie wirken generisch und sind fast immer durch eine konkretere, spezifischere Beschreibung ersetzbar.

**Prüfmethode:** Suche nach dem Muster "[Adjektiv/Beschreibung], [Adjektiv/Beschreibung] und [Adjektiv/Beschreibung]" — besonders als Satzabschluss oder charakterisierende Aufzählung.

**Beispiele für Fundstellen:**
- "Es ist laut, gesellig und manchmal ein bisschen überdreht."
- "Der Markt ist lebendig, farbenfroh und voller Aromen."
- "Die Stadt zeigt sich hier elegant, großzügig und fast demonstrativ geschniegelt."

**Output:** Liste jede Dreierkaskade. Schlage eine spezifischere Alternative vor, die NICHT wieder drei Dinge aufzählt.

---

### Check 4 — Prophylaktische Relativierungen (KI-Hedging)

**Regel:** LLMs neigen dazu, jeden möglichen Lesereinwand vorwegzunehmen. Das erzeugt einen defensiven Ton und ist ein starkes KI-Signal. In gutem SEO-Content trifft der Autor eine Aussage und steht dazu.

**Prüfmethode:** Suche nach:
- "Selbst wer [damit/mit X] wenig anfangen kann…"
- "Auch wenn Sie/du nicht [X wollen/willst]…"
- "Das ist nicht garantiert, aber/bleibt aber…"
- "Ob man nun [X] mag oder nicht…"
- "Wer [X] nicht kennt, wird trotzdem…"
- Jede Form von "Einwand vorwegnehmen + trotzdem empfehlen"

**Output:** Zitiere jede Fundstelle. Entscheide: Streichen oder durch direkte Aussage ersetzen.

---

### Check 5 — Literarische Antithesen

**Regel:** Das Muster "kein X, sondern Y" / "nicht X — Y" als stilistisches Mittel ohne Informationswert ist LLM-typisch. In SEO-Content sollte eine Sache direkt beschrieben werden, ohne erst zu sagen, was sie nicht ist.

**Prüfmethode:** Suche nach:
- "kein/e X, sondern Y"
- "nicht X — sondern Y [mit Bühne/Charakter/Geschichte]"
- "weniger X, mehr Y"
- Jede Konstruktion, die zuerst negiert und dann umformuliert

**Output:** Zitiere Fundstellen. Schlage direkte Formulierung vor.

**Beispiel:**
- ❌ "Das hier ist kein Museum, sondern Alltag mit Bühne."
- ✅ "Der Viktualienmarkt ist Münchens lebendiger Alltagsmarkt."

---

### Check 6 — Gleichförmiger Absatzrhythmus

**Regel:** Wenn mehrere aufeinanderfolgende Absätze dem gleichen Schema folgen (z.B. Sachliche Beschreibung → atmosphärische Beobachtung → praktischer Tipp → emotionaler Abschluss), wirkt der Text maschinell. Menschliche Autoren variieren den Aufbau.

**Prüfmethode:** Analysiere die Struktur der ersten 5+ inhaltlichen Absätze. Notiere für jeden das Schema (z.B. "Fakt → Atmosphäre → Tipp → Emotion"). Wenn 3+ Absätze hintereinander das gleiche Schema haben → markieren.

**Output:** Zeige die Absatzstruktur-Analyse. Markiere gleichförmige Sequenzen. Schlage vor, welche Absätze einen anderen Aufbau brauchen (z.B. mal nur praktisch, mal mit Anekdote startend, mal nur ein kurzer Satz).

---

### Check 7 — Answer-First / "Das Wichtigste in Kürze"

**Regel:** Jeder SEO-Artikel sollte direkt nach der H1 einen kompakten Block haben, der die Kernfrage in 3–5 kurzen Punkten beantwortet. Das ist Standard für AI-Readiness, Featured Snippets und LLM-Zitierbarkeit.

**Prüfmethode:**
1. Hat der Artikel einen TL;DR / "Wichtigste in Kürze" / "Auf einen Blick"-Block in den ersten 200 Wörtern?
2. Wenn ja: Beantwortet er die Suchintention in extrahierbarer Form (Bullet Points, nicht Fließtext)?
3. Wenn nein: ❌

**Output:** Bestanden/Nicht bestanden. Wenn nicht bestanden: Schlage einen konkreten TL;DR-Block vor, basierend auf dem Artikelinhalt.

---

### Check 8 — Überschriften-Qualität

**Regel:** H2/H3-Überschriften müssen informativ und scanbar sein. Ein Leser, der nur die Überschriften liest, muss verstehen, worum es in jedem Abschnitt geht. Keine Metaphern, keine Wortspiele, keine atmosphärischen Titel.

**Prüfmethode:** Liste alle H2/H3-Überschriften. Bewerte jede einzeln:
- **Informativ:** Sagt die Überschrift sofort, worum es geht? (z.B. "Frauenkirche" ✅)
- **Atmosphärisch:** Klingt die Überschrift schön, aber man muss den Abschnitt lesen, um zu wissen worum es geht? (z.B. "Macht, Ruhe und der nachdenkliche Schlussakkord" ❌)
- **Keyword-relevant:** Enthält die Überschrift relevante Suchbegriffe?

**Output:** Tabelle aller Überschriften mit Bewertung. Für jede nicht-informative Überschrift: Alternative vorschlagen.

---

### Check 9 — Du/Sie-Konsistenz

**Regel:** Die Ansprache muss im gesamten Artikel konsistent sein. Kein Wechsel zwischen Du und Sie. Die Ansprache muss zur Brand Voice des Kunden passen (falls bekannt).

**Prüfmethode:**
1. Scanne den gesamten Text nach Du-Formen und Sie-Formen.
2. Zähle jeweils.
3. Gibt es einen Mix? → ❌
4. Falls Kunde bekannt: Passt die gewählte Ansprache zur Brand Voice?

**Output:** Ansprache-Analyse mit Zählung. Warnung bei Inkonsistenz oder Brand-Voice-Mismatch.

---

### Check 10 — Format-Check (1 Thema = 1 Abschnitt)

**Regel:** Jeder H3-Abschnitt sollte genau ein Hauptthema behandeln. Wenn mehrere eigenständige Themen (z.B. verschiedene Sehenswürdigkeiten, verschiedene Produkte) in einem Abschnitt gebündelt sind, leidet die Scannability und die Bildlogik geht verloren.

**Prüfmethode:** Gehe jeden H3-Abschnitt durch. Zähle die eigenständigen Themen/Entitäten. Wenn ein Abschnitt 2+ klar trennbare Themen behandelt → markieren.

**Output:** Liste der problematischen Abschnitte mit Vorschlag, wie sie aufgetrennt werden sollten.

---

### Check 11 — Faktencheck

**Regel:** Alle konkreten Fakten im Artikel müssen stimmen. Das betrifft Zahlen, Daten, Öffnungszeiten, Preise, historische Angaben, Entfernungen, Eigennamen und Sachaussagen. Falsche Fakten untergraben die Glaubwürdigkeit des gesamten Artikels — und können bei Kunden-Websites rechtliche oder reputationsbezogene Folgen haben.

**Warum dieser Check besonders wichtig ist:** Wenn der Artikel auf Basis der vorherigen Checks überarbeitet und verbessert wird, schleichen sich häufig neue Fakten ein — z.B. konkretere Zahlen, Tipps oder Details, die der überarbeitende LLM "ergänzt" hat. Diese klingen plausibel, sind aber nicht immer korrekt. Deshalb ist die Verifizierung ein eigenständiger, abschließender Check.

**Prüfmethode:**
1. Gehe den Artikel absatzweise durch und extrahiere alle überprüfbaren Faktenbehauptungen:
   - Zahlen (Preise, Entfernungen, Einwohnerzahlen, Jahreszahlen, Öffnungszeiten)
   - Eigennamen (Personen, Orte, Unternehmen, Gebäude)
   - Sachaussagen ("X wurde im Jahr Y gegründet", "X ist das größte Y in Z")
   - Praktische Tipps mit konkreten Angaben ("Die Fahrt dauert 20 Minuten", "Eintritt kostet 12 €")
2. Verifiziere jede Faktenbehauptung:
   - **Primär:** Nutze Web-Suche (Google/Chrome), um die Fakten online zu überprüfen. Suche gezielt nach der konkreten Behauptung.
   - **Bei Kundendomain:** Wenn eine Domain bekannt ist, prüfe auch die Website des Kunden — stimmen die Angaben im Artikel mit den Infos auf der Kunden-Website überein? (z.B. Preise, Produktnamen, Öffnungszeiten, Standorte)
   - **Quellen notieren:** Halte für jede geprüfte Faktenbehauptung fest, woher die Bestätigung oder Widerlegung kommt.
3. Kategorisiere jede Faktenbehauptung:
   - ✅ **Bestätigt** — durch mindestens eine verlässliche Quelle verifiziert
   - ⚠️ **Nicht verifizierbar** — keine Quelle gefunden, aber Behauptung klingt plausibel
   - ❌ **Falsch / Widerspruch** — Quelle widerspricht der Behauptung im Artikel

**Output:** Tabelle aller geprüften Fakten mit Status, Quelle und — bei Fehlern — korrekter Information. Für jeden Fehler: konkreten Korrekturvorschlag mit Quellenangabe.

**Beispiel:**
| Fakt im Artikel | Status | Quelle / Korrektur |
|---|---|---|
| "Die Frauenkirche wurde 1468 erbaut" | ⚠️ | Baubeginn war 1468, Fertigstellung 1488 — Formulierung präzisieren |
| "Eintritt: 7,50 €" | ❌ | Laut muenchen.de aktuell 10 € (Stand 2025) |
| "Öffnungszeiten: 9–17 Uhr" | ✅ | Bestätigt via offizieller Website |

---

### Check 12 — Wettbewerber-Check

**Regel:** Ein SEO-Artikel wird für einen bestimmten Kunden geschrieben. Der Text darf keine Wettbewerber-Brands oder Konkurrenzprodukte nennen, empfehlen oder in ein besseres Licht rücken als die Kunden-Brand. LLMs neigen dazu, bei vergleichenden Themen automatisch Marktführer oder bekannte Alternativen aufzuzählen — das ist für Kunden-Content ein echtes Problem, weil es Traffic und Vertrauen an die Konkurrenz verschenkt.

**Was genau geprüft wird:**

1. **Direkte Wettbewerber-Nennungen:** Werden Konkurrenz-Brands, -Produkte oder -Dienste namentlich erwähnt?
   - Markennamen (z.B. "Produkt X von [Wettbewerber]")
   - Produkt- oder Dienstnamen, die eindeutig einem Wettbewerber zuzuordnen sind
   - Domains oder URLs von Wettbewerbern
   - Beiläufige Erwähnungen wie "ähnlich wie [Wettbewerber]" oder "bekannt durch Anbieter wie [Wettbewerber]"

2. **Wettbewerber-Promotion:** Wird ein Wettbewerber positiv dargestellt oder sogar empfohlen? Typische KI-Muster:
   - "Neben [Kunde] bieten auch [Wettbewerber A] und [Wettbewerber B] gute Lösungen an"
   - "Eine beliebte Alternative ist [Wettbewerber]"
   - Vergleichstabellen oder Aufzählungen, in denen Wettbewerber gleichwertig oder besser positioniert werden
   - "Marktführer wie [Wettbewerber]" — positioniert den Wettbewerber aktiv als führend

3. **Negative Positionierung der Kunden-Brand:** Wird der Kunde schlechter dargestellt als die Konkurrenz?
   - "Im Vergleich zu [Wettbewerber] ist [Kunde] zwar günstiger, aber..."
   - Relativierungen wie "nicht so bekannt wie...", "kleiner als..."
   - Formulierungen, die dem Kunden eine untergeordnete Marktposition zuweisen

4. **Generische Wettbewerber-Verweise:** Auch ohne konkreten Markennamen kann der Text indirekt Wettbewerber pushen:
   - "Andere Anbieter in diesem Bereich bieten zusätzlich..."
   - "Im Marktvergleich schneiden einige Anbieter besser ab bei..."
   - Jede Formulierung, die dem Leser nahelegt, sich woanders umzusehen

**Prüfmethode:**
1. Identifiziere die Kunden-Brand (aus Briefing, Ordner-Scan oder Nutzer-Angabe). Wenn kein Kundenname bekannt ist, prüfe trotzdem auf generische Wettbewerber-Verweise und offensichtliche Fremd-Brands.
2. Scanne den gesamten Text nach Markennamen, Produktnamen und Firmennamen, die nicht zur Kunden-Brand gehören.
3. Prüfe bei jeder gefundenen Fremd-Marke: Wird sie neutral-informativ erwähnt (z.B. als Fakt in einem historischen Kontext) oder wird sie promotet/empfohlen?
4. Prüfe, ob die Kunden-Brand im Text immer mindestens gleichwertig oder stärker positioniert ist als jede andere erwähnte Marke.

**Wichtige Ausnahme:** Nicht jede Erwähnung einer anderen Marke ist ein Problem. Kontextabhängig akzeptabel:
- Historische oder faktische Einordnungen ("Das Gebäude wurde von [Architekturbüro] entworfen")
- Branchenstandards oder Normen ("nach DIN-Norm", "zertifiziert durch [Organisation]")
- Technische Kompatibilität ("kompatibel mit [Plattform/Format]")

Die Kernfrage ist immer: Profitiert der Wettbewerber von dieser Erwähnung? Könnte der Leser dadurch zum Wettbewerber abwandern?

**Output:** Liste aller Wettbewerber-Erwähnungen mit Zitat, Einschätzung (problematisch / akzeptabel) und — bei problematischen Stellen — Vorschlag, wie die Passage ohne Wettbewerber-Nennung umformuliert werden kann.

**Beispiel:**
- ❌ "Neben Kunde bietet auch KonkurrenzTool eine leistungsstarke Lösung." → Streichen. Stattdessen: die Stärke des Kunden-Produkts direkt benennen.
- ❌ "Ähnlich wie bei MarktführerX setzt Kunde auf KI-gestützte Analyse." → Der Vergleich positioniert MarktführerX als Referenz. Besser: "Kunde setzt auf KI-gestützte Analyse — [konkreter Vorteil]."
- ✅ "Das System ist mit SAP und Salesforce kompatibel." → Technische Kompatibilität, kein Wettbewerber-Push.

---

## Gesamtbewertung

Nach allen 12 Checks: Erstelle eine Zusammenfassung.

```
## Gesamtbewertung

**Bestanden:** [X] von 12 Checks
**Verbesserungswürdig:** [X]
**Nicht bestanden:** [X]

### Prioritätsliste (nach Wichtigkeit sortiert)
1. [Kritischster Punkt] — [1 Satz warum]
2. [Zweitwichtigster Punkt] — [1 Satz warum]
3. ...

### Stärken
- [Was der Artikel gut macht]

### Fazit
[2–3 Sätze Gesamturteil: Ist der Artikel publikationsreif oder braucht er Überarbeitung? Was ist der größte Hebel?]
```

---

## Export-Datei für Rewrite

Nach der Gesamtbewertung: Erstelle automatisch eine **Markdown-Datei** (`rewrite-briefing.md`), die alle Check-Ergebnisse kompakt zusammenfasst — optimiert dafür, sie in einem neuen Chat als Input für einen Rewrite-Skill zu verwenden.

**Wichtig:** Das Rewrite-Briefing enthält **nicht** den Originaltext. Der Nutzer fügt den Originaltext selbst separat in den Rewrite-Chat ein. Das Briefing enthält ausschließlich die Check-Ergebnisse, Fundstellen, Verbesserungsvorschläge und Rewrite-Anweisungen — also alles, was beschreibt, *was* am Text geändert werden soll.

**Dateistruktur:**

```markdown
# Rewrite-Briefing: [Artikeltitel oder Thema]

## Check-Ergebnisse

### Check 1 — Inhaltliche Tiefe & Redundanz
**Status:** [✅/⚠️/❌]
**Probleme:**
- **"[Zitat]"** → [Problem] → [Verbesserungsvorschlag]
- ...

### Check 2 — Atmosphärisch-poetischer Stil
**Status:** [✅/⚠️/❌]
**Probleme:**
- **"[Zitat]"** → [Problem] → [Verbesserungsvorschlag]
- ...

[... alle weiteren Checks ...]

---

## Prioritätsliste
1. [Kritischster Punkt]
2. [Zweitwichtigster Punkt]
3. ...

---

## Rewrite-Anweisungen
- Behebe alle oben gelisteten Probleme
- Behalte alle bestätigten Fakten und korrekten Informationen bei
- Ersetze oberflächliche Abschnitte durch inhaltlich tiefere Alternativen
- Entferne alle redundanten Sätze und Füller
- Entferne oder ersetze alle problematischen Wettbewerber-Nennungen
- Stelle sicher, dass die Kunden-Brand nie schwächer positioniert wird als Fremd-Brands
- Halte die Ansprache konsistent: [Du/Sie]
- Keyword: [Keyword falls bekannt]
- Kunde/Domain: [Kunde falls bekannt]
```

**Vorgehen:**
1. Erstelle die Datei `rewrite-briefing.md` im Arbeitsverzeichnis.
2. Füge alle Check-Ergebnisse mit konkreten Fundstellen und Verbesserungsvorschlägen ein.
3. Speichere die Datei und biete sie dem Nutzer zum Download an.
4. Weise den Nutzer darauf hin: "Du kannst diese Datei zusammen mit dem Originaltext in einem neuen Chat mit deinem Rewrite-Skill verwenden. Füge den Originaltext dort separat ein."

---

## Wichtige Hinweise für die Durchführung

1. **Sei konkret.** Keine vagen Bewertungen ("könnte besser sein"). Immer mit Zitat aus dem Text belegen.
2. **Schlage Alternativen vor.** Jedes markierte Problem braucht einen konkreten Verbesserungsvorschlag.
3. **Sei ehrlich, nicht diplomatisch.** Der Skill existiert, um Probleme zu finden, nicht um den Text zu loben.
4. **Gehe sequentiell vor.** Jeden Check einzeln durchführen, den gesamten Artikel durchgehen, dann zum nächsten Check. Nicht mehrere Checks gleichzeitig.
5. **Zähle.** Wo möglich, Fundstellen zählen. "3 Dreierkaskaden gefunden" ist besser als "einige Dreierkaskaden gefunden".
6. **Erstelle immer die Export-Datei.** Nach jedem vollständigen Durchlauf wird automatisch das Rewrite-Briefing generiert und zum Download angeboten.
