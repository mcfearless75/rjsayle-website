import re, glob
for f in glob.glob("**/*.html", recursive=True):
    h = open(f, encoding="utf-8").read()
    if "cdn.tailwindcss.com" not in h: continue
    h = re.sub(r'[ \t]*<script src="https://cdn\.tailwindcss\.com"></script>\s*\n', '', h)
    h = re.sub(r'[ \t]*<script>\s*tailwind\.config\s*=.*?</script>\s*\n', '', h, flags=re.S)
    h = h.replace('</head>', '  <link rel="stylesheet" href="/assets/tailwind.css">\n</head>', 1)
    open(f, "w", encoding="utf-8").write(h)
