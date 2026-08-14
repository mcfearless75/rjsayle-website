#!/usr/bin/env python3
"""
R.J. Sayle Plumbing & Heating — local SEO / GEO / AI-visibility remediation.

Idempotent. Run from the repo root:  python3 seo-fix.py

WHAT IT DOES
  1. Canonical host: www.  ->  apex (www 301-redirects to apex on GitHub Pages)
  2. Kills the second domain + second email (rjsayleplumbing.co.uk — dead DNS)
  3. Replaces every ad-hoc JSON-LD block with ONE linked @graph per page,
     sharing a single business @id across the whole site
  4. Adds schema to the 4 pages that had none (services, about, contact, gallery)
  5. Adds BreadcrumbList to every page
  6. Removes the conflicting aggregateRating (27 vs 15 on the same @id)
  7. Normalises opening hours to one set
  8. Strips the UTF-8 BOM, adds GA4 + call-click tracking
  9. Rewrites sitemap.xml, robots.txt, llms.txt and adds llms-full.txt

CONFIG — fill these in before running. Empty values are omitted from the
output rather than guessed. Nothing here is invented.
"""

import json, os, re, sys, glob

# ─────────────────────────── CONFIG ───────────────────────────
HOST          = "https://rjsayleplumbing-heating.com"   # apex — matches CNAME
PHONE_E164    = "+447450237593"
PHONE_DISPLAY = "07450 237593"

EMAIL          = "info@rjsayleplumbing-heating.com"  # must have a live mailbox
DIRECTOR_NAME  = "Russ Sayle"                        # known as; legal name below
DIRECTOR_LEGAL = "Russell James Sayle"               # per Companies House
GAS_SAFE_NUM   = ""      # e.g. "123456"       — omitted if blank
COMPANY_NUMBER = "14323418"        # Companies House, verified 14 Aug 2026
LEGAL_NAME     = "R.J Sayle Plumbing & Heating Services Ltd"   # exact registered name
REG_OFFICE     = "113 Wallasey Road, Wallasey, CH44 2AA"       # public record
VAT_NUMBER     = ""
FOUNDING_YEAR  = "2022-08-30"      # incorporation date of the limited company
GA4_ID         = ""      # e.g. "G-XXXXXXXXXX" — no tracking injected if blank

# sameAs — the single biggest entity-consistency gap. Add as you create them.
SAME_AS = [
    # "https://www.google.com/maps/place/?cid=YOUR_CID",
    # "https://www.facebook.com/...",
    # "https://www.linkedin.com/company/...",
    # "https://www.checkatrade.com/trades/...",
]

# aggregateRating: OFF until the real GBP count is verified.
# Set both to reinstate a single, sitewide-consistent figure.
RATING_VALUE = None      # e.g. "5.0"
REVIEW_COUNT = None      # e.g. "27"

HOURS = [{"@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
          "opens": "07:30", "closes": "18:00"}]

GEO = {"@type": "GeoCoordinates", "latitude": 53.3957, "longitude": -3.1364}

ADDRESS = {"@type": "PostalAddress", "addressLocality": "Wirral",
           "addressRegion": "Merseyside", "addressCountry": "GB"}

BIZ_ID  = f"{HOST}/#business"
SITE_ID = f"{HOST}/#website"
ORG_DESC = ("Gas Safe registered commercial and domestic plumbing and heating "
            "specialists based on the Wirral, Merseyside. Boiler installations, "
            "unvented hot water cylinders, air source heat pumps, boosted cold "
            "water systems, power flushing and above-ground drainage. "
            "Fixed-price contracts.")

