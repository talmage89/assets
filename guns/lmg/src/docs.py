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
    assert source.resolve() == (BASE / 'export/lmg.glb').resolve()
    assert row['sha256'] == hashlib.sha256(source.read_bytes()).hexdigest(), (folder, name, 'stale')
    PROVENANCE.append(dict(folder=folder, shot=name, source='export/lmg.glb',
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
    assert json.loads((BASE / 'build/delivery/verify.json').read_text())['passed']
    DOCS.mkdir(exist_ok=True)
    shots = {n: checked('beauty', n) for n in (
        'hero', 'front', 'side', 'back', 'top', 'cover_open_full', 'rear_sight',
        'barrel_handle', 'furniture', 'belt', 'aimed_macro', 'scale')}
    feed = checked('docs-feed', 'belt_laid')
    eevee = checked('eevee', 'hero', 'BLENDER_EEVEE')
    turnaround = sheet([(n.title(), shots[n]) for n in ('front', 'side', 'back', 'top')], OUT / 'turnaround.jpg')
    details = sheet([(label, shots[n]) for label, n in (
        ('Rear aperture and pressed sight ears', 'rear_sight'),
        ('Barrel, heat shield and carrying handle', 'barrel_handle'),
        ('Molded stock and grip', 'furniture'),
        ('Blackened links and brass', 'belt'))], OUT / 'details.jpg', (800, 600))
    action = sheet([
        ('Reload / cover open, belt on tray', shots['cover_open_full']),
        ('Reload / belt laid, frame 264', feed),
        ('Exact eye frame / sight macro', shots['aimed_macro']),
        ('Scale / 1.8 m silhouette', shots['scale'])], OUT / 'action.jpg', (800, 650))
    all_stills = [(name, checked('beauty', name))
                  for name in json.loads((OUT / 'beauty/shots.json').read_text())]
    sheet([*all_stills, ('Eevee hero', eevee), ('Reload / laid belt', feed)],
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
