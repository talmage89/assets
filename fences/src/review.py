"""Only final GLB imagery becomes the three bounded documentation JPGs."""
import argparse,json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet
from kit.delivery_docs import jpg as bounded

p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');p.add_argument('--renders',required=True);a=p.parse_args();f=Path(a.renders)
meta=json.loads((f/'shots.json').read_text())
if a.final:
    digest=hashlib.sha256((ROOT/'fences/export/WoodPrivacy.glb').read_bytes()).hexdigest()
    assert all(v['stage']=='final' and v['source'].endswith('.glb') and v['source_sha256']==digest for v in meta.values())
    eevee_meta=json.loads((f.parent/'final-eevee/shots.json').read_text())
    assert eevee_meta['hero_closed']['source_sha256']==digest
    assembly_meta=json.loads((f.parent/'assembly/shots.json').read_text())
    assembly_digest=hashlib.sha256((ROOT/'fences/export/PrivacyAssembly.glb').read_bytes()).hexdigest()
    assert all(v['source_sha256']==assembly_digest and v['stage']=='final' for v in assembly_meta.values())
    assert json.loads((ROOT/'fences/export/PrivacyAssembly.json').read_text())['source_sha256']==digest
paths=[f/(n+'.png') for n in meta if (f/(n+'.png')).exists()]
eevee=f.parent/'final-eevee/hero_closed.png'
assembly=f.parent/'assembly'
if (assembly/'corner_good.png').exists():paths.extend([assembly/'corner_good.png',assembly/'corner_rails.png'])
if eevee.exists():paths.append(eevee)
contact(paths,f/'contact.jpg',width=2200,title='Wood privacy kit / exported GLB / Cycles + Eevee last',captions={str(eevee):'Eevee / exported GLB'})
if a.final:
    review_sheet([[f/'front.png',f/'back.png'],[f/'side.png',f/'top.png'],[f/'gate.png',f/'gate_back.png'],[f/'posts.png',f/'scale.png']],f/'modules-contact.jpg',width=2000,title='Privacy fence / module views / construction / scale')
    review_sheet([[f/'hero_open.png'],[f/'grain.png',f/'joinery.png',f/'hardware.png']],f/'construction-contact.jpg',width=2200,title='Rail side / original baked pine / physical hardware')
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from family_review import compose
    compose()
