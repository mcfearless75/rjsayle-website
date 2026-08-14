#!/usr/bin/env python3
"""
Phase 1 task 5 of SEO-WORK-ORDER.md — sticky mobile click-to-call bar.

Idempotent: inserts a fixed-bottom tap-to-call bar (visible only below the
md breakpoint, matches the Tailwind config already compiled into
assets/tailwind.css) before </body> on every page that doesn't already have
one, and pads <body> so it doesn't obscure footer content on mobile.

Run from the repo root: python sticky-call-bar.py
"""
import glob

MARKER = 'id="mobile-call-bar"'

BAR = '''  <a href="tel:+447450237593" id="mobile-call-bar" class="md:hidden fixed bottom-0 inset-x-0 z-50 flex items-center justify-center gap-2 bg-brand text-white font-heading font-bold text-base py-3.5 shadow-[0_-4px_16px_rgba(0,0,0,0.15)]" aria-label="Call R.J. Sayle Plumbing and Heating on 07450 237593">
    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
    Call Now: 07450 237593
  </a>
'''

BODY_PAD = '<style>@media(max-width:767px){body{padding-bottom:52px}}</style>\n</head>'

def process(path):
    html = open(path, encoding="utf-8").read()
    if MARKER in html:
        return False
    if "</body>" not in html or "</head>" not in html:
        return False
    html = html.replace("</head>", BODY_PAD, 1)
    html = html.replace("</body>", BAR + "</body>", 1)
    open(path, "w", encoding="utf-8").write(html)
    return True

if __name__ == "__main__":
    pages = [p for p in glob.glob("**/*.html", recursive=True)
             if not p.startswith("google")]
    changed = 0
    for p in pages:
        if process(p):
            changed += 1
            print(f"  + {p}")
    print(f"\nDone. {changed}/{len(pages)} pages updated (rest already had the bar or aren't full HTML documents).")
