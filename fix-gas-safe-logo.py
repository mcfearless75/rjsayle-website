#!/usr/bin/env python3
"""
Shrink the Gas Safe Register logo consistently site-wide and add explicit
width/height HTML attributes (not just CSS) so the browser reserves the
correct box immediately and the image can never flash to its full
intrinsic size (298x335px) before styling applies.

viewBox is 120x135 -> aspect ratio 0.8889. At height=22 that's width~20.

Idempotent: matches any of the previous height:28px/32px/36px variants.
Run from the repo root: python fix-gas-safe-logo.py
"""
import re, glob

OLD = re.compile(
    r'<img src="([./a-zA-Z]*Gas_Safe_Register\.svg)" alt="Gas Safe Register"\s+'
    r'style="height:\d+px;width:auto;display:block;"\s+loading="eager">'
)

NEW = ('<img src="{src}" alt="Gas Safe Register" width="20" height="22" '
       'style="height:22px;width:20px;display:block;" loading="eager">')

def process(path):
    html = open(path, encoding="utf-8").read()
    new_html, n = OLD.subn(lambda m: NEW.format(src=m.group(1)), html)
    if n:
        open(path, "w", encoding="utf-8").write(new_html)
    return n

if __name__ == "__main__":
    total = 0
    for p in glob.glob("**/*.html", recursive=True):
        if p.startswith("google"):
            continue
        n = process(p)
        if n:
            print(f"  {p}: {n} replaced")
            total += n
    print(f"\nDone. {total} logo instances resized.")
