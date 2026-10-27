"""Independent raw GLB validation and measured shared-edge/construction checks.

Serialization, modular continuity and geometric construction have separate
reports. Repeating terrain UVs intentionally overlap in texture space; physical
triangle area, density and duplicate surfaces are checked instead of atlas packing.
"""
import argparse,hashlib,io,json,math,sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parent))
from kit.gltf import GLB
from kit.tiling import edge_error
from dimensions import *
from textures import RECTS


def raw(path):
    g=GLB(path);d=g.json;report={'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    assert len(d['materials'])==6,len(d['materials']);assert len(d['images'])==12,len(d['images'])
    assert all(s.get('wrapS',10497)==10497 and s.get('wrapT',10497)==10497 for s in d.get('samplers',[]))
    for m in d['materials']:
        p=m['pbrMetallicRoughness'];assert 'baseColorTexture' in p and 'metallicRoughnessTexture' in p
        assert 'normalTexture' in m and 'occlusionTexture' in m
        assert m['normalTexture'].get('scale',1)==1
        expected='MASK' if m['name']=='GroundFoliage' else 'BLEND' if m['name'].startswith('GroundTrim') else 'OPAQUE'
        assert m.get('alphaMode','OPAQUE')==expected
        if expected=='MASK':assert m.get('doubleSided') and abs(m.get('alphaCutoff',.5)-.30)<1e-5
        for key in ('baseColorTexture','metallicRoughnessTexture'):
            assert p[key].get('texCoord',0)==0
    textures=[]
    for i,im in enumerate(d['images']):
        data=g.image(i);img=Image.open(io.BytesIO(data));assert img.width==img.height and img.width<=2048 and img.width&(img.width-1)==0,img.size
        textures.append(dict(name=im.get('name'),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),size=img.size))
    tex_size=textures[0]['size'][0];assert all(t['size']==(tex_size,tex_size) for t in textures)
    report['images']=textures;report['materials']=len(d['materials']);report['triangles']=0
    densities={m['name']:[] for m in d['materials']};zero=[];inverted=[];normerr=0;colors=0
    for mesh in d['meshes']:
        for p in mesh['primitives']:
            pos=g.accessor(p['attributes']['POSITION']);n=g.accessor(p['attributes']['NORMAL']);uv=g.accessor(p['attributes']['TEXCOORD_0'])
            ix=g.accessor(p['indices']).reshape(-1,3);report['triangles']+=len(ix)
            assert np.isfinite(pos).all() and np.isfinite(n).all() and np.isfinite(uv).all()
            normerr=max(normerr,float(np.max(np.abs(np.linalg.norm(n,axis=1)-1))))
            tri=pos[ix];a=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
            ut=uv[ix];du=ut[:,1]-ut[:,0];dv=ut[:,2]-ut[:,0];ua=np.abs(du[:,0]*dv[:,1]-du[:,1]*dv[:,0])/2
            name=mesh['name'];mat=d['materials'][p['material']]['name']
            keys=[tuple(sorted(tuple(np.round(v,6)) for v in t)) for t in tri]
            assert len(keys)==len(set(keys)),('Duplicate geometric triangles',name)
            if np.any(a<1e-11):zero.append(name)
            if np.any(ua<1e-12):zero.append('UV '+name)
            if mat in ('GroundTrim','GroundFoliage','GroundIron'):
                author_uv=ut.copy();author_uv[:,:,1]=1-author_uv[:,:,1]
                assert author_uv.min()>=-1e-6 and author_uv.max()<=1+1e-6,('Atlas escaped',name)
                contained=np.zeros(len(ix),bool)
                for u0,v0,u1,v1 in RECTS.values():
                    contained|=((author_uv[:,:,0]>=u0-1e-6)&(author_uv[:,:,0]<=u1+1e-6)&(author_uv[:,:,1]>=v0-1e-6)&(author_uv[:,:,1]<=v1+1e-6)).all(axis=1)
                assert contained.all(),('Triangle crosses atlas regions',name)
            densities[mat].extend((np.sqrt(ua/np.maximum(a,1e-14))*tex_size).tolist())
            if 'COLOR_0' in p['attributes']:
                colors+=1;cc=g.accessor(p['attributes']['COLOR_0']);assert np.isfinite(cc).all() and cc[:,:3].min()>=0 and cc[:,:3].max()<=1.00001
            elif mat not in ('GroundTrim','GroundFoliage','GroundIron'):raise AssertionError('Lost vertex tint '+name)
            # glTF Y-up. Every terrain skin must face upward; normal-mapped trim may be a curb face.
            cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])
            if mat not in ('GroundTrim','GroundFoliage','GroundIron') and np.min(cross[:,1])< -1e-9:inverted.append(name)
    assert not zero,zero;assert not inverted,inverted;assert normerr<2e-5,normerr
    report.update(normal_length_error=normerr,color_primitives=colors,density_px_m={k:dict(zip(('p5','median','p95'),map(float,np.percentile(v,[5,50,95])))) for k,v in densities.items()})
    world_points=[]
    for ni,node in enumerate(d['nodes']):
        if 'mesh' not in node:continue
        matrix=g.world(ni)
        for primitive in d['meshes'][node['mesh']]['primitives']:
            pos=g.accessor(primitive['attributes']['POSITION']);w=(matrix@np.column_stack([pos,np.ones(len(pos))]).T).T[:,:3]
            world_points.extend(w[:,[0,2,1]]*np.array([1,-1,1]))
    world_points=np.array(world_points);lo=world_points.min(axis=0);hi=world_points.max(axis=0)
    report['world_bounds_blender_m']=dict(min=lo.tolist(),max=hi.tolist(),size=(hi-lo).tolist())
    for key,coverage in [('Asphalt',ASPHALT_TILE),('Concrete',CONCRETE_TILE),('Lawn',LAWN_TILE)]:
        stats=report['density_px_m'][key];target=tex_size/coverage
        if key=='Asphalt':assert target*.97<stats['p5']<=stats['median']<target*1.01
        else:assert stats['p5']>target*.5 and target*.9<stats['median']<target*1.25 and stats['p95']<target*1.6
    report['passed']=True;return report


