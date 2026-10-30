"""Reproducible, real-speed README GIFs from exported gun GLBs.

Ordinary Python drives Blender under the shared GPU lock, composites a flat
studio background, then uses ffmpeg's global palette and difference rectangles.
The Blender worker reuses common.render and the member's final_shots recipe.
A member supplies src/gif.json and includes ../common/gif.mk in its Makefile.
No source geometry, material overrides, text or artificial slow motion is used.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]


def timeline(spec, clips, source_fps):
    """Time sampling on half-open clip intervals, preserving exact playback time."""
    fps = spec['fps']
    if fps not in (20, 25):
        raise ValueError('GIF rate must be 20 or 25 Hz (integer centiseconds)')
    rows = []
    elapsed = 0
    for segment in spec['sequence']:
        clip = segment['clip']
        start = segment.get('start', 0)
        end = segment.get('end', clips[clip]['frames'])
        if not 0 <= start < end <= clips[clip]['frames']:
            raise ValueError(f'Invalid {clip} range {start}..{end}')
        # Segment boundaries lie on the output time grid. The next clip starts
        # at that boundary; adding an endpoint frame would lengthen playback.
        count = (end-start)*fps/source_fps
        if abs(count-round(count)) > 1e-7:
            raise ValueError('Trim endpoints must align with GIF sample times')
        for i in range(round(count)):
            rows.append(dict(action=clip, frame=start+i*source_fps/fps,
                             time_s=elapsed+i/fps))
        elapsed += (end-start)/source_fps
    return rows


def worker(base, spec, out, preview):
    import bpy
    sys.path[:0] = [str(ROOT), str(base/'src')]
    import final_shots
    import interface
    from guns.common.render import main as render
    rows = timeline(spec, interface.CLIPS, interface.FPS)
    picks = sorted(set([0, *[min(len(rows)-1, round(v*(len(rows)-1)))
                            for v in (.2, .4, .6, .8)], len(rows)-1])) if preview else range(len(rows))
    shots = {f'f{i:04d}': dict(spec['camera'], **rows[i], background='transparent') for i in picks}

    def configure(scene, source):
        # Some member recipes split named surfaces for diagnostics when the
        # input's basename is ak.glb. A byte-identical presentation copy avoids
        # that source-blend attribution path; all shipped triangles stay intact.
        final_shots.configure_scene(scene, source)
        if scene.render.engine == 'CYCLES':
            scene.cycles.seed = 0
            scene.cycles.use_animated_seed = False
            scene.cycles.use_adaptive_sampling = False
        scene.render.use_persistent_data = True
        scene.render.use_file_extension = True
        scene.render.image_settings.color_depth = '8'
        arm = next(o for o in scene.objects if o.type == 'ARMATURE')
        for segment in spec['sequence']:
            assert any(a.name == segment['clip'] for a in bpy.data.actions)
        assert any(n.type == 'TEX_IMAGE' for mat in bpy.data.materials if mat.use_nodes
                   for n in mat.node_tree.nodes), 'Baked GLB textures required'

    config = SimpleNamespace(FINAL_STAGE=True, RENDER_STAGE='README GIF / exported baked GLB',
        DEFAULT_SHOTS=','.join(shots), SHOTS=shots, PHOTO_POSES={},
        floor_height=final_shots.floor_height, configure_scene=configure,
        prepare_shot=final_shots.prepare_shot)
    source = out/'presentation.glb'
    source.write_bytes((base/spec['source']).read_bytes())
    sys.argv = [sys.argv[0], '--', '--source', str(source), '--out', str(out/'raw'),
                '--width', str(spec['width']), '--samples', str(spec['samples']),
                '--engine', 'BLENDER_WORKBENCH' if preview else 'CYCLES']
    render(config, interface)
    (out/'timeline.json').write_text(json.dumps(rows, indent=2))


def first_hold(path, centiseconds):
    """Add only a delay to the first GIF graphic-control extension, losslessly."""
    data = bytearray(path.read_bytes())
    assert data[:6] in (b'GIF87a', b'GIF89a')
    offset = 13 + (3*(2**((data[10]&7)+1)) if data[10]&128 else 0)
    while offset < len(data):
        if data[offset:offset+3] == b'!\xf9\x04':
            delay = struct.unpack_from('<H', data, offset+4)[0]
            struct.pack_into('<H', data, offset+4, delay+centiseconds)
            path.write_bytes(data)
            return
        assert data[offset] == 0x21, 'Expected extension before first image'
        offset += 2
        while data[offset]:
            offset += data[offset]+1
        offset += 1
    raise ValueError('GIF has no graphic-control extension')


def encode(base, spec, out):
    from PIL import Image, ImageDraw
    rows = json.loads((out/'timeline.json').read_text())
    source_digest = hashlib.sha256((base/spec['source']).read_bytes()).hexdigest()
    metadata = json.loads((out/'raw/shots.json').read_text())
    assert len(metadata) == len(rows), 'Full final render required; previews cannot be encoded'
    for i, row in enumerate(rows):
        shot = metadata[f'f{i:04d}']
        assert shot['engine'] == 'CYCLES' and shot['sha256'] == source_digest
        assert all(shot[k] == v for k,v in spec['camera'].items()), 'Camera changed since render'
        assert all(shot[k] == v for k,v in row.items()), 'Sampling changed since render'
    frames = out/'frames'; frames.mkdir(exist_ok=True)
    for stale in frames.glob('f*.png'):
        stale.unlink()
    for i in range(len(rows)):
        raw = Image.open(out/'raw'/f'f{i:04d}.png').convert('RGBA')
        bg = Image.new('RGBA', raw.size, (*spec['background'], 255))
        bg.alpha_composite(raw)
        bg.convert('RGB').save(frames/f'f{i:04d}.png')
    fps = spec['fps']
    ffmpeg = ['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-y', '-threads', '1',
              '-filter_threads', '1', '-filter_complex_threads', '1']
    input_args = ['-framerate', str(fps), '-i', str(frames/'f%04d.png')]
    subprocess.run([*ffmpeg, *input_args, '-vf',
        f"palettegen=max_colors={spec['colors']}:stats_mode=full:reserve_transparent=1",
        '-frames:v', '1', '-update', '1', str(out/'palette.png')], check=True)
    candidate = out/'motion.gif'
    subprocess.run([*ffmpeg, *input_args, '-i', str(out/'palette.png'), '-lavfi',
        'paletteuse=dither=none:diff_mode=rectangle', '-gifflags', '+offsetting+transdiff',
        '-loop', '0', '-final_delay', str(100//fps), str(candidate)], check=True)
    first_hold(candidate, 50)
    decoded = []
    durations = []
    with Image.open(candidate) as gif:
        palette = gif.getpalette()
        for i in range(gif.n_frames):
            gif.seek(i)
            durations.append(gif.info['duration'])
            decoded.append(gif.convert('RGB').copy())
        size = gif.size
    expected = [1000//fps]*len(rows); expected[0] += 500
    assert durations == expected, (durations, expected)
    assert size[0] <= 960 and candidate.stat().st_size <= 450_000, (
        'Tighten crop/trim moving span before reducing rate or palette', size, candidate.stat().st_size)
    # Every decoded frame gets an ignored, numbered native-width review page.
    review = out/'review'; review.mkdir(exist_ok=True)
    for start in range(0, len(decoded), 8):
        w, h = size
        page = Image.new('RGB', (2*w, 4*(h+24)), (225, 226, 222))
        draw = ImageDraw.Draw(page)
        for j, im in enumerate(decoded[start:start+8]):
            i = start+j; x = j%2*w; y = j//2*(h+24)
            page.paste(im, (x,y+24))
            row = rows[i]
            draw.text((x+8,y+5), f"{i:03d} | {row['action']} f{row['frame']:g} | {row['time_s']:.2f} s", fill='black')
        page.save(review/f'frames-{start:04d}.jpg', quality=94)
    # Small complete contact sheet for navigation, with native pages above.
    thumb_w = 320; thumb_h = round(size[1]*thumb_w/size[0])
    contact = Image.new('RGB', (thumb_w*4, math.ceil(len(decoded)/4)*(thumb_h+20)), (225,226,222))
    draw = ImageDraw.Draw(contact)
    for i,im in enumerate(decoded):
        x=i%4*thumb_w; y=i//4*(thumb_h+20)
        contact.paste(im.resize((thumb_w,thumb_h),Image.Resampling.LANCZOS),(x,y+20))
        draw.text((x+5,y+3),f'{i:03d} / {rows[i]["time_s"]:.2f}s',fill='black')
    contact.save(out/'contact-sheet.jpg',quality=94)
    source = base/spec['source']
    report = dict(path=spec['output'], source=spec['source'], source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        sequence=spec['sequence'], camera=spec['camera'], size=list(size), frames=len(decoded), fps=fps,
        palette_limit=spec['colors'], palette_colors=len(set(tuple(palette[i:i+3]) for i in range(0,len(palette),3))),
        bytes=candidate.stat().st_size, duration_ms=sum(durations), first_hold_ms=500,
        frame_durations_ms=durations, samples=rows, engine='CYCLES', render_samples=spec['samples'],
        dither='none', palette='global', ffmpeg_version=subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
        gif_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest())
    (out/'report.json').write_text(json.dumps(report,indent=2))
    dest = base/spec['output']; dest.parent.mkdir(exist_ok=True)
    dest.write_bytes(candidate.read_bytes())
    (out/'playback.html').write_text(
        '<!doctype html><meta charset="utf-8"><title>Signature motion / 1x</title>'
        '<style>body{margin:0;background:#222;display:grid;place-items:center;min-height:100vh}'
        'img{max-width:100%;height:auto}</style>'
        '<img src="../../docs/motion.gif" alt="Signature motion at authored speed">')
    print(json.dumps({k:report[k] for k in ('path','size','frames','fps','palette_colors','bytes','gif_sha256')},indent=2))


def main():
    args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--asset', type=Path, default=Path.cwd())
    p.add_argument('--render', action='store_true')
    p.add_argument('--preview', action='store_true')
    p.add_argument('--encode-only', action='store_true')
    p.add_argument('--blender', default='blender')
    a = p.parse_args(args)
    base = a.asset.resolve()
    spec = json.loads((base/'src/gif.json').read_text())
    out = base/'build/gif'; out.mkdir(parents=True,exist_ok=True)
    if a.render:
        worker(base,spec,out,a.preview)
    else:
        if not a.encode_only:
            cmd = [a.blender, '-b', '--factory-startup',
                   '--python-exit-code', '1', '--python', str(Path(__file__).resolve()),
                   '--', '--asset', str(base), '--render', *(['--preview'] if a.preview else [])]
            if not a.preview:
                cmd = [str(ROOT/'kit/with_gpu.sh'), *cmd]
            with (out/'render.log').open('w') as log:
                subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True,
                               env={**os.environ,'TMPDIR':str(ROOT/'build/tmp')})
        if not a.preview:
            encode(base,spec,out)


if __name__ == '__main__':
    main()
