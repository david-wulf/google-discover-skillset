#!/usr/bin/env python3
"""
textstats.py — deterministisches Rechen-Backend fuer den Skill discover-content-optimizer.

Berechnet reproduzierbare Textmetriken, damit die Bewertung nicht auf Gefuehl basiert:
  * Dokumentstatistik (Woerter, Saetze, Absaetze, Satzlaengenverteilung)
  * Lesbarkeit (Flesch EN / Flesch-Amstad DE)
  * Headline- und Lead-Metriken (Answer-First-Heuristik)
  * Faktendichte (Zahlen, Prozente, Waehrungen, Datumsangaben, Einheiten pro 100 Woerter)
  * TF-IDF ueber die Absaetze des Dokuments (echte IDF, kein reines TF)
  * Pro Entitaet: Frequenz, Erstposition, Absatz-Spread, Definitions-/Vergleichs-Marker
  * Entitaeten-Kookkurrenzmatrix (Jaccard ueber Saetze) + Integrations-Score

Nur Standardbibliothek. Aufruf:

    python textstats.py --input payload.json
    cat payload.json | python textstats.py

payload.json:
    {
      "text": "Headline in Zeile 1\n\nAbsatz ...",
      "entities": ["Apple", "M5 MacBook Pro"],     # optional
      "lang": "de"                                  # optional: de | en | auto (default auto)
    }

Ausgabe: JSON auf stdout.
"""

import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict

# --------------------------------------------------------------------------- #
# Sprachressourcen
# --------------------------------------------------------------------------- #

STOPWORDS = {
    "de": set("""
aber alle allem allen aller alles als also am an ander andere anderem anderen anderer anderes
auch auf aus bei beim bin bis bist da damit dann dar das dass dasselbe dazu dein deine dem den
denn der derer des deshalb dessen dich die dies diese dieselbe diesem diesen dieser dieses dir
doch dort du durch ein eine einem einen einer eines einig einige einigen einiger einiges einmal
er es etwas euer eure fuer gegen gewesen hab habe haben hat hatte hatten hier hin hinter ich
ihm ihn ihnen ihr ihre ihrem ihren ihrer ihres im in indem ins ist ja jede jedem jeden jeder
jedes jene jenem jenen jener jenes jetzt kann kein keine keinem keinen keiner keines koennen
koennte machen man manche manchem manchen mancher manches mein meine mit muss musste nach
nicht nichts noch nun nur ob oder ohne sehr sein seine seinem seinen seiner seines selbst sich
sie sind so solche solchem solchen solcher solches soll sollte sondern sonst ueber um und uns
unsere unser unter viel vom von vor waehrend war waren warum was weg weil weiter welche welchem
welchen welcher welches wenn werde werden wie wieder will wir wird wirst wo wollen wollte
wuerde wuerden zu zum zur zwar zwischen dabei schon mehr etwa laut wer wem wen sowie bzw
""".split()),
    "en": set("""
a about above after again against all am an and any are as at be because been before being
below between both but by can did do does doing down during each few for from further had has
have having he her here hers herself him himself his how i if in into is it its itself just me
more most my myself no nor not now of off on once only or other our ours ourselves out over own
same she should so some such than that the their theirs them themselves then there these they
this those through to too under until up very was we were what when where which while who whom
why will with you your yours yourself yourselves also would could may might one two per s t
""".split()),
}

# Generische Fuellwoerter, die nur beim Keyword-Ranking ausgeschlossen werden
# (nicht in der Entitaetenanalyse) — sie erzeugen sonst Scheintreffer wie
# "last year" oder "four years" in der Liste der thematischen Kernbegriffe.
LOW_INFO = {
    "de": set("""
letzte letzten letzter letztes erste ersten erster erstes zweite zweiten dritte neue neuen neuer
neues neu alte alten viele vieles wenige ganz ganze ganzen gute guter gutes gross grosse grossen
klein kleine lang lange kurz kurze eins zwei drei vier fuenf sechs sieben acht neun zehn beide
gibt geben gab gehen macht machte kommt kommen genau bereits jeweils dabei damit ebenso zudem
gut wichtig wichtigsten wichtige einfach richtig richtige weniger langfristig meist meisten
regel dinge trend moeglich moechten laesst
""".split()),
    "en": set("""
last first second third next new old same other another still much many even well way ways thing
things get gets got make makes made take takes took like really actually kind sort lot good bad
big small long short four five six seven eight nine ten twelve back come comes came go goes going
""".split()),
}

