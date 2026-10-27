"""Final GLB provenance, measured tone, contact sheets and three bounded docs."""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image
import review_lookdev as R
ROOT=Path(__file__).resolve().parents[1]


def doc(source,target):
 im=Image.open(source).convert('RGB');im.thumbnail((1600,16000),Image.Resampling.LANCZOS)
 target.parent.mkdir(parents=True,exist_ok=True)
 for quality in range(93,45,-2):
  im.save(target,quality=quality,optimize=True)
  if target.stat().st_size<=200000:return
 raise ValueError('Doc image exceeds 200 KB: '+str(target))


def main():
 p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--final',action='store_true');a=p.parse_args()
 root=Path(a.renders);folders=[root,root.parent/'final-eevee',root.parent/'final-pairs'];all_rows=[]
 digest=hashlib.sha256((ROOT/'export/AlderC150.glb').read_bytes()).hexdigest()
 for folder in folders:
  rows=json.loads((folder/'shots.json').read_text());all_rows.extend(rows.values())
  if any(r.get('stage')!='final' or Path(r['source']).suffix!='.glb' or r['source_sha256']!=digest for r in rows.values()):raise ValueError('Finals must come from current GLB: '+str(folder))
  sys.argv=['review_lookdev','--renders',str(folder)];R.main()
 if len({r['render_recipe_sha256'] for r in all_rows})!=1:raise ValueError('Final views use different shader or presentation revisions')
 views=['hero','front','side','back','top','front_detail','wheel_detail','interior','scale','lamps_lit']
 colors=['paint_'+name for name in ['Porcelain','Carbon','Aluminum','Graphite','Atlantic']]
 files=[root/(n+'.png') for n in views+colors]+[root.parent/'final-eevee/hero.png']
 for path in files:
  if not path.exists():raise FileNotFoundError(path)
 R.sheet(files,root/'contact.jpg',columns=3,width=800,captions={str(files[-1]):'hero / Eevee, thin-sheet glass'})
 R.sheet([root/(n+'.png') for n in ['front','side','back','top']],root/'turnaround.jpg',columns=2,width=800)
 # Front at full width, wheel/interior below at half width.
 canvas=Image.new('RGB',(1600,1700),(226,228,225))
 canvas.paste(R.panel(root/'front_detail.png',(1600,1100)),(0,0))
 canvas.paste(R.panel(root/'wheel_detail.png',(800,600)),(0,1100))
 canvas.paste(R.panel(root/'interior.png',(800,600)),(800,1100))
 canvas.save(root/'details.jpg',quality=94,optimize=True)
 R.sheet([root/(n+'.png') for n in colors],root/'five-colors.jpg',columns=2,width=800)
 # Reference photographs stay in ignored review outputs, never docs or textures.
 R.sheet([root.parent/'final-pairs'/(n+'-pair.jpg') for n in ['used_front','aged_front','used_rear','aged_rear']],root.parent/'final-pairs/used-pairs-contact.jpg',columns=1,width=1600)
 if a.final:
  for name,source in [('hero','hero.jpg'),('details','details.jpg'),('five-colors','five-colors.jpg')]:doc(root/source,ROOT/'docs'/(name+'.jpg'))
 (root/'provenance.json').write_text(json.dumps(dict(source='export/AlderC150.glb',source_sha256=digest,views=len(files),photo_pairs=4,method='Fresh GLB import; only embedded baked maps and delivery factory uniforms. No high scene or procedural manufacturing shaders.'),indent=2))
 print('FINAL_REVIEW',len(files),'GLB images, four pairs, three bounded docs JPGs')
if __name__=='__main__':main()
