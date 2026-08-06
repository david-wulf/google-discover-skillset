#!/usr/bin/env python3
"""
pctr.py — Mess- und Rechen-Backend fuer den Skill discover-headline.

Zwei Unterbefehle, bewusst getrennt, damit die Bewertung nicht im Modellkopf
verrechnet wird:

  features  messbare Titelmerkmale (Laenge, Zahlen, Ansprache, Clickbait-Lexikon,
            erkannte Formel, Position der Kernentitaet) — Anker fuer die Bewertung
  score     rechnet die acht bewerteten Dimensionen nach der veroeffentlichten
            pCTR-Formel in einen Prozentwert um und vergleicht die Varianten

Die Formel und die Gewichte stammen aus dem pCTR Predictor von metehan.ai
(pctr-discover.pages.dev), wo beide offen auf der Seite dokumentiert sind:

    quality   = Summe(w_i * f_i)              acht Dimensionen, Gewichte unten
    beta      = 1 - 0.35 * (clickbait / 10)
    raw       = quality * beta
    pCTR      = 0.5% + (22% - 0.5%) * sigmoid(0.65 * (raw - 5.5))

Bandgrenzen ebenfalls aus dem Original (Client-JS): >=14 top, >=9 hoch,
>=5 mittel, darunter niedrig.

Aufruf:
    python pctr.py features --titles-file titel.txt [--entity "Balkonkraftwerk"]
    python pctr.py score --input bewertung.json

bewertung.json:
    {
      "titles": [
        {"title": "...", "baseline": true,
         "scores": {"entity_density": 6.5, "topic_clarity": 8, ...},
         "clickbait_score": 2.0}
      ]
    }

Nur Standardbibliothek.
"""

import argparse
import json
import math
import re
import sys
import unicodedata

# --------------------------------------------------------------------------- #
# Modellkonstanten — aus dem Original uebernommen, nicht selbst gewaehlt
# --------------------------------------------------------------------------- #

WEIGHTS = {
    "entity_density": 0.22,
    "topic_clarity": 0.18,
    "informational_value": 0.16,
    "freshness_signal": 0.12,
    "engagement_depth": 0.10,
    "title_formatting": 0.08,
    "natural_authority": 0.08,
    "visual_promise": 0.06,
}

BETA_MAX_PENALTY = 0.35     # maximaler Abzug bei clickbait_score = 10
PCTR_FLOOR = 0.5            # Prozent
PCTR_CEIL = 22.0            # Prozent
SIGMOID_SLOPE = 0.65
SIGMOID_MIDPOINT = 5.5

# Bandgrenzen des Originals (pctrClass im Client-JS)
PCTR_BANDS = [(14.0, "top"), (9.0, "hoch"), (5.0, "mittel"), (0.0, "niedrig")]

# Laengenfenster fuer den og:title. Richtwert ~70-95 Zeichen: darunter bleibt
# Platz fuer den Haken ungenutzt, darueber wird im Feed abgeschnitten.
LEN_SWEET = (70, 95)
LEN_ACCEPTABLE = (50, 110)

# --------------------------------------------------------------------------- #
# Lexika
# --------------------------------------------------------------------------- #

CLICKBAIT_PATTERNS = {
    "de": [
        r"\bdu wirst (?:es )?nicht glauben\b", r"\bwas dann (?:passiert|geschah)\b",
        r"\bdas passiert,? wenn\b", r"\bniemand (?:weiss|weiß|spricht|redet)\b",
        r"\bkeiner (?:weiss|weiß|merkt|ahnt)\b", r"\bschockierend\b", r"\bunglaublich\b",
        r"\bkrass\b", r"\bwahnsinn\b", r"\bdieser (?:eine )?(?:trick|fehler|grund)\b",
        r"\bdiese (?:eine )?(?:sache|regel|zahl)\b", r"\bgeheim(?:e|es|nis)?\b",
        r"\bdas steckt (?:wirklich )?dahinter\b", r"\bendlich (?:klar|bewiesen)\b",
        r"\bjeder sollte\b", r"\bachtung\b", r"\bwarnung\b", r"\bsofort\b",
        r"\bdas aendert alles\b", r"\bdas (?:ae|ä)ndert alles\b",
    ],
    "en": [
        r"\byou won'?t believe\b", r"\bwhat happened next\b", r"\bthis one (?:trick|thing)\b",
        r"\bnobody (?:knows|talks)\b", r"\bshocking\b", r"\bunbelievable\b", r"\binsane\b",
        r"\bsecret\b", r"\bthe real reason\b", r"\bchanges everything\b",
        r"\beveryone should\b", r"\bwarning\b", r"\bright now\b", r"\bgone wrong\b",
    ],
}

