"""Native procedural source beside photo and shipped export; bake-loss review."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from look_matches import FINISHES
from look_review import panel,stats
from kit.fonts import find_font

def main():
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48);a=p.parse_args()
    out=BASE/'renders/final/source';out.mkdir(parents=True,exist_ok=True)
    source=BASE/'build/delivery/high.blend';digest=hashlib.sha256(source.read_bytes()).hexdigest()
    export=json.loads((BASE/'renders/final/photos/shots.json').read_text());current=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
    from photo_render import render
    widths={name:Image.open(BASE/'renders/final/photos'/(name+'.png')).width for name in export}
    render(source,out,a.samples,source_diagnostic=True,widths=widths)
    current=json.loads((out/'shots.json').read_text());ids={n:int(i) for i,n in json.loads((BASE/'build/look-part-ids.json').read_text()).items()}
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),21);rows={}
    for name,row in FINISHES.items():
        shot=row['shot'];s=current[shot];e=export[shot]
        for key in ('location','target','lens','exposure','aspect','roll','shift_x','shift_y','look_light','look_world','look_world_color','look_paper','look_paper_x','look_reflection_card','look_light_colors','look_strips','look_flags'):
            assert s.get(key)==e.get(key),(name,key)
        labels=np.asarray(Image.open(BASE/'renders/final/cpu-masks'/(shot+'.png')))
        selected=np.isin(labels[:,:,0],[ids[n] for n in row['parts']])&(labels[:,:,3]>250)
        yy,xx=np.nonzero(selected);box=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1))
        native=Image.open(out/(shot+'.png'));baked=Image.open(BASE/'renders/final/photos'/(shot+'.png'))
        photo=Image.open(BASE/'build/look-photos'/(row['photo']+'.png'))
        sheet=Image.new('RGB',(1800,650),(230,231,227));d=ImageDraw.Draw(sheet)
        d.text((15,10),name+' / procedural source — balanced photograph — exported 2048 atlas',font=font,fill='black')
        for i,(im,bb) in enumerate(((native,box),(photo,row['crop']),(baked,box))):sheet.paste(panel(im,bb,(580,480)),(10+i*600,50))
        delta=np.abs(np.array(native.convert('RGB'),dtype=float)-np.array(baked.convert('RGB'),dtype=float))[selected]
        rows[name]=dict(source_sha256=digest,export_sha256=e['sha256'],
            photo_camera_sha256=e['photo_camera_sha256'],photo_renderer_sha256=e['photo_renderer_sha256'],
            mean_absolute_rgb_difference=delta.mean(0).tolist(),
            p95_max_rgb_difference=float(np.percentile(delta.max(1),95)),
            source_values=stats(np.asarray(native.convert('RGB'))[np.asarray(Image.fromarray(np.uint8(selected)*255).filter(ImageFilter.MinFilter(3)))>0]),
            export_values=stats(np.asarray(baked.convert('RGB'))[np.asarray(Image.fromarray(np.uint8(selected)*255).filter(ImageFilter.MinFilter(3)))>0]),note='Image bake-loss diagnostic; a low difference proves consistency, not photographic correctness.')
        d.text((15,550),'Same physical illumination/camera; source bump versus actual shipped normal, color and ORM.',font=font,fill='black')
        d.text((15,585),'Source/export RGB mean absolute difference: '+str(np.round(delta.mean(0),2).tolist()),font=font,fill='black')
        sheet.save(out/(name+'-source-photo-export.jpg'),quality=94,optimize=True)
    (out/'bake-loss.json').write_text(json.dumps(rows,indent=2));print('SOURCE/PHOTO/EXPORT',len(rows))
    subprocess.run([sys.executable,str(BASE/'src/look_review.py'),'--folder',str(BASE/'renders/final')],check=True)
if __name__=='__main__':main()
