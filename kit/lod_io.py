"""LOD-only glTF I/O. Never rewrites a source; keeps unknown JSON and attributes.

Intentionally separate from the established GLB delivery reader/exporter. Supports
the library's uncompressed triangle glTF/GLB, external PNGs, skin and animations.
Unsupported compression, sparse accessors and morph targets fail explicitly.
"""
import copy
import hashlib
import json
import math
import os
import struct
from pathlib import Path
from urllib.parse import unquote, quote

import numpy as np

DTYPES = {5120: 'i1', 5121: 'u1', 5122: '<i2', 5123: '<u2', 5125: '<u4', 5126: '<f4'}
WIDTHS = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}


def digest(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):value.update(chunk)
    return value.hexdigest()


def distance(height, screen_height, vfov=60):
    """Distance to centered vertical extent, not nearest surface; meters."""
    if height <= 0 or not 0 < screen_height <= 1 or not 0 < vfov < 180:
        raise ValueError('Invalid height, screen fraction or field of view')
    return height / (2 * screen_height * math.tan(math.radians(vfov) / 2))


def local(node):
    if 'matrix' in node:
        return np.asarray(node['matrix']).reshape(4, 4).T
    x, y, z, w = node.get('rotation', [0, 0, 0, 1])
    r = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                  [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                  [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
    m = np.eye(4); m[:3, :3] = r @ np.diag(node.get('scale', [1, 1, 1]))
    m[:3, 3] = node.get('translation', [0, 0, 0])
    return m


class Document:
    def __init__(self, path):
        self.path = Path(path).resolve(); raw = self.path.read_bytes()
        binary = b''
        if self.path.suffix == '.glb':
            if struct.unpack_from('<III', raw) != (0x46546c67, 2, len(raw)):
                raise ValueError('Invalid GLB header')
            offset = 12
            while offset < len(raw):
                size, kind = struct.unpack_from('<II', raw, offset)
                payload = raw[offset+8:offset+8+size]; offset += size+8
                if kind == 0x4e4f534a: self.data = json.loads(payload)
                elif kind == 0x004e4942: binary = payload
        elif self.path.suffix == '.gltf': self.data = json.loads(raw)
        else: raise ValueError('LOD source must be delivered glTF or GLB')
        self.buffers = [self.resolve(b['uri']).read_bytes() if 'uri' in b else binary
                        for b in self.data.get('buffers', [])]
        for m in self.data.get('meshes', []):
            for p in m['primitives']:
                if p.get('mode', 4) != 4 or p.get('targets') or p.get('extensions'):
                    raise ValueError('Only uncompressed triangles without morphs supported')
        self.parents = {c: i for i, n in enumerate(self.data['nodes']) for c in n.get('children', [])}
        self.replacements = {}

    def resolve(self, uri):
        if ':' in uri or uri.startswith('/'):
            raise ValueError('Only relative local resources supported')
        return (self.path.parent / unquote(uri)).resolve()

    def dependencies(self):
        paths = [self.path] + [self.resolve(x['uri']) for key in ('buffers', 'images')
                              for x in self.data.get(key, []) if 'uri' in x]
        return {os.path.relpath(p, self.path.parent): digest(p) for p in sorted(set(paths))}

    def view(self, index):
        v = self.data['bufferViews'][index]; a = v.get('byteOffset', 0)
        return self.buffers[v['buffer']][a:a+v['byteLength']]

    def accessor(self, index):
        if index in self.replacements: return self.replacements[index].copy()
        a = self.data['accessors'][index]
        if 'sparse' in a or 'bufferView' not in a:
            raise ValueError('Sparse or zero-initialized accessors unsupported')
        v = self.data['bufferViews'][a['bufferView']]; dt = np.dtype(DTYPES[a['componentType']])
        w = WIDTHS[a['type']]
        values = np.ndarray((a['count'], w), dtype=dt, buffer=self.buffers[v['buffer']],
                            offset=v.get('byteOffset', 0)+a.get('byteOffset', 0),
                            strides=(v.get('byteStride', w*dt.itemsize), dt.itemsize)).copy()
        if a.get('normalized'):
            values = values.astype(np.float32)/np.iinfo(dt).max
            if dt.kind == 'i': values = np.maximum(-1, values)
        return values

    def world(self, i):
        return (self.world(self.parents[i]) if i in self.parents else np.eye(4)) @ local(self.data['nodes'][i])

    def primitives(self):
        for mi, m in enumerate(self.data['meshes']):
            for pi, p in enumerate(m['primitives']): yield mi, pi, p

    def selected_nodes(self, names):
        if not names:return set(range(len(self.data['nodes'])))
        selected={i for i,n in enumerate(self.data['nodes']) if n.get('name') in names}
        if len(selected)!=len(names):raise ValueError('Missing or duplicate selected roots: '+str(names))
        pending=list(selected)
        while pending:
            i=pending.pop()
            for c in self.data['nodes'][i].get('children',[]):
                if c not in selected:selected.add(c);pending.append(c)
        return selected

    def select(self, names):
        """An opt-in module view of one delivery; original resource is untouched.

        Keep every transform-only node so indices, socket frames and ancestry
        stay stable, but drop nonselected geometry and unused material/images.
        Cannot select subsets of skins/animations; use the complete delivery.
        """
        if not names:return
        if self.data.get('skins') or self.data.get('animations'):
            raise ValueError('Module selection requires an unskinned static hierarchy')
        selected=self.selected_nodes(names)
        for i,n in enumerate(self.data['nodes']):
            if i not in selected:n.pop('mesh',None)
        def compact(key,used):
            old=self.data.get(key,[]);mapping={i:j for j,i in enumerate(sorted(used))}
            self.data[key]=[old[i] for i in sorted(used)];return mapping
        mm=compact('meshes',{n['mesh'] for n in self.data['nodes'] if 'mesh' in n})
        for n in self.data['nodes']:
            if 'mesh' in n:n['mesh']=mm[n['mesh']]
        pm=compact('materials',{p['material'] for _,_,p in self.primitives()})
        for _,_,p in self.primitives():p['material']=pm[p['material']]
        infos=[]
        def visit(node):
            if isinstance(node,dict):
                for k,v in node.items():
                    if k.endswith('Texture') and isinstance(v,dict) and 'index' in v:infos.append(v)
                    visit(v)
            elif isinstance(node,list):
                for v in node:visit(v)
        visit(self.data['materials'])
        tm=compact('textures',{i['index'] for i in infos})
        for i in infos:i['index']=tm[i['index']]
        im=compact('images',{t['source'] for t in self.data.get('textures',[])})
        for t in self.data.get('textures',[]):t['source']=im[t['source']]

    def arrays(self, p):
        return {k: self.accessor(i) for k, i in p['attributes'].items()}, self.accessor(p['indices']).reshape(-1, 3)

    def replace(self, p, attributes, indices):
        for name, values in list(attributes.items()) + [('indices', indices.reshape(-1, 1))]:
            source_desc=self.data['accessors'][p['attributes'][name]] if name!='indices' and name in p['attributes'] else {}
            desc = dict(componentType=(5123 if int(indices.max())<=65535 else 5125) if name == 'indices' else source_desc.get('componentType',5123 if name.startswith('JOINTS_') else 5126),
                        count=len(values), type='SCALAR' if name == 'indices' else
                        {2:'VEC2', 3:'VEC3', 4:'VEC4'}[values.shape[1]])
            if source_desc.get('normalized'):desc['normalized']=True
            if name == 'POSITION':
                desc.update(min=values.min(axis=0).tolist(), max=values.max(axis=0).tolist())
            i = len(self.data['accessors']); self.data['accessors'].append(desc)
            self.replacements[i] = np.asarray(values, dtype='<u4' if name == 'indices' else '<f4')
            if name == 'indices': p['indices'] = i
            else: p['attributes'][name] = i

    def image(self, i):
        entry = self.data['images'][i]
        return self.resolve(entry['uri']).read_bytes() if 'uri' in entry else self.view(entry['bufferView'])

    def bounds(self, include=None):
        points = []
        selected=self.selected_nodes(include)
        for i, n in enumerate(self.data['nodes']):
            if 'mesh' not in n or i not in selected: continue
            for p in self.data['meshes'][n['mesh']]['primitives']:
                v = self.accessor(p['attributes']['POSITION']); m = self.world(i)
                points.append(v @ m[:3,:3].T + m[:3,3])
        v = np.concatenate(points)
        return v.min(axis=0), v.max(axis=0)

    def stats(self, include=None):
        triangles = sum(len(self.accessor(p['indices']))//3 for _, _, p in self.primitives())
        selected=self.selected_nodes(include)
        placed = sum(sum(len(self.accessor(p['indices']))//3 for p in self.data['meshes'][n['mesh']]['primitives'])
                     for i,n in enumerate(self.data['nodes']) if 'mesh' in n and i in selected)
        images = []; gpu = 0
        for i, entry in enumerate(self.data.get('images', [])):
            raw = self.image(i)
            if raw[:8] != b'\x89PNG\r\n\x1a\n': raise ValueError('Expected PNG images')
            w, h = struct.unpack_from('>II', raw, 16)
            # 8 bits/texel blocks, exact 4x4 allocation at each mip.
            a, b, mem = w, h, 0
            while True:
                mem += math.ceil(a/4)*math.ceil(b/4)*16
                if a == b == 1: break
                a, b = max(1,a//2), max(1,b//2)
            gpu += mem
            images.append(dict(name=entry.get('name', ''), size=[w,h], bytes=len(raw),
                               sha256=hashlib.sha256(raw).hexdigest(), compressed_mip_bytes=mem))
        deps = self.dependencies()
        package = sum((self.path.parent/p).stat().st_size for p in deps)
        embedded=sum(len(self.image(i)) for i,im in enumerate(self.data.get('images',[])) if 'bufferView' in im)
        geometry_bytes=self.path.stat().st_size-embedded+sum(self.resolve(b['uri']).stat().st_size for b in self.data.get('buffers',[]) if 'uri' in b)
        used={v for _,_,p in self.primitives() for v in [p['indices'],*p['attributes'].values()]}
        mesh_gpu=sum(self.data['accessors'][i]['count']*WIDTHS[self.data['accessors'][i]['type']]*np.dtype(DTYPES[self.data['accessors'][i]['componentType']]).itemsize for i in used)
        return dict(triangles=triangles, placed_triangles=placed, materials=len({p.get('material',0) for _,_,p in self.primitives()}),
                    draw_calls=sum(len(self.data['meshes'][n['mesh']]['primitives']) for i,n in enumerate(self.data['nodes']) if 'mesh' in n and i in selected),
                    file_bytes=self.path.stat().st_size, geometry_bytes=geometry_bytes,package_bytes=package, images=images,
                    texture_gpu_bytes=gpu,mesh_gpu_bytes=mesh_gpu)

    def save(self, path, image_paths=None):
        """Compact referenced accessors/views; keep node/material/skin JSON exact."""
        path = Path(path).resolve()
        protected={self.path} | {self.resolve(x['uri']) for key in ('buffers','images')
                               for x in self.data.get(key,[]) if 'uri' in x}
        targets={path,path.with_suffix('.bin')} if path.suffix=='.gltf' else {path}
        if targets & protected:raise ValueError('Refusing to overwrite a LOD0 resource')
        d = copy.deepcopy(self.data); accessors = []; views = []; binary = bytearray(); mapping = {}; vm = {}
        def add_view(raw, template=None):
            binary.extend(b'\0' * (-len(binary)%4)); offset = len(binary); binary.extend(raw)
            row = dict(template or {}); row.update(buffer=0, byteOffset=offset, byteLength=len(raw))
            row.pop('byteStride', None); views.append(row); return len(views)-1
        def acc(i):
            if i in mapping: return mapping[i]
            src = self.data['accessors'][i]; values = self.accessor(i)
            dt = np.dtype(DTYPES[src['componentType']])
            if src.get('normalized'): values = np.rint(values*np.iinfo(dt).max)
            raw = np.ascontiguousarray(values, dtype=dt).tobytes()
            row = copy.deepcopy(src); row.pop('byteOffset', None)
            row['bufferView'] = add_view(raw); accessors.append(row)
            mapping[i] = len(accessors)-1; return mapping[i]
        for mesh in d['meshes']:
            for p in mesh['primitives']:
                p['indices'] = acc(p['indices'])
                p['attributes'] = {k:acc(v) for k,v in p['attributes'].items()}
        for skin in d.get('skins', []):
            if 'inverseBindMatrices' in skin: skin['inverseBindMatrices'] = acc(skin['inverseBindMatrices'])
        for animation in d.get('animations', []):
            for s in animation['samplers']:
                s['input'], s['output'] = acc(s['input']), acc(s['output'])
        for image_index, entry in enumerate(d.get('images', [])):
            if image_paths and image_index in image_paths:
                entry.pop('bufferView', None); entry.pop('mimeType', None)
                entry['uri'] = quote(os.path.relpath(image_paths[image_index], path.parent), safe='/')
            elif 'uri' in entry:
                entry['uri'] = quote(os.path.relpath(self.resolve(entry['uri']), path.parent), safe='/')
            else:
                vi = entry['bufferView']
                if vi not in vm: vm[vi] = add_view(self.view(vi))
                entry['bufferView'] = vm[vi]
        d['accessors'], d['bufferViews'] = accessors, views
        d['buffers'] = [dict(byteLength=len(binary))]
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == '.gltf':
            bp = path.with_suffix('.bin'); d['buffers'][0]['uri'] = bp.name
            bp.write_bytes(binary); path.write_text(json.dumps(d, separators=(',',':'))+'\n')
        elif path.suffix == '.glb':
            js = json.dumps(d, separators=(',',':')).encode(); js += b' '*(-len(js)%4)
            binary.extend(b'\0'*(-len(binary)%4))
            path.write_bytes(struct.pack('<III',0x46546c67,2,28+len(js)+len(binary)) +
                             struct.pack('<II',len(js),0x4e4f534a)+js+
                             struct.pack('<II',len(binary),0x004e4942)+binary)
        else: raise ValueError('Expected .glb or .gltf')
