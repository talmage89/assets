"""Manufactured upper-loft derivatives, paired laminate roles, retained fields.

The C2 die is independent of a triangulated nearest-point query. A cut corner
must not select the neighboring steel phase or reverse side of a thin sheet.
"""
from mathutils import Vector
from sedan_upper_surface import field,ease


def normal(p,parent):
    x,y,z=p
    # Every upper control vertex is fitted to this same C2 die. Its own
    # derivatives continue through the deck roll and cut corners; nearest
    # triangulated-parent phases must not re-enter at a rear Y cutoff.
    w=ease(.68,.76,z);sample=field
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
    # Blender encodes custom normals in each smoothing fan's local space.
    # Coincident cut fans can have different angular precision. An encoded
    # representative is stable in its own fan; synchronize the finer fans to
    # that representable direction instead of repeatedly averaging two bins.
    encoded_spread=0.;passes=0
    for iteration in range(4):
        decoded=[n.vector.copy() for n in me.corner_normals];repairs={};encoded_spread=0.
        for loops in groups.values():
            center=sum((decoded[i] for i in loops),Vector()).normalized()
            spread=max(((decoded[i]-decoded[loops[0]]).length for i in loops),default=0.)
            encoded_spread=max(encoded_spread,spread)
            if spread>=.0008:
                representative=max((decoded[i] for i in loops),key=lambda n:(n-center).length_squared)
                for i in loops:repairs[i]=representative
        if not repairs:break
        if iteration==3:raise ValueError(('Coincident normal encoding does not converge',ob.name,encoded_spread))
        for i,n in repairs.items():decoded[i]=n
        me.normals_split_custom_set(decoded);passes+=1
    ob['coincident_outer_normal_field']=json.dumps(dict(position_radius_m=2e-7,changed_corners=changed,maximum_vector_correction=maximum,encoding_passes=passes,maximum_decoded_shared_difference=encoded_spread))
