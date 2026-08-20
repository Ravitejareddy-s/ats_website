# AGENT NOTES — ats_website

Agent-maintained context. Not for human docs. Keep terse; update when you learn something a future session would waste tokens rediscovering.also delete if you feel something is unnessasary that task is done or the future agents dosent need that info its just waste of tokens 

## What this is
Single-file marketing site for **A2S Technical Services** (aka ATS / Ark Design Studio) — a UAE lighting + technical-services company. Everything lives in `index.html` (inline `<style>`, no build step). Deployed to Cloudflare via `wrangler.jsonc` (static assets, serves repo root).

## Layout of index.html
Sections in order: nav → hero → about → mission/vision → services → brands → clients → organization (org chart) → contact → footer. All CSS is one inline `<style>` block; responsive breakpoints at 900px and 560px.

## Design system
- Palette: cream (`--cream-1 #f7f2e8`, `--cream-2`, `--cream-3`), ink `#29231b`, amber (`#e2a04c`/`#c9852f`/`#a5651b`).
- Fonts: Bricolage Grotesque (headings), Fraunces italic (accent), Inter (body).
- Assets committed at root: `logo.jpg`, `skyline.jpg`.
- We deliberately kept the softer amber aesthetic instead of the PDF's brighter orange (`#f26a21`) for cohesion.

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

## source-material/ (gitignored + assetsignored — NOT committed, NOT served)
- `A2S PDF (1).pdf` = company profile, source of truth for all copy.
- `pages/page-01..10.png` = the PDF rendered to images (each PDF page is a slide). Read these images to re-extract info.

## Toolchain available
python3 has PyMuPDF (`fitz`) for PDF→PNG and Playwright (chromium launches OK). `sips`, `qlmanage` present. No poppler/imagemagick. brew + node available. To re-convert the PDF: use fitz to render pages at ~2x zoom to `source-material/pages/`.

## Workflow reminders for this repo
- **You cannot judge alignment/layout from the code alone.** After any visual change, run `agent-scripts/shoot.py` (desktop 1366 + mobile 390), read the PNGs back, and eyeball them. Only then is it "verified". The user reviews the final result only, so this self-check is on you.
- Use subagents for fan-out work.
- `.assetsignore` keeps `source-material/`, `agent-scripts/`, and this file out of the public Cloudflare deploy. This file + `agent-scripts/shoot.py` ARE committed to git so future sessions inherit them; `agent-scripts/shots/` and `source-material/` are gitignored.
