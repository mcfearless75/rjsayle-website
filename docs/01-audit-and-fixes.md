# R.J. Sayle Plumbing & Heating — Local SEO / GEO / AI Visibility Audit
**rjsayleplumbing-heating.com** · GitHub Pages · audited 14 August 2026 against repo `mcfearless75/rjsayle-website@master`

---

## Verdict

The build quality is well above the average trade site — clean semantic HTML, one H1 per page, 100% image alt coverage, a skip-link, 11 area pages, `llms.txt` already present, and AI crawlers explicitly allowed in `robots.txt`. Somebody thought about this.

But **it is currently leaking most of its own authority**, and three things are actively working against it:

1. **Every canonical, OG tag, sitemap entry and schema URL points at `www.`, which 301-redirects to the apex.** Every canonical signal the site owns points at a redirect hop.
2. **The business entity is fragmented and self-contradictory.** Two domains, two email addresses, three sets of opening hours, and two different review counts on the same `@id`.
3. **The entire site's styling depends on `cdn.tailwindcss.com` executing in the visitor's browser.** When I rendered the live build with that CDN unavailable, the page came back completely unstyled. That's a single point of failure sitting in front of every page, plus a Core Web Vitals problem.

Add to that: **zero analytics**, **zero social/citation profiles** (`sameAs: []`), a **404ing OG image**, and **no schema at all** on four pages including `/services.html`.

I've fixed all of it. Everything below is done and in the attached build, except the items marked **ACTION NEEDED** which require information only you have.

**Confidence: high** on everything in Sections 1–3 (verified directly against the repo and live HTTP behaviour). **Moderate** on the traffic impact estimates — no Search Console or analytics data exists to baseline against, which is itself finding #6.

---

## 1. Critical — fixed

### 1.1 Canonical host mismatch (every page)

`CNAME` = `rjsayleplumbing-heating.com` (apex). GitHub Pages therefore serves the apex as canonical and **301-redirects `www.` to it**. Yet:

| Signal | Was | Now |
|---|---|---|
| `<link rel="canonical">` | `https://www.…` | `https://rjsayleplumbing-heating.com/…` |
| `og:url` / `twitter:*` | `https://www.…` | apex |
| All 19 `sitemap.xml` `<loc>` | `https://www.…` | apex |
| JSON-LD `@id`, `url`, `publisher` | `https://www.…` | apex |
| `robots.txt` `Sitemap:` | `https://www.…` | apex |
| `llms.txt` (18 URLs) | `https://www.…` | apex |

Google was being told the canonical version of every page is a URL that redirects. Not fatal, but it dilutes consolidation and wastes crawl budget on a small site that hasn't got any to waste.

> **Note on `.html` vs extensionless.** GitHub Pages serves both `/about` and `/about.html` with a 200 — it cannot 301 between them. Google has indexed the extensionless forms. Canonicals now consistently declare `.html`, which is what every internal link uses, so consolidation will happen via the canonical tag. Don't chase this further; it resolves itself.

### 1.2 A second, dead domain inside your structured data

Four pages — `/areas/index.html`, `/areas/liverpool.html`, `/areas/ellesmere-port.html`, `/areas/nationwide.html` — carried a **different** LocalBusiness entity:

```json
"name":  "RJ Sayle Plumbing & Heating",          // no "Ltd"
"url":   "https://www.rjsayleplumbing.co.uk",    // different domain
"email": "info@rjsayleplumbing.co.uk",           // different mailbox
"openingHoursSpecification": Mon–Fri 08:00–18:00, Sat 08:00–13:00
```

`rjsayleplumbing.co.uk` **has no DNS records at all** — it doesn't resolve, and it has no MX, so `info@rjsayleplumbing.co.uk` is a black hole. Those four pages also had a live `mailto:` in the footer pointing at it.

Anyone who emailed from those pages got silence. Every enquiry sent that way was lost.

**Fixed:** all references replaced with the apex domain and `info@rjsayleplumbing-heating.com` sitewide.

> **ACTION NEEDED — confirm `info@rjsayleplumbing-heating.com` has a working mailbox.** If it doesn't, tell me and I'll strip the email entirely rather than repeat the same failure on a different domain.

### 1.3 Contradictory review counts on the same entity

Same `@id` (`/#business`), three different claims:

- `index.html`, `commercial-…`, `landlord-…` → `reviewCount: 27`, `ratingValue: 5.0`
- 12 area pages → `reviewCount: 15`, `ratingValue: 5`
- Neither verified against the actual Google Business Profile