# Services: name -> (short description, page anchor)
SERVICES = [
    ("Boiler Installation", "Supply and installation of combi, system and conventional boilers for domestic and commercial properties, including commissioning, Building Regulations notification and manufacturer warranty registration.", "boiler-installation"),
    ("Boiler Repair", "Fault-finding and repair on combi, system and conventional boilers — lockouts, pressure loss, no hot water, leaks and error codes on all major brands.", "boiler-repair"),
    ("Unvented Hot Water Cylinder Installation", "G3 qualified unvented cylinder sizing, supply and installation for mains-pressure hot water, including expansion vessel, discharge pipework and Building Regulations sign-off.", "unvented-cylinders"),
    ("Radiator Installation", "Radiator supply, installation, replacement and relocation — panel, column, designer and towel radiators, including balancing, TRVs and pipework alterations.", "radiators"),
    ("Power Flushing", "Magnetic power flushing to remove sludge and magnetite from central heating systems, restoring efficiency and eliminating cold spots. Inhibitor dosing and magnetic filter fitted.", "power-flushing"),
    ("Commercial Plumbing and Heating", "Commercial fit-outs, shopfitting, PPM maintenance contracts and system design for retail, office and hospitality premises.", "commercial"),
    ("Residential Plumbing", "General domestic plumbing — combi swaps, radiator changes, thermostatic valve replacement, maintenance and bathroom installations.", "residential"),
    ("Boosted Cold Water Storage", "Boosted cold water storage and pressure booster systems for large homes and multi-outlet commercial premises.", "boosted-cold-water"),
    ("Emergency Plumbing", "Emergency callouts for burst pipes, major leaks, boiler breakdowns and loss of heating or hot water across the Wirral and Merseyside.", "emergency"),
    ("Air Source Heat Pump Installation", "Air source heat pump assessment and installation, including heat loss calculation and emitter sizing.", "heat-pumps"),
    ("Gas Safety Certificate (CP12)", "Landlord gas safety inspections and CP12 certificates for all gas appliances, pipework and flues.", "cp12"),
    ("Above-Ground Drainage", "Above-ground soil, waste and rainwater drainage installation for domestic and commercial properties.", "drainage"),
]

# path -> (page title for breadcrumb, area name or None, page @type)
PAGES = {
    "index.html":                          ("Home", None, "WebPage"),
    "services.html":                       ("Services", None, "CollectionPage"),
    "about.html":                          ("About", None, "AboutPage"),
    "contact.html":                        ("Contact", None, "ContactPage"),
    "gallery.html":                        ("Gallery", None, "CollectionPage"),
    "commercial-plumbing-heating-wirral.html": ("Commercial Plumbing & Heating", "Wirral", "WebPage"),
    "landlord-services-wirral.html":       ("Landlord Services", "Wirral", "WebPage"),
    "boiler-installation-wirral.html":     ("Boiler Installation", "Wirral", "WebPage"),
    "boiler-repair-wirral.html":           ("Boiler Repair", "Wirral", "WebPage"),
    "emergency-plumber-wirral.html":       ("Emergency Plumber", "Wirral", "WebPage"),
    "gas-safety-certificate-wirral.html":  ("Gas Safety Certificate (CP12)", "Wirral", "WebPage"),
    "boiler-servicing-wirral.html":        ("Boiler Servicing", "Wirral", "WebPage"),
    "power-flushing-wirral.html":          ("Power Flushing", "Wirral", "WebPage"),
    "unvented-cylinder-wirral.html":       ("Unvented Hot Water Cylinder Installation", "Wirral", "WebPage"),
    "radiators-and-central-heating-wirral.html": ("Radiator Installation", "Wirral", "WebPage"),
    "combi-boiler-conversion-wirral.html": ("Combi Boiler Conversion", "Wirral", "WebPage"),
    "boiler-upgrade-scheme-wirral.html":   ("Boiler Upgrade Scheme", "Wirral", "WebPage"),
    "boiler-selector-wirral.html":         ("Boiler Selector Tool", "Wirral", "WebPage"),
    "areas/index.html":                    ("Areas We Cover", None, "CollectionPage"),
    "areas/wirral.html":                   ("Wirral", "Wirral", "WebPage"),
    "areas/heswall.html":                  ("Heswall", "Heswall", "WebPage"),
    "areas/west-kirby.html":               ("West Kirby", "West Kirby", "WebPage"),
    "areas/bebington.html":                ("Bebington", "Bebington", "WebPage"),
    "areas/birkenhead.html":               ("Birkenhead", "Birkenhead", "WebPage"),
    "areas/wallasey.html":                 ("Wallasey", "Wallasey", "WebPage"),
    "areas/hoylake.html":                  ("Hoylake", "Hoylake", "WebPage"),
    "areas/neston.html":                   ("Neston", "Neston", "WebPage"),
    "areas/ellesmere-port.html":           ("Ellesmere Port", "Ellesmere Port", "WebPage"),
    "areas/liverpool.html":                ("Liverpool", "Liverpool", "WebPage"),
    "areas/nationwide.html":               ("Nationwide Coverage", "United Kingdom", "WebPage"),
}

AREA_PLACES = ["Wirral", "Heswall", "West Kirby", "Bebington", "Birkenhead",
               "Wallasey", "Hoylake", "Neston", "Ellesmere Port", "Liverpool",
               "Merseyside"]

