import json, datetime, os
BASE='https://porticosuites.com'; IMG=f'{BASE}/images'; TODAY=datetime.date.today().isoformat()
import pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
SITE=ROOT/'site'
CSS=(ROOT/'tools'/'page.css').read_text()
P=lambda *ps:"".join(f"<p>{x}</p>" for x in ps)
T=lambda *i:"<ul class='ticks'>"+"".join(f"<li>{x}</li>" for x in i)+"</ul>"
USP="Sleeps 10 · 7 bedrooms · 5 bathrooms · 3 minutes' walk to Harrogate Convention Centre · central Franklin Road"

def page(pg, all_pages):
    sibs=[o for o in all_pages if o['cluster']==pg['cluster'] and o['slug']!=pg['slug']][:4]
    hubs=[o for o in all_pages if o.get('hub') and o['slug']!=pg['slug']][:3]
    others={o['slug']:o for o in sibs+hubs}; others=list(others.values())[:6]
    faq_ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in pg['faqs']]}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Portico Suites","item":BASE+"/"},{"@type":"ListItem","position":2,"name":pg['h1'],"item":f"{BASE}/{pg['slug']}/"}]}
    secs="".join(f"""<section><div class="wrap"><div class="grid2">
<div><div class="eyebrow">{pg['eyebrow']}</div><h2>{s['h2']}</h2><div class="rule"></div>{s['body']}</div>
<img src="{IMG}/{s['img']}" alt="{s['alt']}" loading="lazy"></div></div></section>""" for s in pg['sections'])
    faqs="".join(f"<dt>{q}</dt><dd>{a}</dd>" for q,a in pg['faqs'])
    links="".join(f"<a href='/{o['slug']}/'>{o['nav']}</a>" for o in others)
    return f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{pg['title']}</title><meta name="description" content="{pg['desc']}">
