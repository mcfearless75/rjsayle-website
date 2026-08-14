import re, glob
# Tailwind Preflight sets img{height:auto}, nullifying the height attribute.
for f in glob.glob("**/*.html", recursive=True):
    h = open(f, encoding="utf-8").read(); o = h
    h = re.sub(r'(<img[^>]*?)height="(\d+)"([^>]*?)style="width:auto;display:block;"',
               r'\1\3style="height:\2px;width:auto;display:block;"', h)
    if h != o: open(f, "w", encoding="utf-8").write(h)
