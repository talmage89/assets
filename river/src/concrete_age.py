"""Placement-owned concrete aging over the unchanged freeway mineral maps.

Like freeway.weather, sample causes on actual surface positions into COLOR_0.
Clipped planar cells preserve construction, UVs and interpolated split normals.
The existing maintenance atlas supplies pores and shallow form-tie recesses.
"""
import math
import random
import bpy
from mathutils import Vector
import geometry as G


def clip(poly,axis,limit,keep):
    result=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        da=(a[0][axis]-limit)*keep;db=(b[0][axis]-limit)*keep
        if da>=-1e-7:result.append(a)
        if (da<0<db) or (db<0<da):
            t=da/(da-db)
            result.append(tuple(u.lerp(v,t) for u,v in zip(a,b)))
    clean=[]
    for item in result:
        if not clean or (item[0]-clean[-1][0]).length_squared>1e-14:clean.append(item)
    if len(clean)>1 and (clean[0][0]-clean[-1][0]).length_squared<1e-14:clean.pop()
    return clean


def shade(point,local,normal,name,phase,plan):
    x,y,z=point;u=local.x if abs(normal.y)>.6 else local.y
    panel=math.floor((u+.13)/2.44);lift=math.floor((local.z+.08)/1.22)
    pour=.88+.10*math.sin(panel*13.71+lift*7.31+phase)
    # Uneven cement paste, form oil and persistent moisture, in meter space.
    field=.11*math.sin(u*2.6+local.z*3.1+phase)+.07*math.sin(u*8.3-local.z*1.7)
    value=pour+field
    ground=0 if plan is None else plan.water_z(y)
    if plan is not None and name.startswith('Abutment'):
        from channel import surface_z
        ground=surface_z(plan,x,y)
    level=z-ground
    if name.startswith(('Pier','Abutment','Floodwall','Opposite')):
        water=.38+.09*math.sin(u*3.7+phase)+.035*math.sin(u*13)
        damp=math.exp(-(max(0,level)/.55)**1.4)
        algae=max(0,min(1,(water-level)/.20))
        if name.startswith('Abutment'):
            algae*=max(0,min(1,(.45-(z-(plan.water_z(y) if plan else 0)))/.20))
        value*=1-.48*damp
        if name.startswith(('Floodwall','Opposite')):
            # A flood leaves a broken remnant above normal water; recesses
            # stay damp longer than exposed panel crowns.
            band=math.exp(-((level-1.12-.06*math.sin(u*2.3))/.16)**2)
            value*=1-.16*band*(.45+.55*math.sin(u*3.2+phase)**2)
        # Head-connected leakage under the cap, varying with circumference.
        if name.startswith('Pier'):
            stream=(.5+.5*math.sin(u*14+phase+.06*math.sin(z*4)))**12
            value*=1-.24*stream*min(1,max(0,level)/1.2)
    else:algae=0
    # Correct the warm canonical cement toward neutral weathered gray.
    return (max(.08,value*.59)*(1-.12*algae),max(.08,value*.65),
            max(.08,value*.76)*(1-.24*algae),1)


