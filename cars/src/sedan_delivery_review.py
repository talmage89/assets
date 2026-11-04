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

def bake_loss():
    """Measure delivered appearance loss separately from photographic error."""
    source=ROOT/'renders/sedan-source-pairs';baked=ROOT/'renders/sedan-used-pairs'
    sp=json.loads((source/'appearance-patches.json').read_text());bp=json.loads((baked/'appearance-patches.json').read_text())
    sm=json.loads((source/'shots.json').read_text());bm=json.loads((baked/'shots.json').read_text());records=[]
    source_digest=hashlib.sha256((ROOT/'build/sedan/detail-game.blend').read_bytes()).hexdigest()
    for view,record in sp.items():
        if sm[view]['source_sha256']!=source_digest:raise ValueError('Stale procedural source comparison')
        if sm[view]['render_recipe_sha256']!=bm[view]['render_recipe_sha256']:raise ValueError('Source/baked comparison uses different presentation recipes')
        for key in ['location','target','lens','roll','paint','lighting','exposure','width','height']:
            if sm[view].get(key)!=bm[view].get(key):raise ValueError('Source/baked comparison differs in '+key)
        for label,patch in record['patches'].items():
            a=patch['render']['display_rgb'];b=bp[view]['patches'][label]['render']['display_rgb']
            records.append(dict(view=view,patch=label,source_display_rgb=a,baked_display_rgb=b,max_channel_difference=max(abs(x-y) for x,y in zip(a,b))))
    report=dict(method='Same calibrated camera, procedural sun/sky, factory factors and exposure; ray-measured surface patches on source and imported GLB',source_sha256=sm['used_front']['source_sha256'],glb_sha256=bm['used_front']['source_sha256'],patches=records,maximum_patch_channel_difference=max(r['max_channel_difference'] for r in records))
    (baked/'bake-loss.json').write_text(json.dumps(report,indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');p.add_argument('--diagnostics');a=p.parse_args()
    if a.diagnostics:diagnostic_sheet(a.diagnostics);return
    root=ROOT/'renders/sedan-detail';folders=[root,ROOT/'renders/sedan-used-pairs',ROOT/'renders/sedan-eevee',ROOT/'renders/sedan-motion']
    digest=hashlib.sha256((ROOT/'export/AlderS240.glb').read_bytes()).hexdigest();rows=[]
    for folder in folders:
        meta,_=R.tone(folder);rows+=list(meta.values())
    if any(r['source_sha256']!=digest or r['stage']!='final exported GLB' for r in rows):raise ValueError('Final gallery uses a stale or non-GLB source')
    if len({r['render_recipe_sha256'] for r in rows})!=1:raise ValueError('Mixed presentation recipe')
    bake_loss()
    names=['front_three_quarter','rear_three_quarter','front','side','rear','top','face','lamp_unlit','lamp_lit','wheel','mirror','interior_glass','underbody','underbody_layout','opened_front','opened_rear','scale']
    R.sheet([root/(n+'.png') for n in names]+[ROOT/'renders/sedan-eevee/front_three_quarter.png'],root/'contact.jpg',3,1800)
    R.sheet([root/(n+'.png') for n in ['front','side','rear','top']],root/'turnaround.jpg',2,1600)
    details=Image.new('RGB',(1600,1700),(230,232,230))
    for name,box,pos in [('face',(1600,1100),(0,0)),('wheel',(800,600),(0,1100)),('interior_glass',(800,600),(800,1100))]:
        im=R.rgb(root/(name+'.png'));im.thumbnail(box,Image.Resampling.LANCZOS)
        details.paste(im,(pos[0]+(box[0]-im.width)//2,pos[1]+(box[1]-im.height)//2))
    details.save(root/'details.jpg',quality=93,optimize=True)
    R.sheet([root/(c+'_'+v+'.png') for c in ['Porcelain','Carbon','Graphite','Aluminum','Atlantic'] for v in ['front','rear']],root/'factory-colors.jpg',2,1600)
    motion=ROOT/'renders/sedan-motion';motion_meta=json.loads((motion/'shots.json').read_text())
    R.sheet([motion/(n+'.png') for n in motion_meta],motion/'contact.jpg',5,2400)
    for group in ['doors','hood','trunk','steering','wheels']:
        R.sheet([motion/(group+'_'+str(i)+'.png') for i in range(5)],motion/(group+'-sweep.jpg'),5,2400)
    R.sheet([root/'contact.jpg',root/'factory-colors.jpg',ROOT/'renders/sedan-used-pairs/used_front-pair.jpg',ROOT/'renders/sedan-used-pairs/used_rear-pair.jpg',motion/'contact.jpg',ROOT/'renders/sedan-eevee/front_three_quarter.jpg'],root/'checkpoint.jpg',2,2400)
    if a.docs:
        docs=ROOT/'docs';docs.mkdir(exist_ok=True)
        for name,src in [('hero',root/'front_three_quarter.png'),('rear',root/'rear_three_quarter.png'),('details',root/'details.jpg'),('five-colors',root/'factory-colors.jpg'),('turnaround',root/'turnaround.jpg')]:doc(src,docs/('sedan-'+name+'.jpg'))
    (root/'provenance.json').write_text(json.dumps(dict(source='export/AlderS240.glb',source_sha256=digest,views=len(rows),method='Imported GLB and its three baked maps, factory factor decoder only'),indent=2))
    print('S240_FINAL_REVIEW',digest,len(rows),'views')
if __name__=='__main__':main()
