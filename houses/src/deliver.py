"""Per-seed stock glTF with byte-identical, shared external family images.

A compact embedded GLB in build/ is an intermediate only. Delivery strips its
image views, leaving geometry in each seed's bin and common relative PNG URIs.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import tiling,gltf
from build import build,save
from plan import load,PROOF_SEEDS
from lookdev import prepare
from glb_budget import compact,read
from delivery_io import dependencies,bundle_hash


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_delivery(path):
    """Feed the kit's independent accessor reader a standard external buffer."""
    raw=object.__new__(gltf.GLB);raw.json=json.loads(path.read_text())
    assert len(raw.json['buffers'])==1
    raw.binary=(path.parent/raw.json['buffers'][0]['uri']).read_bytes()
    raw.parents={c:i for i,n in enumerate(raw.json['nodes']) for c in n.get('children',[])}
    return raw



def externalize(source,out,images_folder=Path('textures/ship'),max_images=15):
    doc,binary=read(source);out.parent.mkdir(parents=True,exist_ok=True)
    folder=out.parent/'textures';folder.mkdir(parents=True,exist_ok=True)
    known={digest(p):p for p in sorted(images_folder.glob('*.png'))}
    image_names=[]
    for im in doc['images']:
        view=doc['bufferViews'][im.pop('bufferView')];offset=view.get('byteOffset',0)
        payload=binary[offset:offset+view['byteLength']];key=hashlib.sha256(payload).hexdigest()
        assert key in known, 'Exporter changed a delivered image or emitted an extra image'
        named=images_folder/(im.get('name','')+'.png')
        # Equal normal fields in different named sets still retain stable
        # canonical URIs; directory traversal order must not choose a color.
        chosen=named if named.exists() and digest(named)==key else known[key]
        path=folder/chosen.name
        if not path.exists() or path.read_bytes()!=payload:path.write_bytes(payload)
        im['uri']='textures/'+path.name;image_names.append(path.name)
    assert 12<=len(set(image_names))<=max_images
    # Only geometry views remain. No embedded image payload or dead buffer range.
    used=sorted({a['bufferView'] for a in doc['accessors']});remap={};views=[];output=bytearray()
    for old in used:
        output.extend(b'\0'*(-len(output)%4));v=copy.deepcopy(doc['bufferViews'][old]);start=v.get('byteOffset',0)
        payload=binary[start:start+v['byteLength']];v['byteOffset']=len(output);v['buffer']=0
        output.extend(payload);remap[old]=len(views);views.append(v)
    for a in doc['accessors']:a['bufferView']=remap[a['bufferView']]
    doc['bufferViews']=views;doc['buffers']=[dict(byteLength=len(output),uri=out.with_suffix('.bin').name)]
    out.with_suffix('.bin').write_bytes(output);out.write_text(json.dumps(doc,separators=(',',':'))+'\n')
    return dict(gltf_bytes=out.stat().st_size,bin_bytes=len(output),images=sorted(image_names),bundle_sha256=bundle_hash(out))


def export_house(seed,plan=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    base=Path(f'build/family/form-{seed}.blend');save(build(load(seed,plan)),base,export=False)
    game=Path(f'build/family/game-{seed}.blend');meta=prepare(base,game,Path('textures/ship'))
    meta['stage']='baked game delivery; shared external images';game.with_suffix('.json').write_text(json.dumps(meta,indent=2))
    moving={bpy.data.objects[n] for n in ('FrontDoor','PatioDoor','ServiceDoor')}
    static=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent not in moving]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in static:ob.select_set(True)
    bpy.context.view_layer.objects.active=static[0];bpy.ops.object.join();static[0].name='House_Static'
    embedded=Path(f'build/family/house-{seed}.glb');tiling.export(embedded);compact(embedded)
    out=Path(f'export/Hearthfield-{seed}.gltf');size=externalize(embedded,out)
    out.with_suffix('.json').write_text(json.dumps(meta,indent=2))
    print('DELIVERED',seed,meta['triangles'],size['gltf_bytes']+size['bin_bytes'],flush=True)
    doc,_=read(embedded)
    return dict(seed=seed,triangles=meta['triangles'],materials=len(doc['materials']),meshes=len(doc['meshes']),**size)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)));p.add_argument('--plan',type=Path)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);seeds=list(dict.fromkeys(map(int,a.seeds.split(','))))
    assert seeds,'Select at least one seed'
    # Generated exports from a previous seed list are not part of this delivery.
    expected={f'Hearthfield-{seed}{suffix}' for seed in seeds for suffix in ('.gltf','.bin','.json')}
    for old in Path('export').glob('Hearthfield-*'):
        if old.suffix in ('.gltf','.bin','.json') and old.name not in expected:old.unlink()
    # Publish every family set even when this selection contains no veneer.
    # Refresh old baked images so parameter changes require no manual clean.
    folder=Path('export/textures');folder.mkdir(parents=True,exist_ok=True)
    for image in Path('textures/ship').glob('T_*.png'):
        target=folder/image.name;payload=image.read_bytes()
        if not target.exists() or target.read_bytes()!=payload:target.write_bytes(payload)
    rows=[export_house(seed,a.plan) for seed in seeds]
    images=list(Path('export/textures').glob('T_House*.png'));assert len(images)==15
    Path('build/family/delivery.json').write_text(json.dumps(dict(rows=rows,shared_png_bytes=sum(p.stat().st_size for p in images),
        total_geometry_bytes=sum(r['gltf_bytes']+r['bin_bytes'] for r in rows),shared_images=len(images)),indent=2))
