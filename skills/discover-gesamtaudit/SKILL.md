---
name: discover-gesamtaudit
description: >
  Orchestriert ein vollständiges Google-Discover-Audit über alle Ebenen und fasst die
  Einzelergebnisse zu einem Kundenbericht zusammen: Zulassung und Domain-Traffic, technische
  Prüfung der veröffentlichten URL, Artikeltext, Headline und Titelbild. Ruft dafür die
  zuständigen Spezial-Skills in der richtigen Reihenfolge auf, bricht früh ab, wenn eine
  Vorstufe blockiert, und liefert eine Stationsdiagnose statt einer Mängelliste.
  Verwende diesen Skill, wenn ein umfassendes oder vollständiges Discover-Audit gewünscht ist —
  auch bei: "komplettes Discover-Audit", "Discover-Analyse für Kunden", "volle Discover-Prüfung",
  "Discover-Audit für Domain X und Artikel Y", "alles zu Discover prüfen", "Discover-Report",
  "warum läuft Discover bei uns nicht", "Discover-Potenzialanalyse", "Discover-Beratung",
  "Rundum-Check Discover".
  Nicht verwenden, wenn nur ein einzelner Hebel geprüft werden soll — dann direkt den passenden
  Skill: discover-readiness-domain (Domain), discover-readiness-artikel (URL-Technik),
  discover-content-optimizer (Text), discover-headline (Titel), discover-titelbild (Bild).
---

# Discover Gesamtaudit — Orchestrierung

Fünf Skills prüfen fünf Ebenen. Dieser Skill ruft sie in der richtigen Reihenfolge auf, bricht
früh ab, wenn eine Vorstufe blockiert, und macht aus fünf Teilergebnissen **einen** Bericht mit
einer Diagnose.

Der Wert liegt nicht im Zusammenkleben, sondern in der Reihenfolge: Es ist sinnlos, Headline und
Bild zu optimieren, wenn die Domain im betroffenen Verzeichnis gar nicht discover-fähig ist. Genau
das passiert in der Praxis regelmäßig.

## Grundregeln

1. **Reihenfolge einhalten.** Die Ebenen bauen aufeinander auf. Wer bei Ebene 4 anfängt,
   optimiert vielleicht an einem Artikel, der nie ausgespielt wird.
2. **Früh abbrechen, nicht durchlaufen.** Blockiert eine Vorstufe (manuelle Maßnahme,
   Blocker-Tag, fehlendes `max-image-preview:large`), wird das gemeldet und **gefragt**, ob
   weitergeprüft werden soll — statt fünf Berichte zu erzeugen, von denen vier keine Rolle spielen.
3. **Kein Meta-Score.** Die Einzelscores werden **nicht** zu einer Gesamtnote verrechnet. Sie
   messen Verschiedenes auf verschiedenen Ebenen; ein Mittelwert wäre eine erfundene Zahl. Der
   Bericht führt sie nebeneinander und benennt den Engpass.
4. **Nichts doppelt beurteilen.** Jede Aussage kommt aus genau einem Skill. Wo zwei Skills dasselbe
   prüfen (`max-image-preview:large`, Bildbreite), gilt das Ergebnis des spezialisierteren.
5. **Belegpflicht bleibt.** Der zusammengeführte Bericht übernimmt Zitate und Messwerte, nicht
   Zusammenfassungen von Zusammenfassungen.

## Die fünf Ebenen

| # | Ebene | Skill | Braucht | Liefert |
|---|-------|-------|---------|---------|
| 1 | **Zulassung und Domain** | `discover-readiness-domain` | Domain, GSC-Zugang | Stationsdiagnose, Traffic nach Verzeichnis, Zulassungs-Blocker |
| 1b | **CTR-Diagnose** *(nur mit GSC)* | `discover-ctr-optimierung` | URL-Klicks und -Impressionen | Ob die CTR-Lücke statistisch belegt ist, welcher Engpass, Messplan |
| 2 | **URL-Technik** | `discover-readiness-artikel` | Artikel-URL | OG-Vollständigkeit, Schema, News-Sitemap, Startseiten-Prominenz, E-E-A-T im HTML |
| 3 | **Artikeltext** | `discover-content-optimizer` | Artikeltext | Discover Content Score, Entitäten, semantische Lücken, JSON-LD |
| 4 | **Headline** | `discover-headline` | `og:title` plus Text | pCTR, Varianten, Delta, Clickbait |
| 5 | **Titelbild** | `discover-titelbild` | Bild-URL plus `og:title` | Feed-Karten-Score, „was in welcher Größe verschwindet" |

**Ebene 1b ist der Wegweiser, wenn GSC angebunden ist.** Sie sagt, ob überhaupt ein CTR-Problem
vorliegt und ob es bei diesem Impressionsvolumen belegbar ist — und damit, ob die Ebenen 4 und 5
den Aufwand lohnen. Ohne diesen Schritt optimiert man leicht die Karte eines Artikels, der nur
200 Impressionen hat und dessen CTR-Schwankung reines Rauschen ist. Sie liefert außerdem den
Messplan, mit dem die Wirkung der Maßnahmen später überhaupt überprüfbar wird.

