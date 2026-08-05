/**
 * Meta Ads — official CLI driver (Meta Ads CLI, released Apr 2026).
 * Wraps the `meta` executable rather than raw Graph API calls, so auth,
 * pagination, retries and exit codes are Meta's problem, not ours.
 *
 * Prereqs (see developers.facebook.com/blog/post/2026/04/29/introducing-ads-cli):
 *  - Python 3.12+ on the server, CLI installed via pip/uv
 *  - Access token + ad account provided via environment variables
 *    (scope narrowly: ONE ad account per token)
 *
 * NOTE ON FLAGS: command shapes below follow Meta's launch examples
 * (`meta ads campaign create --name ... --objective ... --daily-budget ...`).
 * Verify exact flag names against `meta ads --help` on the deployed box —
 * all arg construction is isolated in the build* functions so any drift is
 * a one-file fix. The raw-API module (lib/meta-ads.js) remains as fallback.
 */
const { execFile } = require('child_process');

const CLI_BIN = process.env.META_CLI_BIN || 'meta';

function runMeta(args) {
  return new Promise((resolve, reject) => {
    // execFile with an args array — no shell, no injection surface.
    execFile(CLI_BIN, args, {
      timeout: 120000,
      env: { ...process.env },          // CLI reads token/account from env vars
      maxBuffer: 4 * 1024 * 1024
    }, (err, stdout, stderr) => {
      if (err) {
        // CLI exit codes: 0 ok, 3 auth error, 4 API error
        const code = err.code;
        const msg = (stderr || stdout || err.message || '').toString().slice(0, 500);
        const e = new Error(`meta CLI exit ${code}: ${msg}`);
        e.exitCode = code;
        return reject(e);
      }
      const out = stdout.toString().trim();
      try { resolve(out ? JSON.parse(out) : {}); }
      catch { resolve({ raw: out }); }
    });
  });
}

async function cliAvailable() {
  try { await runMeta(['--version']); return true; }
  catch (e) { return e.exitCode !== undefined && e.exitCode !== 127 ? true : false; }
}

const idOf = (r) => r.id || r.data?.id || r.campaign_id || r.raw?.match(/\d{8,}/)?.[0];

/* ---- arg builders (single point of flag-name truth) ------------------- */
function buildCampaignArgs(c) {
  return ['ads', 'campaign', 'create',
    '--name', c.name,
    '--objective', c.objective,
    '--daily-budget', String(c.daily_budget),   // minor units per CLI examples
    '--output', 'json'];
}
function buildAdsetArgs(campaignId, adset, endTime) {
  return ['ads', 'adset', 'create', campaignId,
    '--name', adset.name,
    '--optimization-goal', adset.optimization_goal,
    '--billing-event', adset.billing_event,
    '--targeting-countries', 'GB',
    '--end-time', endTime,
    '--output', 'json'];
  /* VERIFY: radius / custom-audience targeting may exceed simple flags —
     refine geo-radius + retargeting audiences in Ads Manager after creation
     (everything is PAUSED), or use the raw-API fallback for those ad sets. */
}
function buildCreativeArgs(pageId, name, imagePath, body, title, link) {
  return ['ads', 'creative', 'create',
    '--name', name,
    '--page-id', pageId,
    '--image', imagePath,
    '--body', body,
    '--title', title,
    '--link', link,
    '--output', 'json'];
}
function buildAdArgs(adsetId, name, creativeId) {
  return ['ads', 'ad', 'create', adsetId,
    '--name', name,
    '--creative-id', creativeId,
    '--output', 'json'];
}

/**
 * Create the full structure via CLI. Creatives: one per image × headline
 * (bodies rotate), capped at 6 per ad set — Meta's Advantage+ creative still
 * optimises among them. Full asset-feed dynamic creative remains available
 * via the raw-API fallback (META_DRIVER=api).
 * Everything is created PAUSED — the CLI's default — and stays paused
 * until a human activates it in Ads Manager.
 */
async function createFullCampaignCLI(payload, imagePaths) {
  const { campaign, adsets, creative, accounts, duration_days } = payload;
  const feed = creative.dynamic_asset_feed;
  const endTime = new Date(Date.now() + duration_days * 86400000).toISOString();
  const created = { driver: 'cli', adsets: [], ads: [] };

  const camp = await runMeta(buildCampaignArgs(campaign));
  created.campaignId = idOf(camp);
  if (!created.campaignId) throw new Error('Campaign created but no id parsed from CLI output');

  // Build capped creative combinations
  const combos = [];
  imagePaths.forEach((img, i) => feed.titles.forEach((title, j) => {
    if (combos.length < 6) combos.push({ img, title, body: feed.bodies[(i + j) % feed.bodies.length] });
  }));

  for (const adset of adsets) {
    const as = await runMeta(buildAdsetArgs(created.campaignId, adset, endTime));
    const adsetId = idOf(as);
    created.adsets.push(adsetId);

    for (const [k, c] of combos.entries()) {
      const cr = await runMeta(buildCreativeArgs(
        accounts.page_id, `${adset.name} — creative ${k + 1}`,
        c.img, c.body, c.title, feed.link));
      const ad = await runMeta(buildAdArgs(adsetId, `${adset.name} — ad ${k + 1}`, idOf(cr)));
      created.ads.push(idOf(ad));
    }
  }
  return created;
}

module.exports = { createFullCampaignCLI, cliAvailable };