DEFINITION_MARKERS = {
    "de": [r"\bist ein", r"\bist eine", r"\bsind (?:ein|die|das|der)\b", r"\bbezeichnet\b",
           r"\bbedeutet\b", r"\bhandelt sich um\b", r"\bdefiniert\b", r"\bnennt man\b",
           r"\bsteht f(?:ue|ü)r\b", r"\bd\.h\.", r"\balso\b"],
    "en": [r"\bis a\b", r"\bis an\b", r"\bare (?:a|the)\b", r"\brefers to\b", r"\bmeans\b",
           r"\bdefined as\b", r"\bknown as\b", r"\bstands for\b", r"\bi\.e\."],
}

COMPARISON_MARKERS = {
    "de": [r"\bim Vergleich\b", r"\bverglichen\b", r"\bgegen(?:ue|ü)ber\b", r"\bals\b",
           r"\bstatt\b", r"\banstelle\b", r"\bwaehrend\b", r"\bw(?:ae|ä)hrend\b",
           r"\bUnterschied\b", r"\bvs\.?\b", r"\bbesser als\b", r"\bschneller als\b"],
    "en": [r"\bcompared\b", r"\bversus\b", r"\bvs\.?\b", r"\bthan\b", r"\bunlike\b",
           r"\bwhereas\b", r"\bdifference\b", r"\binstead of\b", r"\bagainst\b"],
}

CAUSAL_MARKERS = {
    "de": [r"\bweil\b", r"\bdeshalb\b", r"\bdaher\b", r"\bdadurch\b", r"\bfolglich\b",
           r"\bsodass\b", r"\bso dass\b", r"\bfuehrt zu\b", r"\bf(?:ue|ü)hrt zu\b",
           r"\bGrund\b", r"\bUrsache\b", r"\bbedeutet f(?:ue|ü)r\b"],
    "en": [r"\bbecause\b", r"\btherefore\b", r"\bthus\b", r"\bhence\b", r"\bso that\b",
           r"\bleads to\b", r"\bresults in\b", r"\breason\b", r"\bcause\b", r"\bwhich means\b"],
}

# Erfahrungs-/E-E-A-T-Marker (Erstautorschaft, eigener Test, Zitat)
# Bewusst eng gefasst: generische Woerter wie "selbst" wuerden sonst jeden Text
# als erfahrungsbasiert markieren ("selbst Strom erzeugen").
EXPERIENCE_MARKERS = {
    "de": [r"\bich habe\b", r"\bwir haben\b", r"\bim (?:eigenen )?Test\b", r"\bgetestet\b",
           r"\bselbst (?:getestet|gemessen|ausprobiert|erlebt|gebaut)\b",
           r"\bmeiner Erfahrung\b", r"\bunsere Messung\b", r"\bgemessen\b", r"\bausprobiert\b",
           r"\bvor Ort\b", r"\bim Praxistest\b"],
    "en": [r"\bi have\b", r"\bwe have\b", r"\bi tested\b", r"\bwe tested\b", r"\bin my testing\b",
           r"\bhands-on\b", r"\bmeasured\b", r"\bi tried\b", r"\bin practice\b"],
}

# Plural- und Beugungsformen mitnehmen: "Studien zeigen" ist der haeufigste
# Fall einer vagen Quellenangabe und darf nicht durchs Raster fallen.
SOURCE_MARKERS = {
    "de": [r"\blaut\b", r"\bzufolge\b", r"\bStudie[ns]?\b", r"\bnach Angaben\b", r"\bQuellen?\b",
           r"\bberichtet\b", r"\bmitgeteilt\b", r"\bAngaben\b", r"\bInstitut[se]?\b",
           r"\bUmfrage[n]?\b", r"\bUntersuchung(?:en)?\b", r"\bDaten (?:von|des|der)\b"],
    "en": [r"\baccording to\b", r"\bstud(?:y|ies)\b", r"\bresearch\b", r"\breported\b",
           r"\bsources?\b", r"\bsurveys?\b", r"\bdata from\b", r"\bsaid\b", r"\bannounced\b"],
}

# --------------------------------------------------------------------------- #
# Hilfen
# --------------------------------------------------------------------------- #

ABBREV = re.compile(r"\b(?:z\.B|bzw|u\.a|d\.h|ca|Nr|Abb|Dr|Prof|Mr|Mrs|Ms|St|vs|etc|Inc|approx|e\.g|i\.e)\.$",
                    re.IGNORECASE)