Kanalunabhängige Textqualität (KI-Muster, Tiefe, Überschriften) prüft `content-checker`. Er ist
**nicht** Teil dieser Kette, weil er nichts über Discover aussagt — bei Bedarf separat aufrufen und
das im Bericht als eigenen Block führen.

## Ablauf

### Schritt 0 — Umfang klären

Einmal fragen, wenn nicht aus der Anfrage hervorgeht:

| Was | Warum |
|-----|-------|
| **Domain** | für Ebene 1 |
| **Ein bis drei Beispiel-Artikel-URLs** | für Ebene 2–5. Idealerweise ein starker und ein schwacher Artikel — der Vergleich ist aussagekräftiger als zwei durchschnittliche |
| **GSC-Zugang vorhanden?** | ohne GSC entfällt der Traffic-Teil von Ebene 1; der Rest läuft |
| **Zielgruppe des Berichts** | intern oder Kunde. Bestimmt Sprache und Detailtiefe, nicht die Prüfung |

Wenn nur eine Domain kommt: Ebene 1 laufen lassen, daraus die Top-Discover-Seiten und ein
schwaches Verzeichnis ziehen und **daraus** die Beispiel-URLs wählen. Das ist besser als zu fragen,
weil die Daten die Auswahl treffen.

### Schritt 1 — Ebene 1: Zulassung und Domain

`discover-readiness-domain` aufrufen.

**Danach die Abbruchprüfung.** Wenn eines davon zutrifft, wird gestoppt und gefragt:

| Befund | Warum das alles andere überholt |
|--------|--------------------------------|
| Manuelle Maßnahme für Discover in der GSC | Solange die steht, wird nichts ausgespielt. Alles andere ist zweitrangig |
| `notranslate` oder `nopagereadaloud` gesetzt | Hält die Verarbeitung komplett an — stiller Totalausfall |
| `max-image-preview:large` domainweit fehlend | Ein-Zeilen-Fix mit maximaler Hebelwirkung; bis dahin läuft die gesamte Bildarbeit ins Leere |
| Transparenz-Angaben fehlen (Autor, Datum, Redaktion, Kontakt) | Zulassungsvoraussetzung, nicht Optimierung |
| Werbeanteil überschreitet den Nachrichtenanteil | Richtlinienverstoß mit Konsequenz für das Seitenlayout |

Formulierung in diesem Fall: den Befund nennen, den Fix nennen, und fragen, ob die Detailanalyse
trotzdem gefahren werden soll — es kann sinnvoll sein, sie vorzubereiten, während der Blocker
behoben wird. Aber die Entscheidung liegt beim Nutzer, nicht im Automatismus.

Aus Ebene 1 mitnehmen: die **Stationsdiagnose** (an welcher Station hängt es) und das
**Verzeichnis mit dem größten Missverhältnis** zwischen Publikationsvolumen und
Discover-Impressionen. Beides steuert, worauf die Ebenen 2–5 schauen.

### Schritt 1b — CTR-Diagnose, wenn GSC angebunden ist

`discover-ctr-optimierung` auf die ausgewählten Beispiel-URLs. Der Schritt kostet wenig und
verhindert den häufigsten Fehlaufwand im ganzen Audit.

Drei Ergebnisse steuern das weitere Vorgehen:

| Ergebnis | Konsequenz |
|----------|-----------|
| **Zu wenige Impressionen** für eine belastbare CTR | Ebenen 4 und 5 sind nicht datengestützt begründbar. Sie können trotzdem laufen, aber als begründete Verbesserung statt als messbarer Hebel — und der Bericht sagt das |
| **CTR belegt unter dem Referenzwert** | Ebenen 4 und 5 sind der Hebel. Die Engpass-Diagnose sagt, welche von beiden zuerst |
| **CTR im Zielband, Abstand nicht belegt** | Der Hebel liegt woanders. Ebenen 4 und 5 auf Feinschliff reduzieren und den Aufwand in Ebene 2 und 3 stecken |

Aus diesem Schritt außerdem mitnehmen: den **Messplan** (Portfolio- oder Einzelartikel-Messung,
Gruppengröße, Zeitfenster) und die **URL-Entscheidung** je Artikel — optimieren oder neu aufsetzen.
Beides gehört in den Maßnahmenteil des Berichts, weil es den Aufwand bestimmt.

### Schritt 2 — Ebenen 2 bis 5 je Artikel

Pro Beispiel-Artikel in dieser Reihenfolge, weil jede Ebene der nächsten etwas liefert:

1. **`discover-readiness-artikel`** — holt das HTML und liefert `og:title`, Bild-URL und
   Schema-Befunde. Damit sind die Eingaben für Ebene 3–5 beschafft.
2. **`discover-content-optimizer`** — braucht den Artikeltext. Liefert zusätzlich den **stärksten
   Fakt** des Textes, den Ebene 4 als Rohmaterial braucht.
3. **`discover-headline`** — braucht `og:title` (nicht die H1) und den stärksten Fakt aus Ebene 3.
   Liefert den **empfohlenen Titel**, den Ebene 5 für die Doppelungsprüfung braucht.
