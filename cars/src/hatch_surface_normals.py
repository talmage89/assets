"""Resolve reflected-normal interpolation on the accepted evaluated parent.

Positions and cut outlines remain held; new local samples land on that same
parent. Its disposable dense field also supplies continuous corner normals.
"""
import bpy,math
from mathutils import Vector
from hatch_optical_surfaces import normal


def apply():
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.name!='Hood outer' and not ob.name.startswith(('Front fender','Rear quarter','Front molded fascia','Rear molded fascia','Liftgate outer')):continue
        me=ob.data;count=ob.get('outer_skin_faces',0);roles=me.attributes.get('hatch_outer_skin');matrix=ob.matrix_world;nm=matrix.to_3x3().transposed()
        custom=[n.vector.copy() for n in me.corner_normals];changed=0
        for face in me.polygons:
            if not (roles.data[face.index].value if roles else face.index<count):continue
            for li in face.loop_indices:
                p=matrix@me.vertices[me.loops[li].vertex_index].co
                # Keep the accepted cowl/canopy handoff; concentrate this
                # correction on the explicitly diagnosed reflected panels.
                blend=(1 if p.y<-1.24 or p.y>1.70 else 0)
                if ob.name.startswith(('Front fender','Rear quarter')) and abs(p.x)>.83 and p.z<1.00:blend=1
                if not blend:continue
                n=nm@normal(p)
                if n.dot(custom[li])<.85:continue
                custom[li]=n;changed+=1
        me.normals_split_custom_set(custom);ob['parent_normal_corners']=changed


def sample_reflections(b):
    """Resolve reflected normal direction, rather than position error alone."""
    import bmesh
    from hatch_reference_surface import field
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.name not in ['Hood outer','Front molded fascia','Rear quarter_L','Rear quarter_R']:continue
        me=ob.data;count=ob.get('outer_skin_faces',0);role=me.attributes.get('hatch_outer_skin')
        if role is None:
            role=me.attributes.new('hatch_outer_skin','INT','FACE')
            for f in me.polygons:role.data[f.index].value=int(f.index<count)
        saved=me.attributes.new('H120 sample held normals','FLOAT_VECTOR','CORNER')
        for row,n in zip(saved.data,me.corner_normals):row.vector=n.vector
        bm=bmesh.new();bm.from_mesh(me);outer=bm.faces.layers.int['hatch_outer_skin'];matrix=ob.matrix_world;inverse=matrix.inverted();candidates=[]
        for e in bm.edges:
            if len(e.link_faces)!=2 or not all(f[outer] for f in e.link_faces):continue
            a,c=[matrix@v.co for v in e.verts];p=(a+c)/2
            if ob.name=='Hood outer':valid=p.y<-1.24
            elif ob.name=='Front molded fascia':valid=abs(p.x)>.62 and p.y<-1.40 and p.z<.62
            else:valid=abs(p.x)>.78 and 1.29<p.y<2.08 and p.z<1.02
            if not valid or (a-c).length<.015:continue
            score=normal(p).angle((normal(a)+normal(c)).normalized())
            if ob.name=='Front molded fascia' and .65<abs(p.x)<.85 and -1.80<p.y<-1.55 and .20<p.z<.50 and (a-c).length>.022:score+=1
            if score>math.radians(.10):candidates.append((score,e))
        bm.edges.index_update();added=0;projection=0
        limit=(140 if b.high else 70) if ob.name!='Front molded fascia' else (400 if b.high else 220)
        for score,e in sorted(candidates,key=lambda q:(-q[0],q[1].index))[:limit]:
            a,c=e.verts;p=matrix@((a.co+c.co)/2);q=p.copy()
            hit=field()(p+normal(p)*.02,-normal(p))
            if hit is not None:q=hit[0]
            if (q-p).length>.003:q=p
            _,v=bmesh.utils.edge_split(e,a,.5);v.co=inverse@q;added+=1;projection=max(projection,(q-p).length)
        bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if len(f.verts)>3]);bm.to_mesh(me);bm.free()
        saved=me.attributes['H120 sample held normals'];me.normals_split_custom_set([r.vector for r in saved.data]);me.attributes.remove(saved)
        ob['reflection_samples_added']=added;ob['reflection_projection_max_m']=projection