SUPERLATIVES = {
    "de": [r"\bbeste[nrs]?\b", r"\bschlechteste[nrs]?\b", r"\bgroesste[nrs]?\b",
           r"\bgr(?:oe|ö)(?:ss|ß)te[nrs]?\b", r"\bschnellste[nrs]?\b",
           r"\bbilligste[nrs]?\b", r"\bg(?:ue|ü)nstigste[nrs]?\b", r"\berste[nrs]?\b",
           r"\beinzige[nrs]?\b", r"\bnie\b", r"\bimmer\b", r"\balle\b"],
    "en": [r"\bbest\b", r"\bworst\b", r"\bbiggest\b", r"\bfastest\b", r"\bcheapest\b",
           r"\bonly\b", r"\bnever\b", r"\balways\b", r"\bevery\b"],
}

AUTHORITY_MARKERS = {
    "de": [r"\blaut\b", r"\bnach Angaben\b", r"\bStudie\b", r"\bTest\b", r"\bStiftung\b",
           r"\bInstitut\b", r"\bExperten?\b", r"\bForscher\b", r"\bzufolge\b",
           r"\boffiziell\b", r"\bGericht\b", r"\bMinisterium\b"],
    "en": [r"\baccording to\b", r"\bstudy\b", r"\bresearch\b", r"\bexperts?\b",
           r"\bofficial\b", r"\bcourt\b", r"\bdata\b"],
}

FRESHNESS_MARKERS = {
    "de": [r"\bjetzt\b", r"\bneu(?:e|er|es)?\b", r"\bab (?:sofort|Januar|Februar|M(?:ae|ä)rz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\b",
           r"\bseit\b", r"\bab \d{4}\b", r"\b20\d{2}\b", r"\bheute\b", r"\bgerade\b",
           r"\bkommt\b", r"\bstartet\b", r"\b(?:aendert|ändert) sich\b", r"\bneue Regel\b"],
    "en": [r"\bnow\b", r"\bnew\b", r"\bstarting\b", r"\bsince\b", r"\b20\d{2}\b",
           r"\btoday\b", r"\bjust\b", r"\barrives\b", r"\bchanges\b"],
}

FORMULA_PATTERNS = [
    ("How-to", [r"^wie\b", r"\bso (?:geht|funktioniert|machst|baust)\b", r"^how to\b",
                r"\bin \d+ Schritten\b", r"\banleitung\b"]),
    ("Nummerierte Liste", [r"^\d+\s", r"\b\d+ (?:Wege|Tipps|Gr(?:ue|ü)nde|Fehler|Dinge|Tricks|Regeln|things|ways|reasons|tips)\b"]),
    ("Konträrer Ansatz", [r"\bwarum\b.*\b(?:falsch|nicht|kein)\b", r"\bstatt\b",
                          r"\bmythos\b", r"\bwhy\b.*\b(?:wrong|isn'?t|not)\b", r"\binstead\b"]),
    ("Trend-Hook", [r"\b20\d{2}\b", r"\bneue[snr]? (?:Gesetz|Regel|Pflicht|Vorschrift)\b",
                    r"\bab (?:Januar|Februar|M(?:ae|ä)rz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\b",
                    r"\bwas das f(?:ue|ü)r\b.*\bbedeutet\b"]),
    ("Experten-Zitat", [r"^laut\b", r"\bzufolge\b", r"\bsagt\b", r"\bwarnt\b",
                        r"\baccording to\b", r"\bsays\b"]),
    ("Entscheidungshilfe", [r"\boder\b.*\?", r"\blohnt sich\b", r"\bwann\b.*\bsinnvoll\b",
                            r"\bsollte(?:st|n)? (?:du|ich|man|Sie)\b", r"\bshould you\b"]),
    ("Zahlen-Kontrast", [r"\d+(?:[,.]\d+)?\s*(?:bis|statt|gegen|vs\.?)\s*\d+",
                         r"\bstatt \d+\b", r"\d+\s?(?:x|mal)\s+(?:schneller|mehr|weniger|so)\b",
                         r"\d+(?:[,.]\d+)?\s*(?:to|versus|vs\.?)\s*\d+"]),
    ("Kosten-Hook", [r"\bspar(?:st|en|t)\b", r"\bkostet\b", r"\bEuro\b", r"\b€\b",
                     r"\bcent\b", r"\bpreis\b", r"\bg(?:ue|ü)nstiger\b", r"\bsaves?\b"]),
    ("Frage", [r"\?\s*$"]),
]

