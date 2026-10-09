import json, datetime, os
BASE='https://porticosuites.com'; IMG=f'{BASE}/images'; TODAY=datetime.date.today().isoformat()
FAVICON='<link rel="icon" type="image/png" sizes="120x120" href="/favicon.png"><link rel="apple-touch-icon" href="/favicon.png">'
import pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
SITE=ROOT/'site'
CSS=(ROOT/'tools'/'page.css').read_text()
P=lambda *ps:"".join(f"<p>{x}</p>" for x in ps)
T=lambda *i:"<ul class='ticks'>"+"".join(f"<li>{x}</li>" for x in i)+"</ul>"
USP="Sleeps 10 · 7 bedrooms · 5 bathrooms · 3 minutes' walk to Harrogate Convention Centre · central Franklin Road"


GUIDE_GROUPS=[('hcc','Convention Centre & Events'),('family','Groups, Families & Breaks'),('corporate','Corporate & Contractors'),('area','Harrogate Area Guides')]
def guides_block(current=None):
    """Site-wide directory linking every landing page, so no page is orphaned."""
    out=[]
    for cl,label in GUIDE_GROUPS:
        links="".join(f"<a href='/{o['slug']}/'>{o['nav']}</a>" for o in PAGES if o['cluster']==cl and o['slug']!=current)
        out.append(f"<div class='gg'><div class='eyebrow'>{label}</div><div class='linkrow'>{links}</div></div>")
    return ("<section class='guides'><div class='wrap'><div class='eyebrow'>Explore</div><h2>All Portico Suites Guides</h2><div class='rule'></div>"
            +"".join(out)+"<div class='linkrow'><a href='/journal/'>The Journal</a><a href='/'>Portico Suites home</a></div></div></section>")

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
{FAVICON}
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
{guides_block(pg['slug'])}
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

def event(slug,nav,h1,title,desc,intro,hero,sections,faqs):
    """HCC-cluster event page with fully bespoke copy (no shared template body)."""
    return dict(slug=slug,nav=nav,cluster='hcc',title=title,desc=desc,eyebrow='Harrogate Convention Centre' if 'hcc' in title.lower() or 'convention' in title.lower() else 'Harrogate Events',
    h1=h1,intro=intro,hero_img=hero,sections=sections,faqs=faqs)
