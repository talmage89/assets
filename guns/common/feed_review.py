"""Native-pixel inspection pages and synchronized before/after feed strips."""
import argparse,hashlib,json,math,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font

def panel(path,label):
    raw=Image.open(path).convert('RGBA')
    bg=Image.new('RGBA',raw.size,(58,61,65,255));bg.alpha_composite(raw)
    out=Image.new('RGB',(raw.width,raw.height+28),(229,230,226));out.paste(bg.convert('RGB'),(0,28))
    ImageDraw.Draw(out).text((8,3),label,font=ImageFont.truetype(find_font('Noto Sans','Regular'),15),fill=(22,28,25))
    return out

def sheet(panels,path,columns):
    w,h=panels[0].size;out=Image.new('RGB',(w*columns,h*math.ceil(len(panels)/columns)),(229,230,226))
    for i,p in enumerate(panels):out.paste(p,(w*(i%columns),h*(i//columns)))
    path.parent.mkdir(parents=True,exist_ok=True);out.save(path,quality=90,optimize=True)

def inspect(base,stage):
    source=base/'renders/feed'/stage;timing=json.loads((source/'timing.json').read_text())
    unique={};records=[]
    for clip,row in timing.items():
        metadata=json.loads((source/clip/'shots.json').read_text())
        for name,spec in metadata.items():
            assert spec['sha256']==row['source_sha256']
            path=source/clip/(name+'.png');raw=Image.open(path).convert('RGBA')
            digest=hashlib.sha256(raw.tobytes()).hexdigest()
            entry=dict(path=str(path.relative_to(base)),clip=clip,frame=spec['frame'],image_sha256=digest,
                       source_sha256=spec['sha256'],renderer_sha256=spec['renderer_sha256'])
            records.append(entry);unique.setdefault(digest,entry)
    out=base/'build/feed-inspection'/stage;values=list(unique.values())
    for page,start in enumerate(range(0,len(values),12)):
        sheet([panel(base/r['path'],f'{r["clip"]}  f{r["frame"]:g}') for r in values[start:start+12]],out/f'unique-{page:03}.jpg',3)
    result=dict(stage=stage,rendered_records=len(records),unique_images=len(values),pages=math.ceil(len(values)/12),records=records)
    (out/'index.json').write_text(json.dumps(result,indent=2)+'\n')
    print('FEED INSPECTION',base.name,stage,len(records),len(values),'unique images',flush=True)
    return result

def compare(base):
    root=base/'renders/feed';before=json.loads((root/'before/timing.json').read_text());after=json.loads((root/'after/timing.json').read_text())
    assert before.keys()==after.keys();out=root/'comparison';out.mkdir(exist_ok=True);records={}
    for clip,row in after.items():
        assert before[clip]['frames']==row['frames']
        panels=[]
        for f in row['frames']:
            for stage in ('before','after'):
                panels.append(panel(root/stage/clip/f'f{f:04d}.png',f'{stage.upper()}  {clip}  f{f:g}'))
        sheet(panels,out/(clip+'.jpg'),2)
        for page,start in enumerate(range(0,len(panels),16)):
            sheet(panels[start:start+16],out/clip/f'inspect-{page:02}.jpg',2)
        records[clip]=dict(frames=row['frames'],rate_hz=30,before_sha256=before[clip]['source_sha256'],after_sha256=row['source_sha256'])
    (out/'index.json').write_text(json.dumps(records,indent=2)+'\n')
    print('FEED COMPARISONS',base.name,len(records),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--asset',required=True);p.add_argument('--stage',choices=('before','after'));p.add_argument('--compare',action='store_true');a=p.parse_args()
    if a.stage:inspect(Path(a.asset),a.stage)
    if a.compare:compare(Path(a.asset))