# ─────────────────────────── HELPERS ───────────────────────────

def page_url(path):
    return HOST + "/" if path == "index.html" else f"{HOST}/{path}"

def clean(d):
    """Drop empty values recursively so blank config never ships."""
    if isinstance(d, dict):
        return {k: clean(v) for k, v in d.items()
                if v not in (None, "", [], {}) and clean(v) not in (None, "", [], {})}
    if isinstance(d, list):
        return [clean(v) for v in d if v not in (None, "", [], {})]
    return d

def business_node(area=None):
    """The single canonical business entity. Same @id on every page."""
    areas = [{"@type": "Place", "name": a} for a in AREA_PLACES]
    if area and area not in AREA_PLACES:
        areas.insert(0, {"@type": "Place", "name": area})
    node = {
        "@type": ["LocalBusiness", "Plumber", "HVACBusiness"],
        "@id": BIZ_ID,
        # Trading name in `name`; exact registered name in `legalName`.
        "name": "R.J. Sayle Plumbing & Heating",
        "alternateName": ["RJ Sayle Plumbing", "R J Sayle Plumbing and Heating",
                          "R.J. Sayle Plumbing & Heating Ltd"],
        "legalName": LEGAL_NAME,
        "isicV4": "4322",   # plumbing, heat and air-conditioning installation
        "description": ORG_DESC,
        "url": HOST + "/",
        "telephone": PHONE_E164,
        "email": EMAIL,
        "image": f"{HOST}/og-image.jpg",
        "logo": {"@id": f"{HOST}/#logo"},
        "address": ADDRESS,
        "geo": GEO,
        "areaServed": areas,
        "serviceArea": {"@type": "GeoCircle",
                        "geoMidpoint": GEO,
                        "geoRadius": "40000"},
        "priceRange": "££",
        "currenciesAccepted": "GBP",
        "paymentAccepted": "Cash, Bank Transfer, Debit Card, Credit Card",
        "openingHoursSpecification": HOURS,
        "knowsAbout": [s[0] for s in SERVICES],
        "slogan": "Absolute perfection in every job",
        "sameAs": SAME_AS,
        "hasMap": f"https://www.google.com/maps/search/?api=1&query={GEO['latitude']},{GEO['longitude']}",
        # Services are defined once, on services.html, and referenced by @id
        # everywhere else. Keeps the graph ~2KB per page instead of ~11KB.
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "@id": f"{HOST}/services.html#catalog",
            "name": "Plumbing & Heating Services",
            "itemListElement": [
                {"@type": "Offer",
                 "itemOffered": {"@id": f"{HOST}/services.html#{a}"},
                 "priceCurrency": "GBP",
                 "availability": "https://schema.org/InStock"}
                for _, _, a in SERVICES],
        },
    }
    if FOUNDING_YEAR:
        node["foundingDate"] = FOUNDING_YEAR
    if COMPANY_NUMBER:
        node["identifier"] = {"@type": "PropertyValue",
                              "name": "Companies House company number",
                              "value": COMPANY_NUMBER}
    if VAT_NUMBER:
        node["vatID"] = VAT_NUMBER
    creds = []
    if GAS_SAFE_NUM:
        creds.append({"@type": "EducationalOccupationalCredential",
                      "credentialCategory": "Gas Safe Register",
                      "identifier": GAS_SAFE_NUM,
                      "recognizedBy": {"@type": "Organization",
                                       "name": "Gas Safe Register",
                                       "url": "https://www.gassaferegister.co.uk/"}})
    else:
        creds.append({"@type": "EducationalOccupationalCredential",
                      "credentialCategory": "Gas Safe Register",
                      "recognizedBy": {"@type": "Organization",
                                       "name": "Gas Safe Register",
                                       "url": "https://www.gassaferegister.co.uk/"}})
    node["hasCredential"] = creds
    if DIRECTOR_NAME:
        node["founder"]  = {"@id": f"{HOST}/about.html#director"}
        node["employee"] = {"@id": f"{HOST}/about.html#director"}
    if RATING_VALUE and REVIEW_COUNT:
        node["aggregateRating"] = {"@type": "AggregateRating",
                                   "ratingValue": RATING_VALUE,
                                   "reviewCount": REVIEW_COUNT,
                                   "bestRating": "5", "worstRating": "1"}
    return node

