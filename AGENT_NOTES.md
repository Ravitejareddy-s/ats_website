# AGENT NOTES — ats_website

Agent-maintained context. Not for human docs. Keep terse; update when you learn something a future session would waste tokens rediscovering.also delete if you feel something is unnessasary that task is done or the future agents dosent need that info its just waste of tokens 

## What this is
Single-file marketing site for **A2S Technical Services** (aka ATS / Ark Design Studio) — a UAE lighting + technical-services company. Everything lives in `index.html` (inline `<style>`, no build step). Deployed to Cloudflare via `wrangler.jsonc` (static assets, serves repo root).

## Layout of index.html
Sections in order: nav → hero → about → mission/vision → services → products → brands → clients → organization (org chart) → contact → footer. All CSS is one inline `<style>` block; responsive breakpoints at 900px and 560px.

## Design system
- Palette: cream (`--cream-1 #f7f2e8`, `--cream-2`, `--cream-3`), ink `#29231b`, amber (`#e2a04c`/`#c9852f`/`#a5651b`).
- Fonts: Bricolage Grotesque (headings), Fraunces italic (accent), Inter (body).
- Assets committed at root: `logo.jpg`, `skyline.jpg`.
- We deliberately kept the softer amber aesthetic instead of the PDF's brighter orange (`#f26a21`) for cohesion.
- **Hero bg is now PURE WHITE** (`#ffffff`), per user — was a cream gradient. `.skyline-fade` fades to white too. The skyline reads as a soft grey silhouette on white. Content/copy of hero is unchanged (user said "details are right").

