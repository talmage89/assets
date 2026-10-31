"""Gate the texture round against the handed-off exported geometry and rig.

The rifle retains exact geometry/UV/rig/clip data and JSON semantics. Its
decoded maps allow at most 1/255 per channel at 128 texels per map versus the
reviewed accepted bake; PNG compression and buffer allocation are incidental.
Detachables retain oriented corner attributes and node frames byte-for-byte;
their density and inverse atlas surface samples are checked independently by
atlas_verify. The old/new review also checks UV transforms and tangent direction.
No baseline is recorded by make.
"""
from pathlib import Path
import argparse,hashlib,json,struct
import numpy as np
from bake_identity import verify as verify_bake
BASE=Path(__file__).resolve().parents[1]
NAMES=('ak','magazine_loaded','magazine_empty','cartridge','case')

def signature(path):
    data=path.read_bytes();length=struct.unpack_from('<I',data,12)[0]
    g=json.loads(data[20:20+length]);binary=data[28+length:]
    images={i['bufferView'] for i in g['images']}
    tangents={g['accessors'][p['attributes']['TANGENT']]['bufferView']
              for m in g['meshes'] for p in m['primitives'] if 'TANGENT' in p['attributes']}
    chunks=[binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
            for i,v in enumerate(g['bufferViews']) if i not in images]
    structure={k:g[k] for k in ('nodes','skins','animations','meshes','accessors','scenes') if k in g}
    return dict(non_image_buffers=hashlib.sha256(b''.join(chunks)).hexdigest(),
                geometry_buffers=hashlib.sha256(b''.join(binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']] for i,v in enumerate(g['bufferViews']) if i not in images|tangents)).hexdigest(),
                structure=hashlib.sha256(json.dumps(structure,sort_keys=True).encode()).hexdigest())

def geometry_equal(a,b):return all(a[k]==b[k] for k in ('geometry_buffers','structure'))

def detachable_signature(path):
    """Hash oriented non-UV corners, independent of exporter vertex indexing."""
    data=path.read_bytes();length=struct.unpack_from('<I',data,12)[0]
    g=json.loads(data[20:20+length]);binary=data[28+length:]
    def accessor(index):
        a=g['accessors'][index];v=g['bufferViews'][a['bufferView']]
        dtype=np.dtype({5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']])
        width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
        return np.ndarray((a['count'],width),dtype,buffer=binary,
            offset=v.get('byteOffset',0)+a.get('byteOffset',0),
            strides=(v.get('byteStride',width*dtype.itemsize),dtype.itemsize))
    triangles=[];schemas=[]
    for mesh in g['meshes']:
        for p in mesh['primitives']:
            assert p.get('mode',4)==4
            attributes={k:accessor(i) for k,i in sorted(p['attributes'].items())
                        if k not in ('TEXCOORD_0','TANGENT')}
            schemas.append([(k,a.dtype.str,a.shape[1]) for k,a in attributes.items()])
            for indices in accessor(p['indices']).reshape(-1,3):
                corners=[b''.join(a[i].tobytes() for a in attributes.values()) for i in indices]
                start=min(range(3),key=corners.__getitem__)
                triangles.append(b''.join(corners[start:]+corners[:start]))
    return dict(triangles=len(triangles),
        attributes=hashlib.sha256(b''.join(sorted(triangles))).hexdigest(),
        structure=hashlib.sha256(json.dumps(dict(schemas=schemas,
            nodes=g['nodes'],scenes=g['scenes']),sort_keys=True).encode()).hexdigest())

def main():
    p=argparse.ArgumentParser();p.add_argument('--record-from');a=p.parse_args()
    accepted=BASE/'src/accepted_texture_round.json'
    folder=BASE/a.record_from if a.record_from else BASE/'export'
    measured={n:signature(folder/(n+'.glb')) for n in NAMES}
    if a.record_from:
        assert not accepted.exists(),'Never replace the handed-off baseline'
        accepted.write_text(json.dumps(measured,indent=2)+'\n')
    else:
        expected=json.loads(accepted.read_text())
        assert geometry_equal(measured['ak'],expected['ak']),'Rifle geometry, UV, normals, weights, rig, clips or layout changed'
        baseline=json.loads((BASE/'src/accepted_detachable_geometry.json').read_text())
        bake=json.loads((BASE/'src/accepted_bake.json').read_text())
        assert bake.get('historical_handoff_sha256',bake['accepted_glb_sha256'])==baseline['main_sha256'],'Bake reference is not descended from the accepted handoff'
        textures=verify_bake(folder/'ak.glb',bake)
        main_sha256=hashlib.sha256((folder/'ak.glb').read_bytes()).hexdigest()
        detached={n:detachable_signature(folder/(n+'.glb')) for n in NAMES[1:]}
        assert detached==baseline['geometry'],'Detachable geometry, normals, attributes or origins changed'
        (BASE/'build/texture-preservation.json').write_text(json.dumps(dict(passed=True,signatures=measured,
            detachable_geometry=detached,main_sha256=main_sha256,accepted_main_sha256=baseline['main_sha256'],
            decoded_textures=textures,scope=__doc__),indent=2))
        print('PRESERVED: exact rifle non-image data/JSON semantics; accepted decoded maps within sparse 1/255 rounding; detachable oriented geometry, normals, attributes and origins; remapped UVs verified separately')
if __name__=='__main__':main()