_UMLAUT = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
                         "Ä": "ae", "Ö": "oe", "Ü": "ue"})


def fold(token):
    """Umlaut- und akzentfreie Vergleichsform.

    Die Stoppwortlisten sind in ASCII notiert ("fuer", "ueber"). Ohne diese
    Faltung wuerde "fuer" im Text nie als Stoppwort erkannt werden.
    """
    t = token.lower().translate(_UMLAUT)
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def folded_set(words):
    return {fold(w) for w in words}


def detect_lang(text):
    """Grobe, aber ausreichende Sprachheuristik ueber Stopwort-Trefferquote."""
    words = re.findall(r"[^\W\d_]+", text.lower(), re.UNICODE)
    if not words:
        return "en"
    sample = [fold(w) for w in words[:400]]
    scores = {}
    for lang, sw in STOPWORDS.items():
        swf = folded_set(sw)
        scores[lang] = sum(1 for w in sample if w in swf)
    return max(scores, key=scores.get)


def split_paragraphs(text):
    parts = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
    if len(parts) <= 1:
        parts = [p.strip() for p in text.split("\n") if p.strip()]
    return parts


def split_sentences(text):
    """Satzsplit mit Abkuerzungsschutz."""
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    raw = re.split(r"(?<=[.!?:;])\s+", text)
    out, buf = [], ""
    for chunk in raw:
        buf = (buf + " " + chunk).strip() if buf else chunk
        if ABBREV.search(buf):
            continue
        out.append(buf)
        buf = ""
    if buf:
        out.append(buf)
    return [s for s in out if re.search(r"[^\W\d_]", s, re.UNICODE)]


def words_of(text):
    return re.findall(r"[^\W_]+(?:[-'’][^\W_]+)*", text, re.UNICODE)


def count_syllables(word, lang):
    w = word.lower()
    w = "".join(c for c in unicodedata.normalize("NFD", w) if unicodedata.category(c) != "Mn")
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if lang == "en" and w.endswith("e") and n > 1 and not w.endswith(("le", "ee", "ye")):
        n -= 1
    return max(1, n)


def normalize_token(tok):
    t = tok.lower().strip("-'’")
    return t


def is_heading_line(line):
    s = line.strip()
    if not s or len(s) > 120:
        return False
    if s.startswith("#"):
        return True
    if s.endswith((".", "!", "?", ":", ";", ",")):
        return False
    return len(words_of(s)) <= 12


def find_markers(text, patterns):
    """Sucht Marker im Original und in gefalteter Form.

    Die Muster sind teils ASCII notiert; die Faltung stellt sicher, dass
    "waehrend" und "während" beide treffen.
    """
    hits = []
    folded = fold(text)
    for p in patterns:
        for source in (text, folded):
            for m in re.finditer(p, source, re.IGNORECASE):
                hits.append(m.group(0).strip())
    return hits


# --------------------------------------------------------------------------- #
# Faktendichte
# --------------------------------------------------------------------------- #

NUM_PATTERNS = {
    "percent": r"\d+(?:[.,]\d+)?\s?%|\bProzent\b|\bpercent\b",
    "currency": r"(?:[€$£]\s?\d[\d.,]*)|(?:\d[\d.,]*\s?(?:Euro|EUR|Dollar|USD|Cent|dollars?))",
    "date": r"\b(?:\d{1,2}\.\s?(?:Jan|Feb|M(?:ae|ä)r|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez)[a-z]*|"
            r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2})\b"
            r"|\b(?:19|20)\d{2}\b",
    "unit": r"\b\d+(?:[.,]\d+)?\s?(?:kWh|Wh|kW|W|GB|TB|MB|GHz|MHz|km|m|cm|mm|kg|g|l|ml|"
            r"Zoll|inch|inches|Sekunden?|Minuten?|Stunden?|Tage?|Jahre?|seconds?|minutes?|hours?|days?|years?|"
            r"GB/s|MB/s|fps|nm|mAh|°C|Grad)\b",
    "plain_number": r"\b\d+(?:[.,]\d+)?\b",
}


def fact_density(text, word_count):
    counts = {}
    for key, pat in NUM_PATTERNS.items():
        counts[key] = len(re.findall(pat, text, re.IGNORECASE))
    total_specific = counts["percent"] + counts["currency"] + counts["date"] + counts["unit"]
    per100 = (counts["plain_number"] / word_count * 100) if word_count else 0.0
    spec100 = (total_specific / word_count * 100) if word_count else 0.0
    return {
        "counts": counts,
        "numbers_per_100_words": round(per100, 2),
        "specific_facts_per_100_words": round(spec100, 2),
    }


