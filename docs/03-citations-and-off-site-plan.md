# Local Citations, NAP Consistency & Off-Site Link Plan
## R.J. Sayle Plumbing & Heating Ltd — Wirral, Merseyside
**Prepared: August 2026. All costs and platform statuses verified this month.**

---

## 0. What I found before writing this (live audit)

I pulled the live site and DNS rather than relying on the brief. Three things change the plan:

1. **`rjsayleplumbing.co.uk` has no DNS records at all.** `getent hosts` returns nothing for the apex or www. It is not hosting a site, and it may not even be registered any more. You cannot redirect a domain that resolves to nothing.
2. **Every canonical on the site points at a URL that 301-redirects.** The site is served from GitHub Pages on the apex (`185.199.108.153`). `www.rjsayleplumbing-heating.com` returns `301 → https://rjsayleplumbing-heating.com/`. Yet `<link rel="canonical">`, `og:url`, all 15 `sitemap.xml` entries and the JSON-LD `url`/`@id` all specify **`https://www.rjsayleplumbing-heating.com/`**. Every canonical signal you own points at a redirect hop.
3. **Four pages carry a second, contradictory LocalBusiness entity.** Confirmed on `/areas/index.html`, `/areas/liverpool.html`, `/areas/ellesmere-port.html`, `/areas/nationwide.html`:

```json
"name": "RJ Sayle Plumbing & Heating",
"url": "https://www.rjsayleplumbing.co.uk",
"email": "info@rjsayleplumbing.co.uk",
"openingHoursSpecification": [ Mon–Fri 08:00–18:00, Sat 08:00–13:00 ],
"aggregateRating": { "ratingValue":"5", "reviewCount":"15" }
```

versus everywhere else:

```json
"name": "R.J. Sayle Plumbing & Heating Ltd",
"url": "https://www.rjsayleplumbing-heating.com",
"openingHoursSpecification": [ Mon–Fri 07:30–18:00 ],   // no Saturday
"aggregateRating": { "reviewCount":"27" }                // homepage; 15 elsewhere
```

Those same four pages also have a live footer `mailto:info@rjsayleplumbing.co.uk` — pointing at a domain with no MX, no A record. **Any customer who clicks it sends mail into a black hole.** That is a revenue bug, not an SEO bug, and it is the single most urgent item in this document.

