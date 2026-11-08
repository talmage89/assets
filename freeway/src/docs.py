"""Five bounded final-gallery JPGs, from current exported presentation frames."""
import io,json,hashlib,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from review import main as review

def collage(sources,columns=2,width=1600):
 cell=width//columns;h=round(cell/1.5)+30;rows=(len(sources)+columns-1)//columns
 out=Image.new('RGB',(width,rows*h),(28,33,30));d=ImageDraw.Draw(out);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),17)
 for i,(path,label) in enumerate(sources):
  im=Image.open(path).convert('RGB');im.thumbnail((cell-8,h-38));x=i%columns*cell+4;y=i//columns*h+4
  out.paste(im,(x+(cell-8-im.width)//2,y));d.text((x+6,y+h-31),label,font=font,fill=(231,235,224))
 return out

def main():
 review();proof=json.loads(Path('build/final-provenance.json').read_text())
 crops=json.loads(Path('renders/fix-crops/cameras.json').read_text());assert len(crops)==9
 for row in crops.values():assert hashlib.sha256(Path(row['after']).read_bytes()).hexdigest()==row['after_sha256']
 folder=Path('renders/final');docs=Path('docs');docs.mkdir(exist_ok=True)
 spec={
  'hero-101.jpg':[(folder/'101/hero.png','Alder Junction')],
  'hero-202.jpg':[(folder/'202/hero.png','Cedar Hollow')],
  'plans.jpg':[(folder/'101/above_clean.png','Diamond / 101'),(folder/'202/above_clean.png','Sound-wall corridor / 202')],
  'details.jpg':[(folder/'101/pier_girders.png','Type IV girders and pier'),(folder/'101/bearings.png','Bearing seats and joint runoff'),(folder/'101/terminal.png','Ramp terminal'),(folder/'101/gore.png','Gore and attenuator'),(folder/'101/sign_structure.png','Guide-sign structure'),(folder/'101/guardrail_end.png','Guardrail and terminal')],
  'scale-eevee.jpg':[(folder/'scale.png','1.8 m figure and native car'),(Path('renders/final-eevee/101/hero.png'),'Exported scene / Eevee'),(folder/'101/barrier.png','Median barrier'),(folder/'202/cable_median.png','Cable median and backyards')]}
 rows={}
 for name,sources in spec.items():
  im=Image.open(sources[0][0]).convert('RGB') if len(sources)==1 else collage(sources,3 if name=='details.jpg' else 2)
  im.thumbnail((1600,16000));quality=94
  while True:
   data=io.BytesIO();im.save(data,format='JPEG',quality=quality,optimize=True,subsampling=0 if quality>75 else 2)
   if len(data.getvalue())<=200000:break
   quality-=2;assert quality>=40,(name,'Cannot retain a readable bounded gallery image')
  path=docs/name;path.write_bytes(data.getvalue())
  rows[name]=dict(bytes=path.stat().st_size,size=list(im.size),quality=quality,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),sources=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p,label in sources])
 assert len(list(docs.glob('*.jpg')))==5
 Path('build/docs.json').write_text(json.dumps(dict(images=rows,reviewed_export_frames=proof['count'],scope='Gallery assembly and byte/size/source checks; full-size visual judgment is recorded in REVIEW.md before committing these images.'),indent=2));print('DOCS PASSED',[(k,r['bytes'],r['quality']) for k,r in rows.items()])
if __name__=='__main__':main()
