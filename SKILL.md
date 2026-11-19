---
name: meta-ads-launch
description: Plan, build and teach the launch of a small-budget Meta (Facebook and Instagram) ad test for any app, SaaS or small-business product that has a website and a web app. Produces ad creatives (feed, square, story and link shapes, in any languages including right-to-left), a Facebook page profile picture and cover, Meta Pixel and sign-up tracking, ad copy, and a one-step-at-a-time campaign walkthrough for a first-time advertiser. Use when asked to "run ads", "set up Meta ads", "make social ads", "add the Meta pixel", "teach me to advertise", or to prepare an ad test on a small budget.
---

# meta-ads-launch

Takes a product that already has a website and a web app, and gets a first Meta ad test live on a small budget: accounts, tracking, creatives, copy, the campaign build, and how to read the result. Written for someone who has never run an ad, and reusable for any product in any market.

**You prepare everything; the user presses every button that spends money or accepts terms.** Never enter payment details, accept Meta terms, publish a campaign or raise a budget yourself. Walk the user through those screens, one step at a time, and ask for a screenshot before the next step.

## Workflow

1. **Inspect, never invent.** Read the product's site and app for what it really does, what is free, its URLs, its privacy page, the languages and currency it supports, and whether it has screens to show. Ads may only say what the product does today: no prices before paid plans exist, no "available on the store" for an app that is not published, no invented numbers, testimonials or guarantees.
2. **Ask what changes the plan** (one message): who the buyer is and where (country, language or languages); the budget for the first test; whether a Facebook page, an Instagram account and a Meta Business account already exist. Defaults if the user does not know: the product's main market, its main language plus one more if it supports it, about USD 25 a day for two days, nothing exists yet.
3. **Accounts** (`references/campaign-walkthrough.md` Part 1): Facebook page, an Instagram account separate from the user's personal one, Meta Business account, ad account currency, payment method. The user does these.
4. **Tracking** (`references/tracking.md`): add the Meta Pixel to the site and the web app, with a sign-up event and a "first real use" event. Keep the pixel id in one config value; empty means off and nothing is sent. Update the privacy page. Verify in a real browser that the requests go out, then have the user confirm in Events Manager -> Test events (the Website section, not the Server one).
5. **Creatives** (`scripts/make_creatives.py`, `references/creative-specs.md`): one hook headline per ad, an offer badge, one button, the product on a browser and a phone, and either two small floating cards or one feature checklist. Make every placement shape (feed 4:5, square 1:1, story 9:16, link 1.91:1) in each language. Look at the outputs yourself before handing them over.
6. **Page assets** (`make_creatives.py --page`): profile picture 1080x1080 (circle-safe) and a cover 1640x924 with the content kept in the middle band.
7. **Copy** (`templates/copy.md`): primary text, headline, description, call-to-action and a tracking link with UTM tags, in each language.
8. **Build the campaign with the user, one step at a time** (`references/campaign-walkthrough.md` Parts 2-5). The first test is the Traffic objective, manual (not Advantage+) setup, ad-set budget, one ad set per language, one to three ads, AI image generation and enhancements OFF, a separate correctly sized image for each placement, and a two-day schedule.
9. **Read the result** (`references/campaign-walkthrough.md` Part 6): impressions, CTR, cost per click and landing-page views after 24-48 hours; pause the weakest; do not judge sign-ups until there are enough. Move to a sign-up campaign only after roughly 50 sign-up events in a week, then add retargeting.

## Rules

- **Beginner mode:** when the user says they are confused or asks for "one by one", give at most four small steps, say exactly what to click and what to type, and stop for a screenshot. Name the screen they are on from their screenshot before giving steps.
- **Honesty:** state what is verified (you saw it) and what is not (rules, prices and costs quoted from third-party articles). Cost per click, special-category rules and local advertiser permits must be checked on the official source before spending; say so (`references/compliance.md`).
- **Privacy:** keep the pixel id, emails, account ids and any company data out of the skill, the creatives' file names and any repo. Use placeholders in everything you commit or share.
- **Never** buy followers, promise results, target by protected characteristics, or use before/after claims.
- **Do not deploy or commit** without an explicit request in that turn. Tracking changes need the web app (and the API, if it changed) deployed before they take effect; ask first.

## Lessons from a first run (these cost real time)

| Symptom | Cause and fix |
|---|---|
| Events Manager "Connect data" offers Shopify, WooCommerce and Tag Manager | Click "See other ways to set up", then Meta Pixel -> manual. Do not pick a partner. |
| Test events shows a "server" test code | That is the Conversions API test. Use the second section, "website's events", and enter the site URL. |
| "Campaign schedule is too short: ad sets using a daily budget" | Daily budgets need a longer window. Make the end date two days after the start, or use a lifetime budget. The "ad can't be uploaded" error on the ad is only a result of this. |
| "You need access to advertise for <instagram account>" | The Instagram account is not assigned to the ad account. Quick fix: run the ad as the Facebook page. Proper fix: Business settings -> Instagram accounts -> add, then assign the ad account. |
| Preview shows a stock photo of a person holding a phone | Meta AI "image generation" and "enhancements" invented it. Turn both off, and Vary aspect ratio too. The thumbnails must show only your own design. |
| "Select media crop" warnings and grey bars | One image is being stretched to every placement. Replace each placement (square, vertical, horizontal) with its own file. Keep light/dark variants matched. |
| UTM tags missing from the URL field | Meta moved them to Tracking -> URL parameters. Paste them there and tick Website events. |
| Budget strategy offers Campaign budget / Budget sharing / Ad set budget | For a tiny test choose Ad set budget so each ad gets the amount set. |

## Files

- `references/campaign-walkthrough.md` - accounts, campaign, ad set, ad, publish, read results (the screen-by-screen guide).
- `references/tracking.md` - pixel code for a static site and a single-page or Flutter web app, events, new-account detection, privacy text, verification.
- `references/creative-specs.md` - sizes, safe zones, what to put on an ad, copy rules, what to avoid.
- `references/compliance.md` - special ad categories, local advertiser rules, platform policies; all to be verified at the source.
- `scripts/make_creatives.py` - builds the ad images and page assets from a JSON config with headless Chrome.
- `templates/ads.example.json` - a config to copy. `templates/copy.md` - copy patterns to fill in.