STOP_DE = set("""
der die das den dem des ein eine einen einem einer eines und oder aber
ist sind war waren wird werden hat haben mit von zu im in am an auf
fuer für ueber über bei nach vor aus als wie was wer wo wann warum
so nicht kein keine nur auch schon noch mehr sehr man sich es
sie ihr ihre ihren ihrem du dein deine dich dir wir uns unser
""".split())


def fold(t):
    t = t.lower().translate(str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}))
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def detect_lang(text):
    words = [fold(w) for w in re.findall(r"[^\W\d_]+", text, re.UNICODE)]
    hits = sum(1 for w in words if w in {fold(x) for x in STOP_DE})
    return "de" if hits >= max(1, len(words) * 0.15) else "en"


def hits(text, patterns):
    found = []
    folded = fold(text)
    for p in patterns:
        for src in (text, folded):
            m = re.search(p, src, re.IGNORECASE)
            if m:
                found.append(m.group(0).strip().lower())
                break
    return sorted(set(found))


def length_band(n):
    if LEN_SWEET[0] <= n <= LEN_SWEET[1]:
        return "optimal"
    if LEN_ACCEPTABLE[0] <= n < LEN_SWEET[0]:
        return "kurz — Platz fuer den Haken bleibt ungenutzt"
    if LEN_SWEET[1] < n <= LEN_ACCEPTABLE[1]:
        return "lang — Abschneiden im Feed moeglich"
    if n < LEN_ACCEPTABLE[0]:
        return "zu kurz — traegt kaum einen Haken"
    return "zu lang — wird im Feed abgeschnitten"


def detect_formulas(title):
    found = []
    folded = fold(title)
    for name, pats in FORMULA_PATTERNS:
        for p in pats:
            if re.search(p, title, re.IGNORECASE) or re.search(p, folded, re.IGNORECASE):
                found.append(name)
                break
    return found


def entity_position(title, entity):
    """Zeichenposition der Kernentitaet und ob sie in den ersten 40 Zeichen steht."""
    if not entity:
        return None
    pos = fold(title).find(fold(entity))
    if pos < 0:
        return {"found": False}
    return {"found": True, "char_position": pos, "within_first_40": pos < 40,
            "share_of_title": round(pos / max(1, len(title)), 3)}


