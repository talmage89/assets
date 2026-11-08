"""Surface receipts for native presentation cars; garage geometry stays exact.

All points come from our accepted scripted exports, never reference models.
Samples cover every named mesh, including small trim, plus its six extrema.
"""
import hashlib,json,random
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from kit.gltf import GLB


class Document(GLB):
    def __init__(self,path):
        path=Path(path)
        if path.suffix=='.glb':super().__init__(path)
        else:
            self.json=json.loads(path.read_text());self.binary=(path.parent/self.json['buffers'][0]['uri']).read_bytes()
            self.parents={child:i for i,node in enumerate(self.json['nodes']) for child in node.get('children',[])}


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def surface(doc,index):
    node=doc.json['nodes'][index];mesh=doc.json['meshes'][node['mesh']];vertices=[];faces=[];materials=[]
    xf=doc.world(index)
    for primitive in mesh['primitives']:
        offset=len(vertices);v=doc.accessor(primitive['attributes']['POSITION'])
        vertices.extend((np.c_[v,np.ones(len(v))]@xf.T)[:,:3].tolist())
        faces.extend((doc.accessor(primitive['indices']).reshape(-1,3)+offset).tolist())
        materials.append(doc.json['materials'][primitive['material']]['name'])
    return vertices,faces,materials


def points(vertices,faces,name):
    v=np.asarray(vertices);f=np.asarray(faces);tri=v[f]
    area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)
    rng=random.Random(name);samples=[]
    # Sample face interiors at the six extent stations. Native return/gauge
    # meshes can retain loose or degenerate edge vertices; those aren't surface.
    centers=tri.mean(axis=1);valid=np.flatnonzero(area>1e-10)
    for axis in range(3):
        for extreme in (np.argmin,np.argmax):samples.append(centers[valid[extreme(centers[valid,axis])]])
    for i in rng.choices(range(len(f)),weights=area,k=24):
        a,b=rng.random(),rng.random()
        if a+b>1:a,b=1-a,1-b
        samples.append(tri[i,0]*(1-a-b)+tri[i,1]*a+tri[i,2]*b)
    return [[round(float(x),8) for x in p] for p in samples]


def capture(path):
    doc=Document(path);rows={};triangles=0
    for i,node in enumerate(doc.json['nodes']):
        row=dict(mesh='mesh' in node)
        if row['mesh']:
            v,f,m=surface(doc,i);triangles+=len(f)
            row.update(materials=m,triangles=len(f),samples=points(v,f,node['name']))
        rows[node['name']]=row
    assert len(rows)==len(doc.json['nodes']),'Duplicate object names'
    definitions=sorted(doc.json.get('materials',[]),key=lambda m:m['name'])
    return dict(sha256=digest(path),triangles=triangles,objects=rows,
                material_definitions_sha256=hashlib.sha256(json.dumps(definitions,sort_keys=True).encode()).hexdigest(),
                materials=sorted(m['name'] for m in doc.json.get('materials',[])))


def compare(reference,path):
    doc=Document(path);names={n['name']:i for i,n in enumerate(doc.json['nodes'])}
    assert set(names)==set(reference['objects']),('Car object names differ',path)
    assert sorted(m['name'] for m in doc.json['materials'])==reference['materials'],('Car materials differ',path)
    definitions=sorted(doc.json['materials'],key=lambda m:m['name'])
    assert hashlib.sha256(json.dumps(definitions,sort_keys=True).encode()).hexdigest()==reference['material_definitions_sha256'],('Car material definitions differ',path)
    triangles=0;maximum=0;count=0
    for name,row in reference['objects'].items():
        index=names[name];node=doc.json['nodes'][index]
        assert ('mesh' in node)==row['mesh'],(path,name,'Object type')
        if not row['mesh']:continue
        v,f,m=surface(doc,index);triangles+=len(f)
        assert m==row['materials'],(path,name,'Material assignment')
        tree=BVHTree.FromPolygons(v,f,all_triangles=True)
        for point in row['samples']:
            hit=tree.find_nearest(Vector(point));assert hit[0] is not None
            maximum=max(maximum,float(hit[3]));count+=1
    relative=abs(triangles-reference['triangles'])/reference['triangles']
    assert relative<=.001,(path,'Triangle delta',relative)
    assert maximum<=.001,(path,'Sampled surface distance',maximum)
    return dict(passed=True,reference_sha256=reference['sha256'],actual_sha256=digest(path),
                reference_triangles=reference['triangles'],actual_triangles=triangles,
                relative_triangle_delta=relative,surface_samples=count,max_surface_distance_m=maximum)
