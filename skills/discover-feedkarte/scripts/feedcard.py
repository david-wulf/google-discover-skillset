#!/usr/bin/env python3
"""
feedcard.py — Mess- und Render-Backend fuer den Skill discover-feedkarte.

Ein Discover-Titelbild wird nicht in Originalgroesse gesehen, sondern als
Feed-Karte von rund 340 x 190 Punkten. Ob ein Motiv dort noch lesbar ist, laesst
sich am 1200-px-Original nicht beurteilen. Dieses Skript misst das Bild und
erzeugt genau die Ansichten, in denen es tatsaechlich wahrgenommen wird — die
danach visuell bewertet werden.

Aufruf:
    python feedcard.py --image <pfad-oder-url> [--out <verzeichnis>]

Ausgabe: JSON auf stdout (Messwerte + Pfade der erzeugten Ansichten).
Benoetigt Pillow. Ohne Pillow bricht das Skript mit klarer Meldung ab; der Skill
arbeitet dann im eingeschraenkten Modus weiter.
"""

import argparse
import json
import math
import os
import sys
import urllib.request
from fractions import Fraction

try:
    from PIL import Image, ImageFilter, ImageStat
except ImportError:
    sys.stderr.write(
        "Pillow fehlt. Installation: pip install pillow\n"
        "Ohne Pillow entfaellt der Thumbnail-Test; das Bild kann nur in "
        "Originalgroesse beurteilt werden.\n")
    sys.exit(2)

# Discover-Kartenformate. Die Werte sind Groessenordnungen der ausgelieferten
# Karten, keine von Google dokumentierten Spezifikationen.
FEED_CARD = (340, 190)      # grosse Karte im Feed
COMPACT_SQUARE = (80, 80)   # kompakte Listenansicht
MIN_WIDTH = 1200            # Mindestbreite fuer die grosse Karte

COMMON_RATIOS = {
    "16:9": 16 / 9, "4:3": 4 / 3, "3:2": 3 / 2, "1:1": 1.0,
    "21:9": 21 / 9, "5:4": 5 / 4, "2:1": 2.0, "9:16": 9 / 16, "2:3": 2 / 3,
}


def fetch(src, out_dir):
    """Laedt eine URL herunter oder gibt einen lokalen Pfad zurueck."""
    if not src.lower().startswith(("http://", "https://")):
        if not os.path.isfile(src):
            raise SystemExit("Bilddatei nicht gefunden: %s" % src)
        return src, None
    name = os.path.basename(src.split("?")[0]) or "titelbild"
    if "." not in name:
        name += ".img"
    target = os.path.join(out_dir, "original_" + name)
    req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp, open(target, "wb") as fh:
        fh.write(resp.read())
    return target, src


def closest_ratio(w, h):
    r = w / h
    best = min(COMMON_RATIOS, key=lambda k: abs(COMMON_RATIOS[k] - r))
    dev = abs(COMMON_RATIOS[best] - r) / COMMON_RATIOS[best]
    exact = str(Fraction(w, h).limit_denominator(50)).replace("/", ":")
    return {"measured": round(r, 3), "closest": best,
            "deviation_pct": round(dev * 100, 1), "exact": exact}


def cover_crop(im, size):
    """Skaliert und beschneidet wie eine CSS-Regel object-fit: cover."""
    tw, th = size
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = max(1, round(sw * scale)), max(1, round(sh * scale))
    resized = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def center_crop_ratio(im, ratio=16 / 9):
    """Mittiger Beschnitt auf ein Zielverhaeltnis — zeigt, was wegfaellt."""
    w, h = im.size
    if w / h > ratio:
        nw, nh = round(h * ratio), h
    else:
        nw, nh = w, round(w / ratio)
    left, top = (w - nw) // 2, (h - nh) // 2
    return im.crop((left, top, left + nw, top + nh))


def edge_density(im):
    """Mittlere Kantenenergie. Nur innerhalb derselben Auflaesung vergleichbar."""
    g = im.convert("L").filter(ImageFilter.FIND_EDGES)
    return round(ImageStat.Stat(g).mean[0] / 255, 4)