Two problems. Google doesn't render review rich results for self-serving reviews on `LocalBusiness` anyway, so this was buying nothing — and if the numbers overstate reality, it's a misleading-practice exposure under the DMCCA 2024, which the CMA can now enforce directly.

**Fixed:** `aggregateRating` removed entirely, plus the single hardcoded "Tim G, Brighton" review object.

> **ACTION NEEDED — get the true count from GBP.** Set `RATING_VALUE` and `REVIEW_COUNT` at the top of `seo-fix.py` and re-run; it reinstates one accurate figure sitewide. Leave it off until then.

### 1.4 Opening hours — three versions

`07:30–18:00 Mon–Fri` in most places, `08:00–18:00 Mon–Fri + Sat 08:00–13:00` on four pages, "emergency callouts available" as loose prose.

**Fixed:** normalised to `Mon–Fri 07:30–18:00` everywhere.

> **ACTION NEEDED — confirm this is right, and that it matches GBP exactly.** Do NOT set 24/7 hours for emergency cover; "Open now" filtering will send 3am calls and generate one-star reviews when you don't pick up.

### 1.5 `og-image.jpg` was a 404

Every page referenced `https://…/og-image.jpg`. **The file did not exist in the repo.** Every share on WhatsApp, Facebook, LinkedIn or iMessage rendered with a blank card — and AI assistants that pull OG images for entity cards got nothing.

**Fixed:** generated a branded 1200×630 `og-image.jpg` (attached, source SVG included so you can restyle it) and added the missing `og:image:width`, `og:image:height` and `og:image:alt` tags.

---

## 2. Structured data — rebuilt

### What was wrong

| Issue | Detail |
|---|---|
| No `@graph` | Each page emitted 0–3 **standalone, unlinked** JSON-LD blocks. Entities floated free with nothing joining them. |
| **4 pages had no schema at all** | `services.html`, `about.html`, `contact.html`, `gallery.html` — including your single most commercially important page. |
| No `BreadcrumbList` | Anywhere. Costs you breadcrumb display in SERPs and hurts hierarchy comprehension. |
| No `Service` entities | 12 services described in prose, none marked up. This is exactly what AI assistants extract for "who does X near me". |
| `sameAs: []` | Empty. The single strongest entity-disambiguation signal, unused. |
| No `hasCredential` | Gas Safe registration — your biggest trust asset — not in the graph. |
| No `founder` / `Person` | No E-E-A-T entity despite the About page being built entirely around the director. |
| Mixed dialects | `services.html` used **microdata** FAQ; everywhere else used JSON-LD. |
| `@type` drift | Some pages `[LocalBusiness, Plumber]`, others `[LocalBusiness, Plumber, HVACBusiness]`. |

### What's there now

One `@graph` per page, every node `@id`-addressable and cross-linked, one shared business entity across all 19 pages:

```
ImageObject(#logo)
  └─ LocalBusiness/Plumber/HVACBusiness (#business)   ← ONE @id sitewide
       ├─ address, geo, serviceArea (GeoCircle 40km)
       ├─ areaServed × 11 places
       ├─ openingHoursSpecification
       ├─ hasCredential → Gas Safe Register
       ├─ knowsAbout × 12
       ├─ hasOfferCatalog → 12 Offers, each → Service @id
       └─ sameAs [ ready for your profiles ]
  ├─ WebSite (#website) → publisher → #business
  ├─ WebPage / AboutPage / ContactPage / CollectionPage (#webpage)
  ├─ BreadcrumbList (#breadcrumb)
  ├─ FAQPage (#faq)                       ← preserved, now on services.html too
  ├─ Service × 12 (services.html)         ← new
  ├─ ContactPoint (contact.html)          ← new
  └─ ImageGallery + 24 ImageObject (gallery.html)  ← new
```

**Validation:** all 19 pages parse as valid JSON; exactly one block per page; zero dangling `@id` references; every `canonical` = `og:url` = schema `url`; sitemap and canonicals match exactly.

Schema payload dropped from ~11 KB/page to ~7 KB/page by referencing Services by `@id` rather than inlining them on every page.

### Update — director and company identity now resolved

Confirmed against the public register and built in:

