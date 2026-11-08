"""Independent exported surfaces; deliberately not a final look-dev certificate."""
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit import motion
import geometry as G
from plan import FLOOR,SPAN,AISLE,DEPTH,STALL,ramp_fraction


def tree(objects,select=lambda m:True,up_only=False):
    vs=[];fs=[]
    for o in objects:
        if o.type!='MESH':continue
        o.data.calc_loop_triangles();offset=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices)
        for t in o.data.loop_triangles:
            m=o.data.materials[t.material_index]
            if select(m) and (not up_only or (o.matrix_world.to_3x3()@t.normal).z>.7):fs.append(tuple(offset+i for i in t.vertices))
    return BVHTree.FromPolygons(vs,fs,all_triangles=True)


def floor_planes(objects):
    triangles=[]
    for o in objects:
        o.data.calc_loop_triangles()
        for t in o.data.loop_triangles:
            name=o.data.materials[t.material_index].name
            if ('form Deck' in name or 'form Seal' in name or name.split('.')[0]=='Concrete') and (o.matrix_world.to_3x3()@t.normal).z>.7:
                triangles.append([tuple(o.matrix_world@o.data.vertices[i].co) for i in t.vertices])
    return np.asarray(triangles,dtype=np.float64)


def measured_height(triangles,point):
    """Direct imported triangle planes, independent of source BVH projection."""
    x,y,z=point;xy=np.array([x,y])
    keep=np.all(triangles[:,:,:2].min(axis=1)<=xy+.00001,axis=1)&np.all(triangles[:,:,:2].max(axis=1)>=xy-.00001,axis=1)
    t=triangles[keep]
    if not len(t):return None
    a=t[:,0];u=t[:,1]-a;v=t[:,2]-a;q=xy-a[:,:2];det=u[:,0]*v[:,1]-u[:,1]*v[:,0]
    alpha=(q[:,0]*v[:,1]-q[:,1]*v[:,0])/det;beta=(u[:,0]*q[:,1]-u[:,1]*q[:,0])/det
    height=a[:,2]+alpha*u[:,2]+beta*v[:,2]
    valid=(alpha>=-1e-6)&(beta>=-1e-6)&(alpha+beta<=1+1e-6)&(height<=z+.15)&(height>=z-.15)
    return float(height[valid].max()) if valid.any() else None


