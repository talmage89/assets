"""Current-GLB provenance, required final sheets and uncommitted docs JPGs."""
from pathlib import Path
import argparse,json,hashlib,math,sys
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
OUT=BASE/'renders/final';FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
def panel(path,size):
 im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(108,111,114,255));bg.alpha_composite(im)
 return ImageOps.contain(bg.convert('RGB'),size,Image.Resampling.LANCZOS)
def sheet(path,items,columns=3,cell=(600,420)):
 w,h=cell;out=Image.new('RGB',(w*columns,h*math.ceil(len(items)/columns)),(231,233,230));d=ImageDraw.Draw(out)
 for i,(name,p) in enumerate(items):
  x=i%columns*w;y=i//columns*h;d.text((x+12,y+9),name,font=FONT,fill=(25,35,30))
  im=panel(p,(w-10,h-44));out.paste(im,(x+(w-im.width)//2,y+38+(h-44-im.height)//2))
 path.parent.mkdir(parents=True,exist_ok=True);out.save(path,quality=93,optimize=True);return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');a=p.parse_args();records=[];stills=[]
 from wear_sites import main as wear_review
 wear_review()
 from final_shots import DEFAULT_SHOTS
 for folder in ('beauty','eevee','photos','source-photos','loaded','empty','cartridge','case'):
  meta=json.loads((OUT/folder/'shots.json').read_text())
  for name,row in meta.items():
   source=Path(row['source']);assert row['sha256']==hashlib.sha256(source.read_bytes()).hexdigest(),(folder,name,'stale')
   assert source.suffix==('.blend' if folder=='source-photos' else '.glb')
   with Image.open(OUT/folder/(name+'.png')) as im:im.verify()
   records.append(dict(folder=folder,shot=name,source=source.name,sha256=row['sha256'],engine=row['engine']))
   if folder not in ('source-photos','photos'):stills.append((folder+' / '+name,OUT/folder/(name+'.png')))
 assert set(DEFAULT_SHOTS.split(','))<=set(json.loads((OUT/'beauty/shots.json').read_text()))
 timing=json.loads((OUT/'strips/timing.json').read_text());frames=[]
 for clip,t in timing.items():
  meta=json.loads((OUT/'strips'/clip/'shots.json').read_text())
  for name,row in meta.items():
   assert row['sha256']==hashlib.sha256(Path(row['source']).read_bytes()).hexdigest(),(clip,name,'stale')
   assert row['engine']=='BLENDER_EEVEE';frames.append((clip+' / '+name,OUT/'strips'/clip/(name+'.png')))
   records.append(dict(folder='strips',shot=name,source='ak.glb',sha256=row['sha256'],engine=row['engine']))
  with Image.open(OUT/'strips'/(clip+'.webp')) as im:
   duration=0
   for i in range(im.n_frames):im.seek(i);im.load();duration+=im.info.get('duration',0)
  assert duration==t['duration_ms'],clip
 sheet(OUT/'turnaround.jpg',[(n,OUT/'beauty'/(n+'.png')) for n in ('front','side','back','top')],2,(800,650))
 sheet(OUT/'details.jpg',[(n,OUT/'beauty'/(n+'.png')) for n in ('receiver','rear_sight','front_sight','gas_muzzle','wood','grip_detail')],2,(800,620))
 sheet(OUT/'form-fixes.jpg',[(n,OUT/'beauty'/(n+'.png')) for n in ('gas_muzzle','gas_ortho_side','front_sight','retainer','retainer_side','rear_ortho_side','cover_rear','rear_sight')],2,(800,620))
 sheet(OUT/'retainer-reference.jpg',[('GLB / flat diaphragm, fitted return and seated sling eye',OUT/'beauty/retainer.png'),('Independent sharp photo / same held oblique-front view',OUT/'pairs/retainer_photo-pair.jpg')],2,(1000,780))
 sheet(OUT/'wear-sites.jpg',[(n,OUT/'beauty'/(n+'.png')) for n in ('receiver','cover_rear','trigger','controls','open','gas_muzzle','wood','grip_stock','magazine')],3,(800,620))
 sheet(OUT/'action.jpg',[(n,OUT/'beauty'/(n+'.png')) for n in ('open','aimed')]+[(n,OUT/f/(shot+'.png')) for n,f,shot in [('Loaded magazine','loaded','mag_standalone'),('Empty magazine','empty','mag_lips'),('Cartridge','cartridge','cartridge'),('Fired case','case','case_mouth')]],2,(800,600))
 pairs=[(p.stem,p) for p in sorted((OUT/'pairs').glob('*-pair.jpg'))]
 pairs += [(p.stem,p) for p in sorted((OUT/'paint-review').glob('*-histograms.jpg'))]
 sheet(OUT/'photo-pairs.jpg',pairs,2,(1100,750))
 for i in range(0,len(frames),18):sheet(OUT/'inspection'/f'clips-{i//18:02d}.jpg',frames[i:i+18],3,(410,370))
 evidence=[('Metal abrasion / controlled GLB difference',OUT/'metal-wear-proof.jpg'),
           ('Wood / broad and residual value',OUT/'look-review/wood-two-scale.jpg'),
           ('Wood / worn and adjacent intact colors',OUT/'look-review/wood-edge-colors.jpg')]
 sheet(OUT/'contact-sheet.jpg',stills+pairs+evidence+[(clip+' / real-speed strip',OUT/'strips'/(clip+'.jpg')) for clip in timing])
 panel(OUT/'beauty/hero.png',(1600,1000)).save(OUT/'hero-gray.jpg',quality=96)
 predecessor=OUT/'precedent/smg_hero.png'
 if predecessor.exists():
  sheet(OUT/'hero-beside-smg.jpg',[('Rill 39 / current exported GLB',OUT/'beauty/hero.png'),('Relay 9 / same studio',predecessor)],2,(1200,750))
 tone={}
 for name in ('hero','hero_right'):
  rgba=np.asarray(Image.open(OUT/'beauty'/(name+'.png')).convert('RGBA'));rgb=rgba[rgba[:,:,3]>250,:3].astype(float)
  luma=rgb@np.array([.2126,.7152,.0722])
  tone[name]=dict(luma_p1_50_99=np.percentile(luma,[1,50,99]).tolist(),fraction_below_24=float((luma<24).mean()),fraction_white_clipped=float((rgb.min(axis=1)>=254).mean()))
  assert tone[name]['fraction_white_clipped']<.001,(name,tone[name])
 (OUT/'tonal-range.json').write_text(json.dumps(tone,indent=2))
 result=dict(passed=True,stage='exported GLBs with baked 2048 maps; dense sources labeled separately',render_records=len(records),records=records,clip_frames=len(frames),clip_timing=timing)
 (BASE/'build/provenance.json').write_text(json.dumps(result,indent=2))
 if a.docs:
  for filename in ('verify','construction','imported-construction'):
   data=json.loads((BASE/'build/delivery'/(filename+'.json')).read_text());assert data['passed']
  folder=BASE/'docs';folder.mkdir(exist_ok=True)
  for name,path in [('hero',OUT/'beauty/hero.png'),('turnaround',OUT/'turnaround.jpg'),('details',OUT/'details.jpg'),('action',OUT/'action.jpg'),('eevee',OUT/'eevee/hero.png')]:
   im=panel(path,(1600,1400));quality=94
   while True:
    dest=folder/(name+'.jpg');im.save(dest,quality=quality,optimize=True)
    if dest.stat().st_size<200000:break
    quality-=3;assert quality>=60
  print('DOCS prepared for lead review, left uncommitted: five JPGs <=1600 px / 200 KB',flush=True)
 print('FINAL REVIEW',len(records),'verified renders;',len(frames),'clip frames;',OUT/'contact-sheet.jpg',flush=True)
if __name__=='__main__':main()
