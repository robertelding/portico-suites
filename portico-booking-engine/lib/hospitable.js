/**
 * Hospitable Public API v2 client (Personal Access Token auth).
 * Docs: https://developer.hospitable.com — verify exact response schemas
 * against current docs at integration time; field names below follow the
 * developer brief and are normalised in one place (normalizeCalendar) so
 * schema drift only ever needs fixing here.
 */
const BASE = process.env.HOSPITABLE_API_BASE || 'https://public.api.hospitable.com/v2';
const TOKEN = process.env.HOSPITABLE_TOKEN;

async function hospitable(path, options = {}) {
  const res = await fetch(BASE + path, {
    ...options,
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...(options.headers || {})
    }
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(`Hospitable ${res.status} on ${path}: ${JSON.stringify(body).slice(0, 300)}`);
    err.status = res.status;
    err.body = body;
    throw err;
  }
  return body;
}

/** GET /v2/properties — listing details, amenities, base pricing, occupancy */
async function getProperty(propertyId) {
  const data = await hospitable(`/properties/${propertyId}`);
  return data.data || data;
}

/** GET /v2/properties/{id}/calendar — night-by-night availability + rates */
async function getCalendar(propertyId, startDate, endDate) {
  const q = new URLSearchParams({ start_date: startDate, end_date: endDate });
  const data = await hospitable(`/properties/${propertyId}/calendar?${q}`);
  return normalizeCalendar(data.data || data);
}

/** Normalise calendar days to {date, available, price, minStay, closedForCheckin,
 *  closedForCheckout}. Live schema (checked Nov 2026): each day has
 *  status: { available: bool, reason }, price: { amount: <pence> }, min_stay. */
function normalizeCalendar(raw) {
  const days = raw.days || raw.calendar || raw || [];
  return days.map(d => {
    const st = d.status;
    const available = d.available ??
      (st && typeof st === 'object' ? !!st.available : st ? st === 'available' : true);
    return {
      date: d.date,
      available,
      price: Number(d.price?.amount ?? d.rate ?? d.price ?? 0) / (d.price?.amount ? 100 : 1),
      minStay: Number(d.min_stay) || 1,
      closedForCheckin: !!d.closed_for_checkin,
      closedForCheckout: !!d.closed_for_checkout
    };
  });
}

const pence = (n) => Math.round((Number(n) || 0) * 100);

/** Split what the guest actually paid into Hospitable's financial lines
 *  (minor units). Any voucher discount comes off the accommodation line. */
function buildFinancials(totals, currency) {
  const total = Number(totals.total) || 0;
  const cleaning = Number(totals.cleaningFee) || 0;
  const addons = (totals.addonItems || []).filter(a => a.amount > 0);
  const addonTotal = addons.reduce((s, a) => s + a.amount, 0);
  const f = { currency: String(currency || 'gbp').toUpperCase(), accommodation: pence(total) };
  if (total > 0 && total - cleaning - addonTotal >= 0) {
    f.accommodation = pence(total - cleaning - addonTotal);
    if (cleaning) f.cleaning_fee = pence(cleaning);
    if (addons.length) f.other_fees = addons.map(a => ({ label: a.label, amount: pence(a.amount) }));
  }
  return f;
}

/** POST /v2/reservations — create the direct booking as a manual reservation.
 *  Body follows Hospitable's manual-reservation schema: property UUID,
 *  check_in/check_out, guests.adults, guest (last_name required), language,
 *  financials in minor units. There is no metadata field, so the Stripe
 *  payment reference goes in the internal note. */
async function createReservation({ propertyId, guest, checkIn, checkOut, guests, addons, paymentIntentId, totals, currency }) {
  const note = [
    'Direct booking via porticosuites.com.',
    paymentIntentId ? `Stripe payment ${paymentIntentId}, paid £${Number(totals.total).toFixed(2)}.`
                    : 'No payment taken (100% voucher).',
    totals.voucher ? `Voucher: ${totals.voucher}.` : '',
    addons && addons.length ? `Add-ons: ${addons.join(', ')}.` : ''
  ].filter(Boolean).join(' ');
  return hospitable('/reservations', {
    method: 'POST',
    body: JSON.stringify({
      property_id: propertyId,
      check_in: checkIn,
      check_out: checkOut,
      guests: { adults: Math.max(1, Number(guests) || 1) },
      guest: {
        first_name: guest.firstName,
        last_name: guest.lastName || '-',
        email: guest.email,
        phone: guest.phone            // feeds Yale PIN generation (last 4–6 digits)
      },
      language: 'en',
      channel: 'direct',
      notes: note,
      financials: buildFinancials(totals, currency)
    })
  });
}

/** Replace a reservation's internal note (partial update; used to mark disputes).
 *  The public API accepts a notes-only update on manual reservations. */
async function setReservationNote(reservationId, notes) {
  const body = JSON.stringify({ notes });
  try {
    return await hospitable(`/reservations/${reservationId}`, { method: 'PATCH', body });
  } catch (e) {
    if (e.status !== 405) throw e;
    return hospitable(`/reservations/${reservationId}`, { method: 'PUT', body });
  }
}

module.exports = { getProperty, getCalendar, createReservation, setReservationNote, buildFinancials, normalizeCalendar };
