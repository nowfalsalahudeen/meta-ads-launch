#!/usr/bin/env python3
"""Ad creatives and Facebook page assets from a JSON config, drawn as HTML and photographed with headless Chrome.

  python3 make_creatives.py /abs/path/to/ads.json            # all ads, all languages, all shapes
  python3 make_creatives.py ads.json --lang en --only launch  # one language, one ad
  python3 make_creatives.py ads.json --page                  # profile picture and cover photos

Needs Google Chrome or Chromium (set CHROME=/path if it is not found) and, for the web fonts, internet access.
Inputs are screenshots of the real product (a desktop browser window and a phone screen) that you captured yourself; nothing is invented.
See templates/ads.example.json for every option. Paths in the config are relative to the config file unless absolute.

Shapes: feed 1080x1350, square 1080x1080, story 1080x1920, link 1200x628. Page: profile 1080x1080, cover 1640x924.
"""
import argparse
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SHAPES = {"feed": (1080, 1350), "square": (1080, 1080), "story": (1080, 1920), "link": (1200, 628)}

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Cairo:wght@600;700;800&family=Inter:wght@500;600&display=swap" rel="stylesheet">'
)


def find_chrome():
    env = os.environ.get("CHROME")
    if env and Path(env).exists():
        return env
    for p in (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ):
        if Path(p).exists():
            return p
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("Chrome or Chromium not found. Install it or set CHROME=/path/to/chrome.")


class Cfg:
    def __init__(self, path):
        self.path = Path(path).resolve()
        self.root = self.path.parent
        self.d = json.loads(self.path.read_text(encoding="utf-8"))
        b = self.d["brand"]
        self.name = b["name"]
        self.parts = b.get("parts") or [b["name"], ""]
        self.navy = b.get("navy", "#0A192F")
        self.slate = b.get("slate", "#1F4068")
        self.cyan = b.get("cyan", "#00B4D8")
        self.teal = b.get("teal", "#2FD3B5")
        self.accent = b.get("accent", "#FF6F61")
        self.logo = self.file(b["logo"])
        self.out = self.file(self.d.get("out", "out"))
        self.langs = self.d["langs"]

    def file(self, p):
        q = Path(p)
        return (q if q.is_absolute() else self.root / q).resolve()

    def uri(self, p):
        return self.file(p).as_uri()


def accent_word(text):
    out, on = "", False
    for part in html.escape(text).split("*"):
        out += f'<span class="word">{part}</span>' if on else part
        on = not on
    return out