DATES="Show dates move from year to year, so check the organiser's website for the current edition before you book."


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
 title='Large Group Accommodation in Harrogate — 7-Bed House Sleeps 10 | Portico Suites',
 desc='Large group accommodation in central Harrogate: a 7-bedroom Victorian townhouse sleeping up to 10, with 5 bathrooms, a full kitchen and self check-in. Book direct.',
 eyebrow='Groups of up to 10', h1='Large Group Accommodation in Harrogate',
 intro='Portico Suites is a 7-bedroom Victorian townhouse on Franklin Road in central Harrogate. It sleeps up to 10 guests across 219 m² and three floors, so a large group can stay together in one house instead of several hotel rooms.',
 hero_img=I_LIV, sections=[
 dict(h2='Room for Everyone', img=I_FLR, alt='Floorplan of 7-bedroom large group accommodation in Harrogate',
  body=P("This is large accommodation in Harrogate for groups who want to stay together: seven bedrooms over three floors means couples, friends and colleagues each get real privacy, and with five bathrooms (four en-suite) mornings never queue.",
  "The sitting room gathers everyone around the fireplace and bay window, and the dining kitchen seats the full party at one oak table.")+
  T("7 bedrooms · sleeps up to 10","5 bathrooms, 4 en-suite","219 m² over three floors","Sitting room + dining kitchen for the whole group")),
 dict(h2='How the Beds Are Arranged', img=BEDS[0], alt='Principal bedroom with large double bed at Portico Suites',
  body=P("Six of the bedrooms each have one large double bed. The seventh bedroom has a double sofa bed. Two further sofa beds can be set up as alternatives where a group needs a different arrangement.",
  "The house sleeps a maximum of 10 guests. That limit is set by fire regulations and applies however the beds are arranged.")),
 dict(h2='Who Stays Here', img=I_SOFA, alt='Sitting room with leather sofa at Portico Suites',
  body=P("Groups book Portico Suites for friends' weekends, family reunions and multi-generation holidays, and for project teams and contractors who want one base. Event teams use it for the Harrogate Convention Centre, which is a 3-minute walk away.",
  'See our guides for <a href="/large-family-accommodation-harrogate/">large families</a>, <a href="/corporate-accommodation-harrogate/">corporate stays</a>, <a href="/team-offsite-harrogate/">team off-sites</a> and <a href="/harrogate-convention-centre-accommodation/">Convention Centre events</a>.',
  "It is a house for gatherings, not parties or events, and we ask all groups to respect our quiet hours for the neighbours.")),
 dict(h2='How a Group Stay Works', img=I_KIT, alt='Dining kitchen at group accommodation in Harrogate',
  body=P("Arrival is by self check-in with a smart lock, from 3pm, so the group can come in at different times. Early check-in from 1pm can be added when you book, and check-out is by 10am.",
  "There is a full kitchen, a washer and dryer, fast Wi-Fi throughout and free on-street parking overnight (a reserved space can be added during booking where offered). Well-behaved dogs are welcome.")+
  T("Self check-in by smart lock","Full kitchen &amp; laundry","Fast Wi-Fi throughout","Dog-friendly")),
 dict(h2='In the Heart of Harrogate', img=I_GAR, alt='Garden terrace with church views at group house Harrogate',
  body=P("Franklin Road is genuinely central. The town centre is a 7-minute walk, Bettys Café Tea Rooms and the Valley Gardens are each 10 minutes on foot, and Harrogate rail station is 12 minutes, which suits groups travelling without cars.",
  "Back at the house, the garden terrace has quiet seating with views of a church spire. Book the whole house directly for the best rate, instant confirmation and one simple payment for the group."))],
 faqs=[("Is there large accommodation in Harrogate for a big group?","Yes. Portico Suites is a 7-bedroom house in central Harrogate that sleeps up to 10 guests, with 5 bathrooms, a full kitchen and a large oak dining table."),
 ("How many people can stay at Portico Suites?","Up to 10 guests across 7 bedrooms with 5 bathrooms, 4 of them en-suite. The maximum is 10 because of fire regulations."),
 ("How are the beds arranged?","Six bedrooms have one large double bed each, and the seventh has a double sofa bed. Two further sofa beds can be used as alternatives, but the maximum stays at 10 guests."),
 ("Is it suitable for celebrations?","The house suits family gatherings, reunions and group breaks. It is not for parties or events, and we ask all groups to respect our quiet-hours policy for our neighbours."),
 ("Is the house self-catering?","Yes. There is a full kitchen with a large oak dining table seating the whole party, plus a washer and dryer."),
 ("How does check-in work for a group?","Self check-in by smart lock from 3pm, so guests can arrive at different times. Early check-in from 1pm can be added during booking. Check-out is by 10am."),
 ("Where exactly is it?","Franklin Road, central Harrogate, HG1 5EN. It is a 7-minute walk to the town centre, 12 minutes to the rail station and 3 minutes to the Convention Centre.")]),

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
 desc='Things to do in Harrogate: Bettys, the Turkish Baths, Valley Gardens, RHS Harlow Carr, Knaresborough and day trips to the Dales, Fountains Abbey and York.',
 eyebrow='Local Guide', h1='Things To Do in Harrogate',
 intro="The best things to do in Harrogate centre on its spa-town heritage: the Turkish Baths, the Valley Gardens, the Stray and Bettys tea rooms. Beyond town, Knaresborough, Fountains Abbey, Brimham Rocks and the Dales are an easy trip. This is the shortlist we give every guest.",
 hero_img=A_KNA, sections=[
 dict(h2='In Town on Foot', img=I_EXT, alt='Franklin Road in central Harrogate near the town centre',
  body=P("From Portico Suites, the town centre is a 7-minute walk, Bettys Café Tea Rooms and the Valley Gardens are each 10 minutes, and the rail station is 12.")+
  T("<strong>Bettys Café Tea Rooms</strong> — the institution; go early or queue happily","<strong>Valley Gardens</strong> — 17 acres of gardens on the edge of the centre, once the site of Harrogate's mineral springs","<strong>The Stray</strong> — 200 acres of open grass around the town, protected from building by law","<strong>Montpellier Quarter</strong> — independent shops, galleries and restaurants")),
 dict(h2='Spa Heritage and Gardens', img=A_HRW, alt='Garden and heritage day out near Harrogate',
  body=P("<strong>The Turkish Baths</strong> on Parliament Street opened in 1897 as part of the Royal Baths and are still in use. Sessions are separated by gender at some times, so check the session times and book ahead.",
  "<strong>The Royal Pump Room Museum</strong> was built in 1842 to shelter visitors taking the town's sulphur waters, and has been a museum since 1953.",
  "<strong>RHS Harlow Carr</strong> is a 58-acre garden on the edge of town. It has the UK's longest streamside garden, woodland, meadows and a Bettys tea room.")),
 dict(h2='Knaresborough', img=A_KNA, alt='Knaresborough viaduct over the River Nidd',
  body=P("Knaresborough is about 4 miles east of Harrogate, and trains run there on the Harrogate to York line. The viaduct, built in 1851, crosses the River Nidd, and you can hire a rowing boat on the river beneath it.",
  "Above the river stand the ruins of the castle, begun by the Normans around 1100. Mother Shipton's Cave and the Petrifying Well, where water turns objects to stone, are also in the town.")),
 dict(h2='Easy Days Out', img=A_BRM, alt='Brimham Rocks in Nidderdale near Harrogate',
  body=T("<strong>Fountains Abbey &amp; Studley Royal</strong> — a Cistercian abbey founded in 1132 and a World Heritage Site, run by the National Trust","<strong>Brimham Rocks</strong> — National Trust moorland rock formations in Nidderdale, an Area of Outstanding Natural Beauty","<strong>Ripley Castle &amp; village</strong> — a compact, charming half-day","<strong>Harewood House</strong> — state rooms, gardens and bird garden between Harrogate and Leeds","<strong>The Yorkshire Dales</strong> — Nidderdale and Wharfedale begin on Harrogate's doorstep","<strong>York</strong> — direct trains make it an easy day trip")),
 dict(h2='Through the Year', img=I_GAR, alt='Garden terrace at Portico Suites in summer',
  body=P("Harrogate has a calendar of events. The Spring Flower Show is held in April, the Great Yorkshire Show takes over the showground for four days in July, and the Theakston Old Peculier Crime Writing Festival also runs in July. The Christmas Market comes to town in November.",
  'We have guides for the <a href="/great-yorkshire-show-accommodation/">Great Yorkshire Show</a> and the <a href="/crime-writing-festival-harrogate-accommodation/">Crime Writing Festival</a>. Dates change every year, so check the organisers before you book.')),
 dict(h2='Visiting With a Group', img=I_LIV, alt='Sitting room at Portico Suites',
  body=P('Portico Suites sleeps up to 10 across 7 bedrooms, so a group of friends or a family can see all of this from one base. See our <a href="/group-accommodation-harrogate/">group accommodation guide</a> or check dates below.'))],
 faqs=[("What are the best things to do in Harrogate?","Bettys tea rooms, the Turkish Baths, the Valley Gardens, the Stray and RHS Harlow Carr in town, then Knaresborough, Fountains Abbey and Brimham Rocks nearby."),
 ("What is Harrogate best known for?","Its spa-town heritage, including the Turkish Baths, the Royal Pump Room and the Valley Gardens, plus Bettys tea rooms and access to the Yorkshire Dales."),
 ("What can families do in Harrogate?","The Valley Gardens, Knaresborough's boats and castle, RHS Harlow Carr and easy Dales walks all suit children well."),
 ("How do I get to Knaresborough from Harrogate?","Trains run between the two towns on the Harrogate to York line. Knaresborough is about 4 miles east of Harrogate."),
 ("Do I need a car?","Not for the town itself. Everything central is walkable from Portico Suites, and trains run direct to York, Leeds and Knaresborough."),
 ("Where can a group stay near all this?","Portico Suites on Franklin Road sleeps up to 10 across 7 bedrooms, a 7-minute walk from the town centre.")]),

