# How it works

## The skill

`SKILL.md` is a short workflow with rules and a table of lessons. It points to four reference files that the agent opens only when needed, so the main file stays small.

1. **Inspect the product** so ads only say what is true today.
2. **Ask** the few questions that change the plan (buyer, country, languages, budget, existing accounts).
3. **Accounts**, then **tracking**, **creatives**, **page assets**, **copy**.
4. **Build the campaign with the user**, one step at a time, asking for a screenshot after each.
5. **Read the result** and decide what to do next.

The skill never enters payment details, accepts terms, publishes or raises a budget. Those are the user's clicks.

## The image script

`scripts/make_creatives.py` draws each image as an HTML page (the product in a browser frame and on a phone, a headline, an offer badge, a button, and floating cards or a checklist) and photographs it with headless Chrome at the exact pixel size. There is no image library and no Python package to install. The same code makes the Facebook profile picture and cover photos.

Because it works from your own screenshots, the ads show your real product, in your languages and currency.

## The tracking approach

Everything hangs off one config value, the pixel id. Empty means the script is not added and nothing is sent.

- On a site, a snippet in the head records page views and a `Lead` when someone clicks through to the app.
- In a single-page or Flutter web app, the same script is loaded from code, only on the web build.
- A sign-up is counted once by treating an account as new when it was created in the last 15 minutes and this browser has not reported it before, using the account's creation time from the API.

Details and code are in [references/tracking.md](../references/tracking.md).

## Why one test, two days, a tiny budget

You are buying information, not customers: does the creative get noticed, what does a click cost in this market, does the landing page hold people. Two days and about USD 20-30 is enough to learn that. Sign-ups need volume before Meta can optimise for them, so the first test uses the Traffic objective and a later campaign switches to sign-ups after roughly 50 events in a week.
