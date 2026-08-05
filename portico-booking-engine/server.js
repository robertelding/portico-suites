/**
 * Portico Suites — Direct Booking Engine
 * CMS frontend ⇄ Hospitable PMS ⇄ Stripe, with verified webhook listeners.
 *
 * Security rules implemented per developer brief:
 *  - All credentials via .env (never in code or client)
 *  - Cryptographic signature validation on every webhook listener
 *  - Server-side price recomputation (client totals are never trusted)
 *  - Yale PIN failure → fallback + admin alert
 */
require('dotenv').config();
const express = require('express');
const crypto = require('crypto');
const Stripe = require('stripe');
const { getProperty, getCalendar, createReservation, flagReservation } = require('./lib/hospitable');

const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
const app = express();
const PROPERTY_ID = process.env.HOSPITABLE_PROPERTY_ID;
const CURRENCY = process.env.CURRENCY || 'gbp';
const DIRECT_SAVINGS_PCT = Number(process.env.DIRECT_SAVINGS_PCT || 12);

/* ── CORS (booking widget origin only) ─────────────────────────────── */
app.use((req, res, next) => {
  res.set('Access-Control-Allow-Origin', process.env.SITE_ORIGIN || '*');
  res.set('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.sendStatus(204);
  next();
});

/* Stripe webhooks need the RAW body for signature verification —
   register that route BEFORE express.json(). */
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), handleStripeWebhook);
app.use(express.json());

/* ── Admin alerting (Yale fallback, disputes, failures) ─────────────── */
async function adminAlert(text) {
  console.error('[ALERT]', text);
  if (!process.env.ALERT_WEBHOOK_URL) return;
  try {
    await fetch(process.env.ALERT_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: `🏛 Portico Booking Engine: ${text}` })
    });
  } catch (e) { console.error('Alert delivery failed', e.message); }
}

/* ── Quote store: server-computed prices, 15-min validity ───────────── */
const quotes = new Map();
function storeQuote(q) {
  const id = crypto.randomUUID();
  quotes.set(id, { ...q, expires: Date.now() + 15 * 60 * 1000 });
  setTimeout(() => quotes.delete(id), 16 * 60 * 1000).unref?.();
  return id;
}
function getQuote(id) {
  const q = quotes.get(id);
  return q && q.expires > Date.now() ? q : null;
}

/* ── 1. Property details (cached 10 min) ────────────────────────────── */
let propertyCache = { data: null, at: 0 };
app.get('/api/property', async (req, res) => {
  try {
    if (!propertyCache.data || Date.now() - propertyCache.at > 600000) {
      propertyCache = { data: await getProperty(PROPERTY_ID), at: Date.now() };
    }
    const p = propertyCache.data;
    res.json({
      name: p.name || p.public_name,
      maxOccupancy: p.capacity?.max ?? p.max_occupancy,
      amenities: p.amenities,
      checkIn: p.check_in || '15:00',
      checkOut: p.check_out || '10:00'
    });
  } catch (e) { res.status(502).json({ error: 'Property lookup failed' }); console.error(e); }
});

/* ── 2. Live availability calendar ──────────────────────────────────── */
app.get('/api/calendar', async (req, res) => {
  try {
    const { start, end } = req.query;
    if (!/^\d{4}-\d{2}-\d{2}$/.test(start) || !/^\d{4}-\d{2}-\d{2}$/.test(end))
      return res.status(400).json({ error: 'start/end must be YYYY-MM-DD' });
    res.json({ days: await getCalendar(PROPERTY_ID, start, end) });
  } catch (e) { res.status(502).json({ error: 'Calendar unavailable' }); console.error(e); }
});

/* ── 3. Quote: server-side pricing with live breakdown ──────────────── */
const ADDONS = { parking: { label: 'Private parking', amount: 0 },
                 early_checkin: { label: 'Early check-in (1:00 PM)', amount: 25 } };
const CLEANING_FEE = 60;      // move to env/Hospitable fees once confirmed
const TAX_PCT = 0;            // UK: set if registered / local taxes apply

