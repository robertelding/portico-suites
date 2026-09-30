# Site build tools

Everything under `site/` is generated from two sources:

| Output | Source | Command (run from repo root) |
|---|---|---|
| `site/index.html` (homepage) | the **default content** inside `cms/portico-suites-cms.html` | `node tools/build-homepage.js` |
| 30 landing pages, `site/journal/`, `site/sitemap.xml` | `tools/build-pages.py` (page data lives in this script) | `python3 tools/build-pages.py` |

Setup once: `cd tools && npm install` (installs jsdom).

## Making a change
- **Homepage content** (text, reviews, FAQ, gallery, policies, contact details): edit the defaults in
  `cms/portico-suites-cms.html` (the `DEFAULT_CONTENT` object), then run `build-homepage.js`.
- **Landing pages / Journal**: edit `tools/build-pages.py`, then run it. New Journal posts go in the
  `JPOSTS` list here *and* in the CMS `blog.posts` defaults (so the homepage cards match).
- Images: add to `site/images/` using `portico-suites-*.jpg` names; keep them under ~300 KB.
- Commit and push to `main` — Cloudflare Pages republishes automatically (~1 minute).
  Engine changes under `portico-booking-engine/` redeploy on Render automatically.

## Rules
- Never commit `.env` or any secret. Secrets live in Render's Environment settings only.
- Keep "Portico Suites" as the property name everywhere (it must match Hospitable Direct / Google).
- Reviews must be quoted verbatim and be real.
