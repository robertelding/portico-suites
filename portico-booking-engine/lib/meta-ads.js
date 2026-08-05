/**
 * Meta (Facebook) Marketing API — campaign creation from CMS payload.
 * Requires in .env: META_ACCESS_TOKEN (system-user token with ads_management),
 * CMS_ADMIN_KEY (shared secret with the CMS panel).
 *
 * Creates: 1 campaign (CBO, lowest-cost, PAUSED) → N ad sets (Advantage+
 * placements, dynamic creative) → 1 dynamic-creative ad per ad set.
 * Meta's delivery system then handles combination testing and budget shifting.
 *
 * Verify field names against current Graph API docs (developers.facebook.com/
 * docs/marketing-api) at integration time — versions move quarterly.
 */
const GRAPH = 'https://graph.facebook.com/v21.0';

async function meta(path, body) {
  const res = await fetch(`${GRAPH}/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...body, access_token: process.env.META_ACCESS_TOKEN })
  });
  const out = await res.json();
  if (out.error) {
    const err = new Error(`Meta API: ${out.error.message} (code ${out.error.code})`);
    err.meta = out.error;
    throw err;
  }
  return out;
}

/** Map CMS audience names to targeting specs. Interests use Meta's canonical
 *  IDs — resolve via /search?type=adinterest at setup and pin them here. */
function targetingFor(adset, pixelId) {
  const base = { geo_locations: { countries: ['GB'] }, age_min: 28, age_max: 65 };
  if (/retargeting/i.test(adset.name)) {
    return { ...base,
      custom_audiences: pixelId ? [{ /* create website-visitor audience from pixel in Ads Manager; insert its ID here or via setup script */ }] : [] };
  }
  if (/harrogate|yorkshire/i.test(adset.name)) {
    return { geo_locations: { custom_locations: [{ latitude: 53.9921, longitude: -1.5418, radius: 50, distance_unit: 'kilometer' }], countries: ['GB'] }, age_min: 28, age_max: 65 };
  }
  return { ...base, flexible_spec: [{ interests: [/* boutique hotels, spa breaks, weekend getaways — pin IDs at setup */] }] };
}

async function createFullCampaign(payload, imageUrls) {
  const { campaign, adsets, creative, accounts, duration_days } = payload;
  const acct = accounts.ad_account_id.startsWith('act_') ? accounts.ad_account_id : 'act_' + accounts.ad_account_id;
  const created = { adsets: [], ads: [] };

  // 1. Campaign — CBO, lowest cost, PAUSED for human review
  const camp = await meta(`${acct}/campaigns`, {
    name: campaign.name, objective: campaign.objective,
    special_ad_categories: [], status: 'PAUSED',
    daily_budget: campaign.daily_budget,
    bid_strategy: campaign.bid_strategy
  });
  created.campaignId = camp.id;

  const end = new Date(Date.now() + duration_days * 86400000).toISOString();

  // 2. Upload images once, reuse hashes across ad sets
  const hashes = [];
  for (const url of imageUrls) {
    const img = await meta(`${acct}/adimages`, { url });
    const first = Object.values(img.images || {})[0];
    if (first?.hash) hashes.push(first.hash);
  }

  for (const adset of adsets) {
    // 3. Ad set — Advantage+ placements (omit placement spec), dynamic creative
    const as = await meta(`${acct}/adsets`, {
      name: adset.name, campaign_id: camp.id,
      optimization_goal: adset.optimization_goal,
      billing_event: adset.billing_event,
      targeting: targetingFor(adset, accounts.pixel_id),
      end_time: end, status: 'PAUSED', is_dynamic_creative: true
    });
    created.adsets.push(as.id);

    // 4. Dynamic creative via asset feed — Meta tests every combination
    const cr = await meta(`${acct}/adcreatives`, {
      name: `${adset.name} — dynamic`,
      object_story_spec: { page_id: accounts.page_id },
      asset_feed_spec: {
        images: hashes.map(hash => ({ hash })),
        titles: creative.dynamic_asset_feed.titles.map(text => ({ text })),
        bodies: creative.dynamic_asset_feed.bodies.map(text => ({ text })),
        link_urls: [{ website_url: creative.dynamic_asset_feed.link }],
        call_to_action_types: [creative.dynamic_asset_feed.call_to_action],
        ad_formats: ['SINGLE_IMAGE']
      }
    });

    const ad = await meta(`${acct}/ads`, {
      name: `${adset.name} — ad`, adset_id: as.id,
      creative: { creative_id: cr.id }, status: 'PAUSED'
    });
    created.ads.push(ad.id);
  }
  return created;
}

module.exports = { createFullCampaign };
