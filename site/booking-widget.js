/**
 * Portico Suites — booking widget v2.
 * Owns the full journey inside #bw-app: live calendar → date selection →
 * server quote (with voucher) → guest details → payment (Stripe when a
 * publishable key is provided) or contact-to-book fallback.
 * 100% voucher bookings complete with no card and no Stripe key at all.
 *
 *   <script src="https://js.stripe.com/v3/"></script>
 *   <script src="/booking-widget.js" data-api="https://booking.example.com"
 *           data-stripe-pk="pk_live_…"></script>   (pk optional pre-launch)
 */
(function () {
  const me = document.currentScript;
  const API = (me.dataset.api || '').replace(/\/$/, '');
  const STRIPE_PK = me.dataset.stripePk || '';
  const app = document.getElementById('bw-app');
  if (!API || !app) return;

  const PHONE = app.dataset.phone || '', EMAIL = app.dataset.email || '';
  const stripe = (STRIPE_PK && window.Stripe) ? Stripe(STRIPE_PK) : null;
  let days = {}, selIn = null, selOut = null, quote = null, elements = null, stage = 'pick';
  let view = new Date(); view.setDate(1);
  const money = (n) => '£' + Number(n).toFixed(2);
  const iso = (d) => d.toISOString().slice(0, 10);
  const esc = (s) => String(s || '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

  async function loadMonth(d) {
    const y = d.getFullYear(), m = d.getMonth();
    const start = `${y}-${String(m+1).padStart(2,'0')}-01`;
    const end = `${y}-${String(m+1).padStart(2,'0')}-${String(new Date(y,m+1,0).getDate()).padStart(2,'0')}`;
    if (days['loaded-'+start]) return;
    const r = await fetch(`${API}/api/calendar?start=${start}&end=${end}`);
    const j = await r.json();
    (j.days || []).forEach(x => days[x.date] = x);
    days['loaded-'+start] = true;
  }
  function rangeOk(a, b) {
    for (let d = new Date(a); iso(d) < b; d.setDate(d.getDate()+1)) {
      const x = days[iso(d)];
      if (!x || !x.available) return false;
    }
    return true;
  }
  async function fetchQuote() {
    if (!selIn || !selOut) return;
    const vc = (document.getElementById('bw-promo') ? document.getElementById('bw-promo').value : '').trim();
    const r = await fetch(`${API}/api/quote`, { method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ checkIn: selIn, checkOut: selOut, guests: gCount, voucherCode: vc || undefined }) });
    const j = await r.json();
    if (!r.ok) { quote = null; render(notice(j.error || 'Those dates are unavailable.')); return; }
    quote = j; stage = 'quote'; elements = null; render();
  }

  let gCount = 2;
  const notice = (t) => `<div class="bw-notice">${esc(t)}</div>`;

  function calendarHTML() {
    const y = view.getFullYear(), m = view.getMonth();
    const title = view.toLocaleString('en-GB', { month:'long', year:'numeric' });
    const first = (new Date(y, m, 1).getDay() + 6) % 7;
    const nDays = new Date(y, m+1, 0).getDate();
    const today = iso(new Date());
    let cells = ['Mo','Tu','We','Th','Fr','Sa','Su'].map(d => `<div class="dow">${d}</div>`).join('');
    for (let i = 0; i < first; i++) cells += '<div class="day blank"></div>';
    for (let d = 1; d <= nDays; d++) {
      const ds = `${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      const info = days[ds];
      const past = ds < today;
      const booked = past || (info && !info.available);
      let cls = 'day' + (booked ? ' booked' : ' free');
      if (selIn && ds === selIn) cls += ' sel';
      if (selOut && ds === selOut) cls += ' sel';
      if (selIn && selOut && ds > selIn && ds < selOut) cls += ' inr';
      cells += `<div class="${cls}" data-d="${ds}">${d}</div>`;
    }
    return `<div class="cal-head"><button type="button" data-nav="-1" aria-label="Previous month">‹</button>
      <span class="cal-title">${title}</span>
      <button type="button" data-nav="1" aria-label="Next month">›</button></div>
      <div class="cal-grid">${cells}</div>
      <p class="bw-hint">Select your arrival night, then your departure day.</p>`;
  }

  function summaryHTML() {
    if (!quote) return `<div class="row"><span>Select dates on the calendar</span><span></span></div>
      <div class="row"><span>Guests</span><span>${gCount}</span></div>`;
    const q = quote;
    return `
      <div class="row"><span>${q.checkIn} → ${q.checkOut}</span><span>${q.nights} night${q.nights>1?'s':''} · ${q.guests} guests</span></div>
      <div class="row"><span>Accommodation</span><span>${money(q.subtotal)}</span></div>
      <div class="row"><span>Cleaning fee</span><span>${money(q.cleaningFee)}</span></div>
      ${q.tax ? `<div class="row"><span>Taxes</span><span>${money(q.tax)}</span></div>` : ''}
      ${q.voucher ? `<div class="row" style="color:#8A6A3B;font-weight:600"><span>Voucher ${esc(q.voucher.label)} (−${q.voucher.pct}%)</span><span>−${money(q.voucher.discount)}</span></div>` : ''}
      ${q.savingsLine ? `<div class="row" style="color:#7d9471;font-weight:600"><span>✓ ${esc(q.savingsLine.split(':')[0])}</span><span>${esc((q.savingsLine.split('(')[1]||'').replace(')',''))} saved</span></div>` : ''}
      <div class="row total"><span>Total</span><span>${money(q.total)}</span></div>
      <div class="bw-promo"><input id="bw-promo" placeholder="Voucher code" value="${q.voucher ? esc(q.voucher.code) : ''}">
      <button type="button" id="bw-apply">Apply</button></div>`;
  }

  function formHTML() {
    if (!quote) return '';
    const free = quote.total <= 0 && quote.voucher && quote.voucher.pct === 100;
    const canPay = !!stripe;
    let action;
    if (free) action = `<button class="btn gold bw-cta" id="bw-go">Confirm Booking — No Payment Needed</button>`;
    else if (canPay && stage === 'pay') action = `<div id="bw-payment"></div><button class="btn gold bw-cta" id="bw-go">Confirm &amp; Pay Securely</button>`;
    else if (canPay) action = `<button class="btn gold bw-cta" id="bw-go">Continue to Secure Payment</button>`;
    else action = `<div class="bw-notice" style="border-color:#C4A55E;color:#6b5a33">Secure card checkout is launching shortly. To book these dates now:
      ${PHONE ? `<a href="tel:${esc(PHONE.replace(/\s/g,''))}">${esc(PHONE)}</a> · ` : ''}
      <a href="mailto:${esc(EMAIL)}?subject=${encodeURIComponent('Booking request '+quote.checkIn+' to '+quote.checkOut)}&body=${encodeURIComponent('Dates: '+quote.checkIn+' → '+quote.checkOut+'\nGuests: '+gCount+'\nQuoted total: £'+quote.total)}">${esc(EMAIL || 'email us')}</a></div>`;
    return `<div class="bw-form">
      <div class="bw-2"><input id="bw-fn" placeholder="First name" autocomplete="given-name"><input id="bw-ln" placeholder="Last name" autocomplete="family-name"></div>
      <input id="bw-em" type="email" placeholder="Email address" autocomplete="email">
      <input id="bw-ph" type="tel" placeholder="Mobile number" autocomplete="tel">
      ${action}<div id="bw-msg"></div>
      <p class="secure-note" style="margin-top:14px">256-bit SSL · Powered by Stripe · Instant confirmation</p></div>`;
  }

  function render(extra) {
    app.innerHTML = `<div class="bw-cols">
      <div class="bw-cal checkout-card">${calendarHTML()}
        <div class="bw-guests"><span>Guests</span>
          <div class="guest-counter"><button type="button" data-g="-1" aria-label="Fewer guests">−</button><b id="bw-g">${gCount}</b><button type="button" data-g="1" aria-label="More guests">+</button></div></div>
      </div>
      <div class="checkout-card bw-sum">${summaryHTML()}${formHTML()}${extra || ''}</div>
    </div>`;
    wire();
  }

  function wire() {
    app.querySelectorAll('[data-nav]').forEach(b => b.onclick = async () => {
      view.setMonth(view.getMonth() + parseInt(b.dataset.nav));
      await loadMonth(view); render();
    });
    app.querySelectorAll('.day.free').forEach(el => el.onclick = () => pick(el.dataset.d));
    app.querySelectorAll('[data-g]').forEach(b => b.onclick = () => {
      gCount = Math.min(10, Math.max(1, gCount + parseInt(b.dataset.g)));
      quote ? fetchQuote() : render();
    });
    const ap = document.getElementById('bw-apply'); if (ap) ap.onclick = fetchQuote;
    const pr = document.getElementById('bw-promo'); if (pr) pr.onkeydown = e => { if (e.key === 'Enter') fetchQuote(); };
    const go = document.getElementById('bw-go'); if (go) go.onclick = proceed;
  }

  function pick(ds) {
    if (!selIn || (selIn && selOut)) { selIn = ds; selOut = null; quote = null; stage = 'pick'; render(); return; }
    if (ds <= selIn) { selIn = ds; render(); return; }
    if (!rangeOk(selIn, ds)) { selIn = ds; selOut = null; render(notice('That range includes a booked night — pick a fresh arrival date.')); return; }
    selOut = ds; render(); fetchQuote();
  }

  function guest() {
    const g = { firstName: v('bw-fn'), lastName: v('bw-ln'), email: v('bw-em'), phone: v('bw-ph') };
    if (!g.firstName || !g.email || !g.phone) { msg('Please complete name, email and mobile number.'); return null; }
    return g;
  }
  const v = (id) => { const el = document.getElementById(id); return el ? el.value.trim() : ''; };
  const msg = (t) => { const m = document.getElementById('bw-msg'); if (m) m.innerHTML = notice(t); };

  async function proceed() {
    const free = quote.total <= 0 && quote.voucher && quote.voucher.pct === 100;
    const btn = document.getElementById('bw-go');
    if (free) return reserve(null, btn);
    if (stage !== 'pay') {
      if (!guest()) return;
      btn.disabled = true; btn.textContent = 'Preparing secure payment…';
      const r = await fetch(`${API}/api/payments/intent`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ quoteId: quote.quoteId }) });
      const j = await r.json();
      if (j.free) return reserve(null, btn);
      if (!r.ok || !j.clientSecret) { btn.disabled = false; btn.textContent = 'Continue to Secure Payment'; return msg(j.error || 'Could not start payment.'); }
      const fn = v('bw-fn'), ln = v('bw-ln'), em = v('bw-em'), ph = v('bw-ph');
      stage = 'pay'; render();
      ['bw-fn','bw-ln','bw-em','bw-ph'].forEach((id, i) => { const el = document.getElementById(id); if (el) el.value = [fn,ln,em,ph][i]; });
      elements = stripe.elements({ clientSecret: j.clientSecret });
      elements.create('payment').mount('#bw-payment');
      return;
    }
    const g = guest(); if (!g) return;
    btn.disabled = true; btn.textContent = 'Processing…';
    const { error, paymentIntent } = await stripe.confirmPayment({ elements, redirect: 'if_required',
      confirmParams: { payment_method_data: { billing_details: { name: `${g.firstName} ${g.lastName}`, email: g.email, phone: g.phone } } } });
    if (error) { msg(error.message); btn.disabled = false; btn.textContent = 'Confirm & Pay Securely'; return; }
    reserve(paymentIntent.id, btn, g);
  }

  async function reserve(intentId, btn, g) {
    g = g || guest(); if (!g) { if (btn) { btn.disabled = false; } return; }
    if (btn) { btn.disabled = true; btn.textContent = 'Confirming…'; }
    const r = await fetch(`${API}/api/reservations`, { method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ quoteId: quote.quoteId, paymentIntentId: intentId, guest: g }) });
    const j = await r.json();
    if (r.ok) location.href = j.redirect || `/booking-confirmation/?reservation_id=${j.reservationId || ''}`;
    else { msg(j.error || 'Could not complete the booking.'); if (btn) { btn.disabled = false; btn.textContent = 'Try Again'; } }
  }

  function heroSync() {
    const ci = document.getElementById('checkin'), co = document.getElementById('checkout');
    if (!ci || !co || !ci.value || !co.value || co.value <= ci.value) return;
    const gc = document.getElementById('guestCount');
    if (gc) gCount = Math.min(10, Math.max(1, parseInt(gc.textContent) || 2));
    selIn = ci.value; selOut = co.value; view = new Date(selIn); view.setDate(1);
    loadMonth(view).then(() => {
      if (!rangeOk(selIn, selOut)) { selOut = null; render(notice('Some of those nights are booked — pick alternatives on the calendar.')); }
      else { render(); fetchQuote(); }
    });
  }
  const sb = document.querySelector('.search-bar');
  if (sb) sb.addEventListener('submit', () => setTimeout(heroSync, 50));

  loadMonth(view).then(() => { const n = new Date(view); n.setMonth(n.getMonth()+1); return loadMonth(n); })
    .then(render)
    .catch(() => { const f = app.querySelector('.bw-fallback-note'); if (f) f.insertAdjacentHTML('beforeend',
      '<p style="color:#a04b3a;font-size:13px">Live availability is briefly unreachable — please use the phone or email above.</p>'); });
})();
