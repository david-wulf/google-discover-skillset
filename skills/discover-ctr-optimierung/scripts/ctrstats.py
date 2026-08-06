#!/usr/bin/env python3
"""
ctrstats.py — Rechen-Backend fuer den Skill discover-ctr-optimierung.

Beantwortet die Fragen, die in CTR-Diskussionen fast immer uebersprungen werden:

  ci         Wie genau ist diese CTR ueberhaupt? (Wilson-Konfidenzintervall)
  compare    Ist der Unterschied zwischen zwei Zeitraeumen echt oder Rauschen?
             (Zwei-Stichproben-z-Test fuer Anteile)
  power      Wie viele Impressionen brauche ich, um eine Verbesserung von x %
             ueberhaupt nachweisen zu koennen?
  mde        Welche Verbesserung kann ich bei diesem Impressionsvolumen
             ueberhaupt erkennen? (minimal detektierbarer Effekt)

Der Grund fuer dieses Skript: Eine CTR-Aenderung von 6,2 % auf 6,8 % bei 800
Impressionen ist statistisch nicht unterscheidbar von Zufall. Wer daraus eine
Massnahme ableitet, optimiert auf Rauschen. Discover erlaubt keinen echten
A/B-Test — man kann nur aendern und beobachten. Deshalb muss man wenigstens
wissen, ob die beobachtete Differenz etwas bedeutet.

Aufruf:
    python ctrstats.py ci --clicks 412 --impressions 8300
    python ctrstats.py compare --before 412/8300 --after 388/6900
    python ctrstats.py power --baseline-ctr 0.062 --uplift-rel 0.15
    python ctrstats.py mde --impressions 8300 --baseline-ctr 0.062
    python ctrstats.py benchmark --clicks 412 --impressions 8300 --typ non-news

Nur Standardbibliothek.
"""

import argparse
import json
import math
import sys

# Zweiseitig alpha = 0.05, Power = 0.80
Z_ALPHA_2 = 1.959963985
Z_BETA_80 = 0.841621234

# Beobachtete Discover-CTR-Bandbreiten aus einer GSC-Auswertung ueber
# 11.000 URLs von 62 Domains ueber 12 Monate. Referenzwerte, keine Zielvorgabe
# von Google.
BENCHMARKS = {
    "news": {"mittel": 0.11, "label": "News-Seiten"},
    "non-news": {"mittel": 0.06, "label": "Non-News"},
}
ZIELBAND = (0.07, 0.09)     # Arbeitsziel
HANDLUNGSSIGNAL = 0.05      # darunter besteht Handlungsbedarf


