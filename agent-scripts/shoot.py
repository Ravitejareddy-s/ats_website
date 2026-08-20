import sys, pathlib
from playwright.sync_api import sync_playwright

# This file lives in <repo>/agent-scripts/, so parents[1] is the repo root.
ROOT = pathlib.Path(__file__).resolve().parents[1]
url = (ROOT / "index.html").as_uri()
outdir = ROOT / "agent-scripts" / "shots"
outdir.mkdir(parents=True, exist_ok=True)

# section id -> filename (full element screenshot). "FULL" = full page, "VP" = viewport
targets = [
    ("home", "hero"),
    ("about", "about"),
    ("services", "services"),
    ("brands", "brands"),
    ("clients", "clients"),
    ("organization", "organization"),
    ("contact", "contact"),
]

def shoot(width, tag):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": width, "height": 900}, device_scale_factor=2)
        pg.goto(url)
        pg.wait_for_timeout(400)
        # trigger reveals: scroll through the page
        h = pg.evaluate("document.body.scrollHeight")
        y = 0
        while y < h:
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(120)
            y += 700
        pg.evaluate("window.scrollTo(0,0)")
        pg.wait_for_timeout(300)
        # full page
        pg.screenshot(path=str(outdir / f"{tag}-full.png"), full_page=True)
        # per-section
        for sid, name in targets:
            try:
                el = pg.query_selector(f"#{sid}")
                el.scroll_into_view_if_needed()
                pg.wait_for_timeout(250)
                el.screenshot(path=str(outdir / f"{tag}-{name}.png"))
            except Exception as e:
                print("skip", sid, e)
        b.close()

tag = sys.argv[1] if len(sys.argv) > 1 else "desktop"
width = int(sys.argv[2]) if len(sys.argv) > 2 else 1366
shoot(width, tag)
print("done", tag, width)
