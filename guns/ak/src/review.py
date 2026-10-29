"""Rebuildable checkpoint sheets, exterior rulers and all-frame inspection pages."""
import hashlib,json,math,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from shots import DEFAULT_SHOTS,PHOTO_POSES,SHOTS
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'renders/checkpoint'
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
def panel(path,w,h):
 im=Image.open(path).convert('RGBA');im.thumbnail((w,h),Image.Resampling.LANCZOS)
 b=Image.new('RGBA',(w,h),(215,217,218,255));b.alpha_composite(im,((w-im.width)//2,(h-im.height)//2));return b.convert('RGB')
def sheet(items,destination,cols=3,w=500,h=360):
 s=Image.new('RGB',(cols*w,math.ceil(len(items)/cols)*h),(236,236,232));d=ImageDraw.Draw(s)
 for i,(label,path) in enumerate(items):
  x=i%cols*w;y=i//cols*h;d.text((x+10,y+8),label,font=FONT,fill=(25,35,30));s.paste(panel(path,w-8,h-42),(x+4,y+38))
 s.save(destination,quality=91,optimize=True)
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 beauty=sorted((OUT/'beauty').glob('*.png'));sheet([(p.stem,p) for p in beauty],OUT/'beauty-sheet.jpg')
 pairs=sorted((OUT/'pairs').glob('*-pair.jpg'))
 if pairs:sheet([(p.stem,p) for p in pairs],OUT/'photo-pairs.jpg',cols=1,w=1500,h=600)
 strips=sorted((OUT/'strips').glob('*.jpg'))
 if strips:sheet([(p.stem,p) for p in strips],OUT/'clips.jpg',cols=2,w=750,h=420)
 rock=sorted((OUT/'strips/Reload').glob('*.png'))
 rock=[p for p in rock if 28<=int(p.stem.split('_')[-1])<=34]
 if rock:
  schedule=json.loads((OUT/'strips/Reload/shots.json').read_text())
  sheet([(f"f{schedule[p.stem]['frame']:g} / {schedule[p.stem]['time_s']:.3f} s",p) for p in rock],OUT/'rock-in.jpg',cols=4,w=400,h=360)
 selection=sorted((OUT/'selector').glob('*.png'))
 if selection:sheet([(p.stem,p) for p in selection],OUT/'selector.jpg',cols=3,w=500,h=400)
 # Every rendered strip sample is retained at useful scale on separate pages.
 frames=sorted((OUT/'strips').glob('*/*.png'))
 for start in range(0,len(frames),18):
  ps=frames[start:start+18];sheet([(p.parent.name+' '+p.stem,p) for p in ps],OUT/f'clip-inspection-{start//18:02d}.jpg',cols=3,w=500,h=430)
 tri=json.loads((BASE/'build/triangles.json').read_text());meta={}
 for folder in ('beauty','photos','source-photos','loaded','empty','cartridge','case','selector','contacts','source-contacts'):
  p=OUT/folder/'shots.json'
  if p.exists():meta[folder]=json.loads(p.read_text())
 calibration=json.loads((BASE/'build/cameras.json').read_text())
 assert set(meta['beauty'])==set(DEFAULT_SHOTS.split(',')),'missing checkpoint beauty'
 for name,row in meta['beauty'].items():
  expected=SHOTS[name]
  if 'diagnostic_prefixes' in expected:
   assert row.get('diagnostic_prefixes')==expected['diagnostic_prefixes'],('stale orthographic isolation',name)
 for folder in ('photos','source-photos'):
  assert set(meta[folder])==set(calibration),('missing photo view',folder)
  for name,row in meta[folder].items():
   for key in ('location','target','lens','aspect','roll'):
    assert row[key]==calibration[name]['shot'][key],('stale camera',folder,name,key)
   for key in ('action','frame','diagnostic_prefixes','diagnostic_isolate'):
    if key in PHOTO_POSES.get(name,{}):
     assert row.get(key)==PHOTO_POSES[name][key],('stale photo pose',folder,name,key)
 render_records=0
 for folder,data in [*meta.items(),*[(str(p.parent.relative_to(OUT)),json.loads(p.read_text())) for p in (OUT/'strips').glob('*/shots.json')]]:
  for name,row in data.items():
   assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['sha256'],('stale render',folder,name)
   with Image.open(OUT/folder/(name+'.png')) as im:im.verify()
   render_records+=1
 extras=[(folder+'/'+p.stem,p) for folder in ('loaded','empty','cartridge','case','selector') for p in sorted((OUT/folder).glob('*.png'))]
 if extras:sheet(extras,OUT/'extra-sheet.jpg',cols=3,w=500,h=420)
 contact_items=[(folder+'/'+p.stem,p) for folder in ('contacts','source-contacts') for p in sorted((OUT/folder).glob('*.png'))]
 if contact_items:sheet(contact_items,OUT/'contacts.jpg',cols=2,w=750,h=600)
 # Actual bounds are measured independently in check.py.
 check=json.loads((BASE/'build/check.json').read_text());g=check['geometry'];dims=g['bounds_m']['size']
 s=Image.new('RGB',(1500,1300),(236,236,232));d=ImageDraw.Draw(s)
 d.text((20,15),'Rill 39 / orthographic dimensions / exported inspection GLB',font=FONT,fill=(25,35,30))
 for i,name in enumerate(('side','top','front')):
  p=OUT/'beauty'/(name+'.png');s.paste(panel(p,1450,350),(25,60+i*400))
  label=f'Envelope: length {dims[1]*1000:.2f} mm | width {dims[0]*1000:.2f} mm | height {dims[2]*1000:.2f} mm'
  d.text((25,415+i*400),label,font=FONT,fill=(25,35,30))
 s.save(OUT/'dimensions.jpg',quality=92)
 items=[('Exported views',OUT/'beauty-sheet.jpg'),('Actual sections',OUT/'sections.jpg'),('Exterior dimensions',OUT/'dimensions.jpg')]
 for label,f in [('Photographic pairs','photo-pairs.jpg'),('Clips at real duration','clips.jpg')]:
  if (OUT/f).exists():items.append((label,OUT/f))
 if extras:items.append(('Detachables, ammunition and selector',OUT/'extra-sheet.jpg'))
 if contact_items:items.append(('Actual contact diagnostics / source and GLB',OUT/'contacts.jpg'))
 if (OUT/'trigger-measurements.jpg').exists():items.append(('Photographic trigger observations',OUT/'trigger-measurements.jpg'))
 if (OUT/'form-observations.jpg').exists():items.append(('Round 3 photographic form observations',OUT/'form-observations.jpg'))
 sheet(items,OUT/'contact-sheet.jpg',cols=2,w=800,h=650)
 (BASE/'build/media.json').write_text(json.dumps(dict(triangles=tri['total'],render_groups=meta,strip_frames=len(frames),verified_render_records=render_records),indent=2))
 print('REVIEW',len(beauty),'beauties',len(pairs),'photo pairs',len(frames),'strip samples;',render_records,'verified source hashes')
if __name__=='__main__':main()
