# Portico Suites — Hospitable Automated Messaging Templates
Paste into Hospitable → Messaging → Rules. Variables use Hospitable's %...% mapping.

---

## Template A — Check-In & Access Keycode Delivery
**Trigger:** Reservation Status = `Verified` (Duve check-in complete) AND Timing = `24 hours before check-in`
**Channel:** SMS/WhatsApp + email copy

```
Hi %guest_first_name%! We are looking forward to hosting you at %property_name%.

Your check-in is scheduled for tomorrow at %check_in_time%.

🔑 KEYLESS ACCESS INSTRUCTIONS:
1. Located at the entrance keypad of suite %unit_number%.
2. Touch the keypad to illuminate numbers.
3. Enter your unique access PIN: %smart_lock_code% followed by the # key.

📶 Wi-Fi Details:
Network: %wifi_network%
Password: %wifi_password%

If you need anything prior to arrival, please let us know!

— Portico Suites, Franklin Road · Harrogate
```

**Guard:** rule must require Verified status — guests who have not completed the
Duve ID + selfie + deposit flow never receive the PIN.

---

## Template B — Minut Noise Threshold Breach
**Trigger:** Minut webhook event = `noise_threshold_exceeded`
(threshold: >75 dB sustained 10 min, 11:00 PM–7:00 AM)
**Channel:** SMS

```
Hi %guest_first_name%, hope you're having a great evening! Our quiet hours system detected a sustained noise level rise at %property_name%.

Out of respect for neighbouring residents, our quiet hours run from 11:00 PM to 7:00 AM. We appreciate your assistance in keeping noise levels to a minimum!

— Portico Suites
```

---

## Template C (recommended addition) — Verification Nudge
**Trigger:** 48 hours before check-in AND Status ≠ Verified
```
Hi %guest_first_name%, your stay at %property_name% is almost here! To receive your door entry code, please complete quick online check-in (ID + a few details) via the secure link Duve sent you. It takes about 3 minutes. Need the link again? Just reply here.
```

## Template D (recommended addition) — Departure & Review
**Trigger:** 10:30 AM on departure date
```
Thank you for staying at %property_name%, %guest_first_name%! We hope Harrogate treated you well. Doors lock automatically at check-out — no need to do anything. If you enjoyed your stay, a short review means the world to a small independent host. Safe travels!
```
