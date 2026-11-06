"""Review-only before/after crops and numeric tonal receipt; never textures."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
out=Path('renders/comparison');out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(find_font('DejaVu Sans','Book'),24)
for name,old,new,crop in [
 ('meter',ROOT/'build/furniture-before/meter.png',Path('renders/final/meter.png'),(140,280,1430,900)),
 ('symbols',ROOT/'build/furniture-before/signs-warning.png',Path('renders/final/signs-warning.png'),(340,240,1030,445)),
 ('route-plate',ROOT/'build/furniture-before/route/route-plate.png',Path('renders/final/route-plate.png'),(0,0,1440,1080)),
 ('setting',ROOT/'build/furniture-before/hero.png',Path('renders/final/hero.png'),(0,0,1440,873))]:
 ims=[]
 for p in (old,new):
  im=Image.open(p).convert('RGB');scale=im.width/1440;box=tuple(round(v*scale) for v in crop);im=im.crop(box);im=im.resize((max(800,im.width),round(im.height*max(800,im.width)/im.width)),Image.Resampling.LANCZOS);ims.append(im)
 w=max(i.width for i in ims);ims=[i.resize((w,round(i.height*w/i.width)),Image.Resampling.LANCZOS) for i in ims];h=max(i.height for i in ims);canvas=Image.new('RGB',(w*2,h+50),(224,226,219));d=ImageDraw.Draw(canvas)
 for j,(im,caption) in enumerate(zip(ims,('Before / accepted checkpoint','After / exported PBR glTF'))):canvas.paste(im,(j*w,50));d.text((j*w+15,10),caption,font=font,fill=(20,25,22));im.save(out/(name+('-before.png' if j==0 else '-after.png')))
 canvas.save(out/(name+'-pair.jpg'),quality=94)
route={}
for label,path in [('before',ROOT/'build/furniture-before/route/route-plate.json'),('after',Path('renders/final/route-plate.json'))]:
 route[label]=json.loads(path.read_text()).get('measurements')
Path('build/route-plate-comparison.json').write_text(json.dumps(route,indent=2))
for mechanism in ('meter','news'):
 for label,path in [('before',ROOT/'build/furniture-before/matches'/('used-'+mechanism+'-pair.jpg')),('after',Path('renders/match')/('used-'+mechanism+'-pair.jpg'))]:
  im=Image.open(path).convert('RGB');width=min(1600,max(800,im.width));im=im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS)
  im.save(out/('reference-'+mechanism+'-'+label+'.jpg'),quality=94)
hero=np.asarray(Image.open('renders/final/hero.png').convert('RGB')).astype(float)/255;lum=hero@np.array([.2126,.7152,.0722]);report=dict(hero_srgb_luminance_percentiles={str(p):float(np.percentile(lum,p)) for p in (1,5,50,95,99)},hero_share_max_channel_at_least_254=float((hero.max(axis=2)>=254/255).mean()),hero_share_luminance_below_005=float((lum<.05).mean()),scope='Display-referred final PNG luminance, not linear albedo. Full-size visual audit is separate.')
Path('build/hero-range.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