## "Sleek, not PowerPoint" redesign pass (user asked to de-slide the non-hero sections)
The old sections felt like slides: faint ghost cards (`rgba(255,255,255,0.6)` + `var(--line)` border), a 5-card Services grid that orphaned card #5, near-invisible logo tiles, and very airy `section-pad`. Fixes now in place — keep them:
- **Cards** (`.svc-card`, `.mv-card`, `.office-card`, `.contact-extra`, `.logo-tile`): solid `#fff`, `1px solid rgba(70,58,42,0.10)` border, layered `box-shadow: 0 14px 34px -18px rgba(...)`, radius 20. All lift on hover. Don't revert to translucent fills — that's what made them look like slide clip-art.
- **Services** = flexbox `justify-content:center` with `.svc-card { flex:1 1 300px; max-width:344px }` → renders 3 + 2 (centered) on desktop, no orphan; wraps to 2 then 1 on smaller screens automatically (no media queries needed). Editorial index numbers `01`–`05` come from a CSS counter on `.svc-grid`/`.svc-card::before` (NOT in HTML — don't add number markup).
- **Brands + Clients** are now compact "logo strip" sections: `section-pad-sm` + `.section-head.compact` (smaller h2) so they read as supporting proof, not full title slides. Logo tiles are crisp white w/ shadow, still grayscale→color on hover (default `opacity:0.72`).
- **Spacing**: global `.section-pad` tightened to `clamp(64px,8.5vw,108px)`; added `.section-pad-sm = clamp(48px,6vw,80px)`.
- Org section left structurally as-is (hard requirement); it's the dark section and looks intentional despite the Project-Division-is-tall imbalance.

## Brands / clients logo walls = REAL logos now wired in (was CSS wordmarks)
The `#brands` and `#clients` `.logo-grid`s in `index.html` now use real `<img class="logo-img" src="logos/...">` (transparent PNGs from `./logos/`), NOT the old CSS wordmarks. The `.logo-tile` grayscale-to-color-on-hover treatment is unchanged and unifies them. Verified on desktop 1366 + mobile 390 (2-col, no overflow).
- Brands imgs: tridonic.png, tci.png, vossloh-schwabe.png, leddomain.png, meanwell.png (meanwell is a solid RED badge — corners are red, not a bg to remove).
- Clients imgs: mediclinic.png, smartpoles-logo-nobg.png (=Smart Pole Fabrications tile), areej-landscaping.png (dark recolor, reads on cream), ghtc-logo-website-removebg-preview.png. **Horizon Trading LLC has NO real logo** → still the hand-built `.wm-horizon` wordmark (SVG icon + text).
- `.logo-img` CSS: `max-width:100%; max-height:82px; object-fit:contain`. The `.wm-*` wordmark CSS is now mostly DEAD except `.wm` base + `.wm-horizon` (still used). Left in place as harmless fallback; remove if tidying.

### ./logos/ real-logo assets (sourced from official sites, bg removed/verified)
Files: `meanwell.png`, `leddomain.png`, `vossloh-schwabe.png`(+`.svg`), `tridonic.png`(+`.svg`), `tci.png`, `mediclinic.png`, `areej-landscaping.png` (dark, use this on the cream site) + `areej-landscaping-white.png` (original white), plus pre-existing `ghtc-*` and `smartpoles-*`. `_proof-*.png` are throwaway verification sheets (deletable).
- **`./logos/` is NOT gitignored and NOT in `.assetsignore`** => these WILL be committed AND served publicly on Cloudflare. (Third-party trademarks — fine for a partners/clients strip, but be aware.)
- Per-logo color caveats (matters on the cream/light site): leddomain + vossloh-schwabe are **black** (great on cream, invisible on dark); areej official is **white** (invisible on cream — that's why `areej-landscaping.png` is a recolored-dark derivative; `-white.png` is the untouched original); tridonic(purple)/tci(blue)/mediclinic(blue)/meanwell(red) work on any bg.
- Sourcing gotchas for re-fetch: tridonic.com returns **403 to curl** — must load via Playwright real browser (logo = `/image/tridonic_logo.svg`). meanwell logo is only a **90x52 CSS bg** at `/styles/images/logo2.png` (low-res, white bg flood-filled). vossloh/tridonic came as SVG → rasterized to PNG with Playwright (`omit_background=True`, device_scale_factor=3). areej/mediclinic/tci/leddomain already had transparent PNGs on-site. Clearbit logo API is dead; Brandfetch CDN needs a key.
- **Grid gotcha:** logo grids MUST use `repeat(N, minmax(0, 1fr))`, not `repeat(N, 1fr)`. `1fr` = min-content floor, and a wide unbreakable token (e.g. the non-breaking hyphen once in "Vossloh-Schwabe") blows the track past the viewport on mobile. minmax(0,1fr) caps it. Big wordmarks also get font-size reductions inside the `max-width: 560px` query.

## Mobile nav drawer — the see-through/short-drawer trap (fixed, don't reintroduce)
Symptom user hit: on mobile, AFTER SCROLLING, the open menu drawer went transparent and page text bled through it. Two compounding bugs, both from `.nav.scrolled` gaining `backdrop-filter`:
1. **Nested backdrop-filter** — the drawer had its own `backdrop-filter` nested inside the scrolled nav's `backdrop-filter`; iOS/WebKit renders the inner one see-through. Fix: drawer is now a SOLID opaque `background:#f6f1e6` with NO backdrop-filter. Don't re-add blur to the drawer.
2. **Containing-block trap** — `backdrop-filter` (like transform/filter) makes `.nav` the containing block for its `position:fixed` child `.nav-links`. So the old `inset:0 0 0 auto` (bottom:0) sized the drawer to the ~64px nav bar, not the viewport → short/mis-anchored drawer. Fix: drawer now uses `top:0; right:0; height:100dvh` (with `100vh` fallback) instead of relying on `bottom:0`. Keep it that way regardless of any nav backdrop-filter.
- Also added: a `.nav-scrim` (`#navScrim`, z-index 45) that dims the page behind the drawer; JS toggles `.open` on it alongside the drawer + closes on scrim click. Drawer z-index 55, toggle/X z-index 60 (stays clickable above drawer). Mobile links are full-width rows w/ hairline dividers; Contact is a full-width amber pill.
- **How to verify the drawer** (shoot.py doesn't open it): quick Playwright — viewport 390x844, `scrollTo(0,900)` to trigger `.nav.scrolled`, `click('#navToggle')`, screenshot, read it back. Must be opaque + full-height. The scroll step is essential; the bug ONLY appears once scrolled.

## Org chart = hand-built HTML (hard requirement)
User explicitly forbade pasting it as an image. Structure: root node "A2S Technical Services" → dashed rail → 4 divisions:
- Sales & Marketing → Marketing Team, Sales Engineer
- Project Division → two "Site Engineering" subgroups (A: Creative Team, Technology Engineer; B: Project Execution Supervisors, On Site Team, Off Site Team)
- Operations → Logistics & Purchase
- Account Admin → Logistics & Purchase
Duplicated labels ("Site Engineering" ×2, "Logistics & Purchase" ×2) are faithful to the source PDF — do not "fix" them. Desktop = 4-col grid; ≤900px = 2-col + rail hidden; ≤520px = 1-col. The neutral root node was added by us (source had none).

## Contact info (from PDF + user)
Three offices as `.office-card`s in an `.offices-grid` (3-col desktop → 2-col ≤900px → 1-col ≤560px), each with pin icon, country heading, `<address>`, and bottom-anchored `.office-phone` link. Shared email + "Send an enquiry" CTA in a `.contact-extra` bar below. **The Google Maps iframe was removed** (user request) — do not re-add.
- UAE: A2S Technical Services, FZC 1st Floor, SPCFZ, E311 St, Sharjah, UAE. +971 58 627 9497
- India: 1st Floor, 16-6-185/1, Chadhar Ghat X Road, Near Day Break Cafe, Osmanpura, Hyderabad, Telangana 500024. +91 91007 12697
- USA: 29245 Stephenson Hwy, Madison Heights, MI 48071. +1 612-643-0990
- Emails: sales@a2stechnicalservices.com, info@a2stechnicalservices.com. Footer Contact column lists all three phones.

## agent-scripts/ (committed to git, NOT served — in .assetsignore)
- `shoot.py` = Playwright screenshot tool. **This is the only way to know whether the layout/alignment is actually correct.** You are editing a raw HTML/CSS file blind — you cannot tell if tiles overflow, connectors line up, or sections render right just by reading the code. You MUST run this script, then read the generated PNGs back into your own context and visually inspect them before claiming anything is aligned/done. The mobile brands-grid overflow (see logo-grid gotcha above) was invisible in the code and only caught this way.
- Run: `python3 agent-scripts/shoot.py <tag> <width>` — e.g. `python3 agent-scripts/shoot.py desktop 1366` and `python3 agent-scripts/shoot.py mobile 390`.
- Output → `agent-scripts/shots/{tag}-{section}.png` per section + `{tag}-full.png`. That `shots/` subfolder is gitignored (throwaway); the script itself is committed so future sessions inherit it.
- **8000px guard (don't undo this):** the model's image reader rejects any PNG whose W or H exceeds 8000px. The old script used `device_scale_factor=2` on a `full_page` shot → tall pages produced >8000px images and EVERY read failed. Current script: section shots stay at scale 2 (sections are short; a too-tall one gets tiled), and the `{tag}-full.png` pass measures page height first and picks a fractional `device_scale_factor` so no side exceeds `MAX_PX=7600`. So the full shot is intentionally lower-res on tall pages — that's expected, use section shots for detail.
- The full-page pass also force-reveals all `.reveal`/`.fade` elements (adds `.in` + injects an `!important` opacity/transform override) before shooting, else below-the-fold sections screenshot blank (reveal-on-scroll didn't fire during the fast auto-scroll).

## source-material/ (gitignored + assetsignored — NOT committed, NOT served)
- `A2S PDF (1).pdf` = company profile, source of truth for all copy.
- `pages/page-01..10.png` = the PDF rendered to images (each PDF page is a slide). Read these images to re-extract info.

## Products section (#products, after Services) — product PDFs live in `products/` (public)
- Decision: NO iframe/inline PDF embed (mobile browsers render PDF iframes badly; installers want the file). Each product = a `.prod-card` with 4:3 cover JPG + View (new tab, browser's PDF viewer) + Download (`download` attr with a branded filename). PDFs kept at original size (user chose not to compress).
- `.prod-grid` uses the same centred-flex pattern as `.svc-grid` (1 card centres; more wrap with no orphans). **To add a product:** copy the `<article class="prod-card">` (HTML comment marks it), drop `products/<slug>-manual.pdf` + `products/<slug>-cover.jpg` (~850x640, ~50 KB), update title/model/desc/meta "PDF • N pages • X MB".
- **Product video (optional per card):** a `.prod-video` row ("Watch installation video" + duration) sits between `.prod-meta` and `.prod-actions`. Its `data-video`/`data-poster` attributes open one shared `<dialog id="videoModal">` lightbox (markup is just above the main `<script>`). The `<video>` uses `preload="none"` and its src is set only on click, so the 24 MB file never loads with the page. On close (X, Esc, or backdrop click) the video pauses and the src is removed. The `href` points to the mp4 itself, so it still plays without JS. Gotcha: `.video-modal` needs `margin:auto`, because the global `* {margin:0}` reset removes the dialog's built-in centring. For a product with no video, delete the `<a class="prod-video">`.
- Cover thumbnail = embedded photo extracted from PDF page 1 via fitz (raw image xref, no overlaid text), cropped 4:3 with PIL.
- Current item: Neon Flex In-Ground 2260 SV (PL-NS2260), v4.0, 13 pages, 3.8 MB (was `ATS.pdf.pdf` at root). PDF p13 prints UAE phone as "+970" (site has correct +971); user said ignore.
- Adding the section flipped backgrounds to keep alternation: Products=white, Brands=cream-2, Clients=white. Nav + footer have a Products link (nav still fits at 861px, just above the 860px drawer breakpoint).

## Rebranding supplier videos (cover their logo with ours)
- Done once: Potato Lighting "In-Ground Neon Flex Installation Tutorial" (WhatsApp mp4, 1024x576, 30fps, 208 s) → `products/neon-flex-in-ground-2260-install-video.mp4` (24 MB). The original WhatsApp file was deleted at the user's request. Poster = frame at 1.5 s → `products/neon-flex-in-ground-2260-video-poster.jpg`.
- Badge PNGs: `python3 agent-scripts/video_badge.py <H> <minW> out.png`. Title card used 94x416 at (24,18); small watermark on the rest used 62x214 (renders 240 wide) at (0,30).
- Find the title-card cut with `select='gt(scene,0.3)',showinfo` (was 3.033 s); switch badges with `enable='lt(t,T)'` / `gte(t,T)`.
- Encode 2-pass `-b:v 850k -preset slow -c:a copy -movflags +faststart` → 24 MB, which is under Cloudflare's 25 MiB per-file limit. CRF 18 gave 85 MB and CRF 25 gave 41 MB (the source is noisy), so don't use CRF.
- ffmpeg here has no `drawtext` (no freetype). Draw text in PIL. Keep the pill alpha at 255, because alpha 250 let the old logo ghost through.
- **wrangler serves the repo root**, so any `.mp4` left in the root deploys publicly unless it is listed in `.assetsignore`.

## Toolchain available
python3 has PyMuPDF (`fitz`) for PDF→PNG and Playwright (chromium launches OK). `sips`, `qlmanage` present. No poppler/imagemagick. brew + node available. To re-convert the PDF: use fitz to render pages at ~2x zoom to `source-material/pages/`.

## Workflow reminders for this repo
- **Branch is `main` (not master). A collaborator (GitHub `tcr233036`, "TCR") also edits `index.html` via PRs merged on GitHub** — e.g. added #news section (after #organization, bg-cream), a welcome popup (`#welcome-popup`, z-index 2000, shows on load — remove it in Playwright before screenshots), India address change. Run `git fetch && git status` before starting work so local doesn't diverge. Nav now has 8 links (… Products … Organization, News, Contact); still fits at 861px.
- **You cannot judge alignment/layout from the code alone.** After any visual change, run `agent-scripts/shoot.py` (desktop 1366 + mobile 390), read the PNGs back, and eyeball them. Only then is it "verified". The user reviews the final result only, so this self-check is on you.
- Use subagents for fan-out work.
- `.assetsignore` keeps `source-material/`, `agent-scripts/`, and this file out of the public Cloudflare deploy. This file + `agent-scripts/shoot.py` ARE committed to git so future sessions inherit them; `agent-scripts/shots/` and `source-material/` are gitignored.
