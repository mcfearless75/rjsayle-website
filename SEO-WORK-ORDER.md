# SEO / GEO Work Order — R.J. Sayle Plumbing & Heating

**Repo:** `rjsayle-website` (GitHub Pages, static HTML, apex domain `rjsayleplumbing-heating.com`)
**Written:** 14 August 2026 · **Supersedes:** `docs/gmb-optimisation.md`, `APPLY-README.md`
**For:** Claude Code, working in this repo.

---

## 0. Read this first

A full local SEO / GEO / AI-visibility audit was completed on 14 Aug 2026. **Phase 0 fixes are already written and shipped as a patch** — they may or may not be applied to this working copy yet. Check before doing anything (§1).

Three companion documents contain the detailed research behind this work order. Read the relevant one before starting a phase, not before starting the job:

| File | Read before |
|---|---|
| `01-audit-and-fixes.md` | Anything technical. It explains *why* each Phase 0 change was made. |
| `02-content-gap-and-build-out-plan.md` | Phases 2, 3, 4. Contains full page specs, FAQs and local research. |
| `03-citations-and-off-site-plan.md` | Phase 5. Off-site — mostly not a code task. |
| `04-google-business-profile-plan.md` | Not a code task. Owner action. |

**Do not re-audit. Do not re-derive decisions.** The calls below were made deliberately, with reasoning recorded in the companion docs. If you think one is wrong, say so and stop — don't silently do something different.

---

## 1. State of play

### Already fixed (Phase 0 — verify, don't redo)

Run this first:

```bash
grep -rl "cdn.tailwindcss.com" --include=*.html .   # expect: no output
grep -rl "www.rjsayleplumbing"  --include=*.html .   # expect: no output
grep -rl "rjsayleplumbing.co.uk" --include=*.html .  # expect: no output
ls og-image.jpg assets/tailwind.css                  # expect: both exist
```

If any check fails, the patch isn't applied. Apply `rjsayle-seo.patch` (or overlay the zip) before continuing.

What Phase 0 did:

- **Canonical host** — every `canonical`, `og:url`, `sitemap.xml` `<loc>`, JSON-LD `@id`/`url` and `robots.txt` sitemap line moved from `www.` to the apex. `www.` 301-redirects to apex on GitHub Pages, so every canonical previously pointed at a redirect.
- **Dead second domain removed** — `rjsayleplumbing.co.uk` (no DNS, no MX) and `info@rjsayleplumbing.co.uk` appeared in JSON-LD and live footer `mailto:` links on four pages. Enquiries sent there vanished. All replaced with the apex domain and `info@rjsayleplumbing-heating.com`.
- **Structured data rebuilt** — one `@graph` per page, one shared business `@id` sitewide, all nodes cross-linked. Added: `BreadcrumbList` (all pages), 12 `Service` nodes, `ContactPoint`, `ImageGallery`, `Person` for the director, `hasCredential`, `isicV4`, Companies House `identifier`. Four pages had **no schema at all** (`services`, `about`, `contact`, `gallery`) — they do now.
- **Conflicting `aggregateRating` removed** — same `@id` claimed 27 reviews on three pages and 15 on twelve others. Both unverified. Removed entirely pending a real figure.
- **Opening hours normalised** — three different sets existed across schema and visible copy. Now `Mon–Fri 07:30–18:00` everywhere.
- **Tailwind Play CDN replaced** with compiled `assets/tailwind.css` (28 KB). The site previously rendered **completely unstyled** if `cdn.tailwindcss.com` was slow or blocked.
- **`og-image.jpg` created** — it was referenced on every page and 404ing.
- **Legal footer disclosure added** — the site was non-compliant with Companies Act 2006 s.82 / e-Commerce Regs (registered name, company number, registered office now shown on all 19 pages).
- **`llms.txt` rewritten**, `robots.txt` expanded for current AI crawlers.

### Confirmed business facts — use these, do not invent

