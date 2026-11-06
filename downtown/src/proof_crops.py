"""Native-resolution before/after panels; never committed as docs."""
from pathlib import Path
from PIL import Image,ImageDraw
CASES={
 'cornice':('checkpoint/midwest/cornice.png','whole'),
 'cast-hood':('matches/northeast/foster.png','top'),
 'washed-sill':('checkpoint/midwest/window.png','whole'),
 'iron-piers':('matches/northeast/foster.png','bottom'),
 'canvas':('checkpoint/midwest/storefront.png','whole'),
 'corner-entry':('checkpoint/midwest/corner.png','whole'),
 'alley':('checkpoint/midwest/rear.png','whole')}
def generate():
 out=Path('renders/fixes');out.mkdir(parents=True,exist_ok=True)
 for label,(shot,area) in CASES.items():
  a=Image.open(Path('build/before/renders')/shot).convert('RGB');b=Image.open(Path('renders')/shot).convert('RGB')
  width=min(a.width,b.width);height=min(a.height,b.height,1000 if area!='whole' else 100000)
  assert width>=800
  aa=(a.width-width)//2;bb=(b.width-width)//2
  ay=a.height-height if area=='bottom' else 0;by=b.height-height if area=='bottom' else 0
  a=a.crop((aa,ay,aa+width,ay+height));b=b.crop((bb,by,bb+width,by+height))
  im=Image.new('RGB',(2*width,height+32),(235,233,227));im.paste(a,(0,32));im.paste(b,(width,32));d=ImageDraw.Draw(im);d.text((15,9),'Before / 889d811 / native pixels',fill=(30,30,30));d.text((width+15,9),'After / exported baked buildings / native pixels',fill=(30,30,30));im.save(out/(label+'.jpg'),quality=95,optimize=True)
if __name__=='__main__':generate()