Also present: `sameAs: []`, self-serving `review`/`aggregateRating` markup on `LocalBusiness` (against Google's structured data guidelines and manual-action bait — one testimonial is attributed to "Tim G, Brighton", which also contradicts the stated service area), no `@id` on the area-page schema so nothing consolidates to one entity, and a placeholder `john@example.com` left in the contact form on `/contact.html`.

**Do not build a single citation until sections 1 and 2 are executed.** Building 40 listings on top of a fractured entity means auditing and re-editing 40 listings later.

---

## 1. NAP canonical record — single source of truth

Store this as a locked document (Google Doc or a `nap.md` in the repo). Every listing, every profile, every schema block copies from here. No paraphrasing, no "close enough".

| Field | Canonical value | Notes for use |
|---|---|---|
| **Legal name** | `R.J. Sayle Plumbing & Heating Ltd` | Use verbatim, with full stops and `Ltd`. Where a platform strips punctuation automatically, accept it — do not pre-strip it yourself. |
| **Fallback name** | `R.J. Sayle Plumbing & Heating` | Only for platforms that reject `Ltd` or ampersands. Never `RJ Sayle Plumbing`. Retire that string entirely. |
| **Do NOT use** | `RJ Sayle Plumbing`, `RJ Sayle Plumbing & Heating`, `R J Sayle` | Currently live in `alternateName` and on four area pages. Remove. |
| **Address** | See §1a — decision required | Service-area business. |
| **Locality** | `Wirral` | |
| **Region** | `Merseyside` | |
| **Country** | `United Kingdom` / `GB` | |
| **Phone (display)** | `07450 237593` | UK national format, single space after the 5th digit. |
| **Phone (E.164)** | `+447450237593` | For schema `telephone` and any platform requiring international format. Already correct on site. |
| **Email** | `info@rjsayleplumbing-heating.com` | **Final call.** See §2. |
| **Website (canonical)** | `https://rjsayleplumbing-heating.com/` | **Apex, no `www`, trailing slash, HTTPS.** This is what the server actually serves. See §2. |
| **Hours** | Mon–Fri 07:30–18:00; Sat 08:00–13:00; Sun closed | Decision required — see §1b. |
| **Emergency** | Stated in description text only, never as 24/7 opening hours | |
| **Primary category** | `Plumber` | |
| **Secondary categories** | `Heating contractor`, `Gasfitter`, `Boiler supplier`, `Commercial refrigeration/HVAC contractor` (where offered) | Cap at 4–5. Adding 10 categories dilutes primary-category relevance in the local pack. |
| **Year established** | `2005` (implied by "20+ years") | Confirm exact year. |
| **Logo** | One 1:1 PNG ≥ 720×720, transparent-safe background, identical file everywhere | |
| **Cover image** | One 16:9 JPG ≥ 1440×810, van + branding, identical everywhere | |

### 1a. Address handling — service-area business, no shopfront

The rule that matters: **do not invent an address, and never use a virtual office, mailbox or co-working address.** Google actively de-lists SABs using mailbox addresses, and a suspension costs you 4–8 weeks of visibility plus reinstatement paperwork.

Your practical options, in order of preference:

1. **Use the real operating address (home or unit), marked "I deliver goods and services to my customers" so it is hidden on Google Business Profile.** This is the correct answer for 95% of UK SABs. Google still verifies against a real address; the public just never sees it. Service areas are then set by town/postcode district.
2. **On directories with a mandatory public address field**, enter the same real address. Consistency beats privacy here — the address is already public via Companies House registered office in any case (see §1c).
3. **On directories that permit locality-only**, enter `Wirral, Merseyside` plus the postcode district (e.g. `CH43`) and nothing more.

Set the GBP service area to the **towns**, not a radius: Birkenhead, Wallasey, Bebington, Heswall, West Kirby, Hoylake, Neston, Ellesmere Port, Liverpool, Chester. Cap it at 20 areas; Google has soft-ignored oversized service areas for years, and a 60-mile radius actively dilutes proximity relevance in the Wirral core.

### 1b. Hours

You currently publish two different sets. Pick one and never deviate. My recommendation, absent client input:

```
Monday–Friday   07:30 – 18:00
Saturday        08:00 – 13:00
Sunday          Closed
```

Do **not** publish 24/7 hours to capture "emergency plumber Wirral". If you list 24-hour opening and don't answer at 03:00, you collect one-star reviews for a call you never wanted. Handle emergencies in the description copy and in a dedicated on-page CTA instead.

### 1c. Descriptions

**Short (≤ 150 characters — Yell, Scoot, Facebook, Apple):**

> Gas Safe registered plumbing and heating engineers serving Wirral, Liverpool and Chester. Boiler installation, repairs and commercial fit-outs.

**Medium (≈ 250 characters — GBP "from the business", Bing):**

> R.J. Sayle Plumbing & Heating Ltd is a Gas Safe registered, fully insured plumbing and heating company based on the Wirral. We install and repair boilers, unvented cylinders and heating systems for homes, landlords and commercial sites across Merseyside and Cheshire.

**Long (≈ 750 characters — Checkatrade, Which?, LinkedIn, Facebook About, Chamber directory):**

> R.J. Sayle Plumbing & Heating Ltd is a Gas Safe registered, fully insured plumbing and heating company operating across the Wirral peninsula, Liverpool, Chester and wider Merseyside, with nationwide coverage for commercial contracts.
>
> With more than 20 years in the trade and over 500 completed projects, we deliver boiler installation and repair, G3-certified unvented cylinder work, radiator installation, power flushing, boosted cold water storage, above-ground drainage and air source heat pump installation.
>
> Our commercial division handles full plumbing and heating fit-outs and shopfitting projects. For landlords we provide CP12 gas safety certificates and planned maintenance. Emergency plumbing call-outs available.
>
> Registered in England and Wales. Gas Safe registration and insurance details available on request.

Use these verbatim. Do not "spin" them per directory — that was 2013 advice, and duplicate directory descriptions have never triggered a penalty.

### 1d. ⚠️ Decisions the client must confirm before anything is published

| # | Decision | Why it blocks work | Suggested default |
|---|---|---|---|
| 1 | **Companies House registered number** | Required by Which? Trusted Traders, TrustMark, Chamber membership, and belongs in the site footer and `LocalBusiness` schema. It is a top-tier trust signal and currently absent. | Obtain from the incorporation certificate. |
| 2 | **Gas Safe registration number** | Should be displayed on the site, in the footer and on every listing that has a credentials field. Its absence is conspicuous for a Gas Safe business. | Obtain and publish. |
| 3 | **Publish an address, yes or no** | Determines GBP setup and how ~40 directory forms are completed. Cannot be changed cheaply later. | Real address, hidden on GBP, entered consistently where mandatory. |
| 4 | **Which email** | Two are in circulation; one is undeliverable. | `info@rjsayleplumbing-heating.com`. |
| 5 | **Keep the mobile, or add a geographic 0151 number** | An 0151 number materially lifts conversion for domestic heating work in Merseyside — some homeowners still distrust a mobile-only trader. But changing the number **after** 40 citations are built creates exactly the NAP mess we're fixing. Decide now, once. | Either is defensible. If switching, buy the 0151 VoIP number, port-forward to the mobile, and use it from day one of citation building. Never run both publicly. |
| 6 | **Confirm hours including Saturday** | Two conflicting sets are live. | Mon–Fri 07:30–18:00, Sat 08:00–13:00. |
| 7 | **VAT registration status/number** | Required for commercial tenders and some directories. | Confirm. |
| 8 | **Public liability cover level & insurer** | Which? and TrustMark demand evidence; "fully insured" alone is a weak claim. | Confirm £2m or £5m. |
| 9 | **Substantiate "20+ years" and "500+ projects"** | These appear in copy that will be republished across dozens of third-party sites. If challenged (ASA, a competitor complaint, a Which? assessor) they need to hold up. | Confirm and keep evidence. |
| 10 | **Does the client own `rjsayleplumbing.co.uk`?** | It does not resolve. If unregistered, it can be sniped by a competitor. | Check registration; see §2. |

---

## 2. NAP consistency risks already present, and the fix

### Risk register

| # | Risk | Severity | Evidence | Fix |
|---|---|---|---|---|
| 1 | **Undeliverable email published in the footer of four pages** | Critical | `mailto:info@rjsayleplumbing.co.uk` on `/areas/index.html`, `/liverpool.html`, `/ellesmere-port.html`, `/nationwide.html`. Domain has no DNS, therefore no MX. | Replace with `info@rjsayleplumbing-heating.com`. Same day. |
| 2 | **Two conflicting business entities in structured data** | Critical | Name, URL, email, hours and review count all differ between the four area pages and the rest of the site. | Delete the second schema block; deploy one shared block with a single `@id`. |
| 3 | **Every canonical points at a redirecting hostname** | High | Canonical, `og:url`, sitemap and JSON-LD all say `www.`; the server 301s `www.` → apex. | Global find/replace `https://www.rjsayleplumbing-heating.com` → `https://rjsayleplumbing-heating.com`. Regenerate sitemap. Resubmit in GSC. |
| 4 | **Self-serving review + aggregateRating markup** | High | `aggregateRating` (5.0/27 and 5/15) plus an on-page `review` object. Google does not permit self-serving reviews on `LocalBusiness` and this is a live manual-action risk. | Remove `review` and `aggregateRating` entirely. Let real GBP reviews carry the stars. |
| 5 | **`reviewCount` contradicts itself** | Medium | 27 on the homepage, 15 on area pages. | Resolved by fix 4. |
| 6 | **Two conflicting opening-hours sets** | Medium | 07:30–18:00 no-Saturday vs 08:00–18:00 plus Saturday. | Single set, per §1b. |
| 7 | **Name variant `RJ Sayle Plumbing` in `alternateName` and area schema** | Medium | Homepage `alternateName`, four area pages `name`. | Standardise. Drop `alternateName` or set it to `R.J. Sayle Plumbing & Heating`. |
| 8 | **`sameAs: []` empty** | Medium | Homepage schema. | Populate as social profiles go live (§7). |
| 9 | **Placeholder `john@example.com` in the contact form** | Low | `/contact.html` input placeholder. | Change to `you@example.com` or a name-neutral string. |
| 10 | **No company number, no Gas Safe number anywhere on site** | Medium | Absent from footer and schema. | Add both to the footer and to schema (`identifier` / `hasCredential`). |

### The `rjsayleplumbing.co.uk` decision — final call

**Retire it. Purge every reference. Then, if and only if the client already owns it, register/renew it defensively and park it on a 301 to the apex. Do not build anything on it, ever.**

Reasoning, in order:

- **It does not resolve.** No A record, no MX. A 301 requires DNS and hosting. Right now there is nothing to redirect *from*. Any advice to "just redirect it" is unactionable until someone confirms who holds the registration.
- **It has no equity to preserve.** No indexed pages, no inbound links, no citations, no traffic. The entire argument for keeping a legacy domain — accumulated authority — is absent. There is nothing to salvage.
- **Two domains for one Wirral sole-operator business is strictly negative.** It splits nothing useful and doubles the entity-resolution work Google has to do. Google is already receiving two `url` values, two names and two emails for what is one business. That is precisely the ambiguity that keeps a local pack ranking soft.
- **The `.co.uk` versus `.com` question is a red herring here.** A `.co.uk` does carry a marginal geo-trust advantage for UK domestic search, and if this were a greenfield build I would pick `.co.uk`. But the `.com` is the one that is live, indexed, linked from your Google Business Profile, and about to receive 40 citations. Migrating to the `.co.uk` now would mean redirecting a live site, rebuilding every citation, and re-earning trust — an expensive move to chase a rounding error. The cost of the switch exceeds the benefit by an order of magnitude.
- **Do register it defensively if it is genuinely free.** £8–15/year. An unregistered near-exact-match of your brand is an open invitation for a lead-gen affiliate or a competitor to grab it and rank on your brand name. Register, park, 301 to the apex, and forget it. Do not put a site on it.

**Action:** developer purges all four `rjsayleplumbing.co.uk` references today. Client checks registration status at the registrar this week. Then it never appears in a citation, a schema block, an email signature, a van livery, a business card or an invoice again.

### Apex vs www — final call

**Apex (`https://rjsayleplumbing-heating.com/`), no `www`.** That is what GitHub Pages serves with a 200; `www` is the redirect. Reversing that on GitHub Pages is possible but pointless. Update every canonical, `og:url`, sitemap entry and schema `url`/`@id` to the apex, and use the apex in every single citation. A citation pointing at `www.` still works via the 301, but you want zero redirect hops in your off-site link profile — some directories strip or nofollow redirecting URLs, and a few validators flag them.

---

## 3. Tier 1 citations — non-negotiable

Complete this entire tier before touching Tier 2. Total cash cost: **£0**. Total effort: roughly 8–12 hours plus verification waits.

| Site | URL | Cost | Link | Effort | Priority | Notes |
|---|---|---|---|---|---|---|
| **Google Business Profile** | business.google.com | Free | Dofollow (website field) | 2h + postcard/video verification | **P0 — prerequisite** | Not optional and not "beyond Google". Everything else in this document is scaffolding around GBP. Set as SAB with hidden address. Video verification is now the common path for SABs — record van, branded clothing, tools, and the property exterior in one unbroken take. Add all services, products, and 20+ geotag-free photos. |
| **Gas Safe Register — Find an Engineer** | gassaferegister.co.uk | Free (included in registration) | Trust citation; treat link as uncertain | 30 min | **P0** | The highest-trust citation a UK gas business can hold, and it is already half-built — the business is registered, so the record exists. The job is making it *correct and complete*. Log into the business account and verify trading title, address, contact number and the full services list (the public panel exposes a "View Services" breakdown — populate every qualification: natural gas, unvented, LPG if held). Capita's contract to run the Register was renewed in 2025 and runs to December 2029, so this is a stable asset. Confirm in-account whether a website field is available; do not assume a dofollow link. |
| **Companies House** | find-and-update.company-information.service.gov.uk | Free (statutory) | No website field | 30 min | **P0** | There is no URL field, so this is not a link — it is entity verification. Google, Bing and every trust-assessing directory cross-reference it. What matters is that the **registered name and registered office exactly match** what you publish elsewhere, that filings are current, and that the SIC code is right (`43220` — plumbing, heat and air-conditioning installation). A dormant-looking or overdue-filing record undermines Which?/TrustMark applications. |
| **Bing Places for Business** | bing.com/forbusiness | Free | Dofollow | 45 min | **P1** | Relaunched October 2025 with a new interface at a new URL, improved Google import (preserves name, hours, attributes), a listing-health recommendation tool, and automatic migration of legacy accounts. Now materially more important than it was: it is the local data layer behind Copilot. Import from GBP, then hand-check every field. |
| **Apple Business** (formerly Apple Business Connect) | businessconnect.apple.com | Free | Dofollow | 45 min | **P1** | Rebranded and consolidated into the unified **Apple Business** platform on 14 April 2026, merging Business Connect, Business Manager and Business Essentials. Same registration flow. Roughly 25–30% of UK mobile map queries never touch Google. Supports service-area configuration. Add the Showcase cards. |
| **Facebook Page** | facebook.com | Free | Nofollow | 1h | **P1** | Dual-purpose: a Tier 1 citation *and* a genuine acquisition channel on the Wirral, where local buy/sell and community groups drive real trade referrals. Complete every NAP field, set the service area, enable Recommendations. |
| **LinkedIn Company Page** | linkedin.com/company | Free | Nofollow | 45 min | **P1** | The commercial fit-out and shopfitting side of the business is the justification. Facilities managers and shopfitting principal contractors check LinkedIn before awarding subcontracts; they do not check Checkatrade. Also a strong, permanent brand citation. |
| **Nextdoor Business Page** | business.nextdoor.com/en-gb | Free | Nofollow | 30 min | **P1** | Free UK business pages with Recommendations. Wirral has dense, active Nextdoor neighbourhoods. Word-of-mouth for trades converts better here than on any paid directory, and the listing itself is a clean citation. |
| **Yell.com** | yell.com/free-listing | **Free listing still available** | Nofollow | 30 min | **P1** | Take the free listing and nothing else. It remains the highest-authority UK trade directory and Google still uses it as a corroborating NAP source. **Decline every sales call.** Yell's paid packages run £30–£100+/month on 12-month rolling terms, plus £200+/month for managed PPC — money far better spent on your own Google Ads. |
| **Trustpilot** | trustpilot.com | Free plan | Nofollow | 30 min | **P1** | Claim the free profile: it is a citation, it ranks for "[brand] reviews", and it pre-empts anyone else claiming it. Stay on free. Paid plans start around £200/month — indefensible for a Wirral plumber. |
| **Thomson Local** | thomsonlocal.com | Free listing | Nofollow | 20 min | **P2** | Still live and still trading in 2026 despite the print decline. Low traffic, but it is a long-standing aggregator source. Twenty minutes, once. |
| **Scoot** | scoot.co.uk | Free listing | Nofollow | 20 min | **P2** | Still live and accepting new business submissions via "Add My Business". Historically a UK data-syndication node. Low direct value, cheap consistency signal. |
| **Yelp UK** | biz.yelp.co.uk | Free | Nofollow | 30 min | **P2** | Weak in the UK compared with the US, and Yelp's review-filter is notoriously aggressive — expect solicited reviews to be suppressed. Claim it anyway: it is a high-DA citation and it feeds Apple Maps' data ecosystem. Do not solicit reviews there. |
| **FreeIndex** | freeindex.co.uk | Free (paid upgrade optional) | Nofollow on free tier | 30 min | **P2** | Genuinely still ranks for long-tail "[trade] in [town]" queries in the UK. Free tier is fine; skip the paid upgrade. |
| **BT / thephonebook.bt.com** | thephonebook.bt.com | Free | Nofollow | 20 min | **P2** | Legacy aggregator, feeds 118-type services. Cheap. |
| **118 Information** | 118information.co.uk | Free | Nofollow | 20 min | **P2** | Same rationale. |
| **Cylex UK** | cylex-uk.co.uk | Free | Dofollow | 20 min | **P2** | One of the few genuinely dofollow free UK directories left. |
| **Central Index** | centralindex.com | Free | Nofollow | 20 min | **P3** | Data-syndication node; propagates NAP to smaller directories. Low effort, low value, do it once. |
| **Foursquare / Places** | foursquare.com | Free | Nofollow | 20 min | **P3** | Absorbed the old Factual dataset. Still feeds a surprising number of third-party maps and apps. |
| **Hotfrog UK** | hotfrog.co.uk | Free | Nofollow | 15 min | **P3** | Marginal. Do it only when P0–P2 are complete. |

**Skip entirely:** every "submit to 500 directories for £49" service; Brownbook, Tupalo, Yasabe, Where's My Business and the rest of the scraped-directory long tail; any directory that wants payment for a basic listing; anything you have never heard of that appeared in a "Top 200 UK citation sites" blog post. Twenty accurate, high-authority citations outrank two hundred sloppy ones, and the long tail is where NAP inconsistency breeds.

---

## 4. Tier 2 — trade and vertical directories

This is where UK tradespeople lose the most money. The business model of most of these platforms is **selling the same homeowner enquiry to three to five competitors simultaneously**, so your true cost per acquired job is the lead price divided by your win rate. A £20 lead with a 25% win rate is an £80 customer acquisition cost — before you have done any work.

Read the verdict column first.

| Platform | Model & real 2026 cost | Lead-sharing reality | Contract | Verdict |
|---|---|---|---|---|
| **Which? Trusted Traders** | £248 non-refundable assessment, then £66/month (0–3 staff) or £797/year. Six-step process, ~30 working days, including a ~90-minute assessment by a trading standards professional, DBS, credit and financial checks, plus document evidence within 48 hours. | **No shared leads.** Customers contact you directly. | Monthly or annual | **JOIN.** The single best-value paid membership for a business selling £3k–£5k boiler installs and commercial fit-outs. The Which? brand carries more weight with the exact demographic that buys a full system replacement than every other directory combined, and the badge lifts on-site conversion irrespective of directory traffic. The assessment is also a free business-process audit. Budget £1,045 in year one. Trade-body members (e.g. CIPHE, HETAS) get a discount — check eligibility before applying. |
| **MyBuilder** | Pay-per-shortlist only. No subscription. From ~£7 per shortlist; typically £5–£35. Bathrooms £50+, extensions £100+. | Multiple trades shortlisted, but **you choose which leads to pay for**, after seeing the job. | **None.** No minimum commitment. | **MAYBE — the only lead site with an honest structure.** Zero downside risk: no contract, no subscription, you pay only when you decide a specific job is worth bidding on. Use it tactically to fill genuine gaps in the diary, never as a primary channel. Set a hard monthly cap of £100 and measure won-job value against it. |
| **Checkatrade** | £30/month published "Approved" tier; "from £59/month" for lead-generating Growth plans. Members widely report **£80–£500/month** all-in. | 3–4 trades per lead. | **12-month fixed term.** | **AVOID in year one.** The published price is not the price anyone pays. At £100–£300/month you are spending £1,200–£3,600/year on a 12-month non-exit contract for shared leads, on top of an untested GBP. And the reviews are rented — stop paying and years of accumulated review history disappears from public view, whereas Google reviews are free and permanent. Revisit only after 12 months if GBP plus Google Ads is genuinely saturated in the Wirral. Brand recognition is its one real argument; it is not worth £3,000. |
| **TrustATrader** | No published pricing — callback form only. Reported £600–£1,000+/year, billed annually in advance, non-refundable. | Not shared; membership capped by area. | 12 months, annual prepay | **MAYBE, lower priority than Which?.** The area cap and non-shared leads are genuinely better than Checkatrade's model, and it is cheaper. But brand recognition in Merseyside is materially below Checkatrade and Which?, and paying a non-refundable year in advance to an unpublished price is a poor opening position. If budget stretches to only one paid membership, it is Which?. |
| **Rated People** | No published pricing. Reported £30–£60/month + VAT, **plus** £15–£40 per lead. "Unlimited" plan reported at ~£72/month. | Up to 3 tradespeople per lead. | 12 months reported | **AVOID.** Subscription *and* per-lead charges *and* shared leads *and* a 12-month term. You pay to be allowed to pay for leads you then have to fight two competitors for. There is no configuration of this business model that favours you. |
| **Bark.com** | Credit-based. £1.80/credit. Typical lead 5–20+ credits = £9–£36+. **Credits expire after 3 months.** | Sold to **up to 5** professionals. | None, but expiring credits create pressure to spend | **AVOID — worst of the category.** Five-way lead resale means an ~20% baseline win rate, putting real CPA at £45–£180 for jobs that are frequently price-shoppers or tyre-kickers. Expiring credits are a deliberate spend-forcing mechanism. Skip. |
| **Boiler Guide** | Commission/lead-resale model; installer network, boiler-replacement enquiries sold onward. | Shared, typically 3–4 installers per enquiry. | Varies | **AVOID unless you have idle capacity.** Vertical relevance is high — these are people actively buying a boiler — but it is still a shared-lead auction, and boiler-replacement enquiries are the most aggressively price-compared jobs in the trade. If capacity is genuinely idle in January, test with a hard budget cap; otherwise skip. |
| **HomeHow** | Free listing | Negligible traffic | None | **SKIP** — or spend 10 minutes on a free listing purely as a citation and never think about it again. Do not pay for anything here. |
| **TrustMark** | Registration is via an approved **Scheme Provider** (NICEIC, NAPIT, etc.), not directly with TrustMark. Cost is bundled into the scheme provider's fee. | N/A — it is a quality framework, not a lead source. | Annual via scheme provider | **JOIN ONLY IF pursuing grant-funded work.** TrustMark is a compliance gate, not a marketing channel: it is mandatory for ECO4, the Great British Insulation Scheme and much retrofit work, and it pairs with MCS for heat pump grant eligibility. If air source heat pumps and the Boiler Upgrade Scheme are a genuine strategic direction (§5), TrustMark plus MCS is the required package. If not, skip — its SEO value alone does not justify the cost or the audit burden. |
| **Houzz Pro** | £139/month software + £119+/month advertising | Placement bought | Annual | **SKIP.** Wrong audience entirely. Houzz is design-led renovation; you sell boiler swaps and commercial fit-outs. |
| **Local Heroes (British Gas)** | — | — | — | **DEAD — do not pursue.** The platform closed. `localheroes.com` now 302-redirects to `britishgas.co.uk/local-heroes.html`. Anyone still recommending it is working from a stale list. |
| **Local council Trading Standards "Buy With Confidence"** | Typically £100–£300/year where operated | Not a lead source | Annual | **CHECK LOCALLY, then join if available.** Buy With Confidence is a national scheme delivered by *participating* Trading Standards services, and coverage is patchy — I could not confirm Wirral/Merseyside participation from the national site. Ring Wirral Council Trading Standards directly. If they run a scheme, it is a `.gov.uk` citation with a genuine dofollow link and real local trust weight for a fraction of Checkatrade's price. Best-value item in this table if it exists locally. |

**Total recommended Tier 2 spend, year one: £1,045** (Which? Trusted Traders) **plus up to £100/month capped, discretionary on MyBuilder.** Everything else is either free or a trap.

---

## 5. Manufacturer and accreditation schemes

Be clear-eyed about what these are worth. The installer-finder backlinks are typically **nofollow or JavaScript-rendered**, so direct link equity is near zero. Their actual value is threefold, in descending order of importance:

1. **Conversion rate.** "Worcester Bosch Accredited Installer, 10-year guarantee" on a quotation beats an unbadged competitor at the same price. This is worth more than every backlink in this document combined.
2. **High-intent referral traffic.** A homeowner using a manufacturer's "find an installer" tool has already chosen the boiler and is looking for someone to fit it. That is the warmest lead in the trade, and it is free.
3. **Brand-entity corroboration.** Being named on `worcester-bosch.co.uk` or `idealheating.com` is a strong, permanent, high-authority brand mention — valuable to entity understanding even when nofollowed.

The common requirement across all of them: **attend the manufacturer's product training** (usually free or heavily subsidised, typically 1 day at a regional training centre, plus travel and a lost day's earnings — call it £250–£400 in opportunity cost each), then **register installations** through the manufacturer's portal to maintain status. Note the honest caveat: accreditation certifies that you attended training, not that you are a better engineer. Customers do not know that, which is precisely why it converts.

