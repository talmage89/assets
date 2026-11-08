"""Exact garage/town payloads, tolerant native-car surfaces in mixed sites."""
import copy,hashlib,json
import numpy as np
from pathlib import Path
from context_geometry import Document,capture,compare,digest

CAR_PREFIXES=('Parked ','Street parked ','Entry queue vehicle','Meter parked ',
              'Cross street parked ','Street traffic ','Surface court ')


def car_nodes(doc):
    result=set()
    def add(i):
        result.add(i)
        for child in doc.json['nodes'][i].get('children',[]):add(child)
    for i,n in enumerate(doc.json['nodes']):
        if n.get('name','').startswith(CAR_PREFIXES):add(i)
    return result


def signature(doc,index):
    node=copy.deepcopy(doc.json['nodes'][index]);mesh=node.pop('mesh',None)
    node['children']=[doc.json['nodes'][i]['name'] for i in node.get('children',[])]
    if mesh is not None:
        primitives=[]
        for p in doc.json['meshes'][mesh]['primitives']:
            values={k:hashlib.sha256(doc.accessor(a).tobytes()).hexdigest() for k,a in p['attributes'].items()}
            values.update(indices=hashlib.sha256(doc.accessor(p['indices']).tobytes()).hexdigest(),
                          material=doc.json['materials'][p['material']]['name'],mode=p.get('mode',4))
            primitives.append(values)
        node['primitives']=primitives
    return node


def check(before,after):
    left,right=Document(before),Document(after);lc,rc=car_nodes(left),car_nodes(right)
    ln={n['name']:i for i,n in enumerate(left.json['nodes'])};rn={n['name']:i for i,n in enumerate(right.json['nodes'])}
    assert set(ln)==set(rn),('Embedded object names differ',before,after)
    assert {left.json['nodes'][i]['name'] for i in lc}=={right.json['nodes'][i]['name'] for i in rc}
    # Material and image definitions stay exact, regardless of mesh counts.
    for key in ('materials','textures','images','samplers'):
        assert left.json.get(key)==right.json.get(key),(before,key)
    exact=0
    for name,i in ln.items():
        if i in lc:continue
        assert signature(left,i)==signature(right,rn[name]),(before,name,'Non-car payload changed')
        exact+=1
    # Repeated placements share geometry; sample each distinct placed mesh
    # once, using its real world transform. Names/materials above cover all.
    from context_geometry import surface,points
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    maximum=0;total=0;original=0;samples=0;seen=set()
    for i in sorted(lc):
        node=left.json['nodes'][i];name=node['name'];other=right.json['nodes'][rn[name]]
        assert ('mesh' in node)==('mesh' in other),(name,'Car object type')
        if 'mesh' not in node:continue
        old_count=sum(left.json['accessors'][p['indices']]['count']//3 for p in left.json['meshes'][node['mesh']]['primitives'])
        new_count=sum(right.json['accessors'][p['indices']]['count']//3 for p in right.json['meshes'][other['mesh']]['primitives'])
        assert abs(old_count-new_count)<=max(old_count,1)*.001,(name,'Car triangle delta')
        original+=old_count;total+=new_count
        pair=(node['mesh'],other['mesh'])
        # Shared geometry can skip a repeated placement only if its pose also
        # agrees exactly. A changed placement must pass its own surface test.
        if pair in seen and np.array_equal(left.world(i),right.world(rn[name])):continue
        seen.add(pair);lv,lf,lm=surface(left,i);v,f,m=surface(right,rn[name])
        assert m==lm,(name,'Car material assignment')
        # Bidirectional, deterministic surface points include six extrema.
        for av,af,bv,bf in ((lv,lf,v,f),(v,f,lv,lf)):
            tree=BVHTree.FromPolygons(bv,bf,all_triangles=True)
            for point in points(av,af,name):
                hit=tree.find_nearest(Vector(point));assert hit[0] is not None
                maximum=max(maximum,float(hit[3]));samples+=1
    delta=abs(total-original)/max(original,1)
    assert delta<=.001,(before,'Car triangle delta',delta)
    assert maximum<=.001,(before,'Car surface delta',maximum)
    return dict(passed=True,reference_sha256=digest(before),actual_sha256=digest(after),
                exact_noncar_nodes=exact,car_triangles=total,relative_triangle_delta=delta,
                sampled_car_meshes=len(seen),surface_samples=samples,max_surface_distance_m=maximum)
