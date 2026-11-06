"""Native accepted/fixed comparisons. Camera equality is checked, not assumed."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
CASES={'corner-entry':('midwest','corner'),'iron-piers':('northeast','iron_detail'),'scrolls':('midwest','cornice_profile'),'ghost-sign':('midwest','ghost'),'store-glass':('midwest','storefront'),'hero-wear':('midwest','hero'),'dusk-pools':('midwest','dusk')}

def generate():
 out=Path('renders/fixes');out.mkdir(parents=True,exist_ok=True)
 for label,(region,name) in CASES.items():
  before=Path('build/accepted-workspace/downtown/renders')/('matches' if region=='northeast' else 'checkpoint')/region
  after=Path('renders/proof')/region
  ca=json.loads((before/'provenance.json').read_text())[name]['camera'];cb=json.loads((after/'provenance.json').read_text())[name]['camera']
  assert ca==cb,(label,'cameras differ')
  a=Image.open(before/(name+'.png')).convert('RGB');b=Image.open(after/(name+'.png')).convert('RGB');assert a.size==b.size and a.width>=800
  # Iron pier detail keeps at least 800 native pixels; no render resampling.
  if name=='foster':
   y=round(a.height*.57);a=a.crop((0,y,a.width,a.height));b=b.crop((0,y,b.width,b.height))
  im=Image.new('RGB',(a.width*2,a.height+32),(235,233,227));im.paste(a,(0,32));im.paste(b,(a.width,32));d=ImageDraw.Draw(im)
  d.text((15,9),'Accepted caf80a6 / native exported pixels',fill=(30,30,30));d.text((a.width+15,9),'Fixed / same camera / native exported pixels',fill=(30,30,30));im.save(out/(label+'.jpg'),quality=95,optimize=True)
if __name__=='__main__':generate()