| Field | Value | Source |
|---|---|---|
| Director | **Russ Sayle** (Russell James Sayle) | Companies House officers, sole director since 30 Aug 2022 |
| Registered name | **R.J Sayle Plumbing & Heating Services Ltd** | Companies House |
| Company number | **14323418** | Companies House |
| Incorporated | 30 August 2022 | Companies House |
| Registered office | 113 Wallasey Road, Wallasey, CH44 2AA | Companies House |
| SIC | 43220 — plumbing, heat and air-conditioning installation | Companies House |
| Status | Active. Accounts to 31 Mar 2025 filed; next due 31 Dec 2026 | Companies House |

**A `Person` node for Russ is now on every page** (`#director`), carrying `founder` and `employee` links from the business, with the full E-E-A-T version on `/about.html` — description, `knowsAbout` across all 12 services, and `hasOccupation`. The About page is written entirely around "the director oversees every job" and until now there was no entity behind that claim.

**Three things this surfaced that need your call:**

1. **The registered name has "Services" in it; the site doesn't.** Legal name is *R.J Sayle Plumbing & Heating **Services** Ltd*; the site says *R.J. Sayle Plumbing & Heating Ltd*. I've handled it correctly in schema — `name` is now the trading name *R.J. Sayle Plumbing & Heating*, `legalName` is the exact registered string, and the old form is retained in `alternateName`. **But** using "Ltd" in visible branding attached to a name that isn't the registered one is a business-name disclosure point for his accountant. More practically: **the GBP business name should match real-world signage and the register.** Decide which name is the brand and make site, GBP and every citation say the same thing — this is the single most common cause of NAP drift.

2. **The site was not compliant with the Companies Act 2006 s.82 / e-Commerce Regulations.** A limited company's website must show the registered name, company number, place of registration and registered office address. It showed only "Registered in England & Wales". **Fixed** — a compliant disclosure block now appears in the footer of all 19 pages:

   > R.J Sayle Plumbing & Heating Services Ltd · Registered in England & Wales, Company No. 14323418 · Gas Safe Registered · Fully Insured
   > Registered office: 113 Wallasey Road, Wallasey, CH44 2AA

   The registered office is already public record, so this discloses nothing new. **It is deliberately NOT in the `PostalAddress` schema** — that stays locality-level (Wirral, Merseyside) so GBP can run as a service-area business with the address hidden. Legal disclosure in the footer, no address in the structured data. If you'd rather the registered office moved to an accountant's address first, say so and I'll hold this one line back.

3. **`foundingDate` is now `2022-08-30`, alongside the site's "20+ years experience" claim.** Not a contradiction — the *company* is three years old, the *engineer* has 20+ years — and the schema now expresses exactly that, with the experience on the `Person` node where it belongs. It is defensible and matches the public record, which is a trust signal for both Google and AI systems that cross-reference Companies House. If you'd rather not draw the eye to it, set `FOUNDING_YEAR = ""` and re-run.

**Also fixed in this pass:** four pages (`/areas/index`, `/liverpool`, `/ellesmere-port`, `/nationwide`) still displayed *"Mon–Fri 8am–6pm / Sat 8am–1pm"* in the visible footer — the wrong hours, contradicting every other page. Now normalised to "Mon–Fri 7:30am–6pm / Emergency callouts available" sitewide.

> **ACTION NEEDED — two config values left.** Fill in at the top of `seo-fix.py` and re-run:
> - `GAS_SAFE_NUM` → puts the registration number into `hasCredential`. Strongest trust signal in the trade, and the one thing I can't look up for you.
> - `GA4_ID` → see §5.
> - `SAME_AS` → add each profile URL as you create it (citations plan). **Still the highest-value item in this document.**
> - `RATING_VALUE` / `REVIEW_COUNT` → once verified in GBP.

---

## 3. Performance — the Tailwind problem

`cdn.tailwindcss.com` is the **Tailwind Play CDN**. Tailwind's own documentation says it is not for production. It ships a large JS bundle that scans your DOM and compiles CSS *in the browser, on every page load*.

I rendered the live build headless. **With that CDN unreachable, the page returns completely unstyled** — raw HTML, giant unconstrained images, no layout. Not degraded: broken. That's your entire site depending on a third-party CDN executing JavaScript successfully, on every visit, on every device, including a plumber's customer on 3G in Neston.

It also guarantees a poor LCP and a CLS spike, because nothing can be styled until the JS downloads, parses, scans the DOM and injects a stylesheet.

