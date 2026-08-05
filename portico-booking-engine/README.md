# Portico Suites — Direct Booking Engine

Production integration layer connecting the CMS-built website to Hospitable (PMS),
Stripe (payments), Yale Access (smart locks), Duve (verification), and Minut (noise).

## Architecture

    [ CMS Website (static export) + booking-widget.js ]
                 │ HTTPS (no secrets client-side)
                 ▼
    [ This Node/Express server ]───Bearer PAT───►[ Hospitable Public API v2 ]
                 │                                        │ native integrations
                 ├─► Stripe PaymentIntents (3DS/SCA)      ├─► Yale Access (PIN gen)
                 ├─◄ /webhooks/stripe   (sig-verified)    ├─► Duve (ID sync, portal)
                 ├─◄ /webhooks/hospitable (HMAC)          └─► Minut (noise alerts)
                 └─◄ /webhooks/minut   (audit log)

Design decisions:
- The browser never holds API tokens. The widget talks only to this server.
- Prices are computed **server-side** from the live Hospitable calendar and held as
  15-minute quotes — a tampered client can never change what gets charged.
- Payment is verified against Stripe **before** the reservation is created;
  if reservation creation fails after a successful charge, an admin alert fires.
- All webhook listeners validate cryptographic signatures (Stripe official SDK
  verification; Hospitable HMAC with timing-safe comparison).

## Setup

1. `npm install`
2. `cp .env.example .env` and fill in every value:
   - **Hospitable PAT**: my.hospitable.com → Apps → API access → Access tokens.
     PATs expire after **one year** — diarise renewal.
   - **Stripe keys**: Dashboard → Developers → API keys.
3. `npm start` (deploy to Render/Railway/Fly/Heroku; HTTPS required for Stripe).
4. Register webhooks:
   - Stripe Dashboard → Webhooks → `https://<host>/webhooks/stripe`
     with events `payment_intent.succeeded`, `charge.dispute.created`;
     copy the signing secret to `STRIPE_WEBHOOK_SECRET`.
   - Hospitable → Webhooks → `https://<host>/webhooks/hospitable`
     (reservation events); shared secret to `HOSPITABLE_WEBHOOK_SECRET`.
5. Website: in the CMS export, before `</body>` add:
   ```html
   <script src="https://js.stripe.com/v3/"></script>
   <script src="booking-widget.js" data-api="https://<host>" data-stripe-pk="pk_live_..."></script>
   ```
6. Create `/booking-confirmation` page (CMS custom section or standalone) reading
   `?reservation_id=` for the thank-you state.

## Dashboard configuration (no code — native Hospitable integrations)

**Stripe inside Hospitable** — Settings → Direct Booking → Payment Gateways →
connect the same Stripe account, enabling tokenized post-stay incidental holds.

**Yale Access** — Hospitable → Apps → Smart Locks → Yale:
- PIN format: last 4–6 digits of guest's primary phone number
- Active from 3:00 PM arrival day (1:00 PM when the early check-in add-on is
  purchased) → auto-revoke 10:00 AM departure day
- Fallback: if Yale API fails, Hospitable's default PIN format applies; this
  server also raises an admin alert if a confirmed reservation is missing a
  smart-lock code 10 minutes after acceptance.

**Duve** — connect Hospitable account in Duve; enable: ID scan + selfie match +
security deposit hold; automation at T-72h via WhatsApp/SMS with personal portal
link; on completion Duve marks the Hospitable stay `Verified` — which is the
gate for the keycode message (Template A).

**Minut** — pair sensors to the property in Hospitable → Apps → Minut:
- Threshold: >75 dB sustained 10 minutes, 11:00 PM–7:00 AM
- On breach: Hospitable fires Template B to the guest's mobile automatically;
  optionally point Minut's outgoing webhook at `/webhooks/minut` for audit
  logging + admin visibility.

## Verify-at-integration notes

Endpoint paths and auth follow Hospitable Public API v2 (Bearer PAT,
`public.api.hospitable.com/v2`). Exact response field names for calendar days,
reservation payloads, and the reservation-update endpoint should be confirmed
against developer.hospitable.com when credentials are in hand — all schema
touchpoints are isolated in `lib/hospitable.js` (one normaliser function) so
any drift is a five-minute fix in one file.

## Meta Ads drivers

Campaign creation from the CMS supports two drivers (META_DRIVER):
- **cli** (default): drives Meta's official **Ads CLI** (Apr 2026) via safe
  argv spawn — auth, pagination, retries and exit codes handled by Meta's
  supported tool; everything created PAUSED by the CLI's own default.
  Install on the server: Python 3.12+, then the CLI per Meta's blog post
  (developers.facebook.com/blog/post/2026/04/29/introducing-ads-cli).
  Run `meta ads --help` after install and confirm the flag names in
  lib/meta-ads-cli.js (single point of truth in the build* functions).
- **api**: raw Graph API fallback (lib/meta-ads.js) — auto-used when the CLI
  binary is absent; also the route for full asset-feed dynamic creative or
  complex targeting the CLI flags don't express.
Guardrails either way: one ad account per token, token in .env only, PAUSED
until a human activates in Ads Manager.

## Files

    server.js                     Express app: API + verified webhooks
    lib/hospitable.js             Hospitable v2 client + schema normaliser
    lib/meta-ads-cli.js           Meta Ads CLI driver (preferred)
    lib/meta-ads.js               Raw Graph API driver (fallback)
    public/booking-widget.js      Frontend drop-in for the CMS export
    templates/hospitable-messages.md  Messaging templates A–D
    .env.example                  All required configuration
