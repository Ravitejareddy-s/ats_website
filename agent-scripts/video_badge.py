"""Build the white A2S pill badge (logo | A2S / TECHNICAL SERVICES) as a PNG for ffmpeg overlay.

Usage: python3 agent-scripts/video_badge.py <height_px> <min_width_px> <out.png>
Example (1024x576 video): 94 416 badge_title.png   and   62 214 badge_small.png
Pill is fully opaque (alpha 255); any lower alpha lets the covered logo ghost through.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logo = Image.open(os.path.join(ROOT, 'logo.jpg')).convert('RGBA')
# logo.jpg has alpha with faint noise near the edges; threshold before trimming to the real mark
logo = logo.crop(logo.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
F = '/System/Library/Fonts/Avenir Next.ttc'              # index 2 = Demi Bold, 5 = Medium


def badge(H, minW, path, S=4):
    H2 = H * S; m = int(H2 * 0.12)                         # outer margin for shadow
    ih = H2 - 2 * m
    f1 = ImageFont.truetype(F, int(ih * 0.34), index=2)
    f2 = ImageFont.truetype(F, int(ih * 0.165), index=5)
    lh = int(ih * 0.78); lw = int(logo.size[0] * lh / logo.size[1])
    padL = int(ih * 0.36); gap = int(ih * 0.20)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    t2 = 'TECHNICAL SERVICES'
    tw = max(tmp.textlength('A2S', font=f1), tmp.textlength(t2, font=f2) + (len(t2) - 1) * ih * 0.012)
    inner = padL + lw + gap * 2 + tw + int(ih * 0.42)
    W2 = max(int(inner) + 2 * m, minW * S); W = W2 // S; W2 = W * S
    x0, y0, x1, y1 = m, m, W2 - m, H2 - m
    extra = int((x1 - x0 - inner) // 2)                    # centre content if minW made it wider
    im = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
    sh = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + S * 2, x1, y1 + S * 2), radius=int(ih * 0.30), fill=(0, 0, 0, 85))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(S * 2.5)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, y0, x1, y1), radius=int(ih * 0.30), fill=(255, 255, 255, 255))
    lx = x0 + padL + extra; ly = y0 + (ih - lh) // 2
    im.alpha_composite(logo.resize((lw, lh), Image.LANCZOS), (lx, ly))
    dx = lx + lw + gap
    d.line((dx, y0 + ih * 0.24, dx, y1 - ih * 0.24), fill=(201, 133, 47, 255), width=max(S, int(ih * 0.035)))
    tx = dx + gap
    d.text((tx, y0 + ih * 0.13), 'A2S', font=f1, fill=(41, 35, 27, 255))
    x = tx
    for ch in t2:                                          # letter-spaced caption
        d.text((x, y0 + ih * 0.60), ch, font=f2, fill=(165, 101, 27, 255))
        x += tmp.textlength(ch, font=f2) + ih * 0.012
    im.resize((W, H), Image.LANCZOS).save(path); print(path, (W, H))


if __name__ == '__main__':
    badge(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