| Field | Value |
|---|---|
| Trading name | R.J. Sayle Plumbing & Heating |
| Registered name | R.J Sayle Plumbing & Heating Services Ltd |
| Company number | 14323418 |
| Director | Russ Sayle (Russell James Sayle) — sole director |
| Incorporated | 30 August 2022 |
| Registered office | 113 Wallasey Road, Wallasey, CH44 2AA |
| SIC | 43220 |
| Phone | 07450 237593 |
| Email | info@rjsayleplumbing-heating.com |
| Hours | Mon–Fri 07:30–18:00, emergency callouts subject to availability |
| Canonical host | `https://rjsayleplumbing-heating.com` (no www) |

### Blocked — needs the owner, do not guess

| Item | Where it goes | Status |
|---|---|---|
| **Gas Safe registration number** | `GAS_SAFE_NUM` in `seo-fix.py` | **Blocking Phase 1** |
| **GA4 measurement ID** | `GA4_ID` in `seo-fix.py` | **Blocking Phase 1** |
| Verified Google review count + rating | `RATING_VALUE` / `REVIEW_COUNT` | Blocks `/reviews.html` |
| Public liability insurance value | `/guarantees-insurance-accreditations.html` | Blocks that page |
| MCS certification — yes or no? | Determines whether `/air-source-heat-pumps-wirral.html` is built at all | Blocks P1-11 |
| Real call-out / repair pricing | Pricing sections on service pages | Blocks P1-04 |
| Social/citation profile URLs | `SAME_AS` in `seo-fix.py` | Ongoing |

**If a blocker isn't resolved, skip that item and flag it. Never invent a Gas Safe number, a price, an insurance figure, or a review.**

---

## 2. Ground rules

These are hard constraints. Breaking them undoes Phase 0.

1. **Never re-add `<script src="https://cdn.tailwindcss.com">`.** If you add Tailwind classes, recompile:
   ```bash
   npx tailwindcss@3 -c tailwind.config.js -i tailwind.input.css -o assets/tailwind.css --minify
   ```
2. **All URLs are apex, no `www`.** Canonical, `og:url`, schema `url`, sitemap, internal links.
3. **One JSON-LD block per page**, always an `@graph`, always reusing `@id` `https://rjsayleplumbing-heating.com/#business`. Never emit a second standalone `LocalBusiness`.
4. **Generate schema by running `seo-fix.py`, not by hand.** Add new pages to its `PAGES` dict and re-run. It is idempotent. Hand-written JSON-LD is how the original fragmentation happened.
5. **No `aggregateRating` or `Review` markup** until a verified count exists.
6. **Flat URLs** — `/boiler-installation-wirral.html`, not `/services/boiler-installation/`. GitHub Pages, ~15 pages, no directory-index migration needed.
7. **No street address in `PostalAddress` schema.** Locality-level only (Wirral, Merseyside) so GBP can run as a service-area business with the address hidden. The registered office belongs in the footer legal line only.
8. **Never generate pages from a `{{town}}` template.** If you find yourself in a loop substituting a place name, stop — that is the doorway-page pattern this work is fixing.
9. **UK English throughout.** Existing copy voice: direct, plain, no marketing fluff, first person plural.
10. **One `<h1>` per page.** Keep the skip-link and existing accessibility markup.

---

## 3. Phases

Work top to bottom. Each phase has a definition of done. Commit per phase.

---

### PHASE 1 — Unblock measurement *(do first, ~30 min)*

Nothing else can be evaluated until this is in. The site currently has **no analytics of any kind** and 142 unmeasured `tel:` links.

**Tasks**

1. Set `GA4_ID` in `seo-fix.py` CONFIG. Re-run `python seo-fix.py`. This injects GA4 plus two events: `call_click` (every `tel:` click, with page path) and `generate_lead` (contact form submit).
2. Set `GAS_SAFE_NUM`. Re-run. Puts the number into `hasCredential`.
3. Add the Gas Safe number to the visible footer next to "Gas Safe Registered". Highest-value trust element on the site and it costs nothing.
4. Verify the Formspree endpoint (`formspree.io/f/myklezqd` in `contact.html`) still delivers, and to which mailbox. Four pages previously pointed at a dead email — assume nothing.
5. Add a sticky click-to-call bar on mobile (`tel:07450237593`), below 768px, not obscuring content.

