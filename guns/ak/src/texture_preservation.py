"""Gate the texture round against the handed-off exported geometry and rig.

Positions/normals/UV/weights, accessor/node/mesh layout, skin, animations and
scene structure are byte-hashed. Exporter-derived tangents are recorded
separately: Blender can round a few regenerated components by 0.0001.
No baseline is recorded by make.
"""
from pathlib import Path
import argparse,hashlib,json,struct
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
        assert all(geometry_equal(measured[n],expected[n]) for n in NAMES),'Geometry, UV, normals, weights, rig, clips or layout changed'
        (BASE/'build/texture-preservation.json').write_text(json.dumps(dict(passed=True,signatures=measured,scope=__doc__),indent=2))
        print('TEXTURE ROUND: all five exports have byte-identical geometry, normals, UVs, weights, rig, clips and layout; derived tangents recorded separately')
if __name__=='__main__':main()