# ---- HCC EVENT PAGES (7, each with its own copy) ----
event('flooring-show-harrogate-accommodation','Flooring Show','Accommodation for The Flooring Show',
 'The Flooring Show Harrogate — Group Accommodation Near the HCC | Portico Suites',
 'Where to stay for The Flooring Show at Harrogate Convention Centre in September: a 7-bedroom house sleeping 10, 3 minutes from the halls. Book direct.',
 "September is flooring month in Harrogate. If your brand, distribution team or buying group is exhibiting or visiting, here is a house that keeps everyone together.",I_KIT,[
 dict(h2='A Trade Show With Long Days',img=I_KIT,alt='Dining kitchen at Portico Suites for flooring show teams',
  body=P("The Flooring Show brings retail and contract flooring buyers and suppliers to the Harrogate Convention Centre each September, and it has been doing so for a long time. Stands are heavy, samples are bulky and the days run from early set-up to evening customer dinners.",
  "A house changes how that week works. The kitchen handles early breakfasts, the oak dining table becomes the place to go through the day's leads, and the washer and dryer deal with a week of shirts without a hotel laundry bill.")+
  T("Full kitchen for early starts","Oak table &amp; benches seat the whole party","Washer &amp; dryer in the house","3 minutes' walk to the HCC")),
 dict(h2='Sales Team, Stand Crew and Management Together',img=BEDS[0],alt='Principal bedroom with sitting area at Portico Suites',
  body=P("Seven bedrooms across four floors means the sales director, the account managers and the stand crew each have a door that closes. The principal bedroom has its own sitting area, and four of the five bathrooms are en-suite, so mornings do not become a queue.",
  "Because the house sleeps up to ten, one booking covers a typical exhibiting team, and you pay for the nights you actually need rather than a hotel block's minimum.")),
 dict(h2='Build-Up, Show Days and Breakdown',img=I_FIRE,alt='Sitting room with fireplace at Portico Suites',
  body=P("Self check-in by smart lock means a late-evening arrival after a long drive needs no front-desk handover. Check-in is from 3pm (early check-in from 1pm can be added when you book) and check-out is by 10am, so a breakdown day can start with the house already settled.",
  "Evenings can be quiet in the sitting room or out in the centre of Harrogate, which is a 7-minute walk away. "+DATES))],
 [("Is the house available for build-up and breakdown days?","Yes. Book the nights you actually need, including the build-up evening before the show opens."),
  ("What month is The Flooring Show held?","It is held each September at the Harrogate Convention Centre. Exact dates change each year, so check the organiser's website."),
  ("Where do vans and cars go?","There is free on-street parking overnight outside the house, and a reserved space can be added during booking where offered."),
  STD_FAQS[0]]),

