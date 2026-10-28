"""Independent bark-only regression against a local pre-edit snapshot.

No source or reference pixels enter modeling. Run with Blender for the raw GLB
reader's mathutils dependency. Accessor byte equality includes geometry, UVs,
normals, tangents and Wind; embedded leaf-region equality protects all foliage.
Snapshot files are ignored rebuild outputs, never committed assets.
"""
import argparse,hashlib,io,json,struct,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def check(baseline,out,restore_tangent_rounding=False):
    trees=ROOT/'trees';a=GLB(baseline/'PinOak.glb');b=GLB(trees/'export/PinOak.glb')
    assert a.json['accessors']==b.json['accessors'],'Oak accessor schema changed'
    arrays=[];restore=[]
    tangents={p['attributes']['TANGENT'] for m in a.json['meshes'] for p in m['primitives']}
    for i in range(len(a.json['accessors'])):
        x=a.accessor(i).tobytes();y=b.accessor(i).tobytes()
        delta=np.abs(a.accessor(i).astype(float)-b.accessor(i).astype(float))
        if x!=y and restore_tangent_rounding and i in tangents:
            # Explicit map-only refresh: retain our own original tangent frame
            # when Blender's recalculation changes a few near-zero float bits.
            # Every other accessor and all layouts must still be exactly equal.
            assert np.count_nonzero(delta)<=4 and delta.max()<=.00011,'Tangent change exceeds rounding'
            restore.append(dict(index=i,changed_components=int(np.count_nonzero(delta)),max_component_delta=float(delta.max())))
        else:assert x==y,f'Oak accessor {i} changed'
        arrays.append(dict(index=i,byte_identical=x==y,changed_components=int(np.count_nonzero(delta)),max_component_delta=float(delta.max()),sha256=hashlib.sha256(y).hexdigest()))
    for key in ('meshes','nodes','materials','samplers','textures'):
        assert a.json[key]==b.json[key],f'Oak {key} changed'
    images=[]
    assert len(a.json['images'])==len(b.json['images']),'Image allocation changed'
    for i,row in enumerate(a.json['images']):
        x=np.asarray(Image.open(io.BytesIO(a.image(i))));y=np.asarray(Image.open(io.BytesIO(b.image(i))))
        assert x.shape==y.shape
        # Lower UV half is the bottom half in PNG image coordinates.
        leaf=x.shape[0]//2
        assert np.array_equal(x[leaf:],y[leaf:]),'Foliage texels changed: '+row['name']
        alpha_equal=bool(np.array_equal(x[:,:,3],y[:,:,3])) if x.shape[2]==4 else None
        if alpha_equal is not None:assert alpha_equal,'Alpha changed'
        images.append(dict(name=row['name'],leaf_region_byte_identical=True,alpha_byte_identical=alpha_equal,
                           changed_bark_channels=int(np.count_nonzero(x[:leaf]!=y[:leaf]))))
    hashes=json.loads((baseline/'hashes.json').read_text());maple=[]
    for name,expected in hashes.items():
        p=ROOT/name
        if name.endswith('PinOak.glb'):continue
        # Verification reports may be regenerated; they are not asset data.
        if p.suffix=='.json' and p.name not in ('growth.json','branchlet-atlas.json'):continue
        # Source containers, original procedural inputs, growth metadata,
        # shipped maps and existing maple GLB must not be rewritten.
        assert sha(p)==expected,'Maple file changed: '+name
        maple.append(dict(path=name,byte_identical=True,sha256=expected))
    assert (baseline/'RedMaple.glb').read_bytes()==(trees/'export/RedMaple.glb').read_bytes()
    if restore:
        image_payloads=[b.image(i) for i in range(len(images))]
        path=trees/'export/PinOak.glb';data=bytearray(path.read_bytes());offset=12
        while offset<len(data):
            size,kind=struct.unpack_from('<II',data,offset)
            if kind==0x004e4942:break
            offset+=8+size
        assert kind==0x004e4942,'Missing BIN chunk'
        for row in restore:
            i=row['index'];va=a.json['bufferViews'][a.json['accessors'][i]['bufferView']]
            vb=b.json['bufferViews'][b.json['accessors'][i]['bufferView']]
            assert va['byteLength']==vb['byteLength'] and va.get('byteStride')==vb.get('byteStride')
            start=offset+8+vb.get('byteOffset',0);old=va.get('byteOffset',0);length=va['byteLength']
            data[start:start+length]=a.binary[old:old+length]
        path.write_bytes(data);b=GLB(path)
        for i,row in enumerate(arrays):
            assert a.accessor(i).tobytes()==b.accessor(i).tobytes(),'Frame restoration changed another accessor'
            row.update(byte_identical=True,changed_components=0,max_component_delta=0.,sha256=hashlib.sha256(b.accessor(i).tobytes()).hexdigest())
        for i,payload in enumerate(image_payloads):assert b.image(i)==payload,'Image changed during frame restoration'
    result=dict(passed=True,oak_accessors=arrays,oak_layout_materials_nodes_byte_equivalent=True,
                original_tangent_rounding_restored=restore,oak_glb_sha256=sha(trees/'export/PinOak.glb'),
                oak_embedded_maps=images,maple_files=maple,maple_glb_sha256=sha(trees/'export/RedMaple.glb'),
                scope='Exact accessor bytes including tangents, unchanged layout/material constants, complete leaf region/alpha, and maple source/input/delivery file bytes. Proves preservation, not visual quality.')
    out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--restore-tangent-rounding',action='store_true',help='Explicit map-only refresh; retain original tangent bytes after all other preservation checks pass')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);check(args.baseline,args.out,args.restore_tangent_rounding)