<link rel="canonical" href="{BASE}/{pg['slug']}/">
<meta property="og:title" content="{pg['title']}"><meta property="og:description" content="{pg['desc']}">
<meta property="og:image" content="{IMG}/portico-suites-exterior-franklin-road.jpg">
<meta property="og:url" content="{BASE}/{pg['slug']}/"><meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(faq_ld)}</script>
<script type="application/ld+json">{json.dumps(crumb)}</script>
<style>{CSS}</style></head><body>
<nav><a class="brand" href="/">PORTICO SUITES</a><a class="cta" href="/#book">Check Availability</a></nav>
<header class="hero" style="background:linear-gradient(rgba(40,50,36,.58),rgba(40,50,36,.74)),url('{IMG}/{pg['hero_img']}') center/cover no-repeat">
<div><div class="eyebrow">{pg['eyebrow']}</div><h1>{pg['h1']}</h1><p>{pg['intro']}</p>
<a class="cta gold" href="/#book">Check Availability &amp; Book Direct</a></div></header>
{secs}
<section style="padding-top:0"><div class="wrap faq"><div class="eyebrow">Quick Answers</div><h2>Frequently Asked</h2><div class="rule"></div><dl>{faqs}</dl></div></section>
<div class="band" id="availability"><h2>{USP.split(' · ')[0]} · {USP.split(' · ')[1]}</h2><p>{USP}. Book directly for the guaranteed best rate — no platform fees, instant confirmation.</p><a class="cta gold" href="/#book">Check Availability</a></div>
<section><div class="wrap"><div class="eyebrow">Related Guides</div><div class="linkrow">{links}<a href="/">← Portico Suites home</a></div></div></section>
<footer>PORTICO SUITES · Franklin Road, Harrogate HG1 5EN · <a href="/">porticosuites.com</a> · <a href="/#book">Book Direct</a></footer>
</body></html>"""

# image cycles per cluster
I_LIV='portico-suites-living-room-bay-window.jpg'; I_FIRE='portico-suites-living-room-fireplace.jpg'
I_SOFA='portico-suites-living-room-leather-sofa.jpg'; I_TV='portico-suites-living-room-tv-lounge.jpg'
I_KIT='portico-suites-dining-kitchen.jpg'; I_TAB='portico-suites-dining-kitchen-table.jpg'
I_EXT='portico-suites-exterior-franklin-road.jpg'; I_GAR='portico-suites-garden-terrace.jpg'
I_FLR='portico-suites-floorplan.jpg'
A_KNA='attraction-knaresborough-viaduct.jpg'; A_FTN='attraction-fountains-abbey.jpg'
A_BRM='attraction-brimham-rocks.jpg'; A_FEW='attraction-fewston-reservoir.jpg'
A_HRW='attraction-harewood-house.jpg'; A_RIP='attraction-ripley-castle.jpg'
BEDS=['portico-suites-bedroom-principal.jpg','portico-suites-bedroom-mustard.jpg','portico-suites-bedroom-garnet.jpg','portico-suites-bedroom-sage.jpg','portico-suites-bedroom-silver.jpg','portico-suites-bedroom-slate.jpg']

HCC3="Portico Suites is about a 3-minute walk from the Harrogate Convention Centre."
STD_FAQS=[("How many people can stay?","Up to 10 guests across 7 bedrooms with 5 bathrooms, 4 of them en-suite."),
("How close is the Convention Centre?",HCC3),
("Why book direct?","Booking directly on porticosuites.com always carries our best rate — no platform fees — with instant confirmation.")]

def event(slug,nav,event_name,season,angle,img,extra_faq=None):
    return dict(slug=slug,nav=nav,cluster='hcc',
    title=f"{event_name} Accommodation — 3 Min Walk to HCC | Portico Suites Harrogate",
    desc=f"Staying for {event_name}? Portico Suites is a 3-minute walk from Harrogate Convention Centre — 7 bedrooms, sleeps 10. House your whole team. Book direct.",
    eyebrow='Harrogate Convention Centre', h1=f"Accommodation for {event_name}",
    intro=f"{angle} Portico Suites puts your whole team a 3-minute walk from the halls — 7 private bedrooms, one booking.",
    hero_img=img, sections=[
    dict(h2='Three Minutes Door to Door', img=I_EXT, alt=f'House near Harrogate Convention Centre for {event_name}',
     body=P(f"When {event_name} comes to Harrogate{', '+season if season else ''}, accommodation near the Convention Centre disappears fast. Franklin Road is about three minutes on foot from the HCC entrances — closer than most of the car parks — so setup mornings and breakdown evenings stop being a logistics problem.",
     "Seven separate bedrooms mean exhibitors, reps and crew each get their own room and en-suite where available; the oak dining table doubles as the stand-planning desk.")+
     T("3 minutes' walk to HCC","7 private bedrooms · sleeps 10","Fast Wi-Fi &amp; workspace","Full kitchen for show-day starts","One direct booking for the whole team")),
    ],
    faqs=[(f"Where can a team stay for {event_name}?",f"Portico Suites on Franklin Road sleeps up to 10 in 7 separate bedrooms, about a 3-minute walk from the Harrogate Convention Centre."),
    ("Can we book the full show week including build-up days?","Yes — full-week and multi-week bookings around events are welcome. Book early: event weeks sell out well ahead."),
    ]+([extra_faq] if extra_faq else [])+[STD_FAQS[2]])

PAGES=[
# ---- HUBS (6, updated with 3-min) ----
dict(slug='harrogate-convention-centre-accommodation',nav='Convention Centre Stays',cluster='hcc',hub=True,
 title='Accommodation Near Harrogate Convention Centre — 3 Min Walk | Portico Suites',
 desc='Group accommodation a 3-minute walk from Harrogate Convention Centre. 7 bedrooms, sleeps 10 — ideal for exhibitors, delegates and event crews. Book direct.',
 eyebrow='Harrogate Convention Centre', h1='Accommodation Near Harrogate Convention Centre',
 intro='Seven bedrooms, five bathrooms and a full working kitchen — about three minutes on foot from the HCC halls. Skip the hotel-block scramble and house your whole team under one roof.',
 hero_img=I_EXT, sections=[
 dict(h2='Three Minutes to the Halls', img=I_LIV, alt='Sitting room at Portico Suites near Harrogate Convention Centre',
  body=P("Portico Suites sits on Franklin Road, about a 3-minute walk from the Harrogate Convention Centre — closer than most of its car parks. No shuttle timetables, and back at base moments after the halls close.",
  "For exhibitions, conferences and trade shows, the house takes the entire team: seven separate bedrooms mean nobody shares, and everyone stays together for the working week.")+
  T("3 minutes' walk to HCC","7 separate bedrooms — no sharing","Fast Wi-Fi throughout","Full kitchen for early starts &amp; late finishes")),
 dict(h2='Built for the Working Week', img=I_KIT, alt='Large dining kitchen workspace at Portico Suites Harrogate',
  body=P("The oak dining table seats the whole party for breakfast briefings or an evening debrief — genuinely useful space when a stand needs re-planning at 9pm.",
  "Monday-to-Thursday stays are our core midweek pattern, and multi-week event bookings are welcome. Booking direct means one straightforward payment for the whole house — simpler for expenses than ten separate hotel rooms."))],
 faqs=[("How far is Portico Suites from Harrogate Convention Centre?","About a 3-minute walk — the house is on Franklin Road, closer to the halls than most HCC car parks."),
 STD_FAQS[0],("Can we book for a full exhibition week?","Yes — midweek, full-week and multi-week bookings are all available. Book direct for the best rate."),
 ("Is there space to work?","Fast Wi-Fi runs throughout, and the large oak dining table comfortably seats the whole team.")]),

dict(slug='corporate-accommodation-harrogate',nav='Corporate Accommodation',cluster='corporate',hub=True,
 title='Corporate & Contractor Accommodation in Harrogate | Portico Suites',
 desc='Corporate accommodation in central Harrogate for project teams and contractors. 7 bedrooms, sleeps 10, fast Wi-Fi, one simple direct booking.',
 eyebrow='Corporate Stays', h1='Corporate Accommodation in Harrogate',
 intro='One house, one booking, seven private bedrooms — a smarter alternative to a block of hotel rooms for project teams, contractors and relocations.',
 hero_img=I_FIRE, sections=[
 dict(h2='Why Teams Choose a House', img=BEDS[5], alt='Private double bedroom for corporate stays in Harrogate',
  body=P("Hotel blocks split your team across floors and add per-room admin. Portico Suites keeps everyone together with seven separate bedrooms — most with en-suite bathrooms — and shared spaces that make a working week feel less like living out of a suitcase.",
  "Central Harrogate means restaurants, supermarkets and the rail station are minutes away on foot, and the A1(M) and A61 are an easy drive for site work across North Yorkshire.")+
  T("7 private bedrooms · 5 bathrooms","Sleeps up to 10","Fast Wi-Fi &amp; large work table","Full kitchen &amp; laundry","Central Harrogate, walk to station")),
 dict(h2='Simple, Direct Booking', img=I_TAB, alt='Oak dining table workspace at corporate house Harrogate',
  body=P("Book the whole house directly with the owner: one payment, one confirmation, best-rate guarantee, and no online-travel-agency fees inflating the invoice.",
  "Midweek (Monday–Thursday) availability is our core corporate pattern, with weekly and longer project stays welcome."))],
 faqs=[("Do you accept contractor and project-team bookings?","Yes — corporate groups, contractors and project teams are one of our core guest groups, particularly Monday to Thursday."),
 ("How is payment handled?","One direct card payment for the whole house through our secure checkout — simpler than reconciling multiple hotel rooms."),
 ("How close is the rail station?","Harrogate station is a short walk, with direct services to Leeds and York."),STD_FAQS[1]]),

dict(slug='group-accommodation-harrogate',nav='Group Accommodation',cluster='family',hub=True,
 title='Group Accommodation in Harrogate — Large House Sleeps 10 | Portico Suites',
 desc='Large group accommodation in central Harrogate: a 7-bedroom Victorian townhouse sleeping 10, with 5 bathrooms. Self-catering, book direct for the best rate.',
 eyebrow='Groups of up to 10', h1='Group Accommodation in Harrogate',
 intro='A 219 m² Victorian townhouse across four floors — one of the largest holiday houses in central Harrogate, for any group that wants to actually stay together.',
 hero_img=I_LIV, sections=[
 dict(h2='Room for Everyone', img=I_FLR, alt='Floorplan of 7-bedroom group accommodation in Harrogate',
  body=P("Seven bedrooms over four floors means couples, friends and colleagues each get real privacy — and with five bathrooms (four en-suite), mornings never queue.",
  "The sitting room gathers everyone around the fireplace and bay window; the dining kitchen seats the full party at one oak table.")+
  T("7 bedrooms · sleeps 10","5 bathrooms, 4 en-suite","219 m² over four floors","Sitting room + dining kitchen for the whole group")),
 dict(h2='In the Heart of Harrogate', img=I_GAR, alt='Garden terrace with church views at group house Harrogate',
  body=P("Franklin Road is genuinely central: Bettys, the Valley Gardens, the Turkish Baths and the town's restaurants are all a short walk, with the rail station close by for car-free groups.",
  "Book the whole house directly — best rate guaranteed, instant confirmation, one simple payment for the group."))],
 faqs=[STD_FAQS[0],("Is it suitable for celebrations?","The house suits family gatherings, reunions and group breaks. We ask all groups to respect our quiet-hours policy for our neighbours."),
 ("Is the house self-catering?","Yes — a full kitchen with a large oak dining table seating the whole party."),
 ("Where exactly is it?","Franklin Road, central Harrogate, HG1 5EN — a short walk from the town centre, station and a 3-minute walk from the Convention Centre.")]),

dict(slug='large-family-accommodation-harrogate',nav='Family Weekends',cluster='family',hub=True,
 title='Large Family Accommodation in Harrogate | 7-Bed House, Sleeps 10',
 desc='Large family holiday house in central Harrogate sleeping 10 across 7 bedrooms. Perfect weekend base for multi-generation family breaks. Book direct.',
 eyebrow='Family Breaks', h1='Large Family Accommodation in Harrogate',
 intro='Grandparents, parents, cousins — the whole clan under one Victorian roof, a stroll from the Valley Gardens, Bettys and everything that makes a Harrogate weekend.',
 hero_img=I_GAR, sections=[
 dict(h2='A Weekend House for the Whole Family', img=BEDS[0], alt='Principal bedroom with sitting area, family house Harrogate',
  body=P("Multi-generation trips fall apart when the family is scattered across hotel rooms. Here, everyone has their own bedroom — seven of them — and the day starts and ends together in the sitting room or around the big kitchen table.",
  "Friday-to-Sunday breaks are our weekend rhythm, and the house holds birthdays, anniversaries and get-togethers of up to 10 beautifully.")+
  T("7 bedrooms — everyone gets their own","5 bathrooms end the morning queue","Fireplace sitting room with bay window seat","Garden terrace for summer evenings")),
 dict(h2='Steps from the Weekend Itself', img=A_KNA, alt='Knaresborough viaduct near family accommodation Harrogate',
  body=P("Walk to Bettys for breakfast, the Valley Gardens for the kids to run, the Turkish Baths for the grown-ups. Knaresborough's riverside and castle are ten minutes away; RHS Harlow Carr and the Dales just beyond.",
  'See our full guide to <a href="/things-to-do-harrogate/">things to do in Harrogate</a> for the family shortlist.'))],
 faqs=[("Is the house suitable for children?","Yes — families are one of our core guest groups. Tell us ages when booking and we can advise on room arrangements."),
 ("Can two or three families share?","Comfortably — seven bedrooms across four floors give each family its own space, up to 10 guests in total."),
 ("What is nearby for kids?","The Valley Gardens, Knaresborough boating and castle, RHS Harlow Carr, and the Nidderdale countryside are all close."),
 ("Do you take weekend bookings?","Yes — Friday to Sunday breaks are our core weekend pattern. Book direct for the best rate.")]),

dict(slug='weekend-breaks-harrogate',nav='Weekend Breaks',cluster='family',hub=True,
 title='Weekend Breaks in Harrogate for Groups | House Sleeps 10 | Portico Suites',
 desc='Plan a Harrogate weekend break for up to 10: a 7-bedroom townhouse walkable to Bettys, the Turkish Baths and Valley Gardens. Fri–Sun stays, book direct.',
 eyebrow='Fri – Sun', h1='Weekend Breaks in Harrogate',
 intro='Spa-town mornings, Dales afternoons, long dinners back at the house — the classic Harrogate weekend, with room for all ten of you.',
 hero_img=I_TV, sections=[
 dict(h2='The Perfect 48 Hours', img=I_FIRE, alt='Fireplace sitting room for weekend breaks in Harrogate',
  body=P("Arrive Friday evening to a house that is ready — smart-lock self check-in, beds made, kettle on. Saturday: breakfast at Bettys, the Montpellier Quarter, an hour in the Turkish Baths, dinner in town.",
  "Sunday: the Valley Gardens or a run out to Fountains Abbey before the drive home. Every evening ends together in one sitting room, not scattered along a hotel corridor.")),
 dict(h2='Why a House Beats Hotel Rooms', img=BEDS[3], alt='Sage bedroom at weekend break house Harrogate',
  body=T("One booking for up to 10 — no room-block admin","7 bedrooms &amp; 5 bathrooms — privacy and no queues","A shared sitting room and kitchen — the weekend happens together","Central Franklin Road — walk everywhere","Direct booking — best rate, no platform fees")+
  P("Check your dates now — Harrogate weekends book ahead, especially in show and race seasons."))],
 faqs=[("Do you offer two-night weekend stays?","Yes — Friday to Sunday is our standard weekend pattern."),
 ("What is walkable from the house?","Bettys, the Valley Gardens, the Turkish Baths, the Montpellier Quarter and the rail station are all a short walk."),
 ("Is the house good for special occasions?","Birthdays, anniversaries and reunions for up to 10 work beautifully, with respect for our neighbours and quiet hours."),
 ("When should we book?","Popular weekends — race days, show weekends, Christmas markets — sell out well ahead. Booking direct always carries our best rate.")]),

dict(slug='things-to-do-harrogate',nav='Things To Do',cluster='area',hub=True,
 title='Things To Do in Harrogate — A Local Guide | Portico Suites',
 desc='The best things to do in Harrogate: Bettys, Turkish Baths, Valley Gardens, RHS Harlow Carr, Knaresborough and the Dales — from a 7-bed house sleeping 10.',
 eyebrow='Local Guide', h1='Things To Do in Harrogate',
 intro="England's original spa town rewards a slow weekend or a working week's evenings alike. Here is the shortlist we give every guest — all of it close to the house.",
 hero_img=A_KNA, sections=[
 dict(h2='In Town — All Walkable', img=A_HRW, alt='Harewood House day trip from Harrogate',
  body=T("<strong>Bettys Café Tea Rooms</strong> — the institution; go early or queue happily","<strong>The Turkish Baths</strong> — restored Victorian baths, book a session ahead","<strong>Valley Gardens</strong> — gardens, play areas and the boating-lake path","<strong>Montpellier Quarter</strong> — independent shops, galleries and restaurants","<strong>RHS Harlow Carr</strong> — one of the great northern gardens, with a Bettys of its own")),
 dict(h2='Easy Days Out', img=A_BRM, alt='Brimham Rocks in Nidderdale near Harrogate',
  body=T("<strong>Knaresborough</strong> — riverside rowing boats beneath the viaduct, castle ruins above (10 minutes)","<strong>Fountains Abbey &amp; Studley Royal</strong> — World Heritage abbey ruins and water gardens","<strong>Ripley Castle &amp; village</strong> — a compact, charming half-day","<strong>Harewood House</strong> — grand state rooms, gardens and bird garden between Harrogate and Leeds","<strong>The Yorkshire Dales</strong> — Nidderdale and Wharfedale begin on Harrogate's doorstep","<strong>York</strong> — direct trains make it an easy day trip")+
  P('Staying with a group? See our <a href="/group-accommodation-harrogate/">group accommodation guide</a> or check dates below.'))],
 faqs=[("What is Harrogate best known for?","Its spa-town heritage — the Turkish Baths, Valley Gardens and Montpellier Quarter — plus Bettys tea rooms and access to the Yorkshire Dales."),
 ("What can families do in Harrogate?","The Valley Gardens, Knaresborough's boats and castle, RHS Harlow Carr and easy Dales walks all suit children well."),
 ("Do I need a car?","Not for the town itself — everything central is walkable from Portico Suites, and trains run direct to York, Leeds and Knaresborough."),
 ("Where can a group stay near all this?","Portico Suites on Franklin Road sleeps up to 10 across 7 bedrooms, a short walk from everything in this guide.")]),

# ---- HCC EVENT PAGES (9) ----
event('flooring-show-harrogate-accommodation','Flooring Show','The Flooring Show','held each September at the HCC',
 'The UK flooring trade descends on Harrogate every September.',I_KIT,
 ("Is the house available for build-up and breakdown days?","Yes — book the days you actually need, including pre-show build-up.")),
event('harrogate-christmas-gift-fair-accommodation','Christmas & Gift Fair','Harrogate Christmas & Gift Fair','each January',
 'The gifting trade starts its year in Harrogate every January.',I_FIRE,None),
event('harrogate-bridal-show-accommodation','Bridal Show','the Harrogate Bridal Show','',
 'When the bridal trade comes to Harrogate, retailers and designers need beds near the halls.',BEDS[2],None),
event('harrogate-nursery-fair-accommodation','Nursery Fair','Harrogate International Nursery Fair','',
 'The nursery trade gathers in Harrogate — and accommodation near the HCC goes first.',BEDS[1],None),
event('home-and-gift-harrogate-accommodation','Home & Gift','Home &amp; Gift Buyers Festival','held each July across Harrogate',
 "July's Home &amp; Gift takes over the whole town — beds nearby become gold dust.",I_SOFA,None),
event('great-yorkshire-show-accommodation','Great Yorkshire Show','the Great Yorkshire Show','held each July at the Great Yorkshire Showground',
 "England's biggest agricultural show fills every bed in the district each July.",I_GAR,
 ("How far is the Great Yorkshire Showground?","The showground is on the edge of Harrogate — a short drive or taxi from Franklin Road, with central town on your doorstep in the evenings.")),
event('crime-writing-festival-harrogate-accommodation','Crime Writing Festival','the Theakston Old Peculier Crime Writing Festival','held each July',
 "Each July, crime fiction's biggest festival brings readers and writers to Harrogate.",I_LIV,None),
dict(slug='exhibitor-accommodation-harrogate',nav='Exhibitor Stays',cluster='hcc',
 title='Exhibitor Accommodation in Harrogate — 3 Min to HCC | Portico Suites',
 desc='Exhibitor accommodation 3 minutes from Harrogate Convention Centre: 7 bedrooms, sleeps 10, full kitchen and workspace. One booking for the whole stand team.',
 eyebrow='Exhibitors', h1='Exhibitor Accommodation in Harrogate',
 intro='Stand crew, sales team and management under one roof, three minutes from the halls — with a kitchen for 6am starts and a table big enough to re-plan the stand.',
 hero_img=I_TAB, sections=[
 dict(h2='The Exhibitor Problem, Solved', img=I_EXT, alt='Exhibitor house 3 minutes from Harrogate Convention Centre',
  body=P("Every show at the HCC empties Harrogate's hotels and scatters teams across town. Portico Suites keeps up to 10 of you together on Franklin Road, about three minutes' walk from the halls — with seven private bedrooms so a week of shows stays civilised.",
  "Trolley cases roll door-to-door. Early build-up? Breakfast at the house at six. Late breakdown? The kettle and the sitting room are three minutes away.")+
  T("3 minutes' walk, door to halls","7 private bedrooms, 4 en-suite","Kitchen, laundry &amp; fast Wi-Fi","Book exactly the nights you need"))],
 faqs=[("Can we store stand materials at the house?","Reasonable personal and light stand materials are fine; talk to us about anything bulky before arrival."),
 STD_FAQS[0],("Do you host teams for multiple shows a year?","Yes — several trade shows return to the HCC annually and repeat team bookings are very welcome."),STD_FAQS[2]]),
dict(slug='event-crew-accommodation-harrogate',nav='Event Crew',cluster='hcc',
 title='Event Crew & Production Accommodation Harrogate | Near HCC',
 desc='Crew accommodation 3 minutes from Harrogate Convention Centre. Sleeps 10 in 7 rooms — production, AV, build and rigging teams. Flexible nights, book direct.',
 eyebrow='Production & Crew', h1='Event Crew Accommodation in Harrogate',
 intro='Build, AV, rigging and production teams: seven proper beds, five bathrooms, a real kitchen — and a three-minute walk to the loading side of town.',
 hero_img=I_KIT, sections=[
 dict(h2='Crew-Friendly by Design', img=BEDS[4], alt='Crew bedroom near Harrogate Convention Centre',
  body=P("Odd hours are the job. Self check-in by smart lock means arrivals at any hour; blackout-friendly bedrooms, five showers and a washing machine keep a long build week workable.",
  "One direct booking covers the whole crew — no per-room hotel admin, no breakfast-window nonsense, and a kitchen that feeds a team at whatever hour the schedule allows.")+
  T("Self check-in, any hour","7 bedrooms · 5 bathrooms","Washing machine &amp; full kitchen","3 minutes' walk to the HCC"))],
 faqs=[("Do you take short, odd-length bookings around events?","Where the calendar allows, yes — tell us your build and breakdown dates and we will confirm."),
 ("Is check-in flexible for late crew arrivals?","Smart-lock self check-in works at any hour once your booking is verified."),STD_FAQS[0],STD_FAQS[2]]),

# ---- CORPORATE LONG-TAIL (3) ----
dict(slug='contractor-accommodation-harrogate',nav='Contractor Digs',cluster='corporate',
 title='Contractor Accommodation in Harrogate — Digs for up to 10 | Portico Suites',
 desc='Contractor digs in central Harrogate: 7 private bedrooms, 5 bathrooms, kitchen, laundry and parking advice. Weekly and monthly stays, one direct booking.',
 eyebrow='Contractor Stays', h1='Contractor Accommodation in Harrogate',
 intro='Proper digs for working crews: private rooms for up to 10, real cooking and laundry, and central Harrogate on the doorstep after knocking-off time.',
 hero_img=BEDS[5], sections=[
 dict(h2='Better Than B&Bs, Cheaper Than Hotels', img=I_KIT, alt='Kitchen at contractor accommodation Harrogate',
  body=P("Long jobs need somewhere that works: seven separate bedrooms so the crew is not sharing, five bathrooms so mornings move, a kitchen that beats eating out every night, and a washing machine on site.",
  "Weekly and monthly bookings welcome, Monday-to-Friday patterns included. One payment for the whole house keeps the paperwork simple.")+
  T("7 private rooms — no bunk-sharing","Kitchen &amp; laundry on site","Weekly / monthly rates by direct enquiry","Easy reach of the A1(M) and A61"))],
 faqs=[("Do you take long-term contractor bookings?","Yes — weekly and monthly stays are welcome; contact us with your project dates for a direct quote."),
 ("Is there somewhere to park vans?","On-street and nearby options exist around Franklin Road — tell us your vehicles when booking and we will advise honestly."),
 STD_FAQS[0],STD_FAQS[2]]),
dict(slug='relocation-accommodation-harrogate',nav='Relocation Stays',cluster='corporate',
 title='Relocation & Temporary Accommodation in Harrogate | Portico Suites',
 desc='Temporary accommodation in Harrogate for relocations and between-homes stays: a fully equipped 7-bedroom house, flexible lengths, booked direct.',
 eyebrow='Between Homes', h1='Relocation & Temporary Accommodation in Harrogate',
 intro='Moving to the district, renovating, or between completions? A whole house — not a cramped serviced flat — while you land properly.',
 hero_img=I_LIV, sections=[
 dict(h2='Land Softly in Harrogate', img=I_FIRE, alt='Sitting room, temporary accommodation Harrogate',
  body=P("Relocations rarely run to schedule. The house offers real space for a family mid-move: everyone keeps a bedroom, the kitchen keeps routines alive, and central Harrogate — schools, station, shops — is on foot.",
  "Flexible stay lengths by direct arrangement; tell us your dates and we will work with the calendar.")+
  T("Full house, fully equipped","Walkable to station, shops &amp; schools","Flexible lengths by direct enquiry","One simple direct booking"))],
 faqs=[("Do you offer stays of several weeks or months?","Subject to the calendar, yes — longer relocation stays are welcome by direct enquiry."),
 ("Is the house family-ready?","Fully — 7 bedrooms, 5 bathrooms, full kitchen and laundry."),STD_FAQS[2],STD_FAQS[1]]),
dict(slug='team-offsite-harrogate',nav='Team Offsites',cluster='corporate',
 title='Team Offsite Venue with Accommodation — Harrogate | Portico Suites',
 desc='Run a team offsite in Harrogate: house sleeps 10 with meeting-friendly dining table, fast Wi-Fi and a spa town outside the door. Book the whole house direct.',
 eyebrow='Offsites & Awaydays', h1='Team Offsites in Harrogate',
 intro='Strategy in the morning around one big oak table, the Turkish Baths or a Dales walk in the afternoon — an offsite people actually thank you for.',
 hero_img=I_TAB, sections=[
 dict(h2='Work Room + Bedrooms + Spa Town', img=I_SOFA, alt='Breakout sitting room for team offsite Harrogate',
  body=P("The dining kitchen seats the whole team for working sessions; the sitting room takes breakouts; seven bedrooms mean nobody draws the short straw. Then Harrogate does the rest — restaurants for the team dinner, the Turkish Baths for the wind-down, the Dales for the walking meeting.",
  "Direct trains from Leeds and York make it genuinely reachable, and one direct booking covers the venue and the beds in a single line on expenses.")+
  T("Seats 10 around one table","Fast Wi-Fi throughout","7 bedrooms · 5 bathrooms","Direct trains from Leeds &amp; York"))],
 faqs=[("How many can an offsite accommodate?","Up to 10 staying guests across 7 bedrooms; the dining table seats the full group for sessions."),
 ("Is Wi-Fi good enough for video calls?","Fast Wi-Fi runs throughout the house and comfortably supports simultaneous video calls."),
 ("What can teams do in the afternoons?","The Turkish Baths, Bettys, Valley Gardens and Dales walking routes are the classics — see our things-to-do guide."),STD_FAQS[2]]),

# ---- FAMILY / OCCASION LONG-TAIL (6) ----
dict(slug='multi-generation-family-holidays-harrogate',nav='Multi-Gen Holidays',cluster='family',
 title='Multi-Generation Family Holidays in Harrogate | House Sleeps 10',
 desc='Three generations, one Victorian house: 7 bedrooms over four floors in central Harrogate. Grandparents to toddlers, everyone gets their own space.',
 eyebrow='Three Generations', h1='Multi-Generation Family Holidays in Harrogate',
 intro='Grandparents on one floor, parents on another, cousins up top — four floors give a big family togetherness and escape hatches.',
 hero_img=BEDS[0], sections=[
 dict(h2='Four Floors, One Family', img=I_FLR, alt='Four-floor floorplan for multi-generation holiday Harrogate',
  body=P("The vertical layout is the secret: bedrooms spread over four floors mean early-rising grandparents, napping toddlers and teenagers on different schedules all coexist happily, meeting in the sitting room and around the big table when it matters.",
  "Central Harrogate keeps every generation entertained on foot — gardens and play areas for the young, Bettys and the Turkish Baths for the grown-ups, benches and level strolls for the grandparents.")+
  T("Bedrooms across four floors","5 bathrooms — no morning queues","Level, walkable town centre nearby","Everything under one roof, one booking"))],
 faqs=[("Is the house suitable for older guests?","Bedrooms are spread over four floors reached by stairs; a ground-floor bedroom with en-suite sits closest to the living spaces — tell us your party's needs and we will advise honestly."),
 ("Can we celebrate a big birthday or anniversary here?","Yes — milestone gatherings for up to 10 are exactly what the house does best, with respect for neighbours and quiet hours."),STD_FAQS[0],STD_FAQS[2]]),
dict(slug='birthday-weekend-harrogate',nav='Birthday Weekends',cluster='family',
 title='Birthday Weekend House in Harrogate — Sleeps 10 | Portico Suites',
 desc='Celebrate a milestone birthday in Harrogate: a 7-bedroom house for 10, walkable to restaurants, the Turkish Baths and Valley Gardens. Book direct.',
 eyebrow='Milestones', h1='Birthday Weekends in Harrogate',
 intro='A 40th, 60th or 80th with everyone under one roof: long table for the birthday dinner, sitting room for the toasts, and Harrogate for everything else.',
 hero_img=I_FIRE, sections=[
 dict(h2='A House That Hosts', img=I_TAB, alt='Dining table for birthday dinner Harrogate house',
  body=P("The oak table seats the whole party for the birthday dinner — cook together, or walk to the town's restaurants and roll home. The fireplace sitting room takes the toasts and the board games; seven bedrooms take everyone afterwards.",
  "We are a residential street, so celebrations here are the dinner-party kind rather than the amplified kind — brilliant for milestone birthdays, not built for parties that rattle windows.")+
  T("Dinner for 10 at one table","Walk to restaurants &amp; back","7 bedrooms — nobody drives home","Quiet-hours friendly celebrations"))],
 faqs=[("Can we host a birthday dinner at the house?","Absolutely — the dining kitchen and oak table are made for it, and local caterers and private chefs serve the area."),
 ("Are parties allowed?","Dinner-party celebrations, yes; amplified music and late-night parties, no — we sit on a residential street and protect our neighbours' evenings."),STD_FAQS[0],STD_FAQS[2]]),
dict(slug='family-reunion-accommodation-harrogate',nav='Reunions',cluster='family',
 title='Family Reunion Accommodation in Harrogate | 7-Bed House for 10',
 desc='Family reunion house in central Harrogate: 7 bedrooms, big shared spaces, walkable spa town. One booking brings everyone back together.',
 eyebrow='Reunions', h1='Family Reunion Accommodation in Harrogate',
 intro='Scattered across the country? Harrogate sits in the middle of everywhere — direct trains, easy motorways, and a house big enough for the whole story.',
 hero_img=I_SOFA, sections=[
 dict(h2='The Meeting Point of the North', img=I_EXT, alt='Victorian house for family reunions Harrogate',
  body=P("Harrogate is reunion-perfect geography: direct trains from Leeds and York connect the national network, the A1(M) runs close, and once everyone lands nobody needs a car again.",
  "Seven bedrooms give every branch of the family its own door; the sitting room and one long table do what reunions are for.")+
  T("Central northern location, easy trains","7 bedrooms for family branches","One long table for the big dinner","Walkable town for every age"))],
 faqs=[("Why choose Harrogate for a reunion?","Central northern location with direct rail links, a compact walkable town, and this house — one of few in the centre sleeping 10 in 7 bedrooms."),
 STD_FAQS[0],("Can we book a whole weekend?","Friday-to-Sunday is our standard weekend pattern, with longer stays welcome."),STD_FAQS[2]]),
dict(slug='christmas-accommodation-harrogate',nav='Christmas & New Year',cluster='family',
 title='Christmas & New Year Accommodation in Harrogate | House for 10',
 desc='Spend Christmas or New Year in Harrogate: a 7-bedroom Victorian house for 10, fireplace sitting room, walk to the festive market and lights. Book early.',
 eyebrow='Festive Stays', h1='Christmas & New Year in Harrogate',
 intro='A Victorian sitting room with a fireplace, a table for ten, and one of the prettiest festive towns in the north outside the door.',
 hero_img=I_FIRE, sections=[
 dict(h2='A Proper Festive House', img=I_KIT, alt='Kitchen ready for Christmas dinner Harrogate house',
  body=P("Harrogate in December earns its reputation: festive markets, lights along the Stray and Montpellier, Bettys in full seasonal dress, and the Turkish Baths for the day after Boxing Day.",
  "The house does the rest — a kitchen built for the big dinner, an oak table that seats all ten, and bedrooms enough that hosting Christmas no longer means airbeds.")+
  T("Fireplace sitting room","Kitchen &amp; table for the full Christmas dinner","Walk to the festive market &amp; lights","7 bedrooms — no airbeds this year"))],
 faqs=[("Do you take Christmas and New Year bookings?","Yes — festive weeks book furthest ahead of anything in the calendar, so enquire early."),
 ("Is the kitchen up to Christmas dinner for 10?","Fully equipped, with an oak dining table that seats the whole party."),STD_FAQS[0],STD_FAQS[2]]),
dict(slug='golf-breaks-harrogate',nav='Golf Breaks',cluster='family',
 title='Golf Break Accommodation in Harrogate — Group House for 10',
 desc='Golf group base in Harrogate: sleep 10 in 7 bedrooms with courses across the district, and a spa town for the nineteenth hole. Book the house direct.',
 eyebrow='Golf Groups', h1='Golf Breaks in Harrogate',
 intro='A district thick with courses, a town that does the evenings properly, and one house where the whole fourball-times-two stays together.',
 hero_img=I_GAR, sections=[
 dict(h2='Base Camp for a Golf Week', img=BEDS[4], alt='Bedroom at golf break house Harrogate',
  body=P("Harrogate and its surroundings hold a generous spread of courses within easy driving, from parkland classics to moorland tests — build an itinerary of a different course each day and return to the same beds each night.",
  "Evenings are the point: Harrogate's restaurants and bars on foot, a sitting room for the scorecard arguments, and seven bedrooms so snorers are containable.")+
  T("Courses across the district within easy reach","7 bedrooms · 5 bathrooms for 10 golfers","Drying space for the inevitable weather","Town-centre nineteenth holes on foot"))],
 faqs=[("Which courses are nearby?","A wide choice sits within easy driving of Harrogate across the district and the Dales fringe — we are happy to share guest recommendations."),
 ("Can we store clubs securely?","Yes — there is sensible storage space for a full group's clubs and trolleys."),STD_FAQS[0],STD_FAQS[2]]),
dict(slug='walking-holidays-harrogate-dales',nav='Walking Breaks',cluster='family',
 title='Walking Holiday Base for the Yorkshire Dales — Harrogate House for 10',
 desc='Walking group accommodation in Harrogate: sleep 10 on the edge of the Dales, with Nidderdale and Wharfedale close and a spa town for rest days.',
 eyebrow='Walking Groups', h1='A Walking Base for the Yorkshire Dales',
 intro='Nidderdale on the doorstep, Wharfedale beyond, and a hot shower times five when the boots come off.',
 hero_img=A_FEW, sections=[
 dict(h2='Dales Days, Spa-Town Evenings', img=A_BRM, alt='Sitting room after Dales walking day, Harrogate base',
  body=P("Harrogate is the comfortable way to walk the Dales: Nidderdale AONB begins minutes away, Wharfedale and the classic Dales honeypots sit within an easy drive, and Knaresborough's riverside paths start a train stop away.",
  "Back at base: five bathrooms clear ten walkers fast, the kitchen refuels everyone, and rest days have the Turkish Baths waiting.")+
  T("Nidderdale &amp; Wharfedale in easy reach","Boot &amp; kit space, washing machine","5 bathrooms for post-walk showers","Rest-day spa town on foot"))],
 faqs=[("Is Harrogate a good Dales base?","An excellent comfortable one — Nidderdale starts nearby and the central Dales are an easy drive, with town comforts every evening."),
 ("Can wet gear be dried?","Yes — practical space and a washing machine handle a wet Yorkshire day."),STD_FAQS[0],STD_FAQS[2]]),

# ---- AREA / DAY TRIPS (5) ----
dict(slug='visit-knaresborough-from-harrogate',nav='Knaresborough',cluster='area',
 title='Visiting Knaresborough from Harrogate — Guide | Portico Suites',
 desc='Knaresborough from Harrogate: rowing boats under the viaduct, castle ruins, Mother Shipton\'s Cave — ten minutes from your Harrogate base sleeping 10.',
 eyebrow='Day Trips', h1='Knaresborough, Ten Minutes Away',
 intro='One of England\'s most photographed views — the viaduct over the Nidd — is a single train stop from your front door.',
 hero_img=A_KNA, sections=[
 dict(h2='The Classic Half-Day', img=I_SOFA, alt='Base for visiting Knaresborough from Harrogate',
  body=T("<strong>Rowing boats on the Nidd</strong> — beneath the great railway viaduct","<strong>Knaresborough Castle</strong> — ruins, ravens and the best picnic view in the district","<strong>Mother Shipton's Cave</strong> — England's oldest visitor attraction","<strong>The market square</strong> — Wednesday markets and independent cafés","<strong>Riverside walks</strong> — level paths the whole family manages")+
  P("Trains run frequently from Harrogate station — a short walk from the house — or it is a ten-minute drive."))],
 faqs=[("How do we get to Knaresborough from Harrogate?","One stop by train from Harrogate station, or around ten minutes by car."),
 ("Is Knaresborough good with children?","Very — boats, castle grounds and riverside ice creams make it the easiest family half-day from the house."),STD_FAQS[0],STD_FAQS[2]]),
dict(slug='fountains-abbey-from-harrogate',nav='Fountains Abbey',cluster='area',
 title='Fountains Abbey from Harrogate — Day Trip Guide | Portico Suites',
 desc='Visit Fountains Abbey & Studley Royal from Harrogate: World Heritage ruins and water gardens ~25 minutes from your group house sleeping 10.',
 eyebrow='Day Trips', h1='Fountains Abbey & Studley Royal',
 intro='Britain\'s largest monastic ruins in a World Heritage water garden — the district\'s grandest day out, an easy drive from the house.',
 hero_img=A_FTN, sections=[
 dict(h2='A Full, Easy Day', img=A_RIP, alt='Ripley Castle near Fountains Abbey and Harrogate',
  body=P("Allow a whole unhurried day: the abbey ruins themselves, the Georgian water gardens of Studley Royal, the deer park beyond, and tearooms when legs give out. Paths suit pushchairs and grandparents alike on the main circuits.",
  "It is roughly a 25-minute drive from Franklin Road, pairing naturally with pretty Ripon or Ripley Castle on the way back.")+
  T("World Heritage abbey &amp; gardens","Deer park and family trails","~25 minutes by car from the house","Pairs with Ripon or Ripley village"))],
 faqs=[("How far is Fountains Abbey from Harrogate?","Roughly a 25-minute drive from the house; National Trust members visit free."),
 ("Is it suitable for all ages?","The main circuits are manageable for most ages, with plenty of resting points and tearooms."),STD_FAQS[0],STD_FAQS[2]]),
dict(slug='york-day-trip-from-harrogate',nav='York Day Trip',cluster='area',
 title='York Day Trip from Harrogate by Train — Guide | Portico Suites',
 desc='Do York from Harrogate: direct trains from a station near your house sleeping 10. Minster, Shambles, walls and railway museum — no city parking pain.',
 eyebrow='Day Trips', h1='York, By Train, No Parking Pain',
 intro='The Minster, the Shambles, the city walls and the National Railway Museum — all reached by a direct train from the station down the road.',
 hero_img=I_LIV, sections=[
 dict(h2='The Car-Free City Day', img=I_TAB, alt='Group base for York day trips from Harrogate',
  body=T("<strong>York Minster</strong> — climb the tower if the legs agree","<strong>The Shambles &amp; snickelways</strong> — medieval streets made for wandering","<strong>City walls circuit</strong> — the best free view in Yorkshire","<strong>National Railway Museum</strong> — free, and children surrender happily","<strong>River cruises &amp; chocolate history</strong> — for whatever time remains")+
  P("Direct trains run from Harrogate throughout the day; the station is a short walk from the house, and York's is inside the city walls."))],
 faqs=[("How long is the train from Harrogate to York?","Direct services connect the two throughout the day — an easy, car-free day trip."),
 ("Is York doable with a big family group?","Ideal — the train removes parking, and the city is compact and walkable for all ages."),STD_FAQS[0],STD_FAQS[2]]),
dict(slug='yorkshire-dales-from-harrogate',nav='The Dales',cluster='area',
 title='The Yorkshire Dales from Harrogate — Day Guide | Portico Suites',
 desc='Explore the Yorkshire Dales from a Harrogate base sleeping 10: Nidderdale, Wharfedale, Bolton Abbey and waterfall walks within easy reach.',
 eyebrow='Day Trips', h1='The Yorkshire Dales from Harrogate',
 intro='Harrogate sits where the spa town ends and the Dales begin — drive minutes, not hours, to the good stuff.',
 hero_img=A_BRM, sections=[
 dict(h2='Pick Your Dale', img=A_FEW, alt='Fewston Reservoir in the Washburn Valley near Harrogate',
  body=T("<strong>Nidderdale</strong> — the local AONB: Brimham Rocks' natural sculptures and How Stean Gorge","<strong>Washburn Valley</strong> — Fewston &amp; Swinsty reservoir circuits, minutes from town","<strong>Wharfedale</strong> — Bolton Abbey's ruins, river stepping stones and the Strid woods","<strong>Grassington &amp; Burnsall</strong> — the postcard Dales villages","<strong>Malham</strong> — the Cove and Gordale Scar for the ambitious day","<strong>Waterfall country</strong> — Ingleton and Aysgarth further afield")+
  P("Evenings return you to restaurants and hot water — the civilised way to do the Dales with a group of 10."))],
 faqs=[("Which Dales day is best with children?","Bolton Abbey and Brimham Rocks are the family bankers — space to clamber and easy facilities."),
 ("Do we need a car for the Dales?","For the Dales proper, yes — though Nidderdale begins close to town and Knaresborough is reachable by train."),STD_FAQS[0],STD_FAQS[2]]),
dict(slug='harrogate-restaurants-guide',nav='Eating Out',cluster='area',
 title='Where to Eat in Harrogate — Group Dining Guide | Portico Suites',
 desc='Eating out in Harrogate with a group: the quarters, cuisines and booking tips locals use — all walkable from a house sleeping 10 in the centre.',
 eyebrow='Eating & Drinking', h1='Where to Eat in Harrogate',
 intro='A spa town that has always fed its visitors well — from Bettys ceremony to Montpellier bistros, all on foot from the house.',
 hero_img=I_TAB, sections=[
 dict(h2='How Locals Navigate It', img=I_KIT, alt='Kitchen alternative to Harrogate restaurants',
  body=P("Head for the <strong>Montpellier Quarter</strong> for the bistro-and-wine-bar heart of town; <strong>Cold Bath Road</strong> for neighbourhood favourites; the centre for everything from Italian stalwarts to modern Yorkshire menus. <strong>Bettys</strong> remains the ceremony — queue for breakfast or book the Imperial Room experience ahead.",
  "Groups of ten should book ahead everywhere at weekends. And when the town is full or the mood is home-cooked, the house's own oak table seats the party with a kitchen to match — private chefs and caterers also serve the area.")+
  T("Montpellier Quarter — the bistro heart","Cold Bath Road — neighbourhood gems","Bettys — book or queue, both worth it","Group tip: reserve ahead for 10 at weekends"))],
 faqs=[("Can a group of 10 eat out easily in Harrogate?","Yes with booking — the town is well supplied, but weekend tables for 10 should be reserved ahead."),
 ("Can we hire a private chef at the house?","Private chefs and caterers serve the Harrogate area and the house kitchen suits them well — a lovely option for a special night in."),STD_FAQS[0],STD_FAQS[2]]),

# ---- PRACTICAL (1) ----
dict(slug='getting-to-harrogate',nav='Getting Here',cluster='area',
 title='Getting to Harrogate — Train, Car & Airport Guide | Portico Suites',
 desc='How to get to Harrogate: direct trains from Leeds & York, road routes via the A1(M) and A61, and Leeds Bradford Airport nearby. Your house is central.',
 eyebrow='Travel Guide', h1='Getting to Harrogate',
 intro='However you travel, the last step is short: Portico Suites sits in the town centre, a short walk from the station and three minutes from the HCC.',
 hero_img=I_EXT, sections=[
 dict(h2='Rail, Road & Air', img=I_LIV, alt='Central Harrogate house near station',
  body=T("<strong>By train</strong> — direct services link Harrogate with Leeds and York, connecting the national network; the station is a short walk from the house","<strong>By car</strong> — the A1(M) and A61 bring the north's motorway network close; central Harrogate is well signed","<strong>By air</strong> — Leeds Bradford Airport is the closest, an easy taxi or drive away","<strong>Arriving late?</strong> — smart-lock self check-in works at any hour once verified")+
  P("Once here, most stays never need the car again: town, station, Convention Centre and the Valley Gardens are all on foot."))],
 faqs=[("Which airport is closest to Harrogate?","Leeds Bradford is the closest airport, with Manchester a longer but well-connected alternative."),
 ("Do I need a car in Harrogate?","Not for the town — the house, station, HCC and centre are all walkable; a car helps only for Dales days."),STD_FAQS[1],STD_FAQS[2]]),
]


urls=[f"{BASE}/"]+[f"{BASE}/{p['slug']}/" for p in PAGES]
# ===== JOURNAL =====
import re as _re
def _slug(t): return _re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
JPOSTS=[
("Three Minutes to the Halls: The Exhibitor\u2019s Guide to Harrogate","2026-09-24","portico-suites-exterior-franklin-road.jpg",
"How trade-show teams turn Convention Centre weeks from a logistics headache into the easiest part of the job.",
["Every show at the HCC empties the town\u2019s hotels within weeks of dates being announced \u2014 and scatters teams across Harrogate in the process. The alternative is simpler: one house, seven private bedrooms, three minutes\u2019 walk from the halls.",
"The rhythm of a show week changes when base camp is that close. Build-up mornings start with a proper breakfast at the big table; breakdown evenings end with the kettle on minutes after the shutters come down. One booking, one invoice line, and nobody draws the short straw on a distant hotel.",
"Our guides to accommodation for specific shows \u2014 from the Flooring Show to Home &amp; Gift \u2014 are linked in the site footer."]),
("The Perfect Harrogate Weekend for a Group of Ten","2026-09-17","portico-suites-living-room-bay-window.jpg",
"Forty-eight hours, ten people, zero hotel-corridor logistics \u2014 the weekend template our guests keep repeating.",
["Friday: arrive to smart-lock self check-in, beds made, and the sitting room ready for the first drink of the weekend. Saturday: Bettys for breakfast, the Montpellier Quarter for wandering, the Turkish Baths for an hour of Victorian steam, dinner in town and a slow walk home.",
"Sunday belongs to the Valley Gardens \u2014 or a run out to Fountains Abbey \u2014 before the drive home. The difference a whole house makes is simple: every evening happens together, in one room, rather than along a corridor of hotel doors."]),
("Knaresborough with Kids: Boats, Castles and Ice Cream","2026-09-10","attraction-knaresborough-viaduct.jpg",
"One train stop away sits the easiest family half-day in Yorkshire.",
["The view from the castle grounds \u2014 the great viaduct striding over the Nidd \u2014 is the one everybody photographs, but the day belongs to the river: rowing boats by the hour, riverside paths flat enough for every generation, and ice cream at both ends.",
"Add Mother Shipton\u2019s Cave, England\u2019s oldest visitor attraction, and Wednesday\u2019s market in the square, and you have a half-day that asks nothing of the driver: the train from Harrogate takes minutes, and the station is a twelve-minute walk from our front door."]),
("Where to Eat in Harrogate Right Now: A Local Shortlist","2026-09-03","portico-suites-dining-kitchen.jpg",
"The quarters, the bookings worth making, and the honest tips for tables of ten.",
["Head for the Montpellier Quarter when in doubt \u2014 it remains the bistro heart of town \u2014 with Cold Bath Road close behind for neighbourhood favourites. Bettys is the ceremony: queue for breakfast or book ahead, and regret neither.",
"The honest tip for groups: reserve ahead everywhere at weekends, especially in show and race seasons. And when the town is booked out, the house fights back \u2014 an oak table for ten and a kitchen that local private chefs know well."]),
("Fountains Abbey: Planning the District\u2019s Grandest Day Out","2026-08-27","attraction-fountains-abbey.jpg",
"World Heritage ruins, Georgian water gardens and a deer park \u2014 how to do it properly.",
["Give it a full, unhurried day. The abbey ruins reward slow walking \u2014 the vaulted cellarium is the photograph everyone leaves with \u2014 before the path opens into Studley Royal\u2019s water gardens and the deer park beyond.",
"It sits roughly twenty-five minutes from Franklin Road by car, and pairs beautifully with Ripley\u2019s castle and village on the way home. National Trust members visit free; everyone else should still consider it the best-value day in the district."]),
("Brimham Rocks and the Washburn Valley: Walks from the Doorstep","2026-08-20","attraction-brimham-rocks.jpg",
"Nidderdale starts minutes from town \u2014 here are the two walks we send every guest to first.",
["Brimham Rocks is the crowd-pleaser: acres of wind-carved gritstone sculptures that children treat as a natural climbing frame and photographers treat as a studio, with Nidderdale rolling away below.",
"Quieter, and closer still, the Washburn Valley strings together Fewston and Swinsty reservoirs with level woodland circuits \u2014 the reliable leg-stretch when half the group wants a walk and the other half wants to be back for lunch."]),
("Why Big Families Choose a Townhouse Over a Row of Hotel Rooms","2026-08-13","portico-suites-bedroom-principal.jpg",
"Multi-generation trips succeed on architecture: four floors, seven doors, one table.",
["The failure mode of the three-generation holiday is well known: the family scattered along a corridor, negotiating breakfast windows. A vertical Victorian townhouse solves it structurally \u2014 early-rising grandparents, napping toddlers and nocturnal teenagers each get a floor\u2019s worth of distance.",
"The togetherness happens where it should: one sitting room, one long oak table, and a town outside built for every walking speed."]),
("Harrogate\u2019s Event Calendar: When to Book Early","2026-08-06","portico-suites-living-room-fireplace.jpg",
"Show weeks, race days and festival summers \u2014 the dates that empty the town\u2019s beds first.",
["Harrogate runs on its calendar. Trade shows at the Convention Centre \u2014 flooring in the autumn, gifting in deep winter, weddings and nurseries between \u2014 book the town solid, and July stacks the Great Yorkshire Show against festival season.",
"The practical rule: if your dates touch an event week, book the moment plans firm up. Direct booking guarantees our best rate whenever you land."]),
("Book Direct vs the Platforms: What the 12% Really Means","2026-07-30","portico-suites-living-room-leather-sofa.jpg",
"The same house, the same dates \u2014 and why the direct price is always the better one.",
["Online travel platforms add service fees that can push a group booking\u2019s total up substantially \u2014 money that buys nothing extra for the guest. Booking direct removes that layer entirely, which is why our direct rate beats the platforms for identical dates.",
"Direct guests also deal with the owner, not a call centre: instant confirmation, straight answers, and one payment for the whole house."]),
("Inside the House: Seven Bedrooms Across Four Floors","2026-07-23","portico-suites-floorplan.jpg",
"A tour of the layout \u2014 and why 219 square metres works so well for groups of ten.",
["The floorplan tells the story better than adjectives: a ground floor holding the bay-windowed sitting room, an en-suite bedroom and the long dining kitchen; three more floors stacking six further bedrooms and four more bathrooms above.",
"Five bathrooms \u2014 four of them en-suite \u2014 is the number guests notice most. Mornings simply never queue, whether the party is a wedding\u2019s worth of family or a full exhibition team."]),
]
def article_page(title,date,cover,excerpt,paras,allposts):
    slug=_slug(title)
    ld={"@context":"https://schema.org","@type":"BlogPosting","headline":title.replace("&amp;","&"),
        "datePublished":date,"description":excerpt.replace("&amp;","&"),
        "image":f"{IMG}/{cover}","mainEntityOfPage":f"{BASE}/journal/{slug}/",
        "author":{"@type":"Organization","name":"Portico Suites"},
        "publisher":{"@type":"Organization","name":"Portico Suites"}}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Portico Suites","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"The Journal","item":BASE+"/journal/"},
        {"@type":"ListItem","position":3,"name":title.replace("&amp;","&"),"item":f"{BASE}/journal/{slug}/"}]}
    others=[t for (t,_,_,_,_) in allposts if t!=title][:3]
    olinks="".join(f"<a href='/journal/{_slug(t)}/'>{t}</a>" for t in others)
    body="".join(f"<p>{x}</p>" for x in paras)
    return f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | The Journal | Portico Suites Harrogate</title>
<meta name="description" content="{excerpt}">
<link rel="canonical" href="{BASE}/journal/{slug}/">
<meta property="og:title" content="{title}"><meta property="og:description" content="{excerpt}">
<meta property="og:image" content="{IMG}/{cover}"><meta property="og:url" content="{BASE}/journal/{slug}/"><meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld)}</script>
<script type="application/ld+json">{json.dumps(crumb)}</script>
<style>{CSS}
.art{{max-width:720px;margin:0 auto;padding:56px 24px}}
.art time{{font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--bronze)}}
.art h1{{font-size:clamp(24px,3.4vw,34px);margin:12px 0 20px}}
.art .cover{{width:100%;border-radius:3px;margin:8px 0 26px;display:block}}
.art p{{font-size:15.5px}}</style></head><body>
<nav><a class="brand" href="/">PORTICO SUITES</a><a class="cta" href="/#book">Check Availability</a></nav>
<article class="art">
<a href="/journal/" style="font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--bronze);text-decoration:none">\u2190 The Journal</a>
<div style="height:14px"></div><time datetime="{date}">{date}</time><h1>{title}</h1>
<img class="cover" src="{IMG}/{cover}" alt="{title}">{body}</article>
<div class="band"><h2>Sleeps 10 \u00b7 7 Bedrooms \u00b7 Central Harrogate</h2><p>{USP}. Book directly for the guaranteed best rate.</p><a class="cta gold" href="/#book">Check Availability</a></div>
<section><div class="wrap"><div class="eyebrow">Keep Reading</div><div class="linkrow">{olinks}<a href="/journal/">All Journal posts</a></div></div></section>
<footer>PORTICO SUITES \u00b7 Franklin Road, Harrogate HG1 5EN \u00b7 <a href="/">porticosuites.com</a> \u00b7 <a href="/#book">Book Direct</a></footer>
</body></html>"""

