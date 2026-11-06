"""Presentation-only ground age, pole backfill and NC corner plan.

Original fields and placed blades/leaves; no neighboring asset is modified.
"""
import itertools,json,math,random
from pathlib import Path
import bpy
from mathutils import Vector
from kit import model as G


def matte(name,color,rough=.9):
    m=bpy.data.materials.new(name);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough
    return m


def ground_age(meta):
    """Patchiness follows walks, tree shade and disturbed installation soil."""
    for m in list(bpy.data.materials):
        if not m.use_nodes or not any(s in m.name for s in ('Context_Lawn','Context_Concrete')):continue
        ns,ls=m.node_tree.nodes,m.node_tree.links;bs=ns.get('Principled BSDF');original=bs.inputs['Base Color'].links[0].from_socket
        pos=ns.new('ShaderNodeNewGeometry');noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.42;noise.inputs['Detail'].default_value=3
        ls.new(pos.outputs['Position'],noise.inputs['Vector'])
        ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.24;ramp.color_ramp.elements[1].position=.75
        if 'Lawn' in m.name:
            ramp.color_ramp.elements[0].color=(.46,.39,.17,1);ramp.color_ramp.elements[1].color=(1.30,1.13,.68,1)
        else:
            ramp.color_ramp.elements[0].color=(.55,.52,.45,1);ramp.color_ramp.elements[1].color=(1.13,1.10,1.02,1)
        ls.new(noise.outputs['Fac'],ramp.inputs[0]);mul=ns.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1
        ls.new(original,mul.inputs[1]);ls.new(ramp.outputs[0],mul.inputs[2]);ls.new(mul.outputs[0],bs.inputs['Base Color'])
        if 'Lawn' in m.name:
            sep=ns.new('ShaderNodeSeparateXYZ');ls.new(pos.outputs['Position'],sep.inputs[0])
            absolute=ns.new('ShaderNodeMath');absolute.operation='ABSOLUTE';ls.new(sep.outputs['X'],absolute.inputs[0])
            nearest=[]
            for edge in (6.096,7.62):
                sub=ns.new('ShaderNodeMath');sub.operation='SUBTRACT';ls.new(absolute.outputs[0],sub.inputs[0]);sub.inputs[1].default_value=edge
                distance=ns.new('ShaderNodeMath');distance.operation='ABSOLUTE';ls.new(sub.outputs[0],distance.inputs[0]);nearest.append(distance.outputs[0])
            minimum=ns.new('ShaderNodeMath');minimum.operation='MINIMUM';ls.new(nearest[0],minimum.inputs[0]);ls.new(nearest[1],minimum.inputs[1])
            mask=ns.new('ShaderNodeMapRange');mask.inputs['From Min'].default_value=.015;mask.inputs['From Max'].default_value=.27;mask.inputs['To Min'].default_value=.65;mask.inputs['To Max'].default_value=0;ls.new(minimum.outputs[0],mask.inputs[0])
            vary=ns.new('ShaderNodeMath');vary.operation='MULTIPLY';ls.new(mask.outputs[0],vary.inputs[0]);ls.new(noise.outputs['Fac'],vary.inputs[1])
            worn=ns.new('ShaderNodeMixRGB');worn.inputs[2].default_value=(.10,.071,.031,1);ls.new(vary.outputs[0],worn.inputs[0]);ls.new(mul.outputs[0],worn.inputs[1]);ls.new(worn.outputs[0],bs.inputs['Base Color'])
        else:
            # Surface darkening follows the slab scores and settles unevenly.
            sep=ns.new('ShaderNodeSeparateXYZ');ls.new(pos.outputs['Position'],sep.inputs[0]);joint=ns.new('ShaderNodeMath');joint.operation='PINGPONG';joint.inputs[1].default_value=1.524;ls.new(sep.outputs['Y'],joint.inputs[0])
            mask=ns.new('ShaderNodeMapRange');mask.inputs['From Max'].default_value=.045;mask.inputs['To Min'].default_value=.42;mask.inputs['To Max'].default_value=0;ls.new(joint.outputs[0],mask.inputs[0])
            stain=ns.new('ShaderNodeMixRGB');stain.inputs[2].default_value=(.105,.095,.072,1);ls.new(mask.outputs[0],stain.inputs[0]);ls.new(mul.outputs[0],stain.inputs[1]);ls.new(stain.outputs[0],bs.inputs['Base Color'])
    soil=matte('Disturbed gravelly pole backfill',(.085,.062,.034));stones=matte('Pole backfill stones',(.18,.166,.132));grass=matte('Unmown grass at pole',(.084,.115,.025));dry=matte('Dry grass sheaths',(.18,.143,.060));leaf=matte('Shed leaf litter',(.105,.065,.023))
    ns,ls=soil.node_tree.nodes,soil.node_tree.links;bs=ns.get('Principled BSDF');noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=120;noise.inputs['Detail'].default_value=2
    bump=ns.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.007;ls.new(noise.outputs['Fac'],bump.inputs['Height']);ls.new(bump.outputs[0],bs.inputs['Normal'])
    rng=random.Random(meta['plan']['seed']+891)
    for row in meta['plan']['poles']:
        x,y,z=row['location'];n=96;vs=[(x,y,z-.006)];coverage=[1];faces=[]
        for ring in (0,1):
            for i in range(n):
                t=math.tau*i/n;r=(.32 if ring==0 else .49)+.025*math.sin(t*3)+.015*math.sin(t*7)+rng.uniform(-.004,.004)
                vs.append((x+r*math.cos(t),y+r*math.sin(t),z-.006));coverage.append(1 if ring==0 else 0)
        faces=[(0,i+1,(i+1)%n+1) for i in range(n)]
        faces.extend((i+1,n+i+1,n+(i+1)%n+1,(i+1)%n+1) for i in range(n))
        patch=G.mesh('Bare soil around pole installation',vs,faces,soil);attr=patch.data.attributes.new('BackfillCoverage','FLOAT','POINT')
        for d,v in zip(attr.data,coverage):d.value=v
        vs=[];fs=[]
        for tuft in range(18):
            t=rng.uniform(0,math.tau);r=rng.uniform(.18,.48);center=Vector((x+r*math.cos(t),y+r*math.sin(t),z-.0085))
            for i in range(18):
                p=center+Vector((rng.uniform(-.018,.018),rng.uniform(-.018,.018),0));length=rng.uniform(.045,.19);ang=rng.uniform(0,math.tau);w=rng.uniform(.0012,.0025)
                side=Vector((math.cos(ang),math.sin(ang),0))*w;lean=Vector((math.sin(ang),-math.cos(ang),0))*length*rng.uniform(.25,.65)
                mid=p+lean*.22+Vector((0,0,length*.6));tip=p+lean+Vector((0,0,length*.82))
                k=len(vs);vs.extend((p-side,p+side,mid-side*.48,mid+side*.48,tip));fs.extend(((k,k+1,k+3,k+2),(k+2,k+3,k+4)))
        ob=G.mesh('Unmown overlapping grass blades',vs,fs,grass);ob.data.materials.append(dry)
        for f in ob.data.polygons:f.material_index=int(rng.random()<.22)
        for i in range(35):
            t=rng.uniform(0,math.tau);r=rng.uniform(.18,.40);px,py=x+r*math.cos(t),y+r*math.sin(t);sz=rng.uniform(.006,.017)
            pebble=G.smooth(G.lathe('Rounded backfill aggregate',[(0,0),(.002,sz),(.008,sz*.83),(.011,0)],stones,8,center=(px,py)))
            pebble.location.z=z-.0085
    # Leaf litter accumulates under the actual near street-tree rows, while
    # worn lawn edges vary continuously along the pavement rather than stripes.
    vs=[];fs=[]
    for i in range(1200):
        yy=rng.uniform(-80,meta['plan']['length']+130);xx=rng.choice((-1,1))*rng.uniform(8.0,15.0);zz=.170
        if rng.random()>.35 and abs((yy+180)%31-15)>6:continue
        p=Vector((xx,yy,zz));t=rng.uniform(0,math.tau);d=Vector((math.cos(t),math.sin(t),0))*rng.uniform(.02,.055);s=Vector((-d.y,d.x,0))*.45
        k=len(vs);vs.extend((p-d,p+s,p+d+Vector((0,0,.006)),p-s));fs.append((k,k+1,k+2,k+3))
    G.mesh('Leaf litter beneath street trees',vs,fs,leaf)
    attr=soil.node_tree.nodes.new('ShaderNodeAttribute');attr.attribute_name='BackfillCoverage'
    soil.node_tree.links.new(attr.outputs['Fac'],soil.node_tree.nodes.get('Principled BSDF').inputs['Alpha']);soil.surface_render_method='DITHERED'


