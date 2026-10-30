"""Rebuildable 30-Hz port/cutaway evidence with exact-duration playback."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from kit.fonts import find_font


def _run(base, manifest):
    p=argparse.ArgumentParser()
    p.add_argument('--before', action='store_true')
    p.add_argument('--clips')
    p.add_argument('--width', type=int, default=560)
    a=p.parse_args()
    gun=base.name
    source=base/(f'build/feed-before/{gun}.glb' if a.before else f'export/{gun}.glb')
    reference=base/('build/feed-before/finalized.blend' if a.before else 'build/delivery/finalized.blend')
    out=base/'renders/feed'/('before' if a.before else 'after')
    out.mkdir(parents=True,exist_ok=True)
    clips=a.clips.split(',') if a.clips else [n for n in manifest.CLIPS if n.startswith(('Fire','Cycle','Reload')) or n in ('Chamber','Inspect')]
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    renderer_digest=hashlib.sha256((ROOT/'guns/common/feed_views.py').read_bytes()+(base/'src/cycle_views.py').read_bytes()).hexdigest()
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
    report={}
    for clip in clips:
        for cutaway in (False,True):
            name=clip+('-cutaway' if cutaway else '-port')
            folder=out/name;folder.mkdir(exist_ok=True)
            metadata=folder/'shots.json'
            current=json.loads(metadata.read_text()) if metadata.exists() else {}
            if not current or any(r['sha256']!=digest or r.get('renderer_sha256')!=renderer_digest for r in current.values()):
                cmd=[str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1',
                    '--python',str(base/'src/cycle_views.py'),'--','--source',str(source),'--reference',str(reference),
                    '--out',str(folder),'--engine','BLENDER_EEVEE','--width',str(a.width),'--samples','12','--clip',clip]
                if cutaway:cmd.append('--cutaway')
                with (folder/'render.log').open('w') as log:
                    subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT,cwd=ROOT)
                current=json.loads(metadata.read_text())
            frames=[r['frame'] for r in current.values()]
            wanted=list(range(0,manifest.CLIPS[clip]['frames']+1,2))
            if wanted[-1]!=manifest.CLIPS[clip]['frames']:wanted.append(manifest.CLIPS[clip]['frames'])
            assert frames==wanted,(clip,frames)
            play=[];panels=[]
            for shot,row in current.items():
                rgba=Image.open(folder/(shot+'.png')).convert('RGBA')
                bg=Image.new('RGBA',rgba.size,(58,61,65,255));bg.alpha_composite(rgba)
                raw=bg.convert('RGB');play.append(raw)
                panel=Image.new('RGB',(a.width,raw.height+28),(229,230,226));panel.paste(raw,(0,28))
                ImageDraw.Draw(panel).text((8,3),f'{clip}  f{row["frame"]:g}  {"SECTION" if cutaway else "PORT"}',font=font,fill=(22,28,25))
                panels.append(panel)
            # Full strips retain every sample. Inspection pages keep the
            # native action pixels large enough to inspect all rendered frames.
            height=panels[0].height
            sheet=Image.new('RGB',(a.width*3,height*((len(panels)+2)//3)),(229,230,226))
            for i,panel in enumerate(panels):sheet.paste(panel,(a.width*(i%3),height*(i//3)))
            sheet.save(out/(name+'.jpg'),quality=90,optimize=True)
            for page,start in enumerate(range(0,len(panels),12)):
                selected=panels[start:start+12]
                page_image=Image.new('RGB',(a.width*3,height*((len(selected)+2)//3)),(229,230,226))
                for i,panel in enumerate(selected):page_image.paste(panel,(a.width*(i%3),height*(i//3)))
                page_image.save(folder/f'inspect-{page:02d}.jpg',quality=90,optimize=True)
            times=[round(f/60*1000) for f in frames]
            durations=[b-c for c,b in zip(times,times[1:])]
            playback=out/(name+'.webp')
            play[0].save(playback,save_all=True,append_images=play[1:-1],duration=durations,loop=0,quality=86)
            with Image.open(playback) as encoded:
                actual=0
                for i in range(encoded.n_frames):
                    encoded.seek(i);encoded.load();actual+=encoded.info.get('duration',0)
            assert actual==times[-1],(clip,actual,times[-1])
            report[name]=dict(clip=clip,rate_hz=30,frames=frames,decoded_duration_ms=actual,
                              source_sha256=digest,cutaway=cutaway)
            print('FEED STRIP',gun,name,len(panels),'frames',flush=True)
            (out/'timing.json').write_text(json.dumps(report,indent=2)+'\n')


def main(base, manifest):
    # Like the family's final strip renderer, hold one shared lease for the
    # short Eevee batch; child guards use a nested worktree-local lease.
    import fcntl
    shared=Path(os.environ['ASSETS_GPU_LOCK']);shared.parent.mkdir(parents=True,exist_ok=True)
    (base/'build').mkdir(exist_ok=True)
    with shared.open('a') as lease:
        fcntl.flock(lease,fcntl.LOCK_EX)
        os.environ['ASSETS_GPU_LOCK']=str(base/'build/feed-strip-inner.lock')
        _run(base,manifest)

