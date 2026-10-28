"""Checkpoint sheets, actual section plots, timing and provenance audit."""
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'renders/checkpoint'
FONT=find_font('Noto Sans','Regular')


def font(size):return ImageFont.truetype(FONT,size)
def panel(path,size):
    raw=Image.open(path).convert('RGBA');raw.thumbnail(size,Image.Resampling.LANCZOS)
    image=Image.new('RGBA',size,(100,101,103,255));image.alpha_composite(raw,((size[0]-raw.width)//2,(size[1]-raw.height)//2))
    return image.convert('RGB')


def sheet(items,path,columns=3,width=1800,height=330):
    cell=width//columns;rows=(len(items)+columns-1)//columns
    im=Image.new('RGB',(width,rows*(height+38)),(43,45,48));draw=ImageDraw.Draw(im)
    for i,(title,p) in enumerate(items):
        x=i%columns*cell;y=i//columns*(height+38)
        im.paste(panel(p,(cell,height)),(x,y+38));draw.text((x+10,y+5),title,font=font(17),fill='white')
    im.save(path,quality=92,optimize=True)
    return im


def section_sheet(data):
    rows=data['lever'];cellw,cellh=600,440;im=Image.new('RGB',(1800,((len(rows)+2)//3)*cellh),(236,236,232));d=ImageDraw.Draw(im)
    colors={'Stock':(95,51,27),'Forend':(95,51,27),'Receiver':(40,45,50),'Loading_Gate':(100,70,140),
            'Barrel':(35,55,70),'Magazine_Tube':(90,100,110),'Carrier_Cradle':(130,120,80)}
    for i,row in enumerate(rows):
        x=i%3*cellw;y=i//3*cellh
        d.text((x+15,y+10),row['region']+' / Y %g mm'%row['station_mm'],font=font(21),fill=(20,25,30))
        points=[p for lines in row['parts'].values() for line in lines for p in line]
        lo=[min(p[k] for p in points) for k in (0,1)];hi=[max(p[k] for p in points) for k in (0,1)]
        scale=min(410/max(hi[0]-lo[0],1),270/max(hi[1]-lo[1],1));cx=(hi[0]+lo[0])/2;cz=(hi[1]+lo[1])/2
        def xy(p):return x+300+(p[0]-cx)*scale,y+225-(p[1]-cz)*scale
        for a,b in row.get('uninletted_wood',[]):d.line((*xy(a),*xy(b)),fill=(170,170,160),width=4)
        # Dense source in red under the actual game cuts, exposing reduction loss.
        high=data['sculpt'][i]
        for lines in high['parts'].values():
            for a,b in lines:d.line((*xy(a),*xy(b)),fill=(220,145,132),width=3)
        for name,lines in row['parts'].items():
            for a,b in lines:d.line((*xy(a),*xy(b)),fill=colors.get(name,(65,90,100)),width=2)
        a=xy((lo[0],lo[1]))[0];b=xy((hi[0],lo[1]))[0]
        d.line((a,y+378,b,y+378),fill='black',width=2)
        d.text((x+25,y+393),'%.2f mm wide × %.2f mm high'%(row['width_mm'],row['height_mm']),font=font(18),fill='black')
        d.text((x+22,y+43),'Game outline / dense source in pale red',font=font(15),fill=(80,60,55))
        if row.get('uninletted_wood'):d.text((x+22,y+63),'Gray: measured wood before inletting',font=font(14),fill=(95,95,85))
    im.save(OUT/'sections.jpg',quality=94,optimize=True)


def dimensions(data):
    w=1600;im=Image.new('RGB',(w,1380),(235,235,231));d=ImageDraw.Draw(im)
    for i,name in enumerate(('right','top','front')):
        y=i*450;im.paste(panel(OUT/'views'/(name+'.png'),(w,360)),(0,y+35))
        d.text((20,y+5),name.upper()+' / orthographic exported GLB',font=font(23),fill='black')
    size=data['bounds_m']['size']
    labels=['Measured overall %.2f mm | breech to crown %.2f mm'%(size[1]*1000,data['barrel_length_m']*1000),
            'Published targets 965.2 / 508 mm | measured pull %.2f mm'%(data['length_of_pull_m']*1000),
            'Measured width %.2f mm / height %.2f mm'%(size[0]*1000,size[2]*1000)]
    for i,label in enumerate(labels):d.text((30,i*450+405),label,font=font(24),fill=(20,30,40))
    im.save(OUT/'dimensions.jpg',quality=94,optimize=True)


def sight_pixels():
    path=OUT/'views/aimed.png';native=Image.open(path).convert('RGB')
    cx,cy=native.width//2,native.height//2
    rect=(cx-55,cy-42,cx+55,cy+42)
    crop=native.crop(rect)
    crop.save(OUT/'aimed-native-crop.png')
    # Integer nearest-neighbor enlargement: every source pixel is an 8x8
    # square. No rerender, sharpening or changed camera/sight alignment.
    zoom=crop.resize((crop.width*8,crop.height*8),Image.Resampling.NEAREST)
    result=Image.new('RGB',(zoom.width,zoom.height+86),(236,236,232));d=ImageDraw.Draw(result)
    d.text((14,10),'Exact Socket_Eye / native pixels enlarged 8×',font=font(21),fill='black')
    d.text((14,43),'70° horizontal FOV; crop %s from %d × %d'% (str(rect),native.width,native.height),font=font(17),fill='black')
    result.paste(zoom,(0,86));result.save(OUT/'aimed-pixels.jpg',quality=97,optimize=True)
    result.save(OUT/'aimed-pixels.png')
    (BASE/'build/aimed-crop.json').write_text(json.dumps(dict(source=str(path.relative_to(BASE)),
        source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),rectangle=rect,integer_scale=8,
        filter='NEAREST',changed_camera=False),indent=2))


def provenance():
    hashes={n:hashlib.sha256((BASE/'build'/n).read_bytes()).hexdigest() for n in ('lever.glb','sculpt.blend','cartridge.glb','case.glb')}
    records=[]
    folders=[OUT/'views',OUT/'pairs',OUT/'source-pairs',OUT/'cartridge',OUT/'case']
    folders+=list((OUT/'strips').glob('*'))+list((OUT/'detail-strips').glob('*'))
    for folder in folders:
        if not folder.is_dir() or not (folder/'shots.json').exists():continue
        for name,row in json.loads((folder/'shots.json').read_text()).items():
            source=Path(row['source']).name
            assert row['sha256']==hashes[source],(folder,name,'stale image')
            path=folder/(name+'.png');assert path.exists()
            records.append(dict(path=str(path.relative_to(BASE)),source=source,sha256=row['sha256']))
    timing=json.loads((OUT/'strips/timing.json').read_text())
    import importlib.util
    spec=importlib.util.spec_from_file_location('lever_interface',BASE/'src/interface.py');binding=importlib.util.module_from_spec(spec);spec.loader.exec_module(binding)
    assert set(timing)==set(binding.CLIPS)
    for name,s in binding.CLIPS.items():assert timing[name]['encoded_duration_ms']==round(s['frames']/60*1000)
    detail=json.loads((OUT/'detail-strips/timing.json').read_text())
    from strips import DETAIL_CLIPS
    assert set(detail)==set(DETAIL_CLIPS)
    for name,row in detail.items():assert row['encoded_duration_ms']==round(binding.CLIPS[name]['frames']/60*1000)
    result=dict(detail_clips=len(detail),passed=True,records=len(records),sources=hashes,images=records,clips=len(timing))
    (BASE/'build/provenance.json').write_text(json.dumps(result,indent=2))
    print('PROVENANCE',len(records),'current-source images;',len(timing),'real-duration clips')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    views=json.loads((OUT/'views/shots.json').read_text())
    items=[(name,OUT/'views'/(name+'.png')) for name in views]
    items += [(folder+' / '+n,OUT/folder/(n+'.png')) for folder,n in [('cartridge','cartridge'),('cartridge','headstamp'),('case','case'),('case','mouth'),('case','headstamp')]]
    sheet(items,OUT/'contact-sheet.jpg',columns=3,height=330)
    sheet([(n,OUT/'views'/(n+'.png')) for n in ('receiver','receiver_left','hammer','trigger','sights','forend','stock','front_sight','open')],OUT/'regions.jpg')
    sheet([(p.stem,p) for p in sorted((OUT/'pairs').glob('*-pair.jpg'))],OUT/'photo-pairs.jpg',columns=1,width=1800,height=550)
    sheet([(p.stem+' / dense source',p) for p in sorted((OUT/'source-pairs').glob('*-pair.jpg'))],OUT/'source-pairs.jpg',columns=1,width=1800,height=550)
    section_sheet(json.loads((BASE/'build/sections.json').read_text()))
    dimensions(json.loads((BASE/'build/check.json').read_text()))
    sight_pixels()
    sheet([(n,OUT/'views'/(n+'.png')) for n in ('lever_rest_ortho','lever_mid_ortho','lever_open_ortho')],
          OUT/'lever-stroke.jpg',columns=3,height=650)
    sheet([(n,OUT/'pairs'/(n+'-pair.jpg')) for n in ('hammer_photo','trigger_right','trigger_quarter')],
          OUT/'hammer-trigger-pairs.jpg',columns=1,width=2000,height=650)
    sheet([(n,OUT/'views'/(n+'.png')) for n in ('receiver_raking_right','receiver_raking_left')],
          OUT/'raking.jpg',columns=2,height=600)
    timing=json.loads((OUT/'strips/timing.json').read_text())
    sheet([(n,OUT/'strips'/(n+'.jpg')) for n in timing],OUT/'clips.jpg',columns=4,width=2000,height=260)
    detail=json.loads((OUT/'detail-strips/timing.json').read_text())
    sheet([(n,OUT/'detail-strips'/(n+'.jpg')) for n in detail],OUT/'clips-detail.jpg',columns=3,width=1800,height=350)
    # Every rendered clip sample is exposed at a useful inspection size.
    inspection=BASE/'build/inspection';inspection.mkdir(exist_ok=True);frames=[]
    for clip in timing:
        data=json.loads((OUT/'strips'/clip/'shots.json').read_text())
        frames += [(clip+' %.3f s'%s['time_s'],OUT/'strips'/clip/(n+'.png')) for n,s in data.items()]
    for start in range(0,len(frames),24):
        sheet(frames[start:start+24],inspection/('clips-%02d.jpg'%(start//24)),columns=4,width=1920,height=300)
    provenance()
    print('CHECKPOINT SHEETS',OUT/'contact-sheet.jpg')


if __name__=='__main__':main()