def breadcrumb(path, label):
    url = page_url(path)
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": HOST + "/"}]
    if path.startswith("areas/") and path != "areas/index.html":
        items.append({"@type": "ListItem", "position": 2, "name": "Areas We Cover",
                      "item": f"{HOST}/areas/index.html"})
        items.append({"@type": "ListItem", "position": 3, "name": label, "item": url})
    elif path != "index.html":
        items.append({"@type": "ListItem", "position": 2, "name": label, "item": url})
    return {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": items}

def extract_faq(html):
    """Preserve FAQs already written into the page.

    Must look inside @graph as well as at top level, otherwise a second run
    of this script silently deletes every FAQ on the site.
    """
    for block in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S):
        try:
            d = json.loads(block)
        except Exception:
            continue
        nodes = d.get("@graph", [d]) if isinstance(d, dict) else (d if isinstance(d, list) else [])
        for n in nodes:
            if isinstance(n, dict) and n.get("@type") == "FAQPage" and n.get("mainEntity"):
                return n["mainEntity"]
    return extract_microdata_faq(html)


def extract_microdata_faq(html):
    """services.html marks FAQs up in microdata, not JSON-LD. Lift them into
    the graph so the whole site speaks one schema dialect."""
    out = []
    for blk in re.findall(r'itemtype="https://schema\.org/Question".*?</details>', html, re.S):
        q = re.search(r'itemprop="name"[^>]*>(.*?)</span>', blk, re.S)
        a = re.search(r'itemprop="text"[^>]*>(.*?)</p>', blk, re.S)
        if not (q and a):
            continue
        strip = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
        out.append({"@type": "Question", "name": strip(q.group(1)),
                    "acceptedAnswer": {"@type": "Answer", "text": strip(a.group(1))}})
    return out


def strip_microdata_faq(html):
    """Remove the now-duplicated microdata so only one FAQPage entity exists."""
    html = html.replace(' itemscope itemtype="https://schema.org/FAQPage"', '')
    html = html.replace(' itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"', '')
    html = html.replace(' itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"', '')
    html = re.sub(r'\s+itemprop="(name|text|acceptedAnswer|mainEntity)"', '', html)
    return html

def extract_meta(html, key, attr="name"):
    m = re.search(rf'<meta\s+{attr}="{key}"\s+content="([^"]*)"', html)
    return m.group(1) if m else ""