def import_glb(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    bpy.context.view_layer.update()


def measurements_library(path):
    import_glb(path);result={}
    expected={'Road_Straight_A':(2*ASPHALT_HALF,LENGTH),'Road_Straight_B':(2*ASPHALT_HALF,LENGTH),'Road_Straight_C':(2*ASPHALT_HALF,LENGTH),'Road_Intersection':(2*CORE,2*CORE),'Curb_Straight':(GUTTER+CURB,BAY),'Curb_DrivewayCut':(GUTTER+CURB,LENGTH),'Curb_Ramp':(GUTTER+CURB,BAY),'Curb_StormInlet':(GUTTER+CURB,BAY),'Sidewalk_A':(PANEL,PANEL),'Sidewalk_B':(PANEL,PANEL),'Sidewalk_Ramp':(STRIP+PANEL,BAY),'Driveway_Apron':(STRIP,LENGTH),'Driveway_Slab':(BAY,BAY)}
    for rt in [ob for ob in bpy.context.scene.objects if ob.parent is None]:
        meshes=[ob for ob in rt.children_recursive if ob.type=='MESH'];count=0;points=[]
        for ob in meshes:
            ob.data.calc_loop_triangles();count+=len(ob.data.loop_triangles)
            points.extend([tuple(rt.matrix_world.inverted()@ob.matrix_world@v.co) for v in ob.data.vertices])
            assert max(abs(s-1) for s in ob.scale)<1e-6
        assert 0<count<=(3000 if rt.name in ('Manhole','Curb_StormInlet') else 2000),(rt.name,count)
        if rt.name in ('Manhole','Curb_StormInlet'):assert count>=500,(rt.name,count)
        pts=np.array(points);size=pts.max(axis=0)-pts.min(axis=0)
        if rt.name in expected:assert np.max(np.abs(size[:2]-expected[rt.name]))<3e-5,(rt.name,size,expected[rt.name])
        sockets={ob.name.split('__')[-1]:list(ob.location) for ob in rt.children if ob.type=='EMPTY'}
        result[rt.name]=dict(triangles=count,bounds_m=size.tolist(),sockets=sockets)
    ramp=bpy.data.objects['Sidewalk_Ramp'];ob=next(ob for ob in ramp.children if ob.type=='MESH' and ob.name.startswith('Ramp_and'))
    valid={i for p in ob.data.polygons if ob.data.materials[p.material_index].name=='Concrete' for i in p.vertices}
    pts=np.array([ob.data.vertices[i].co[:] for i in sorted(valid)]);base=pts[np.abs(pts[:,0])<1e-5];top=pts[np.abs(pts[:,0]-STRIP)<1e-5]
    # Center ramp edge vertices are the actual mesh, not declared slope constants.
    low=base[np.abs(base[:,1])<PANEL/2+.0001,2].mean();high=top[np.abs(top[:,1])<PANEL/2+.0001,2].mean()
    measured=float((high-low)/STRIP);assert measured<=1/12+1e-5
    slopes=[]
    for poly in ob.data.polygons:
        pp=np.array([ob.data.vertices[i].co[:] for i in poly.vertices])
        if ob.data.materials[poly.material_index].name!='Concrete' or pp[:,0].max()>STRIP+1e-6 or np.abs(pp[:,1]).max()>PANEL/2+1e-6:continue
        d=pp[1:3]-pp[0]
        gradient=np.linalg.solve(d[:,:2],d[:,2]);slopes.append(abs(float(gradient[0])))
    assert max(slopes)<=1/12+1e-5
    result['construction']=dict(ramp_running_slope=measured,ramp_max_triangle_slope=max(slopes),landing_clear_width_m=float(pts[:,0].max()-STRIP),scope='actual imported surface vertices; not drainage or legal certification')
    # New service castings: measure actual imported skins and ray-hit the
    # throat rather than restating nominal dimensions from the source script.
    from mathutils.bvhtree import BVHTree
    def local_points(rt,ob):return [rt.matrix_world.inverted()@ob.matrix_world@v.co for v in ob.data.vertices]
    inlet=bpy.data.objects['Curb_StormInlet'];grate=next(o for o in inlet.children_recursive if o.type=='MESH' and o.name.startswith('Inlet_grate_casting'))
    body=next(o for o in inlet.children if o.type=='MESH');pp=local_points(inlet,body);body.data.calc_loop_triangles()
    tree=BVHTree.FromPolygons(pp,[tuple(t.vertices) for t in body.data.loop_triangles],all_triangles=True)
    gp=np.array(local_points(inlet,grate));top=float(gp[:,2].max())
    cap,_,_,_=tree.ray_cast(Vector((.015,0,.05)),Vector((0,0,1)))
    left,_,_,_=tree.ray_cast(Vector((.071,0,.05)),Vector((0,-1,0)))
    right,_,_,_=tree.ray_cast(Vector((.071,0,.05)),Vector((0,1,0)))
    assert cap is not None and left is not None and right is not None
    chamber_ends=[]
    for sign in (-1,1):
        end,_,_,_=tree.ray_cast(Vector((-.20,0,-.12)),Vector((0,sign,0)))
        assert end is not None and abs(end.y-sign*.45)<3e-5
        chamber_ends.append(float(end.y))
    width=float((right-left).length);height=float(cap.z-top)
    assert .79<width<.81 and .094<height<.097 and -.028<top<-.020
    # Grate and hood have disjoint X extents. This clearance is invariant
    # throughout a straight vertical service lift, rather than a sampled pose.
    box_min=min(p.x for p in pp if p.z>.04 and p.x>-.011)
    lift_gap=float(box_min-gp[:,0].max());assert lift_gap>.009
    end_gap=min(gp[:,1].min()-chamber_ends[0],chamber_ends[1]-gp[:,1].max())
    assert end_gap>.0049
    front,_,_,_=tree.ray_cast(Vector((-.2,0,-.12)),Vector((-1,0,0)))
    assert front is not None
    front_gap=float(gp[:,0].min()-front.x);assert front_gap>.0049
    grate.data.calc_loop_triangles()
    gt=BVHTree.FromPolygons([Vector(p) for p in gp],[tuple(t.vertices) for t in grate.data.loop_triangles],all_triangles=True)
    grate_seat_gaps=[]
    for x in (-.394,-.031):
        support,_,_,_=tree.ray_cast(Vector((x,0,-.03)),Vector((0,0,-1)))
        underside,_,_,_=gt.ray_cast(Vector((x,0,-.10)),Vector((0,0,1)))
        assert support is not None and underside is not None
        grate_seat_gaps.append(float((support-underside).length))
    assert max(grate_seat_gaps)<5e-5
    # Compare actual imported curb faces, independently of source parameters.
    straight=bpy.data.objects['Curb_Straight'];so=next(o for o in straight.children if o.type=='MESH')
    so.data.calc_loop_triangles()
    st=BVHTree.FromPolygons(local_points(straight,so),[tuple(t.vertices) for t in so.data.loop_triangles],all_triangles=True)
    profile_errors=[]
    for level in (.08,.10,.125):
        p,_,_,_=tree.ray_cast(Vector((-.10,0,level)),Vector((1,0,0)))
        q,_,_,_=st.ray_cast(Vector((-.10,.25,level)),Vector((1,0,0)))
        assert p is not None and q is not None
        profile_errors.append(abs(float(p.x-q.x)))
    assert max(profile_errors)<5e-5,profile_errors
    iron_ids={i for poly in body.data.polygons if body.data.materials[poly.material_index].name=='GroundIron' for i in poly.vertices}
    cap_top=max(pp[i].z for i in iron_ids);cap_back=max(pp[i].x for i in iron_ids)
    assert abs(cap_top-CURB_HEIGHT)<5e-5 and abs(cap_back-CURB)<5e-5
    # Scan actual open intervals through the 35 mm casting, then ray to each
    # slot wall. These dimensions prove construction, not just serialization.
    widths=[];bar_widths=[];last=None
    for y in np.linspace(-.419,.419,1801):
        hit,_,_,_=gt.ray_cast(Vector((-.2125,float(y),-.04)),Vector((0,0,1)))
        if hit is not None:continue
        a,_,_,_=gt.ray_cast(Vector((-.2125,float(y),-.04)),Vector((0,-1,0)))
        c,_,_,_=gt.ray_cast(Vector((-.2125,float(y),-.04)),Vector((0,1,0)))
        if a is not None and c is not None and (last is None or abs(float(a.y)-last)>.001):
            widths.append(float(c.y-a.y))
            if last is not None:bar_widths.append(float(a.y-prev_end))
            last=float(a.y);prev_end=float(c.y)
    assert len(widths)==25 and max(widths)<.0127 and min(widths)>.009, widths
    assert min(bar_widths)>.0249 and max(bar_widths)<.0251,bar_widths
    result['construction'].update(inlet_curb_profile_error_m=profile_errors,inlet_cap_top_m=float(cap_top),
        inlet_cap_back_m=float(cap_back),inlet_slot_widths_m=widths,inlet_bar_widths_m=bar_widths)
    cover_root=bpy.data.objects['Manhole'];cover=next(o for o in cover_root.children_recursive if o.type=='MESH' and o.name.startswith('Manhole_Cover'))
    cp=np.array(local_points(cover_root,cover));diameter=float(cp[:,0].max()-cp[:,0].min());assert abs(diameter-MANHOLE_COVER)<3e-5
    frame=next(o for o in cover_root.children_recursive if o.type=='MESH' and o!=cover)
    ids={i for p in frame.data.polygons if frame.data.materials[p.material_index].name=='GroundIron' for i in p.vertices}
    fp=local_points(cover_root,frame);inner=min(math.hypot(fp[i].x,fp[i].y) for i in ids if fp[i].z>-.020)
    radial_gap=inner-float(np.linalg.norm(cp[:,:2],axis=1).max());assert radial_gap>.0014
    frame.data.calc_loop_triangles();cover.data.calc_loop_triangles()
    ft=BVHTree.FromPolygons(fp,[tuple(t.vertices) for t in frame.data.loop_triangles if frame.data.materials[t.material_index].name=='GroundIron'],all_triangles=True)
    ct=BVHTree.FromPolygons([Vector(p) for p in cp],[tuple(t.vertices) for t in cover.data.loop_triangles],all_triangles=True)
    seat,_,_,_=ft.ray_cast(Vector((.298,0,.02)),Vector((0,0,-1)))
    bottom,_,_,_=ct.ray_cast(Vector((.298,0,-.10)),Vector((0,0,1)))
    assert seat is not None and bottom is not None
    seat_gap=float((seat-bottom).length);assert seat_gap<5e-5
    result['construction'].update(inlet_grate_top_m=top,inlet_clear_throat_width_m=width,inlet_clear_throat_height_m=height,
        grate_vertical_lift_xy_clearance_m=lift_gap,grate_vertical_lift_end_clearance_m=float(end_gap),grate_vertical_lift_front_clearance_m=front_gap,grate_seat_gaps_m=grate_seat_gaps,inlet_chamber_end_hits_m=chamber_ends,cover_diameter_m=diameter,cover_vertical_lift_radial_clearance_m=radial_gap,cover_seat_gap_m=seat_gap,
        casting_scope='Fresh-import vertices and ray-hit hood/cheeks. Lift clearances use disjoint actual XY bounds; no gravity/drainage simulation.')
    return result


def edge_segments(root,axis,coordinate,restrict=None,all_materials=False):
    rows=[]
    for ob in [root]+list(root.children_recursive):
        if ob.type!='MESH' or ob.get('surface_kind')=='GroundTrim':continue
        me=ob.data;uv=me.uv_layers.active;normal_matrix=ob.matrix_world.to_3x3().inverted().transposed()
        loop_normals=me.corner_normals
        for poly in me.polygons:
            if not all_materials and ob.data.materials[poly.material_index].name not in ('Asphalt','Concrete','Lawn'):continue
            lis=list(poly.loop_indices)
            for li,lj in zip(lis,lis[1:]+lis[:1]):
                vs=[]
                for k in (li,lj):
                    loop=me.loops[k];p=ob.matrix_world@me.vertices[loop.vertex_index].co
                    n=(normal_matrix@loop_normals[k].vector).normalized()
                    vs.append(np.array([*p,*n,*uv.data[k].uv]))
                a,b=vs
                if abs(a[axis]-coordinate)>3e-5 or abs(b[axis]-coordinate)>3e-5 or np.linalg.norm(a[:3]-b[:3])<1e-7:continue
                if restrict and not (restrict(a[:3]) and restrict(b[:3])):continue
                rows.append((a,b))
    if not rows:raise AssertionError('Missing boundary '+root.name+' '+str(coordinate))
    return rows


def compare_edges(a,b):
    samples=[]
    for x,y in a:
        for t in np.linspace(0,1,9):
            p=x*(1-t)+y*t;matches=[]
            for u,v in b:
                d=v[:3]-u[:3];f=np.clip(np.dot(p[:3]-u[:3],d)/np.dot(d,d),0,1);q=u*(1-f)+v*f
                matches.append((np.linalg.norm(p[:3]-q[:3]),q))
            _,q=min(matches,key=lambda r:r[0]);p[3:6]/=np.linalg.norm(p[3:6]);q[3:6]/=np.linalg.norm(q[3:6]);samples.append((p,q))
    return edge_error([x for x,y in samples],[y for x,y in samples],tolerance=5e-5,normal_tolerance=.002)


def continuity(path):
    import_glb(path);obs=bpy.context.scene.objects;tests={};groups={}
    for rt in [ob for ob in obs if ob.parent is None]:
        module=rt.get('module','');category=module.split('_')[0]
        if category not in ('Road','Curb','Sidewalk','Lawn'):continue
        for port in rt.children:
            side=port.name.split('__')[-1]
            if port.type!='EMPTY' or side not in ('N','S','E','W'):continue
            position=np.array(port.matrix_world.translation)
            key=(category,*np.round(position/2e-5).astype(int))
            direction=rt.matrix_world.to_3x3()@Vector((0,1,0) if side in ('N','S') else (1,0,0))
            axis=int(np.argmax(np.abs(direction)))
            groups.setdefault(key,[]).append((rt,port,axis,float(position[axis])))
    for key,pair in groups.items():
        if len(pair)==1:continue # exposed end, a future extension point
        assert len(pair)==2,('Ambiguous duplicate snap',key,[p[0].name for p in pair])
        (aa,pa,axis,at),(bb,pb,axis2,at2)=pair;assert axis==axis2
        a=edge_segments(aa,axis,at);b=edge_segments(bb,axis,at)
        other=1-axis
        alo=min(min(x[other],y[other]) for x,y in a);ahi=max(max(x[other],y[other]) for x,y in a)
        blo=min(min(x[other],y[other]) for x,y in b);bhi=max(max(x[other],y[other]) for x,y in b)
        lo,hi=max(alo,blo),min(ahi,bhi);assert hi-lo>1e-4
        if key[0]=='Lawn':
            # Yard corners join part of a longer rectangular edge. Clip that
            # shared interval before using the unchanged seam measurement.
            def clip(rows):
                out=[]
                for x,y in rows:
                    d=y[other]-x[other]
                    if abs(d)<1e-8:continue
                    t0,t1=sorted(((lo-x[other])/d,(hi-x[other])/d));t0=max(0,t0);t1=min(1,t1)
                    if t1-t0>1e-7:out.append((x+(y-x)*t0,x+(y-x)*t1))
                return out
            a,b=clip(a),clip(b)
        else:
            a=[(x,y) for x,y in a if min(x[other],y[other])>=lo-3e-5 and max(x[other],y[other])<=hi+3e-5]
            b=[(x,y) for x,y in b if min(x[other],y[other])>=lo-3e-5 and max(x[other],y[other])<=hi+3e-5]
        name=aa.name+' / '+bb.name
        assert a and b,('No shared interval',name,lo,hi)
        tests[name]=compare_edges(a,b)
        tests[name]['socket_error_m']=float((pa.matrix_world.translation-pb.matrix_world.translation).length)
    # Internal boundaries between intersection wedges and arms also need actual
    # crown-height continuity, independently of the serialized root envelope.
    for k in range(4):
        theta=k*math.pi/2;cs,sn=round(math.cos(theta)),round(math.sin(theta))
        axis=0 if k%2==0 else 1;sign=1 if k in (0,1) else -1
        aa=obs[f'Junction__Intersection_wedge_{k}'];bb=obs[f'Junction__Intersection_arm_{k}']
        a=edge_segments(aa,axis,sign*ASPHALT_HALF);b=edge_segments(bb,axis,sign*ASPHALT_HALF,
            lambda p:ASPHALT_HALF-2e-5<= (p[1] if k==0 else -p[0] if k==1 else -p[1] if k==2 else p[0]) <=CORE+2e-5)
        tests[f'junction_internal_{k}']=compare_edges(a,b)
    def contact(name,a,b,uv=False):
        out=compare_edges(a,b)
        out['normal_policy']='measured, intentional construction grade break'
        out['uv_policy']='shared concrete phase' if uv else 'different material sets'
        out['passed']=out['position_m']<5e-5 and (not uv or out['uv_delta']<5e-5)
        tests[name]=out
    for arm in range(4):
        for side in (-1,1):
            rt=obs[f'Arm{arm}_Curb{side}_0_0'];walk=obs[f'Arm{arm}_Ramp{side}']
            p=rt.matrix_world@Vector((CURB,0,0));axis=0 if arm%2==0 else 1
            contact(f'curb_ramp_run_{arm}_{side}',edge_segments(rt,axis,p[axis]),edge_segments(walk,axis,p[axis]),uv=True)
            count=6 if arm in (0,2) else 3
            for i in range(count):
                road=obs[f'Arm{arm}_Road{i}']
                for j in range(2):
                    name=f'Arm{arm}_Curb{side}_{i}_{j}'
                    if name not in obs:continue
                    curb=obs[name];p=curb.matrix_world@Vector((-GUTTER,0,0));other=1-axis
                    a=edge_segments(curb,axis,p[axis],all_materials=True)
                    lo=min(min(x[other],y[other]) for x,y in a);hi=max(max(x[other],y[other]) for x,y in a)
                    b=edge_segments(road,axis,p[axis],restrict=lambda v:lo-3e-5<=v[other]<=hi+3e-5)
                    contact('road_pan_'+name,a,b)
    def at_edge_z(rt):
        rows=[]
        for ob in [rt]+list(rt.children_recursive):
            if ob.type!='MESH':continue
            me=ob.data;uv=me.uv_layers.active
            for poly in me.polygons:
                lis=list(poly.loop_indices)
                for li,lj in zip(lis,lis[1:]+lis[:1]):
                    pair=[]
                    for k in (li,lj):
                        p=ob.matrix_world@me.vertices[me.loops[k].vertex_index].co
                        pair.append(np.array([*p,0,0,1,*uv.data[k].uv]))
                    if all(abs(v[2]-ROAD_EDGE)<1e-6 for v in pair):rows.append(pair)
        assert rows
        return rows
    for k in range(4):
        contact(f'corner_pan_{k}',at_edge_z(obs[f'Corner_{k}']),at_edge_z(obs[f'Junction__Intersection_wedge_{k}']))
    for arm,side in ((0,1),(2,-1)):
        curb=obs[f'Arm{arm}_Curb{side}_2_0'];apron=obs[f'Arm{arm}_Drive_apron']
        p=curb.matrix_world@Vector((CURB,0,0))
        contact(f'drive_apron_curb_{arm}',edge_segments(curb,0,p.x),edge_segments(apron,0,p.x),uv=True)
    assert len(tests)>150,len(tests)
    return tests


def decal_support(path):
    from mathutils.bvhtree import BVHTree
    import_glb(path);base_verts=[];base_faces=[];cards=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();uv=ob.data.uv_layers.active
        for tri in ob.data.loop_triangles:
            poly=ob.data.polygons[tri.polygon_index];mat=ob.data.materials[poly.material_index].name
            points=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
            coords=[uv.data[i].uv for i in tri.loops]
            if mat in ('GroundFoliage','GroundIron'):continue
            joint=mat.startswith('GroundTrim') and all(.625-1e-6<=v.x<=.75+1e-6 and 0<=v.y<=.25 for v in coords)
            # New structural iron and upright organic cards use the shared
            # trim atlas, but are not paving overlays. Preserve the existing
            # narrow clearance policy for every actual paint/weather decal.
            structural=False
            if mat.startswith('GroundTrim'):
                for region in ('iron','manhole','foundry','grass'):
                    u0,v0,u1,v1=RECTS[region]
                    if all(u0-1e-6<=v.x<=u1+1e-6 and v0-1e-6<=v.y<=v1+1e-6 for v in coords):structural=True
            if structural:continue
            if mat in ('Asphalt','Concrete','Lawn') or joint:
                index=len(base_verts);base_verts.extend(points);base_faces.append((index,index+1,index+2))
            else:cards.append(points)
    bvh=BVHTree.FromPolygons(base_verts,base_faces,all_triangles=True)
    distances=[];signed=[];bad=[]
    for tri in cards:
        for p in [tri[0]*(i/4)+tri[1]*(j/4)+tri[2]*(1-(i+j)/4) for i in range(5) for j in range(5-i)]+[sum(tri,Vector())/3]:
            hit,normal,_,distance=bvh.find_nearest(p)
            if hit is None:raise AssertionError('Unsupported decal')
            distances.append(distance);signed.append(float((p-hit).dot(normal)))
            if distance<.00025 or signed[-1]<-.00005 or distance>.0125:bad.append(dict(point=list(p),nearest=list(hit),distance=distance,signed=signed[-1]))
    report=dict(triangles=len(cards),samples=len(distances),min_distance_m=min(distances),max_distance_m=max(distances),min_signed_distance_m=min(signed),sampling='15 barycentric grid points plus centroid per non-joint trim triangle; closest actual imported skin triangle')
    Path('build/decal-support-diagnostics.json').write_text(json.dumps(bad[:40],indent=2))
    assert min(distances)>.00025 and min(signed)>-.00005 and max(distances)<.0125,report
    report['passed']=True;return report


def main():
    p=argparse.ArgumentParser();p.add_argument('--library',type=Path,required=True);p.add_argument('--assembly',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    report=dict(library=raw(a.library),assembly=raw(a.assembly))
    assert np.max(np.abs(np.array(report['assembly']['world_bounds_blender_m']['size'])[:2]-[2*(CORE+3*LENGTH),2*(CORE+6*LENGTH)]))<1e-4
    # Exact shared image bytes across the two GLBs prevent accidental duplicate texture families.
    assert sorted(x['sha256'] for x in report['library']['images'])==sorted(x['sha256'] for x in report['assembly']['images'])
    report['modules']=measurements_library(a.library)
    Path('build/delivery-check.json').write_text(json.dumps(report,indent=2))
    tests=continuity(a.assembly);passed=all(v['passed'] for v in tests.values());Path('build/seam-check.json').write_text(json.dumps(dict(passed=passed,tests=tests),indent=2))
    assert passed,{k:v for k,v in tests.items() if not v['passed']}
    support=decal_support(a.assembly);Path('build/decal-support.json').write_text(json.dumps(support,indent=2))
    print('PASS raw GLB, reimport, module budgets, physical ramp; PASS',len(tests),'shared-edge position/normal/UV tests')

if __name__=='__main__':main()
