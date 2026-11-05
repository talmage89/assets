"""Final GLB provenance, tone, bake-loss evidence and bounded hatch docs.

Sheet layout reuses the pickup's gallery review helpers. Photographs and
before/after diagnostics remain in ignored renders, separate from docs.
"""
import argparse,hashlib,json,math,os,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import review_lookdev as R
from hatch_pair_measure import measure
from hatch_final_views import FINAL_VIEWS
ROOT=Path(__file__).resolve().parents[1]


def sheet(files,out,columns=3,width=800,captions=None):
    """Pickup panel treatment, with cells sized to the native gallery aspect."""
    title=max(38,round(width*.048));height=round(width/1.5)+title
    canvas=Image.new('RGB',(columns*width,math.ceil(len(files)/columns)*height),(226,228,225))
    draw=ImageDraw.Draw(canvas);font=ImageFont.truetype(R.FONT,max(17,round(width*.022)))
    for i,path in enumerate(files):
        x=i%columns*width;y=i//columns*height
        canvas.paste(R.panel(path,(width,height-title)),(x,y+title))
        draw.text((x+14,y+8),(captions or {}).get(str(path),path.stem),font=font,fill=(25,32,30))
    canvas.save(out,quality=92,optimize=True)


def doc(source,target):
    image=Image.open(source).convert('RGB');image.thumbnail((1600,16000),Image.Resampling.LANCZOS)
    target.parent.mkdir(parents=True,exist_ok=True)
    for quality in range(94,43,-2):
        image.save(target,quality=quality,optimize=True)
        if target.stat().st_size<=200000:return
    raise ValueError('Doc over 200 KB: '+str(target))


def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--docs',action='store_true');a=p.parse_args()
    folder=Path(a.renders).resolve();os.chdir(ROOT)
    eevee=folder.parent/'hatch-final-eevee';pairs=folder.parent/'hatch-final-pairs'
    source_pairs=folder.parent/'hatch-source-pairs';digest=hashlib.sha256((ROOT/'export/AlderH120.glb').read_bytes()).hexdigest()
    all_rows=[]
    for directory in [folder,eevee,pairs]:
        records=json.loads((directory/'shots.json').read_text());all_rows.extend(records.values())
        if any(r.get('stage')!='final' or Path(r['source']).suffix!='.glb' or r['source_sha256']!=digest for r in records.values()):raise ValueError('Stale or non-GLB final: '+str(directory))
        sys.argv=['review_lookdev','--renders',str(directory)];R.main()
    if len({r['render_recipe_sha256'] for r in all_rows})!=1:raise ValueError('Mixed final presentation recipes')
    records=json.loads((folder/'shots.json').read_text())
    if abs(records['scale']['human_measured_height_m']-1.8)>1e-5:raise ValueError('Scale silhouette is not 1.8 m')
    colors=['paint_'+c for c in ['Porcelain','Carbon','Graphite','Aluminum','Atlantic']]
    views=list(FINAL_VIEWS);files=[folder/(n+'.png') for n in views+colors]+[eevee/'hero.png']
    labels={'face':'Grille and lettering','lamp':'Projector optics','wheel':'Alloy and sidewall',
        'rear_quarter':'Rear lens and fuel flap','gate':'Liftgate draw','plate':'Dealer insert',
        'cargo':'Open cargo area','scale':'1.8 m scale'}
    captions={str(folder/(n+'.png')):labels.get(n,n.removeprefix('paint_').replace('_',' ').capitalize()) for n in views+colors}
    captions[str(eevee/'hero.png')]='Eevee / exported GLB'
    for path in files:
        if not path.exists():raise FileNotFoundError(path)
    sheet(files,folder/'contact-sheet.jpg',columns=3,width=800,captions=captions)
    sheet([folder/(n+'.png') for n in ['front','side','back','top']],folder/'turnaround.jpg',columns=2,width=800,captions=captions)
    sheet([folder/(n+'.png') for n in ['face','lamp','wheel','rear_quarter']],folder/'details.jpg',columns=2,width=800,captions=captions)
    sheet([folder/(n+'.png') for n in colors],folder/'five-colors.jpg',columns=2,width=800,captions=captions)
    sheet([folder/'scale.png',eevee/'hero.png'],folder/'scale-eevee.jpg',columns=1,width=1600,captions=captions)
    sheet([pairs/(n+'-pair.jpg') for n in ['used_front','used_rear']],pairs/'contact-sheet.jpg',columns=1,width=1600)
    if (source_pairs/'shots.json').exists():
        source_meta=json.loads((source_pairs/'shots.json').read_text());expected=hashlib.sha256((ROOT/'build/hatch-detail/game.blend').read_bytes()).hexdigest()
        if any(r['source_sha256']!=expected for r in source_meta.values()):raise ValueError('Stale source comparison')
        before=measure(source_pairs);after=measure(pairs);loss={}
        for name in before:
            original={r['label']:r for r in before[name]['patches']}
            loss[name]={r['label']:dict(source_luma=original[r['label']]['render']['luma_median_255'],export_luma=r['render']['luma_median_255'],
                export_minus_source=r['render']['luma_median_255']-original[r['label']]['render']['luma_median_255']) for r in after[name]['patches']}
        (folder/'bake-loss.json').write_text(json.dumps(loss,indent=2))
    if a.docs:
        for name in ['hero','details','turnaround','five-colors','scale-eevee']:doc(folder/(name+'.jpg'),ROOT/'docs'/('hatch-'+name+'.jpg'))
    (folder/'provenance.json').write_text(json.dumps(dict(source='export/AlderH120.glb',source_sha256=digest,views=len(files),photo_pairs=2,
        gallery='Unchanged C150 studio/lights/view transform; hatch camera framing only',
        method='Fresh GLB import; embedded baked maps and factory/lamp uniforms only; no procedural source finishes'),indent=2))
    print('H120_FINAL_REVIEW',len(files),'gallery views; two pairs; source comparison; bounded docs' if a.docs else 'gallery views; two pairs; source comparison; docs deferred')
if __name__=='__main__':main()
