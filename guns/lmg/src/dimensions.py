"""Dimensioned orthographic evidence, using measured bounds and camera scale."""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from kit.fonts import find_font

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'renders/checkpoint'
geometry = json.loads((BASE / 'build/check.json').read_text())['geometry']
shots = json.loads((OUT / 'shots.json').read_text())
lo, hi = geometry['bounds_mm']
font = ImageFont.truetype(find_font('Noto Sans', 'Regular'), 24)
small = ImageFont.truetype(find_font('Noto Sans', 'Regular'), 19)
ink, line, paper = (22, 46, 44), (69, 112, 106), (237, 239, 234)
panels = []

for name, horizontal, vertical, signs in [
    ('side', 1, 2, (1, 1)), ('top', 1, 0, (1, -1)),
    ('front', 0, 2, (-1, 1))]:
    raw = Image.open(OUT / (name + '.png')).convert('RGB')
    w, h = raw.size
    left, top = 180, 64
    panel = Image.new('RGB', (w + left + 44, h + top + 120), paper)
    panel.paste(raw, (left, top))
    d = ImageDraw.Draw(panel)
    s = shots[name]
    scale = w / (s['ortho'] * 1000)
    target = [v * 1000 for v in s['target']]
    def xpos(v):
        return left + w / 2 + signs[0] * (v - target[horizontal]) * scale
    def ypos(v):
        return top + h / 2 - signs[1] * (v - target[vertical]) * scale
    x0, x1 = sorted((xpos(lo[horizontal]), xpos(hi[horizontal])))
    y0, y1 = sorted((ypos(lo[vertical]), ypos(hi[vertical])))
    # Witness lines share the orthographic projection's measured endpoints.
    ybar, xbar = top + h + 34, left - 28
    for x in (x0, x1):
        d.line((x, y1, x, ybar + 8), fill=line, width=1)
        d.line((x - 7, ybar - 7, x + 7, ybar + 7), fill=ink, width=2)
    d.line((x0, ybar, x1, ybar), fill=ink, width=2)
    label = f'{hi[horizontal] - lo[horizontal]:.2f} mm'
    d.text(((x0 + x1) / 2, ybar + 11), label, font=font, fill=ink, anchor='mt')
    for y in (y0, y1):
        d.line((xbar - 8, y, x0, y), fill=line, width=1)
        d.line((xbar - 7, y - 7, xbar + 7, y + 7), fill=ink, width=2)
    d.line((xbar, y0, xbar, y1), fill=ink, width=2)
    d.text((12, (y0 + y1) / 2), f'{hi[vertical] - lo[vertical]:.2f} mm',
           font=font, fill=ink, anchor='lm')
    d.text((left, 13), f'{name.title()} | exported GLB | measured exterior envelope',
           font=font, fill=ink)
    d.text((left, panel.height - 29), 'Inspection constants; stowed bipod and loaded belt. See sections for individual walls.',
           font=small, fill=ink)
    panel.save(OUT / (name + '-dimensions.png'))
    panel.thumbnail((1600, 1600))
    panels.append(panel)

sheet = Image.new('RGB', (1600, sum(p.height for p in panels)), paper)
y = 0
for panel in panels:
    sheet.paste(panel, (0, y))
    y += panel.height
sheet.save(OUT / 'orthographic-dimensions.jpg', quality=92, optimize=True)
print('DIMENSIONS', geometry['dimensions_mm'], 'mm')
