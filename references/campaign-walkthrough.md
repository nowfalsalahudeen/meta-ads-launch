# Campaign walkthrough (beginner, one step at a time)

Meta renames buttons often. Name the screen from the user's screenshot first, say "your screen may differ slightly", and adapt. The user clicks everything; you never enter payment details, accept terms or publish.

## Part 1 - Accounts (about 30 minutes, once)

1. **Facebook page** for the brand (Pages -> Create). Name, category "Software", logo, website, support email. Ads must run from a page.
2. **Instagram account**, separate from the user's personal one.
   - Already logged in to a personal account? Do not log out. In the phone app: profile -> tap the username at the top -> Add Instagram account -> Create new account. On a computer use a private window.
   - Sign up with the **business email** (not the personal phone). Do not use "new profile in this Meta account", which ties it to the personal login.
   - Switch to a **Professional (Business)** account: Settings -> Account type and tools -> Switch to professional account -> Business, category Software. Add the public contact details and the website link.
   - Post 3-6 posts before ads start (an empty account looks untrustworthy), at least one in each language.
   - Do not buy followers, do not make it private.
3. **Link Instagram to the page:** page -> Settings -> Linked accounts -> Instagram -> Connect.
4. **Meta Business account** (business.facebook.com): add the page and the Instagram account. Verify the business if asked, now rather than when blocked.
5. **Ad account:** choose the currency carefully, it cannot be changed. Add a payment method (the user does this). Set a daily spending limit they are comfortable with.
6. **Pixel** (see `tracking.md`). Events Manager -> Connect data -> "See other ways to set up" -> Meta Pixel -> manual. Name it, enter the site. Only the pixel/dataset id is needed.

## Part 2 - Campaign level

1. Ads Manager -> Create.
2. **Objective: Traffic** for the first test (not Sales or Leads: Meta has no sign-up history yet).
3. Choose **manual** (not Advantage+) so you control each ad.
4. Name it, for example `Test 1 - <country>`.
5. **Special ad category:** none unless Meta asks. If it asks, answer honestly (see `compliance.md`).
6. **Budget strategy: Ad set budget** (not Campaign budget or Budget sharing). With a tiny budget each ad set must spend what you set. Bid strategy Highest volume. A/B test off.

## Part 3 - Ad set level

- **Name:** `<market> - <language>`; make one per language.
- **Conversion location:** Website. **Performance goal:** Maximise number of landing page views (cheaper than clicks and filters accidental taps). **Dataset:** the pixel. Attribution Standard.
- **Budget:** daily budget about USD 10 per ad set (enter it in the account currency). **Schedule:** start now, **end two days after the start**. A daily budget with an end date that is too soon fails with "Campaign schedule is too short"; if it persists, use a lifetime budget (for example 2x the daily amount) with the same end date.
- **Locations:** the target country, "people living in this location". **Age** the range of the real buyer (for example 25-55; do not guess wide). **Gender** all. **Languages** blank.
- **Audience:** Advantage+ audience (broad). With a small budget the ad does the targeting. Add interests later.
- **Placements:** Advantage+ placements.

## Part 4 - Ad level

1. **Identity:** the Facebook page and the Instagram account. If it says "You need access to advertise for <account>", pick "Use Facebook Page" for now and fix the assignment later (Business settings -> Accounts -> Instagram accounts -> add, then assign the ad account).
2. Dismiss the "shopping experience / add products" box.
3. **Creative source:** Manual upload. **Format:** Single image or video.
4. Turn **Multi-advertiser ads off** (it can crop the design).
5. **Media:** upload the feed (4:5) image. On the **Crop** step Meta shows Square, Vertical and Horizontal; click **Replace** on each and upload the matching file (square 1:1, story 9:16, link 1.91:1). Use the same variant (light or dark) for all four. The orange warnings disappear when each has its own file.
6. **Text:** primary text, headline, description from `templates/copy.md`. **Call to action:** Sign up (or Learn more).
7. **Destination:** website URL. Meta moves the UTM tags to **Tracking -> URL parameters**: paste `utm_source=meta&utm_medium=paid&utm_campaign=test1&utm_content=<ad id>` there and tick **Website events**. Leave Browser add-ons "None", skip Third-party reporting, Languages off.
8. **Image generation and Enhancements: turn every toggle OFF**, and Vary aspect ratio off. If left on, Meta may invent a photo of a person holding a phone with an altered screen. After turning them off, the preview thumbnails must show only your own design.
9. Check the preview in Feed, Story and Reels.

## Part 5 - Publish

Check the summary: objective, budget and end date, country, name. The user clicks Publish. "Processing" and "In review" are normal and can last minutes to a day. Do not edit while in review (it restarts). Statuses: Active/Learning = live; Rejected = open the reason, Edit or Request review.

## Part 6 - Read the result (after 24-48 hours)

Columns: Impressions, Reach, CPM, Link clicks, CTR (link), CPC, Landing page views. A link CTR above about 1% on a feed ad is decent; cost per click depends on the market (quoted ranges conflict, use the account's own numbers). One day of data is noisy and early days cost more; judge on two. Pause the weakest ad and keep the best one or two for five to seven days. For sign-ups use the app's own user list until the pixel has seen enough events; do not optimise for sign-ups before about 50 in a week.

## Part 7 - Next stage

- **Sales or Leads campaign** with the sign-up event as the conversion once there are enough events.
- **Retargeting:** after about 1,000 visitors, show an ad to people who visited the site and did not sign up.
- Add a messaging or lead-form variation only if someone can answer it quickly.
- Add more audiences or markets one at a time.
