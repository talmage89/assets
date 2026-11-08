"""Current exported-frame provenance and contact sheets; no source-scene finals."""
import json,sys,math,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from external import bundle
from render_recipe import digest as recipe
from render_batch import SCENES

def sheet(files,out,cols=3,width=480):
 rows=math.ceil(len(files)/cols);heights=[round(width*.68)+30]*rows
 if cols==1:heights=[round((width-12)*Image.open(p).height/Image.open(p).width)+40 for p in files]
 im=Image.new('RGB',(width*cols,sum(heights)),(31,36,33));d=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),15)
 for i,path in enumerate(files):
  row=i//cols;h=heights[row];image=Image.open(path).convert('RGB');image.thumbnail((width-12,h-40));x=(i%cols)*width+6;y=sum(heights[:row])+6
  im.paste(image,(x+(width-12-image.width)//2,y));d.text((x,y+h-32),str(path.relative_to(Path('renders'))).replace('.png',''),font=font,fill=(228,235,222))
 Path(out).parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91,optimize=True)

def validate(path,engine='CYCLES',source_fields=False):
 record=json.loads(path.with_suffix('.json').read_text());assert record['engine']==engine,path
 assert record['bundle_sha256']==bundle(record['source']),('Stale geometry or PBR',path)
 assert record['frame_sha256']==hashlib.sha256(path.read_bytes()).hexdigest(),('Changed frame',path)
 assert record['recipe_sha256']==recipe(),('Stale presentation recipe',path)
 for ctx in record.get('context',[]):assert ctx['bundle_sha256']==bundle(ctx['source']),('Stale context',path)
 assert Image.open(path).width>=800,path
 if source_fields:
  assert record['material_stage']=='4096 source-field inspection' and record['source_field_changes'],path
  for name,h in record['source_field_hashes'].items():assert hashlib.sha256((Path('textures/source')/name).read_bytes()).hexdigest()==h,path
 else:assert record.get('material_stage')=='exported shipped PBR',path
 return record

def main():
 folder=Path('renders/final');files=[folder/str(s)/(v+'.png') for s,names in SCENES.items() for v in names]
 receipts={str(path):validate(path) for path in files}
 modules=json.loads(Path('build/modules.json').read_text())
 for name in modules:
  path=folder/'modules'/(name+'.png');receipts[str(path)]=validate(path)
 scale=folder/'scale.png';record=json.loads(scale.with_suffix('.json').read_text())
 assert record['bundle_sha256']==bundle(record['source']) and record['recipe_sha256']==recipe()
 assert record['frame_sha256']==hashlib.sha256(scale.read_bytes()).hexdigest()
 assert abs(record['measured_human_height_m']-1.8)<1e-5
 assert record['car_glb_sha256']==hashlib.sha256(Path(record['car_glb']).read_bytes()).hexdigest()
 receipts[str(scale)]=record
 modules_png=folder/'modules.png';module_record=json.loads(modules_png.with_suffix('.json').read_text())
 assert module_record['bundle_sha256']==bundle(module_record['source'])
 assert module_record['frame_sha256']==hashlib.sha256(modules_png.read_bytes()).hexdigest()
 assert module_record['sheet_recipe_sha256']==hashlib.sha256(Path('src/module_sheet.py').read_bytes()).hexdigest()
 eevee=Path('renders/final-eevee/101/hero.png');receipts[str(eevee)]=validate(eevee,'BLENDER_EEVEE')
 cameras=json.loads(Path('build/cameras.json').read_text())
 for folder_name,source in [('renders/final-matches',False),('renders/final-source-matches',True)]:
  for name,row in cameras.items():
   path=Path(folder_name)/(name+'.png');r=validate(path,source_fields=source);assert r['camera']==row['shot'],('Stale match camera',path);receipts[str(path)]=r
  pairs=sorted(Path(folder_name).glob('*-pair.jpg'));assert len(pairs)==4
  sheet(pairs,folder_name+'/contact.jpg',cols=1,width=1400)
 sheet([*files,folder/'modules.png',scale,eevee],folder/'contact.jpg')
 Path('build/final-provenance.json').write_text(json.dumps(dict(frames=receipts,count=len(receipts),scope='Every raw frame uses current exported geometry/images and the current presentation recipe. Native tree thin-leaf profiles read only exported baked images; separate source-field pairs are labeled. This is provenance, not a visual quality certificate.'),indent=2))
 print('FINAL PROVENANCE PASSED',len(receipts),'raw frames; contacts assembled')
if __name__=='__main__':main()