def features(title, entity=None, lang="auto"):
    if lang == "auto":
        lang = detect_lang(title)
    lk = lang if lang in CLICKBAIT_PATTERNS else "en"
    words = re.findall(r"[^\W_]+(?:[-'’][^\W_]+)*", title, re.UNICODE)
    caps = [w for w in words if len(w) > 2 and w.isupper()]

    cb = hits(title, CLICKBAIT_PATTERNS[lk])
    sup = hits(title, SUPERLATIVES[lk])
    auth = hits(title, AUTHORITY_MARKERS[lk])
    fresh = hits(title, FRESHNESS_MARKERS[lk])

    return {
        "title": title,
        "language": lang,
        "length": {
            "characters": len(title),
            "words": len(words),
            "band": length_band(len(title)),
            "in_sweet_spot_70_95": LEN_SWEET[0] <= len(title) <= LEN_SWEET[1],
        },
        "concreteness": {
            "has_number": bool(re.search(r"\d", title)),
            "has_percent": bool(re.search(r"%|\bProzent\b|\bpercent\b", title, re.I)),
            "has_currency": bool(re.search(r"[€$£]|\bEuro\b|\bCent\b|\bDollar\b", title, re.I)),
            "has_year": bool(re.search(r"\b(?:19|20)\d{2}\b", title)),
            "has_unit": bool(re.search(r"\d+\s?(?:kWh|kW|W|GB|TB|km|kg|l|m|Watt|Grad|°C|Zoll|Jahre?|Tage?|Minuten?|Stunden?)\b", title, re.I)),
            # Bewusst NICHT "proper_nouns": im Deutschen werden alle Substantive
            # grossgeschrieben, "Tag" und "Team" waeren dann Eigennamen. Die
            # Liste ist eine Rohbeobachtung, kein Entitaetennachweis — welche
            # davon echte Entitaeten sind, entscheidet die Bewertung.
            "capitalized_tokens": [w for w in words[1:]
                                   if w[:1].isupper()
                                   and fold(w) not in {fold(x) for x in STOP_DE}][:8],
            "capitalization_note": ("Deutsch schreibt alle Substantive gross — "
                                    "die Liste ist kein Entitaetennachweis"
                                    if lang == "de" else
                                    "Grossschreibung mitten im Satz ist ein "
                                    "Hinweis auf Eigennamen, kein Beweis"),
        },
        "address": {
            "question": title.strip().endswith("?"),
            "direct_address": bool(re.search(r"\b(?:du|dich|dir|dein\w*|euch|eure?\w*|your|you)\b", title, re.I))
                              or bool(re.search(r"\bSie\b|\bIhre?\w*\b", title)),
            "first_person": bool(re.search(r"\b(?:ich|mein\w*|wir|unser\w*|I|my|we|our)\b", title)),
            "exclamations": title.count("!"),
            "allcaps_words": caps,
        },
        "signals": {
            "authority_markers": auth,
            "freshness_markers": fresh,
            "superlatives": sup,
        },
        "clickbait_lexicon": {
            "matches": cb,
            "count": len(cb),
            "reading": ("keine Lexikontreffer" if not cb else
                        "ein Treffer — pruefen ob eingeloest" if len(cb) == 1 else
                        "mehrere Treffer — Clickbait-Verdacht"),
        },
        "formulas_detected": detect_formulas(title),
        "structure": {
            "has_colon": ":" in title,
            "has_dash": bool(re.search(r"\s[–—-]\s", title)),
            "segments": len([s for s in re.split(r"[:–—]|\s-\s", title) if s.strip()]),
        },
        "entity": entity_position(title, entity),
    }


# --------------------------------------------------------------------------- #
# Rechnung
# --------------------------------------------------------------------------- #

def sigmoid(x):
    if x < -60:
        return 0.0
    if x > 60:
        return 1.0
    return 1.0 / (1.0 + math.exp(-x))


def band_for(pctr):
    for threshold, name in PCTR_BANDS:
        if pctr >= threshold:
            return name
    return "niedrig"


def compute(scores, clickbait_score):
    missing = [k for k in WEIGHTS if k not in scores]
    if missing:
        raise SystemExit("Fehlende Dimensionen: %s" % ", ".join(sorted(missing)))
    unknown = [k for k in scores if k not in WEIGHTS]
    if unknown:
        raise SystemExit("Unbekannte Dimensionen: %s" % ", ".join(sorted(unknown)))
    for k, v in list(scores.items()) + [("clickbait_score", clickbait_score)]:
        if not (0 <= float(v) <= 10):
            raise SystemExit("%s = %s liegt ausserhalb 0..10" % (k, v))

    quality = sum(WEIGHTS[k] * float(scores[k]) for k in WEIGHTS)
    beta = 1.0 - BETA_MAX_PENALTY * (float(clickbait_score) / 10.0)
    raw = quality * beta
    pctr = PCTR_FLOOR + (PCTR_CEIL - PCTR_FLOOR) * sigmoid(
        SIGMOID_SLOPE * (raw - SIGMOID_MIDPOINT))

    contributions = {k: round(WEIGHTS[k] * float(scores[k]), 3) for k in WEIGHTS}
    ranked = sorted(contributions.items(), key=lambda kv: kv[1])
    # Kopfraum: wie viele Qualitaetspunkte laesst die Dimension noch liegen
    headroom = {k: round(WEIGHTS[k] * (10.0 - float(scores[k])), 3) for k in WEIGHTS}
    best_lever = max(headroom.items(), key=lambda kv: kv[1])

    return {
        "scores": {k: round(float(scores[k]), 1) for k in WEIGHTS},
        "clickbait_score": round(float(clickbait_score), 1),
        "quality_score": round(quality, 2),
        "beta_penalty": round(beta, 4),
        "beta_penalty_pct": round(beta * 100, 1),
        "quality_lost_to_clickbait": round(quality - raw, 2),
        "raw_score": round(raw, 2),
        "pctr_pct": round(pctr, 1),
        "band": band_for(pctr),
        "contributions": contributions,
        "weakest_contributions": [k for k, _ in ranked[:3]],
        "headroom": headroom,
        "biggest_lever": {"dimension": best_lever[0],
                          "quality_points_available": best_lever[1]},
    }


