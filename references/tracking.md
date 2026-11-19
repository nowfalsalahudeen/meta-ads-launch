# Tracking: Meta Pixel and sign-up events

Goal: Meta learns who visits and who signs up, without leaking customer data. The pixel id lives in one config value; empty means no script, no cookies, no requests.

## Events to send

| Event | Where | When |
|---|---|---|
| `PageView` | every page of the site and the web app | page load |
| `Lead` | the marketing site | a click on a link to the app (sign-up intent) |
| `CompleteRegistration` | the web app | a brand-new account is created, once per browser |
| custom `FirstAction` (name it for your product's first real action, for example `CreatedProject`) | the web app | the first thing that shows real use |

Use standard event names where one fits, because Meta optimises on them. Send **no** customer data (names, amounts, emails) in event parameters.

## Marketing site (static HTML or any framework)

Inject once in the head, only when an id is configured:

```html
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'PIXEL_ID');
fbq('track', 'PageView');
document.addEventListener('click', function (e) {
  var a = e.target && e.target.closest ? e.target.closest('a') : null;
  if (a && a.href && a.href.indexOf('https://app.example.com') === 0) fbq('track', 'Lead');
});
</script>
```

In Astro use `<script is:inline define:vars={{ id, appUrl }}>` so the values are filled at build time; wrap it in `{id && (...)}`.

## Single-page / Flutter web app

Load the script from code only on the web build and only when an id was given at build time (`--dart-define=META_PIXEL_ID=...`). Keep a stub for mobile builds so nothing is sent from them.

- Flutter: a conditional export (`dart.library.js_interop`) with `pixel_web.dart` (append a `<script>` element whose text is the snippet above, then call `fbq` through `globalContext.callMethod`) and a no-op `pixel_stub.dart`.
- Call `initPixel()` before `runApp`.

## Counting a sign-up once, without a server flag

If the API does not say "this account is new", add the account creation time (`created_at`, RFC 3339) to the user object. On sign-in the client counts a sign-up when the account is under about 15 minutes old **and** this browser has not reported it before (store `pixel.signup.<userId>` in local storage). Signing in again later or on another device is then not a second sign-up. The API change must be deployed before the event can fire.

## Privacy

Say it in the privacy policy: the pixel is used when ads run, it can record that a visitor came from an ad, the pages opened, and that an account was created or a first action happened; it sets cookies; it shares those events (not the records, names or amounts users enter) with Meta; users can block it or turn off ad personalisation in their Meta settings. Where law requires consent (the EU and some other regions), add a consent step before loading the script; do not target those regions without one.

## Verify (do both)

1. **In a real browser** (headless is fine): load the site and read `performance.getEntriesByType('resource')` for `facebook.com/tr/?id=<id>&ev=PageView`; simulate a click on the app link with `preventDefault` and look for `ev=Lead`. Your own test visits count as events in the dataset, so tell the user.
2. **In Meta:** Events Manager -> Datasets -> the dataset -> **Test events** -> channel **Website** -> open the **website's events** section (not the server one), enter the URL and Open website. PageView and Lead should appear within seconds. For `CompleteRegistration` sign up once with a new email in that same test tab. The test code and the Graph API Explorer are for the Conversions API; ignore them. "Needs attention" about missing parameters is normal at the start.
