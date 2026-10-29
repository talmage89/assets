"""Checkpoint evidence sheets, measured orthos and current-source provenance.

Never writes docs images or implies final finish acceptance. Photographs are
comparison-only; current gun renders are tied to the baked 2048 GLB.
"""
import json,sys,hashlib,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'renders/checkpoint'
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),23)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def gray(path):
 raw=Image.open(path).convert('RGBA');im=Image.new('RGBA',raw.size,(95,98,102,255));im.alpha_composite(raw);return im.convert('RGB')
def dimensions(stats):
 panels=[]
 for name,labels in [('side',(f"Length {stats['dimensions_mm'][1]:.2f} mm",f"Height {stats['dimensions_mm'][2]:.2f} mm")),
  ('top',(f"Length {stats['dimensions_mm'][1]:.2f} mm",f"Width {stats['dimensions_mm'][0]:.2f} mm")),
  ('front',(f"Width {stats['dimensions_mm'][0]:.2f} mm",f"Height {stats['dimensions_mm'][2]:.2f} mm"))]:
  raw=Image.open(OUT/'beauty'/(name+'.png')).convert('RGBA');box=raw.getchannel('A').getbbox();assert box
  im=Image.new('RGB',(raw.width+180,raw.height+145),(235,237,232));im.paste(gray(OUT/'beauty'/(name+'.png')),(65,55));d=ImageDraw.Draw(im)
  d.text((18,10),name.upper()+' / orthographic imported GLB',font=FONT,fill=(25,36,31))
  x0,y0,x1,y1=box;x0+=65;x1+=65;y0+=55;y1+=55;y=im.height-52
  d.line((x0,y,x1,y),fill=(25,36,31),width=2)
  for x in (x0,x1):d.line((x,y-8,x,y+8),fill=(25,36,31),width=2)
  d.text((65,y+13),labels[0]+'; '+labels[1],font=SMALL,fill=(25,36,31));panels.append(im)
 sheet=Image.new('RGB',(1600,sum(round(p.height*1600/p.width) for p in panels)),(235,237,232));y=0
 for im in panels:
  im=im.resize((1600,round(im.height*1600/im.width)),Image.Resampling.LANCZOS);sheet.paste(im,(0,y));y+=im.height
 sheet.save(OUT/'dimensions.jpg',quality=92,optimize=True)
