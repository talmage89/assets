"""Seeded town blocks and afternoon actors, in separate exported packages.

Read-only native library deliveries supply all buildings, foliage and bodies.
House envelopes use the existing explicit distance adapter. No civil alignment
is changed by these placements. Colors decode the native original paint data.
"""
import math,random,json
from pathlib import Path
import bpy
from mathutils import Vector
import geom as Q
from plan import ramp_points


def town(p):
    from town_context import town as build_town
    return build_town(p)


def factory_variants(template):
    """Decode the car family's baked coverage into ordinary PBR color images.

    This local derivative changes factory paint only; the native body, bake and
    deliveries stay immutable. Distant variants are 1024; original blue is shared.
    """
    from context_colors import ensure
    paints=sorted({m for ob in template.children_recursive if ob.type=='MESH' for m in ob.data.materials if m and m.get('paint_decode')},key=lambda m:m.name)
    result={};folder=Path('textures/context');folder.mkdir(parents=True,exist_ok=True)
    from context_colors import FLEET
    for name in FLEET:
        replacements={}
        for mat in paints:
            m=mat.copy()
            texture=next(n for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
            if name!='Atlantic':
                path=ensure(mat.name,name)
                texture.image=bpy.data.images.load(str(path.resolve()),check_existing=True)
            # Preserve the ORM/coat maps and apply the factory metallic factor,
            # as the car family's delivery decoder does for silver and gray.
            metals=json.loads(mat['paint_metallic'])
            target=metals.get(name,{'Garnet':0.,'Spruce':.12,'Sand':.42}.get(name,.12))
            bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');socket=bs.inputs['Metallic']
            # Import stores the old factor upstream in a color mix. Nesting
            # another ratio after it renders correctly in the source, but the
            # glTF exporter recognizes only the outer factor. Use its supported
            # direct ORM B * absolute factory factor graph for serialization.
            orm=next(n for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and 'ORM' in n.image.name)
            split=m.node_tree.nodes.new('ShaderNodeSeparateColor')
            m.node_tree.links.new(orm.outputs['Color'],split.inputs['Color'])
            factor=m.node_tree.nodes.new('ShaderNodeMath');factor.operation='MULTIPLY';factor.inputs[1].default_value=target
            m.node_tree.links.new(split.outputs['Blue'],factor.inputs[0]);m.node_tree.links.new(factor.outputs[0],socket)
            m['factory_color']=name;m['native_paint_source']=mat.name
            m['factory_metallic']=target
            for prop in ('paint_decode','paint_reference_color','paint_colors','paint_metallic'):
                if prop in m:del m[prop]
            replacements[mat]=m
        result[name]=replacements
    return result


def traffic(p):
    from freeway_site import load,clone,delete,along
    rt=Q.root('Traffic',module_kind='traffic');rng=random.Random(p.seed*37);placements=[]
    bodies=[load('build/context/'+n+'.glb') for n in ('Hatch','SUV','Crossover')];full=[load('build/context/'+n+'.glb') for n in ('HeroHatch','HeroSUV','HeroCrossover')];hero=full[0]
    variants=[factory_variants(t) for t in [*bodies,*full]];mesh_variants={};lamp_off={}
    # Flat parking/neighborhood surfaces are measured, not assigned a nominal
    # clearance above grade. Preserve all native inputs and adjust actor roots.
    from mathutils.bvhtree import BVHTree
    bpy.context.view_layer.update();floors=[]
    for template in [*bodies,*full]:
        parts=[o for o in template.children_recursive if o.type=='MESH']
        tires=[o for o in parts if 'Tire_' in o.name] or [o for o in parts if '__Wheel_' in o.name]
        inverse=template.matrix_world.inverted()
        floors.append(min((inverse@o.matrix_world@v.co).z for o in tires for v in o.data.vertices))
    vs=[];fs=[]
    for ob in bpy.data.objects['TownContext'].children_recursive:
        if ob.type!='MESH':continue
        if not any(m and m.name.split('.')[0] in ('Asphalt','Concrete') for m in ob.data.materials):continue
        offset=len(vs);vs.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        ob.data.calc_loop_triangles()
        for face in ob.data.loop_triangles:
            if ob.data.materials[face.material_index].name.split('.')[0] in ('Asphalt','Concrete'):
                fs.append(tuple(offset+i for i in face.vertices))
    town_paving=BVHTree.FromPolygons(vs,fs,all_triangles=True)
    # Stock close-up cameras also need native bodies nearby. The town origin
    # alone is not a distance test for a 1.6km excerpt. This changes actor LOD,
    # never the civil plan, actor positions, speeds, spacing or seeded colors.
    inspection_zones=([(6,-405),(-6,405),(10,-291),(22,-251),
                       (29,-249),(55,-34),(112,-58)] if p.kind=='diamond'
                      else [(15,-75),(24,-5),(3,-26)])
    def colorize(ob,kind,color,lights=False):
        replacements=dict(variants[kind][color])
        if not lights:
            for mesh in ob.children_recursive:
                if mesh.type!='MESH':continue
                for mat in mesh.data.materials:
                    if not mat or 'Lamps' not in mat.name:continue
                    if mat not in lamp_off:
                        m=mat.copy();m.name=mat.name+' / daylight off';bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
                        for link in list(bs.inputs['Emission Strength'].links):m.node_tree.links.remove(link)
                        bs.inputs['Emission Strength'].default_value=0;lamp_off[mat]=m
                    replacements[mat]=lamp_off[mat]
        for mesh in ob.children_recursive:
            if mesh.type!='MESH' or not any(m in replacements for m in mesh.data.materials):continue
            key=(mesh.data.as_pointer(),color,kind,lights)
            if key not in mesh_variants:
                data=mesh.data.copy()
                for i,m in enumerate(data.materials):
                    if m in replacements:data.materials[i]=replacements[m]
                mesh_variants[key]=data
            mesh.data=mesh_variants[key]
    def actor(pos,yaw,where,speed=0,roll=0,nearest=False,pitch=0):
        heading=math.radians(yaw);forward=(math.sin(heading),-math.cos(heading));lateral=(math.cos(heading),math.sin(heading))
        for old in placements[:]:
            dx=pos[0]-old['location'][0];dy=pos[1]-old['location'][1]
            same_lane=abs(dx*lateral[0]+dy*lateral[1])<2.3 and abs(dx*forward[0]+dy*forward[1])<6.6 and abs(pos[2]-old['location'][2])<.7
            if not same_lane:continue
            if where in ('terminal_queue','arterial_queue') and 'queue' not in old['role']:
                delete(bpy.data.objects[old['name']]);placements.remove(old)
            else:return None
        i=len(placements);kind=3 if nearest else rng.randrange(3)
        near_origin=where in ('mainline','bridge','arterial_queue') and abs(pos[1])<120 and abs(pos[0])<110
        near_inspection=any(math.hypot(pos[0]-x,pos[1]-y)<36 for x,y in inspection_zones)
        if not nearest and (near_origin or near_inspection):kind+=3
        from context_colors import FLEET,WEIGHTS
        color=rng.choices(FLEET,WEIGHTS)[0]
        if nearest:color=FLEET[(p.seed//101+4)%len(FLEET)]
        if where in ('commercial_parked','neighborhood'):
            hit=town_paving.ray_cast(Vector((pos[0],pos[1],pos[2]+.35)),Vector((0,0,-1)),1.5)[0]
            assert hit is not None,('Missing flat traffic paving',where,pos)
            pos=list(pos);pos[2]=hit.z-floors[kind]+.001
        ob=clone(full[kind-3] if kind>=3 else bodies[kind],f'Car_{i:03d}',pos,yaw,rt);ob.rotation_euler.y=roll;ob.rotation_euler.x=pitch;colorize(ob,kind,color,lights=speed<.5 and 'queue' in where)
        ob['speed_mps']=speed;ob['traffic_role']=where
        placements.append(dict(name=ob.name,body=('Hatch','SUV','Crossover','HeroHatch','HeroSUV','HeroCrossover')[kind],color=color,location=list(pos),yaw=yaw,speed_mps=speed,role=where))
        return ob
    # Busy afternoon: 1.15–1.9 seconds at 20–25m/s. The two-lane corridor
    # cannot reproduce the reference's larger lane count; density is per lane.
    for side in (-1,1):
        for lane in range(2):
            s=-p.length/2+rng.uniform(10,65)
            while s<p.length/2-10:
                speed=rng.uniform(20,25);pos=p.xyz(s,p.lane(side,lane));yaw=-math.degrees(s/p.radius if p.radius else 0)+(180 if side>0 else 0)
                actor(pos,yaw,'mainline',speed,math.atan(side*p.bank if p.bank else -.02));s+=speed*rng.uniform(1.15,1.9)
    # Retain the exact accepted near-car anchor for before/after scale.
    side,lane,s=(1,0,-26) if p.kind=='diamond' else (1,1,-22)
    pos=p.xyz(s,p.lane(side,lane))
    # Remove a potential flow placement within 10m of the retained actor.
    for row in placements[:]:
        if math.dist(row['location'],pos)<10:
            delete(bpy.data.objects[row['name']]);placements.remove(row)
    actor(pos,180-math.degrees(s/p.radius if p.radius else 0),'mainline',27,math.atan(side*p.bank if p.bank else -.02),True)
    if p.kind=='diamond':
        for side in (-1,1):
            for entry in (False,True):
                pts=list(map(Vector,ramp_points(p,side,entry,192)))
                # Stop queues belong to the off-ramp, entrance ramps remain flowing.
                indices=[18,48,81,118,152] if entry else [14,51,91,133,181,186,191]
                for j in indices:
                    v=pts[j];d=pts[j+1]-pts[j-1];yaw=math.degrees(math.atan2(d.x,-d.y))
                    # Forward is native -Y. Crossfall reverses with travel direction.
                    actor(v,yaw,'entrance' if entry else ('terminal_queue' if j>=178 else 'exit'),13 if entry else (0 if j>=178 else 18),-.02,pitch=-math.atan2(d.z,math.hypot(d.x,d.y)))
        for side in (-1,1):
            for lane,y in enumerate((side*3.3528,side*6.7056)):
                for x in range(-350,351,39 if lane else 57):
                    # Signal reservation is kept clear; queuing occurs upstream.
                    if abs(abs(x)-78)<20:continue
                    z=7.35-.02*abs(y);actor((x+rng.uniform(-4,4),y,z),90 if side<0 else -90,'arterial',12,-.02)
            for tx in (-78,78):
                for j in range(3):
                    x=tx+side*(23+j*6.9);y=side*6.7056;actor((x,y,7.35-.02*abs(y)),90 if side<0 else -90,'arterial_queue',0,-.02)
        for x,y in ((-19,3.3528),(9,-6.7056),(17,6.7056)):
            side=1 if y>0 else -1;actor((x,y,7.35-.02*abs(y)),90 if side<0 else -90,'bridge',12,-.02)
        for x,y,yaw in [(143.28,24.332,0),(155.10,24.332,180),(-143.28,-25.332,0),(-207,27,0),(-190,27,0),(-162,27,0)]:actor((x,y,7.05),yaw,'commercial_parked')
    else:
        for side in (-1,1):
            for j,s in enumerate(range(-430,431,76)):
                # Follow the actual first neighborhood street and its lane,
                # including offset-curve position and tangent, at flat grade.
                pos=list(p.xyz(s,side*(86+1.6)));pos[2]=.04
                yaw=-math.degrees(s/p.radius if p.radius else 0)+(180 if side>0 else 0)
                actor(pos,yaw,'neighborhood',8)
    for lib in [*bodies,*full]:delete(lib)
    rt['placements_json']=json.dumps(placements);return rt
