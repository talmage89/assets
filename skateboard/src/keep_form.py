"""Raw-accessor accepted-form comparison; material/UV edits may reorder vertices.

Season must retain every oriented triangle. Beat may change only front-left
wheel geometry for its requested skid flat, with identical triangle counts.
"""
from pathlib import Path
import json,struct,sys
import numpy as np

def load(path):
    data=path.read_bytes();offset=12;binary=None;g=None
    while offset<len(data):
        size,kind=struct.unpack_from('<II',data,offset);payload=data[offset+8:offset+8+size];offset+=size+8
        if kind==0x4e4f534a:g=json.loads(payload)
        elif kind==0x004e4942:binary=payload
    def accessor(i):
        a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];dt=np.dtype({5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);n={'VEC3':3,'SCALAR':1}[a['type']]
        return np.ndarray((a['count'],n),dtype=dt,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',dt.itemsize*n),dt.itemsize)).copy()
    result={}
    for node in g['nodes']:
        if 'mesh' not in node:continue
        tris=[]
        for p in g['meshes'][node['mesh']]['primitives']:
            position=accessor(p['attributes']['POSITION']);indices=accessor(p['indices']).ravel().reshape(-1,3)
            for tri in position[indices]:
                points=[tuple(row) for row in np.rint(tri*1e7).astype(np.int64)]
                tris.append(min(tuple(points[k:]+points[:k]) for k in range(3)))
        result[node['name']]=sorted(tris)
    transforms={n['name']:{k:n[k] for k in ('matrix','rotation','translation','scale') if k in n} for n in g['nodes']}
    return result,transforms

result={}
for state in (sys.argv[1:] or ('season','beat')):
    old,ox=load(Path(f'build/accepted/export/{state}.glb'));new,nx=load(Path(f'export/{state}.glb'))
    assert ox==nx,(state,'node frames changed')
    assert old.keys()==new.keys(),(state,'mesh set changed')
    changed=[]
    for name in old:
        assert len(old[name])==len(new[name]),(state,name,'triangle count changed')
        if old[name]!=new[name]:changed.append(name)
    assert changed==(['Wheel_Front_LMesh'] if state=='beat' else []),(state,changed)
    result[state]=dict(node_frames_equal=True,oriented_triangle_positions_equal_except=changed,quantization_m=1e-7,triangles=sum(map(len,new.values())))
Path('build/kept-form.json').write_text(json.dumps(result,indent=2));print(result)
