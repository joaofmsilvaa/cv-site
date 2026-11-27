"""Local CMS smoke test: open /admin, edit Profile headline, save, check the JSON file and the rebuilt page."""
import sys, json, time, pathlib
from playwright.sync_api import sync_playwright

base, out = sys.argv[1], sys.argv[2]
marker = "CMS TEST EDIT"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    pg.goto(base + "/admin/")
    pg.get_by_role("button", name="Login").click()
    pg.goto(base + "/admin/#/collections/cv/entries/profile")
    field = pg.get_by_label("Headline")
    field.wait_for(timeout=60000)
    pg.screenshot(path=f"{out}/admin_profile.png")
    original = field.input_value()
    field.fill(marker)
    pg.get_by_text("Publish", exact=True).first.click()
    pg.get_by_text("Publish now").click()
    time.sleep(4)
    saved = json.loads(pathlib.Path("content/profile.json").read_text(encoding="utf-8"))
    print("file headline:", saved["headline"])
    time.sleep(3)
    pg.goto(base + "/")
    print("page shows edit:", marker in pg.content())
    b.close()
