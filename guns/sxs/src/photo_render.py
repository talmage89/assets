"""Photo evidence at approximately native projected-part pixel density.

Whole-gun, macro and small-control photographs have different native scales.
Keep the shipped 2048 atlas unchanged. Each camera uses one neutral physical
light rig; no photographic pixels or statistics alter rendered pixels.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path[:0]=[str(ROOT),str(BASE/'src')]
from look_matches import SHOTS
WIDTHS={'look_side':5977,'look_macro':2825,'look_muzzle':2560,'look_safety':512,'look_deep_blue':1555}

def render(source,out,samples=48,source_diagnostic=False,widths=None):
    widths=widths or WIDTHS
    source=Path(source).resolve();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    camera=BASE/'build/look-cameras.json';camera_digest=hashlib.sha256(camera.read_bytes()).hexdigest()
    h=hashlib.sha256(json.dumps(SHOTS,sort_keys=True).encode())
    for p in [BASE/'src/final_render.py',BASE/'src/final_shots.py',BASE.parent/'common/render.py',Path(__file__)]:h.update(p.read_bytes())
    renderer_digest=h.hexdigest()
    records=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
    for name,width in widths.items():
        old=records.get(name,{})
        valid=(old.get('sha256')==digest and old.get('samples_used')==samples and
            old.get('photo_camera_sha256')==camera_digest and old.get('photo_renderer_sha256')==renderer_digest and
            (out/(name+'.png')).exists() and Image.open(out/(name+'.png')).width==width)
        if not valid:
            log=BASE/'build'/('native-photo-'+out.name+'-'+name+'.log')
            args=[str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1',
                '--python',str(BASE/'src/final_render.py'),'--','--source',str(source),'--out',str(out),
                '--width',str(width),'--samples',str(samples),'--look','--camera-file',str(camera),'--shots',name]
            if source_diagnostic:args.append('--source-diagnostic')
            with log.open('w') as f:subprocess.run(args,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
            actual=json.loads((out/'shots.json').read_text())[name]
            actual.update(photo_camera_sha256=camera_digest,photo_renderer_sha256=renderer_digest,
                comparison_width=width,comparison_resolution_note='Approximately native projected-part scale; original 2048 texture images remain unchanged.')
            records[name]=actual
        (out/'shots.json').write_text(json.dumps(records,indent=2))
    assert set(records)==set(widths),set(records)
    print('PHOTO COMPARISON WIDTHS',widths,source.name,flush=True)
    return records

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--samples',type=int,default=48);p.add_argument('--source-diagnostic',action='store_true');a=p.parse_args()
    render(a.source,a.out,a.samples,a.source_diagnostic)
if __name__=='__main__':main()