def css(c):
    return f"""
*{{box-sizing:border-box;margin:0}}
html,body{{width:var(--w);height:var(--h);overflow:hidden}}
body{{position:relative;background:#fff;font-family:'Poppins','Cairo',sans-serif;color:{c.navy}}}
body.rtl{{font-family:'Cairo','Poppins',sans-serif}}
.glow{{position:absolute;border-radius:50%;filter:blur(var(--blur))}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(rgba(10,25,47,.07) 2px,transparent 2px);background-size:34px 34px;
  -webkit-mask-image:linear-gradient(180deg,#000 0,transparent 55%);mask-image:linear-gradient(180deg,#000 0,transparent 55%)}}
h1{{position:absolute;font-weight:700;line-height:1.12;letter-spacing:-.01em;font-size:var(--hs);text-wrap:balance}}
body.rtl h1{{font-weight:800;line-height:1.3;letter-spacing:0}}
.word{{background:linear-gradient(95deg,{c.slate},{c.cyan});-webkit-background-clip:text;background-clip:text;color:transparent}}
.device{{position:absolute;background:#0f1b2d;box-shadow:0 60px 120px rgba(10,25,47,.35),0 18px 40px rgba(10,25,47,.25),inset 0 0 0 3px #26354c}}
.device img{{display:block;width:100%;height:100%;object-fit:cover;object-position:top;background:#f4f7fb}}
.brand{{position:absolute;display:flex;align-items:center;gap:var(--bg);font-weight:700;font-size:var(--bs);color:{c.navy}}}
.brand img{{width:var(--bl);height:var(--bl)}}
.brand b{{color:{c.accent}}}
.browser{{position:absolute;background:#fff;border-radius:var(--br);overflow:hidden;box-shadow:0 50px 110px rgba(10,25,47,.34),0 14px 34px rgba(10,25,47,.20),0 0 0 2px rgba(10,25,47,.06)}}
.browser .bar{{height:var(--bh);display:flex;align-items:center;gap:var(--bd);padding:0 var(--bp);background:#eef3f9;border-bottom:2px solid #e3eaf2}}
.browser .bar i{{width:var(--bdot);height:var(--bdot);border-radius:50%;background:#c9d4e2}}
.browser .bar span{{margin-inline-start:var(--bd);background:#fff;color:#52627a;font-family:Inter,sans-serif;font-weight:500;font-size:var(--bf);padding:var(--bpad);border-radius:99px}}
.browser img{{display:block;width:100%;object-fit:cover;object-position:top left}}
.pill{{position:absolute;display:inline-flex;align-items:center;background:{c.accent};color:#fff;font-weight:700;letter-spacing:.06em;font-size:var(--ps);padding:var(--pp);border-radius:99px;box-shadow:0 14px 30px rgba(255,111,97,.40)}}
body.rtl .pill{{letter-spacing:0}}
.cta{{position:absolute;display:inline-flex;align-items:center;gap:var(--cg2);background:{c.navy};color:#fff;font-weight:600;font-size:var(--cts);padding:var(--ctp);border-radius:99px;box-shadow:0 22px 44px rgba(10,25,47,.30)}}
.cta b{{display:grid;place-items:center;width:var(--ctc);height:var(--ctc);border-radius:50%;background:{c.accent};font-size:calc(var(--ctc)*.62)}}
.card{{position:absolute;display:flex;align-items:center;gap:var(--kg);padding:var(--kp);background:#fff;border-radius:var(--kr);color:{c.navy};box-shadow:0 30px 60px rgba(10,25,47,.30),0 6px 16px rgba(10,25,47,.14)}}
.card i{{flex:none;display:grid;place-items:center;width:var(--ki);height:var(--ki);border-radius:30%;background:linear-gradient(135deg,{c.teal},{c.cyan});color:#fff;font-style:normal;font-weight:800;font-size:calc(var(--ki)*.55)}}
.card strong{{display:block;font-weight:700;font-size:var(--kt);line-height:1.2}}
.card span{{display:block;color:#52627a;font-weight:500;font-size:var(--ks);margin-top:2px}}
.feat{{position:absolute;display:grid;grid-template-columns:1fr 1fr;gap:var(--fg) calc(var(--fg)*1.6);padding:var(--fp);background:#fff;border-radius:var(--fr);color:{c.navy};box-shadow:0 30px 60px rgba(10,25,47,.30),0 6px 16px rgba(10,25,47,.14)}}
.feat div{{display:flex;align-items:center;gap:calc(var(--fg)*.7);font-weight:700;font-size:var(--ffs);white-space:nowrap}}
.feat i{{flex:none;display:grid;place-items:center;width:var(--fi);height:var(--fi);border-radius:50%;background:linear-gradient(135deg,{c.teal},{c.cyan});color:#fff;font-style:normal;font-weight:800;font-size:calc(var(--fi)*.62)}}
"""


def dark_css(c):
    return f"""
body{{background:radial-gradient(120% 80% at 80% 0%,#12365f 0%,{c.navy} 55%,#07101f 100%)}}
.dots{{background-image:radial-gradient(rgba(255,255,255,.08) 2px,transparent 2px)!important;-webkit-mask-image:linear-gradient(180deg,#000 0,transparent 60%)!important}}
.glow{{opacity:.85}}
h1{{color:#fff}}
.word{{background:linear-gradient(95deg,{c.teal},{c.cyan})!important;-webkit-background-clip:text!important;background-clip:text!important;color:transparent!important}}
.brand{{color:#fff}}
.cta{{background:{c.accent};box-shadow:0 22px 44px rgba(255,111,97,.40)}}
.cta b{{background:#fff;color:{c.accent}}}
.pill{{background:#fff;color:{c.navy};box-shadow:0 14px 30px rgba(0,0,0,.35)}}
"""


def blobs(variant, w, h):
    left = variant % 2 == 0
    return (
        f'<div class="glow" style="width:{w*.8}px;height:{w*.8}px;top:{-h*.05}px;{"left" if left else "right"}:{-w*.35}px;background:rgba(255,111,97,.38)"></div>'
        f'<div class="glow" style="width:{w*.95}px;height:{w*.95}px;top:{h*.28}px;{"right" if left else "left"}:{-w*.5}px;background:rgba(0,180,216,.34)"></div>'
        f'<div class="glow" style="width:{w*.7}px;height:{w*.7}px;bottom:{-h*.12}px;{"left" if left else "right"}:{-w*.2}px;background:rgba(47,211,181,.22)"></div>'
        '<div class="dots"></div>'
    )


