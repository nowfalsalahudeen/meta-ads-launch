# `ads.json` reference

Paths are relative to the JSON file unless absolute. A complete working file is `examples/ads.json`.

```json
{
  "brand":  { "name": "Acme Invoices", "parts": ["Acme", "Invoices"], "logo": "assets/logo.svg" },
  "browser_label": "app.acme.example",
  "out": "out",
  "shapes": ["feed", "square", "story", "link"],
  "langs": { "en": { "dir": "ltr", "badge": "FREE EARLY ACCESS", "cta": "Start free · acme.example" } },
  "ads": [ { "id": "launch", "theme": "dark", "headline": { "en": "Get *paid* on time" }, "desktop": {}, "phone": {} } ],
  "page": { "covers": { "en": { "headline": "...", "sub": "...", "desktop": "...", "phone": "..." } } }
}
```

## `brand`

| Key | Meaning |
|---|---|
| `name` | Brand name. |
| `parts` | The wordmark split in two, so the second part takes the accent colour (`["Acme","Invoices"]`). |
| `logo` | SVG or PNG of the mark. Used beside the wordmark and, alone, on the profile picture. |
| `navy`, `slate`, `cyan`, `teal`, `accent` | Optional colours (defaults are a navy, cyan and coral palette). `accent` colours the badge and button. |

## Top level

| Key | Meaning |
|---|---|
| `browser_label` | Text shown in the browser frame's address bar. |
| `out` | Output folder. Images go to `out/<lang>/<shape>/<ad id>.png`; page assets to `out/page/`. |
| `shapes` | Any of `feed` (1080x1350), `square` (1080x1080), `story` (1080x1920), `link` (1200x628). |

## `langs`

One entry per language code you will advertise in.

| Key | Meaning |
|---|---|
| `dir` | `ltr` or `rtl`. `rtl` mirrors the whole layout (Arabic, Hebrew, Urdu). |
| `badge` | The offer pill ("FREE EARLY ACCESS"). Keep it short. |
| `cta` | The button text, usually the action and the address. |

## `ads[]`

| Key | Meaning |
|---|---|
| `id` | File name and the value for `utm_content`. |
| `theme` | `dark` (navy, high contrast) or `light` (white with soft glow). |
| `headline` | Per language. Wrap the accent word in `*stars*`. Two lines work best. |
| `desktop` | Per language: a screenshot of the product in a desktop browser window. |
| `phone` | Per language: a phone screenshot (a tall image, ideally 1320x2868). |
| `cards` | Two floating cards showing the product doing its job: `{ "glyph", "color"?, "title": {lang}, "line": {lang} }`. `color` sets the card icon's background. |
| `features` | Instead of `cards`: a checklist of up to six items, each `{ "<lang>": "label" }`. |

Use `cards` **or** `features` on an ad, not both. A language missing from a field falls back to `en`.

## `page`

`covers.<lang>` makes `out/page/cover-<lang>.png` (1640x924): `headline` (use `\n` for line breaks and `*stars*` for the accent), `sub` (the pill under the headline), and the two screenshots. A square `profile.png` (1080x1080) of the logo is always made with `--page`.

## Command line

```
python3 scripts/make_creatives.py ads.json                   # all ads, languages and shapes
python3 scripts/make_creatives.py ads.json --lang en --only launch
python3 scripts/make_creatives.py ads.json --page            # profile and covers
```

Environment: `CHROME=/path/to/chrome` if Chrome or Chromium is not found automatically.