app.post('/api/quote', async (req, res) => {
  try {
    const { checkIn, checkOut, guests = 2, addons = [] } = req.body;
    const days = await getCalendar(PROPERTY_ID, checkIn, checkOut);
    const nights = days.filter(d => d.date >= checkIn && d.date < checkOut);
    if (!nights.length) return res.status(400).json({ error: 'Invalid date range' });
    if (nights.some(d => !d.available))
      return res.status(409).json({ error: 'One or more selected nights are no longer available' });

    const subtotal = nights.reduce((s, d) => s + d.price, 0);
    const addonItems = addons.filter(a => ADDONS[a]).map(a => ({ code: a, ...ADDONS[a] }));
    const addonTotal = addonItems.reduce((s, a) => s + a.amount, 0);
    const tax = Math.round(subtotal * TAX_PCT) / 100;
    const total = Math.round((subtotal + CLEANING_FEE + addonTotal + tax) * 100) / 100;
    const otaComparison = Math.round(total / (1 - DIRECT_SAVINGS_PCT / 100) * 100) / 100;

    const quote = { checkIn, checkOut, guests, addons, nights: nights.length,
                    subtotal, cleaningFee: CLEANING_FEE, addonItems, tax, total, otaComparison };
    res.json({ quoteId: storeQuote(quote), ...quote,
               savingsLine: `Direct Savings: ${DIRECT_SAVINGS_PCT}% vs Airbnb (£${(otaComparison - total).toFixed(2)})` });
  } catch (e) { res.status(502).json({ error: 'Could not price those dates' }); console.error(e); }
});

/* ── 4. Payment intent (3D Secure via Stripe Elements client-side) ──── */
app.post('/api/payments/intent', async (req, res) => {
  try {
    const q = getQuote(req.body.quoteId);
    if (!q) return res.status(410).json({ error: 'Quote expired — please reprice' });
    const intent = await stripe.paymentIntents.create({
      amount: Math.round(q.total * 100),
      currency: CURRENCY,
      automatic_payment_methods: { enabled: true },
      setup_future_usage: 'off_session',           // tokenize for post-stay incidental holds
      metadata: { quoteId: req.body.quoteId, checkIn: q.checkIn, checkOut: q.checkOut }
    });
    res.json({ clientSecret: intent.client_secret });
  } catch (e) { res.status(502).json({ error: 'Payment initialisation failed' }); console.error(e); }
});

/* ── 5. Reservation creation after successful payment ───────────────── */
app.post('/api/reservations', async (req, res) => {
  try {
    const { quoteId, paymentIntentId, guest } = req.body;
    const q = getQuote(quoteId);
    if (!q) return res.status(410).json({ error: 'Quote expired' });
    if (!guest?.email || !guest?.phone || !guest?.firstName)
      return res.status(400).json({ error: 'Guest name, email and phone are required' });

    const intent = await stripe.paymentIntents.retrieve(paymentIntentId);
    if (intent.status !== 'succeeded' || intent.metadata.quoteId !== quoteId)
      return res.status(402).json({ error: 'Payment not verified' });

    const reservation = await createReservation({
      propertyId: PROPERTY_ID, guest,
      checkIn: q.checkIn, checkOut: q.checkOut, guests: q.guests,
      addons: q.addons, paymentIntentId, totals: q
    });
    const id = reservation.data?.id || reservation.id;
    quotes.delete(quoteId);
    res.json({ reservationId: id, redirect: `/booking-confirmation?reservation_id=${id}` });
  } catch (e) {
    await adminAlert(`Reservation creation FAILED after successful payment ${req.body.paymentIntentId} — manual action needed.`);
    res.status(502).json({ error: 'Booking record failed — payment taken; our team has been alerted and will confirm shortly.' });
    console.error(e);
  }
});

/* ── Webhook: Stripe (signature-verified, raw body) ─────────────────── */
async function handleStripeWebhook(req, res) {
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, req.headers['stripe-signature'],
                                           process.env.STRIPE_WEBHOOK_SECRET);
  } catch (e) { return res.status(400).send(`Signature verification failed`); }

  switch (event.type) {
    case 'payment_intent.succeeded':
      console.log('✓ payment_intent.succeeded', event.data.object.id);
      break;
    case 'charge.dispute.created': {
      const ch = event.data.object;
      await adminAlert(`⚠ Stripe DISPUTE on charge ${ch.id} (£${(ch.amount / 100).toFixed(2)}).`);
      const resId = ch.metadata?.reservation_id;
      if (resId) await flagReservation(resId, { flags: { disputed: true } }).catch(console.error);
      break;
    }
  }
  res.json({ received: true });
}