def page(c, w, h, rtl, inner, vars_, dark=False):
    v = ";".join(f"--{k}:{val}" for k, val in vars_.items())
    style = css(c) + (dark_css(c) if dark else "")
    return (
        f'<!doctype html><html dir="{"rtl" if rtl else "ltr"}"><head><meta charset="utf-8">{FONTS}'
        f'<style>:root{{--w:{w}px;--h:{h}px;{v}}}{style}</style></head><body class="{"rtl" if rtl else "ltr"}">{inner}</body></html>'
    )


def browser_box(c, off, side, top, width, src, scale, rot=0, label="app.example.com"):
    bh = int(44 * scale)
    return (
        f'<div class="browser" style="top:{top}px;{side}:{off}px;width:{width}px;transform:rotate({rot}deg);'
        f'--br:{int(22*scale)}px;--bh:{bh}px;--bd:{int(8*scale)}px;--bp:{int(18*scale)}px;--bdot:{int(12*scale)}px;--bf:{int(15*scale)}px;--bpad:{int(5*scale)}px {int(16*scale)}px">'
        f'<div class="bar"><i></i><i></i><i></i><span>{html.escape(label)}</span></div><img src="{src}"></div>'
    )


def phone_box(side, off, top, width, src, rot=0, ratio=2868 / 1320):
    pad = int(width * 0.035)
    ph = int((width - 2 * pad) * ratio + 2 * pad)
    return (
        f'<div class="device" style="top:{top}px;{side}:{off}px;width:{width}px;height:{ph}px;border-radius:{int(width*.13)}px;padding:{pad}px;transform:rotate({rot}deg)">'
        f'<img style="border-radius:{int(width*.105)}px" src="{src}"></div>'
    )


def card_box(kind, side, off, top, data, lang, rot=0):
    title = data["title"].get(lang) or data["title"]["en"]
    line = data["line"].get(lang) or data["line"]["en"]
    return (
        f'<div class="card {kind}" style="top:{top}px;{side}:{off}px;transform:rotate({rot}deg)">'
        f'<i{(" style=" + chr(34) + "background:" + data["color"] + chr(34)) if data.get("color") else ""}>{html.escape(data.get("glyph", "✓"))}</i><div><strong>{html.escape(title)}</strong><span>{html.escape(line)}</span></div></div>'
    )


def feature_box(side, off, top, items, lang, rot=0):
    rows = "".join(f'<div><i>✓</i>{html.escape(it.get(lang) or it["en"])}</div>' for it in items)
    return f'<div class="feat" style="top:{top}px;{side}:{off}px;transform:rotate({rot}deg)">{rows}</div>'


# Layout numbers per shape (tuned for 2-line headlines; keep headlines short).
LAYOUT = {
    "feed": dict(m=70, brand_top=62, pill_top=66, h_top=170, cta_top=455, b_top=610, b_w=880, b_scale=1.0, p_off=52, p_top=690, p_w=350,
                 a=(1090, -10), b=(585, 150), feat_top=1050,
                 v={"hs": "88px", "bs": "44px", "bl": "62px", "bg": "16px", "ps": "22px", "pp": "12px 26px", "cts": "30px", "ctp": "18px 34px 18px 18px", "ctc": "46px", "cg2": "16px",
                    "kg": "18px", "kp": "18px 28px 18px 18px", "kr": "28px", "ki": "62px", "kt": "27px", "ks": "21px",
                    "fp": "26px 32px", "fg": "16px", "fr": "28px", "fi": "36px", "ffs": "26px", "blur": "100px"}),
    "square": dict(m=64, brand_top=48, pill_top=52, h_top=140, cta_top=372, b_top=500, b_w=760, b_scale=0.9, p_off=56, p_top=560, p_w=300,
                   a=(880, -10), b=(478, 150), feat_top=830,
                   v={"hs": "72px", "bs": "40px", "bl": "56px", "bg": "14px", "ps": "20px", "pp": "11px 24px", "cts": "27px", "ctp": "16px 30px 16px 16px", "ctc": "42px", "cg2": "14px",
                      "kg": "16px", "kp": "16px 24px 16px 16px", "kr": "24px", "ki": "54px", "kt": "24px", "ks": "18px",
                      "fp": "22px 28px", "fg": "13px", "fr": "24px", "fi": "32px", "ffs": "23px", "blur": "90px"}),
    "story": dict(m=80, brand_top=140, pill_top=146, h_top=290, cta_top=700, b_top=940, b_w=960, b_scale=1.1, p_off=36, p_top=1110, p_w=440,
                  a=(1400, 50), b=(1020, 140), feat_top=1340,
                  v={"hs": "104px", "bs": "50px", "bl": "70px", "bg": "18px", "ps": "26px", "pp": "14px 30px", "cts": "36px", "ctp": "22px 40px 22px 22px", "ctc": "56px", "cg2": "18px",
                     "kg": "20px", "kp": "22px 34px 22px 22px", "kr": "32px", "ki": "74px", "kt": "32px", "ks": "25px",
                     "fp": "30px 38px", "fg": "20px", "fr": "32px", "fi": "42px", "ffs": "31px", "blur": "120px"}),
}


