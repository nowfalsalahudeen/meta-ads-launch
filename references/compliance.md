# Compliance checks (verify each at the official source before spending)

Rules differ by product, country and date, and the articles that summarise them often disagree. Treat this file as a checklist of things to confirm, not as rules. Tell the user which items you could not verify.

## 1. Meta special ad categories

Meta restricts targeting for ads in certain categories: credit (loans, cards, financing), employment (jobs, recruiting), housing (selling or renting homes, mortgages, home insurance and similar), and social issues, elections or politics in many regions. If the product touches one of these (a lending app, a job board, a rental or real-estate tool), expect fixed broad age and gender, a minimum radius and no lookalike or exclusion targeting, and ad copy that does not imply excluding groups.

To do: ask whether the product is covered by reading Meta's current "Special ad categories" help page or asking Meta business support. If the ad flow asks for a declaration, answer honestly; skipping a required one can lead to rejected ads or account penalties. If the product is clearly outside every category, leave the field blank.

## 2. Local advertiser rules

Some countries require a licence, permit or registration to advertise on social media, or approval for certain sectors (financial products, health, real estate, education and others), and some apply to foreign companies advertising to local residents. Example: the UAE Media Council introduced an Advertiser Permit for social-media promotion in 2026; reports of its scope and penalties conflict.

To do: for each country you target, look up the media or advertising regulator's own site (or ask a local lawyer) before running ads there, and say what you could not confirm. Start with one country so you check only one set of rules.

## 3. Platform policies

- Business verification may be requested; do it early.
- The landing page must match the ad, load fast, show a privacy policy, and not collect data the policy does not describe.
- No misleading claims; no copy that asserts personal attributes ("are you in debt?"); nothing about protected characteristics.
- Ads must not promise things the product does not do or an app that is not published.

## 4. Data and privacy

- Pixel and cookie disclosure in the privacy policy (see `tracking.md`).
- Do not send customer data in event parameters. Hashing emails for advanced matching is a separate decision that needs its own disclosure.
- Where consent law applies (the EU and some other regions), show a consent step before loading the pixel, or do not target that region.

## 5. Store rules that touch ads

- An ad that links to a store listing requires the listing to exist.
- Mobile apps declare the advertising ID in the store's data form. A product with no ad SDK and the advertising-ID permission removed answers "No"; adding an ad or conversion SDK inside the app changes that.
