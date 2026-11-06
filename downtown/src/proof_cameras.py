"""Freeze accepted cameras; add a full-height raking view of an iron pier."""
import json
from pathlib import Path

def iron_detail():
 from plan import generate
 b=generate(613,'northeast')['lots'][3];right=b['x']+b['width']/2
 # One stop above the street overview, shared by historical and fixed views,
 # so the shaded dark casting can be judged without recoloring its paint.
 return dict(region='northeast',shot=dict(location=[right+.80,-4.,1.70],target=[right-.17,0,1.62],lens=62,aspect=.65,exposure=.65))

def main():
 from proof_crops import CASES
 out={}
 for region,name in CASES.values():
  base=Path('build/accepted-workspace/downtown/renders')/('matches' if region=='northeast' else 'checkpoint')/region
  out[name]=dict(region=region,shot=json.loads((base/'provenance.json').read_text())[name]['camera'])
 Path('build/proof-cameras.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
