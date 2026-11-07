"""Five bounded final JPGs from audited exported-building renders.

Run only after native-size visual review. No photographic references are used.
"""
import hashlib,io,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
from review import audit_checkpoint
from kit.fonts import find_font
BASE=Path('renders/checkpoint');OUT=Path('docs');rows=[]

def save(im,name,sources):
 im=im.convert('RGB')
 if im.width>1600:im.thumbnail((1600,10000),Image.Resampling.LANCZOS)
 for quality in range(94,39,-1):
  buffer=io.BytesIO();im.save(buffer,'JPEG',quality=quality,optimize=True)
  if len(buffer.getvalue())<=200000:break
 else:raise ValueError('Cannot preserve the docs image inside 200 KB')
 path=OUT/name;path.write_bytes(buffer.getvalue())
 rows.append(dict(path=str(path),bytes=path.stat().st_size,size=list(im.size),quality=quality,sources=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sources]))
 print('DOC',path,im.size,path.stat().st_size,quality)

def grid(cases,name,columns=2,height=470):
 width=800;image=Image.new('RGB',(columns*width,((len(cases)+columns-1)//columns)*height),(225,223,215));draw=ImageDraw.Draw(image)
 font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),21);sources=[]
 for i,(title,path) in enumerate(cases):
  p=BASE/path;sources.append(p);a=Image.open(p).convert('RGB');a.thumbnail((width-12,height-42),Image.Resampling.LANCZOS)
  x=i%columns*width;y=i//columns*height;image.paste(a,(x+(width-a.width)//2,y+35+(height-42-a.height)//2));draw.text((x+14,y+7),title,font=font,fill=(27,32,29))
 save(image,name,sources)

def main():
 OUT.mkdir(exist_ok=True);audit_checkpoint(BASE)
 for name in ('hero','dusk'):save(Image.open(BASE/'midwest'/(name+'.png')),name+'.jpg',[BASE/'midwest'/(name+'.png')])
 towns=[('Midwest · 411','midwest'),('Western · 512','western'),('Northeast · 613','northeast'),('Southern · 714','southern')]
 grid([(title,region+'/across.png') for title,region in towns],'towns.jpg',height=310)
 grid([('Storefront and recessed entry','midwest/storefront.png'),('Keyed hood and washed sill','northeast/hood.png'),('Cornice scrolls','midwest/cornice_profile.png'),('Stone corner entry','midwest/corner.png'),('Ghost paint and former neighbor','midwest/ghost.png'),('Alley fire escape','midwest/escape.png')],'details.jpg',height=520)
 grid([(title+' · roofs and alleys',region+'/rear.png') for title,region in towns],'rears.jpg',height=470)
 assert len(list(OUT.glob('*.jpg')))==5
 Path('build/docs.json').write_text(json.dumps(dict(images=rows,scope='Audited exported geometry/maps; downscaled JPGs only. Full-size visual review is recorded separately in REVIEW.md.'),indent=2)+'\n')
if __name__=='__main__':main()