def apply(root,plan=None):
    bpy.context.view_layer.update();objects=list(root.children_recursive)
    if root.type=='MESH':objects.append(root)
    details={}
    for ob in objects:
        if ob.type!='MESH' or ob.get('river_category') not in ('bridge','site'):continue
        me=ob.data;roles={i for i,m in enumerate(me.materials) if m in (G.M['concrete'],G.M['bridge_concrete'])}
        if not roles:continue
        name=ob.name;phase=sum((i+1)*ord(c) for i,c in enumerate(name))*.013
        support=name.startswith(('Pier','Abutment','FloodwallTrail','OppositeFloodwall'))
        uv=me.uv_layers.active;vc=me.color_attributes.get('Tint');oldnorm=me.corner_normals
        vertices=[];faces=[];data=[];tags=[];rng=random.Random(round(phase*10000))
        batch=details.setdefault(ob.get('river_category'),G.Batch('ConcreteFormEvidence_'+ob.get('river_category'),root,ob.get('river_category')))
        for face in me.polygons:
            poly=[]
            for li in face.loop_indices:
                vi=me.loops[li].vertex_index
                color=vc.data[li if vc.domain=='CORNER' else vi].color if vc else (1,1,1,1)
                poly.append((me.vertices[vi].co.copy(),Vector(uv.data[li].uv),Vector(color),oldnorm[li].vector.copy()))
            concrete=face.material_index in roles;cells=[poly]
            if concrete and support and abs(face.normal.z)<.5:
                manufacture(batch,ob,face,poly)
            if concrete and support and ob.get('river_category')=='bridge' and abs(face.normal.z)<.15:
                forms(batch,ob,face,poly)
            if concrete and support and ob.get('river_category')=='bridge' and abs(face.normal.z)<.5:
                axis=0 if abs(face.normal.y)>.6 else 1
                spacing=((axis,1.0),(2,.48))
                for ax,step in spacing:
                    split=[]
                    for cell in cells:
                        lo=min(v[0][ax] for v in cell);hi=max(v[0][ax] for v in cell)
                        for k in range(math.floor(lo/step),math.floor(hi/step)+1):
                            part=clip(clip(cell,ax,k*step,1),ax,(k+1)*step,-1)
                            if len(part)>=3:split.append(part)
                    cells=split
            for cell in cells:
                if len(cell)<3:continue
                points=[v[0] for v in cell]
                area=sum((points[i]-points[0]).cross(points[i+1]-points[0]).length/2 for i in range(1,len(points)-1))
                if area<1e-10:continue
                start=len(vertices);vertices.extend(points);faces.append(tuple(range(start,start+len(cell))))
                tags.append((face.material_index,face.use_smooth))
                for pos,tex,col,norm in cell:
                    if concrete:
                        world=ob.matrix_world@pos;mul=shade(world,pos,face.normal,name,phase,plan)
                        col=Vector(tuple(col[i]*mul[i] for i in range(4)))
                    data.append((tex,col,norm))
                # Small voids remain shallow alpha recesses; never stone geometry.
                if concrete and support and abs(face.normal.z)<.4:
                    area=sum((points[i]-points[0]).cross(points[i+1]-points[0]).length/2 for i in range(1,len(points)-1))
                    density=2.0 if ob.get('river_category')=='bridge' else 0
                    if rng.random()<min(.8,area*density):
                        center=sum(points,Vector())/len(points);normal=face.normal
                        horiz=normal.cross(Vector((0,0,1))).normalized()
                        radius=rng.uniform(.004,.014);center+=normal*.0012
                        vs=[ob.matrix_world@(center+horiz*a*radius+Vector((0,0,c*radius))) for a,c in ((-1,-1),(1,-1),(1,1),(-1,1))]
                        batch.geom(vs,[(0,1,2,3)],'maintenance',(.8,.83,.86,.65),uv=[(.002,.752),(.022,.752),(.022,.772),(.002,.772)])
        new=bpy.data.meshes.new(name+'__Aged');new.from_pydata(vertices,[],faces);new.update()
        for material in me.materials:new.materials.append(material)
        newuv=new.uv_layers.new(name='UVMap');newcol=new.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER')
        for face,(material,smooth) in zip(new.polygons,tags):
            face.material_index=material;face.use_smooth=smooth
        new['age_surface_cells']=True
        ob.data=new
        for i,(tex,col,norm) in enumerate(data):newuv.data[i].uv=tex;newcol.data[i].color=col
        new.normals_split_custom_set([tuple(v[2].normalized()) for v in data])
        mod=ob.modifiers.new('Aged surface triangles','TRIANGULATE');G.model.apply(ob)
        details[ob.get('river_category')]=batch
    for batch in details.values():
        if batch.v:batch.finish()


