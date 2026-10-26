"""Hash-checked contacts for a fence sublibrary; family docs are composed later."""
import argparse,json,hashlib
from pathlib import Path
from kit.contact import contact,review_sheet

def main(root,asset,assembly_name):
    ap=argparse.ArgumentParser();ap.add_argument('--renders',required=True);ap.add_argument('--final',action='store_true');a=ap.parse_args();f=Path(a.renders)
    meta=json.loads((f/'shots.json').read_text());paths=[f/(n+'.png') for n in meta]
    if a.final:
        digest=hashlib.sha256((root/'export'/f'{asset}.glb').read_bytes()).hexdigest()
        assert all(v['stage']=='final' and v['source_sha256']==digest for v in meta.values())
        eevee=f.parent/'final-eevee/hero_closed.png';em=json.loads((eevee.parent/'shots.json').read_text());assert em['hero_closed']['source_sha256']==digest;paths.append(eevee)
        assembly=f.parent/'assembly';am=json.loads((assembly/'shots.json').read_text());ad=hashlib.sha256((root/'export'/f'{assembly_name}.glb').read_bytes()).hexdigest()
        assert all(v['stage']=='final' and v['source_sha256']==ad for v in am.values())
        assert json.loads((root/'export'/f'{assembly_name}.json').read_text())['source_sha256']==digest
        paths.extend(assembly/(n+'.png') for n in am)
        review_sheet([[f/'front.png',f/'back.png'],[f/'side.png',f/'top.png'],[f/'gate.png',f/'gate_back.png'],[f/'posts.png',f/'scale.png']],f/'modules-contact.jpg',width=2000,title=asset+' / exported modules, pivots and scale')
    contact(paths,f/'contact.jpg',width=2200,title=asset+' / '+('exported GLB, Eevee and assembly' if a.final else 'source review'))
