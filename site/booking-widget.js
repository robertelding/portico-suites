/**
 * Portico Suites — live booking widget.
 * Drop into the exported website before </body>:
 *   <script src="https://js.stripe.com/v3/"></script>
 *   <script src="booking-widget.js"
 *           data-api="https://booking.porticosuites.com"
 *           data-stripe-pk="pk_live_..."></script>
 *
 * Upgrades the CMS-exported page in place:
 *  - demo availability calendar → live Hospitable calendar
 *  - checkout card → real quote breakdown + Stripe Elements + 3DS payment
 *  - on success → POST reservation → redirect /booking-confirmation?reservation_id=
 */
(function () {
  const me = document.currentScript;
  const API = (me.dataset.api || '').replace(/\/$/, '');
  const STRIPE_PK = me.dataset.stripePk;
  if (!API || !STRIPE_PK) { console.warn('booking-widget: data-api / data-stripe-pk missing — demo mode stays active'); return; }

  const $ = (id) => document.getElementById(id);
  const stripe = Stripe(STRIPE_PK);
  let elements, quote = null, liveDays = {};

  /* ── Live calendar ─────────────────────────────────────────────── */
  async function loadMonth(y, m) {
    const start = `${y}-${String(m + 1).padStart(2, '0')}-01`;
    const endD = new Date(y, m + 1, 0).getDate();
    const end = `${y}-${String(m + 1).padStart(2, '0')}-${String(endD).padStart(2, '0')}`;
    try {
      const r = await fetch(`${API}/api/calendar?start=${start}&end=${end}`);
      const { days } = await r.json();
      (days || []).forEach(d => liveDays[d.date] = d);
      paintCalendar();
    } catch (e) { console.warn('calendar fetch failed', e); }
  }
  function paintCalendar() {
    document.querySelectorAll('#calGrid .day:not(.blank)').forEach(el => {
      const title = $('calTitle')?.textContent || '';
      const dt = new Date(`1 ${title}`);
      if (isNaN(dt)) return;
      const iso = `${dt.getFullYear()}-${String(dt.getMonth() + 1).padStart(2, '0')}-${String(el.textContent).padStart(2, '0')}`;
      const day = liveDays[iso];
      if (day) el.classList.toggle('booked', !day.available);
    });
  }
  const origChange = window.changeMonth;
  window.changeMonth = function (d) {
    origChange && origChange(d);
    const t = new Date(`1 ${$('calTitle').textContent}`);
    loadMonth(t.getFullYear(), t.getMonth());
  };

  /* ── Quote + checkout upgrade ──────────────────────────────────── */
  const card = document.querySelector('.checkout-card');
  async function reprice() {
    const ci = $('checkin')?.value, co = $('checkout')?.value;
    if (!ci || !co || co <= ci) return;
    const guests = parseInt(($('guestCount')?.textContent || '2')) || 2;
    const r = await fetch(`${API}/api/quote`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ checkIn: ci, checkOut: co, guests })
    });
    const q = await r.json();
    if (!r.ok) { renderNotice(q.error || 'Those dates are unavailable.'); quote = null; return; }
    quote = q;
    renderQuote();
  }
  function money(n) { return '£' + Number(n).toFixed(2); }
  function renderNotice(msg) {
    const n = card.querySelector('.bw-notice') || card.insertBefore(Object.assign(document.createElement('p'), { className: 'bw-notice' }), card.firstChild.nextSibling);
    n.textContent = msg; n.style.cssText = 'color:#8c4a35;font-size:13px;margin:8px 0';
  }
  function renderQuote() {
    card.querySelector('.bw-notice')?.remove();
    card.querySelectorAll('.row').forEach(r => r.remove());
    card.querySelector('.bw-rows')?.remove();
    const rows = document.createElement('div'); rows.className = 'bw-rows';
    rows.innerHTML = `
      <div class="row"><span>${quote.checkIn} → ${quote.checkOut}</span><span>${quote.nights} night${quote.nights > 1 ? 's' : ''} · ${quote.guests} guests</span></div>
      <div class="row"><span>Accommodation</span><span>${money(quote.subtotal)}</span></div>
      <div class="row"><span>Cleaning fee</span><span>${money(quote.cleaningFee)}</span></div>
      ${quote.tax ? `<div class="row"><span>Taxes</span><span>${money(quote.tax)}</span></div>` : ''}
      <div class="row" style="color:#7d9471;font-weight:600"><span>✓ ${quote.savingsLine.split(':')[0]}</span><span>${quote.savingsLine.split('(')[1]?.replace(')', '') || ''} saved</span></div>
      <div class="row total"><span>Total</span><span>${money(quote.total)}</span></div>`;
    card.insertBefore(rows, card.querySelector('.pay-methods'));
    mountStripe();
  }

  /* ── Stripe Elements + guest details ───────────────────────────── */
  function mountStripe() {
    if ($('bw-payment')) return;
    const pay = card.querySelector('.pay-methods');
    pay.style.display = 'none';
    const wrap = document.createElement('div');
    wrap.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:6px 0 12px">
        <input id="bw-fn" placeholder="First name" style="padding:12px;border:1px solid #DCD4C2;border-radius:4px">
        <input id="bw-ln" placeholder="Last name"  style="padding:12px;border:1px solid #DCD4C2;border-radius:4px">
        <input id="bw-em" placeholder="Email" type="email" style="grid-column:1/3;padding:12px;border:1px solid #DCD4C2;border-radius:4px">
        <input id="bw-ph" placeholder="Mobile (for smart-lock entry code)" type="tel" style="grid-column:1/3;padding:12px;border:1px solid #DCD4C2;border-radius:4px">
      </div>
      <div id="bw-payment" style="margin:0 0 14px"></div>`;
    card.insertBefore(wrap, card.querySelector('.btn'));
    fetch(`${API}/api/payments/intent`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quoteId: quote.quoteId })
    }).then(r => r.json()).then(({ clientSecret, error }) => {
      if (error) return renderNotice(error);
      elements = stripe.elements({ clientSecret });
      elements.create('payment').mount('#bw-payment');
      wireConfirm(clientSecret);
    });
  }

  function wireConfirm(clientSecret) {
    const btn = card.querySelector('.btn');
    btn.onclick = async () => {
      const guest = { firstName: $('bw-fn').value.trim(), lastName: $('bw-ln').value.trim(),
                      email: $('bw-em').value.trim(), phone: $('bw-ph').value.trim() };
      if (!guest.firstName || !guest.email || !guest.phone) return renderNotice('Please complete name, email and mobile number.');
      btn.disabled = true; btn.textContent = 'Processing…';
      const { error, paymentIntent } = await stripe.confirmPayment({
        elements, redirect: 'if_required',
        confirmParams: { payment_method_data: { billing_details: { name: `${guest.firstName} ${guest.lastName}`, email: guest.email, phone: guest.phone } } }
      });
      if (error) { renderNotice(error.message); btn.disabled = false; btn.textContent = 'Confirm & Pay Securely'; return; }
      const r = await fetch(`${API}/api/reservations`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quoteId: quote.quoteId, paymentIntentId: paymentIntent.id, guest })
      });
      const out = await r.json();
      if (r.ok) location.href = out.redirect;
      else { renderNotice(out.error); btn.disabled = false; btn.textContent = 'Confirm & Pay Securely'; }
    };
  }

  ['checkin', 'checkout'].forEach(id => $(id)?.addEventListener('change', reprice));
  const t0 = new Date();
  loadMonth(t0.getFullYear(), t0.getMonth());
})();
