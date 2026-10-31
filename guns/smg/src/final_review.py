"""Current-delivery provenance, all-view review sheets and final compact JPGs."""
from pathlib import Path
import argparse,json,hashlib,math,sys
from PIL import Image,ImageOps,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
from value_review import measure,wear_pair,tonal
from finish_review import build as finish_review
from chip_review import build as chip_review
from wear_2d_review import build as wear_2d_review
from highlight_review import build as highlight_review
from paint_value_review import build as paint_value_review
OUT=BASE/'renders/final';FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
def panel(path,size):
 im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(108,111,114,255));bg.alpha_composite(im)
 return ImageOps.contain(bg.convert('RGB'),size,Image.Resampling.LANCZOS)
def sheet(path,items,columns=3,cell=(600,420)):
 w,h=cell;out=Image.new('RGB',(w*columns,h*math.ceil(len(items)/columns)),(231,233,230));d=ImageDraw.Draw(out)
 for i,(name,p) in enumerate(items):
  x=i%columns*w;y=i//columns*h;d.text((x+12,y+9),name,font=FONT,fill=(25,35,30))
  im=panel(p,(w-10,h-44));out.paste(im,(x+(w-im.width)//2,y+38+(h-44-im.height)//2))
 out.save(path,quality=93,optimize=True);return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');a=p.parse_args();records=[];stills=[]
 for folder in ('beauty','eevee','photos','source-photos','finish-response','loaded','empty','cartridge','case'):
  meta=json.loads((OUT/folder/'shots.json').read_text())
  for name,row in meta.items():
   source=Path(row['source']);assert row['sha256']==hashlib.sha256(source.read_bytes()).hexdigest(),(folder,name,'stale')
   assert source.suffix==('.blend' if folder=='source-photos' else '.glb')
   records.append(dict(folder=folder,shot=name,source=source.name,sha256=row['sha256'],engine=row['engine']))
   if folder!='source-photos':stills.append((folder+' / '+name,OUT/folder/(name+'.png')))
 timing=json.loads((OUT/'strips/timing.json').read_text());frames=[]
 for clip,t in timing.items():
  meta=json.loads((OUT/'strips'/clip/'shots.json').read_text())
  for name,row in meta.items():
   assert row['sha256']==hashlib.sha256(Path(row['source']).read_bytes()).hexdigest(),(clip,name,'stale')
   assert row['engine']=='BLENDER_EEVEE';frames.append((clip+' / '+name,OUT/'strips'/clip/(name+'.png')))
   records.append(dict(folder='strips',shot=name,source='smg.glb',sha256=row['sha256'],engine=row['engine']))
  with Image.open(OUT/'strips'/(clip+'.webp')) as im:
   duration=0
   for i in range(im.n_frames):im.seek(i);im.load();duration+=im.info.get('duration',0)
  assert duration==t['duration_ms'],clip
 values=measure(OUT/'photos');values['tonal_ranges']=tonal(OUT/'beauty');(OUT/'photos/values.json').write_text(json.dumps(values,indent=2));finish_review();wear_2d_review();wear_pair();chip_review();highlight_review();paint_value_review()
 stills.append(('Hero receiver / magazine / native pixels',OUT/'beauty/hero-receiver-magazine-native.png'))
 sheet(OUT/'turnaround.jpg',[(n,OUT/'beauty'/(n+'.png')) for n in ('front','side','back','top')],2,(800,650))
 sheet(OUT/'details.jpg',[(n,OUT/'beauty'/(n+'.png')) for n in ('receiver','handle','sights','front_sight','lower','trigger')],2,(800,620))
 sheet(OUT/'action.jpg',[(n,OUT/'beauty'/(n+'.png')) for n in ('locked','aimed')]+[(n,OUT/f/(shot+'.png')) for n,f,shot in [('Loaded magazine','loaded','mag_standalone'),('Empty magazine','empty','mag_lips'),('Cartridge','cartridge','cartridge'),('Fired case','case','case_mouth')]],2,(800,600))
 pairs=[(n,p) for p in sorted((OUT/'pairs').glob('*-pair.jpg')) for n in [p.stem]]
 pairs += [(p.stem,p) for p in sorted((OUT/'paint-review').glob('*-histograms.jpg'))]
 sheet(OUT/'photo-pairs.jpg',pairs,1,(2200,1250))
 sheet(OUT/'contact-sheet.jpg',stills+pairs)
 inspection=OUT/'inspection';inspection.mkdir(exist_ok=True)
 for i in range(0,len(frames),18):sheet(inspection/f'clips-{i//18:02d}.jpg',frames[i:i+18],3,(600,510))
 clips=[]
 for clip,t in timing.items():
  fs=sorted((OUT/'strips'/clip).glob('*.png'));picks=sorted(set(round(i*(len(fs)-1)/4) for i in range(5)))
  clips.extend([(clip+' / '+str(t['duration_ms'])+' ms / '+fs[i].stem,fs[i]) for i in picks])
 sheet(OUT/'clips.jpg',clips,5,(400,360))
 sheet(OUT/'contact-sheet.jpg',stills+pairs+[(clip+' / real-speed strip',OUT/'strips'/(clip+'.jpg')) for clip in timing])
 result=dict(passed=True,stage='exported GLBs with baked 2048 maps; dense sources labeled separately',render_records=len(records),records=records,clip_frames=len(frames),clip_timing=timing)
 (BASE/'build/provenance.json').write_text(json.dumps(result,indent=2))
 if a.docs:
  for filename in ('verify','construction','imported-construction'):
   data=json.loads((BASE/'build/delivery'/(filename+'.json')).read_text());assert data['passed']
  folder=BASE/'docs';folder.mkdir(exist_ok=True)
  for name,path in [('hero',OUT/'beauty/hero.png'),('turnaround',OUT/'turnaround.jpg'),('details',OUT/'details.jpg'),('action',OUT/'action.jpg'),('eevee',OUT/'eevee/hero.png')]:
   im=panel(path,(1600,1400))
   quality=94
   while True:
    dest=folder/(name+'.jpg');im.save(dest,quality=quality,optimize=True)
    if dest.stat().st_size<200000:break
    quality-=3;assert quality>=60
  print('FINAL DOCS: five JPGs, each <=1600 px / 200 KB',flush=True)
 print('FINAL REVIEW',len(records),'source-verified renders;',len(frames),'clip frames;',OUT/'contact-sheet.jpg',flush=True)
if __name__=='__main__':main()