def nc_corner(context):
    """Coherent T corner and shallow approach bend, presentation only.

    Grade/road/walk geometry is authored as connected ribbons. Utility poles
    and their sockets keep their actual exported positions. Houses stay put.
    """
    for ob in context:
        if ob.parent is None and ob.name.startswith('Parked pickup') and ob.matrix_world.translation.y<25:
            ob.location.y+=110
    names=('Road_','Curb_','Walk_','Planting strip','Raised residential yards','Neighborhood grade')
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith(names):bpy.data.objects.remove(ob,do_unlink=True)
    mats={key:next(m for m in bpy.data.materials if m.name=='Context_'+key) for key in ('Asphalt','Concrete','Lawn')}
    def surface(name,vs,fs,mat):
        ob=G.mesh(name,vs,fs,mats[mat]);uv=ob.data.uv_layers.new(name='UVMap')
        for face in ob.data.polygons:
            for li in face.loop_indices:
                p=ob.data.vertices[ob.data.loops[li].vertex_index].co;tile=6.096 if mat=='Asphalt' else 3.048;uv.data[li].uv=(p.x/tile,p.y/tile)
        return ob
    def band(name,path,offset0,offset1,z,mat,end_tangents=None):
        vs=[]
        for i,p in enumerate(path):
            tangent=Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])
            if end_tangents and i in (0,len(path)-1):tangent=end_tangents[int(i>0)]
            normal=Vector((-tangent.y,tangent.x,0)).normalized()
            for off in (offset0,offset1):vs.append(Vector(p)+normal*off+Vector((0,0,z)))
        return surface(name,vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(path)-1)],mat)
    def wall(name,path,offset,end_tangents=None):
        vs=[]
        for i,p in enumerate(path):
            tangent=Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])
            if end_tangents and i in (0,len(path)-1):tangent=end_tangents[int(i>0)]
            normal=Vector((-tangent.y,tangent.x,0)).normalized()
            for z in (.022,.16764):vs.append(Vector(p)+normal*offset+Vector((0,0,z)))
        return surface(name,vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(path)-1)],'Concrete')
    def centre(y):
        t=max(0,min(1,(18-y)/42));return 2.2*t*t*(3-2*t)
    # Turf stays under paving; raised side yards stop at the actual walk edge.
    G.box('NC low continuous grade',(0,180,-.04),(1400,1400,.06),mats['Lawn'],0)
    path=[(centre(y),y,0) for y in range(-25,620,2)]
    band('NC main road',path,-4.1148,4.1148,.022,'Asphalt')
    surface('NC crossing road',[(-650,-31,.022),(650,-31,.022),(650,-23.0762,.022),(-650,-23.0762,.022)],[(0,1,2,3)],'Asphalt')
    # Ribbons begin above the return radius; continuous concrete faces have
    # no cracks between independently warped prefab modules.
    main=[p for p in path if p[1]>=-17]
    joint=Vector(main[0]);tangent=(Vector(main[1])-joint).normalized()
    joint_normal=Vector((-tangent.y,tangent.x,0));curb_center=(4.1148+4.2672)/2
    main_edges={};return_edges={};cross_edges={}
    for side in (-1,1):
        offsets=sorted((side*4.1148,side*4.2672));curb=band('NC continuous curb crown',main,*offsets,.16764,'Concrete')
        wall('NC cast curb road face',main,side*4.1148)
        offsets=sorted((side*4.2672,side*6.096));band('NC planting verge',main,*offsets,.159,'Lawn')
        offsets=sorted((side*6.096,side*7.62));walk=band('NC continuous walk',main,*offsets,.16764,'Concrete')
        main_edges[-side]=(curb,walk)
        offsets=sorted((side*7.62,side*650));band('NC raised yards',main,*offsets,.16764,'Lawn')
        # Match the actual bent ribbon's endpoint and tangent, not its
        # un-offset centreline. Solve each roughly six-metre return so both
        # end exactly on the crossing curb's common centreline at y=-23.
        start=joint-joint_normal*(side*curb_center)
        radius=(start.y+23)/(1+side*joint_normal.y)
        center=start-joint_normal*(side*radius)
        start_angle=math.atan2(start.y-center.y,start.x-center.x)
        sweep=-math.pi/2-start_angle
        arc=[]
        for i in range(33):
            a=start_angle+sweep*i/32
            arc.append((center.x+radius*math.cos(a),center.y+radius*math.sin(a),0))
        end_tangents=(-tangent,Vector((side,0,0)))
        curved_curb=band('NC curved curb return',arc,-.0762,.0762,.16764,'Concrete',end_tangents)
        wall('NC curved curb road face',arc,-.0762 if side>0 else .0762,end_tangents)
        walk_offsets=sorted((side*(6.096-curb_center),side*(7.62-curb_center)))
        curved_walk=band('NC curved corner walk',arc,*walk_offsets,.16764,'Concrete',end_tangents)
        return_edges[side]=(curved_curb,curved_walk)
        x0,x1=(center.x,650) if side>0 else (-650,center.x)
        crossing_curb=surface('NC crossing curb crown',[(x0,-23.0762,.16764),(x1,-23.0762,.16764),(x1,-22.9238,.16764),(x0,-22.9238,.16764)],[(0,1,2,3)],'Concrete')
        # The curved walk ends farther into the corner than the curb. Its
        # crossing continuation must use that same offset and width.
        walk_y=-23+6.096-curb_center
        crossing_walk=surface('NC cross street north walk',[(x0,walk_y,.16764),(x1,walk_y,.16764),(x1,walk_y+1.524,.16764),(x0,walk_y+1.524,.16764)],[(0,1,2,3)],'Concrete')
        cross_edges[side]=(crossing_curb,crossing_walk)
        wall('NC crossing curb face',[(x0,-23.0762,0),(x1,-23.0762,0)],0)
        boundary=[(p[0],p[1],.159) for p in arc]+[(side*650,-23,.159),(side*650,-17,.159)]
        surface('NC raised grass corner',boundary,[tuple(range(len(boundary)))],'Lawn')
    # Measure the built mesh edges, including finite curve endpoint normals.
    # This proves curb/walk continuity, not a surveyed photographic road plan.
    joins=[]
    for side in (-1,1):
        for role,straight,curved,crossing in zip(('curb','walk'),main_edges[side],return_edges[side],cross_edges[side]):
            pairs=((straight,(0,1),curved,(0,1),'approach'),(curved,(-2,-1),crossing,(0,3) if side>0 else (1,2),'crossing'))
            for a,ai,b,bi,end in pairs:
                aa=[a.data.vertices[i].co for i in ai];bb=[b.data.vertices[i].co for i in bi]
                gap=min(max((p-q).length for p,q in zip(aa,order)) for order in itertools.permutations(bb))
                assert gap<.001,(side,role,end,gap)
                joins.append(dict(side=side,role=role,end=end,measured_maximum_endpoint_gap_m=gap))
    Path('build/nc-corner-joins.json').write_text(json.dumps(dict(scope='Actual built curb/walk mesh edge endpoints; presentation only',joins=joins),indent=2))
    surface('NC opposite corner walk',[(-650,-32.5,.16764),(650,-32.5,.16764),(650,-31,.16764),(-650,-31,.16764)],[(0,1,2,3)],'Concrete')
    wall('NC opposite crossing curb face',[(-650,-31,0),(650,-31,0)],0)
