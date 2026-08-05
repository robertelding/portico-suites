# Portico Suites — Go-Live Runbook
_porticosuites.com · Website (static) + Booking Engine (Node) + integrations_

**Target architecture & monthly cost**

| Piece | Host | Cost |
|---|---|---|
| DNS + SSL + CDN | Cloudflare (free plan) | £0 |
| Website (static export from CMS) | Cloudflare Pages, auto-deploy from GitHub | £0 |
| Booking engine (Node/Express) | Render — Starter web service (always-on, needed for webhooks) | ~£6/mo |
| PMS / channel sync | Hospitable | per their plan |
| Payments | Stripe | per-transaction only |

Everything deploys from `github.com/robertelding/portico-suites` — every commit
to `main` auto-publishes. No servers to patch, HTTPS everywhere by default.

---

## Phase 0 — Repo preparation
- [ ] Commit `/brand` folder (logos PNG + original PDFs + asset guide)
- [ ] Create `/site` folder — this is what Cloudflare Pages will publish:
  - [ ] `index.html` — export from the CMS (Publish/Export button)
  - [ ] `booking-widget.js` — copy from `/portico-booking-engine/public`
  - [ ] `/site/images/` — final photography (also used as Meta ad images)
  - [ ] `robots.txt` + `sitemap.xml` — download from CMS → SEO & AI Search tab
- [ ] Commit this runbook as `docs/GO-LIVE.md`

## Phase 1 — Domain & DNS (Cloudflare)
- [ ] Create free Cloudflare account → Add site `porticosuites.com`
- [ ] At your domain registrar, change nameservers to the two Cloudflare gives you
- [ ] SSL/TLS mode: **Full (strict)**
- [ ] Plan DNS records (created automatically by the steps below):
  - `porticosuites.com` → Pages (website)
  - `booking.porticosuites.com` → Render (engine)

## Phase 2 — Website deploy (Cloudflare Pages)
- [ ] Pages → Create project → connect GitHub repo → build settings: none
      (static), output directory: `/site`
- [ ] Custom domain: `porticosuites.com` (+ `www` redirect)
- [ ] Verify: site loads over https, images render, map shows HG1 5EN
- [ ] Post-engine-deploy, add before `</body>` in `site/index.html`:
      `<script src="https://js.stripe.com/v3/"></script>`
      `<script src="booking-widget.js" data-api="https://booking.porticosuites.com" data-stripe-pk="pk_live_…"></script>`

## Phase 3 — Engine deploy (Render)
- [ ] render.com → New Web Service → connect repo, root dir
      `portico-booking-engine`, build `npm install`, start `npm start`
