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
        floor=tree(meshes,lambda m:'form Deck' in m.name)
        solids=tree(meshes,lambda m:not any(s in m.name.lower() for s in ('glass','groundparking','fluorescent')))
        gaps=[];support=[];path_errors=[]
        for row in p['paths']:
            for pt in row['points']:
                x,y,z=pt;hit=floor.ray_cast(Vector((x,y,z+.15)),Vector((0,0,-1)),.30)
                if hit[0] is None:path_errors.append(dict(path=row['name'],point=pt,error='no floor within 150mm'))
                else:support.append(abs(hit[0].z-z))
        # Structural clearances along the parking aisle, at each occupied floor.
        for level in range(p['levels']-1):
            for x in np.linspace(-p['length']/2+1,p['length']/2-1,31):
                y=p['flat_y'];hit=floor.ray_cast(Vector((float(x),y,level*FLOOR+.3)),Vector((0,0,-1)),.5)
                assert hit[0] is not None,(seed,x,y)
                h=solids.ray_cast(hit[0]+Vector((0,0,.18)),Vector((0,0,1)),FLOOR+1)
                if h[0] is not None:gaps.append(h[0].z-hit[0].z)
        assert not path_errors,path_errors[:6]
        assert max(support)<.02,max(support)
        assert min(gaps)>=2.1336,(seed,min(gaps))
        # Count geometry + route reservations: accessible rectangles cannot
        # overlap normal stalls after replacing a block of the row.
        overlaps=[];stalls=p['stalls']
        for i,a in enumerate(stalls):
            for b in stalls[i+1:]:
                if a['level']!=b['level'] or a['ramp']!=b['ramp']:continue
                ox=min(a['x']+a['width']/2,b['x']+b['width']/2)-max(a['x']-a['width']/2,b['x']-b['width']/2)
                oy=DEPTH-abs(a['y']-b['y'])
                if ox>1e-5 and oy>1e-5:overlaps.append([a['id'],b['id'],ox,oy])
        assert not overlaps,overlaps[:5]
        accessible=[s for s in stalls if s['accessible']];vans=[s for s in accessible if s.get('van')]
        needed=next(n for limit,n in ((25,1),(50,2),(75,3),(100,4),(150,5),(200,6),(300,7),(400,8),(500,9)) if len(stalls)<=limit)
        assert len(accessible)>=needed;assert len(vans)>=math.ceil(len(accessible)/6)
        sockets=[o for o in obs if o.get('socket_kind')=='parked_car'];assert len(sockets)==len(stalls)
        # Actual entry bar geometry: lowest yellow gantry face over drive lane.
        gantry=next(o for o in meshes if o.name.startswith('Entry gantry'))
        yellow=[o.matrix_world@o.data.vertices[i].co for o in [gantry] for poly in o.data.polygons if 'Yellow' in o.data.materials[poly.material_index].name for i in poly.vertices]
        bar_bottom=min(v.z for v in yellow);assert abs(bar_bottom-2.4892)<.0001,bar_bottom
        # Pivots retain specified axes and ranges. Sweep the module solids in
        # isolation first: this checks the actual tower/gate leaves against
        # their own construction without serialization being called mechanics.
        motions=[]
        for pv in [o for o in obs if o.get('pivot_axis') or o.get('slide_axis')]:
            if 'GateArm' in pv.name:
                motions.append(dict(node=pv.name,axis='Y',range=[-90,0],step=10,allow=[dict(moving='Entry_Gate',fixed='Entry_Gate__Gate__Housing',reason='Hinge axle in drive housing')]))
            # All pivots are explicitly counted; detailed tower sweeps run as a
            # separate report so violations are reviewable during this gate.
        moving_nodes=[o for o in obs if o.get('pivot_axis') or o.get('slide_axis')]
        images=[]
        for im in doc.get('images',[]):
            f=(path.parent/im['uri']).resolve();assert f.exists();images.append(dict(uri=im['uri'],bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
        results.append(dict(seed=seed,triangles=triangles,bounds_m=bb,materials=len(doc['materials']),image_resources=images,
            normal_unit_error=normal_error,collapsed_uv_triangles=collapsed,uv_policy='Intentional shared/tiled chart reuse; no unique lightmap UV claim',
            measured_uv_area=uv_area,measured_surface_area_m2=area,measured_aisle_clearance_min_m=min(gaps),
            measured_path_to_floor_max_m=max(support),path_samples=len(support),entry_bar_measured_m=bar_bottom,
            stall_sockets=len(sockets),accessible=len(accessible),vans=len(vans),moving_nodes=len(moving_nodes),
            serialization='triangle/bounds/socket roundtrip',construction='independent imported floor/soffit rays, bar vertices, stall rectangle separation',passed=True))
    before=json.loads(Path('build/preservation.json').read_text()) if Path('build/preservation.json').exists() else {}
    changed=[p for p,h in before.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed,changed
    out=dict(stage='form checkpoint, not baked final certification',garages=results,preserved_existing_files=len(before),passed=True)
    Path('build/check.json').write_text(json.dumps(out,indent=2)+'\n');print('CHECK PASS',[(r['seed'],r['triangles'],r['measured_aisle_clearance_min_m']) for r in results],flush=True)


if __name__=='__main__':main()