event('harrogate-christmas-gift-fair-accommodation','Christmas & Gift Fair','Accommodation for Harrogate Christmas & Gift Fair',
 'Harrogate Christmas & Gift Fair — Stay Near the HCC in January | Portico Suites',
 'Exhibiting or buying at the Harrogate Christmas & Gift Fair in January? A 7-bedroom townhouse sleeping 10, 3 minutes from the Convention Centre. Book direct.',
 "January is when the gift and seasonal trade plans its year, and in Harrogate that means a cold walk between the halls and somewhere warm to stay.",I_FIRE,[
 dict(h2='A Winter Show Needs a Warm Base',img=I_FIRE,alt='Fireplace in the sitting room at Portico Suites',
  body=P("The Harrogate Christmas &amp; Gift Fair takes place at the Harrogate Convention Centre in January, when retailers and wholesalers come to see what the next season holds.",
  "After a day on the show floor, the sitting room with its fireplace and the leather sofa is a better place to compare notes than a hotel bar, and the house is a short walk back.")+
  T("Sitting room with fireplace","3 minutes' walk to the HCC","Fast Wi-Fi for order-writing","Kitchen to cook after a long day")),
 dict(h2='For Buying Groups and Independent Retailers',img=I_TAB,alt='Dining table at Portico Suites for buying groups',
  body=P("Buyers often travel as a group: owner, manager and a colleague who knows the stockroom. The house sleeps up to ten in seven separate bedrooms, so a buying group or a few neighbouring shops can share one booking and split the cost.",
  "The long oak table suits order-writing at the end of the day, with fast Wi-Fi to send it off.")),
 dict(h2='Exhibitors Setting Up in the Cold',img=BEDS[1],alt='Bedroom at Portico Suites for exhibitors',
  body=P("Set-up days are long, and tired exhibitors benefit from a proper bed and a hot shower. Four of the five bathrooms are en-suite, and everyone has their own bedroom.",
  "The town centre is 7 minutes' walk away, with Bettys tea rooms 10 minutes on foot for anyone treating the stand team. "+DATES))],
 [("When is the Harrogate Christmas & Gift Fair?","It is held at the Harrogate Convention Centre in January. Exact dates change each year, so check the organiser's website."),
  ("Is the house warm in winter?","Yes. The sitting room has a fireplace, and there is a full kitchen for hot meals after a day on your feet."),
  ("Can a few retailers share the house?","Yes. One booking covers up to 10 guests across 7 bedrooms, so independent retailers can share and split the cost."),
  STD_FAQS[2]]),