**Done when:** GA4 fires `page_view` and `call_click` in DebugView; Gas Safe number appears in the footer and in `hasCredential` on all 19 pages; a test form submission arrives in a real inbox.

---

### PHASE 2 — Money pages *(the largest revenue item)*

12 services currently share one `/services.html`. That page cannot rank for "boiler installation Wirral", "power flushing Wirral" and "unvented cylinder Wirral" simultaneously. This is the biggest untapped surface on the site.

**Build in this order.** Full specs — H1, meta title with character counts, meta description, section outline, FAQs, internal links — are in `02-content-gap-and-build-out-plan.md` §2. Follow them exactly; the character counts are already validated.

| Order | URL | Notes |
|---|---|---|
| 1 | `/boiler-installation-wirral.html` | Highest revenue per visit. Peaks Sept–Jan — ship before September. |
| 2 | `/boiler-repair-wirral.html` | Volume spikes on the first cold snap. December is peak breakdown month. |
| 3 | `/emergency-plumber-wirral.html` | Best-converting query class. |
| 4 | `/boiler-prices-wirral.html` | **Blocked on real pricing.** Highest-friction objection in the trade. |
| 5 | `/landlord-gas-safety-cp12-wirral.html` | Recurring revenue. |
| 6 | `/boiler-servicing-wirral.html` | Recurring revenue. |
| 7–16 | See §2 table | `/power-flushing-wirral.html`, `/unvented-cylinder-wirral.html`, `/radiators-and-central-heating-wirral.html`, `/combi-boiler-conversion-wirral.html`, `/air-source-heat-pumps-wirral.html` *(MCS-blocked)*, `/boiler-upgrade-scheme-wirral.html`, rebuild `/commercial-plumbing-heating-wirral.html`, `/reviews.html` *(blocked)*, `/guarantees-insurance-accreditations.html` *(partly blocked)*, `/case-studies/index.html` |

**The differentiator to use throughout:** Wirral is a **soft-water area** (~73ppm vs UK average ~230ppm). Every national competitor writes limescale content that is irrelevant here. The real local failure mode is **magnetite sludge and corrosion**. Accurate, useful, and nobody in this market is saying it. Vary the emphasis per page — don't paste the same paragraph.

**Do not build:** a boiler finance page (no FCA-regulated partner in place — regulatory risk), individual boiler brand pages (build one combined comparison page instead), air conditioning (not offered), a careers page.

**For each new page:**
- Add it to the `PAGES` dict in `seo-fix.py`, then re-run — this generates schema, breadcrumbs and the sitemap entry automatically.
- Link it from `/services.html` (which stays as the hub) and from every relevant area page.
- Add the FAQs to the page body; `seo-fix.py` lifts them into `FAQPage` schema automatically if marked up in the existing `<details>` pattern.

**Done when:** all unblocked pages exist, are in `sitemap.xml`, validate on validator.schema.org, and are reachable from `/services.html` within one click.

---

### PHASE 3 — De-templatise the 11 area pages *(risk reduction, not just growth)*

The 11 existing area pages are ~70% identical, with three FAQs that differ only by town name. `02-content-gap-and-build-out-plan.md` §3 makes the case plainly: **these currently sit on the wrong side of Google's doorway-page line.** This is a risk being carried right now, not a theoretical one.

**The universal fix first.** Delete these three FAQs from all eleven pages:
- "Do you cover X?"
- "How quickly can you respond in X?"
- "Do you offer free quotes in X?"

Replace with three questions per page that could only be asked about that place. Suggested replacements are in §4 of the content plan, per area.

**Target: 400+ words of genuinely unique content per page.** Kill the identical "Services Available", "Why Choose" and "Also Serving Nearby" blocks. Replace with: short unique intro → local-specific technical section → one real local job → three different FAQs.

**Local hooks are researched and specific** — §4 of the content plan has 2–4 per area. Summary of the strongest:

