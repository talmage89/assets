"""Read-only native campus and exported fleet presentation placement."""
from mathutils import Matrix,Vector
import math
import bpy

def place(school,bus_source,imported,digest,root):
    campus=imported(school);temp=list(campus)
    socket=next(o for o in campus if 'Bus_loading_0' in o.name)
    bpy.context.view_layer.update()
    # Place the lead toward the beginning of the straight curb. Campus 102's
    # long entrance canopy extends ahead of the nose, visible at eye height.
    school_seed=int(school.stem.split('-')[-1])
    advance=3.5 if school_seed==102 else 5
    transform=Matrix.Translation((0,advance,0))@socket.matrix_world.inverted()
    for ob in campus:
        if ob.parent is None:ob.matrix_world=transform@ob.matrix_world
    # Continue the school's grounds beyond its finite parcel so low cameras
    # cannot see a world void through the native site's outside edge.
    from kit import model as G
    ground=bpy.data.materials.new('Distant school grounds');ground.use_nodes=True
    nt=ground.node_tree;bs=nt.nodes.get('Principled BSDF')
    noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.09
    ramp=nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color=(.034,.048,.013,1)
    ramp.color_ramp.elements[1].color=(.085,.103,.030,1)
    nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value=.94
    temp.append(G.box('Distant school grounds',(0,0,-.075),(2000,2000,.06),ground,0))
    from school_context import landscaping
    plants,plant_receipt=landscaping(campus);temp+=plants
    queued={}
    rear=(103,3.1,25.2,-30) if school_seed==102 else (103,.25,25.2,-3.5)
    for seed,dx,dy,yaw in [(102,0,12.6,0),rear]:
        path=bus_source.parent/f'C75-{seed}.gltf';obs=imported(path);temp+=obs
        placement=Matrix.Translation((dx,dy,0))@Matrix.Rotation(math.radians(yaw),4,'Z')
        for ob in obs:
            if ob.parent is None:ob.matrix_world=placement@ob.matrix_world
        queued[str(seed)]=dict(source=str(path.relative_to(root)),sha256=digest(path),translation_m=[dx,dy,0],yaw_degrees=yaw)
    receipt=dict(source=str(school.relative_to(root)),sha256=digest(school),socket=socket.name,
                 campus_translation_in_bus_frame_m=[0,advance,0],queue=queued,
                 center_spacing_m=12.6,placement='Native loading lane; third bus reaches its east transition')
    receipt['tree_context']=plant_receipt
    return temp,receipt

def audit(campus,buses,plan,body_bounds):
    """Actual imported lane triangles and fleet contact points in this stage."""
    from mathutils.bvhtree import BVHTree
    verts=[];faces=[]
    for ob in campus:
        if ob.type!='MESH':continue
        slots={i for i,m in enumerate(ob.data.materials) if m and m.name.startswith('SchoolGround_Asphalt')}
        ob.data.calc_loop_triangles();offset=len(verts)
        verts.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        faces.extend(tuple(offset+i for i in t.vertices) for t in ob.data.loop_triangles if t.material_index in slots)
    tree=BVHTree.FromPolygons(verts,faces,all_triangles=True)
    site=next(o for o in campus if o.parent is None and o.name.startswith('Campus_'))
    route=[site.matrix_world@Vector((*p,0)) for p in plan['bus_route']]
    def distance(p):
        values=[]
        for a,b in zip(route,route[1:]):
            d=b-a;t=max(0,min(1,(p-a).dot(d)/d.length_squared))
            q=a+t*d;values.append(((p.x-q.x)**2+(p.y-q.y)**2)**.5)
        return min(values)
    rows={};footprints={};errors=[]
    for seed,obs in buses.items():
        wheels={}
        for pivot in [o for o in obs if o.name.startswith('Wheel_')]:
            points=[o.matrix_world@v.co for o in pivot.children_recursive if o.type=='MESH' for v in o.data.vertices]
            if not points:continue
            low=min(p.z for p in points);contacts=[p for p in points if p.z<low+.00002]
            gaps=[];routes=[]
            for p in contacts:
                hit=tree.ray_cast(p+Vector((0,0,1)),Vector((0,0,-1)),2)[0]
                if hit is not None:gaps.append(p.z-hit.z)
                routes.append(distance(Vector((p.x,p.y,0))))
            wheels[pivot.name]=dict(samples=len(contacts),asphalt_hits=len(gaps),gaps_m=gaps,route_distances_m=routes)
            if len(gaps)!=len(contacts) or any(abs(v)>.005 for v in gaps) or max(routes)>7.3152/2:
                errors.append(str(seed)+'/'+pivot.name+' lane contact')
        if len(wheels)!=6:errors.append(str(seed)+' missing six wheel proofs')
        rows[str(seed)]=wheels
        root=next(o for o in obs if o.parent is None);samples=[]
        for x in [body_bounds['min'][0],0,body_bounds['max'][0]]:
            for y in [body_bounds['min'][1],0,body_bounds['max'][1]]:
                p=root.matrix_world@Vector((x,y,0));offset=distance(p)
                hit=tree.ray_cast(p+Vector((0,0,1)),Vector((0,0,-1)),2)[0]
                samples.append(dict(world_xy_m=list(p[:2]),route_distance_m=offset,
                                    asphalt_z_m=hit.z if hit is not None else None))
                if offset>7.3152/2 or hit is None:errors.append(str(seed)+' body footprint outside loading corridor')
        footprints[str(seed)]=samples
    return dict(passed=not errors,errors=errors,fleet=rows,body_footprints=footprints,
                scope='Actual imported tire-bottom vertices against native asphalt; source-measured body/bumper envelope transformed by actual imported roots against the bus-route corridor')