def phi(x):
    """Standardnormalverteilung, kumulativ."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def wilson(clicks, impressions, z=Z_ALPHA_2):
    """Wilson-Score-Intervall.

    Bei kleinen Klickzahlen deutlich verlaesslicher als das
    Normalapproximations-Intervall, das dort negative Untergrenzen liefert.
    """
    if impressions <= 0:
        return None
    p = clicks / impressions
    d = 1 + z * z / impressions
    center = (p + z * z / (2 * impressions)) / d
    margin = (z / d) * math.sqrt(p * (1 - p) / impressions
                                 + z * z / (4 * impressions * impressions))
    return max(0.0, center - margin), min(1.0, center + margin)


def parse_pair(s, name):
    """Nimmt 'klicks/impressionen' entgegen."""
    try:
        a, b = s.split("/")
        return int(a), int(b)
    except Exception:
        raise SystemExit("%s muss die Form klicks/impressionen haben, z.B. 412/8300" % name)


def cmd_ci(args):
    c, n = args.clicks, args.impressions
    if n <= 0:
        raise SystemExit("impressions muss groesser 0 sein")
    p = c / n
    lo, hi = wilson(c, n)
    halbbreite = (hi - lo) / 2
    # Ab wann ist die Schaetzung brauchbar? Faustregel: Halbbreite unter einem
    # Fuenftel des Punktschaetzers.
    belastbar = halbbreite < p / 5 if p > 0 else False
    return {
        "clicks": c,
        "impressions": n,
        "ctr": round(p, 5),
        "ctr_pct": round(p * 100, 2),
        "ci95_pct": [round(lo * 100, 2), round(hi * 100, 2)],
        "ci95_halbbreite_pp": round(halbbreite * 100, 2),
        "belastbar": belastbar,
        "lesart": ("Punktschaetzer belastbar" if belastbar else
                   "Intervall zu breit — die CTR ist bei diesem Volumen nur grob bestimmt; "
                   "keine Massnahme auf Zehntel-Prozentpunkte stuetzen"),
    }


def cmd_compare(args):
    c1, n1 = parse_pair(args.before, "--before")
    c2, n2 = parse_pair(args.after, "--after")
    if n1 <= 0 or n2 <= 0:
        raise SystemExit("Impressionen muessen groesser 0 sein")
    p1, p2 = c1 / n1, c2 / n2
    pool = (c1 + c2) / (n1 + n2)
    se = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
    if se == 0:
        raise SystemExit("Standardfehler 0 — Daten pruefen")
    z = (p2 - p1) / se
    pval = 2 * (1 - phi(abs(z)))
    lo1, hi1 = wilson(c1, n1)
    lo2, hi2 = wilson(c2, n2)
    return {
        "vorher": {"clicks": c1, "impressions": n1, "ctr_pct": round(p1 * 100, 2),
                   "ci95_pct": [round(lo1 * 100, 2), round(hi1 * 100, 2)]},
        "nachher": {"clicks": c2, "impressions": n2, "ctr_pct": round(p2 * 100, 2),
                    "ci95_pct": [round(lo2 * 100, 2), round(hi2 * 100, 2)]},
        "differenz_pp": round((p2 - p1) * 100, 2),
        "differenz_relativ_pct": round((p2 / p1 - 1) * 100, 1) if p1 > 0 else None,
        "z": round(z, 3),
        "p_wert": round(pval, 4),
        "signifikant_alpha_5pct": pval < 0.05,
        "intervalle_ueberlappen": not (hi1 < lo2 or hi2 < lo1),
        "lesart": ("Unterschied statistisch belegbar (p < 0,05)" if pval < 0.05 else
                   "Unterschied nicht von Zufall unterscheidbar — keine Massnahme darauf stuetzen"),
        "warnung_kein_ab_test": (
            "Discover erlaubt keinen echten A/B-Test. Zwei Zeitraeume sind nicht randomisiert: "
            "Freshness-Verfall, andere Kohorten, Saisonalitaet und Wettbewerb wirken mit. Ein "
            "signifikanter Unterschied belegt eine Veraenderung, nicht deren Ursache."),
    }


def sample_size(p1, p2):
    """Impressionen pro Variante fuer alpha=0.05 zweiseitig, Power 0.80."""
    if p1 == p2:
        return None
    pbar = (p1 + p2) / 2
    num = (Z_ALPHA_2 * math.sqrt(2 * pbar * (1 - pbar))
           + Z_BETA_80 * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(num / (p2 - p1) ** 2)


def cmd_power(args):
    p1 = args.baseline_ctr
    if not (0 < p1 < 1):
        raise SystemExit("--baseline-ctr als Anteil angeben, z.B. 0.062")
    p2 = p1 * (1 + args.uplift_rel)
    if p2 >= 1:
        raise SystemExit("Ziel-CTR ueber 100 Prozent — uplift-rel pruefen")
    n = sample_size(p1, p2)
    out = {
        "baseline_ctr_pct": round(p1 * 100, 2),
        "ziel_ctr_pct": round(p2 * 100, 2),
        "uplift_relativ_pct": round(args.uplift_rel * 100, 1),
        "uplift_absolut_pp": round((p2 - p1) * 100, 2),
        "impressionen_pro_variante": n,
        "impressionen_gesamt": n * 2,
        "annahmen": "alpha 0,05 zweiseitig, Power 0,80",
    }
    if args.impressions_per_day:
        tage = math.ceil(n / args.impressions_per_day)
        out["tage_pro_variante"] = tage
        out["tage_gesamt_sequenziell"] = tage * 2
        out["freshness_konflikt"] = tage > 7
        out["lesart_zeit"] = (
            "Messfenster laenger als eine Woche: der Freshness-Verfall ueberlagert den Effekt. "
            "Bei sequenzieller Messung ist das Ergebnis dann nicht mehr sauber der Aenderung "
            "zuzuordnen — auf mehrere Artikel gleichzeitig ausweichen."
            if tage > 7 else
            "Messfenster liegt innerhalb der Woche mit hoher Freshness-Gewichtung.")
    return out


def cmd_mde(args):
    """Kleinster relativer Uplift, der bei gegebenem Volumen nachweisbar ist."""
    p1 = args.baseline_ctr
    n = args.impressions
    if not (0 < p1 < 1) or n <= 0:
        raise SystemExit("baseline-ctr als Anteil und impressions groesser 0 angeben")
    lo, hi = 0.0001, 5.0
    for _ in range(80):
        mid = (lo + hi) / 2
        need = sample_size(p1, p1 * (1 + mid))
        if need is None or need > n:
            lo = mid
        else:
            hi = mid
    mde = hi
    return {
        "impressionen_pro_variante": n,
        "baseline_ctr_pct": round(p1 * 100, 2),
        "mde_relativ_pct": round(mde * 100, 1),
        "mde_absolut_pp": round(p1 * mde * 100, 2),
        "nachweisbare_ziel_ctr_pct": round(p1 * (1 + mde) * 100, 2),
        "lesart": ("Bei diesem Volumen sind nur Verbesserungen ab %.0f Prozent relativ "
                   "nachweisbar. Kleinere Aenderungen bleiben im Rauschen — sie koennen "
                   "trotzdem richtig sein, nur nicht belegbar." % (mde * 100)),
    }


def cmd_benchmark(args):
    c, n = args.clicks, args.impressions
    if n <= 0:
        raise SystemExit("impressions muss groesser 0 sein")
    p = c / n
    lo, hi = wilson(c, n)
    bm = BENCHMARKS[args.typ]
    if p < HANDLUNGSSIGNAL:
        band = "unter Handlungssignal (5 %)"
    elif p < ZIELBAND[0]:
        band = "unter dem Arbeitsziel (7–9 %)"
    elif p <= ZIELBAND[1]:
        band = "im Arbeitsziel (7–9 %)"
    else:
        band = "ueber dem Arbeitsziel"
    # Ist der Abstand zum Referenzwert bei diesem Volumen ueberhaupt belegt?
    ref = bm["mittel"]
    unterschied_belegt = hi < ref or lo > ref
    return {
        "ctr_pct": round(p * 100, 2),
        "ci95_pct": [round(lo * 100, 2), round(hi * 100, 2)],
        "referenz": bm["label"],
        "referenz_ctr_pct": round(ref * 100, 1),
        "band": band,
        "abstand_zur_referenz_pp": round((p - ref) * 100, 2),
        "abstand_belegt": unterschied_belegt,
        "lesart": ("Der Abstand zum Referenzwert ist bei diesem Volumen belegt."
                   if unterschied_belegt else
                   "Das Konfidenzintervall schliesst den Referenzwert ein — die Domain liegt "
                   "statistisch nicht nachweisbar darunter oder darueber."),
        "hinweis_referenz": ("Referenzwerte aus einer GSC-Auswertung ueber 11.000 URLs von "
                             "62 Domains ueber 12 Monate. Beobachtung, keine Google-Zielvorgabe. "
                             "Discover-CTR ist nicht mit Search-CTR vergleichbar: Discover zaehlt "
                             "eine Impression erst bei sichtbarer Karte."),
    }


def main():
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("ci", help="CTR mit Konfidenzintervall")
    a.add_argument("--clicks", type=int, required=True)
    a.add_argument("--impressions", type=int, required=True)

    b = sub.add_parser("compare", help="zwei Zeitraeume vergleichen")
    b.add_argument("--before", required=True, help="klicks/impressionen")
    b.add_argument("--after", required=True, help="klicks/impressionen")

    c = sub.add_parser("power", help="benoetigte Impressionen fuer einen Uplift")
    c.add_argument("--baseline-ctr", type=float, required=True, help="Anteil, z.B. 0.062")
    c.add_argument("--uplift-rel", type=float, required=True, help="relativ, z.B. 0.15 fuer +15 %%")
    c.add_argument("--impressions-per-day", type=int)

    d = sub.add_parser("mde", help="nachweisbarer Effekt bei gegebenem Volumen")
    d.add_argument("--impressions", type=int, required=True)
    d.add_argument("--baseline-ctr", type=float, required=True)

    e = sub.add_parser("benchmark", help="gegen die beobachteten Bandbreiten einordnen")
    e.add_argument("--clicks", type=int, required=True)
    e.add_argument("--impressions", type=int, required=True)
    e.add_argument("--typ", choices=sorted(BENCHMARKS), default="non-news")

    args = ap.parse_args()
    fn = {"ci": cmd_ci, "compare": cmd_compare, "power": cmd_power,
          "mde": cmd_mde, "benchmark": cmd_benchmark}[args.cmd]
    sys.stdout.write(json.dumps(fn(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
