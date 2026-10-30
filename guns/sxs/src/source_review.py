"""Native procedural source beside photo and shipped export; bake-loss review."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from look_matches import FINISHES
from look_review import panel
from kit.fonts import find_font

def main():
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48);a=p.parse_args()
    out=BASE/'renders/final/source';out.mkdir(parents=True,exist_ok=True)
    source=BASE/'build/delivery/high.blend';digest=hashlib.sha256(source.read_bytes()).hexdigest()
    export=json.loads((BASE/'renders/final/photos/shots.json').read_text());current=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
    deps=[BASE/'src/final_shots.py',BASE/'build/look-cameras.json']
    stale=(out/'look_side.png').exists() and (out/'look_side.png').stat().st_mtime<max(p.stat().st_mtime for p in deps)
    if not current or not (out/'look_side.png').exists() or stale or any(r['sha256']!=digest for r in current.values()) or Image.open(out/'look_side.png').width!=a.width:
        with (BASE/'build/source-render.log').open('w') as log:
            subprocess.run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/final_render.py'),
                '--','--source-diagnostic','--source',str(source),'--out',str(out),'--width',str(a.width),'--samples',str(a.samples),'--look',
                '--camera-file',str(BASE/'build/look-cameras.json'),'--shots','look_side,look_macro,look_muzzle,look_safety'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    current=json.loads((out/'shots.json').read_text());ids={n:int(i) for i,n in json.loads((BASE/'build/look-part-ids.json').read_text()).items()}
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),21);rows={}
    for name,row in FINISHES.items():
        shot=row['shot'];s=current[shot];e=export[shot]
        for key in ('location','target','lens','exposure','look_light'):assert s[key]==e[key],(name,key)
        labels=np.asarray(Image.open(BASE/'renders/final/cpu-masks'/(shot+'.png')))
        selected=np.isin(labels[:,:,0],[ids[n] for n in row['parts']])&(labels[:,:,3]>250)
        yy,xx=np.nonzero(selected);box=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1))
        native=Image.open(out/(shot+'.png'));baked=Image.open(BASE/'renders/final/photos'/(shot+'.png'))
        photo=Image.open(BASE/'build/look-photos'/(row['photo']+'.png'))
        sheet=Image.new('RGB',(1800,650),(230,231,227));d=ImageDraw.Draw(sheet)
        d.text((15,10),name+' / procedural source — balanced photograph — exported 2048 atlas',font=font,fill='black')
        for i,(im,bb) in enumerate(((native,box),(photo,row['crop']),(baked,box))):sheet.paste(panel(im,bb,(580,480)),(10+i*600,50))
        delta=np.abs(np.array(native.convert('RGB'),dtype=float)-np.array(baked.convert('RGB'),dtype=float))[selected]
        rows[name]=dict(source_sha256=digest,export_sha256=e['sha256'],mean_absolute_rgb_difference=delta.mean(0).tolist(),
            p95_max_rgb_difference=float(np.percentile(delta.max(1),95)),note='Image bake-loss diagnostic; a low difference proves consistency, not photographic correctness.')
        d.text((15,550),'Same physical illumination/camera; source bump versus actual shipped normal, color and ORM.',font=font,fill='black')
        d.text((15,585),'Source/export RGB mean absolute difference: '+str(np.round(delta.mean(0),2).tolist()),font=font,fill='black')
        sheet.save(out/(name+'-source-photo-export.jpg'),quality=94,optimize=True)
    (out/'bake-loss.json').write_text(json.dumps(rows,indent=2));print('SOURCE/PHOTO/EXPORT',len(rows))
if __name__=='__main__':main()