def compare(entries):
    out = []
    baseline = None
    for e in entries:
        r = compute(e["scores"], e.get("clickbait_score", 0))
        r["title"] = e.get("title", "")
        r["baseline"] = bool(e.get("baseline"))
        if r["baseline"] and baseline is None:
            baseline = r
        out.append(r)

    if baseline:
        for r in out:
            r["delta_vs_baseline"] = {
                "pctr_pp": round(r["pctr_pct"] - baseline["pctr_pct"], 1),
                "quality": round(r["quality_score"] - baseline["quality_score"], 2),
            }

    ranking = sorted(out, key=lambda r: -r["pctr_pct"])
    summary = {
        "count": len(out),
        "baseline_title": baseline["title"] if baseline else None,
        "best_title": ranking[0]["title"] if ranking else None,
        "best_pctr_pct": ranking[0]["pctr_pct"] if ranking else None,
        "spread_pp": (round(ranking[0]["pctr_pct"] - ranking[-1]["pctr_pct"], 1)
                      if len(ranking) > 1 else 0.0),
    }
    if baseline and ranking:
        summary["best_beats_baseline_pp"] = round(
            ranking[0]["pctr_pct"] - baseline["pctr_pct"], 1)
    return {"model": {
                "weights": WEIGHTS,
                "beta_max_penalty": BETA_MAX_PENALTY,
                "pctr_range_pct": [PCTR_FLOOR, PCTR_CEIL],
                "sigmoid": {"slope": SIGMOID_SLOPE, "midpoint": SIGMOID_MIDPOINT},
                "midpoint_maps_to_pctr_pct": round(
                    PCTR_FLOOR + (PCTR_CEIL - PCTR_FLOOR) * 0.5, 2),
            },
            "summary": summary, "results": out}


def main():
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("features", help="messbare Titelmerkmale")
    f.add_argument("--titles-file", help="eine Zeile pro Titel")
    f.add_argument("--title", action="append", help="Titel direkt (mehrfach moeglich)")
    f.add_argument("--entity", help="Kernentitaet, fuer die Positionspruefung")
    f.add_argument("--lang", default="auto")

    s = sub.add_parser("score", help="pCTR aus den bewerteten Dimensionen rechnen")
    s.add_argument("--input", help="JSON-Datei; ohne Angabe wird stdin gelesen")

    args = ap.parse_args()

    if args.cmd == "features":
        titles = list(args.title or [])
        if args.titles_file:
            with open(args.titles_file, encoding="utf-8") as fh:
                titles += [l.strip() for l in fh if l.strip()]
        if not titles:
            raise SystemExit("Keine Titel uebergeben.")
        if len(titles) > 5:
            sys.stderr.write("Hinweis: %d Titel uebergeben, das Original verarbeitet "
                             "maximal 5 pro Durchlauf.\n" % len(titles))
        out = [features(t, args.entity, args.lang) for t in titles]
        sys.stdout.write(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        raw = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
        payload = json.loads(raw)
        entries = payload["titles"] if isinstance(payload, dict) else payload
        sys.stdout.write(json.dumps(compare(entries), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
