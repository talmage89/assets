"""Build the five final README JPGs from hash-verified baked-GLB renders."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import sys
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE.parents[1]))
from kit.fonts import find_font
FONT = ImageFont.truetype(find_font('Noto Sans', 'Regular'), 20)
OUT = BASE / 'renders/final'
DOCS = BASE / 'docs'
PROVENANCE = []


def checked(folder, name, engine='CYCLES'):
    row = json.loads((OUT / folder / 'shots.json').read_text())[name]
    source = Path(row['source'])
    assert source.suffix == '.glb' and row['engine'] == engine
    assert source.resolve() == (BASE / 'export/sxs.glb').resolve()
    assert row['sha256'] == hashlib.sha256(source.read_bytes()).hexdigest(), (folder, name, 'stale')
    PROVENANCE.append(dict(folder=folder, shot=name, source='export/sxs.glb',
                           sha256=row['sha256'], engine=engine,
                           action=row.get('action'), frame=row.get('frame')))
    return OUT / folder / (name + '.png')


def panel(path, size):
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGBA', im.size, (108, 111, 114, 255))
    bg.alpha_composite(im)
    return ImageOps.contain(bg.convert('RGB'), size, Image.Resampling.LANCZOS)


def sheet(entries, path, cell=(800, 520), columns=2):
    w, h = cell
    im = Image.new('RGB', (columns * w, h * ((len(entries) + columns - 1) // columns)), (231, 233, 230))
    draw = ImageDraw.Draw(im)
    for i, (caption, source) in enumerate(entries):
        x, y = i % columns * w, i // columns * h
        draw.text((x + 12, y + 9), caption, font=FONT, fill=(25, 35, 30))
        tile = panel(source, (w - 12, h - 48))
        im.paste(tile, (x + (w - tile.width) // 2, y + 40 + (h - 48 - tile.height) // 2))
    im.save(path, quality=94, optimize=True)
    return path


def main():
    assert json.loads((BASE / 'build/serialization.json').read_text())['passed']
    DOCS.mkdir(exist_ok=True)
    shots = {n: checked('beauty', n) for n in (
        'hero', 'front', 'side', 'back', 'top', 'open', 'breech', 'action',
        'stock', 'forend', 'top_controls', 'muzzle', 'aimed', 'scale', 'open_side')}
    eevee = checked('eevee', 'hero', 'BLENDER_EEVEE')
    turnaround = sheet([(n.title(), shots[n]) for n in ('front', 'side', 'back', 'top')], OUT / 'docs-turnaround.jpg')
    details = sheet([(label, shots[n]) for label, n in (
        ('Faded case colors and rust-blued barrels', 'action'),
        ('Oil walnut and worn wrist checkering', 'stock'),
        ('Splinter forend and cut borders', 'forend'),
        ('Top lever and automatic tang safety', 'top_controls'))], OUT / 'docs-details.png', (800, 600))
    action_top = sheet([
        ('Open / extractors raised, fired hulls retained', shots['open']),
        ('Open / live shells on the extractor', shots['breech'])],
        OUT / 'docs-action-top.png', (800, 600))
    action_bottom = sheet([('Side / barrels at the full 42-degree opening', shots['open_side'])],
        OUT / 'docs-action-bottom.png', (1600, 600), columns=1)
    action = OUT / 'docs-action.png'
    action_image = Image.new('RGB', (1600, 1200))
    action_image.paste(Image.open(action_top), (0, 0))
    action_image.paste(Image.open(action_bottom), (0, 600))
    action_image.save(action, quality=94, optimize=True)
    all_stills = [(name, checked('beauty', name))
                  for name in json.loads((OUT / 'beauty/shots.json').read_text())]
    sheet([*all_stills, ('Eevee hero', eevee)],
          OUT / 'docs-contact-sheet.jpg', (400, 320), columns=4)
    result = {}
    for name, source in [('hero', shots['hero']), ('turnaround', turnaround),
                         ('action', action), ('details', details), ('eevee', eevee)]:
        im = panel(source, (1600, 1400))
        for quality in range(94, 59, -3):
            dest = DOCS / (name + '.jpg')
            im.save(dest, quality=quality, optimize=True)
            if dest.stat().st_size <= 200_000:
                break
        assert dest.stat().st_size <= 200_000 and im.width <= 1600
        result[name] = dict(pixels=list(im.size), bytes=dest.stat().st_size,
                            quality=quality, sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
    (BASE / 'build/docs-report.json').write_text(json.dumps(
        dict(outputs=result, sources=PROVENANCE), indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