def main():
    data=json.loads(Path('build/manifest.json').read_text());results=[]
    for p in data['garages']:
        seed=p['seed'];bpy.ops.wm.read_factory_settings(use_empty=True);path=Path(f'export/ParkingGarage-{seed}.gltf')
        doc=json.loads(path.read_text());bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        obs=list(bpy.context.scene.objects);meshes=[o for o in obs if o.type=='MESH'];triangles=G.triangles(meshes)
        assert triangles==p['garage_triangles'],(seed,triangles,p['garage_triangles']);assert triangles<300000
        bb=G.bounds(meshes);assert max(abs(bb[i][j]-p['bounds_m'][i][j]) for i in range(2) for j in range(3))<.0001
        normal_error=0.;collapsed=0;uv_area=0;area=0
        for o in meshes:
            me=o.data;me.calc_loop_triangles();assert me.uv_layers,o.name
            assert max(abs(s-1) for s in o.scale)<1e-5,(o.name,list(o.scale))
            for n in me.corner_normals:normal_error=max(normal_error,abs(n.vector.length-1))
            for t in me.loop_triangles:
                uv=[Vector(me.uv_layers.active.data[i].uv) for i in t.loops]
                ua=abs((uv[1]-uv[0]).cross(uv[2]-uv[0]))/2
                if ua<1e-12 and t.area>1e-9:collapsed+=1
                uv_area+=ua;area+=t.area
        assert normal_error<.0001,normal_error
        assert collapsed==0,collapsed
        # Actual floor polygons only: ray measurements are independent of
        # the plan values, unlike the separate round-trip comparisons above.
        planes=floor_planes(meshes)
        solids=tree(meshes,lambda m:not any(s in m.name.lower() for s in ('glass','groundparking','fluorescent')))
        gaps=[];support=[];path_errors=[];support_rows=[]
        for row in p['paths']+p['pedestrian_paths']:
            for pt in row['points']:
                x,y,z=pt;height=measured_height(planes,pt)
                if height is None:path_errors.append(dict(path=row['name'],point=pt,error='no imported floor triangle under XY within 150mm'))
                else:
                    error=abs(height-z);support.append(error);support_rows.append(dict(path=row['name'],point=pt,hit=[x,y,height],error_m=error))
        # Include actual downward-face section midpoints, so a regular grid
        # cannot step between every narrow tee stem or hanging fixture.
        aisle_x=set(float(x) for x in np.linspace(-p['length']/2+1,p['length']/2-1,31))
        for ob in meshes:
            for t in ob.data.loop_triangles:
                if (ob.matrix_world.to_3x3()@t.normal).z>-.5:continue
                points=[ob.matrix_world@ob.data.vertices[i].co for i in t.vertices];cut=[]
                for a,b in zip(points,points[1:]+points[:1]):
                    if abs(a.y-p['flat_y'])<1e-6:cut.append(a.x)
                    if (a.y-p['flat_y'])*(b.y-p['flat_y'])<0:
                        cut.append(a.x+(b.x-a.x)*(p['flat_y']-a.y)/(b.y-a.y))
                if len(cut)>=2:
                    x=(min(cut)+max(cut))/2
                    # Keep the original 1m terminal setbacks: the end guard's
                    # top is a downward-section candidate at the next level,
                    # but its solid footprint is outside the driving aisle.
                    if -p['length']/2+1<x<p['length']/2-1:aisle_x.add(round(x,6))
        # Actual floor/soffit samples at every occupied covered floor. This is
        # an aisle section check, not a global continuous headroom proof.
        for level in range(p['levels']-1):
            for x in sorted(aisle_x):
                y=p['flat_y'];floor_z=measured_height(planes,(float(x),y,level*FLOOR+.05))
                assert floor_z is not None,(seed,x,y)
                h=solids.ray_cast(Vector((float(x),y,floor_z+.18)),Vector((0,0,1)),FLOOR+1)
                if h[0] is not None:gaps.append(h[0].z-floor_z)
        assert not path_errors,path_errors[:6]
        assert not p['route_surface_projection']['unsupported_samples'],p['route_surface_projection']['unsupported_samples'][:6]
        Path(f'build/path-support-{seed}.json').write_text(json.dumps(sorted(support_rows,key=lambda r:r['error_m'],reverse=True),indent=2)+'\n')
        assert max(support)<.0002,(max(support),support_rows[support.index(max(support))])
        assert min(gaps)>=2.1336,(seed,min(gaps))
        stop_contacts=[]
        for ob in meshes:
            if not ob.name.startswith('Stop_'):continue
            for v in ob.data.vertices:
                if abs(v.co.z)>.00001:continue
                pt=ob.matrix_world@v.co;height=measured_height(planes,pt)
                assert height is not None,(seed,'wheel-stop floor',ob.name,list(pt))
                gap=pt.z-height;stop_contacts.append(gap)
        assert stop_contacts and max(stop_contacts)<.0002 and min(stop_contacts)>-.0035,(seed,min(stop_contacts),max(stop_contacts))
        apertures={}
        facade_solids=tree(meshes)
        for side in (-1,1):
            clear=total=0
            # Intermediate occupied cells only, avoiding the open roof above
            # the uppermost rear ramp. This is an aperture sample, not a code
            # area takeoff or a fire/ventilation engineering certification.
            for level in range(p['levels']-(1 if side==-1 else 2)):
                for x in np.linspace(-p['length']/2+.25,p['length']/2-.25,161):
                    rise=FLOOR*ramp_fraction(float(x),p) if side==1 else 0
                    for dz in np.linspace(.05,FLOOR-.05,27):
                        hit=facade_solids.ray_cast(Vector((float(x),side*(p['width']/2+.5),level*FLOOR+rise+float(dz))),Vector((0,-side,0)),1.0)
                        total+=1;clear+=hit[0] is None
            apertures['front' if side==-1 else 'rear']=dict(open_samples=clear,total_samples=total,open_fraction=clear/total)
            assert clear/total>.20,(seed,side,clear/total)
        bearings=[]
        if p['system']=='precast':
            girders=tree([o for o in meshes if o.name.startswith('Girder_')])
            for ob in meshes:
                if 'DoubleTee__Mesh' not in ob.name:continue
                cy=ob.parent.matrix_world.translation.y
                for poly in ob.data.polygons:
                    if 'form Seal' not in ob.data.materials[poly.material_index].name:continue
                    normal=ob.matrix_world.to_3x3()@poly.normal
                    center=ob.matrix_world@(sum((ob.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices))
                    if normal.z>-.98 or abs(center.y-cy)<8:continue
                    hit=girders.ray_cast(center+Vector((0,0,.025)),Vector((0,0,-1)),.05)
                    assert hit[0] is not None,('Unsupported tee bearing',ob.name,list(center))
                    bearings.append(abs(hit[0].z-center.z))
            assert bearings and max(bearings)<.001,(len(bearings),max(bearings,default=0))
        # Count geometry + route reservations: accessible rectangles cannot
        # overlap normal stalls after replacing a block of the row.
        overlaps=[];stalls=p['stalls']
        for i,a in enumerate(stalls):
            for b in stalls[i+1:]:
                if a['level']!=b['level'] or a['ramp']!=b['ramp']:continue
                ox=min(a['x']+a['width']/2,b['x']+b['width']/2)-max(a['x']-a['width']/2,b['x']-b['width']/2)
                oy=(a['depth']+b['depth'])/2-abs(a['y']-b['y'])
                if ox>1e-5 and oy>1e-5:overlaps.append([a['id'],b['id'],ox,oy])
        assert not overlaps,overlaps[:5]
        accessible=[s for s in stalls if s['accessible']];vans=[s for s in accessible if s.get('van')]
        needed=next(n for limit,n in ((25,1),(50,2),(75,3),(100,4),(150,5),(200,6),(300,7),(400,8),(500,9)) if len(stalls)<=limit)
        assert len(accessible)>=needed;assert len(vans)>=math.ceil(len(accessible)/6)
        sign_heights=[]
        for ob in meshes:
            if not ob.name.startswith('Accessible sign '):continue
            blue=[ob.matrix_world@ob.data.vertices[i].co for poly in ob.data.polygons if 'form Blue' in ob.data.materials[poly.material_index].name for i in poly.vertices]
            bottom=min(blue,key=lambda v:v.z);grade=measured_height(planes,(bottom.x,bottom.y,0))
            assert grade is not None
            sign_heights.append(bottom.z-grade)
        assert len(sign_heights)==len(accessible) and min(sign_heights)>=1.524,(seed,sign_heights)
        # Actual full-height space at the van reservations and their ground
        # entrance/exit centerlines. Gate leaves are opened for vehicle access;
        # the declared moving-range sweep verifies that mechanism separately.
        vehicle_solids=tree([o for o in meshes if '__Gate__Arm' not in o.name],lambda m:not any(s in m.name.lower() for s in ('glass','groundparking','fluorescent')))
        van_gaps=[]
        column_surfaces=[]
        for ob in meshes:
            if not ob.name.startswith('ColumnShaft_'):continue
            vertices=[ob.matrix_world@v.co for v in ob.data.vertices]
            lo=[min(v[k] for v in vertices) for k in range(3)];hi=[max(v[k] for v in vertices) for k in range(3)]
            column_surfaces.append((ob.name,lo,hi,tree([ob])))
        samples=[]
        for row in p['paths']:
            if row['name'] not in ('Drive_Entry_to_L1','Drive_L1_to_Exit'):continue
            for aa,bb in zip(row['points'],row['points'][1:]):
                start,end=Vector(aa),Vector(bb);delta=end-start
                if delta.xy.length<1e-6:continue
                normal=Vector((-delta.y,delta.x,0)).normalized()
                for j in range(max(1,math.ceil(delta.length/.25))+1):
                    pt=start.lerp(end,j/max(1,math.ceil(delta.length/.25)))
                    samples.extend(list(pt+normal*offset) for offset in (-1.2,0,1.2))
        for s in vans:
            samples.extend([s['x']+dx,s['y']+dy,s['z']] for dx in (-s['width']/2+.25,0,s['width']/2-.25) for dy in (-s['depth']/2+.5,0,s['depth']/2-.5))
        for x,y,z in samples:
            floor_z=measured_height(planes,(x,y,z))
            assert floor_z is not None,(seed,'van floor',x,y,z)
            body_point=Vector((x,y,floor_z+.6))
            for name,lo,hi,column in column_surfaces:
                if all(lo[k]<body_point[k]<hi[k] for k in range(3)):
                    assert not motion.inside(column,body_point),(seed,'Vehicle route inside actual column',name,list(body_point))
            h=vehicle_solids.ray_cast(Vector((x,y,floor_z+.18)),Vector((0,0,1)),FLOOR+1)
            if h[0] is not None:van_gaps.append(h[0].z-floor_z)
        assert min(van_gaps)>=2.4892-.0001,(seed,'van clearance',min(van_gaps))
        sockets=[o for o in obs if o.get('socket_kind')=='parked_car'];assert len(sockets)==len(stalls)
        # Actual entry bar geometry: lowest yellow gantry face over drive lane.
        gantry=next(o for o in meshes if o.name.startswith('Entry gantry'))
        yellow=[o.matrix_world@o.data.vertices[i].co for o in [gantry] for poly in o.data.polygons if 'Yellow' in o.data.materials[poly.material_index].name for i in poly.vertices]
        bar_bottom=min(v.z for v in yellow);bar_center=sum(yellow,Vector())/len(yellow)
        grade=measured_height(planes,(bar_center.x,bar_center.y,0))
        assert grade is not None
        bar_clearance=bar_bottom-grade;assert abs(bar_clearance-2.4892)<.0001,bar_clearance
        moving_nodes=[o for o in obs if o.get('pivot_axis') or o.get('slide_axis')]
        images=[]
        for im in doc.get('images',[]):
            f=(path.parent/im['uri']).resolve();assert f.exists();images.append(dict(uri=im['uri'],bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
        results.append(dict(seed=seed,triangles=triangles,bounds_m=bb,materials=len(doc['materials']),image_resources=images,
            normal_unit_error=normal_error,collapsed_uv_triangles=collapsed,uv_policy='Intentional shared/tiled chart reuse; no unique lightmap UV claim',
            measured_uv_area=uv_area,measured_surface_area_m2=area,measured_aisle_clearance_min_m=min(gaps),
            aisle_clearance_samples=len(gaps),aisle_sample_basis='31 regular stations plus actual downward triangle section midpoints, at each covered flat-aisle level; 1m terminal guard-wall setbacks',
            measured_path_to_floor_max_m=max(support),path_samples=len(support),entry_bar_measured_m=bar_clearance,entry_bar_world_bottom_m=bar_bottom,
            measured_van_route_clearance_min_m=min(van_gaps),van_clearance_samples=len(samples),
            tee_bearing_face_samples=len(bearings),measured_tee_pad_to_girder_max_gap_m=max(bearings,default=None),
            wheel_stop_bottom_vertex_samples=len(stop_contacts),measured_wheel_stop_gap_range_m=[min(stop_contacts),max(stop_contacts)],
            measured_intermediate_facade_aperture_samples=apertures,
            stall_sockets=len(sockets),accessible=len(accessible),vans=len(vans),moving_nodes=len(moving_nodes),
            measured_accessible_sign_bottom_min_m=min(sign_heights),
            serialization='triangle/bounds/socket roundtrip',construction='independent imported floor triangle planes, upward soffit rays, bearing rays, contact/sign/bar vertices, stall rectangle separation',passed=True))
    before=json.loads(Path('build/preservation.json').read_text()) if Path('build/preservation.json').exists() else {}
    changed=[p for p,h in before.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed,changed
    out=dict(stage='form checkpoint, not baked final certification',garages=results,preserved_existing_files=len(before),passed=True)
    Path('build/check.json').write_text(json.dumps(out,indent=2)+'\n');print('CHECK PASS',[(r['seed'],r['triangles'],r['measured_aisle_clearance_min_m']) for r in results],flush=True)


if __name__=='__main__':main()