| Area | Lead angle |
|---|---|
| Heswall | Large detached, poor mains flow — "why a combi is often the wrong answer here". Lower Village/Gayton/Barnston conservation areas. Off-grid pockets toward Barnston/Thurstaston qualify for the £9,000 BUS grant until 31 Mar 2027. **Make this the strongest page — JF Plumbing is based in Heswall.** |
| West Kirby | Solid-wall Victorian/Edwardian villas — radiator sizing that assumes cavity walls undersizes the system. Coastal salt exposure on flue terminals and condensate. |
| Bebington | **Port Sunlight** — Grade II listed model village, tightest external-alteration constraints on the peninsula. Richest local content opportunity on the whole site; no competitor touches it. Plus back-boiler removals in New Ferry, and Bromborough industrial estate as a commercial route. |
| Birkenhead | Hamilton Square listed Georgian conversions; eight of Wirral's 26 conservation areas; highest private-rented concentration → link hard to the CP12 page. |
| Wallasey | Dense 1930s semis with 1970s/80s microbore that clogs. New Brighton coastal exposure, frozen condensate. Microbore-to-standard-bore upgrade is a specific high-value job. |
| Hoylake | King's Gap / Meols Drive Edwardian villas → system boiler + unvented territory. Most exposed frontage on Wirral. Second homes → frost protection and winter vacancy. |
| Neston | **Cheshire West & Chester, not Wirral Council** — different planning authority. Off-grid oil/LPG toward Ness and Burton → £9,000 BUS grant, deadline 31 Mar 2027. Strongest commercial hook of any area page. |
| Ellesmere Port | Cheshire West again. Post-war estate stock with **warm-air heating** still in service — technically demanding, almost zero competition. Industrial corridor → commercial leads. |
| Liverpool | **Be honest about the boundary** — name the L postcodes genuinely served (L1–L8, L17–L19). Water hardness genuinely varies: L10–L19 is 122–131ppm (limescale *is* relevant), L20–L29 is 34–43ppm (it isn't). Precise, verifiable, nobody else says it. |
| Wirral | Reposition as a **hub**, not a leaf. Postcode districts, links to all ten sub-areas, the soft-water/sludge explainer as the anchor. Remove the duplicated service list. |
| Nationwide | Rewrite as **commercial fit-out and shopfitting only**. Link solely from the commercial page; remove from domestic nav. If nationwide commercial isn't genuinely delivered, delete the page. |

**Then, and only then**, build the 8 approved service×area pages listed in §3 of the content plan. **Eight. Not 33, not 165.** Each must clear the five-point gate in that section — including *"contains a real completed job in that town, with the street or district named"*. If the job hasn't been done there, the page isn't built yet.

**Done when:** no FAQ question appears on more than one area page; every area page has 400+ unique words; `/areas/wirral.html` is a hub; `/areas/nationwide.html` is commercial-only or deleted.

---

### PHASE 4 — Gallery → case studies

**Current state:** 24 images, all hotlinked from `static.wixstatic.com`, all with identical alt text `"R.J. Sayle completed plumbing project"`, no captions, locations or dates.

Two problems: if that Wix account lapses the entire gallery 404s, and 24 images with duplicate alt text have zero image-search value.

**Tasks**

1. Download all 24 into `/gallery/` (the folder exists and is empty). Convert to WebP, reasonable dimensions, `loading="lazy"`.
2. Write real alt text per image — *"New Worcester Bosch combi boiler installation, Heswall"*, not the same string 24 times.
3. Update `gallery.html` to local paths. Re-run `seo-fix.py` to refresh `ImageGallery` schema.
4. Convert into ~12 case studies using the template in §5 of the content plan (problem → survey findings → what we did → result → cost → customer words → CTA).
5. Build `/case-studies/index.html` with filters by service and by area.

**Done when:** zero `static.wixstatic.com` references remain; no two images share alt text; 12 case studies published and linked from the relevant service and area pages.

---

### PHASE 5 — Off-site *(mostly not a code task)*

`sameAs` is still empty. Nothing corroborates this business entity — one website asserting facts about itself is the weakest possible position for both local pack and AI citation.

The code task is small: as each profile goes live, add its URL to `SAME_AS` in `seo-fix.py` and re-run. Everything else is in `03-citations-and-off-site-plan.md`.

---

## 4. Definition of done — run before every commit

```bash
# 1. Schema integrity — expect "NONE"
python3 - <<'PY'
import json,re,glob
bad=[]
for f in glob.glob('**/*.html',recursive=True):
    if f.startswith('google'): continue
    h=open(f,encoding='utf-8').read()
    b=re.findall(r'application/ld\+json[^>]*>(.*?)</script>',h,re.S)
    if len(b)!=1: bad.append((f,f'{len(b)} blocks')); continue
    d=json.loads(b[0])
    if '@graph' not in d: bad.append((f,'no @graph')); continue
    can=re.search(r'rel="canonical" href="([^"]+)"',h)
    og=re.search(r'property="og:url" content="([^"]+)"',h)
    if not can or 'www.' in can.group(1): bad.append((f,'bad canonical'))
    if can and og and can.group(1)!=og.group(1): bad.append((f,'og:url != canonical'))
print(bad or 'NONE')
PY

# 2. No regressions
grep -rl "cdn.tailwindcss.com\|www.rjsayleplumbing\|rjsayleplumbing.co.uk" --include=*.html .

# 3. Sitemap matches canonicals exactly
python3 - <<'PY'
import re,glob
locs=set(re.findall(r'<loc>([^<]+)</loc>',open('sitemap.xml').read()))
cans={m.group(1) for f in glob.glob('**/*.html',recursive=True)
      for m in [re.search(r'rel="canonical" href="([^"]+)"',open(f,encoding='utf-8').read())] if m}
print('sitemap-only:', sorted(locs-cans)); print('canonical-only:', sorted(cans-locs))
PY

# 4. Render check — no unstyled pages, no console errors
python3 -m http.server 8080
```

Also: paste one changed page into [validator.schema.org](https://validator.schema.org/) and the [Rich Results Test](https://search.google.com/test/rich-results).

---

## 5. Do not do these

Recorded so they don't get re-litigated:

- **Don't chase extensionless vs `.html` URLs.** GitHub Pages serves both with a 200 and cannot 301 between them. Canonicals handle consolidation.
- **Don't add photo geotagging / EXIF tooling.** Google strips EXIF on upload. It has never worked.
- **Don't build a blog yet.** Service pages and tracking first. Blogging into an unmeasured funnel is how trade sites waste twelve months.
- **Don't add call-tracking numbers.** NAP-consistency risk outweighs the benefit at this scale.
- **Don't add a street address to `PostalAddress` schema.** See ground rule 7.
- **Don't reinstate `aggregateRating`** from the old hardcoded values. They contradicted each other and were unverified.
- **Don't hand-write JSON-LD.** Extend `seo-fix.py`.
- **Don't build more than 8 service×area pages.** "Just a few more" is exactly how a legitimate local cluster becomes a doorway cluster.

---

## 6. Owner actions (not code — chase if blocking)

1. **Gas Safe number** and **GA4 ID** — blocking Phase 1.
2. **Decide the brand name.** Registered name is *R.J Sayle Plumbing & Heating **Services** Ltd*; the site says *…Heating Ltd*. Pick one, then make site, GBP and every citation match. Name drift is the most common cause of NAP damage and is far harder to unpick later.
3. **Confirm `info@rjsayleplumbing-heating.com` has a live mailbox.**
4. **Claim and verify GBP** — hide the address, set 8 named service areas, match hours to the site. See `04-google-business-profile-plan.md`.
5. **Set up missed-call auto-SMS.** Highest-ROI item across all four documents and it isn't SEO. A ranking Wirral plumber takes 15–30 calls a week on one mobile, often mid-job.
6. **Get the true Google review count** so `aggregateRating` can be reinstated accurately.
7. **Confirm MCS certification status** — decides whether the heat pump page gets built.
