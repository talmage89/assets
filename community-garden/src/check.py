"""Independent accessor, re-import, dimensions and actual-surface checks.

Checkpoint scope: unbaked form materials, intentionally reused leaf/fence UVs.
No final atlas overlap, bake coverage, albedo or game-ready claim is made.
"""
import sys,json,math,hashlib
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
from kit.gltf import GLB
from geometry import count
from plan import SEEDS


class Document(GLB):
    def __init__(self,path):
        self.path=Path(path);self.json=json.loads(self.path.read_text())
        assert len(self.json['buffers'])==1
        self.binary=(self.path.parent/self.json['buffers'][0]['uri']).read_bytes()
        self.parents={c:i for i,n in enumerate(self.json.get('nodes',[])) for c in n.get('children',[])}


def raw(path):
    d=Document(path);triangles=0;primitives=0;bad=0;points=[];normerr=0;wind_primitives=0
    for i,node in enumerate(d.json['nodes']):
        if 'mesh' not in node:continue
        for p in d.json['meshes'][node['mesh']]['primitives']:
            assert p.get('mode',4)==4
            xyz=d.accessor(p['attributes']['POSITION']);norm=d.accessor(p['attributes']['NORMAL'])
            assert np.isfinite(xyz).all() and np.isfinite(norm).all()
            assert 'COLOR_0' not in p['attributes'],'Data masks must not multiply the material albedo'
            if '_WIND' in p['attributes']:
                wind=d.accessor(p['attributes']['_WIND']);assert np.isfinite(wind).all() and wind.min()>=0 and wind.max()<=1
                wind_primitives+=1
            normerr=max(normerr,float(np.max(abs(np.linalg.norm(norm,axis=1)-1))))
            ids=d.accessor(p['indices']).ravel();assert len(ids)%3==0;assert ids.max()<len(xyz)
            a,b,c=(xyz[ids.reshape(-1,3)[:,k]] for k in range(3));bad+=int((np.linalg.norm(np.cross(b-a,c-a),axis=1)<1e-14).sum())
            m=d.world(i);points.append((np.c_[xyz,np.ones(len(xyz))]@m.T)[:,:3]);triangles+=len(ids)//3;primitives+=1
    assert bad==0,('Collapsed exported faces',bad)
    assert normerr<.001,('Non-unit normals',normerr)
    images=[]
    for row in d.json.get('images',[]):
        assert 'uri' in row and 'bufferView' not in row
        p=d.path.parent/row['uri'];assert p.is_file()
        images.append(dict(uri=row['uri'],bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    q=np.concatenate(points);return dict(triangles=triangles,primitives=primitives,normal_length_error=normerr,degenerate_triangles=bad,
        bounds_min=q.min(axis=0).tolist(),bounds_max=q.max(axis=0).tolist(),images=images,
        gltf_bytes=d.path.stat().st_size,bin_bytes=len(d.binary),materials=len(d.json.get('materials',[])),unique_meshes=len(d.json['meshes']),wind_primitives=wind_primitives)


def merge(intervals):
    out=[]
    for a,b in sorted(intervals):
        if out and a<=out[-1][1]+1e-5:out[-1][1]=max(out[-1][1],b)
        else:out.append([a,b])
    return out


def route_width(ground,y):
    intervals=[]
    for face in ground.data.polygons:
        ma=ground.data.materials[face.material_index]
        if 'Gravel' not in ma.name or face.normal.z<.9999:continue
        v=[ground.matrix_world@ground.data.vertices[i].co for i in face.vertices];xs=[]
        for a,b in zip(v,v[1:]+v[:1]):
            if abs(a.y-y)<1e-6:xs.append(a.x)
            if (a.y-y)*(b.y-y)<0:xs.append(a.x+(b.x-a.x)*(y-a.y)/(b.y-a.y))
        if len(xs)>1:intervals.append((min(xs),max(xs)))
    union=merge(intervals);center=next((p for p in union if p[0]<=0<=p[1]),None)
    assert center,'No continuous main-route top surface at Y='+str(y)
    return center[1]-center[0]


def imported(seed,expected):
    p=Path(f'export/checkpoint/Garden_{seed}.gltf');bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(p.resolve()));bpy.context.view_layer.update()
    roots=[o for o in bpy.context.scene.objects if not o.parent];assert len(roots)==1
    rt=roots[0];assert rt.matrix_world.translation.length<1e-6
    assert count(rt)==expected['triangles']
    meshes=[o for o in rt.children_recursive if o.type=='MESH'];points=np.array([o.matrix_world@v.co for o in meshes for v in o.data.vertices])
    # Raw glTF is Y-up; compare independent Blender-import world bounds.
    transform=lambda a:np.array([a[0],-a[2],a[1]])
    lo=transform(expected['bounds_min']);hi=transform(expected['bounds_max']);lo[1],hi[1]=hi[1],lo[1]
    err=max(float(abs(points.min(axis=0)-lo).max()),float(abs(points.max(axis=0)-hi).max()));assert err<2e-4
    info=json.loads(Path(f'build/garden-{seed}.json').read_text());plan=info['plan']
    ground=next(o for o in meshes if o.parent and o.parent.name.startswith('GardenGround'))
    spine=plan['paths'][0];start=spine['center'][1]-spine['size'][1]/2+.025;end=spine['center'][1]+spine['size'][1]/2-.025
    widths=[route_width(ground,float(y)) for y in np.linspace(start,end,math.ceil((end-start)/.1524)+1)]
    assert min(widths)>=plan['main_width']-1e-5
    sockets=[o for o in rt.children_recursive if o.get('socket_kind')=='gardener'];assert len(sockets)==len(plan['plots'])+1
    ground.data.calc_loop_triangles();gv=[ground.matrix_world@v.co for v in ground.data.vertices]
    gt=BVHTree.FromPolygons(gv,[t.vertices[:] for t in ground.data.loop_triangles],all_triangles=True)
    socket_errors=[]
    for sock in sockets:
        v=sock.matrix_world.translation;hit=gt.ray_cast(Vector((v.x,v.y,2)),Vector((0,0,-1)),4)[0]
        assert hit is not None;socket_errors.append(abs(v.z-hit.z))
        forward=sock.matrix_world.to_3x3()@Vector((0,-1,0))
        if sock.name.startswith('Socket_Plot'):
            target=sock.parent.matrix_world.translation-v;target.z=0
            assert forward.normalized().dot(target.normalized())>.999,'Plot socket faces away from bed'
    assert max(socket_errors)<.001,('Gardener socket off actual walking surface',max(socket_errors))
    mature=sorted({o.get('species') for o in rt.children_recursive if o.get('stage_fraction',0)>=.7})
    assert {'tomato','bean','corn','squash'}.issubset(set(mature)),('Missing midsummer staple crop',mature)
    gate=next(o for o in rt.children_recursive if o.name.startswith('GateLeaf'))
    assert gate['pivot_axis']=='Z';assert list(gate['range_degrees'])==[-110,0]
    # Actual vertices on the two fixed terminal tubes establish the opening.
    parent=gate.parent;fixed=next(o for o in parent.children if o.type=='MESH')
    verts=[v.co for v in fixed.data.vertices];left=[v.x for v in verts if v.x<-.3];right=[v.x for v in verts if v.x>.3]
    clear=min(right)-max(left);assert clear>.9144
    # Sampled motion geometry is checked separately by kit.motion in motion.py;
    # this section only proves the pivot serializes and preserves distances.
    child=next(o for o in gate.children if o.type=='MESH');hinge=gate.matrix_world.translation.copy()
    gate.rotation_mode='XYZ';gate.rotation_euler.z=0;bpy.context.view_layer.update();a=[child.matrix_world@v.co for v in child.data.vertices]
    gate.rotation_euler.z=math.radians(-110);bpy.context.view_layer.update();b=[child.matrix_world@v.co for v in child.data.vertices]
    radius_error=max(abs((v-hinge).length-(w-hinge).length) for v,w in zip(a,b));assert radius_error<2e-5
    beds=[o for o in rt.children if o.get('plot_id')]
    modules={o.name:count(o) for o in rt.children if o.get('kind') in ('fence','gate') or o.name.startswith('RainCapture')}
    assert all(n<=2000 for n in modules.values()),('Infrastructure module over budget',modules)
    # Footprint and neighbour gaps are measured from bed top edges, selecting
    # wood/block above the soil and ignoring foliage, markers and straw.
    boxes=[]
    for bed in beds:
        vv=[]
        for ob in bed.children:
            if ob.type!='MESH':continue
            for f in ob.data.polygons:
                mat=ob.data.materials[f.material_index].name
                if any(s in mat for s in ('Wood','Block')):
                    for i in f.vertices:
                        v=ob.matrix_world@ob.data.vertices[i].co
                        if .10<v.z<.34:vv.append(v)
        if vv:boxes.append((bed['plot_id'],[min(v[i] for v in vv) for i in (0,1)],[max(v[i] for v in vv) for i in (0,1)]))
    gaps=[]
    for i,a in enumerate(boxes):
        for b in boxes[i+1:]:
            for axis in (0,1):
                other=1-axis
                if min(a[2][other],b[2][other])-max(a[1][other],b[1][other])>.3:
                    gap=max(a[1][axis],b[1][axis])-min(a[2][axis],b[2][axis])
                    if gap>=0:gaps.append(gap)
    assert not gaps or min(gaps)>.85,('Narrow working aisle',min(gaps))
    return dict(import_triangle_count=count(rt),raw_import_bounds_error_m=err,measured_main_route_widths_m=widths,
                measured_gate_clear_width_m=clear,plot_sockets=len(sockets)-1,gate_radius_error_m=radius_error,
                measured_bed_to_bed_min_gap_m=min(gaps) if gaps else None,mature_species=mature,
                gardener_socket_ground_error_m=max(socket_errors),placed_infrastructure_triangles=modules)


def main():
    report=dict(stage='form checkpoint; final UV/bake/texture delivery not claimed',gardens={},pieces={})
    counts=json.loads(Path('build/pieces.json').read_text())
    for n,row in counts.items():
        cap=5000 if row['kind']=='plant' else 8000 if n=='NativeShed' else 2000
        assert row['triangles']<=cap,(n,row['triangles'],cap)
    report['pieces']=counts
    for s in SEEDS:
        row=raw(Path(f'export/checkpoint/Garden_{s}.gltf'));assert row['triangles']<250000
        info=json.loads(Path(f'build/garden-{s}.json').read_text());assert row['triangles']==info['triangles']
        row['import']=imported(s,row);report['gardens'][str(s)]=row
    library=raw('export/checkpoint/CommunityGardenPieces.gltf');report['library']=library
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path('export/checkpoint/CommunityGardenPieces.gltf').resolve()));bpy.context.view_layer.update()
    roots={o.name:o for o in bpy.context.scene.objects if not o.parent}
    def points(n,wood_only=False):
        result=[]
        for ob in roots[n].children_recursive:
            if ob.type!='MESH':continue
            ids={i for f in ob.data.polygons if not wood_only or 'Wood' in ob.data.materials[f.material_index].name for i in f.vertices}
            result.extend(ob.matrix_world@ob.data.vertices[i].co for i in ids)
        return result
    def tree(n):
        vertices=[];faces=[]
        for ob in roots[n].children_recursive:
            if ob.type!='MESH':continue
            start=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
            faces.extend(tuple(start+i for i in f.vertices) for f in ob.data.polygons)
        return BVHTree.FromPolygons(vertices,faces)
    vv=points('Raised4x8',True);w=max(p.x for p in vv)-min(p.x for p in vv);depth=max(p.y for p in vv)-min(p.y for p in vv)
    side=[]
    for ob in roots['Raised4x8'].children_recursive:
        if ob.type!='MESH':continue
        for f in ob.data.polygons:
            if 'Wood' not in ob.data.materials[f.material_index].name or abs((ob.matrix_world.to_3x3()@f.normal).x)<.999:continue
            side.extend(ob.matrix_world@ob.data.vertices[i].co for i in f.vertices if ob.data.vertices[i].co.x>.55)
    gauge=max(p.x for p in side)-min(p.x for p in side)
    assert abs(w-1.2192)<1e-5 and abs(depth-2.4384)<1e-5 and abs(gauge-.0381)<1e-5,dict(width=w,depth=depth,gauge=gauge)
    accessible=tree('Accessible8x3');clear_tests=[]
    for x in (-.37,0,.37):
        for z in (.23,.50,.6858):
            hit=accessible.ray_cast(Vector((x,-1,z)),Vector((0,1,0)),2.0);clear_tests.append(hit[0] is None)
    assert all(clear_tests),'Accessible bed obstructs knee corridor'
    top=accessible.ray_cast(Vector((0,0,2)),Vector((0,0,-1)),3)[0].z
    # Ray upward from inside the knee opening to the actual tray underside.
    underside=accessible.ray_cast(Vector((0,0,.4)),Vector((0,0,1)),1)[0].z
    assert underside>=.6858 and top<.8636
    block=tree('Block4x8');hole=block.ray_cast(Vector((.51435,-.916,.4)),Vector((0,0,-1)),.8)
    web=block.ray_cast(Vector((.51435,-1.016,.4)),Vector((0,0,-1)),.8)
    assert hole[0] is None and web[0] is not None,'CMU open core/web construction failed'
    assert abs(web[0].z-.193675)<1e-6,'CMU height differs from specified 7-5/8in'
    report['construction']=dict(raised_width_m=w,raised_depth_m=depth,side_board_gauge_m=gauge,
        knee_clearance_rays=len(clear_tests),knee_clearance_passed=all(clear_tests),tray_underside_m=underside,
        soil_top_m=top,cmu_core_ray_open=True,cmu_web_top_m=web[0].z,
        scope='actual imported surfaces, separate from raw/import serialization comparison')
    # Shared external leaf/mesh/lawn images must have identical identities.
    identity=[{i['sha256'] for i in row['images']} for row in report['gardens'].values()]
    assert len(set.intersection(*identity))>=6,'Leaf and wire maps must be shared across all seeds'
    canonical={}
    for row in report['gardens'].values():
        for im in row['images']:
            if im['uri'] in canonical:assert canonical[im['uri']]==im['sha256']
            canonical[im['uri']]=im['sha256']
    report['passed']=True
    Path('build/check.json').write_text(json.dumps(report,indent=2));print(json.dumps({s:dict(triangles=r['triangles'],materials=r['materials'],geometry_bytes=r['bin_bytes'],measurements=r['import']) for s,r in report['gardens'].items()},indent=2))


if __name__=='__main__':main()
