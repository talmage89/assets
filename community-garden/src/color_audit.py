"""Measure owned garden COLOR_0 preservation through full-site serialization."""
from pathlib import Path
import json
import numpy as np


class Document:
    def __init__(self,path):
        path=Path(path);self.data=json.loads(path.read_text())
        self.binary=[(path.parent/b['uri']).read_bytes() for b in self.data['buffers']]
        self.nodes={n['name']:n for n in self.data['nodes']}
    def array(self,index):
        a=self.data['accessors'][index];v=self.data['bufferViews'][a['bufferView']]
        dtype=np.dtype({5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
        result=np.ndarray((a['count'],width),dtype=dtype,buffer=self.binary[v['buffer']],offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',width*dtype.itemsize),dtype.itemsize)).astype(float)
        if a.get('normalized'):result/=np.iinfo(dtype).max
        return result
    def colored(self,node,family):
        rows=[]
        for p in self.data['meshes'][node['mesh']]['primitives']:
            ma=self.data['materials'][p['material']]
            if not ma['name'].startswith(family):continue
            assert 'COLOR_0' in p['attributes'],('Missing color',node['name'],ma['name'])
            rows.append(np.concatenate([self.array(p['attributes']['POSITION']),self.array(p['attributes']['COLOR_0'])[:,:3]],axis=1))
        assert rows,('Missing tinted primitive',node['name'],family)
        # Re-import may split extra normal/UV seams. Repeated identical
        # position/color records do not constitute another tint sample.
        a=np.unique(np.concatenate(rows),axis=0);order=np.lexsort(tuple(a[:,i] for i in (5,4,3,2,1,0)))
        return a[order]


def compare(garden,site):
    source=Document(garden);target=Document(site);seen=set();rows=[]
    for name,node in source.nodes.items():
        if 'mesh' not in node:continue
        families={source.data['materials'][p['material']]['name'].split('.')[0] for p in source.data['meshes'][node['mesh']]['primitives'] if 'COLOR_0' in p['attributes']}
        if not families:continue
        placed=target.nodes[name]
        for family in sorted(families):
            key=(node['mesh'],placed['mesh'],family)
            if key in seen:continue
            seen.add(key);a=source.colored(node,family);b=target.colored(placed,family)
            assert a.shape==b.shape,('Tinted vertex count differs',name,family,a.shape,b.shape)
            assert np.allclose(a[:,:3],b[:,:3],atol=2e-6,rtol=0),('Tinted vertex positions differ',name,family)
            error=float(np.max(np.abs(a[:,3:]-b[:,3:])))
            # Blender imports glTF color into BYTE_COLOR (sRGB storage): its
            # worst half-step near white is .00446 linear, plus U16 export.
            assert error<=.0046,('Garden tint lost in site export',name,family,error)
            rows.append(dict(node=name,material=family,vertices=len(a),max_linear_rgb_error=error,source_rgb_min=a[:,3:].min(0).tolist(),site_rgb_min=b[:,3:].min(0).tolist()))
    assert rows
    return dict(passed=True,unique_mesh_material_pairs=len(rows),max_linear_rgb_error=max(r['max_linear_rgb_error'] for r in rows),pairs=rows,scope='actual local vertex positions and RGB streams; .0046 tolerance for Blender BYTE_COLOR import plus normalized U16 export')
