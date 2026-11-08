"""Verify the shipped U-lock encloses actual frame/rack sections without crossings."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import convex_hull_2d
from kit.motion import surface


def combine(parts):
    points=[];faces=[]
    for part in parts:
        start=len(points);points.extend(part['points']);faces.extend(tuple(start+i for i in f) for f in part['faces'])
    assert faces
    return dict(points=points,faces=faces,tree=BVHTree.FromPolygons(points,faces,all_triangles=True))


def selected(ob,root,cell,lock=False):
    uv=ob.data.uv_layers[0];inv=root.matrix_world.inverted();local=[inv@ob.matrix_world@v.co for v in ob.data.vertices];faces=[]
    for f in ob.data.polygons:
        if not all(cell[0]-1e-6<=uv.data[i].uv.x<=cell[2]+1e-6 and cell[1]-1e-6<=uv.data[i].uv.y<=cell[3]+1e-6 for i in f.loop_indices):continue
        if lock and not all(.5<local[i].z<.85 and local[i].x<.05 for i in f.vertices):continue
        faces.append(tuple(f.vertices))
    return dict(points=[ob.matrix_world@v.co for v in ob.data.vertices],faces=faces)


def sections(s,normal,origin):
    # Import splits vertices at UV/smoothing seams. Weld intersection endpoints
    # by distance, rather than decimal rounding across an arbitrary boundary.
    graph={};vertices=[]
    def key(v):
        for i,p in enumerate(vertices):
            if np.linalg.norm(v-p)<.000005:return i
        vertices.append(v);return len(vertices)-1
    for face in s['faces']:
        p=[np.asarray(s['points'][i]) for i in face];d=[float(np.dot(v-origin,normal)) for v in p];hits=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if abs(d[i])<1e-8:hits.append(p[i])
            if d[i]*d[j]<0:hits.append(p[i]+(p[j]-p[i])*(d[i]/(d[i]-d[j])))
        hits=list(dict.fromkeys(key(v) for v in hits))
        if len(hits)==2:
            a,b=hits;graph.setdefault(a,set()).add(b);graph.setdefault(b,set()).add(a)
    remaining=set(graph);result=[]
    while remaining:
        pending=[remaining.pop()];found=set(pending)
        while pending:
            for other in graph[pending.pop()]:
                if other not in found:found.add(other);remaining.discard(other);pending.append(other)
        # A disconnected arc is not evidence that a whole section is enclosed.
        if len(found)>=3 and all(len(graph[i])==2 for i in found):result.append(np.asarray([vertices[i] for i in sorted(found)]))
    return result


def audit(seed):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(f'export/CoffeeShop-{seed}.gltf').resolve()));bpy.context.view_layer.update()
    bike=bpy.data.objects['Locked commuter bicycle'];body=next(o for o in bike.children_recursive if o.type=='MESH');rack=bpy.data.objects['Outdoor_BikeRack'];charts=json.loads(Path('build/atlas/layout.json').read_text())
    lock=combine([selected(body,bike,charts['black'],True)]);frame=combine([selected(body,bike,charts['forest'])]);support=combine([surface(o) for o in rack.children_recursive if o.type=='MESH'])
    used=sorted({i for f in lock['faces'] for i in f});points=np.unique(np.round(np.asarray([lock['points'][i] for i in used]),8),axis=0);origin=points.mean(0);_,_,basis=np.linalg.svd(points-origin,full_matrices=False);normal=basis[2]
    project=lambda p:np.column_stack(((p-origin)@basis[0],(p-origin)@basis[1]))
    planar=project(points);hull=planar[convex_hull_2d([Vector(v) for v in planar])]
    def contains(p):
        cross=np.asarray([(b[0]-a[0])*(p[:,1]-a[1])-(b[1]-a[1])*(p[:,0]-a[0]) for a,b in zip(hull,np.roll(hull,-1,axis=0))])
        return bool(np.all(np.all(cross>=-1e-7,axis=0)|np.all(cross<=1e-7,axis=0)))
    rows={}
    for name,other in (('frame',frame),('rack',support)):
        cuts=sections(other,normal,origin);enclosed=[c for c in cuts if contains(project(c))];crossings=lock['tree'].overlap(other['tree'])
        rows[name]=dict(section_loops=len(cuts),enclosed_section_loops=len(enclosed),surface_triangle_crossings=len(crossings),enclosed_section_bounds_m=[dict(min=c.min(0).tolist(),max=c.max(0).tolist()) for c in enclosed])
        assert enclosed,(seed,'U-lock does not enclose '+name,rows[name])
        assert not crossings,(seed,'U-lock intersects '+name,len(crossings))
    samples=[]
    for ids in lock['faces']:
        a,b,c=[lock['points'][i] for i in ids]
        for i in range(13):
            for j in range(13-i):samples.append(a*(i/12)+b*(j/12)+c*(1-(i+j)/12))
    gap=min(frame['tree'].find_nearest(p)[3] for p in samples);assert gap<.004,(seed,'Lock support gap',gap)
    triangles=sum(len(f.vertices)-2 for f in body.data.polygons);assert triangles<=3000
    return dict(seed=seed,bicycle_triangles=triangles,lock_triangles=len(lock['faces']),sections=rows,minimum_sampled_frame_support_gap_m=gap,support_samples=len(samples),scope='Fresh exported triangles; plane fitted to actual lock skin; complete frame/rack section loops inside its convex span and no surface crossings. Support gap uses barycentric samples, not an exact global distance.')

if __name__=='__main__':
    rows=[audit(seed) for seed in (117,228,339)];Path('build/use-check.json').write_text(json.dumps(rows,indent=2)+'\n');print('USE CHECK PASS',[(r['seed'],r['bicycle_triangles'],r['minimum_sampled_frame_support_gap_m']) for r in rows])
