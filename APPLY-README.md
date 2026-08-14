# How to apply — Windows

Repo: `C:\Users\LAPTOP80\Projects\rjsayle-website`

## Option A — overlay the zip (simplest)

1. Unzip this archive.
2. Copy **all contents** over `C:\Users\LAPTOP80\Projects\rjsayle-website`, overwriting.
3. Then:
   ```
   git status
   git diff
   git add -A
   git commit -m "SEO/GEO: apex canonicals, unified schema @graph, director + company identity, compiled Tailwind, legal footer, OG image, llms.txt"
   git push
   ```
4. GitHub Pages redeploys in about a minute.

## Option B — apply the patch

```
cd C:\Users\LAPTOP80\Projects\rjsayle-website
git apply --stat  rjsayle-seo.patch
git apply --check rjsayle-seo.patch
git apply         rjsayle-seo.patch
```

## Re-running after you fill in the remaining config

Edit the CONFIG block at the top of `seo-fix.py`:

| Value | Status |
|---|---|
| `DIRECTOR_NAME` / `DIRECTOR_LEGAL` | done — Russ Sayle / Russell James Sayle |
| `COMPANY_NUMBER` | done — 14323418 |
| `LEGAL_NAME` / `REG_OFFICE` | done — from Companies House |
| `GAS_SAFE_NUM` | **needed** |
| `GA4_ID` | **needed** |
| `SAME_AS` | add each profile URL as you create it |
| `RATING_VALUE` / `REVIEW_COUNT` | leave blank until verified in GBP |

Then:

```
python seo-fix.py
python geo-assets.py
```

Both are idempotent — safe to run repeatedly. Blank values are omitted from the
output rather than guessed, so nothing in your structured data is invented.

If you change Tailwind classes in the HTML, recompile the stylesheet:

```
npx tailwindcss@3 -c tailwind.config.js -i tailwind.input.css -o assets/tailwind.css --minify
```

Do **not** re-add `<script src="https://cdn.tailwindcss.com">`. That was breaking
rendering whenever the CDN was slow or blocked, and it is a Core Web Vitals problem.

`rebuild.sh` runs the whole chain from a clean clone (Linux/WSL/Git Bash).

## Verify after pushing

- https://validator.schema.org/ — paste the homepage URL
- https://search.google.com/test/rich-results
- https://pagespeed.web.dev/ — bank the Tailwind win
- Search Console: verify the **apex** property (no www), resubmit sitemap.xml
