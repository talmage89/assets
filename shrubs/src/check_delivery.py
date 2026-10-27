"""Verify finalized botanical positions, normals, Wind and shared delivery images.

Uses the shared serialization audit implementation (same invariant for both
botanical families); adds independent per-species budgets and root checks.
"""
import sys,json
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB
from kit.botanical_delivery import main
main()
a=sys.argv[sys.argv.index('--')+1:];path=Path(a[a.index('--glb')+1]);raw=GLB(path)
counts={}
for mesh in raw.json['meshes']:
    species='Boxwood' if mesh['name'].startswith('Boxwood') else 'Hydrangea'
    counts[species]=counts.get(species,0)+sum(raw.json['accessors'][p['indices']]['count']//3 for p in mesh['primitives'])
assert set(counts)=={'Boxwood','Hydrangea'} and all(2000<=n<=6000 for n in counts.values()),counts
assert len(raw.json['images'])==3 and len(raw.json['materials'])==2
for species in counts:
    root=next(n for n in raw.json['nodes'] if n['name']==species)
    assert root.get('translation',[0,0,0])==[0,0,0]
    assert len(root['children'])==2
report=Path(a[a.index('--out')+1]);data=json.loads(report.read_text());data['triangles_by_species']=counts;data['shared_image_count']=3;data['material_count']=2;report.write_text(json.dumps(data,indent=2))

# Each PBR material references the same image identities; no hidden second set.
images={}
for mat in raw.json['materials']:
    pbr=mat['pbrMetallicRoughness']
    channels={'BaseColor':pbr['baseColorTexture'],'Normal':mat['normalTexture'],'ORM':pbr['metallicRoughnessTexture']}
    assert raw.json['textures'][mat['occlusionTexture']['index']]['source']==raw.json['textures'][channels['ORM']['index']]['source']
    for channel,ref in channels.items():
        source=raw.json['textures'][ref['index']]['source']
        if channel in images:assert images[channel]==source
        else:images[channel]=source
for species in counts:
    a=json.loads(Path('build/botanical-check.json' if species=='Boxwood' else 'build/hydrangea/botanical-check.json').read_text())
    if species=='Boxwood':signatures=a['material_definition_sha256']
    else:assert signatures==a['material_definition_sha256']
data['shared_images_by_channel']=images;report.write_text(json.dumps(data,indent=2))