def ad_html(c, ad, lang, shape):
    L = c.langs[lang]
    rtl = L.get("dir") == "rtl"
    w, h = SHAPES[shape]
    start, end = ("right", "left") if rtl else ("left", "right")
    flip = -1 if rtl else 1
    head = accent_word(ad["headline"].get(lang) or ad["headline"]["en"])
    d_src = c.uri(ad["desktop"].get(lang) or ad["desktop"]["en"])
    p_src = c.uri(ad["phone"].get(lang) or ad["phone"]["en"])
    cards = ad.get("cards")
    feats = ad.get("features")
    dark = ad.get("theme") == "dark"
    label = c.d.get("browser_label", "app.example.com")
    logo = c.logo.as_uri()
    brand = f'<img src="{logo}"><span>{html.escape(c.parts[0])}<b>{html.escape(c.parts[1])}</b></span>'
    inner = blobs(1 if shape != "story" else 0, w, h)
    if shape == "link":
        m = 56
        inner += f'<div class="brand" style="top:42px;{start}:{m}px">{brand}</div>'
        inner += f'<div class="pill" style="top:178px;{start}:{m}px">{html.escape(L["badge"])}</div>'
        inner += f'<h1 style="top:238px;{start}:{m}px;width:520px;text-align:{start}">{head}</h1>'
        inner += f'<div class="cta" style="top:508px;{start}:{m}px"><b>→</b>{html.escape(L["cta"])}</div>'
        inner += browser_box(c, 40, end, 78, 640, d_src, 0.8, rot=-2 * flip, label=label)
        inner += phone_box(end, 24, 300, 220, p_src, rot=3 * flip)
        if feats:
            inner += feature_box(end, 330, 440, feats, lang, rot=-2 * flip)
        elif cards:
            inner += card_box("a", end, 330, 470, cards[0], lang, rot=-2 * flip)
        v = {"hs": "54px", "bs": "34px", "bl": "48px", "bg": "12px", "ps": "16px", "pp": "8px 18px", "cts": "24px", "ctp": "12px 26px 12px 12px", "ctc": "36px", "cg2": "12px",
             "kg": "12px", "kp": "11px 18px 11px 11px", "kr": "18px", "ki": "38px", "kt": "17px", "ks": "13px",
             "fp": "14px 18px", "fg": "9px", "fr": "16px", "fi": "22px", "ffs": "15px", "blur": "80px"}
    else:
        Y = LAYOUT[shape]
        m = Y["m"]
        inner += f'<div class="brand" style="top:{Y["brand_top"]}px;{start}:{m}px">{brand}</div>'
        inner += f'<div class="pill" style="top:{Y["pill_top"]}px;{end}:{m}px">{html.escape(L["badge"])}</div>'
        inner += f'<h1 style="top:{Y["h_top"]}px;{start}:{m}px;{end}:{m}px;text-align:{start}">{head}</h1>'
        inner += f'<div class="cta" style="top:{Y["cta_top"]}px;{start}:{m}px"><b>→</b>{html.escape(L["cta"])}</div>'
        inner += browser_box(c, m if shape != "story" else 60, start, Y["b_top"], Y["b_w"], d_src, Y["b_scale"], rot=-2 * flip, label=label)
        inner += phone_box(end, Y["p_off"], Y["p_top"], Y["p_w"], p_src, rot=3 * flip)
        if feats:
            inner += feature_box(start, (m - 10) if shape != "story" else 50, Y["feat_top"], feats, lang, rot=-2 * flip)
        elif cards:
            inner += card_box("a", start, (m - 10) if shape != "story" else Y["a"][1], Y["a"][0], cards[0], lang, rot=-2 * flip)
            if len(cards) > 1:
                inner += card_box("b", end, (m + 150) if shape != "story" else Y["b"][1], Y["b"][0], cards[1], lang, rot=2 * flip)
        v = Y["v"]
    full = {**v, "ep": "10px", "es": "20px", "ci": "40px"}
    return page(c, w, h, rtl, inner, full, dark=dark), (w, h)