event('harrogate-bridal-show-accommodation','Bridal Show','Accommodation for Bridal Week Harrogate',
 'Bridal Week Harrogate Accommodation — Near the Convention Centre | Portico Suites',
 'Stay near Harrogate Convention Centre for Bridal Week, held in March and September. A 7-bedroom house for retailers, designers and teams. Book direct.',
 "Harrogate's bridal trade event, now staged as Bridal Week, brings retailers and designers twice a year. Here is where a whole team can stay close by.",BEDS[2],[
 dict(h2='Two Bridal Weeks a Year',img=BEDS[2],alt='Garnet bedroom at Portico Suites',
  body=P("Bridal Week at the Harrogate Convention Centre runs in spring and autumn, around March and September, bringing bridal retailers and designers together for appointments and orders.",
  "Both are busy weeks for Harrogate accommodation, so a house that sleeps ten gives a retailer and their team a calm place to stay rather than competing for scattered hotel rooms.")+
  T("Spring and autumn editions","7 private bedrooms","Quiet sitting room for debriefs","3 minutes' walk to the HCC")),
 dict(h2='A Calm House Between Appointments',img=I_LIV,alt='Bay-window sitting room at Portico Suites',
  body=P("Show days for the bridal trade are full of appointments. The bay-window sitting room is somewhere to step back, review notes and decide on orders, and the garden terrace has views of a church spire when the weather allows a coffee outside.",
  "Each person gets their own bedroom, which matters when a team has been talking to buyers all day.")),
 dict(h2='Retailers, Designers and Their Teams',img=I_KIT,alt='Dining kitchen at Portico Suites',
  body=P("A boutique owner might travel with a manager and a stylist; a designer might bring a sales agent. One booking for the whole group is simpler than coordinating several rooms.",
  "The house is a 7-minute walk to the centre of Harrogate for dinner, and the full kitchen is there if you would rather stay in. "+DATES))],
 [("When is Bridal Week Harrogate held?","It runs twice a year, in March and September, at the Harrogate Convention Centre. Check the organiser's website for exact dates."),
  ("Can a boutique team book for just a few nights?","Yes. Book the nights you need around your appointments."),
  ("Is there space to sit and review orders?","Yes. There is a bay-window sitting room, a dining table that seats the whole party and fast Wi-Fi throughout."),
  STD_FAQS[0]]),

event('harrogate-nursery-fair-accommodation','Nursery Fair','Accommodation for Harrogate International Nursery Fair',
 'Harrogate International Nursery Fair — Where to Stay in October | Portico Suites',
 'Attending Harrogate International Nursery Fair in October? A 7-bedroom house sleeping 10, a 3-minute walk from the Convention Centre. Book direct.',
 "The nursery trade meets in Harrogate every October. If your brand or buying team is going, here is a place to stay together near the halls.",BEDS[1],[
 dict(h2='An Autumn Fair for Product Launches',img=BEDS[1],alt='Mustard bedroom at Portico Suites',
  body=P("Harrogate International Nursery Fair moved permanently to October from 2022, a timing its organiser said suits new product launches and retailers planning next year's stock. It is held in the Harrogate Convention Centre, on a single level of halls.",
  "For brands, that means a few intense days of demonstrations and buyer meetings. The house gives the team a quiet place afterwards.")+
  T("October fair at the HCC","3 minutes' walk from the house","Kitchen and laundry for a full week","7 bedrooms, sleeps 10")),
 dict(h2='Showing Products, Not Just Carrying Them',img=I_TAB,alt='Oak dining table at Portico Suites',
  body=P("Prams, car seats and cots are bulky to carry. Staying three minutes' walk from the halls keeps the back-and-forth manageable, and the large oak table is useful for laying out samples and sorting orders.",
  "Free overnight on-street parking outside means the van does not need a separate car park booking.")),
 dict(h2='Retail Buyers and Independent Shops',img=I_SOFA,alt='Leather sofa in the sitting room at Portico Suites',
  body=P("Buyers from independent nursery shops often travel in small groups. A shared house means you can split the cost, compare the day's finds in the sitting room and still have your own bedroom.",
  "The centre of Harrogate is 7 minutes' walk for dinner. "+DATES))],
 [("When is Harrogate International Nursery Fair?","It is held in October at the Harrogate Convention Centre. Check the organiser's website for the exact days."),
  ("Is the house suitable for bringing samples?","Yes. There is a large dining table for laying out products and free overnight on-street parking."),
  ("Can the whole team stay in one place?","Yes. Up to 10 guests across 7 bedrooms, with 5 bathrooms, 4 of them en-suite."),
  STD_FAQS[2]]),