**Fixed:** compiled Tailwind properly against your existing config and class usage → `assets/tailwind.css`, **28 KB minified**, render-blocking-but-instant, cacheable, zero JS. Swapped the CDN script and inline `tailwind.config` block out of all 19 pages.

Verified with before/after screenshots at 1280×900 on the homepage and an area page — layout is identical and correct.

**One regression this surfaced and I fixed:** Tailwind's Preflight sets `img { height: auto }`, which overrides HTML `height` attributes. The Gas Safe logo rendered at full intrinsic size (roughly 400px tall). Changed the inline style to `height:36px;width:auto` across all 19 files. This bug existed with the CDN too — it just never showed because the CDN wasn't loading in test.

### Also worth knowing

**All 24 gallery images are hotlinked from `static.wixstatic.com`.** They're on a Wix account that presumably relates to an old site. If that account lapses or the media is deleted, your entire gallery 404s, and you have no control over the format, compression or caching. Also: all 24 share the identical alt text `"R.J. Sayle completed plumbing project"` and the identical caption `"Completed Work"` — 24 images with zero image-search value.

**Recommendation:** download all 24, serve them from `/gallery/` in the repo (the folder already exists and is empty), convert to WebP, and write real alt text — *"New Worcester Bosch combi boiler installation, Heswall"* rather than the same string 24 times. That folder is your case-study raw material; see the content plan.

**Also fixed:** stripped a UTF-8 BOM from `index.html` (can trigger quirks mode in some parsers), added `theme-color`, `author`, `format-detection` and a sitemap `<link rel="alternate">`.

---

## 4. AI / GEO layer

You already had `llms.txt`, which puts you ahead of most trade sites. It had problems: every URL was the `www.` variant, it listed "air source heat pumps" as a service that appears nowhere on the actual services page, and it was thin on the disambiguation that matters.

**Rewritten** with: apex URLs, a structured business-facts table, all 12 services with *what it is and who it suits* (the format assistants extract cleanly), full area coverage, 10 FAQs written as directly-quotable answers, and a "Notes for AI assistants" block.

That last block matters more than it looks. Searching your business name surfaces **R.J. Tilley Plumbing & Heating (Virginia)**, **R.J.'s Plumbing and Heating (Iowa)** and **R J's Plumbing & Heating (Maryland)** above or alongside you. Three US businesses with near-identical names are actively competing for your entity. The notes block states the correct spelling, lists common misspellings, names the confusable businesses explicitly and declares the canonical domain.

`robots.txt` also expanded: added `Claude-User`, `Claude-SearchBot`, `Perplexity-User`, `Applebot`, `Applebot-Extended`, `Amazonbot`, `meta-externalagent`, `YouBot`, `Diffbot`, `CCBot`, `DuckDuckBot`.

**The real GEO lever isn't the file — it's `sameAs` and citations.** AI assistants resolve local business entities largely through corroboration across independent sources. You currently have **zero** corroborating sources. One website asserting facts about itself is the weakest possible position. See the citations plan.

---

## 5. Analytics — the biggest commercial gap