def main():
 from landmarks import main as landmark_rakes
 landmark_rakes()
 digest=sha(BASE/'export/sxs.glb');stats=json.loads((BASE/'build/serialization.json').read_text());assert stats['sha256']==digest
 current=0
 for folder,expected in [('beauty',digest),('photos',digest),
  ('shell',sha(BASE/'build/shell.glb')),('hull',sha(BASE/'build/hull.glb')),('opening-wide',digest)]:
  meta=json.loads((OUT/folder/'shots.json').read_text())
  for name,row in meta.items():assert row['sha256']==expected,(folder,name,'stale source');current+=1
  if folder=='photos':
   calibration=json.loads((BASE/'build/cameras.json').read_text())
   for name,row in meta.items():
    for key in ('location','target','lens','roll','aspect'):
     assert row[key]==calibration[name]['shot'][key],(folder,name,key,'stale camera')
 for p in (OUT/'strips').iterdir():
  if p.is_dir():
   for name,row in json.loads((p/'shots.json').read_text()).items():assert row['sha256']==digest,(p,name);current+=1
 timing=json.loads((OUT/'strips/timing.json').read_text())
 for name,row in timing.items():
  with Image.open(OUT/'strips'/(name+'.webp')) as im:
   elapsed=0
   for i in range(im.n_frames):im.seek(i);im.load();elapsed+=im.info.get('duration',0)
   assert elapsed==row['duration_ms'],name
 for filename,source in [('check.json',BASE/'build/sxs.blend'),('import-check.json',BASE/'export/sxs.glb')]:
  result=json.loads((BASE/'build'/filename).read_text());assert result['passed'] and result['all_clips']
  assert result['source_sha256']==sha(source),'Stale '+filename
 assert json.loads((BASE/'build/repeat.json').read_text())['passed']
 sec=json.loads((OUT/'sections/sections.json').read_text());assert sec['glb_sha256']==digest and sec['source_sha256']==sha(BASE/'build/sxs.blend')
 records=stats['imported_contacts']['records']
 measured={r['name']:r['measured_m']*1000 for r in records if r['name'].startswith(('drop at ','eye above','cheek station'))}
 sections={r['title']:r['part_sizes_mm'] for r in sec['game']}
 (OUT/'measurements.json').write_text(json.dumps(dict(glb_sha256=digest,actual_surfaces_mm=measured,form_gauges=stats.get('form_gauges'),sections_mm=sections,eye_m=stats['imported_contacts']['eye_m'],length_of_pull_mm=stats['length_of_pull_mm']),indent=2))
 names=['hero','side','left','top','front','rake_right','rake_left','open','breech','action','action_left','triggers','trigger_quarter','forend','stock','muzzle','top_controls','lumps','aimed','action_rake_right','action_rake_left','action_rake_top','action_rake_bottom']
 beauty=[OUT/'beauty'/(name+'.png') for name in names]
 gray(OUT/'beauty/hero.png').save(OUT/'hero-gray.jpg',quality=94,optimize=True)
 review_sheet([beauty[i:i+2] for i in range(0,len(beauty),2)],OUT/'contact-sheet.jpg',width=2400,title='Covey 26 / FORM CHECKPOINT / imported baked 2048 GLB')
 for i in range(0,len(beauty),4):review_sheet([beauty[j:j+2] for j in range(i,min(i+4,len(beauty)),2)],OUT/(f'review-page-{i//4+1}.jpg'),width=2400,title='Current exported form / '+', '.join(names[i:i+4]))
 pairs=[OUT/'pairs'/(name+'-pair.jpg') for name in ('right','left','action','action_left','action_top','action_bottom','open','barrel_flats','forend','forend_side','trigger')]
 review_sheet([[p] for p in pairs],OUT/'photo-pairs.jpg',title='Class photographs / same calibrated framing / see native resolution limits')
 contact([OUT/'strips'/(name+'.jpg') for name in timing],OUT/'clips.jpg',width=2400,title='19 clips / uniform 15 Hz frames / adjacent WebPs play at real durations')
 wide=json.loads((OUT/'opening-wide/shots.json').read_text())
 contact([OUT/'opening-wide'/(name+'.png') for name in wide],OUT/'opening.jpg',width=2000,title='Open / full-gun frame strip / uniform 15 Hz / 1.20 seconds')
 contact([OUT/'shell/shell.png',OUT/'hull/hull.png'],OUT/'ammunition.jpg',width=1600,title='Shared original 12-gauge exterior / live shell and open fired hull')
 dimensions(stats)
 raw=np.array(Image.open(OUT/'beauty/hero.png').convert('RGBA'));rgb=raw[:,:,:3][raw[:,:,3]>128];lum=rgb@np.array([.2126,.7152,.0722])
 tone=dict(luma_p1_p50_p99=np.percentile(lum,[1,50,99]).tolist(),deep_shadow_fraction=float((lum<15).mean()),
  all_channel_clipped_fraction=float(np.all(rgb==255,axis=1).mean()),scope='inspection constants; no albedo/finish acceptance')
 (OUT/'audit.json').write_text(json.dumps(dict(passed=True,source_sha256=digest,current_render_records=current,clips=len(timing),hero_tone=tone),indent=2))
 readme=BASE/'README.md';text=readme.read_text();a=text.index('<!-- CHECKPOINT_STATS -->');b=text.index('<!-- /CHECKPOINT_STATS -->')
 lines=['<!-- CHECKPOINT_STATS -->','', '| Inspection output | Triangles | GLB bytes |','| --- | ---: | ---: |',
  f"| Gun, all staged alternatives | {stats['triangles']:,} | {stats['glb_bytes']:,} |"]
 for name,row in stats['standalones'].items():lines.append(f"| {name.title()} | {row['triangles']:,} | {row['bytes']:,} |")
 lines += ['',f"{stats['parts']} named rigid meshes, {stats['bones']} bones, {stats['clips']} clips, {stats['sockets']} sockets; {stats['materials']} atlas material and **three 2048 texture images** (4096 GPU source bake).",'']
 readme.write_text(text[:a]+'\n'.join(lines)+text[b:])
 print('CHECKPOINT REVIEW PASS',current,'current render records;',len(timing),'real-duration clips;',OUT/'contact-sheet.jpg')
if __name__=='__main__':main()
