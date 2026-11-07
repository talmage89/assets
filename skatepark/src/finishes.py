"""Shared baked PBR bindings and local, cause-driven service history."""
import math,random
from pathlib import Path
import bpy
from mathutils import Vector
import geometry as Q
from kit import tiling
from textures import RECTS
CACHE={}
REPO=Path(__file__).resolve().parents[2]

def materials():
    # Initialize Blender's complete 5.2 metadata interface before kit tiling
    # binds Occlusion. Native context imports also request its newer sockets.
    from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
    get_settings_group()
    for key,name in [('Concrete','Concrete'),('Asphalt','Asphalt'),('Lawn','Lawn')]:
        mat=tiling.material(name,REPO/'ground/textures/ship',tint=True)
        mat.name='Skate_'+key;Q.M[key]=mat
        if key=='Concrete':
            nodes=mat.node_tree.nodes;links=mat.node_tree.links;bs=nodes.get('Principled BSDF')
            normal=next(n for n in nodes if n.bl_idname=='ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.16
            rough=bs.inputs['Roughness'].links[0].from_socket;mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=.79;links.new(rough,mul.inputs[0]);links.new(mul.outputs[0],bs.inputs['Roughness'])
    Q.M['Walk']=tiling.material('Concrete',REPO/'ground/textures/ship',tint=True);Q.M['Walk'].name='Skate_BroomWalk'
    for key in ('Steel','Coping','Tile','Grout','Paint','Zinc','ToePlate','Burnish','Scrape','Tag','Dirt','Crack','Rules'):
        mat=tiling.material('SkateTrim',Path('textures/ship'),tint=True);mat.name='Skate_Trim_'+key
        next(n for n in mat.node_tree.nodes if n.bl_idname=='ShaderNodeNormalMap').inputs['Strength'].default_value=.28
        if key in ('Burnish','Scrape','Tag','Dirt','Crack'):
            from kit.export import atlas_material
            # Stock glTF mask. The marks contain absorbed material color, not
            # a reflective transparent film laid above the concrete.
            nodes=mat.node_tree.nodes;links=mat.node_tree.links;bs=nodes.get('Principled BSDF')
            tex=next(n for n in nodes if n.bl_idname=='ShaderNodeTexImage' and 'BaseColor' in n.image.name)
            clip=nodes.new('ShaderNodeMath');clip.operation='GREATER_THAN';clip.inputs[1].default_value=.16
            links.new(tex.outputs['Alpha'],clip.inputs[0]);links.new(clip.outputs[0],bs.inputs['Alpha']);mat.surface_render_method='DITHERED';mat.use_backface_culling=False
        Q.M[key]=mat
    Q.M['Wax']=Q.M['Burnish'].copy();Q.M['Wax'].name='Skate_AbsorbedWax'
    bs=Q.M['Wax'].node_tree.nodes.get('Principled BSDF')
    rough=bs.inputs['Roughness'].links[0].from_socket
    mul=Q.M['Wax'].node_tree.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=.58
    Q.M['Wax'].node_tree.links.new(rough,mul.inputs[0]);Q.M['Wax'].node_tree.links.new(mul.outputs[0],bs.inputs['Roughness'])
    Q.M['Leaf']=Q.M['Dirt'].copy();Q.M['Leaf'].name='Skate_LeafLitter'
    bs=Q.M['Leaf'].node_tree.nodes.get('Principled BSDF')
    for link in list(bs.inputs['Alpha'].links):Q.M['Leaf'].node_tree.links.remove(link)
    bs.inputs['Alpha'].default_value=1
    Q.M['Composite']=tiling.material('Prefab',Path('textures/ship'),tint=True);Q.M['Composite'].name='Skate_Phenolic'
    # Every opaque trim region has identical PBR inputs: one runtime material.
    # Construction labels select UV rectangles, not redundant draw states.
    for key in ('Coping','Tile','Grout','Paint','Zinc','ToePlate','Rules','Leaf'):Q.M[key]=Q.M['Steel']
    for key in ('Scrape','Tag','Dirt','Crack'):Q.M[key]=Q.M['Burnish']
    Q.M['Side']=Q.M['Concrete']
    # Small constant colors sample appropriate opaque trim patches.
    for key,source in [('White','Grout'),('Black','Paint'),('Joint','Grout')]:Q.M[key]=Q.M[source]

def trim_uv(ob,key):
    rect=RECTS.get(key,RECTS['Paint']);u0,v0,u1,v1=rect;pad=8/2048
    if key=='Steel':u0,u1=1/6,1/3  # library's middle-age lane
    uv=ob.data.uv_layers.active
    pts=[ob.matrix_basis@v.co for v in ob.data.vertices]
    lo=[min(v[k] for v in pts) for k in range(3)];hi=[max(v[k] for v in pts) for k in range(3)];size=[hi[k]-lo[k] for k in range(3)];long=max(range(3),key=lambda k:size[k])
    for f in ob.data.polygons:
        for li in f.loop_indices:
            p=pts[ob.data.loops[li].vertex_index]
            u=(p[long]-lo[long])/max(size[long],1e-8)
            if key=='Steel':
                short=max((k for k in range(3) if k!=long),key=lambda k:size[k])
                cross=(p[short]-lo[short])/max(size[short],1e-8)
                v=.40+.20*cross if f.normal.z>.45 else .04+.28*cross
                if long==0 and size[1]<.09 and size[2]<.09:
                    v=(math.atan2(p.y-(lo[1]+hi[1])/2,p.z-(lo[2]+hi[2])/2)/math.tau+.5)%1
            elif key=='Coping' and ob.get('coping_profile_vertices'):
                from contour import rim_xy,normal_xy
                # Six tangent stations per original block; radial top width
                # remains a stable cross-profile coordinate around the bowl.
                vertex=ob.data.loops[li].vertex_index;L=ob['coping_profile_vertices'];q,j=divmod(vertex,L)
                profile=[(.285,-.03175),(.012,-.03175)]+[(.012-.03175*math.sin(k*math.pi/8),-.03175*math.cos(k*math.pi/8)) for k in range(1,9)]+[(.285,.03175)]
                u=q/5;v=(profile[j][0]+.01975)/.30475
            elif key=='Tile':
                # One authored 51mm tile face samples one cell, not 64 tiny tiles.
                ids=list(f.vertices);ii=ids.index(ob.data.loops[li].vertex_index)
                cell=(sum(ord(c) for c in ob.name)%64);u=(cell%8+(1 if ii in (1,2) else 0)) /8
                v=(cell//8+(1 if ii in (2,3) else 0))/8
            else:
                normal=ob.matrix_basis.to_3x3().inverted().transposed()@f.normal
                axes=sorted(range(3),key=lambda k:abs(normal[k]))[:2]
                u=(p[axes[0]]-lo[axes[0]])/max(size[axes[0]],1e-8)
                v=(p[axes[1]]-lo[axes[1]])/max(size[axes[1]],1e-8)
            uv.data[li].uv=(u0+pad+u*(u1-u0-2*pad),v0+pad+v*(v1-v0-2*pad))
        # Tube end caps and narrow folded gauges need their own planar chart.
        # Never let a constant cross-profile coordinate collapse their tangents.
        loops=list(f.loop_indices);coords=[uv.data[li].uv.copy() for li in loops]
        area=sum(a.x*b.y-a.y*b.x for a,b in zip(coords,coords[1:]+coords[:1]))*.5
        if abs(area)<1e-12:
            normal=ob.matrix_basis.to_3x3().inverted().transposed()@f.normal
            axes=sorted(range(3),key=lambda k:abs(normal[k]))[:2]
            for li in loops:
                p=pts[ob.data.loops[li].vertex_index]
                uv.data[li].uv=(u0+pad+(p[axes[0]]-lo[axes[0]])/max(size[axes[0]],1e-8)*(u1-u0-2*pad),v0+pad+(p[axes[1]]-lo[axes[1]])/max(size[axes[1]],1e-8)*(v1-v0-2*pad))

def prepare(roots):
    """Bind source materials before consolidation, retaining metric charts."""
    for rt in roots:
        for ob in [rt,*rt.children_recursive]:
            if ob.type!='MESH':continue
            # Original source name survives until this stage, before join.
            key=ob.get('finish_key') or next((k for k,m in Q.M.items() if ob.data.materials and ob.data.materials[0]==m),None)
            key={'Side':'Concrete','Black':'Paint','White':'Coping','Joint':'Grout','Leaf':'Dirt'}.get(key,key)
            if key in RECTS and key!='Rules':trim_uv(ob,key)
            elif key=='Composite':
                uv=ob.data.uv_layers.active;xs=[v.co.x for v in ob.data.vertices];xmin,xmax=min(xs),max(xs)
                for f in ob.data.polygons:
                    for li in f.loop_indices:
                        v=ob.data.vertices[ob.data.loops[li].vertex_index].co
                        distance=v.y
                        if 'transition_radius_m' in rt and 'profile_run_m' in rt:
                            r=rt['transition_radius_m'];h=rt['height_m'];run=rt['profile_run_m'];angle=math.acos(1-h/r)
                            distance=r*math.atan2(v.y+run/2,r-v.z) if v.y<=run/2+.001 else r*angle+v.y-run/2
                        width=rt['footprint_m'][0]
                        uv.data[li].uv=((v.x+width/2)/width,distance/4.8768)
                # Finite sheet gauges need a physical planar chart too.
                for face in ob.data.polygons:
                    rows=list(face.loop_indices);q=[uv.data[li].uv.copy() for li in rows]
                    if abs(sum(a.x*b.y-a.y*b.x for a,b in zip(q,q[1:]+q[:1])))<1e-12:
                        axes=sorted(range(3),key=lambda k:abs(face.normal[k]))[:2]
                        for li in rows:
                            p=ob.data.vertices[ob.data.loops[li].vertex_index].co
                            uv.data[li].uv=(p[axes[0]]/4.8768,p[axes[1]]/4.8768)
            elif key=='Concrete' and 'profile_run_m' in rt:
                uv=ob.data.uv_layers.active;r=rt['transition_radius_m'];run=rt['profile_run_m'];angle=math.acos(1-rt['height_m']/r)
                for face in ob.data.polygons:
                    if abs(face.normal.x)>.1 or face.normal.z<.01:continue
                    for li in face.loop_indices:
                        p=ob.matrix_basis@ob.data.vertices[ob.data.loops[li].vertex_index].co
                        d=r*math.atan2(p.y+run/2,r-p.z) if p.y<=run/2+.001 else r*angle+p.y-run/2
                        uv.data[li].uv=(p.x/3.048,d/3.048)
            if key and 'Tint' not in ob.data.color_attributes:
                c=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER')
                for row in c.data:row.color=(1,1,1,1)
            if key=='Asphalt':
                # Keep the accepted Ground pixels. As in the strip's value
                # correction, the wearing-course tint controls site albedo.
                for row in ob.data.color_attributes['Tint'].data:row.color=(.45,.45,.445,1)
                for row in ob.data.uv_layers.active.data:row.uv*=.5

def ribbon(rt,name,stations,width,key,age=.6,normals=None):
    """Small authored geometry follows the exact ride surface, with baked marks."""
    verts=[];columns=len(stations[0])
    for row in stations:verts.extend(row)
    faces=[(columns*i+j,columns*i+j+1,columns*(i+1)+j+1,columns*(i+1)+j) for i in range(len(stations)-1) for j in range(columns-1)]
    if normals:
        faces=[tuple(reversed(f)) if (Vector(verts[f[1]])-Vector(verts[f[0]])).cross(Vector(verts[f[2]])-Vector(verts[f[0]])).dot(Vector(normals[f[0]]))<0 else f for f in faces]
    ob=Q.mesh(name,verts,faces,rt,key);uv=ob.data.uv_layers.active;u0,v0,u1,v1=RECTS['Burnish' if key=='Wax' else key];pad=8/2048
    ob['surface_mark']=True
    if normals:
        for face in ob.data.polygons:face.use_smooth=True
        ob.data.normals_split_custom_set_from_vertices(normals)
    for f in ob.data.polygons:
        for li in f.loop_indices:
            i=ob.data.loops[li].vertex_index;uv.data[li].uv=(u0+pad+(i%columns)/(columns-1)*(u1-u0-2*pad),v0+pad+(i//columns)/(len(stations)-1)*(v1-v0-2*pad))
    if key=='Wax':
        for row in ob.data.color_attributes['Tint'].data:row.color=(.33,.31,.28,1)
    return ob

def weather(rt,p):
    age=p['age'];rng=random.Random(p['seed']+sum(ord(c) for c in rt.name))
    # Per-pour value variation is cast/service history, not a universal wash.
    for ob in rt.children_recursive:
        if ob.type!='MESH' or not ob.data.materials:continue
        copied=False
        if any(m and m.name.startswith(('Skate_Concrete','Skate_Phenolic','Skate_Broom')) for m in ob.data.materials):
            ob.data=ob.data.copy();copied=True;attr=ob.data.color_attributes.get('Tint') or ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER')
            for f in ob.data.polygons:
                m=ob.data.materials[f.material_index]
                if not m or not m.name.startswith(('Skate_Concrete','Skate_Phenolic','Skate_Broom')):continue
                for li in f.loop_indices:
                    v=ob.data.vertices[ob.data.loops[li].vertex_index].co
                    value=min(1.,1.01-age*.08+.025*math.sin(v.x*.71+v.y*.37)+.012*math.sin(v.y*4.3+v.x*2.1))
                    if 'Bowl_Sector' in rt.name and v.z<-.03:
                        u,arc=ob.data.uv_layers.active.data[li].uv
                        # Pumping lines circle the pockets, rising/falling as
                        # riders exchange height for speed. Lip contact adds
                        # a separate narrow abrasion zone beneath the coping.
                        flow=math.exp(-((arc-(.28+.11*math.sin(u*2.7)))/.18)**4)
                        lip=math.exp(v.z/.13)*(.55+.45*math.sin(u*3.1)**2)
                        value*=1-age*(.55*flow+.32*lip)
                    # Dark damp/grit on vertical retaining faces at grade.
                    if f.normal.z<.3:value*=1-age*.13*math.exp(-max(0,v.z)*5)
                    attr.data[li].color=(value,value*.997,value*.98,1)
        if any(m and m.name.startswith('Skate_Trim_Steel') for m in ob.data.materials):
            if not copied:ob.data=ob.data.copy()
            uv=ob.data.uv_layers.active;slot=0 if age<.5 else 1 if age<.85 else 2;pad=8/2048
            for face in ob.data.polygons:
                rows=list(face.loop_indices)
                if not all(1/6-1e-5<=uv.data[li].uv.x<=1/3+1e-5 and uv.data[li].uv.y>.75 for li in rows):continue
                for li in rows:
                    f=(uv.data[li].uv.x-(1/6+pad))/(1/6-2*pad)
                    uv.data[li].uv.x=slot/6+pad+f*(1/6-2*pad)
    if 'transition_radius_m' in rt and 'profile_run_m' in rt:
        r=rt['transition_radius_m'];h=rt['height_m'];L=rt['profile_run_m'];a=math.acos(1-h/r);w=rt['footprint_m'][0]
        count=rng.choice((1,2,2,3));centers=(0,) if count==1 else (-.25*w,.24*w) if count==2 else (-.30*w,0,.30*w)
        for k,x in enumerate(centers):
            x+=rng.uniform(-.10,.10)*w;phase=rng.uniform(-1,1)
            stations=[];lane_normals=[]
            for j in range(25):
                t=a*(.08+.89*j/24);y=-L/2+r*math.sin(t);z=r*(1-math.cos(t));normal=Vector((0,-math.sin(t),math.cos(t)))
                cx=x+.16*math.sin(j*.17+k+phase);width=(.35+.75*age)*(.82+.18*math.sin(j*.10+phase)) if p['type']=='poured' else .44
                stations.append([Vector((cx+s*width/2,y,z))+normal*.0012 for s in (-1,1)])
                lane_normals.extend([normal,normal])
            if p['type']=='poured':ribbon(rt,'Burnished wheel approach lane',stations,.65,'Burnish',age,lane_normals)
        stations=[];scrape_normals=[]
        for j in range(20):
            x=-w/2+j*w/19;pair=[]
            for theta in (a-.24/r,a-(.24-.22/3)/r,a-(.24-.44/3)/r,a-.02/r):
                normal=Vector((0,-math.sin(theta),math.cos(theta)))
                pair.append(Vector((x,-L/2+r*math.sin(theta),r*(1-math.cos(theta))))+normal*.0013);scrape_normals.append(normal)
            stations.append(pair)
        ribbon(rt,'Board slide and urethane scars below coping',stations,.2,'Scrape',age,scrape_normals)
    if 'bank_angle_degrees' in rt and 'deck_m' in rt and p['type']=='poured':
        h=rt['height_m'];angle=math.radians(rt['bank_angle_degrees']);run=h/math.tan(angle)+.18*math.tan(angle/2);w=rt['footprint_m'][0]
        for s in (-1,1):
            x=s*w*.24+rng.uniform(-.05,.05)*w;stations=[];width=.38+.45*age
            for j in range(21):
                y=-run/2+.10+(run-.16)*j/20;z=h-(run/2-y)*math.tan(angle);n=Vector((0,-math.sin(angle),math.cos(angle)))
                stations.append([Vector((x+side*width/2,y,z))+n*.0011 for side in (-1,1)])
            ribbon(rt,'Worn approach on the bank ride line',stations,width,'Burnish',age)
    if rt.name.startswith(('Ledge_18in','ManualPad','Prefab_GrindBox')):
        # Grind contact is blackened wax along the top edges, concrete stays open.
        w,length=rt['footprint_m'];h=rt['height_m']
        for s in (-1,1):
            x=s*(w/2-.055)
            ribbon(rt,'Absorbed polished ledge wax',[[ (x-.03,-length/2+.018+j*(length-.036)/16,h+.0016),(x+.03,-length/2+.018+j*(length-.036)/16,h+.0016)] for j in range(17)],.06,'Wax',age)
    if rt.name.startswith('SkatingFlatwork'):
        for k in range(3 if age<.5 else 7):
            x=(1+k%5)*3.048;y=-(1+k//3)*3.048
            ribbon(rt,'Crack starting at an actual saw-cut corner',[[ (x-.20+j*.06,y+j*.22,.001),(x+.20+j*.06,y+j*.22,.001)] for j in range(6)],.4,'Crack',age)
        for k in range(1 if age<.5 else 3):
            x=(2+k)*3.048;y=-(1+k%2)*3.048
            ob=Q.mesh('Local saw-cut repair adjoining a joint',[(x-.15,y-.12,.0008),(x+.62,y-.12,.0008),(x+.69,y+.31,.0008),(x+.57,y+.42,.0008),(x-.15,y+.42,.0008)],[(0,1,2,3,4)],rt,'Concrete')
            for row in ob.data.color_attributes['Tint'].data:row.color=(.84,.83,.80,1)
    if rt.name.startswith(('Quarter','Bank')) and rt['height_m']>.9 and (rt.name.endswith('_2') or (age>.5 and rt.name.endswith('_4'))):
        h=rt['height_m'];w=rt['footprint_m'][0];y=rt.get('profile_run_m',rt['footprint_m'][1]-rt['deck_m'])/2+rt['deck_m']+.001
        ribbon(rt,'Moderate fictional retaining-wall tag',[[(-.9,y,.28),(.9,y,.28)],[(-.9,y,min(.9,h-.1)),(.9,y,min(.9,h-.1))]],1.8,'Tag',age)
    if rt.name=='UpperStreetPlaza':
        cx=p['plaza']['stair_x']+3.2;y=p['plaza']['bounds'][2]-.0015
        ribbon(rt,'Small fictional plaza tag on retaining concrete',[[ (cx-.75,y,.14),(cx+.75,y,.14)],[(cx-.75,y,.53),(cx+.75,y,.53)]],1.5,'Tag',age)
    if rt.name.startswith('Prefab_Quarter_0'):
        w=rt['footprint_m'][0];y=rt['profile_run_m']/2+.15
        ribbon(rt,'Old fictional tag on sheltered prefab side',[[(-w/2-.0025,y,.15),(-w/2-.0025,y+1.1,.15)],[(-w/2-.0025,y,.73),(-w/2-.0025,y+1.1,.73)]],1.1,'Tag',age)

def basin_deposits(roots,p):
    if not p['bowl']:return
    from mathutils.bvhtree import BVHTree
    floor_roots=[r for r in roots if 'Bowl_Floor' in r.name]
    bpy.context.view_layer.update();owner=next(r for r in floor_roots if any(o.get('socket_kind')=='drain' for o in r.children_recursive))
    verts=[];faces=[]
    for rt in floor_roots:
        for ob in rt.children_recursive:
            if ob.type!='MESH':continue
            n=len(verts);verts += [owner.matrix_world.inverted()@ob.matrix_world@v.co for v in ob.data.vertices]
            ob.data.calc_loop_triangles();faces += [tuple(n+i for i in t.vertices) for t in ob.data.loop_triangles if t.normal.z>.2]
    tree=BVHTree.FromPolygons(verts,faces,all_triangles=True)
    def surface(x,y):
        hit=tree.ray_cast(Vector((x,y,1)),Vector((0,0,-1)))[0]
        return hit+Vector((0,0,.0018)) if hit else None
    spread=.8+1.8*p['age']
    # Clip the actual floor triangles into the deposit footprint. This keeps
    # every interior sample on its source plane, including the warped clover
    # sump, without a second independently tessellated floating surface.
    x0,x1=4-spread/2,4+spread/2;y0,y1=-spread*.60,spread*.60
    def clip(poly,axis,value,sign):
        out=[];previous=poly[-1];a=sign*(previous[axis]-value)
        for current in poly:
            b=sign*(current[axis]-value)
            if (a>=0)!=(b>=0):out.append(previous+(current-previous)*(a/(a-b)))
            if b>=0:out.append(current)
            previous=current;a=b
        return out
    vertices=[];polygons=[]
    for face in faces:
        poly=[Vector(verts[i]) for i in face]
        for axis,value,sign in [(0,x0,1),(0,x1,-1),(1,y0,1),(1,y1,-1)]:
            if poly:poly=clip(poly,axis,value,sign)
        if len(poly)<3 or (poly[1]-poly[0]).cross(poly[2]-poly[0]).length<1e-9:continue
        polygons.append(tuple(range(len(vertices),len(vertices)+len(poly))));vertices += [v+Vector((0,0,.0018)) for v in poly]
    dirt=Q.mesh('Sediment fan leaves the actual drain opening clear',vertices,polygons,owner,'Dirt');dirt['surface_mark']=True
    u0,v0,u1,v1=RECTS['Dirt'];pad=8/2048
    for face in dirt.data.polygons:
        for li in face.loop_indices:
            point=dirt.data.vertices[dirt.data.loops[li].vertex_index].co
            dirt.data.uv_layers.active.data[li].uv=(u0+pad+(point.x-x0)/(x1-x0)*(u1-u0-2*pad),v0+pad+(point.y-y0)/(y1-y0)*(v1-v0-2*pad))
    rng=random.Random(p['seed']+701);age=p['age']
    # Fallen leaf blades are original polygon silhouettes, gathered where
    # water carries them. They are litter, not a newly modeled tree family.
    for k in range(round(24+age*85)):
        x=4+rng.gauss(0,.56);y=rng.gauss(0,.48)
        if 3.80<x<4.20 and abs(y)<.20:continue
        c=surface(x,y)
        if c is None:continue
        angle=rng.random()*math.tau;length=rng.uniform(.035,.085);width=length*.43
        u=Vector((math.cos(angle),math.sin(angle),0));v=Vector((-u.y,u.x,0))
        points=[c-u*length*.5,c-u*length*.2+v*width*.5,c+u*length*.42+v*width*.25,c+u*length*.5,c+u*length*.1-v*width*.5]
        ob=Q.mesh('Dry leaf trapped beside drain',points,[(4,3,2,1,0)],owner,'Leaf')
        ob['fallen_litter']=True
        # Opaque soil/leaf tint samples retained texels in the shared strip.
        u0,v0,u1,v1=RECTS['Dirt']
        for li,row in enumerate(ob.data.uv_layers.active.data):
            q=((0,.5),(.3,1),(.9,.75),(1,.5),(.6,0))[ob.data.loops[li].vertex_index]
            row.uv=(u0+(u1-u0)*(.25+.5*q[0]),v0+(v1-v0)*(.25+.5*q[1]))
        for row in ob.data.color_attributes['Tint'].data:row.color=(1.,.81,.47,1)

def surface_mark_contacts(roots):
    """Actual nearest-surface distances, not declarations of decal offsets."""
    from mathutils.bvhtree import BVHTree
    bpy.context.view_layer.update();verts=[];faces=[];marks=[]
    for rt in roots:
        for ob in rt.children_recursive:
            if ob.type!='MESH':continue
            if ob.get('surface_mark'):marks.append(ob);continue
            if ob.get('fallen_litter'):continue
            n=len(verts);verts += [ob.matrix_world@v.co for v in ob.data.vertices]
            ob.data.calc_loop_triangles();faces += [tuple(n+i for i in tri.vertices) for tri in ob.data.loop_triangles]
    if not marks:return None
    tree=BVHTree.FromPolygons(verts,faces,all_triangles=True);rows=[]
    for ob in marks:
        samples=[ob.matrix_world@v.co for v in ob.data.vertices]
        samples += [ob.matrix_world@f.center for f in ob.data.polygons]
        errors=[tree.find_nearest(p)[3] for p in samples]
        maximum=max(errors);assert maximum<.004,(ob.name,maximum)
        rows.append(dict(mark=ob.name,samples=len(samples),maximum_surface_distance_m=maximum))
    return dict(marks=rows,maximum_surface_distance_m=max(r['maximum_surface_distance_m'] for r in rows),scope='Source marks against actual skating triangles; deliberate millimeter overlays, with GLB serialization checked separately')