event('home-and-gift-harrogate-accommodation','Home & Gift','Accommodation for Home & Gift Buyers Festival',
 'Home & Gift Harrogate — July Buyers Festival Accommodation | Portico Suites',
 'Staying for the Home & Gift Buyers Festival in Harrogate each July? A 7-bedroom townhouse sleeping 10, 3 minutes from the Convention Centre. Book direct.',
 "Each July the home, gift and interiors trade fills Harrogate. A house for the whole team beats hunting for rooms.",I_SOFA,[
 dict(h2='A Summer Buying Festival',img=I_GAR,alt='Garden terrace at Portico Suites',
  body=P("Home &amp; Gift is a summer buying festival for retailers in homeware, gifts and interiors, centred on the Harrogate Convention Centre in July. The 2026 festival ran 19 to 22 July, and the next is 18 to 21 July 2027.",
  "Portico Suites keeps a team within a 3-minute walk, and in July the garden terrace, with views of a church spire, is a pleasant place for an evening drink after the halls close.")+
  T("Garden terrace for summer evenings","3 minutes' walk to the HCC","Full kitchen &amp; laundry","Self check-in by smart lock")),
 dict(h2='Buyers Who Like to Plan',img=I_TAB,alt='Dining table at Portico Suites',
  body=P("A show for buyers rewards preparation. The dining table seats the whole party, so a team can map out which stands to visit, and the fast Wi-Fi makes placing orders from the house simple.",
  "Seven bedrooms mean everyone has their own space, and the house sleeps up to ten, so a retailer can bring colleagues, a partner or a friend for the trip.")),
 dict(h2='Harrogate After the Show',img=I_EXT,alt='Portico Suites exterior on Franklin Road',
  body=P("From Franklin Road, the town centre is 7 minutes' walk, Bettys is 10 and the Valley Gardens are 10, so there is plenty to see in the evening. For a group staying several nights, that variety is a welcome change from show-floor food.",
  DATES))],
 [("When is the Home & Gift Buyers Festival?","It is held each July, centred on the Harrogate Convention Centre. The 2026 festival ran 19 to 22 July, and the next runs 18 to 21 July 2027."),
  ("Is there outdoor space?","Yes. The garden terrace has quiet seating and views of a church spire."),
  ("Is parking included?","There is free on-street parking overnight, and a reserved space can be added during booking where offered."),
  STD_FAQS[0]]),

