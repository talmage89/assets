"""Local-only checkpoint sheets, annotated exported plans and tonal receipts."""
import sys,json,math,argparse,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path.insert(0,str(REPO))
from kit.contact import contact,review_sheet
from kit.fonts import find_font
FONT=find_font('Noto Sans')


def bundle(path):
    p=Path(path);doc=json.loads(p.read_text());inputs=[p]+[p.parent/x['uri'] for k in ('buffers','images') for x in doc.get(k,[]) if x.get('uri')]
    return hashlib.sha256(b''.join(hashlib.sha256(x.read_bytes()).digest() for x in inputs)).hexdigest()


def sites():
    """Raw glTF instance counts/image identities, independent of Blender count."""
    report={}
    def count(doc):return sum(doc['accessors'][p['indices']]['count']//3 for n in doc['nodes'] if 'mesh' in n for p in doc['meshes'][n['mesh']]['primitives'])
    for seed in (117,229,341):
        path=Path(f'export/checkpoint/Site_{seed}.gltf');doc=json.loads(path.read_text());receipt=json.loads(Path(f'build/context/site-{seed}.json').read_text())
        garden_path=Path(f'export/checkpoint/Garden_{seed}.gltf');garden_doc=json.loads(garden_path.read_text());garden_triangles=count(garden_doc)
        triangles=count(doc)
        assert triangles==receipt['triangles']==garden_triangles+receipt['context_triangles']
        assert receipt['garden_bundle']==bundle(f'export/checkpoint/Garden_{seed}.gltf')
        assert receipt['scene_bundle']==bundle(path)
        assert receipt['package_recipe']==hashlib.sha256((HERE/'neighborhood.py').read_bytes()).hexdigest()
        unique={};uris=[]
        for im in doc.get('images',[]):
            f=path.parent/im['uri'];sha=hashlib.sha256(f.read_bytes()).hexdigest();w,h=Image.open(f).size
            unique[sha]=dict(width=w,height=h,bytes=f.stat().st_size);uris.append(im['uri'])
        garden_images={hashlib.sha256((garden_path.parent/r['uri']).read_bytes()).hexdigest() for r in garden_doc['images']}
        assert garden_images.issubset(unique),'Packaged scene lost/re-encoded a garden image'
        def descend(i):return [i]+[j for child in doc['nodes'][i].get('children',[]) for j in descend(child)]
        garden=next(i for i,n in enumerate(doc['nodes']) if n.get('name')=='Garden_'+str(seed));garden_nodes=descend(garden)
        assert not any('COLOR_0' in p['attributes'] for i in garden_nodes if 'mesh' in doc['nodes'][i] for p in doc['meshes'][doc['nodes'][i]['mesh']]['primitives']),'Wind leaked into garden base color'
        colors=sum('COLOR_0' in p['attributes'] for m in doc['meshes'] for p in m['primitives'])
        assert colors>0,'Native building material tints lost during scene packaging'
        report[str(seed)]=dict(triangles=triangles,garden_triangles=garden_triangles,context_triangles=receipt['context_triangles'],
            materials=len(doc.get('materials',[])),unique_images=len(unique),compressed_texture_mib=sum(r['width']*r['height']*4/3 for r in unique.values())/2**20,
            gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,external_png_bytes=sum(r['bytes'] for r in unique.values()),native_color_primitives=colors,uris=uris)
    Path('build/site-check.json').write_text(json.dumps(dict(passed=True,scenes=report,scope='raw glTF counts and shared external image bytes; renderer separately checks fresh Blender re-import count'),indent=2))


def above(seed,folder):
    path=Path(folder)/str(seed)/'above.png'
    if not path.exists():return
    im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im);data=json.loads(path.with_suffix('.json').read_text())
    p=data.get('plan') or json.loads(Path(f'build/garden-{seed}.json').read_text())['plan'];span=data['camera']['ortho'];W,H=im.size
    # Orthographic camera at (0,0,Z) with +Y image-up, same as render.shot.
    def pt(x,y):return (W/2+x/span*W,H/2-y/span*W)
    font=ImageFont.truetype(FONT,max(12,round(W*.015)));small=ImageFont.truetype(FONT,max(11,round(W*.012)))
    for b in p['plots']:
        x,y=b['center'];w,d=b['width'],b['depth'];box=(*pt(x-w/2,y+d/2),*pt(x+w/2,y-d/2))
        draw.rectangle(box,outline=(255,228,129),width=2)
        q=pt(x,y);label=f'{b["id"]:02} {b["state"]}\n{w/.3048:g}x{d/.3048:g} ft'
        draw.multiline_text(q,label,font=small,fill='white',stroke_width=2,stroke_fill=(20,25,18),anchor='mm',align='center')
    for r in p['paths']:
        x,y=r['center'];w,d=r['size'];a,b=pt(x-w/2,y+d/2),pt(x+w/2,y-d/2)
        draw.rectangle((*a,*b),outline=(105,218,247),width=3)
        draw.text(pt(x,y),f'{min(w,d):.3f} m',font=font,fill=(105,218,247),stroke_width=2,stroke_fill=(15,23,25),anchor='mm')
    title=f'{p["name"]} | {p["year"]} | {p["size"][0]:.3f} x {p["size"][1]:.3f} m'
    draw.rectangle((0,0,W,40),fill=(24,31,25));draw.text((15,8),title,font=font,fill='white')
    im.save(path.with_name('above-annotated.jpg'),quality=93)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/checkpoint');p.add_argument('--archive',action='store_true');p.add_argument('--sites-only',action='store_true');a=p.parse_args();folder=Path(a.out)
    if a.sites_only:sites();print('SCENE CHECK PASSED');return
    if not a.archive:
        sites()
        checked=[];recipe=hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest()
        for receipt in sorted(folder.rglob('*.json')):
            r=json.loads(receipt.read_text())
            if 'bundle_sha256' not in r:continue
            assert bundle(r['source'])==r['bundle_sha256'],('Render uses stale export',str(receipt))
            if r.get('render_script_sha256'):assert r['render_script_sha256']==recipe,('Render uses stale recipe',str(receipt))
            assert receipt.with_suffix('.png').is_file()
            if receipt.stem=='hero':assert 35<=r['camera']['lens']<=50 and abs(r['camera']['location'][2]-1.65)<1e-5
            checked.append(str(receipt))
        assert len(checked)>=29,('Missing checkpoint render receipts',len(checked))
        (folder/'provenance.json').write_text(json.dumps(dict(passed=True,checked=len(checked),receipts=checked),indent=2))
    files=sorted(folder.glob('*/*.png'));assert files,'No checkpoint renders'
    for s in (117,229,341):above(s,folder)
    for name in ('pieces.png','plants.png'):
        if (folder/name).exists():files.append(folder/name)
    files+=sorted((folder/'matches').glob('*-pair.jpg'))
    captions={str(p):p.parent.name+' / '+p.stem for p in files};contact(files,folder/'contact.jpg',width=1600,title='Community gardens / exported form checkpoint',captions=captions)
    heroes=[folder/str(s)/'hero.png' for s in (117,229,341)]
    if all(p.exists() for p in heroes):review_sheet([[p] for p in heroes],folder/'heroes.jpg',width=1600,title='Eye height / 35–50mm / raking sun')
    pairs=sorted((folder/'matches').glob('*-pair.jpg'))
    if pairs:review_sheet([[p] for p in pairs],folder/'matched-contact.jpg',width=2200,title='Three period garden comparisons / calibrated framing')
    details=[p for p in files if p.stem in ('tomato','bean','corner','compost','water','accessible','scale')]
    if details:contact(details,folder/'details.jpg',width=1600,title='Construction and crop form / exported checkpoint')
    values={}
    for p in heroes:
        if not p.exists():continue
        rgb=np.array(Image.open(p).convert('RGB'))/255;Y=rgb@np.array([.2126,.7152,.0722]);g=(rgb[:,:,1]>rgb[:,:,0]*1.1)&(rgb[:,:,1]>rgb[:,:,2]*1.08)
        values[p.parent.name]=dict(display_luma_p5_median_p95=np.quantile(Y,[.05,.5,.95]).tolist(),channels_clipped_share=float((rgb>=.995).any(axis=2).mean()),green_luma_p5_median_p95=np.quantile(Y[g],[.05,.5,.95]).tolist() if g.any() else None)
    (folder/'tonal-range.json').write_text(json.dumps(values,indent=2));print(json.dumps(values,indent=2))


if __name__=='__main__':main()
