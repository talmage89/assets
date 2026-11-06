"""Raw external-byte equality, actual primitive counts, and fresh image reuse.

Independent of source construction: verifies the shipping format and maps.
"""
import hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from PIL import Image
from deliver import read
from strip_delivery import part_materials


def check():
    rows=[];bpy.ops.wm.read_factory_settings(use_empty=True)
    for seed in (201,202,203,204):
        path=Path(f'export/CommercialStrip-{seed}.gltf');doc=json.loads(path.read_text());meta=json.loads(path.with_suffix('.json').read_text());raw,binary=read(Path(f'build/strip-look/strip-{seed}.glb'))
        assert doc['meshes']==raw['meshes'] and len(doc['accessors'])==len(raw['accessors'])
        payload=path.with_suffix('.bin').read_bytes()
        for a,c in zip(raw['accessors'],doc['accessors']):
            va=raw['bufferViews'][a['bufferView']];vc=doc['bufferViews'][c['bufferView']];x=va.get('byteOffset',0);y=vc.get('byteOffset',0)
            assert binary[x:x+va['byteLength']]==payload[y:y+vc['byteLength']],('Changed external accessor',seed)
        memory=0;image_bytes=0;images={}
        for before,after in zip(raw['images'],doc['images']):
            v=raw['bufferViews'][before['bufferView']];start=v.get('byteOffset',0);imagepath=(path.parent/after['uri']).resolve();data=imagepath.read_bytes()
            assert data==binary[start:start+v['byteLength']],('External image bytes changed',imagepath)
            width,height=Image.open(imagepath).size;memory+=width*height*4/3/1024**2;image_bytes+=len(data);images[str(imagepath)]=hashlib.sha256(data).hexdigest()
        parts=part_materials(doc,meta);fixed=parts['BuildingStatic']['draw_primitives'];building=sum(v['draw_primitives'] for k,v in parts.items() if k=='BuildingStatic' or k.startswith('Bay_'))
        assert fixed<=7 and all(v['draw_primitives']<=3 for k,v in parts.items() if k.startswith('Bay_'))
        primitives=sum(v['draw_primitives'] for v in parts.values());assert primitives<160,(seed,primitives)
        before=set(bpy.data.images);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        used={str(Path(im.filepath).resolve()):im.as_pointer() for im in bpy.data.images if im.filepath and Path(im.filepath).exists()}
        assert set(images)<=set(used),('Missing fresh image paths',set(images)-set(used))
        rows.append(dict(seed=seed,passed=True,gltf_bytes=path.stat().st_size,bin_bytes=len(payload),geometry_bytes=path.stat().st_size+len(payload),shared_image_bytes=image_bytes,compressed_gpu_mib=memory,building_triangles=meta['building_triangles'],placed_triangles=meta['total_triangles'],unique_triangles=meta['unique_mesh_triangles'],static_building_primitives=fixed,building_primitives=building,seed_primitives=primitives,material_states=len(doc['materials']),fixture_lights=len(doc['extensions']['KHR_lights_punctual']['lights']),parts=parts))
    cached={str(Path(im.filepath).resolve()):im.as_pointer() for im in bpy.data.images if im.filepath and Path(im.filepath).exists()}
    assert len(cached)==len([im for im in bpy.data.images if im.filepath and Path(im.filepath).exists()]),'Duplicate decoded image path across centers'
    bpy.ops.import_scene.gltf(filepath=str(Path('export/CommercialStrip-201.gltf').resolve()))
    after={str(Path(im.filepath).resolve()):im.as_pointer() for im in bpy.data.images if im.filepath and Path(im.filepath).exists()}
    assert after==cached,'Repeated seed changed image identities'
    Path('build/strip-look/external-check.json').write_text(json.dumps(dict(passed=True,rows=rows,shared_decoded_images=len(cached),scope=__doc__),indent=2)+'\n')
    print('STRIP EXTERNAL CHECK four seeds + repeated default:',len(cached),'shared image identities PASS')

if __name__=='__main__':check()