def journal_index(allposts):
    cards="".join(f"""<a class="jcard" href="/journal/{_slug(t)}/"><img src="{IMG}/{c}" alt="{t}" loading="lazy"><div class="jbody"><time>{d}</time><h3>{t}</h3><p>{e}</p></div></a>""" for (t,d,c,e,_) in allposts)
    return f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Journal \u2014 Notes From Franklin Road | Portico Suites Harrogate</title>
<meta name="description" content="Guides, local knowledge and seasonal notes from Portico Suites \u2014 a 7-bedroom holiday home in central Harrogate sleeping 10.">
<link rel="canonical" href="{BASE}/journal/">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}
.jgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:22px;margin-top:40px}}
.jcard{{background:#FCFBF7;border:1px solid var(--ivory2);border-radius:4px;overflow:hidden;text-decoration:none;color:var(--ink);display:block;transition:box-shadow .25s}}
.jcard:hover{{box-shadow:0 12px 30px rgba(40,50,36,.12)}}
.jcard img{{width:100%;height:180px;object-fit:cover;display:block}}
.jbody{{padding:16px 18px 20px}}
.jbody time{{font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--bronze)}}
.jbody h3{{font-size:16px;margin:8px 0;line-height:1.4}}
.jbody p{{font-size:13px;margin:0;opacity:.85}}</style></head><body>
<nav><a class="brand" href="/">PORTICO SUITES</a><a class="cta" href="/#book">Check Availability</a></nav>
<section><div class="wrap"><div class="section-head" style="text-align:center"><div class="eyebrow">The Journal</div>
<h2 style="font-size:30px">Notes From Franklin Road</h2><div class="rule" style="margin:16px auto"></div>
<p style="max-width:560px;margin:0 auto">Guides, local knowledge and seasonal notes from the house.</p></div>
<div class="jgrid">{cards}</div></div></section>
<div class="band"><h2>Sleeps 10 \u00b7 7 Bedrooms \u00b7 Central Harrogate</h2><p>{USP}. Book directly for the guaranteed best rate.</p><a class="cta gold" href="/#book">Check Availability</a></div>
<footer>PORTICO SUITES \u00b7 Franklin Road, Harrogate HG1 5EN \u00b7 <a href="/">porticosuites.com</a> \u00b7 <a href="/#book">Book Direct</a></footer>
</body></html>"""

os.makedirs(str(SITE/'journal'),exist_ok=True)
open(SITE/'journal'/'index.html','w').write(journal_index(JPOSTS))
for (t,d,c,e,paras) in JPOSTS:
    dd=str(SITE/'journal'/_slug(t)); os.makedirs(dd,exist_ok=True)
    open(f'{dd}/index.html','w').write(article_page(t,d,c,e,paras,JPOSTS))
print(f"journal: index + {len(JPOSTS)} article pages")
urls.append(f"{BASE}/journal/")
for (t,d,c,e,_) in JPOSTS: urls.append(f"{BASE}/journal/{_slug(t)}/")

os.makedirs(SITE, exist_ok=True)
for pg in PAGES:
    d=str(SITE/pg['slug']); os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html","w").write(page(pg,PAGES))
print(f"✓ {len(PAGES)} pages generated")

home_imgs=[f"{IMG}/portico-suites-exterior-franklin-road.jpg",f"{IMG}/portico-suites-living-room-bay-window.jpg",f"{IMG}/portico-suites-dining-kitchen.jpg",f"{IMG}/portico-suites-bedroom-principal.jpg",f"{IMG}/portico-suites-garden-terrace.jpg"]
page_hero={f"{BASE}/{p['slug']}/": f"{IMG}/{p['hero_img']}" for p in PAGES}
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
for i,u in enumerate(urls):
    imgs=home_imgs if i==0 else [page_hero[u]] if u in page_hero else []
    itags="".join(f"<image:image><image:loc>{im}</image:loc></image:image>" for im in imgs)
    sm+=f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{'weekly' if i==0 else 'monthly'}</changefreq><priority>{'1.0' if i==0 else '0.8' if i<7 else '0.7'}</priority>{itags}</url>\n"
open(SITE/'sitemap.xml','w').write(sm+'</urlset>\n')
print(f"✓ sitemap.xml ({len(urls)} URLs)")