# --------------------------------------------------------------------------- #
# TF-IDF ueber Absaetze
# --------------------------------------------------------------------------- #

def tfidf(paragraphs, lang, top_n=30, ngram_max=3):
    # Vergleich ueber die gefaltete Form, Anzeige in Originalschreibweise.
    sw = folded_set(STOPWORDS.get(lang, STOPWORDS["en"])) | \
         folded_set(LOW_INFO.get(lang, LOW_INFO["en"]))

    def is_sw(tok):
        return fold(tok) in sw

    docs = []
    for p in paragraphs:
        toks = [normalize_token(t) for t in words_of(p)]
        toks = [t for t in toks if t and not t.isdigit() and len(t) > 2]
        grams = []
        content_flags = [not is_sw(t) for t in toks]
        for n in range(1, ngram_max + 1):
            for i in range(len(toks) - n + 1):
                window = toks[i:i + n]
                if not any(content_flags[i:i + n]):
                    continue
                if n > 1 and (is_sw(window[0]) or is_sw(window[-1])):
                    continue
                if n == 1 and is_sw(window[0]):
                    continue
                grams.append(" ".join(window))
        docs.append(grams)

    N = max(1, len(docs))
    df = Counter()
    for d in docs:
        for g in set(d):
            df[g] += 1
    total_tf = Counter()
    for d in docs:
        total_tf.update(d)

    scores = {}
    for g, tf in total_tf.items():
        if tf < 2 and " " not in g:
            continue
        idf = math.log((N + 1) / (df[g] + 1)) + 1.0
        scores[g] = (1 + math.log(tf)) * idf

    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:top_n]
    mx = ranked[0][1] if ranked else 1.0
    peaks = [
        {"term": g, "tf": total_tf[g], "df_paragraphs": df[g],
         "tfidf": round(s, 3), "tfidf_norm": round(s / mx, 3)}
        for g, s in ranked
    ]

    # Thematische Kernbegriffe: haeufig UND ueber viele Absaetze verteilt.
    # Das ist die Klammer des Artikels — TF-IDF-Spitzen sind dagegen lokale
    # Unterthemen. Beide Listen zusammen zeigen Fokus vs. Streuung.
    core_scores = {}
    for g, tf in total_tf.items():
        if df[g] < 2:
            continue
        spread = df[g] / N
        core_scores[g] = (1 + math.log(tf)) * spread
    core_ranked = sorted(core_scores.items(), key=lambda kv: (-kv[1], kv[0]))[:top_n]
    cmx = core_ranked[0][1] if core_ranked else 1.0
    core = [
        {"term": g, "tf": total_tf[g], "df_paragraphs": df[g],
         "paragraph_spread": round(df[g] / N, 3), "core_score": round(s / cmx, 3)}
        for g, s in core_ranked
    ]
    return peaks, core


# --------------------------------------------------------------------------- #
# Entitaeten
# --------------------------------------------------------------------------- #