def detail_loss(im):
    """Wie viel Bildinformation die Feed-Groesse kostet.

    Verfahren: Das Original wird auf die Kartengeometrie beschnitten, auf
    340 x 190 verkleinert und wieder auf die Ausgangsgroesse gebracht. Die
    RMS-Abweichung zum Original ist der Informationsverlust.

    Ein Vergleich der mittleren Kantendichte vor und nach dem Verkleinern waere
    hier falsch: beim Verkleinern steigt die Kantendichte, weil Kanten einen
    groesseren Anteil der Flaeche einnehmen. Die Werte sind ueber
    unterschiedliche Auflaesungen nicht vergleichbar.
    """
    tw, th = FEED_CARD
    ref = center_crop_ratio(im, tw / th)
    if ref.width < tw:
        ref = ref.resize((tw, th), Image.LANCZOS)
    small = ref.resize((tw, th), Image.LANCZOS)
    back = small.resize(ref.size, Image.LANCZOS)
    a, b = ref.convert("L"), back.convert("L")
    from PIL import ImageChops
    rms = ImageStat.Stat(ImageChops.difference(a, b)).rms[0]
    ref_sd = ImageStat.Stat(a).stddev[0] or 1.0
    return {
        "rms_difference": round(rms, 2),
        "loss_pct_of_range": round(rms / 255 * 100, 2),
        "loss_relative_to_contrast": round(rms / ref_sd, 3),
        # Der Wert misst Pixelinformation, nicht Bildaussage. Feine Textur
        # (Zellstruktur eines Solarmoduls, Blattwerk) erzeugt denselben Verlust
        # wie verschwindende Schrift. Er ist deshalb ein Pruefauftrag, kein
        # Urteil — entschieden wird an der gerenderten Kartenansicht.
        "reading": ("hoher Verlust — an der Kartenansicht pruefen, ob die "
                    "Bildaussage betroffen ist oder nur Textur"
                    if rms / 255 * 100 > 6 else
                    "mittlerer Verlust — Kartenansicht pruefen"
                    if rms / 255 * 100 > 2 else
                    "grossflaechiges Motiv — uebersteht Feed-Groesse"),
    }


def colorfulness(im):
    """Hasler-Suesstrunk-Farbigkeit, ohne numpy, auf verkleinerter Kopie."""
    small = im.convert("RGB").resize((160, 160), Image.BILINEAR)
    # tobytes() ist versionsstabil — getdata() ist ab Pillow 14 entfernt und
    # get_flattened_data() liefert je nach Version ein anderes Format.
    raw = small.tobytes()
    n = len(raw) // 3
    rg, yb = [], []
    for i in range(0, n * 3, 3):
        r, g, b = raw[i], raw[i + 1], raw[i + 2]
        rg.append(r - g)
        yb.append(0.5 * (r + g) - b)

    def mean_std(v):
        m = sum(v) / n
        var = sum((x - m) ** 2 for x in v) / n
        return m, math.sqrt(var)

    m_rg, s_rg = mean_std(rg)
    m_yb, s_yb = mean_std(yb)
    return round(math.sqrt(s_rg ** 2 + s_yb ** 2)
                 + 0.3 * math.sqrt(m_rg ** 2 + m_yb ** 2), 1)


def luminance_stats(im):
    g = im.convert("L")
    st = ImageStat.Stat(g)
    hist = g.histogram()
    total = sum(hist) or 1
    return {
        "mean_brightness": round(st.mean[0], 1),
        "rms_contrast": round(st.stddev[0], 1),
        "clipped_black_pct": round(sum(hist[:8]) / total * 100, 1),
        "clipped_white_pct": round(sum(hist[248:]) / total * 100, 1),
    }


