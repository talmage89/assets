"""Manufactured upper-loft derivatives, paired laminate roles, retained fields.

The C2 die is independent of a triangulated nearest-point query. A cut corner
must not select the neighboring steel phase or reverse side of a thin sheet.
"""
from mathutils import Vector
from sedan_upper_surface import field,ease


def normal(p,parent):
    from sedan_body import shoulder_height
    x,y,z=p
    w=ease(-1.22,-1.08,y)*(1-ease(2.08,2.20,y))*ease(.025,.085,z-shoulder_height(y))
    front=ease(-2.42,-2.28,y)*(1-ease(-1.22,-1.08,y))*ease(.68,.76,z)
    if front>w:
        from sedan_body import section_field
        sample=section_field;w=front
    else:sample=field
    if w==0:return parent
    h=.000025
    n=Vector(tuple((sample((x+(h if k==0 else 0),y+(h if k==1 else 0),z+(h if k==2 else 0)))-sample((x-(h if k==0 else 0),y-(h if k==1 else 0),z-(h if k==2 else 0))))/(2*h) for k in range(3))).normalized()
    return parent.lerp(n,w).normalized()


def coalesce(ob):
    """One manufactured normal at coincident outer sheet coordinates.

    Submicron duplicate cut vertices can choose opposite nearest-facet phases.
    Match the delivered FLOAT-position precision; keep reverse/rim fans separate.
    This repairs shared-point provenance, not broad reflection curvature.
    """
    import json
    me=ob.data;roles=me.attributes.get('sheet_role')
    if roles is None:return
    from mathutils.kdtree import KDTree
    groups={};custom=[n.vector.copy() for n in me.corner_normals]
    outside=sorted({me.loops[li].vertex_index for f in me.polygons if roles.data[f.index].value==0 for li in f.loop_indices})
    positions=[ob.matrix_world@me.vertices[i].co for i in outside];tree=KDTree(len(outside))
    for i,p in enumerate(positions):tree.insert(p,i)
    tree.balance();parents=list(range(len(outside)))
    def root(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    for i,p in enumerate(positions):
        for _,j,_ in tree.find_range(p,2e-7):
            a,b=root(i),root(j)
            if a!=b:parents[max(a,b)]=min(a,b)
    owners={vi:root(i) for i,vi in enumerate(outside)}
    for f in me.polygons:
        if roles.data[f.index].value!=0:continue
        for li in f.loop_indices:
            groups.setdefault(owners[me.loops[li].vertex_index],[]).append(li)
    maximum=0.;changed=0
    for loops in groups.values():
        n=sum((custom[i] for i in loops),Vector()).normalized()
        for i in loops:
            difference=(custom[i]-n).length;maximum=max(maximum,difference)
            if difference>1e-6:changed+=1
            custom[i]=n
    me.normals_split_custom_set(custom)
    ob['coincident_outer_normal_field']=json.dumps(dict(position_radius_m=2e-7,changed_corners=changed,maximum_vector_correction=maximum))
