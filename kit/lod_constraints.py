"""Measured LOD source constraints; coincident corner counts are not locks.

UV/normal/material sides are constraints that can slide together. Boundary or
interaction membership does not, by itself, justify freezing a complete part.
Counts overlap and are reported separately from the initial collapse eligibility.
"""
import numpy as np


def contact_points(primitives):
    """Source junctions across attribute groups, and existing >2-face edges.

    Pin only their endpoints before pruning. The same one-micrometer coordinate
    convention is used by the independent assembly topology check.
    """
    edges={}
    for attrs,faces in primitives:
        group=tuple(sorted(attrs));keys=[tuple(p) for p in np.round(attrs['POSITION'],6)]
        for face in faces:
            for a,b in zip(face,np.roll(face,-1)):
                edge=tuple(sorted((keys[a],keys[b])))
                if edge[0]==edge[1]:continue
                row=edges.setdefault(edge,[0,set()]);row[0]+=1;row[1].add(group)
    junctions={edge for edge,(count,groups) in edges.items() if count>2 or len(groups)>1}
    return {point for edge in junctions for point in edge},len(junctions)


def inventory(attrs,faces,*,fixed=(),eligible=None,moving=False):
    """Inventory geometric vertices and their overlapping constraint causes.

    `initial_unoffered` means no initial mapping/weighted-error offer could
    remove that vertex. It does not claim every offered collapse will pass the
    later sampled field/geometry tests, or that every unoffered vertex stays
    locked after its neighbors change. `fixed` are actual persistent pins.
    """
    _,geo=np.unique(np.round(attrs['POSITION'],8),axis=0,return_inverse=True)
    total=int(geo.max(initial=-1)+1);records=[[] for _ in range(total)]
    for i,g in enumerate(geo):records[int(g)].append(i)
    edges={}
    for face in geo[faces]:
        for a,b in zip(face,np.roll(face,-1)):
            edge=tuple(sorted((int(a),int(b))));edges[edge]=edges.get(edge,0)+1
    causes={name:set() for name in ('uv_seams','hard_normals','material_borders','part_borders','moving_parts','protected_surface')}
    causes['part_borders']={v for e,count in edges.items() if count==1 for v in e}
    if moving:causes['moving_parts']=set(range(total))
    uvkeys=[k for k in attrs if k.startswith('TEXCOORD_')]
    for g,ids in enumerate(records):
        if any(np.ptp(attrs[k][ids],axis=0).max(initial=0)>1e-6 for k in uvkeys):causes['uv_seams'].add(g)
        if 'NORMAL' in attrs:
            normals=attrs['NORMAL'][ids].astype(float);normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-20)
            if (normals@normals.T).min(initial=1)<np.cos(np.radians(1)):causes['hard_normals'].add(g)
        if '_LOD_MATERIAL' in attrs and np.ptp(attrs['_LOD_MATERIAL'][ids])>0:causes['material_borders'].add(g)
        if '_LOD_KEEP' in attrs and attrs['_LOD_KEEP'][ids].any():causes['protected_surface'].add(g)
    fixed=set(map(int,fixed));unoffered=set(range(total))-set(eligible) if eligible is not None else set()
    return dict(geometric_vertices=total,corner_records=len(geo),fixed_vertices=len(fixed),
                initial_unoffered_vertices=len(unoffered) if eligible is not None else None,
                by_cause={k:dict(constrained=len(v),fixed=len(v&fixed),initial_unoffered=len(v&unoffered) if eligible is not None else None) for k,v in causes.items()})
