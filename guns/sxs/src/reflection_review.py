"""Comparison-only native head crops and complete reflection review sheets."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'renders/checkpoint'
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),23)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
ROI={'open':(410,445,860,745),'top':(260,400,1180,955),
     'aimed':(480,430,960,650),'right':(400,230,770,510),'left':(670,230,1040,510)}

def crop(path,view):
    im=Image.open(path).convert('RGBA');s=im.width/1440
    im=im.crop(tuple(round(v*s) for v in ROI[view]))
    bg=Image.new('RGBA',im.size,(45,47,50,255));bg.alpha_composite(im)
    return bg.convert('RGB')

def pair(left,right,path,title,labels):
    # Equal-size native crops on both sides; the same pixel rectangle is
    # used before/after and for source/export. No color correction or retouch.
    assert left.size==right.size,(left.size,right.size)
    w,h=left.size;sheet=Image.new('RGB',(w*2,h+90),(237,239,235));d=ImageDraw.Draw(sheet)
    d.text((14,9),title,font=SMALL,fill=(25,36,31))
    for im,x,label in [(left,0,labels[0]),(right,w,labels[1])]:
        d.text((x+14,39),label,font=SMALL,fill=(25,36,31));sheet.paste(im,(x,90))
    sheet.save(path,quality=95,optimize=True)
    return sheet

def stack(panels,path,title):
    width=2000;heights=[round(p.height*width/p.width) for p in panels]
    sheet=Image.new('RGB',(width,sum(heights)+60),(237,239,235));d=ImageDraw.Draw(sheet)
    d.text((18,12),title,font=FONT,fill=(25,36,31));y=60
    for p,h in zip(panels,heights):
        sheet.paste(p.resize((width,h),Image.Resampling.LANCZOS),(0,y));y+=h
    sheet.save(path,quality=94,optimize=True)

def main():
    dest=OUT/'reflections';dest.mkdir(parents=True,exist_ok=True)
    before=ROOT/'build/round7/before';records=[]
    expected={'source':hashlib.sha256((BASE/'build/sculpt.blend').read_bytes()).hexdigest(),
              'export':hashlib.sha256((BASE/'export/sxs.glb').read_bytes()).hexdigest()}
    source_rows=None;current_rows={};baseline_rows={};baseline_checks=0
    for kind in ('source','export'):
        rows=json.loads((dest/kind/'shots.json').read_text())
        assert len(rows)==10
        for name,row in rows.items():
            assert row['sha256']==expected[kind],(kind,name,'stale')
            if kind=='export':assert row['normal_map_retained']
            assert row['diagnostic_roughness']==.045
            if source_rows is not None:
                other=source_rows[name]
                assert row['environment']==other['environment'] and row['resolution']==other['resolution']
                assert max(abs(x-y) for a,b in zip(row['camera_matrix_world'],other['camera_matrix_world']) for x,y in zip(a,b))<.00001
        if kind=='source':source_rows=rows
        current_rows[kind]=rows
        previous=before/('stripes-'+kind)/'shots.json'
        if previous.exists():baseline_rows[kind]=json.loads(previous.read_text())
        records.append(dict(kind=kind,sha256=expected[kind],images=len(rows)))
    for orientation in ('transverse','longitudinal'):
        panels=[];comparisons={kind:[] for kind in ('source','export')}
        for view in ROI:
            name=view+'-'+orientation+'.png'
            a=crop(dest/'source'/name,view);b=crop(dest/'export'/name,view)
            panels.append(pair(a,b,dest/(view+'-source-export-'+orientation+'.jpg'),
                view+' / '+orientation+' parallel bands',('Dense source','Baked 2048 GLB / normal map retained')))
            for kind,current in [('source',a),('export',b)]:
                previous=before/('stripes-'+kind)/name
                if previous.exists():
                    old=baseline_rows[kind][view+'-'+orientation];new=current_rows[kind][view+'-'+orientation]
                    assert old['diagnostic_roughness']==new['diagnostic_roughness']==.045
                    assert old['environment']==new['environment'] and old['resolution']==new['resolution']
                    assert max(abs(x-y) for a,b in zip(old['camera_matrix_world'],new['camera_matrix_world']) for x,y in zip(a,b))<.00001
                    baseline_checks+=1
                    comparisons[kind].append(pair(crop(previous,view),current,
                        dest/(view+'-before-after-'+kind+'-'+orientation+'.jpg'),
                        view+' / identical camera and procedural bands',('Before / round 6 / '+kind,'After / round 7 / '+kind)))
        stack(panels,dest/('source-export-'+orientation+'.jpg'),'All five views / '+orientation+' / dense source and baked export')
        for kind,images in comparisons.items():
            if images:stack(images,dest/('before-after-'+kind+'-'+orientation+'.jpg'),
                'Round 6 / round 7 / '+kind+' / '+orientation+' / all five views')
    # The ordinary player's view crop uses its actual full-resolution PNG.
    current=crop(OUT/'beauty/open.png','open');current.save(dest/'open-head-after.png')
    previous=before/'checkpoint/beauty/open.png'
    if previous.exists():
        old=crop(previous,'open');old.save(dest/'open-head-before.png')
        pair(old,current,dest/'open-head-before-after.jpg','Open player camera / native 450 x 300 head crops',('Before / round 6','After / round 7 / baked 2048 GLB'))
    (dest/'audit.json').write_text(json.dumps(dict(passed=True,records=records,
        comparison_only='Fixed pixel crops; no shader, texture, geometry or color edits',
        baseline_available=previous.exists(),baseline_camera_lighting_checks=baseline_checks),indent=2))
    return 20

if __name__=='__main__':main()