- [ ] Instance: **Starter** (always-on; free tier sleeps and drops webhooks)
- [ ] Environment: add every variable from `.env.example` (values only in
      Render's dashboard — never in the repo)
- [ ] Custom domain: `booking.porticosuites.com`
- [ ] Verify: `https://booking.porticosuites.com/health` → `{"ok":true}`

## Phase 4 — Hospitable (the hub)
- [ ] Connect the property; confirm Airbnb/Vrbo channels sync
- [ ] Apps → API access → create **Personal Access Token** → Render env
      `HOSPITABLE_TOKEN` (⚠ expires after 1 year — diarise renewal)
- [ ] Property ID → `HOSPITABLE_PROPERTY_ID`
- [ ] Webhooks → add `https://booking.porticosuites.com/webhooks/hospitable`,
      shared secret → `HOSPITABLE_WEBHOOK_SECRET`
- [ ] Verify field names vs `lib/hospitable.js` normaliser (5-min check against
      developer.hospitable.com)

## Phase 5 — Stripe
- [ ] Live keys → Render env (`STRIPE_SECRET_KEY`, publishable key into the
      widget tag)
- [ ] Webhook endpoint `https://booking.porticosuites.com/webhooks/stripe`
      with events `payment_intent.succeeded`, `charge.dispute.created`;
      signing secret → `STRIPE_WEBHOOK_SECRET`
- [ ] Inside Hospitable: Settings → Direct Booking → Payment Gateways →
      connect the same Stripe account (enables post-stay incidental holds)

## Phase 6 — Guest-experience stack (all configured inside Hospitable)
- [ ] **Yale**: Apps → Smart Locks → Yale · PIN = last 4–6 digits of guest
      phone · active 3:00 PM arrival (1:00 PM with early check-in add-on) ·
      revoke 10:00 AM departure
- [ ] **Duve**: connect account · enable ID scan + selfie + deposit hold ·
      automation at T-72h via WhatsApp/SMS · completion sets status
      **Verified** (the gate for the keycode message)
- [ ] **Minut**: pair sensor · threshold >75 dB / 10 min / 11 PM–7 AM ·
      optional audit webhook → `/webhooks/minut`
- [ ] Load messaging Templates A–D from
      `portico-booking-engine/templates/hospitable-messages.md`
      (Template A trigger MUST require status = Verified)

## Phase 7 — Meta Ads (after new Business account exists)
- [ ] New Meta Business account + ad account + Page for Portico Suites
- [ ] Install **Meta Pixel** on the website; ID into CMS → Facebook Ads panel
- [ ] On Render: install Meta **Ads CLI** (Python 3.12+, per Meta's Apr-2026
      developer blog post) · `meta ads --help` → confirm flags vs
      `lib/meta-ads-cli.js` build* functions
- [ ] System-user token scoped to the ONE ad account → `META_ACCESS_TOKEN`
- [ ] Ad image paths (from `/site/images`) → `META_AD_IMAGE_PATHS`
- [ ] Shared secret → `CMS_ADMIN_KEY` (Render) = Admin key (CMS panel)
- [ ] Pin interest-targeting IDs (boutique hotels / spa breaks / weekend
      getaways) in `lib/meta-ads.js`
- [ ] Test: create a campaign from the CMS → confirm it appears **PAUSED**
      in Ads Manager → review → activate manually

## Phase 8 — Newsletter capture
- [ ] Pick an email platform (e.g. Brevo/Mailchimp) → import subscriber CSV
      from CMS → paste its form endpoint into CMS → Newsletter → endpoint
- [ ] Re-export site so the live form posts to it

## Phase 9 — Content finalisation (in the CMS)
- [ ] Real photography into gallery slots (+ hero)
- [ ] Actual bedrooms/baths/sleeps, amenities, walk times (HG1 5EN is
      central — confirm 5–10 min figures)
- [ ] Nightly rate + cleaning fee (drives live checkout totals)
- [ ] Policies: finalise cancellation terms; privacy policy UK-GDPR complete
      (worth a legal read before taking payments)
- [ ] Replace placeholder reviews with 3 real ones from Airbnb/Vrbo
- [ ] SEO tab: confirm meta title/description, OG image, Key Facts; health
      check ≥ 80%

## Phase 10 — End-to-end testing (Stripe test mode first)
- [ ] Calendar on site matches Hospitable exactly (block a date → refresh)
- [ ] Quote maths correct incl. "Direct Savings" line
- [ ] Test-card booking → 3DS challenge → reservation appears in Hospitable →
      confirmation redirect works
- [ ] Webhook signatures verified (Stripe CLI test events; bad-signature
      rejected with 400/401)
- [ ] Duve flow fires at T-72h on a dummy reservation; keycode message only
      after Verified
- [ ] Admin alerts arrive (kill Yale sync on a test booking → alert within
      10 min)
- [ ] Mobile pass: booking flow end-to-end on a phone

## Phase 11 — Launch
- [ ] Switch Stripe to live keys · one real £1-rate test booking, then refund
- [ ] Google Search Console: verify domain, submit sitemap
- [ ] Confirm robots.txt live at porticosuites.com/robots.txt (AI crawlers
      welcomed)
- [ ] Announce: first newsletter (Template: Classic Announcement) + first
      Meta campaign activated
- [ ] Diarise: quarterly content refresh (SEO), Hospitable PAT renewal (1 yr)

---
_Working model from here: repo is source of truth · CMS manages content ·
commits auto-deploy · Drive keeps Build Log, content seeds & brand originals._
