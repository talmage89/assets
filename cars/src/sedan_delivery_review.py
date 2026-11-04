"""Final GLB provenance, tonal audit, gallery sheets and bounded sedan docs."""
import argparse,json,hashlib,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sedan_detail_review as R
ROOT=Path(__file__).resolve().parents[1]

def doc(src,dst):
    im=R.rgb(src);im.thumbnail((1600,12000),Image.Resampling.LANCZOS)
    for q in range(93,43,-2):
        im.save(dst,quality=q,optimize=True)
        if dst.stat().st_size<=200000:return
    raise ValueError('Doc exceeds budget: '+str(dst))

def diagnostic_sheet(folder):
    folder=Path(folder)
    from kit.fonts import find_font
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
    for name in ['front_three_quarter','rear_three_quarter','side','front','rear']:
        images=[R.rgb(folder/(name+'-'+mode+'.png')) for mode in ['curvature','horizontal','vertical']]
        w=1200;h=round(w*images[0].height/images[0].width)
        canvas=Image.new('RGB',(w*3,h+70),(235,237,233));draw=ImageDraw.Draw(canvas)
        for i,(im,label) in enumerate(zip(images,['Actual triangle mean curvature H','Horizontal reflection bands','Vertical reflection bands'])):
            canvas.paste(im.resize((w,h)),(i*w,40));draw.text((i*w+15,8),label,font=font,fill=(30,35,35))
        draw.text((15,h+44),'Fixed H scale [1/m]: purple -20 / blue -5 / cyan -1 / green 0 / yellow +1 / orange +5 / red +20; gray: boundary and gauge',font=font,fill=(30,35,35))
        canvas.save(folder/(name+'-comparison.jpg'),quality=93,optimize=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');p.add_argument('--diagnostics');a=p.parse_args()
    if a.diagnostics:diagnostic_sheet(a.diagnostics);return
    root=ROOT/'renders/sedan-detail';folders=[root,ROOT/'renders/sedan-used-pairs',ROOT/'renders/sedan-eevee',ROOT/'renders/sedan-motion']
    digest=hashlib.sha256((ROOT/'export/AlderS240.glb').read_bytes()).hexdigest();rows=[]
    for folder in folders:
        meta,_=R.tone(folder);rows+=list(meta.values())
    if any(r['source_sha256']!=digest or r['stage']!='final exported GLB' for r in rows):raise ValueError('Final gallery uses a stale or non-GLB source')
    if len({r['render_recipe_sha256'] for r in rows})!=1:raise ValueError('Mixed presentation recipe')
    names=['front_three_quarter','rear_three_quarter','front','side','rear','top','face','lamp_unlit','lamp_lit','wheel','mirror','interior_glass','underbody','underbody_layout','opened_front','opened_rear','scale']
    R.sheet([root/(n+'.png') for n in names]+[ROOT/'renders/sedan-eevee/front_three_quarter.png'],root/'contact.jpg',3,1800)
    R.sheet([root/(n+'.png') for n in ['front','side','rear','top']],root/'turnaround.jpg',2,1600)
    R.sheet([root/(n+'.png') for n in ['face','wheel','interior_glass']],root/'details.jpg',1,1600)
    R.sheet([root/(c+'_'+v+'.png') for c in ['Porcelain','Carbon','Graphite','Aluminum','Atlantic'] for v in ['front','rear']],root/'factory-colors.jpg',2,1600)
    if a.docs:
        docs=ROOT/'docs';docs.mkdir(exist_ok=True)
        for name,src in [('hero',root/'front_three_quarter.png'),('rear',root/'rear_three_quarter.png'),('details',root/'details.jpg'),('five-colors',root/'factory-colors.jpg'),('turnaround',root/'turnaround.jpg')]:doc(src,docs/('sedan-'+name+'.jpg'))
    (root/'provenance.json').write_text(json.dumps(dict(source='export/AlderS240.glb',source_sha256=digest,views=len(rows),method='Imported GLB and its three baked maps, factory factor decoder only'),indent=2))
    print('S240_FINAL_REVIEW',digest,len(rows),'views')
if __name__=='__main__':main()
