"""Screenshot pages of a running site. Usage: python tools/shoot.py BASE_URL OUT_DIR path1 path2 ..."""
import sys
from playwright.sync_api import sync_playwright

base, out, paths = sys.argv[1], sys.argv[2], sys.argv[3:]
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp in [("desktop", {"width": 1280, "height": 900}), ("mobile", {"width": 390, "height": 844})]:
        pg = b.new_page(viewport=vp)
        for path in paths:
            pg.goto(base + path, wait_until="networkidle")
            slug = path.strip("/").replace("/", "_") or "home"
            pg.screenshot(path=f"{out}/{slug}_{name}.png", full_page=True)
    b.close()
