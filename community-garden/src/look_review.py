"""Local look-dev evidence: same-camera changes, plant photographs and costs."""
import argparse,json,hashlib,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.fonts import find_font
FONT=find_font('Noto Sans')

def pair(a,b,out,title,left,right,width=1200):
    a,b=map(lambda p:Image.open(p).convert('RGB'),(a,b));h=max(round(a.height*width/a.width),round(b.height*width/b.width))
    canvas=Image.new('RGB',(width*2,h+90),(232,234,228));d=ImageDraw.Draw(canvas);font=ImageFont.truetype(FONT,24)
    d.text((18,8),title,font=font,fill=(22,31,22));d.text((18,45),left,font=font,fill=(22,31,22));d.text((width+18,45),right,font=font,fill=(22,31,22))
    for j,im in enumerate((a,b)):
        im.thumbnail((width,h),Image.Resampling.LANCZOS);canvas.paste(im,(j*width+(width-im.width)//2,90+(h-im.height)//2))
    canvas.save(out,quality=94,optimize=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/lookdev');a=p.parse_args();out=Path(a.out);(out/'comparisons').mkdir(parents=True,exist_ok=True)
    old=Path('build/lookdev-before/renders')
    for seed in (117,229,341):
        if not (old/str(seed)/'hero.png').exists():continue
        before=json.loads((old/str(seed)/'hero.json').read_text())['camera'];after=json.loads((out/str(seed)/'before-camera.json').read_text())['camera']
        for key in ('location','target','lens','aspect'):assert np.allclose(before[key],after[key]),('Historical camera differs',seed,key)
        pair(old/str(seed)/'hero.png',out/str(seed)/'before-camera.png',out/'comparisons'/f'{seed}-before-after.jpg',f'{seed} / same lens and camera pose','Accepted construction checkpoint','Dense planting and baked look-dev')
    balances={};balanced=Path('build/plant-photo-balance');balanced.mkdir(parents=True,exist_ok=True)
    regions={'tomato':(.93,.50,.97,.54),'squash':(.80,.91,.89,.96)}
    for sp in ('tomato','squash','bean','corn','marigold'):
        im=ImageOps.exif_transpose(Image.open(Path('refs')/(sp+'.jpg'))).convert('RGB');arr=np.array(im,dtype=float)/255;lin=np.where(arr<=.04045,arr/12.92,((arr+.055)/1.055)**2.4);gains=np.ones(3)
        if sp in regions:
            x0,y0,x1,y1=regions[sp];patch=lin[round(y0*im.height):round(y1*im.height),round(x0*im.width):round(x1*im.width)];neutral=np.median(patch,axis=(0,1));gains=neutral.mean()/np.maximum(neutral,1e-6)
            lin*=gains
        arr=np.where(lin<=.0031308,lin*12.92,1.055*np.maximum(lin,0)**(1/2.4)-.055);photo=balanced/(sp+'.jpg');Image.fromarray(np.uint8(np.clip(arr,0,1)*255)).save(photo,quality=97)
        balances[sp]=dict(region_fraction=regions.get(sp),gains=gains.tolist(),neutral={'tomato':'concrete walkway at right, assumed neutral','squash':'black weed cloth at lower right, assumed neutral'}.get(sp,'No trustworthy neutral: morphology only; no numerical color calibration claimed'))
        pair(out/'plants'/(sp+'.png'),photo,out/'comparisons'/(sp+'-photo.jpg'),sp+' / original exported specimen and botanical photograph','Cycles / unchanged exported maps','Photo / morphology; lighting and scale differ')
    (balanced/'balance.json').write_text(json.dumps(balances,indent=2))
    rows={}
    for seed in (117,229,341):
        data=json.loads(Path(f'build/garden-{seed}.json').read_text());p=Path(f'export/final/Garden_{seed}.gltf');d=json.loads(p.read_text());images=[]
        for im in d['images']:
            path=p.parent/im['uri'];w,h=Image.open(path).size;images.append(dict(uri=im['uri'],size=[w,h],bytes=path.stat().st_size))
        rows[str(seed)]=dict(triangles=data['triangles'],plants=sum(len(q['plants']) for q in data['plan']['plots']),materials=len(d['materials']),gltf_bytes=p.stat().st_size,bin_bytes=p.with_suffix('.bin').stat().st_size,texture_mib=sum(i['size'][0]*i['size'][1]*4/3 for i in images)/2**20,images=images)
    (out/'costs.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
