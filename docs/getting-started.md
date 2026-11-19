# Getting started

A first-time advertiser's path from nothing to a running test. The agent walks you through it; this page is the same map for you.

## 0. What you need

- A product with a **website** and, ideally, a **web app** (so sign-ups can be tracked).
- A **payment card** for Meta (you enter it yourself).
- A budget you are comfortable losing: about **USD 25 a day for two days** is enough to learn from.
- Screenshots of your real product: one desktop browser window and one phone screen, in each language you will advertise in.

## 1. Install the skill

See the [README](../README.md#install). Then start a conversation with your agent and describe the product, the buyer, the country and the budget.

## 2. Accounts (about 30 minutes, once)

The agent gives you exact steps; the order is:

1. **Facebook page** for the brand (ads must run from a page).
2. **Instagram business account**, separate from your personal one. If you are already logged in to a personal account, add a second account in the app instead of logging out. Sign up with a business email, not a personal phone.
3. **Link Instagram to the page.**
4. **Meta Business account**; verify the business now if asked.
5. **Ad account** with the right currency (it cannot be changed) and a payment method.

## 3. Tracking

The agent adds the **Meta Pixel** to your site and web app with these events:

| Event | When |
|---|---|
| `PageView` | any page loads |
| `Lead` | a visitor clicks from the site to the app |
| `CompleteRegistration` | a brand-new account is created (once per browser) |
| `FirstAction` (name it for your product) | the first real use |

The pixel id sits in one config value; leaving it empty turns everything off. The agent also updates your privacy page and checks in a real browser that requests reach Meta. You then confirm in **Events Manager -> Test events -> Website** (not the Server option).

## 4. Creatives

Prepare screenshots, copy `examples/` as a starting point, edit `ads.json` (brand, languages, headlines, screens) and run the script. You get, per ad and language: feed (4:5), square (1:1), story (9:16) and link (1.91:1) images, plus a profile picture and cover photo. See [config-reference.md](config-reference.md).

Rules the agent holds to: only what the product does today, no invented numbers or testimonials, no prices before paid plans exist.

## 5. Copy

Fill in the patterns in `templates/copy.md`: primary text, headline, description, button, and the tracking link with UTM tags.

## 6. Build the campaign (one step at a time)

You click; the agent says exactly where. The first test is:

- Objective **Traffic**, **manual** setup, budget at the **ad set** level
- One ad set per language, about USD 10 a day each, ending **two days** after the start
- Broad audience in one country, your buyer's real age range, automatic placements
- One to three ads, **AI image generation and enhancements off**, each placement with its own correctly sized image
- Tracking tags under **Tracking -> URL parameters**, **Website events** ticked

Then you press **Publish**. "Processing" and "In review" are normal.

## 7. Read the result

After 24-48 hours look at impressions, link click-through rate, cost per click and landing-page views. A link CTR around 1% or more on a feed ad is decent. Pause the weakest ad, keep the best one or two for 5-7 days, and do not judge sign-ups until you have enough events (roughly 50 in a week). Then switch to a sign-up campaign and add retargeting.

## 8. Next

- Add a second country (check its advertiser rules first, see [compliance](../references/compliance.md)).
- Make a feature-led and a pain-led ad and compare.
- Add retargeting after about 1,000 visitors.