event('great-yorkshire-show-accommodation','Great Yorkshire Show','Accommodation for the Great Yorkshire Show',
 'Great Yorkshire Show Accommodation — Large House in Central Harrogate | Portico Suites',
 'Looking for a place to stay for the Great Yorkshire Show in July? A 7-bedroom Harrogate townhouse sleeping 10, a short drive from the showground. Book direct.',
 "Four days in July bring crowds of farmers, families and exhibitors to Harrogate. A house for a group is the easy way to stay together.",I_GAR,[
 dict(h2='A Big Show on the Edge of Town',img=I_GAR,alt='Garden terrace at Portico Suites',
  body=P("The Great Yorkshire Show is held over four days each July at the Great Yorkshire Showground on Railway Road, Harrogate. In 2026 it ran 14 to 17 July.",
  "The showground is on the edge of town, a short drive or taxi from Franklin Road, which makes a base in central Harrogate a good compromise: restaurants and the Stray are close by in the evening.")+
  T("Short drive or taxi to the showground","Central Harrogate base","Garden terrace for summer evenings","Free on-street parking overnight")),
 dict(h2='Families, Exhibitors and Friends Together',img=I_LIV,alt='Sitting room at Portico Suites',
  body=P("A show attracts mixed groups: a farming family, a stand team, friends who go every year. Seven bedrooms and a large dining table mean everyone has a place, and four of the five bathrooms are en-suite.",
  "After a long day on your feet, the sitting room is a place to rest, and the kitchen is there for a proper breakfast before an early start.")),
 dict(h2='Dogs, Early Starts and Late Evenings',img=I_KIT,alt='Dining kitchen at Portico Suites',
  body=P("Well-behaved dogs are welcome, which suits families who bring theirs. Self check-in by smart lock means a late arrival after a day at the show is straightforward.",
  "Check-in is from 3pm and check-out by 10am. "+DATES))],
 [("How far is the Great Yorkshire Showground?","The showground is on the edge of Harrogate, a short drive or taxi from Franklin Road, with central town on your doorstep in the evenings."),
  ("When is the Great Yorkshire Show?","It is held for four days in mid-July. The 2026 show ran 14 to 17 July."),
  ("Can we bring a dog?","Yes. Well-behaved dogs are welcome."),
  STD_FAQS[0]]),

