/**
 * Signed voucher codes — stateless, storage-free.
 * Code format:  LABEL-PCT-YYMMDD-SIG6
 *   e.g.  SARAH-100-261231-A7F3B2   (100% off, valid until 31 Dec 2026)
 * SIG6 = first 6 hex chars (uppercase) of HMAC-SHA256(VOUCHER_SECRET, "LABEL|PCT|YYMMDD").
 * Generated in the CMS Vouchers panel with the same secret; verified here.
 * Notes: codes are private links, expiry-bound; single-use enforcement would
 * need storage — revoke everything by rotating VOUCHER_SECRET.
 */
const crypto = require('crypto');

function sig(secret, label, pct, yymmdd) {
  return crypto.createHmac('sha256', secret)
    .update(`${label}|${pct}|${yymmdd}`)
    .digest('hex').slice(0, 6).toUpperCase();
}

/** Returns { label, pct } for a valid, unexpired code; null otherwise. */
function verifyVoucher(code, secret) {
  if (!secret || !code) return null;
  const m = String(code).trim().toUpperCase()
    .match(/^([A-Z0-9]{2,16})-(\d{1,3})-(\d{6})-([A-F0-9]{6})$/);
  if (!m) return null;
  const [, label, pctStr, yymmdd, given] = m;
  const pct = parseInt(pctStr, 10);
  if (pct < 1 || pct > 100) return null;
  const expected = sig(secret, label, pct, yymmdd);
  const a = Buffer.from(given), b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  const expiry = new Date(`20${yymmdd.slice(0,2)}-${yymmdd.slice(2,4)}-${yymmdd.slice(4,6)}T23:59:59Z`);
  if (isNaN(expiry) || expiry < new Date()) return null;
  return { label, pct };
}

module.exports = { verifyVoucher, sig };
