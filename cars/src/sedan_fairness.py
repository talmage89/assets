"""Independent plane/ray section curvature from the evaluated parent and game skin.

No surface is fitted or changed here. Normal-angle differentiation avoids the
Dirac impulses of differentiating piecewise-planar triangle positions twice.
All raw points/normals and the finite-difference window remain in the report.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]


def field(obs):
    points=[];normals=[];triangles=[];parts=[]
    for ob in obs:
        ob.data.calc_loop_triangles();normal_matrix=ob.matrix_world.to_3x3().inverted().transposed()
        for tri in ob.data.loop_triangles:
            face=ob.data.polygons[tri.polygon_index]
            if not face.use_smooth:continue  # cut gauge rims have no smooth curvature
            center=ob.matrix_world@face.center
            radial=center-Vector((0,max(-1.4,min(1.4,center.y)),.6))
            if (normal_matrix@face.normal).dot(radial)<=0:continue  # inner sheet
            offset=len(points)
            for vi,li in zip(tri.vertices,tri.loops):
                points.append(ob.matrix_world@ob.data.vertices[vi].co)
                normals.append((normal_matrix@ob.data.corner_normals[li].vector).normalized())
            triangles.append((offset,offset+1,offset+2));parts.append(ob.name)
    tree=BVHTree.FromPolygons(points,triangles,all_triangles=True)
    def ray(origin,direction):
        p,_,fi,_=tree.ray_cast(Vector(origin),Vector(direction),5)
        if p is None:return None
        a,b,c=triangles[fi]
        n=barycentric_transform(p,points[a],points[b],points[c],normals[a],normals[b],normals[c]).normalized()
        return p,n,parts[fi]
    return ray


def measure(ray,name,kind,station,lo,hi,count=401):
    samples=[]
    for i in range(count):
        t=lo+(hi-lo)*i/(count-1)
        hit=ray((2,station,t),(-1,0,0)) if kind=='side' else ray((t,station,3),(0,0,-1))
        if hit is None:continue
        p,n,part=hit
        if kind=='side' and p.x<0:continue
        if kind=='top' and (p.z<(.90 if station>0 else .70) or n.z<.25):continue
        if kind=='side':slope=-n.z/n.x if abs(n.x)>.08 else None;value=p.x
        else:slope=-n.x/n.z if abs(n.z)>.08 else None;value=p.z
        if slope is not None:samples.append(dict(t=t,value=value,point=list(p),normal=list(n),slope=slope,part=part))
    step=(hi-lo)/(count-1)
    runs=[];run=[]
    for row in samples:
        if run and (row['part']!=run[-1]['part'] or row['t']-run[-1]['t']>1.6*step):runs.append(run);run=[]
        run.append(row)
    if run:runs.append(run)
    crossings=[]
    for run in runs:
        for i,row in enumerate(run):
            a=run[max(0,i-3)];b=run[min(len(run)-1,i+3)]
            row['break_before']=i==0
            row['curvature_m_inv']=((b['slope']-a['slope'])/(b['t']-a['t'])/(1+row['slope']**2)**1.5) if b['t']>a['t'] else 0.
        for a,b in zip(run,run[1:]):
            if a['curvature_m_inv']*b['curvature_m_inv']<0:crossings.append((a['t']+b['t'])/2)
    zones=([dict(name='rocker return',range=[.24,.30]),dict(name='lower die line / rocker roll',range=[.28+.04*station,.46+.04*station]),dict(name='shoulder / belt roll',range=[.87+.037*station,1.04+.037*station])] if kind=='side' else [])
    if kind=='side' and station<-1.8:zones=[dict(name='lower fascia / intake roll',range=[.28,.37])]
    if kind=='side' and station>1.8:zones=[dict(name='bumper upper roll',range=[.69,.80]),dict(name='tail / deck roll',range=[.91,1.05])]
    unexplained=[t for t in crossings if not any(z['range'][0]<=t<=z['range'][1] for z in zones)]
    return dict(name=name,kind=kind,station_y_m=station,samples=samples,raw_sign_crossings=crossings,character_line_zones=zones,unexplained_sign_crossings=unexplained,
                derivative='Centered normal-slope difference, +/-3 samples; no curve fit')


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--parent',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(source));obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_category') in ['body','doors','pillars','fascia','glass']]
    if a.parent:
        import sedan_body
        for ob in list(bpy.context.scene.objects):bpy.data.objects.remove(ob,do_unlink=True)
        master,_=sedan_body.master(2);obs=[master]
    ray=field(obs);sections=[]
    for y in [-2.10,-.65,-.15,.65,2.20]:sections.append(measure(ray,f'Body y={y:+.3f}', 'side',y,.26,min(1.30,.948+.037*y+.075)))
    for y in [-2.05,-1.65,-1.25]:sections.append(measure(ray,f'Hood y={y:+.2f}','top',y,-.80,.80))
    for y in [2.05,2.15,2.25]:sections.append(measure(ray,f'Deck y={y:+.2f}','top',y,-.65,.65))
    coverage=all(len(r['samples'])>=(300 if r['kind']=='top' else 100) for r in sections)
    report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scope='Catmull-Clark parent before cuts' if a.parent else 'Actual game panel positions and authored corner normals',sections=sections,passed=coverage and all(not r['unexplained_sign_crossings'] for r in sections),coverage_passed=coverage,selection='Outward smooth skin only; inner gauge and flat cut rims excluded; physical cuts/parts split derivative runs')
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(report,indent=2))
    print('CURVATURE',[(r['name'],len(r['samples']),len(r['raw_sign_crossings'])) for r in sections])
    if not report['passed']:raise AssertionError('Curvature reversals outside the documented construction lines')
if __name__=='__main__':main()