**There is no tracking on this site. None.** No GA4, no GTM, no Clarity, no call tracking, no conversion measurement, no Search Console verification tag (there's a `googleb2fc2a05259ba444.html` verification file, so a property may exist — check it).

You cannot tell me how many people visit, which pages convert, whether the area pages earn their keep, or whether any of this work moves revenue. Everything in this document is currently unfalsifiable.

**Prepared, not enabled:** `seo-fix.py` has a `GA4_ID` config. Set it and re-run and it injects GA4 plus two custom events:

- `call_click` — fires on every `tel:` click, with the page path. **This is your primary conversion.** 142 `tel:` links across the site and not one of them is measured.
- `generate_lead` — fires on contact form submit.

**Do this first.** Everything else is guesswork until it's in.

Also: the contact form posts to Formspree (`formspree.io/f/myklezqd`). Confirm it still delivers, and to which mailbox — given the dead-email problem on four pages, it's worth a live test.

---

## 6. What's still missing (not fixable in code)

Ranked by commercial impact.

| # | Gap | Why it matters | Where |
|---|---|---|---|
| 1 | **Zero citations, zero social profiles** | `sameAs: []`. Nothing corroborates the entity. Biggest single constraint on both local pack and AI citation. | `03-citations-and-off-site-plan.md` |
| 2 | **Missed calls** | A ranking Wirral plumber takes 15–30 calls/week on one mobile, while under a boiler. Every missed call goes to the next result in ~20 seconds. A missed-call auto-SMS costs a few pounds a month. | GBP plan §11 |
| 3 | **No analytics** | See §5. | Set `GA4_ID` |
| 4 | **No individual service pages** | 12 services, one page. `/services.html` cannot rank for "boiler installation Wirral", "power flushing Wirral" and "unvented cylinder Wirral" simultaneously. This is your largest untapped keyword surface. | `02-content-gap-and-build-out-plan.md` |
| 5 | **Area pages ~70% templated** | Three near-identical FAQs across 11 pages. Thin-content risk and no differentiation. | Content plan §4 |
| 6 | **Review count unverified** | Blocks reinstating `aggregateRating` and it's a compliance exposure. | GBP plan §9 |
| 7 | **Gallery images hotlinked from Wix** | Dependency risk + 24 images with duplicate alt text. | §3 above |
| 8 | **No pricing signal anywhere** | "Fixed-price contracts" with no indicative figures. Highest-friction objection in the trade. | Content plan §7 |

---

## 7. What I'd do, in order

**This week — 3 hours, mostly yours not mine**

1. Push the fixed build (below). One commit.
2. Set up GA4, drop the ID into `seo-fix.py`, re-run, push.
3. Confirm `info@rjsayleplumbing-heating.com` works. Test the Formspree form end-to-end.
4. Set up missed-call auto-SMS.
5. Claim/verify GBP, hide the address, set 8 named service areas, fix hours to match the site.
6. Search Console: verify the apex property, submit the new sitemap, request indexing on the homepage.
7. Send me `DIRECTOR_NAME`, `GAS_SAFE_NUM`, `COMPANY_NUMBER`, real review count.

**Weeks 2–4**
8. Tier 1 citations — the six that matter (citations plan §3). Add each URL to `SAME_AS`, re-run, push.
9. Start the review ask on every job. This is 70% of the local outcome.
10. Build the top 6 service pages (content plan §2).
11. Download the 24 Wix images into the repo, WebP them, write real alt text.

**Months 2–3**
12. De-templatise the area pages (content plan §4).
13. Manufacturer accreditations — Worcester Bosch / Vaillant installer-finder listings are strong links *and* let you offer extended warranties, which is a genuine sales lever.
14. First case studies from the gallery.
15. Baseline geo-grid scan, then monthly.

---

## 8. Things I'd tell you not to bother with

- **Photo geotagging.** Google strips EXIF on upload. It has never worked. Ignore anyone selling it.
- **GBP messaging setup.** Google discontinued it on 31 July 2024. If anyone quotes for it, they're inventing a deliverable.
- **GBP Products.** Wrong tool for a service business. Do Services properly instead.
- **Bought citation bundles.** Do the six that matter and stop.
- **Call tracking numbers in GBP.** NAP-consistency risk outweighs the benefit at your scale. Just ask customers how they found you and log it.
- **Chasing extensionless vs `.html` URLs.** GitHub Pages can't redirect. Canonicals handle it.
- **A blog, yet.** Nothing on this site converts measurably. Build the service pages and get the tracking in first. Blogging into an unmeasured funnel is the most common way trade sites waste twelve months.

---

## 9. The build

Everything above marked "fixed" is in `rjsayle-website-fixed.zip`.

```
seo-fix.py          canonical host, entity unification, @graph rebuild,
                    breadcrumbs, GA4 injection, sitemap + robots
geo-assets.py       llms.txt rewrite, OG image generation
swap-tailwind.py    Play CDN → compiled stylesheet
fix-img.py          Preflight height-attribute regression
rebuild.sh          runs all of the above from a clean clone
```

All idempotent — safe to re-run after changing config. The config block at the top of `seo-fix.py` is the only thing you should need to edit; blank values are omitted from output rather than guessed, so nothing in your structured data is invented.

**To apply:** unzip over the repo (or `git apply rjsayle-seo.patch`), review the diff, commit, push. GitHub Pages redeploys in about a minute.

**Then verify:** paste the homepage into [validator.schema.org](https://validator.schema.org/) and [Google's Rich Results Test](https://search.google.com/test/rich-results), and run PageSpeed Insights before/after to bank the Tailwind win.

---

*Companion documents: `02-content-gap-and-build-out-plan.md`, `03-citations-and-off-site-plan.md`, `04-google-business-profile-plan.md`.*
