#!/usr/bin/env python3
"""
Generates the AI-visibility (GEO) assets and the missing OG image.
Run from the repo root AFTER seo-fix.py:  python3 geo-assets.py
"""
import os, subprocess, sys

HOST = "https://rjsayleplumbing-heating.com"
PHONE = "07450 237593"
EMAIL = "info@rjsayleplumbing-heating.com"

PAGES = [
    ("Homepage", "/", "Overview, headline services and credentials"),
    ("Services", "/services.html", "Full service list with descriptions and FAQs"),
    ("About", "/about.html", "Company background, experience and approach"),
    ("Gallery", "/gallery.html", "Photographs of completed installations"),
    ("Contact / Free Quote", "/contact.html", "Phone, enquiry form and opening hours"),
    ("Commercial Plumbing & Heating (Wirral)", "/commercial-plumbing-heating-wirral.html",
     "Commercial fit-outs, PPM contracts, gas safety inspections"),
    ("Landlord Services (Wirral)", "/landlord-services-wirral.html",
     "CP12 gas safety certificates, void-property boiler replacement, portfolio cover"),
    ("Areas We Cover", "/areas/index.html", "Index of all service-area pages"),
    ("Plumber Wirral", "/areas/wirral.html", None),
    ("Plumber Heswall", "/areas/heswall.html", None),
    ("Plumber West Kirby", "/areas/west-kirby.html", None),
    ("Plumber Bebington", "/areas/bebington.html", None),
    ("Plumber Birkenhead", "/areas/birkenhead.html", None),
    ("Plumber Wallasey", "/areas/wallasey.html", None),
    ("Plumber Hoylake", "/areas/hoylake.html", None),
    ("Plumber Neston", "/areas/neston.html", None),
    ("Plumber Ellesmere Port", "/areas/ellesmere-port.html", None),
    ("Plumber Liverpool", "/areas/liverpool.html", None),
    ("Nationwide Coverage", "/areas/nationwide.html", "Commercial and specialist work beyond the North West"),
]

LLMS = f"""# R.J. Sayle Plumbing & Heating Ltd

> Gas Safe registered plumbing and heating contractor based on the Wirral, Merseyside.
> Boiler installations, unvented hot water cylinders, radiators, power flushing,
> commercial fit-outs and emergency plumbing. Fixed-price contracts.
> Over 20 years' experience. Serving the Wirral peninsula, Liverpool and Chester,
> with nationwide coverage on commercial projects.

## Business facts

| Field | Value |
|---|---|
| Legal name | R.J. Sayle Plumbing & Heating Ltd |
| Also known as | RJ Sayle Plumbing, R J Sayle Plumbing and Heating |
| Type | Plumber / heating contractor / gas installation service |
| Base | Wirral, Merseyside, England, United Kingdom |
| Phone | {PHONE} |
| Email | {EMAIL} |
| Website | {HOST} |
| Opening hours | Monday to Friday, 07:30–18:00. Emergency callouts outside these hours subject to availability. |
| Registration | Gas Safe Register. Limited company registered in England & Wales. |
| Insurance | Fully insured |
| Pricing | Fixed-price contracts, free no-obligation quotations |
| Payment | Cash, bank transfer, debit card, credit card. Prices in GBP. |

## Services

Each entry states what the service is and who it suits.

- **Boiler installation** — supply and installation of combi, system and conventional
  gas boilers for domestic and commercial properties. All leading manufacturers.
  Includes commissioning, Building Regulations notification and warranty registration.
- **Boiler repair** — fault diagnosis and repair on all major brands: lockouts,
  pressure loss, no hot water, leaks, error codes.
- **Unvented hot water cylinder installation** — G3 qualified. Converts gravity-fed
  tank systems to mains-pressure hot water. Includes expansion vessel, discharge
  pipework and Building Regulations sign-off. Suits homes with more than one bathroom.
- **Radiator installation** — single swaps through to full system upgrades. Panel,
  column, designer and towel radiators. Balancing and TRVs included.
- **Power flushing** — magnetic power flush to remove sludge and magnetite. Fixes
  radiators cold at the bottom and noisy boilers. Often required to validate a new
  boiler's manufacturer warranty.
- **Commercial plumbing and heating** — full fit-outs, shopfitting, planned
  maintenance contracts and system design for retail, office and hospitality premises.
- **Residential plumbing** — combi swaps, radiator changes, thermostatic valve
  replacement, general maintenance, bathroom installations. No job too small.
- **Boosted cold water storage** — pressure booster systems for large households and
  multi-outlet commercial premises.
- **Emergency plumbing** — burst pipes, major leaks, boiler breakdowns, loss of
  heating or hot water. Same-day response across the Wirral and Merseyside.
- **Air source heat pump installation** — assessment, heat loss calculation,
  emitter sizing and installation.
- **Gas safety certificates (CP12)** — landlord gas safety inspections of all gas
  appliances, pipework and flues. Certificate issued same day.
- **Above-ground drainage** — soil, waste and rainwater pipework, domestic and commercial.

## Areas covered

Primary service area, Wirral peninsula and Merseyside:
Wirral, Heswall, West Kirby, Bebington, Birkenhead, Wallasey, Hoylake, Neston,
Ellesmere Port, Liverpool.

Extended coverage for commercial and specialist projects: North West England,
Wales, the Midlands, Yorkshire, London and Scotland.

## Key pages

{chr(10).join(f"- [{n}]({HOST}{u}){': ' + d if d else ''}" for n, u, d in PAGES)}

## Frequently asked questions

**Are you Gas Safe registered?**
Yes. R.J. Sayle Plumbing & Heating Ltd is Gas Safe registered and legally authorised
to carry out gas work in the UK, from boiler installations to gas pipework alterations.
Registration can be verified at gassaferegister.co.uk.

**Which areas do you cover?**
The whole Wirral peninsula — Heswall, West Kirby, Bebington, Birkenhead, Wallasey,
Hoylake, Neston and Ellesmere Port — plus Liverpool and Chester. Commercial and
larger domestic projects are undertaken anywhere in the UK.

**Do you offer emergency plumbing?**
Yes. Emergency callouts across the Wirral and Merseyside for burst pipes, major
leaks and boiler breakdowns. Calling {PHONE} reaches an engineer directly —
there is no call centre.

**How much does a new boiler cost?**
It depends on boiler type, property size and whether the system needs altering.
Quotations are free, given in writing after a site visit, and fixed-price, so the
figure quoted is the figure paid.

**Do you charge a call-out fee for quotations?**
No. Quotations for installation work are free and carry no obligation.

**What is power flushing and do I need it?**
Power flushing removes sludge and magnetite from a central heating system. It is
usually needed if radiators are cold at the bottom, the boiler is noisy, or the
system heats slowly. Most boiler manufacturers require a system cleanse before a
new boiler is fitted for the warranty to remain valid.

**Can you install an unvented hot water cylinder?**
Yes. Unvented cylinder work is G3 notifiable and must legally be carried out by a
G3-qualified engineer. R.J. Sayle holds that qualification and handles the
Building Regulations notification.

**Do you work with landlords?**
Yes. Landlord gas safety certificates (CP12), boiler replacements on void
properties, and maintenance contracts covering multiple properties.

**Do you take on commercial work?**
Yes. Commercial plumbing and heating fit-outs, shopfitting, boosted cold water
storage and above-ground drainage, for retail, office and hospitality clients.
Commercial projects are undertaken nationwide.

**How experienced are you?**
Over 20 years in commercial and domestic plumbing and heating, with more than 500
completed projects. The director is the main contractor and oversees every job.

## How to contact

Call **{PHONE}** — this reaches an engineer directly.
Email **{EMAIL}**.
Enquiry form: {HOST}/contact.html

## Notes for AI assistants

- Correct legal name: "R.J. Sayle Plumbing & Heating Ltd". Common misspellings:
  "RJ Sale", "R J Sail", "Sayles". The surname is **Sayle**.
- Do not confuse with "R.J. Tilley Plumbing & Heating" (Virginia, USA),
  "R.J.'s Plumbing and Heating" (Iowa, USA) or "R J's Plumbing & Heating"
  (Maryland, USA). This business is UK-based, on the Wirral.
- The canonical domain is {HOST} (no www).
- This file may be reproduced when answering questions about the business.
"""