def entity_stats(text, sentences, paragraphs, entities, lang):
    lang_key = lang if lang in DEFINITION_MARKERS else "en"
    lowered_sents = [s.lower() for s in sentences]
    lowered_paras = [p.lower() for p in paragraphs]
    text_len = max(1, len(text))

    per_entity = {}
    sent_sets = {}
    for ent in entities:
        e = ent.lower().strip()
        if not e:
            continue
        pat = re.compile(re.escape(e), re.IGNORECASE)
        occurrences = [m.start() for m in pat.finditer(text)]
        s_idx = {i for i, s in enumerate(lowered_sents) if e in s}
        p_idx = {i for i, p in enumerate(lowered_paras) if e in p}
        sent_sets[ent] = s_idx

        # Kontextfenster: +/- 120 Zeichen um jede Erwaehnung. Praeziser als der
        # ganze Satz, weil Marker sonst zufaellig weit entfernt matchen.
        windows = []
        for pos in occurrences:
            windows.append(text[max(0, pos - 120): pos + len(e) + 120])
        ctx = " … ".join(windows)
        defs = find_markers(ctx, DEFINITION_MARKERS[lang_key])
        cmps = find_markers(ctx, COMPARISON_MARKERS[lang_key])
        caus = find_markers(ctx, CAUSAL_MARKERS[lang_key])
        nums = len(re.findall(NUM_PATTERNS["plain_number"], ctx))

        per_entity[ent] = {
            "count": len(occurrences),
            "first_position_pct": round(occurrences[0] / text_len * 100, 1) if occurrences else None,
            "sentences": len(s_idx),
            "paragraphs": len(p_idx),
            "paragraph_spread": round(len(p_idx) / max(1, len(paragraphs)), 3),
            "in_headline": bool(occurrences) and occurrences[0] < len(paragraphs[0]) if paragraphs else False,
            "definition_markers": sorted(set(m.lower() for m in defs))[:5],
            "comparison_markers": sorted(set(m.lower() for m in cmps))[:5],
            "causal_markers": sorted(set(m.lower() for m in caus))[:5],
            "numbers_in_context": nums,
        }

    # Kookkurrenz (Jaccard ueber Saetze)
    names = [e for e in entities if e in sent_sets]
    matrix = {}
    for a in names:
        row = {}
        for b in names:
            if a == b:
                row[b] = 1.0
                continue
            sa, sb = sent_sets[a], sent_sets[b]
            union = len(sa | sb)
            row[b] = round(len(sa & sb) / union, 3) if union else 0.0
        matrix[a] = row

    # Integrations-Score pro Entitaet
    for ent in names:
        st = per_entity[ent]
        others = [v for k, v in matrix[ent].items() if k != ent]
        others.sort(reverse=True)
        top3 = others[:3]
        cooc = sum(top3) / len(top3) if top3 else 0.0

        freq_c = min(1.0, st["count"] / 3.0)
        spread_c = min(1.0, st["paragraph_spread"] / 0.4)
        ctx_hits = sum(1 for k in ("definition_markers", "comparison_markers", "causal_markers") if st[k])
        ctx_c = ctx_hits / 3.0
        num_c = min(1.0, st["numbers_in_context"] / 2.0)

        score = 0.25 * freq_c + 0.20 * spread_c + 0.25 * min(1.0, cooc / 0.35) + \
                0.20 * ctx_c + 0.10 * num_c
        st["max_cooccurrence"] = round(max(others) if others else 0.0, 3)
        st["mean_top3_cooccurrence"] = round(cooc, 3)
        st["integration_score"] = round(min(1.0, score), 3)
        st["integration_band"] = ("stark" if score >= 0.65 else
                                  "mittel" if score >= 0.4 else "isoliert")

    return per_entity, matrix


# --------------------------------------------------------------------------- #
# Hauptanalyse
# --------------------------------------------------------------------------- #