event('crime-writing-festival-harrogate-accommodation','Crime Writing Festival','Accommodation for the Theakston Old Peculier Crime Writing Festival',
 'Crime Writing Festival Harrogate — Group Accommodation in Town | Portico Suites',
 'Staying for the Theakston Old Peculier Crime Writing Festival at the Old Swan Hotel? A 7-bedroom Harrogate townhouse sleeping 10. Book direct.',
 "Every July, readers and writers gather in Harrogate for a long weekend of crime fiction. A house is a good base for a group of friends who read together.",I_LIV,[
 dict(h2='Four Days Based Around the Old Swan',img=I_LIV,alt='Sitting room at Portico Suites',
  body=P("The Theakston Old Peculier Crime Writing Festival is held each July in Harrogate. The 2026 festival ran 23 to 26 July at the Old Swan Hotel and drew a programme of well over a hundred crime and thriller writers.",
  "The festival is based at the Old Swan Hotel in central Harrogate rather than at the Convention Centre, so staying in town suits it well. The Old Swan is an 8-minute walk from Franklin Road.")+
  T("8 minutes' walk to the Old Swan","7 bedrooms, sleeps 10","Sitting room for post-panel debates","Kitchen for slow mornings")),
 dict(h2='A Group of Readers Under One Roof',img=I_SOFA,alt='Leather sofa at Portico Suites',
  body=P("Festival-goers often book as a group of friends. A house gives each person their own bedroom while keeping everyone together in the evening, when the real conversation about who did it begins.",
  "The sitting room and its fireplace are suited to that, and the dining table seats the whole group for breakfast.")),
 dict(h2='Harrogate Between Events',img=I_EXT,alt='Portico Suites exterior on Franklin Road',
  body=P("Between sessions there is plenty to do: Bettys tea rooms are 10 minutes' walk, the Valley Gardens 10 minutes and the Stray close by. July is a busy month in Harrogate, so it is worth booking early.",
  DATES))],
 [("Where is the Crime Writing Festival held?","It is based at the Old Swan Hotel in central Harrogate, not at the Convention Centre. The Old Swan is an 8-minute walk from Portico Suites."),
  ("When is the festival?","It is held each July. The 2026 festival ran 23 to 26 July."),
  ("How many can stay?","Up to 10 guests across 7 bedrooms with 5 bathrooms, 4 of them en-suite."),
  STD_FAQS[2]]),

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
 desc='Contractor accommodation in central Harrogate: 7 private bedrooms, 5 bathrooms, kitchen, laundry and fast Wi-Fi for up to 10. Weekly and monthly stays, one direct booking.',
 eyebrow='Contractor Stays', h1='Contractor Accommodation in Harrogate',
 intro='Portico Suites is contractor accommodation in central Harrogate: 7 private bedrooms, 5 bathrooms, a full kitchen, laundry and fast Wi-Fi for up to 10 people on one booking. Weekly and monthly stays are welcome.',
 hero_img=BEDS[5], sections=[
 dict(h2='One House Instead of Scattered Rooms', img=I_KIT, alt='Kitchen at contractor accommodation Harrogate',
  body=P("Long jobs need somewhere that works. Here that means seven separate bedrooms so the crew is not sharing, five bathrooms (four en-suite) so mornings move, a kitchen for cooking instead of eating out every night, and a washer and dryer on site.",
  "Everyone stays together, which makes lifts to site and early starts simpler than a spread of B&B rooms.")+
  T("7 private rooms, no sharing","5 bathrooms, 4 en-suite","Kitchen &amp; laundry on site","Sleeps up to 10")),
 dict(h2='A Working Week at the House', img=I_TAB, alt='Oak dining table for paperwork and planning at Portico Suites',
  body=P("The large oak dining table doubles as a place for paperwork and planning, and Wi-Fi is fast throughout.",
  "Self check-in by smart lock means a crew can arrive after site hours without waiting for anyone. Check-in is from 3pm (early check-in from 1pm can be added during booking) and check-out is by 10am.")),
 dict(h2='Parking and Vehicles', img=I_EXT, alt='Franklin Road exterior at Portico Suites Harrogate',
  body=P("There is free on-street parking overnight around the house, and a reserved space can be added during booking where offered. Tell us how many vehicles you will bring when you book, and we will advise honestly on what works for your crew.")),
 dict(h2='Weekly and Monthly Stays', img=BEDS[5], alt='Private bedroom for contractors at Portico Suites',
  body=P("Weekly and monthly bookings are welcome, including Monday-to-Friday patterns. Weekly and monthly rates are by direct enquiry, so contact us with your project dates for a quote.",
  "Booking the whole house directly means one payment and one confirmation for the crew, with no online-travel-agency fees.")+
  T("Weekly &amp; monthly stays welcome","Monday-to-Friday patterns welcome","One payment for the whole house","Rates by direct enquiry")),
 dict(h2='Evenings in Harrogate', img=I_FIRE, alt='Sitting room with fireplace at Portico Suites',
  body=P("After a day on site, Franklin Road is a 7-minute walk to the town centre, 10 minutes to Bettys and the Valley Gardens, and 12 minutes to the rail station.",
  "The A1(M) and A61 are an easy drive for site work across North Yorkshire. For corporate groups with different needs, see our <a href=\"/corporate-accommodation-harrogate/\">corporate accommodation guide</a>."))],
 faqs=[("Do you take long-term contractor bookings?","Yes. Weekly and monthly stays are welcome, including Monday-to-Friday patterns. Contact us with your project dates for a direct quote."),
 ("Is there somewhere to park vans?","There is free on-street parking overnight around Franklin Road, and a reserved space can be added during booking where offered. Tell us your vehicles when booking and we will advise honestly."),
 ("Can the whole crew stay in one booking?","Yes. The house sleeps up to 10 across 7 private bedrooms, with 5 bathrooms, 4 of them en-suite."),
 ("Can we arrive after working hours?","Yes. Check-in is by smart lock from 3pm, so the crew can arrive when they finish. Early check-in from 1pm can be added during booking."),
 ("Is there laundry and a kitchen?","Yes. There is a full kitchen and a washer and dryer in the house."),
 ("Is the Wi-Fi good enough for work?","Wi-Fi is fast and runs throughout the house, and there is a large dining table to work at."),
 STD_FAQS[2]]),
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
{FAVICON}
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
{guides_block()}
<footer>PORTICO SUITES \u00b7 Franklin Road, Harrogate HG1 5EN \u00b7 <a href="/">porticosuites.com</a> \u00b7 <a href="/#book">Book Direct</a></footer>
</body></html>"""

def journal_index(allposts):
    cards="".join(f"""<a class="jcard" href="/journal/{_slug(t)}/"><img src="{IMG}/{c}" alt="{t}" loading="lazy"><div class="jbody"><time>{d}</time><h3>{t}</h3><p>{e}</p></div></a>""" for (t,d,c,e,_) in allposts)
    return f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Journal \u2014 Notes From Franklin Road | Portico Suites Harrogate</title>
<meta name="description" content="Guides, local knowledge and seasonal notes from Portico Suites \u2014 a 7-bedroom holiday home in central Harrogate sleeping 10.">
<link rel="canonical" href="{BASE}/journal/">
{FAVICON}
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
{guides_block()}
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