def analyse(src, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    path, source_url = fetch(src, out_dir)
    filesize = os.path.getsize(path)

    with Image.open(path) as raw:
        fmt, mode = raw.format, raw.mode
        animated = getattr(raw, "n_frames", 1) > 1
        im = raw.convert("RGB")
        w, h = im.size

        views = {}
        card = cover_crop(im, FEED_CARD)
        p = os.path.join(out_dir, "ansicht_feedkarte_340x190.png")
        card.save(p)
        views["feed_card"] = p

        square = cover_crop(im, COMPACT_SQUARE)
        p = os.path.join(out_dir, "ansicht_kompakt_80x80.png")
        square.save(p)
        views["compact_square"] = p

        crop = center_crop_ratio(im)
        p = os.path.join(out_dir, "ansicht_crop_16zu9.png")
        crop.copy().resize((min(1200, crop.width),
                            round(min(1200, crop.width) / (16 / 9))),
                           Image.LANCZOS).save(p)
        views["crop_16x9"] = p

        result = {
            "source": source_url or path,
            "local_path": path,
            "file": {
                "format": fmt,
                "mode": mode,
                "animated": animated,
                "bytes": filesize,
                "kilobytes": round(filesize / 1024, 1),
            },
            "dimensions": {
                "width": w,
                "height": h,
                "megapixels": round(w * h / 1e6, 2),
                "meets_min_width_1200": w >= MIN_WIDTH,
                "width_shortfall": max(0, MIN_WIDTH - w),
                "aspect_ratio": closest_ratio(w, h),
            },
            "crop_loss_16x9": {
                "cropped_pixels_pct": round(
                    (1 - (crop.width * crop.height) / (w * h)) * 100, 1),
                # Zu breites Bild verliert an den Seiten, zu hohes oben und unten.
                "cropped_edge": "links und rechts" if w / h > 16 / 9 else
                                ("oben und unten" if w / h < 16 / 9 else "keiner"),
            },
            "luminance": luminance_stats(im),
            "colorfulness_hasler_suesstrunk": colorfulness(im),
            "detail": detail_loss(im),
            "edge_density_original": edge_density(im),
            "views": views,
        }

    # Automatische Hinweise — ersetzen keine visuelle Bewertung, machen aber
    # die Messwerte im Bericht zitierfaehig.
    flags = []
    d = result["dimensions"]
    if not d["meets_min_width_1200"]:
        flags.append("Breite %d px unter 1200 px — grosse Feed-Karte "
                     "entfaellt (fehlen %d px)" % (d["width"], d["width_shortfall"]))
    if d["aspect_ratio"]["closest"] != "16:9" and \
            d["aspect_ratio"]["deviation_pct"] > 8:
        flags.append("Seitenverhaeltnis %s weicht von 16:9 ab — beim Beschnitt "
                     "gehen %.1f %% der Flaeche %s verloren"
                     % (d["aspect_ratio"]["exact"],
                        result["crop_loss_16x9"]["cropped_pixels_pct"],
                        result["crop_loss_16x9"]["cropped_edge"]))
    if result["file"]["format"] == "PNG" and result["file"]["kilobytes"] > 300:
        flags.append("PNG mit %.0f KB — als WebP oder JPEG deutlich kleiner, "
                     "ohne sichtbaren Verlust" % result["file"]["kilobytes"])
    if result["luminance"]["rms_contrast"] < 40:
        flags.append("RMS-Kontrast %.1f ist niedrig — flaue Bilder verlieren im "
                     "Feed gegen kontraststarke Nachbarkarten"
                     % result["luminance"]["rms_contrast"])
    if result["colorfulness_hasler_suesstrunk"] < 15:
        flags.append("Farbigkeit %.1f ist sehr gering — wirkt im Feed "
                     "unauffaellig" % result["colorfulness_hasler_suesstrunk"])
    if result["detail"]["loss_pct_of_range"] > 6:
        flags.append("Informationsverlust bei Feed-Groesse %.1f %% — "
                     "Kartenansicht pruefen: betrifft der Verlust die "
                     "Bildaussage (Schrift, Kernmotiv) oder nur Textur? Nur der "
                     "erste Fall ist ein Mangel"
                     % result["detail"]["loss_pct_of_range"])
    if result["file"]["animated"]:
        flags.append("Animierte Datei — Discover zeigt nur das erste Bild")
    result["automatic_flags"] = flags
    return result


def main():
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, help="Bildpfad oder Bild-URL")
    ap.add_argument("--out", default="feedkarte-ansichten",
                    help="Verzeichnis fuer die erzeugten Ansichten")
    args = ap.parse_args()
    sys.stdout.write(json.dumps(analyse(args.image, args.out),
                                ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
