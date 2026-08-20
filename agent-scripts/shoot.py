import sys, pathlib
from playwright.sync_api import sync_playwright

# This file lives in <repo>/agent-scripts/, so parents[1] is the repo root.
ROOT = pathlib.Path(__file__).resolve().parents[1]
url = (ROOT / "index.html").as_uri()
outdir = ROOT / "agent-scripts" / "shots"
outdir.mkdir(parents=True, exist_ok=True)

# --- WHY THIS FILE GUARDS DIMENSIONS ---------------------------------------
# The model vision input rejects any image whose width OR height exceeds
# 8000 physical pixels. The old script used device_scale_factor=2 with a
# full_page screenshot; on a tall page that easily produced >8000px images
# and every read of the PNG failed. Rules now enforced below:
#   * physical px = css px * device_scale_factor   (must stay < MAX_PX)
#   * per-section shots stay crisp (scale 2) because sections are short;
#     a section taller than the cap is tiled instead of one giant grab.
#   * the whole-page overview is rendered in a separate pass whose scale is
#     computed from the measured page height so it can never blow the cap
#     (it simply downscales for very tall pages).
# Keep the hero realistic: viewport height stays 900 so `min-height:100vh`
# renders like a real screen instead of being stretched by a tall viewport.
MAX_PX = 7600          # hard ceiling, comfortably under the 8000 limit
SECTION_SCALE = 2      # crisp section shots
VIEW_H = 900           # realistic viewport height

# section id -> filename (full element screenshot)
targets = [
    ("home", "hero"),
    ("about", "about"),
    ("services", "services"),
    ("brands", "brands"),
    ("clients", "clients"),
    ("organization", "organization"),
    ("contact", "contact"),
]


def prime(pg):
    """Scroll through the page to trigger reveal-on-scroll animations, then reset."""
    h = pg.evaluate("document.body.scrollHeight")
    y = 0
    while y < h:
        pg.evaluate(f"window.scrollTo(0,{y})")
        pg.wait_for_timeout(90)
        y += 600
    pg.evaluate("window.scrollTo(0,0)")
    pg.wait_for_timeout(250)


def shoot_sections(b, width, tag):
    pg = b.new_page(viewport={"width": width, "height": VIEW_H}, device_scale_factor=SECTION_SCALE)
    pg.goto(url)
    pg.wait_for_timeout(400)
    prime(pg)
    for sid, name in targets:
        try:
            el = pg.query_selector(f"#{sid}")
            if not el:
                print("skip", sid, "(not found)")
                continue
            el.scroll_into_view_if_needed()
            pg.wait_for_timeout(220)
            box = el.bounding_box()
            # If the element is too tall for the pixel cap, tile it vertically.
            if box and box["height"] * SECTION_SCALE > MAX_PX:
                tile_h = MAX_PX / SECTION_SCALE
                n = int(box["height"] // tile_h) + 1
                for i in range(n):
                    y = min(box["y"] + i * tile_h, box["y"] + box["height"] - tile_h)
                    y = max(0, y)
                    pg.evaluate(f"window.scrollTo(0,{y})")
                    pg.wait_for_timeout(120)
                    pg.screenshot(
                        path=str(outdir / f"{tag}-{name}-{i + 1:02d}.png"),
                        clip={"x": 0, "y": 0, "width": width, "height": tile_h},
                    )
            else:
                el.screenshot(path=str(outdir / f"{tag}-{name}.png"))
        except Exception as e:
            print("skip", sid, e)
    pg.close()


def shoot_full(b, width, tag):
    # Measure page height first, then choose a scale that keeps every side < MAX_PX.
    probe = b.new_page(viewport={"width": width, "height": VIEW_H})
    probe.goto(url)
    probe.wait_for_timeout(300)
    prime(probe)
    H = probe.evaluate("document.body.scrollHeight")
    probe.close()
    dsf = min(1.5, MAX_PX / max(H, 1), MAX_PX / width)
    pg = b.new_page(viewport={"width": width, "height": VIEW_H}, device_scale_factor=dsf)
    pg.goto(url)
    pg.wait_for_timeout(400)
    prime(pg)
    # Full-page capture re-lays-out the page; reveal-on-scroll elements below the
    # fold can end up still hidden. Force every reveal/fade element visible so the
    # overview always shows real content instead of blank sections.
    pg.add_style_tag(content=".reveal,.fade{opacity:1!important;transform:none!important}")
    pg.evaluate("document.querySelectorAll('.reveal').forEach(function(e){e.classList.add('in');})")
    pg.wait_for_timeout(250)
    pg.screenshot(path=str(outdir / f"{tag}-full.png"), full_page=True)
    pg.close()


def shoot(width, tag):
    with sync_playwright() as p:
        b = p.chromium.launch()
        shoot_sections(b, width, tag)
        shoot_full(b, width, tag)
        b.close()


tag = sys.argv[1] if len(sys.argv) > 1 else "desktop"
width = int(sys.argv[2]) if len(sys.argv) > 2 else 1366
shoot(width, tag)
print("done", tag, width)