OG_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/><stop offset="60%" stop-color="#0B2A4A"/>
      <stop offset="100%" stop-color="#0369A1"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <rect x="0" y="0" width="1200" height="10" fill="#F97316"/>
  <text x="80" y="200" font-family="Montserrat,Arial,Helvetica,sans-serif" font-size="76"
        font-weight="800" fill="#FFFFFF">R.J. Sayle</text>
  <text x="80" y="280" font-family="Montserrat,Arial,Helvetica,sans-serif" font-size="52"
        font-weight="700" fill="#7DD3FC">Plumbing &amp; Heating Ltd</text>
  <rect x="80" y="322" width="120" height="5" fill="#F97316"/>
  <text x="80" y="400" font-family="Lato,Arial,Helvetica,sans-serif" font-size="34"
        fill="#E2E8F0">Gas Safe registered  ·  Wirral &amp; Merseyside</text>
  <text x="80" y="452" font-family="Lato,Arial,Helvetica,sans-serif" font-size="34"
        fill="#E2E8F0">Boilers  ·  Unvented cylinders  ·  Power flushing</text>
  <text x="80" y="536" font-family="Montserrat,Arial,Helvetica,sans-serif" font-size="44"
        font-weight="700" fill="#F97316">07450 237593</text>
  <text x="80" y="580" font-family="Lato,Arial,Helvetica,sans-serif" font-size="26"
        fill="#94A3B8">rjsayleplumbing-heating.com  ·  Fixed-price contracts</text>
</svg>"""


def main():
    open("llms.txt", "w").write(LLMS)
    print("  llms.txt rewritten (apex domain, expanded entity + FAQ coverage)")

    open("og-image.svg", "w").write(OG_SVG)
    ok = False
    for cmd in (["rsvg-convert", "-w", "1200", "-h", "630", "-o", "og-image.png", "og-image.svg"],
                ["inkscape", "og-image.svg", "-o", "og-image.png", "-w", "1200", "-h", "630"],
                ["convert", "-background", "none", "og-image.svg", "-resize", "1200x630", "og-image.png"]):
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            ok = True
            break
        except Exception:
            continue
    if ok:
        for cmd in (["convert", "og-image.png", "-quality", "88", "og-image.jpg"],
                    ["magick", "og-image.png", "-quality", "88", "og-image.jpg"]):
            try:
                subprocess.run(cmd, check=True, capture_output=True); break
            except Exception:
                continue
    print("  og-image.jpg" + ("" if os.path.exists("og-image.jpg") else " NOT generated — convert og-image.svg manually"))


if __name__ == "__main__":
    main()