def forms(batch,ob,face,poly):
    """Panel joints and ties clipped to the actual support face, including holes."""
    from mathutils.geometry import closest_point_on_tri
    from weather import chart
    normal=face.normal;axis=0 if abs(normal.y)>.6 else 1
    if face.area<.15:return
    def put(part,color,uv=None):
        if len(part)<3:return
        vs=[ob.matrix_world@(v[0]+normal*.0015) for v in part]
        if sum((vs[k]-vs[0]).cross(vs[k+1]-vs[0]).length for k in range(1,len(vs)-1))<1e-10:return
        if uv is None:
            coords=[v[0] for v in part];lo=min(p[axis] for p in coords);hi=max(p[axis] for p in coords)
            bottom=min(p.z for p in coords);top=max(p.z for p in coords)
            uv=[(.502+.246*(p[axis]-lo)/max(.001,hi-lo),.502+.246*(p.z-bottom)/max(.001,top-bottom)) for p in coords]
        batch.geom(vs,[tuple(range(len(vs)))],'maintenance',color,uv=uv)
    for ax,step in ((axis,2.44),(2,1.22)):
        lo=min(v[0][ax] for v in poly);hi=max(v[0][ax] for v in poly)
        for k in range(math.ceil((lo+.01)/step),math.floor((hi-.01)/step)+1):
            line=clip(clip(poly,ax,k*step-.004,1),ax,k*step+.004,-1)
            put(line,(.34,.37,.40,.65))
    # A triangle owns a tie only if its center is inside, avoiding duplicate stamps.
    points=[v[0] for v in poly]
    if len(points)!=3:return
    for k in range(math.ceil(min(p[axis] for p in points)/1.22),math.floor(max(p[axis] for p in points)/1.22)+1):
        for j in range(math.ceil(min(p.z for p in points)/1.22),math.floor(max(p.z for p in points)/1.22)+1):
            center=points[0].copy();center[axis]=k*1.22+.30;center.z=j*1.22+.53
            other=1-axis;center[other]=points[0][other]-(normal[axis]*(center[axis]-points[0][axis])+normal.z*(center.z-points[0].z))/normal[other]
            if (closest_point_on_tri(center,*points)-center).length>.0001:continue
            horizontal=normal.cross(Vector((0,0,1))).normalized();center+=normal*.0018
            vs=[ob.matrix_world@(center+horizontal*a*.019+Vector((0,0,c*.019))) for a,c in ((-1,-1),(1,-1),(1,1),(-1,1))]
            batch.geom(vs,[(0,1,2,3)],'maintenance',uv=[(.002,.752),(.022,.752),(.022,.772),(.002,.772)])


def manufacture(batch,ob,face,poly):
    """A shallow pore/paste alpha tile, reusing the existing repair chart."""
    normal=face.normal;axis=0 if abs(normal.y)>.6 else 1
    if face.area<.10:return
    if ob.get('river_category')=='site' and face.area<2:return
    u0=min(v[0][axis] for v in poly);u1=max(v[0][axis] for v in poly)
    z0=min(v[0].z for v in poly);z1=max(v[0].z for v in poly)
    for i in range(math.floor(u0/2),math.floor(u1/2)+1):
        for j in range(math.floor(z0/1.22),math.floor(z1/1.22)+1):
            part=clip(clip(clip(clip(poly,axis,i*2,1),axis,(i+1)*2,-1),2,j*1.22,1),2,(j+1)*1.22,-1)
            if len(part)<3:continue
            vs=[ob.matrix_world@(v[0]+normal*.0007) for v in part]
            if sum((vs[k]-vs[0]).cross(vs[k+1]-vs[0]).length for k in range(1,len(vs)-1))<1e-10:continue
            uv=[(.502+.246*(v[0][axis]/2-i),.502+.246*(v[0].z/1.22-j)) for v in part]
            batch.geom(vs,[tuple(range(len(vs)))],'maintenance',(.80,.86,.94,.90),uv=uv)