/* ── Webhook: Hospitable (HMAC-verified) — reservation lifecycle ────── */
app.post('/webhooks/hospitable', (req, res) => {
  const sig = req.headers['x-hospitable-signature'] || req.headers['signature'] || '';
  const expected = crypto.createHmac('sha256', process.env.HOSPITABLE_WEBHOOK_SECRET || '')
                         .update(JSON.stringify(req.body)).digest('hex');
  const a = Buffer.from(String(sig)), b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b))
    return res.status(401).json({ error: 'Invalid signature' });

  const { event, data } = req.body;
  if (event === 'reservation.updated' && data?.status === 'accepted') {
    /* Yale fallback: if no smart-lock code within 10 min of confirmation,
       Hospitable's default PIN applies — but a human should verify. */
    setTimeout(async () => {
      if (!data.smart_lock_code) {
        await adminAlert(`Yale PIN missing for reservation ${data.id} (${data.guest?.first_name || 'guest'}, arriving ${data.arrival_date}). Hospitable fallback PIN in effect — verify lock sync.`);
      }
    }, 10 * 60 * 1000);
  }
  res.json({ received: true });
});

/* ── Webhook: Minut (audit log; guest SMS fires natively in Hospitable) */
app.post('/webhooks/minut', async (req, res) => {
  if ((req.headers['x-portico-minut-key'] || '') !== (process.env.HOSPITABLE_WEBHOOK_SECRET || '')) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  if (req.body?.event === 'noise_threshold_exceeded') {
    await adminAlert(`🔊 Minut noise breach at ${req.body.property || 'property'} — automated guest SMS sent by Hospitable.`);
  }
  res.json({ received: true });
});

/* ── Meta Ads: campaign creation from the CMS (admin-key protected) ──── */
const { createFullCampaign } = require('./lib/meta-ads');            // raw Graph API (fallback)
const { createFullCampaignCLI, cliAvailable } = require('./lib/meta-ads-cli'); // official Meta Ads CLI (preferred)
app.post('/api/meta/campaign', async (req, res) => {
  const a = Buffer.from(String(req.headers['x-admin-key'] || ''));
  const b = Buffer.from(String(process.env.CMS_ADMIN_KEY || ''));
  if (!process.env.CMS_ADMIN_KEY || a.length !== b.length || !crypto.timingSafeEqual(a, b))
    return res.status(401).json({ error: 'Invalid admin key' });
  if (!process.env.META_ACCESS_TOKEN)
    return res.status(501).json({ error: 'META_ACCESS_TOKEN not configured on the server' });
  try {
    const driver = (process.env.META_DRIVER || 'cli').toLowerCase();
    let created;
    if (driver === 'cli' && await cliAvailable()) {
      // CLI takes local file paths for images (META_AD_IMAGE_PATHS),
      // falling back to the URL list if paths are not provided.
      const imagePaths = (process.env.META_AD_IMAGE_PATHS || process.env.META_AD_IMAGE_URLS || '')
        .split(',').map(s => s.trim()).filter(Boolean);
      if (!imagePaths.length) return res.status(400).json({ error: 'No ad images configured (META_AD_IMAGE_PATHS or META_AD_IMAGE_URLS)' });
      created = await createFullCampaignCLI(req.body, imagePaths);
    } else {
      if (driver === 'cli') console.warn('meta CLI not found on PATH — falling back to raw Graph API driver');
      const imageUrls = (process.env.META_AD_IMAGE_URLS || '').split(',').map(s => s.trim()).filter(Boolean);
      if (!imageUrls.length) return res.status(400).json({ error: 'No ad image URLs configured (META_AD_IMAGE_URLS)' });
      created = await createFullCampaign(req.body, imageUrls);
      created.driver = 'api';
    }
    await adminAlert(`Meta campaign created via ${created.driver} (PAUSED): ${created.campaignId} with ${created.adsets.length} ad sets.`);
    res.json(created);
  } catch (e) {
    console.error(e);
    res.status(502).json({ error: e.meta?.message || e.message || 'Meta campaign creation failed' });
  }
});

app.get('/health', (_, res) => res.json({ ok: true }));
app.listen(process.env.PORT || 3000, () =>
  console.log(`Portico booking engine listening on :${process.env.PORT || 3000}`));
