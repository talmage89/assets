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
import geometry as G
from plan import FLOOR,SPAN,AISLE,DEPTH,STALL


def tree(objects,select=lambda m:True):
    vs=[];fs=[]
    for o in objects:
        if o.type!='MESH':continue
        o.data.calc_loop_triangles();offset=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices)
        for t in o.data.loop_triangles:
            m=o.data.materials[t.material_index]
            if select(m):fs.append(tuple(offset+i for i in t.vertices))
    return BVHTree.FromPolygons(vs,fs,all_triangles=True)


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
        floor=tree(meshes,lambda m:'form Deck' in m.name or 'form Seal' in m.name or m.name.split('.')[0]=='Concrete')
        solids=tree(meshes,lambda m:not any(s in m.name.lower() for s in ('glass','groundparking','fluorescent')))
        gaps=[];support=[];path_errors=[];support_rows=[]
        for row in p['paths']+p['pedestrian_paths']:
            for pt in row['points']:
                x,y,z=pt;hit=floor.ray_cast(Vector((x,y,z+.15)),Vector((0,0,-1)),.30)
                if hit[0] is None:path_errors.append(dict(path=row['name'],point=pt,error='no floor within 150mm'))
                else:
                    error=abs(hit[0].z-z);support.append(error);support_rows.append(dict(path=row['name'],point=pt,hit=list(hit[0]),error_m=error))
        # Structural clearances along the parking aisle, at each occupied floor.
        for level in range(p['levels']-1):
            for x in np.linspace(-p['length']/2+1,p['length']/2-1,31):
                y=p['flat_y'];hit=floor.ray_cast(Vector((float(x),y,level*FLOOR+.3)),Vector((0,0,-1)),.5)
                assert hit[0] is not None,(seed,x,y)
                h=solids.ray_cast(hit[0]+Vector((0,0,.18)),Vector((0,0,1)),FLOOR+1)
                if h[0] is not None:gaps.append(h[0].z-hit[0].z)
        assert not path_errors,path_errors[:6]
        Path(f'build/path-support-{seed}.json').write_text(json.dumps(sorted(support_rows,key=lambda r:r['error_m'],reverse=True),indent=2)+'\n')
        assert max(support)<.0002,(max(support),support_rows[support.index(max(support))])
        assert min(gaps)>=2.1336,(seed,min(gaps))
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
        # Actual full-height space at the van reservations and their ground
        # entrance/exit centerlines. Gate leaves are opened for vehicle access;
        # the declared moving-range sweep verifies that mechanism separately.
        vehicle_solids=tree([o for o in meshes if '__Gate__Arm' not in o.name],lambda m:not any(s in m.name.lower() for s in ('glass','groundparking','fluorescent')))
        van_gaps=[]
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
            hit=floor.ray_cast(Vector((x,y,z+.15)),Vector((0,0,-1)),.30)
            assert hit[0] is not None,(seed,'van floor',x,y,z)
            h=vehicle_solids.ray_cast(hit[0]+Vector((0,0,.18)),Vector((0,0,1)),FLOOR+1)
            if h[0] is not None:van_gaps.append(h[0].z-hit[0].z)
        assert min(van_gaps)>=2.4892-.0001,(seed,'van clearance',min(van_gaps))
        sockets=[o for o in obs if o.get('socket_kind')=='parked_car'];assert len(sockets)==len(stalls)
        # Actual entry bar geometry: lowest yellow gantry face over drive lane.
        gantry=next(o for o in meshes if o.name.startswith('Entry gantry'))
        yellow=[o.matrix_world@o.data.vertices[i].co for o in [gantry] for poly in o.data.polygons if 'Yellow' in o.data.materials[poly.material_index].name for i in poly.vertices]
        bar_bottom=min(v.z for v in yellow);assert abs(bar_bottom-2.4892)<.0001,bar_bottom
        moving_nodes=[o for o in obs if o.get('pivot_axis') or o.get('slide_axis')]
        images=[]
        for im in doc.get('images',[]):
            f=(path.parent/im['uri']).resolve();assert f.exists();images.append(dict(uri=im['uri'],bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
        results.append(dict(seed=seed,triangles=triangles,bounds_m=bb,materials=len(doc['materials']),image_resources=images,
            normal_unit_error=normal_error,collapsed_uv_triangles=collapsed,uv_policy='Intentional shared/tiled chart reuse; no unique lightmap UV claim',
            measured_uv_area=uv_area,measured_surface_area_m2=area,measured_aisle_clearance_min_m=min(gaps),
            measured_path_to_floor_max_m=max(support),path_samples=len(support),entry_bar_measured_m=bar_bottom,
            measured_van_route_clearance_min_m=min(van_gaps),van_clearance_samples=len(samples),
            tee_bearing_face_samples=len(bearings),measured_tee_pad_to_girder_max_gap_m=max(bearings,default=None),
            stall_sockets=len(sockets),accessible=len(accessible),vans=len(vans),moving_nodes=len(moving_nodes),
            serialization='triangle/bounds/socket roundtrip',construction='independent imported floor/soffit rays, bar vertices, stall rectangle separation',passed=True))
    before=json.loads(Path('build/preservation.json').read_text()) if Path('build/preservation.json').exists() else {}
    changed=[p for p,h in before.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed,changed
    out=dict(stage='form checkpoint, not baked final certification',garages=results,preserved_existing_files=len(before),passed=True)
    Path('build/check.json').write_text(json.dumps(out,indent=2)+'\n');print('CHECK PASS',[(r['seed'],r['triangles'],r['measured_aisle_clearance_min_m']) for r in results],flush=True)


if __name__=='__main__':main()
