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

/** Normalise calendar days to {date, available, price} regardless of schema variant */
function normalizeCalendar(raw) {
  const days = raw.days || raw.calendar || raw || [];
  return days.map(d => ({
    date: d.date,
    available: d.available ?? (d.status ? d.status === 'available' : true),
    price: Number(d.price?.amount ?? d.rate ?? d.price ?? 0) / (d.price?.amount ? 100 : 1)
  }));
}

/** POST /v2/reservations — create the direct booking record */
async function createReservation({ propertyId, guest, checkIn, checkOut, guests, addons, paymentIntentId, totals }) {
  return hospitable('/reservations', {
    method: 'POST',
    body: JSON.stringify({
      property_id: propertyId,
      arrival_date: checkIn,
      departure_date: checkOut,
      guests: { total: guests },
      guest: {
        first_name: guest.firstName,
        last_name: guest.lastName,
        email: guest.email,
        phone: guest.phone            // feeds Yale PIN generation (last 4–6 digits)
      },
      addons,                          // e.g. ["parking","early_checkin"]
      metadata: {
        source: 'direct-cms',
        stripe_payment_intent: paymentIntentId,
        quoted_total: totals.total
      }
    })
  });
}

/** PATCH reservation flags (e.g. payment confirmed / dispute) — verify exact
 *  endpoint & payload against current docs when wiring live. */
async function flagReservation(reservationId, flags) {
  return hospitable(`/reservations/${reservationId}`, {
    method: 'PATCH',
    body: JSON.stringify(flags)
  });
}

module.exports = { getProperty, getCalendar, createReservation, flagReservation };
