"""Fetch every page in the live sitemap and write a Markdown text copy (Source 1 for the report)."""
import re, sys, html, urllib.request, datetime

base = sys.argv[1].rstrip("/")
out = sys.argv[2]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (cv-site knowledge export)"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")

def text(page):
    m = re.search(r"(?is)<main[^>]*>(.*)</main>", page)
    t = m.group(1) if m else page
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", "", t)
    t = re.sub(r"(?i)<h1[^>]*>", "\n# ", t)
    t = re.sub(r"(?i)<h2[^>]*>", "\n## ", t)
    t = re.sub(r"(?i)<h3[^>]*>", "\n### ", t)
    t = re.sub(r"(?i)<li[^>]*>", "\n- ", t)
    t = re.sub(r"(?i)<(dt)[^>]*>", "\n**", t); t = re.sub(r"(?i)</dt>", "**", t)
    t = re.sub(r"(?i)</(p|h[1-6]|dd|ul|ol|div|section|header)>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    lines = [re.sub(r"[ \t\xa0]+", " ", l).strip() for l in t.splitlines()]
    res, prev = [], None
    for l in lines:
        if l in ("-",):
            continue
        if not l and not prev:
            continue
        res.append(l); prev = l
    return "\n".join(res).strip()

sm = get(base + "/sitemap.xml")
urls = re.findall(r"<loc>(.*?)</loc>", sm)
order = ["/", "/education/", "/experience/", "/skills/", "/projects/", "/cv/", "/chat/"]
urls.sort(key=lambda u: order.index(u[len(base):]) if u[len(base):] in order else 99)

parts = [f"# Source 1: Personal website\n\n- **URL:** {base}/\n- **Pages:** {len(urls)} (from {base}/sitemap.xml)\n- **Retrieved:** {datetime.date.today().isoformat()}\n- **Note:** this is the text the chatbot crawls. Content is managed in Decap CMS at {base}/admin/.\n"]
for u in urls:
    parts.append(f"\n---\n\n<!-- page: {u} -->\n**Page URL:** {u}\n\n" + text(get(u)))
open(out, "w", encoding="utf-8").write("\n".join(parts) + "\n")
print(len(urls), "pages")
