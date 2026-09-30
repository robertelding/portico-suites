# Portico Suites — project brief for Claude Code

Direct-booking website for **Portico Suites**, a 7-bedroom Victorian townhouse on Franklin Road,
Harrogate HG1 5EN (sleeps 10, 5 bathrooms, ~3 min walk to Harrogate Convention Centre).
Owner: Robert Elding. Live site: https://porticosuites.com

## Layout
- `site/` — the published website (Cloudflare Pages serves this folder; push to `main` = live in ~1 min)
- `cms/portico-suites-cms.html` — single-file Site Manager; its DEFAULT_CONTENT drives the homepage
- `tools/` — build scripts (see tools/README.md): `node tools/build-homepage.js`, `python3 tools/build-pages.py`
- `portico-booking-engine/` — Node engine on Render (booking.porticosuites.com): Meta Ads endpoint,
  vouchers, webhooks. Auto-deploys from `main`.
- `brand/` — logos + brand board. Palette: Chalk Ivory #F3F0E8, Deep Olive #34402F, Aged Bronze #8A6A3B,
  Soft Gold #C4A55E. Fonts: Cinzel (headings), Montserrat (body).
- `docs/GO-LIVE.md` — launch runbook.

## How bookings work
The homepage booking section embeds **Hospitable's Direct widget** (site UUID a2c4edd4-…, property 2466600).
The custom engine journey is kept as a fallback (clear the Hospitable Site UUID in CMS booking settings).

## Standard workflow for any change
1. Edit source (CMS defaults, or tools/build-pages.py for landing/journal pages)
2. Rebuild with the tools; check the output
3. Show the owner a summary of what changed, then commit with a clear message and push

## Non-negotiables
- Never commit secrets or `.env`. Secrets live in Render only.
- Property name is exactly "Portico Suites" (must match Hospitable Direct + Google Vacation Rentals).
- Reviews: real and verbatim only. No invented reviews or claims.
- Keep schema (VacationRental) consistent: 10 guests, 7 bedrooms, 5 bathrooms, coords 54.0002205, -1.5377262.
- Images go in `site/images/`, SEO-named `portico-suites-*.jpg`, web-optimised.