def page_assets(c):
    out = []
    d = c.d.get("page")
    if not d:
        sys.exit('Add a "page" block to the config (see templates/ads.example.json).')
    # profile: the mark only, centred, inside the circle-safe middle 60%
    w = h = 1080
    mark = 560
    inner = (
        '<div class="glow" style="width:760px;height:760px;top:-260px;left:-240px;background:rgba(255,111,97,.45)"></div>'
        '<div class="glow" style="width:820px;height:820px;bottom:-320px;right:-260px;background:rgba(0,180,216,.45)"></div>'
        '<div class="glow" style="width:520px;height:520px;top:300px;right:-200px;background:rgba(47,211,181,.25)"></div><div class="dots"></div>'
        f'<img src="{c.logo.as_uri()}" style="position:absolute;width:{mark}px;height:{mark}px;left:{(w-mark)//2}px;top:{(h-mark)//2}px;filter:drop-shadow(0 12px 24px rgba(0,0,0,.25))">'
    )
    out.append(("profile.png", page(c, w, h, False, inner, {"blur": "90px", "ep": "0", "es": "0"}, dark=True), (w, h)))
    # cover per language: text and devices stay inside y 160..770
    for lang, cv in d.get("covers", {}).items():
        L = c.langs[lang]
        rtl = L.get("dir") == "rtl"
        start, end = ("right", "left") if rtl else ("left", "right")
        flip = -1 if rtl else 1
        w, h = 1640, 924
        headline = "<br>".join(accent_word(x) for x in cv["headline"].split("\n"))
        d_src, p_src = c.uri(cv["desktop"]), c.uri(cv["phone"])
        logo = c.logo.as_uri()
        brand = f'<img src="{logo}"><span>{html.escape(c.parts[0])}<b>{html.escape(c.parts[1])}</b></span>'
        inner = blobs(0, w, h)
        inner += f'<div class="brand" style="top:178px;{start}:150px">{brand}</div>'
        inner += f'<h1 style="top:290px;{start}:150px;width:680px;text-align:{start}">{headline}</h1>'
        inner += f'<div class="pill" style="top:700px;{start}:150px;background:#fff;color:{c.navy}">{html.escape(cv["sub"])}</div>'
        inner += browser_box(c, 90, end, 215, 640, d_src, 0.85, rot=-2 * flip, label=c.d.get("browser_label", "app.example.com"))
        inner += phone_box(end, 40, 265, 235, p_src, rot=3 * flip)
        v = {"hs": "60px", "bs": "40px", "bl": "58px", "bg": "16px", "ps": "20px", "pp": "10px 26px", "blur": "110px", "ep": "10px", "es": "20px"}
        out.append((f"cover-{lang}.png", page(c, w, h, rtl, inner, v, dark=True), (w, h)))
    return out


def shoot(chrome, html_text, size, dest, tmp):
    dest.parent.mkdir(parents=True, exist_ok=True)
    f = Path(tmp) / (dest.stem + "_" + dest.parent.name + ".html")
    f.write_text(html_text, encoding="utf-8")
    w, h = size
    subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", f"--window-size={w},{h}",
         "--force-device-scale-factor=1", "--virtual-time-budget=12000", f"--screenshot={dest}", f.as_uri()],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--lang")
    ap.add_argument("--only", help="ad id")
    ap.add_argument("--page", action="store_true", help="profile picture and covers instead of ads")
    a = ap.parse_args()
    c = Cfg(a.config)
    chrome = find_chrome()
    with tempfile.TemporaryDirectory() as tmp:
        if a.page:
            for name, t, size in page_assets(c):
                shoot(chrome, t, size, c.out / "page" / name, tmp)
                print("wrote", c.out / "page" / name)
            return
        shapes = c.d.get("shapes", list(SHAPES))
        for lang in c.langs:
            if a.lang and lang != a.lang:
                continue
            for shape in shapes:
                for ad in c.d["ads"]:
                    if a.only and ad["id"] != a.only:
                        continue
                    t, size = ad_html(c, ad, lang, shape)
                    dest = c.out / lang / shape / f'{ad["id"]}.png'
                    shoot(chrome, t, size, dest, tmp)
            print("done", lang)


if __name__ == "__main__":
    main()