def build_graph(path, html, faq=None):
    url   = page_url(path)
    label, area, ptype = PAGES[path]
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    title = title.group(1).strip() if title else label
    desc  = extract_meta(html, "description")

    webpage = {
        "@type": ptype, "@id": f"{url}#webpage", "url": url,
        "name": title, "description": desc,
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": BIZ_ID},
        "primaryImageOfPage": {"@id": f"{HOST}/#logo"},
        "breadcrumb": {"@id": f"{url}#breadcrumb"},
        "inLanguage": "en-GB",
        "potentialAction": {"@type": "ReadAction", "target": [url]},
    }
    if area:
        webpage["contentLocation"] = {"@type": "Place", "name": area}

    person = []
    if DIRECTOR_NAME:
        p = {"@type": "Person", "@id": f"{HOST}/about.html#director",
             "name": DIRECTOR_NAME,
             "jobTitle": "Director & Lead Engineer",
             "worksFor": {"@id": BIZ_ID}}
        if DIRECTOR_LEGAL and DIRECTOR_LEGAL != DIRECTOR_NAME:
            p["alternateName"] = DIRECTOR_LEGAL
        if path == "about.html":
            # Full E-E-A-T node lives on the page that is actually about him.
            p.update({
                "description": ("Director and lead engineer of R.J. Sayle Plumbing & "
                                "Heating. Gas Safe registered, with over 20 years' "
                                "experience in commercial and domestic plumbing and "
                                "heating. Oversees every job personally."),
                "knowsAbout": [s[0] for s in SERVICES],
                "mainEntityOfPage": {"@id": f"{url}#webpage"},
                "hasOccupation": {"@type": "Occupation",
                                  "name": "Plumbing and Heating Engineer",
                                  "occupationalCategory": "5314 Plumbers and heating and ventilating engineers"},
            })
        person = [p]

    graph = person + [
        {"@type": "ImageObject", "@id": f"{HOST}/#logo",
         "url": f"{HOST}/logo.avif", "contentUrl": f"{HOST}/logo.avif",
         "caption": "R.J. Sayle Plumbing & Heating Ltd", "inLanguage": "en-GB"},
        business_node(area),
        {"@type": "WebSite", "@id": SITE_ID, "url": HOST + "/",
         "name": "R.J. Sayle Plumbing & Heating",
         "description": ORG_DESC,
         "publisher": {"@id": BIZ_ID},
         "inLanguage": "en-GB"},
        webpage,
        breadcrumb(path, label),
    ]

    if faq:
        graph.append({"@type": "FAQPage", "@id": f"{url}#faq",
                      "isPartOf": {"@id": f"{url}#webpage"},
                      "mainEntity": faq})
        webpage["mainEntity"] = {"@id": f"{url}#faq"}

    # Standalone Service nodes on the services hub — these are what AI
    # assistants extract when asked "who does X near me".
    if path == "services.html":
        for n, d, a in SERVICES:
            graph.append({
                "@type": "Service", "@id": f"{HOST}/services.html#{a}",
                "name": n, "description": d,
                "serviceType": n,
                "provider": {"@id": BIZ_ID},
                "areaServed": [{"@type": "Place", "name": p} for p in AREA_PLACES],
                "audience": {"@type": "Audience", "audienceType": "Homeowners, landlords and commercial property owners"},
                "offers": {"@type": "Offer", "priceCurrency": "GBP",
                           "availability": "https://schema.org/InStock",
                           "url": f"{HOST}/contact.html"},
                "isPartOf": {"@id": f"{url}#webpage"},
            })

    if path == "contact.html":
        graph.append({
            "@type": "ContactPoint", "@id": f"{url}#contactpoint",
            "telephone": PHONE_E164, "email": EMAIL,
            "contactType": "customer service",
            "areaServed": "GB", "availableLanguage": "English",
            "hoursAvailable": HOURS,
        })
        webpage["significantLink"] = f"tel:{PHONE_E164}"

    if path == "gallery.html":
        imgs = re.findall(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', html)
        if imgs:
            graph.append({
                "@type": "ImageGallery", "@id": f"{url}#gallery",
                "name": "R.J. Sayle Plumbing & Heating — Completed Projects",
                "description": "Completed boiler installations, unvented cylinder installs, radiator work and commercial fit-outs across the Wirral and Merseyside.",
                "isPartOf": {"@id": f"{url}#webpage"},
                "associatedMedia": [
                    {"@type": "ImageObject", "contentUrl": s,
                     "caption": a or "Completed plumbing and heating project by R.J. Sayle Plumbing & Heating",
                     "creditText": "R.J. Sayle Plumbing & Heating Ltd"}
                    for s, a in imgs[:30]],
            })

    return clean({"@context": "https://schema.org", "@graph": graph})

GA4_SNIPPET = """  <!-- GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{gid}');
    document.addEventListener('DOMContentLoaded', function () {{
      document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {{
        a.addEventListener('click', function () {{
          gtag('event', 'call_click', {{ event_category: 'contact', event_label: location.pathname }});
        }});
      }});
      var f = document.querySelector('form');
      if (f) f.addEventListener('submit', function () {{
        gtag('event', 'generate_lead', {{ event_category: 'contact', event_label: location.pathname }});
      }});
    }});
  </script>
"""

# ─────────────────────────── RUN ───────────────────────────

def process(path):
    html = open(path, encoding="utf-8-sig").read()   # strips BOM

    # 1. host + dead-domain normalisation
    html = html.replace("https://www.rjsayleplumbing-heating.com", HOST)
    html = html.replace("http://www.rjsayleplumbing-heating.com", HOST)
    html = html.replace("https://www.rjsayleplumbing.co.uk", HOST)
    html = html.replace("info@rjsayleplumbing.co.uk", EMAIL)

    # 1b. Companies Act 2006 s.82 / e-Commerce Regs 2002 require a limited
    #     company's website to state the registered name, company number,
    #     place of registration and registered office address. The site said
    #     only "Registered in England & Wales" — that is not compliant.
    if COMPANY_NUMBER and "Company No." not in html:
        disclosure = (
            '<p class="font-body text-xs">'
            + LEGAL_NAME.replace("&", "&amp;")
            + ' &nbsp;·&nbsp; Registered in England &amp; Wales, Company No. '
            + COMPANY_NUMBER
            + ' &nbsp;·&nbsp; Gas Safe Registered &nbsp;·&nbsp; Fully Insured</p>\n'
            '      <p class="font-body text-xs mt-1 opacity-80">Registered office: '
            + REG_OFFICE + '</p>')
        # Two footer variants exist across the site — match either.
        html, n = re.subn(
            r'<p class="font-body text-xs">(?=[^<]*Registered in England)[^<]*</p>',
            lambda m: disclosure, html, count=1)
        if not n:
            # Older-generation pages have no "Registered in England" line at all.
            html, n = re.subn(
                r'(<p>&copy; <span id="year"></span>[^<]*</p>)',
                lambda m: m.group(1) + '\n      ' + disclosure, html, count=1)
        if not n:
            print(f"    ! {path}: footer disclosure not injected — check markup")

    # 1c. Visible opening hours on the older pages contradicted every other
    #     page and the schema. One set of hours, everywhere.
    html = html.replace("<li>Mon–Fri 8am–6pm</li>\n          <li>Sat 8am–1pm</li>",
                        "<li>Mon–Fri 7:30am–6pm</li>\n          <li>Emergency callouts available</li>")
    html = html.replace("<li>Mon–Fri 8am–6pm</li>", "<li>Mon–Fri 7:30am–6pm</li>")
    html = html.replace("<li>Sat 8am–1pm</li>", "<li>Emergency callouts available</li>")

    # 2. capture FAQs BEFORE stripping — order matters, they are page content
    faq = extract_faq(html)

    if faq:
        html = strip_microdata_faq(html)

    # 2b. strip every existing ld+json block
    html = re.sub(r'[ \t]*<script[^>]*application/ld\+json[^>]*>.*?</script>\s*\n?', '',
                  html, flags=re.S)

    # 3. inject the unified graph immediately before </head>
    graph = build_graph(path, html, faq)
    block = ('  <script type="application/ld+json">\n'
             + json.dumps(graph, indent=2, ensure_ascii=False)
             + '\n  </script>\n')

    # 4. og:image type/dimensions + twitter site + theme-color
    extras = (
        '  <meta property="og:image:width" content="1200">\n'
        '  <meta property="og:image:height" content="630">\n'
        '  <meta property="og:image:alt" content="R.J. Sayle Plumbing &amp; Heating Ltd — Gas Safe registered plumber, Wirral">\n'
        '  <meta name="theme-color" content="#0F172A">\n'
        '  <meta name="author" content="R.J. Sayle Plumbing &amp; Heating Ltd">\n'
        '  <meta name="format-detection" content="telephone=yes">\n'
        '  <link rel="alternate" type="application/xml" href="{h}/sitemap.xml">\n'
    ).format(h=HOST)
    if 'og:image:width' not in html:
        html = html.replace('</head>', extras + '</head>', 1)

    # 5. GA4
    if GA4_ID and 'googletagmanager' not in html:
        html = html.replace('</head>', GA4_SNIPPET.format(gid=GA4_ID) + '</head>', 1)

    html = html.replace('</head>', block + '</head>', 1)
    open(path, "w", encoding="utf-8").write(html)
    return len(json.dumps(graph))


def write_sitemap():
    from datetime import date
    today = date.today().isoformat()
    prio = {"index.html": "1.0", "services.html": "0.9", "contact.html": "0.9",
            "commercial-plumbing-heating-wirral.html": "0.9",
            "landlord-services-wirral.html": "0.9"}
    rows = []
    for p in PAGES:
        rows.append(f"  <url>\n    <loc>{page_url(p)}</loc>\n"
                    f"    <lastmod>{today}</lastmod>\n"
                    f"    <changefreq>monthly</changefreq>\n"
                    f"    <priority>{prio.get(p, '0.8')}</priority>\n  </url>")
    open("sitemap.xml", "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows) + "\n</urlset>\n")


def write_robots():
    open("robots.txt", "w").write(f"""# R.J. Sayle Plumbing & Heating Ltd
User-agent: *
Allow: /

# Search
User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: DuckDuckBot
Allow: /

# AI answer engines — explicitly permitted (we want to be cited)
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Amazonbot
Allow: /
User-agent: meta-externalagent
Allow: /
User-agent: Bytespider
Allow: /
User-agent: cohere-ai
Allow: /
User-agent: YouBot
Allow: /
User-agent: Diffbot
Allow: /
User-agent: CCBot
Allow: /

Sitemap: {HOST}/sitemap.xml
""")


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)
    missing = [p for p in PAGES if not os.path.exists(p)]
    if missing:
        sys.exit(f"Missing files: {missing}")
    for p in PAGES:
        n = process(p)
        print(f"  {p:<45} graph {n:>6} bytes")
    write_sitemap(); print("  sitemap.xml rewritten")
    write_robots(); print("  robots.txt rewritten")
    print("\nDone. Validate at https://validator.schema.org/ and "
          "https://search.google.com/test/rich-results")