### Priority order

| # | Scheme | Requirement | Cost | Warranty benefit | Verdict |
|---|---|---|---|---|---|
| **1** | **Worcester Bosch Accredited Installer** | Mandatory product training; Gas Safe registration; register installations | Free scheme; ~1 training day | **Up to 10 years**, serviceable by any Gas Safe engineer | **Do first.** Worcester is the dominant domestic brand in the North West and the one homeowners ask for by name. The accredited badge plus a 10-year guarantee is the strongest single conversion lever available to this business. Installer-finder listing included. |
| **2** | **Vaillant Advance** | Mandatory product training; register installations | Free scheme; ~1 training day | **Up to 10 years**, serviceable by any Gas Safe engineer | **Do second.** The clear number two by brand recognition. Covering both Worcester and Vaillant means you can badge-match whatever the customer has already researched. |
| **3** | **Ideal Heating Max Accredited Installer** | Free online assessment, then invitation to apply via the Connect account. Maintain: register **at least one Ideal boiler every 60 days**, and earn **60 Max points within 6 months** (Vogue Max/Logic Max with filter = 10 points; Logic+ = 5; 5-year-warranty models = 2; Halo controls = 1) | **Free** | **Free 12-year extended warranty on the Vogue Max range** | **Do third — cheapest win available.** No fee, and it includes a **free priority listing on the homeowner "Find Your Local Installer" tool**, which Ideal reports generates around 2,000 leads per month across the network. The 60-day registration cadence is the real commitment: only join if you will realistically fit Ideal boilers regularly, or you will lapse and lose the listing. |
| **4** | **Baxi Approved Installer / Baxi Works** | Product training; loyalty points via Baxi Works | Free | 10 years — but **note this is available without accreditation** | **Optional.** The warranty differentiator is weak because customers get 10 years anyway. Join for the Baxi Works loyalty rewards and the installer-finder listing, not for the badge's persuasive power. Low priority. |
| **5** | **Viessmann Trained Installer** | Product training | Free | Up to 10 years | **Optional / later.** Small Wirral market share, but a premium product with better margins and a customer profile that buys on quality rather than price. Worth it only if you actively want to move up-market. |
| **6** | **Glow-worm Club Energy** | Product training (Vaillant Group scheme) | Free | **Up to 15 years — but conditional on annual servicing by Vaillant Group** | **Approach with caution.** The 15-year headline is the longest available and sells well, but the servicing condition hands your customer's annual maintenance revenue to the manufacturer for fifteen years. You would be trading recurring service income for a one-off closing advantage on a budget-brand boiler. Join only if you genuinely target the price-led end of the market and do not want the service book. |
| **7** | **MCS (heat pumps)** | Level 3 competency, a certification body (Amtivo, Certsure/NICEIC, NAPIT, Simply Certification, The IAA), surveillance assessments; **usually paired with TrustMark** | **Initial certification £500–£1,500;** annual packages ~**£800–£1,200**; **£30 per installation registered**; **new for 2026: a mandatory financial protection product on every installation** (6 years' cover, £250 consumer excess), priced per job. Consumer code membership is **no longer mandatory** under the redeveloped scheme. The MCS Certification Fund covers 75% up to £1,000 — **but for heat pumps it is Scottish SMEs only**, so not available here. | N/A | **Strategic decision, not an SEO decision.** MCS is a genuine business-line investment of roughly £1,500–£2,500 in year one plus per-install costs. The commercial case is not the backlink — it is that **MCS certification is the gateway to the Boiler Upgrade Scheme grant**, and without it you cannot quote for grant-funded ASHP work at all. Given the site already markets air source heat pumps, this is currently a credibility gap: you are advertising a service you cannot deliver on the terms most customers will want. **Either commit to MCS in the next 6–12 months, or soften the heat pump messaging on the site.** Do not leave it as it stands. |

**Sequencing:** Worcester and Vaillant training in the first 60 days (they are free, they take a day each, and they raise close rates immediately). Ideal Max as a same-week free online application. Everything else deferred to a Q4 review. MCS is a separate business-planning conversation with a real budget line.

---

## 6. Local link acquisition — 15 tactics for a Wirral tradesman

Ranked by realistic return per hour invested. "Link value" assumes a local business with no existing link profile, where a genuine `.gov.uk`, `.ac.uk`, `.org.uk` or local-news link is worth many times a directory listing.

| # | Tactic | Target type | Effort | Link value | How to actually get it |
|---|---|---|---|---|---|
| **1** | **Wirral Chamber of Commerce membership** | wirralchamber.co.uk | Low (1h + payment) | **High** — member directory listing, established local authority domain, plus event and news mention opportunities | **Membership Premium is £50 + VAT/month; Business Partner is £125 + VAT/month.** Both include a Members Directory listing. Take Premium. The £600+VAT/year buys a durable local link, B2B introductions relevant to the commercial fit-out line, and credibility on tender documents. Best single paid local link available. |
| **2** | **Local council Trading Standards approved-trader scheme** | Wirral Council / Merseyside Trading Standards | Low–Medium | **Very high** — `.gov.uk` domain | Phone Wirral Council Trading Standards directly and ask whether they operate an approved-trader or Buy With Confidence scheme. Coverage is inconsistent nationally. If it exists, apply immediately — a `.gov.uk` local link with a trust badge is unmatched at any price. |
| **3** | **Grassroots football / sports club shirt sponsorship** | Wirral junior football leagues, Sunday league sides, Tranmere Rovers community partner tiers, local cricket and rugby clubs | Low (£250–£750) | **Medium–High** — sponsor page link, plus genuine word-of-mouth among parents | Approach club secretaries directly in July–August (pre-season is when kit budgets are set). Ask explicitly for a logo **and a linked business name** on the sponsors page — most clubs default to an unlinked image. A junior team kit at £300–£500 also puts your brand in front of exactly the 35–55 homeowner demographic that buys boilers. Highest emotional-ROI spend in this table. |
| **4** | **Wirral Globe / Liverpool Echo local business coverage** | wirralglobe.co.uk, liverpoolecho.co.uk | Medium | **High** — regional news domain | Do not pitch "local plumber offers services". Pitch a **story**: a free boiler service for a pensioner or a veteran in winter; an apprentice hired locally; sponsoring a school's heating repair; commentary on rising energy bills or the Boiler Upgrade Scheme from a working engineer's perspective. Regional newsdesks run these year-round and need local voices, especially in October–February. Send photos with the pitch — it roughly doubles the acceptance rate. |
| **5** | **Estate and letting agent "trusted contractor" pages** | Wirral independents — Karl Tatler, Jones & Chapman, Clive Watkin, Bakewell & Horner, local letting agents | Medium (ongoing relationship) | **Medium** — plus the best commercial referral channel available | Letting agents need CP12 gas safety certificates on every managed property, every year. That is recurring, predictable revenue and it maps precisely onto your landlord services line. Approach with a rate card for bulk CP12s, then ask to be listed on their contractors/suppliers page. Lead with the commercial offer; the link is the by-product. **Do this even if no agent ever links to you.** |
| **6** | **Local charity partnership** | Wirral Hospice St John's, Age UK Wirral, Wirral Foodbank, Charity Right / local community trusts | Medium | **Medium–High** — `.org.uk` supporters page | Offer trade services in kind (a boiler service for a hospice property, plumbing for a community building) rather than cash. Charities value skilled labour more highly than a £200 cheque, and it makes a better "our supporters" page entry. Ask for a linked listing as part of the arrangement, up front. |
| **7** | **School PTA and community building sponsorship** | Wirral primary/secondary PTAs, scout huts, community centres, church halls | Low–Medium (£100–£300) | **Medium** — school and PTA sites are often `.sch.uk` or `.org.uk` | PTA summer fair programmes, sports day sponsorship, school newsletter advertising. Ask for the sponsor listing on the PTA website, not just the printed programme. Parents talk, and heating work is overwhelmingly referral-driven in this demographic. |
| **8** | **Merchant and supplier "where to buy / find an installer" pages** | Plumbing merchants (City Plumbing, Wolseley, Plumbase branches), plus manufacturer installer-finders per §5 | Low | **Medium** | Ask your branch manager whether the merchant runs a local recommended-installer listing — several do at branch or regional level. Free, and you are already a customer. Combine with the manufacturer installer-finder listings from §5. |
| **9** | **Community Facebook groups** | "Wirral Community", town-specific buy/sell/recommend groups, "Recommendations Wirral" | Low, ongoing | **Low SEO / Very high commercial** | No dofollow value whatsoever — but for a Wirral tradesman these groups are, bluntly, likely to out-earn every link in this table in year one. Join as the business page owner, read the rules, never spam. Answer heating questions helpfully without pitching. Ask genuinely satisfied customers to tag you when someone asks for a recommendation. This is a referral engine, filed here because it is where the time should go. |
| **10** | **Local business awards** | Wirral Business Awards, Liverpool City Region awards, Chamber awards, trade press awards | Medium (application writing) | **Medium–High** — nominee/finalist listings are linked and get press pickup | Entering is usually free or cheap. A finalist listing generates a link from the awards site, a likely Wirral Globe mention, and a badge for the website and quotations. Even a nomination is usable in marketing. Deadlines cluster in spring — diarise now. |
| **11** | **Supplier and partner reciprocal case studies** | Bathroom showrooms, kitchen fitters, electricians, builders, shopfitting contractors | Medium | **Medium** | You already work alongside these trades on fit-outs. Offer a written case study or testimonial for their site in exchange for one on yours, each with a link. Genuinely reciprocal, genuinely relevant, entirely legitimate. Target 4–6 in the first year. |
| **12** | **Commercial client case studies with client sign-off** | Shopfitting clients, commercial fit-out clients, letting agencies | Medium | **Medium** | Ask commercial clients for permission to publish a project case study naming them, and ask them to link from their own "our suppliers"/"about the fit-out" page. Business-to-business clients agree to this far more often than expected, because it is free publicity for them too. |
| **13** | **Local college / training provider partnerships** | Wirral Met College, Liverpool training providers, apprenticeship schemes | Medium–High | **High** — `.ac.uk` | Offer an apprenticeship placement or a guest talk to plumbing students. Employer-partner pages on college sites carry serious authority and almost no competitor will have one. Slow to land, disproportionate payoff. |
| **14** | **Local blog and community site sponsorship** | Wirral community news sites, "things to do in Wirral" blogs, local podcasts | Low–Medium | **Low–Medium** | Small, cheap, and easy to over-invest in. Cap at two or three, choose ones with genuine local readership, and avoid anything that reads as a link farm. |
| **15** | **Trade association membership** | CIPHE, APHC, HETAS (if solid fuel), Federation of Master Builders | Low–Medium (£100–£400/yr) | **Medium** — member directory link plus credential | CIPHE membership carries the additional benefit of a **discount on Which? Trusted Traders** fees, which partly offsets §4. Also strengthens commercial tender submissions. Check which body's discount stacks best against your Which? application before joining either. |

**What to skip:** paid guest posts on generic "home improvement" blogs; link exchanges with plumbers in other cities (irrelevant and pattern-obvious); any agency selling "50 UK local links"; blog comment links; sponsored posts on sites with no genuine Wirral readership. A Wirral plumber needs perhaps 15–25 genuinely local links, not 200 generic ones.

---

## 7. Social profiles

The business currently has zero, and `sameAs` is empty. Fix the sequence, not the volume.

### Build order

| Order | Platform | Type | Why |
|---|---|---|---|
| 1 | **Facebook Page** | **Real channel** | Non-negotiable. The primary social platform for the Wirral homeowner demographic, the gateway to the community groups in §6, and a Tier 1 citation. Enable Recommendations. |
| 2 | **LinkedIn Company Page** (+ optimise the owner's personal profile) | **Real channel for commercial only** | The commercial fit-out and shopfitting line lives or dies on B2B credibility. The personal profile matters more than the company page — post from it, link the company page to it. |
| 3 | **Instagram Business** (linked to the Facebook Page) | **Real channel** | Plumbing and heating is visually strong: pipework, new installs, before/after. Cross-posts from Facebook at near-zero marginal effort. Strong for the higher-value bathroom and unvented cylinder work. |
| 4 | **Nextdoor Business Page** | Hybrid — citation + genuine local referral | Free, hyper-local, high trust. Low maintenance. |
| 5 | **YouTube** | **Citation play** | Create the channel, upload 3–5 short project or explainer videos ("what a power flush actually does", "why your boiler is losing pressure"), and leave it. It is a high-authority `sameAs` entry and a place to host video embeds for the website. Do not attempt a content schedule. |
| 6 | **TikTok** | Optional real channel | Only if the owner or a family member will genuinely make short videos. Trades content performs extremely well there. If nobody will do it consistently, skip entirely — a dead TikTok is worse than none. |

**Do not create:** X/Twitter (no meaningful UK trade audience, and a dormant account looks worse than absence), Pinterest (wrong vertical for boiler work), Threads, Bluesky, Snapchat. If you want the `sameAs` breadth, YouTube already provides it at lower cost.

### Minimum viable cadence

Realistic for a working engineer, not an agency fantasy:

- **Facebook:** 2 posts/week. One job photo with a one-line caption, one useful tip or seasonal reminder. 15 minutes total.
- **Instagram:** cross-post the same 2, plus 2–3 Stories/week shot on the phone at a job. 10 minutes.
- **LinkedIn:** 1 post/week, commercial focus — fit-out progress, a completed contract, a trade observation. 10 minutes.
- **Nextdoor:** 1 post/month plus replies to any relevant neighbourhood thread. 10 minutes.
- **YouTube:** 1 video/quarter. Optional.
- **Google Business Profile posts:** 1/week — the highest-value 5 minutes on this list, because GBP posts actually influence local pack behaviour. Treat GBP as your most important social channel.

**Total: under 60 minutes a week.** Below that, do not bother; above it without a plan, it will lapse by week six.

**Seasonal rule:** heavy up in September–November (pre-winter boiler service and replacement demand) and in any cold snap. That is when Wirral homeowners actually search and post.

### `sameAs` array — populate as profiles go live

```json
"sameAs": [
  "https://www.facebook.com/<page>",
  "https://www.instagram.com/<handle>",
  "https://www.linkedin.com/company/<slug>",
  "https://nextdoor.co.uk/pages/<slug>",
  "https://www.youtube.com/@<handle>",
  "https://uk.trustpilot.com/review/rjsayleplumbing-heating.com",
  "https://www.yell.com/biz/<slug>",
  "https://find-and-update.company-information.service.gov.uk/company/<number>"
]
```

Include the Companies House URL — it is one of the strongest entity-verification signals available and virtually no competitor uses it.

---

## 8. Review platform strategy beyond Google

**Reality check first:** for a Wirral plumber, Google reviews are worth more than every other review platform combined, by a wide margin. The correct strategy is to concentrate almost all effort there and treat everything else as insurance and citation value. Two further principles:

- **Reviews you rent disappear.** Checkatrade, TrustATrader and similar remove your review history from public view when you stop paying. Google reviews are free and permanent. Never let a review-collection habit become dependent on a subscription.
- **Never gate or incentivise.** No "leave us a review and get £10 off". It breaches Google's policy and, for a Which? Trusted Trader, would fail assessment.

| Platform | Verdict | Rationale |
|---|---|---|
| **Google Business Profile** | **Primary. 90% of effort.** | Target 3–5 new reviews/month, sustained. Ask in person at job completion, then follow up the same day with a text containing the short review link. The same-day text is the single highest-yield tactic in review generation. Reply to every review within 48 hours, positive and negative. |
| **Facebook Recommendations** | **Secondary — worth real effort.** | Trivial for a customer who is already on Facebook, visible to their network, and directly feeds the community-group referral loop in §6. Best second platform for this business. |
| **Trustpilot (free plan)** | **Tertiary — claim it, seed 5–10 reviews, then leave it.** | Ranks for "[brand] reviews" and pre-empts a hostile claim. Do not pay for the plan; paid tiers start around £200/month, which is indefensible here. |
| **Which? Trusted Traders** | **Worth effort once joined.** | Reviews are verified and carry unusual weight with high-value customers. Since you are paying £1,045 in year one, actively feed it. |
| **Nextdoor Recommendations** | **Worth light effort.** | Hyper-local and high trust; a handful of recommendations in the right neighbourhoods punches above its weight. |
| **Manufacturer schemes** (Worcester, Ideal, Vaillant) | Feed where the scheme offers a review facility | Reinforces the installer-finder listing ranking and the accreditation badge. |
| **Yelp UK** | **Claim, then ignore.** | Yelp's filter aggressively suppresses solicited reviews, so effort is wasted and soliciting risks a "we don't ask for reviews" consumer alert. Keep it as a citation only. |
| **Checkatrade / TrustATrader / Rated People / Bark** | **Wasted effort unless already paying.** | Rented reviews on platforms you should not be paying for in the first place. |
| **Trustist, Reviews.io, Feefo** | **Skip.** | Aggregator products aimed at e-commerce. No relevance to a Wirral heating business. |
| **Yell reviews** | **Skip.** | Almost no UK consumer reads Yell reviews in 2026. |

**Process to embed:** a laminated card in the van with the Google short-link QR code; an SMS template saved on the phone; a diary reminder to send the request the same evening as the job. Review velocity is a ranking factor — steady beats bursty. Twenty reviews arriving in one week looks manipulated; three a month for a year looks like a healthy business.

---

## 9. NAP audit and monitoring routine

### Master record
One spreadsheet, one tab per tier, columns: `Platform | Profile URL | Login email | Date created | Date last verified | NAP matches master (Y/N) | Link type | Notes`. Store credentials in a password manager, not the spreadsheet. This document's §1 table is the master record; the spreadsheet tracks compliance against it.

### Cadence

**Weekly (5 minutes)**
- Check GBP for pending "suggested edits" from users and for Google-applied changes. Google silently amends hours, categories and even phone numbers based on third-party signals and user submissions. This is the single most common cause of NAP drift and it is invisible unless you look.
- Check for new reviews across GBP and Facebook; reply.

**Monthly (30 minutes)**
- Search `"R.J. Sayle Plumbing"`, `"RJ Sayle Plumbing"` and `"07450 237593"` in Google and Bing. The phone-number search is the highest-yield check — it surfaces scraped directories that have auto-created listings you never made, which are a leading source of NAP conflict.
- Verify no new instance of `rjsayleplumbing.co.uk` or `info@rjsayleplumbing.co.uk` has reappeared anywhere (including in newly deployed pages — this is exactly the kind of error that recurs from a copied template).
- Check GBP Insights: calls, direction requests, website clicks, search-query breakdown.
- Confirm the site's canonical tags still point at the apex after any deployment.

**Quarterly (2–3 hours)**
- Full audit of every Tier 1 and Tier 2 listing against the master record. Correct any drift.
- Re-run structured data through Google's Rich Results Test and Schema Markup Validator; confirm one entity, one `@id`, no `aggregateRating`.
- Review Search Console: Performance by query and page, plus the Links report for newly acquired backlinks.
- Assess Tier 2 spend against measured job value. Cancel anything not returning.
- Check for duplicate GBP listings (search the business name and the address in Google Maps).

**Annually**
- Renew or cancel paid memberships on a decision, not by default.
- Re-photograph the van and jobs; refresh listing imagery.
- Re-verify the Gas Safe Register record, insurance certificates and Companies House filings.

### Tooling
- **BrightLocal Citation Tracker** — around £29/month. Worth it for the first three months to establish a baseline and find scraped listings, then cancel and maintain manually. Do not pay for it for twelve months.
- **Google Search Console** and **Bing Webmaster Tools** — free, mandatory, set up both.
- **Google Alerts** for `"R.J. Sayle Plumbing"` and `"RJ Sayle Plumbing"` — free, catches unlinked mentions worth converting into links.
- **UTM tagging** on every citation website URL (`?utm_source=yell&utm_medium=citation`) so that GA4 attributes directory traffic. **Important exception: do not UTM-tag the Google Business Profile website field** — it can interfere with attribution and looks untidy in the local pack. Tag the directories only.

---

## 10. 90-day execution schedule and cost

| Week | Workstream | Actions | Owner | Cash cost |
|---|---|---|---|---|
| **1** | **Emergency fixes** | Replace the 4 dead `info@rjsayleplumbing.co.uk` footer links. Delete the second LocalBusiness schema block from `/areas/index`, `/liverpool`, `/ellesmere-port`, `/nationwide`. Remove all `review` and `aggregateRating` markup site-wide. Fix the `john@example.com` placeholder. | Dev | £0 |
| **1** | **Canonical fix** | Global replace `www.rjsayleplumbing-heating.com` → `rjsayleplumbing-heating.com` across canonicals, `og:url`, sitemap and schema. Regenerate and resubmit sitemap. | Dev | £0 |
| **1** | **Client decisions** | Confirm all 10 items in §1d. Nothing else proceeds until items 1–6 are settled. | Client | £0 |
| **1** | **Domain** | Check registration status of `rjsayleplumbing.co.uk`; register/renew defensively and park on a 301 if available. | Client | £10–15 |
| **2** | **NAP master record** | Lock §1 into a shared document. Build the tracking spreadsheet. Set up GSC and Bing Webmaster Tools. | SEO | £0 |
| **2** | **Schema rebuild** | One shared `LocalBusiness` block with a single `@id`, company number, Gas Safe number, agreed hours, correct email, populated `areaServed`. Validate. | Dev | £0 |
| **2–3** | **GBP** | Create/claim, SAB configuration, hidden address, service areas by town, all categories, services, 20+ photos, description, complete verification. | SEO + Client | £0 |
| **3** | **Gas Safe Register** | Log into the business account. Verify trading title, address, phone, full services list. Confirm whether a website field exists. | Client | £0 |
| **3** | **Companies House** | Verify registered name, office address, SIC code `43220`, filings current. Add company number to site footer. | Client | £0 |
| **4** | **Bing Places + Apple Business** | Import from GBP, hand-verify every field. | SEO | £0 |
| **4** | **Facebook + LinkedIn** | Create both, full NAP, long description, imagery. | SEO | £0 |
| **5** | **Instagram + Nextdoor + YouTube** | Create, link Instagram to Facebook, upload 3 videos to YouTube. | SEO | £0 |
| **5** | **`sameAs` populated** | Add all live profile URLs plus Companies House to schema. | Dev | £0 |
| **6** | **Tier 1 free directories, batch 1** | Yell (free listing only), Trustpilot (free), Yelp UK, FreeIndex. | SEO | £0 |
| **6** | **Manufacturer applications** | Apply: Worcester Accredited Installer, Vaillant Advance, Ideal Max (free online assessment). Book training dates. | Client | £0 (~£250–400 opportunity cost per training day) |
| **7** | **Tier 1 free directories, batch 2** | Thomson Local, Scoot, Cylex, BT phonebook, 118 Information, Central Index, Foursquare, Hotfrog. | SEO | £0 |
| **7** | **Review engine** | Van QR cards, SMS template, same-day request process. Target 3–5 GBP reviews/month from here on. | Client | £20 (printing) |
| **8** | **Wirral Chamber** | Join Membership Premium. Complete the directory listing using the canonical NAP and long description. | Client | £50 + VAT/mo |
| **8** | **Trading Standards** | Phone Wirral Council re: approved-trader / Buy With Confidence. Apply if available. | Client | £0–300/yr |
| **9** | **Which? Trusted Traders** | Check CIPHE/trade-body discount eligibility first. Pay assessment, submit documents within 48h, schedule assessment. ~30 working days to endorsement. | Client | £248 + £66/mo |
| **9–10** | **MyBuilder trial (optional)** | Register free. Hard cap £100/month. Track won-job value against spend. | Client | ≤£100/mo |
| **10** | **Estate & letting agents** | Approach 8–10 Wirral independents with a bulk CP12 rate card. Ask for a contractors-page listing. | Client | £0 |
| **11** | **Sponsorship** | Approach 2–3 junior football/sports clubs. Secure a **linked** sponsors-page listing, not just a logo. | Client | £250–750 |
| **11** | **Charity + PTA** | Approach 2 local charities with an in-kind offer; 1–2 PTAs. Request linked supporter listings. | Client | £100–300 |
| **12** | **Press outreach** | Pitch one genuine story to the Wirral Globe and Liverpool Echo. Include photographs. | SEO + Client | £0 |
| **12** | **Reciprocal case studies** | Approach 4–6 allied trades and 2 commercial clients for mutual case studies with links. | Client | £0 |
| **13** | **Audit + baseline** | Full NAP audit of everything built. BrightLocal citation scan. Record GBP Insights baseline. Set the quarterly routine. Review Tier 2 spend and cut anything not performing. | SEO | £29 (1 month) |

### Cost estimate — first 90 days

| Item | Cost |
|---|---|
| Website and schema fixes | £0 (dev time) |
| All Tier 1 citations | **£0** |
| Defensive domain registration | £10–15 |
| Which? Trusted Traders (£248 assessment + 3 months at £66) | **£446** |
| Wirral Chamber (Membership Premium, 3 months at £50 + VAT) | **£180** |
| Sports club sponsorship | £250–750 |
| Charity / PTA sponsorship | £100–300 |
| Review cards and printing | £20 |
| BrightLocal (1 month baseline) | £29 |
| Manufacturer schemes | £0 fees |
| Local Trading Standards scheme (if it exists) | £0–300 |
| MyBuilder trial (optional, capped) | £0–200 |
| **Total 90-day cash** | **£1,035 – £2,240** |
| **Total 90-day labour** | **~45–60 hours** (roughly 35 SEO/admin, 15 client) |

### Ongoing from month 4

| Item | Monthly |
|---|---|
| Which? Trusted Traders | £66 |
| Wirral Chamber | £50 + VAT |
| **Committed monthly** | **~£126 inc. VAT** |
| Discretionary (MyBuilder, capped) | ≤£100 |

**Annualised, roughly £1,500–£2,700.** For context: the Checkatrade-plus-Rated-People path that many Wirral plumbers default into costs £3,000–£6,000 a year on 12-month contracts, buys shared leads, and leaves you owning nothing when you stop paying. Everything in this plan is either free, owned outright, or cancellable.

---

## The blunt summary

1. **Four pages publish an email address that does not exist.** Every enquiry sent to it has been lost. Fix today.
2. **Kill `rjsayleplumbing.co.uk` completely.** It has no DNS, no traffic, no links and no value. Purge the references, register it defensively if it is free, park it, forget it.
3. **All your canonicals point at a redirect.** Move everything to the apex before building a single citation.
4. **Strip the fake review markup.** Self-serving `aggregateRating` on `LocalBusiness` is a manual-action risk with no upside.
5. **Tier 1 is free and takes about ten hours.** There is no excuse for zero citations. Do it in weeks 1–7.
6. **Of the paid trade directories, join Which? and nothing else.** Checkatrade, Rated People, Bark and Boiler Guide are shared-lead auctions where your real CPA is four times the sticker price. Local Heroes is dead. MyBuilder is the only tolerable pay-per-lead option because you choose each lead.
7. **Worcester and Vaillant accreditation are free and will raise your close rate more than any backlink.** Book the training.
8. **You are advertising heat pumps without MCS.** Either commit to certification or soften the claim.
9. **Concentrate reviews on Google.** Everything else is insurance.
10. **Fifteen genuinely local Wirral links beat two hundred generic directory listings**, and a junior football kit sponsorship will out-earn most of this document.

---

### Sources

- [Whitespark — Top UK Local Citation Sources](https://whitespark.ca/top-local-citation-sources-by-country/united-kingdom/)
- [Gas Safe Register — Find an Engineer](https://www.gassaferegister.co.uk/gas-safety/how-to-find-an-engineer-or-check-the-register/)
- [Registered Gas Engineer — Keeping business details up to date](https://registeredgasengineer.co.uk/are-all-your-business-details-up-to-date/)
- [Installer Online — Capita to manage Gas Safe Register until December 2029](https://www.installeronline.co.uk/heating/capita-to-manage-gas-safe-register-until-december-2029/)
- [Which? Trusted Traders — Join (fees and process)](https://for-traders.which.co.uk/join)
- [LocalAdder — UK Trade Lead Cost Tracker](https://localadder.co.uk/uk-trade-lead-cost-tracker/)
- [Whito — UK Trade Directory Costs 2026](https://whito.co.uk/research/uk-trade-directory-costs/)
- [Plumble — British Gas Local Heroes closure](https://plumble.co.uk/british-gas-local-hero-hello-plumble/)
- [British Gas — Local Heroes (redirect target)](https://www.britishgas.co.uk/local-heroes.html)
- [Search Engine Journal — Microsoft launches new Bing Places for Business](https://www.searchenginejournal.com/microsoft-launches-new-bing-places-for-business/557520/)
- [PinMeTo — Apple Business Connect is now Apple Business](https://www.pinmeto.com/blog/apple-business-connect-now-apple-business/)
- [Yell — Free Listing](https://www.yell.com/free-listing/)
- [Thomson Local](https://www.thomsonlocal.com/)
- [Scoot](https://www.scoot.co.uk/)
- [Nextdoor — Create a Free Business Page (UK)](https://business.nextdoor.com/en-gb/getting-started/business-page)
- [Wirral Chamber of Commerce — membership](https://wirralchamber.co.uk/)
- [Ideal Heating — Max Accredited Installer Scheme](https://idealheating.com/support/max-accredited-scheme)
- [The Heating Hub — Gas engineer approved installer schemes](https://www.theheatinghub.co.uk/gas-engineer-approved-installer-scheme)
- [Solarable — MCS certification costs for UK installers 2026](https://solarable.org/guides/mcs-certification-cost-uk-installers)
- [MCS — Umbrella Schemes](https://mcscertified.com/installers/help-resources/umbrella-schemes/)
- [TrustMark — Join TrustMark](https://www.trustmark.org.uk/business/information-guidance/join-trustmark)
- [Buy With Confidence](https://www.buywithconfidence.gov.uk/)
- [Costbench — Trustpilot free plan and paid pricing 2026](https://costbench.com/software/review-management/trustpilot/free-plan/)
agentId: ad34dbef27ed55c8f (use SendMessage with to: 'ad34dbef27ed55c8f', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 99637
tool_uses: 56
duration_ms: 1076576</usage>