def analyse(text, entities=None, lang="auto"):
    entities = entities or []
    text = text.replace("\r\n", "\n").strip()
    if lang == "auto" or lang not in STOPWORDS:
        lang = detect_lang(text)

    lines = [l for l in text.split("\n") if l.strip()]
    paragraphs = split_paragraphs(text)
    headline = lines[0].strip().lstrip("# ").strip() if lines else ""
    body = "\n\n".join(paragraphs[1:]) if len(paragraphs) > 1 else ""

    sentences = split_sentences(text)
    all_words = words_of(text)
    wc = len(all_words)
    sc = max(1, len(sentences))

    sent_lens = [len(words_of(s)) for s in sentences]
    syll = sum(count_syllables(w, lang) for w in all_words)
    asl = wc / sc
    asw = (syll / wc) if wc else 0.0
    if lang == "de":
        flesch = 180 - asl - 58.5 * asw
    else:
        flesch = 206.835 - 1.015 * asl - 84.6 * asw

    lead_para = paragraphs[1] if len(paragraphs) > 1 else (paragraphs[0] if paragraphs else "")
    lead_words = words_of(lead_para)
    lead_sents = split_sentences(lead_para)
    lang_key = lang if lang in SOURCE_MARKERS else "en"

    heading_lines = [l.strip() for l in lines[1:] if is_heading_line(l)]
    list_markers = len(re.findall(r"^\s*(?:[-*•]|\d+[.)])\s+", text, re.MULTILINE))

    ent_stats, cooc = entity_stats(text, sentences, paragraphs, entities, lang)
    tfidf_peaks, core_terms = tfidf(paragraphs, lang)

    result = {
        "language_detected": lang,
        "document": {
            "characters": len(text),
            "words": wc,
            "sentences": sc,
            "paragraphs": len(paragraphs),
            "avg_sentence_words": round(asl, 1),
            "median_sentence_words": (sorted(sent_lens)[len(sent_lens) // 2] if sent_lens else 0),
            "long_sentences_over_25w": sum(1 for n in sent_lens if n > 25),
            "long_sentence_ratio": round(sum(1 for n in sent_lens if n > 25) / sc, 3),
            "avg_paragraph_words": round(wc / max(1, len(paragraphs)), 1),
            "paragraphs_over_120w": sum(1 for p in paragraphs if len(words_of(p)) > 120),
            "subheadings_detected": len(heading_lines),
            "subheading_texts": heading_lines[:20],
            "list_items": list_markers,
            "question_sentences": sum(1 for s in sentences if s.strip().endswith("?")),
            "quote_marks": len(re.findall(r"[\"“”„»«]", text)) // 2,
        },
        "readability": {
            "formula": "Flesch-Amstad (de)" if lang == "de" else "Flesch Reading Ease (en)",
            "score": round(flesch, 1),
            "band": ("sehr leicht" if flesch >= 80 else
                     "leicht" if flesch >= 60 else
                     "mittel" if flesch >= 50 else
                     "schwer" if flesch >= 30 else "sehr schwer"),
            "avg_syllables_per_word": round(asw, 2),
        },
        "headline": {
            "text": headline,
            "characters": len(headline),
            "words": len(words_of(headline)),
            "over_65_chars": len(headline) > 65,
            "contains_number": bool(re.search(r"\d", headline)),
            "contains_colon_or_dash": bool(re.search(r"[:–—-]", headline)),
            "direct_address": bool(re.search(r"\b(?:du|dein|deine|ihr|euer|your|you)\b", headline, re.I)),
            "question": headline.strip().endswith("?"),
        },
        "lead": {
            "text": lead_para[:400],
            "words": len(lead_words),
            "sentences": len(lead_sents),
            "first_sentence_words": len(words_of(lead_sents[0])) if lead_sents else 0,
            "contains_number": bool(re.search(r"\d", lead_para)),
            "answer_first_hint": bool(lead_sents) and len(words_of(lead_sents[0])) <= 25
                                 and bool(re.search(r"\d|\b(?:ist|sind|kostet|bedeutet|is|are|costs|means)\b",
                                                    lead_sents[0], re.I)),
        },
        "fact_density": fact_density(text, wc),
        "trust_markers": {
            "experience": sorted(set(m.lower() for m in find_markers(text, EXPERIENCE_MARKERS[lang_key])))[:10],
            "sources": sorted(set(m.lower() for m in find_markers(text, SOURCE_MARKERS[lang_key])))[:10],
            "causal": sorted(set(m.lower() for m in find_markers(text, CAUSAL_MARKERS[lang_key])))[:10],
            "urls": re.findall(r"https?://[^\s)\"']+", text)[:20],
        },
        "topical_core_terms": core_terms,
        "tfidf_peak_terms": tfidf_peaks,
        "entities": ent_stats,
        "entity_cooccurrence": cooc,
    }

    if ent_stats:
        bands = Counter(v["integration_band"] for v in ent_stats.values())
        result["entity_summary"] = {
            "count": len(ent_stats),
            "bands": dict(bands),
            "mean_integration": round(
                sum(v["integration_score"] for v in ent_stats.values()) / len(ent_stats), 3),
            "isolated": sorted([k for k, v in ent_stats.items() if v["integration_band"] == "isoliert"]),
            "not_found": sorted([k for k, v in ent_stats.items() if v["count"] == 0]),
        }
    return result


def main():
    # Ohne das liefert die Ausgabe auf Windows-Konsolen (cp1252) Ersatzzeichen
    # statt Umlauten.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="Pfad zur JSON-Datei; ohne Angabe wird stdin gelesen")
    ap.add_argument("--text-file", help="Pfad zu einer reinen Textdatei (Alternative zu --input)")
    ap.add_argument("--entities", help="Kommagetrennte Entitaetenliste (nur mit --text-file)")
    ap.add_argument("--lang", default="auto")
    args = ap.parse_args()

    if args.text_file:
        with open(args.text_file, encoding="utf-8") as fh:
            payload = {"text": fh.read()}
        if args.entities:
            payload["entities"] = [e.strip() for e in args.entities.split(",") if e.strip()]
        payload["lang"] = args.lang
    else:
        raw = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
        payload = json.loads(raw)

    out = analyse(payload.get("text", ""),
                  payload.get("entities") or [],
                  payload.get("lang", args.lang))
    sys.stdout.write(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