4. **`discover-titelbild`** — braucht Bild-URL und den empfohlenen Titel aus Ebene 4.

Diese Kette ist der Grund für die Reihenfolge. Wer Ebene 5 vor Ebene 4 laufen lässt, prüft die
Bild-Headline-Doppelung gegen den **alten** Titel und bekommt ein falsches Ergebnis.

**Bei mehreren Artikeln:** Ebenen 2–5 je Artikel vollständig, dann quer vergleichen. Wiederkehrende
Muster über alle Artikel sind wertvoller als Einzelbefunde — „in 3 von 3 Artikeln liegt das
Titelbild unter 1600 px" ist eine Template-Aufgabe, kein Redaktionsfehler.

### Schritt 3 — Zusammenführen

Der Bericht ist **nicht** die Aneinanderreihung der fünf Einzelberichte. Aufbau:

1. **Diagnose in drei Sätzen** — an welcher Station hängt es, was ist der Engpass, was kostet die
   Behebung. Diese drei Sätze sind das Ergebnis des Audits; alles danach ist Belegmaterial.
2. **Zulassungs-Ampel** — die fünf Blocker aus Schritt 1, jeweils erfüllt oder nicht. Ohne grün
   hier ist der Rest Vorarbeit.
3. **Score-Übersicht** — die Einzelscores nebeneinander, **nicht** verrechnet:

   | Ebene | Score | Band | Engpass |
   |-------|-------|------|---------|
   | Domain-Readiness | x/100 | | |
   | Content (je Artikel) | x/100 | | |
   | Headline (pCTR-Delta) | +x pp | | |
   | Feed-Karte (je Artikel) | x/100 | | |

4. **Muster über die Artikel** — was in allen geprüften Artikeln gleich ist. Das sind die
   Template- und Prozessaufgaben mit der größten Hebelwirkung.
5. **Top-5-Maßnahmen über alle Ebenen** — nach Impact sortiert, jede mit Ebene, Aufwand und
   erwarteter Wirkung. Hier werden die Einzelempfehlungen der fünf Skills **priorisiert**, nicht
   addiert. Fünf Skills liefern leicht 30 Empfehlungen; der Bericht bringt die fünf, die zählen.
6. **Was Template ist und was Redaktion ist** — die praktisch wichtigste Trennung für den Kunden.
   Ein fehlendes Meta-Tag ist ein Entwickler-Ticket, eine schwache Headline eine Redaktionsaufgabe.
   Beides landet sonst im selben Topf und nichts passiert.
7. **Methodik und Grenzen** — welche Werte gemessen, welche bewertet, welche geschätzt wurden;
   welche Empfehlungen Google-Doku sind und welche Praxis-Heuristik; und der Hinweis, dass keiner
   der Scores eine CTR-Prognose ist.

### Schritt 4 — Kundendokument anbieten

Einmal fragen, mehrfach wählbar: **Word-Bericht** (Skill `docx`), **Excel-Maßnahmenliste**
(Skill `xlsx`, eine Zeile pro Maßnahme mit Ebene, Priorität, Aufwand, Typ Template/Redaktion,
Status-Spalte zum Abarbeiten), **HTML-Einseiter**. Ohne Auswahl bleibt es beim Bericht im Chat plus
`.md`-Datei.

## Was dieses Audit nicht leistet

Gehört in den Methodik-Abschnitt, damit die Erwartung stimmt:

- **Keine Keyword- oder Themenrecherche.** Das Audit prüft vorhandene Artikel. Welche Themen
  überhaupt Discover-Potenzial haben, ist eine andere Frage.
- **Keine CTR-Prognose.** Kein Score sagt, welche CTR erreicht wird. Zur Einordnung: News-Seiten
  liegen im Schnitt bei rund 11 %, Non-News bei rund 6 %, Arbeitsziel 7–9 %.
- **Keine Aussage über Site-Trust.** Wenn eine Domain in einem Themenfeld keine thematische
  Autorität hat, ist das mit Content-Maßnahmen nicht kurzfristig lösbar. Das Audit erkennt es
  (Verzeichnis ohne Impressionen trotz Volumen), löst es aber nicht.
- **Discover ist ein Impuls, keine Basis.** Ein Artikel, der monatlich Traffic liefern soll,
  braucht Search-Rankings; Discover addiert Spitzen darauf. Wer Discover als Grundlast plant,
  plant falsch.
- **Volatilität ist Konstruktionsmerkmal**, nicht Fehlerbild. Ein Teil der Schwankung ist
  Test-Design von Google. Einzelne Einbrüche nicht überinterpretieren.

## Wenn Skills fehlen

Jeder der fünf Skills ist einzeln funktionsfähig, und dieser Wrapper funktioniert auch, wenn nur
ein Teil verfügbar ist. Dann: die verfügbaren Ebenen laufen lassen, die fehlenden im Bericht
**namentlich** als nicht geprüft ausweisen und sagen, welche Aussage dadurch fehlt. Keine Ebene
grob selbst nachahmen — ein geschätzter Score, der wie ein gemessener aussieht, ist schlimmer als
eine Lücke.
