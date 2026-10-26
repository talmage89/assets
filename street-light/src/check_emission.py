"""Inspect real GLB materials and texture sharing, separately from appearance review."""
import argparse,json,struct
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args();raw=Path(a.source).read_bytes();length=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+length]);mats=g['materials']
emitters=[m for m in mats if max(m.get('emissiveFactor',[0,0,0]))>0];glass=[m for m in mats if m.get('extensions',{}).get('KHR_materials_transmission',{}).get('transmissionFactor',0)>.9]
assert len(mats)==3 and len(g['images'])==3 and len(g['meshes'])==1
assert len(emitters)==len(glass)==1
m=emitters[0];assert m['emissiveTexture']['index']==m['pbrMetallicRoughness']['baseColorTexture']['index'],'Emission must reuse original shared BaseColor texture'
strength=m.get('extensions',{}).get('KHR_materials_emissive_strength',{}).get('emissiveStrength',1)
assert strength>0
r=dict(passed=True,source=a.source,meshes=1,materials=3,images=3,emissive_strength=strength,emission_basecolor_texture_shared=True,transmission=glass[0]['extensions']['KHR_materials_transmission']['transmissionFactor'],ior=glass[0].get('extensions',{}).get('KHR_materials_ior',{}).get('ior',1.5),scope='actual serialized GLB material properties; appearance inspected separately')
Path(a.out).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
