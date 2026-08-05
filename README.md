# Portico Suites — Franklin Road, Harrogate

Direct-booking website, CMS, and integration engine for Portico Suites,
a boutique holiday property in Harrogate (HG1 5EN).

## Structure

| Path | What it is |
|---|---|
| `/cms` | **Site Manager** — single-file CMS: login & editor accounts, all content/image/layout editing, custom sections, subscriber database, email template studio (10 base designs), blog, SEO & AI-search tools, Facebook Ads campaign builder, live preview, website export. |
| `/portico-booking-engine` | Node/Express integration layer: Hospitable PMS (availability, pricing, reservations), Stripe payments (3DS, verified webhooks), Meta Ads (official Ads CLI driver + Graph API fallback), Yale/Duve/Minut configuration docs, messaging templates. |

## Quick start

- **Manage the site:** open `cms/portico-suites-cms.html` (first run creates the
  master account). Publish/Export produces the deployable website.
- **Run the engine:** `cd portico-booking-engine && npm install`, copy
  `.env.example` → `.env`, fill credentials (never commit `.env`), `npm start`.
  Full setup, webhook registration and dashboard configuration: see
  `portico-booking-engine/README.md`.

## Deployment target

Website → static hosting (Netlify) · Engine → Render/Railway (HTTPS required
for Stripe). Connecting both to this repo enables auto-deploy on every commit.

## Related project assets

Brand artwork, content seeds and the build log live in the Google Drive
project folder (`Franklin Rd Property Website`).
