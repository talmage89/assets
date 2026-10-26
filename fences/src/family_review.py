"""Compose the batch's five final docs JPGs after all deliveries and fixes."""
import json,hashlib
from pathlib import Path
from kit.contact import review_sheet,contact
from kit.delivery_docs import jpg
ROOT=Path(__file__).resolve().parents[1]

def verified(folder,asset,assembly):
    digest=hashlib.sha256((folder/'export'/f'{asset}.glb').read_bytes()).hexdigest()
    shots=json.loads((folder/'renders/final/shots.json').read_text());assert all(x['stage']=='final' and x['source_sha256']==digest for x in shots.values())
    ev=json.loads((folder/'renders/final-eevee/shots.json').read_text());assert ev['hero_closed']['source_sha256']==digest
    ad=hashlib.sha256((folder/'export'/f'{assembly}.glb').read_bytes()).hexdigest()
    am=json.loads((folder/'renders/assembly/shots.json').read_text());assert all(x['stage']=='final' and x['source_sha256']==ad for x in am.values())
    assert json.loads((folder/'export'/f'{assembly}.json').read_text())['source_sha256']==digest
    assert json.loads((folder/'build/delivery-check.json').read_text())['passed']
    assert json.loads((folder/'build/construction-check.json').read_text())['passed']
    return folder/'renders/final'

def compose():
    privacy=verified(ROOT,'WoodPrivacy','PrivacyAssembly');picket=verified(ROOT/'picket','WhitePicket','PicketAssembly');chain=verified(ROOT/'chain-link','ChainLink','ChainAssembly')
    out=ROOT/'renders/family';out.mkdir(parents=True,exist_ok=True);docs=ROOT/'docs';docs.mkdir(exist_ok=True)
    for f,name in [(privacy,'privacy'),(picket,'picket'),(chain,'chainlink')]:jpg(f.parent/'assembly/corner_good.png',docs/(name+'-hero.jpg'))
    review_sheet([[privacy/'hardware.png',privacy/'gate_back.png'],[picket/'paint.png',picket/'hardware.png'],[chain/'mesh.png',chain/'joinery.png']],out/'construction.jpg',width=2200,title='Original baked fence family / privacy, painted picket, galvanized chain-link')
    review_sheet([[f/'pieces.png',f/'front.png',f/'back.png',f/'scale.png'] for f in (privacy,picket,chain)],out/'modules.jpg',width=2600,title='Fence modules / per-type inventory, good side, rail side and 1.8 m scale')
    jpg(out/'construction.jpg',docs/'family-construction.jpg');jpg(out/'modules.jpg',docs/'family-modules.jpg')
    for obsolete in ('privacy-construction.jpg','privacy-modules.jpg'):(docs/obsolete).unlink(missing_ok=True)
    paths=[]
    for f in (privacy,picket,chain):
        shots=json.loads((f/'shots.json').read_text());paths.extend(f/(n+'.png') for n in shots)
        paths.extend([f.parent/'final-eevee/hero_closed.png',f.parent/'assembly/corner_good.png',f.parent/'assembly/corner_rails.png'])
    contact(paths,out/'contact.jpg',width=2600,title='Complete fence family / all exported GLB studio, Eevee and assembly shots')
    assert len(list(docs.glob('*.jpg')))==5
