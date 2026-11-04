"""Independent round-three surface measurements on game triangles.

Angles use the rendered interpolated corner-normal field; distances are mesh
rays and silhouette cuts. This measures construction, not visual acceptance.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from hatch_check import bounds,points,mesh_tree
from hatch_fairness import field


def measure(source):
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Hatch']
    skins=[o for o in obs if o.get('part_category') in ['body','doors','fascia','pillars','glass']]
    ray=field(skins);tree=mesh_tree(skins)
    sections=[]
    for name,y in [('front door',-.335),('B pillar',.255),('rear door',.755)]:
        def hit(z):return ray((2,y,z),(-1,0,0))
        def turn(lo,hi,width):
            samples=[]
            for i in range(round((hi-lo)/.001)+1):
                z=lo+i*.001;a,b=hit(z-width/2),hit(z+width/2)
                if a and b:samples.append((math.degrees(a[1].angle(b[1])),z,a,b))
            angle,z,a,b=max(samples,key=lambda r:r[0])
            return dict(normal_turn_degrees=angle,vertical_width_m=width,surface_chord_m=(a[0]-b[0]).length,center_z_m=z,
                        endpoints_m=[list(a[0]),list(b[0])],normals=[list(a[1]),list(b[1])])
        sections.append(dict(name=name,y_m=y,shoulder=turn(.85,.93,.030),lower=turn(.42,.55,.030)))
    crowns=[]
    from hatch_body import shoulder_height
    for y in [-1.255,1.395]:
        h=shoulder_height(y);samples=[]
        for i in range(51):
            z=h-.125+i*.001;a,b=ray((2,y,z),(-1,0,0)),ray((2,y,z+.070),(-1,0,0))
            if a and b:samples.append((math.degrees(a[1].angle(b[1])),a,b))
        angle,a,b=max(samples,key=lambda r:r[0])
        crowns.append(dict(y_m=y,normal_turn_degrees=angle,vertical_width_m=.070,
                           surface_chord_m=(a[0]-b[0]).length,endpoints_m=[list(a[0]),list(b[0])]))
    rear=[]
    def end(x,z):return tree.ray_cast(Vector((x,3,z)),Vector((0,-1,0)),2)[0]
    for x in [0,.25,.50]:
        candidates=[end(x,.648+i*.001) for i in range(38)];candidates=[p for p in candidates if p is not None]
        lip=max(candidates,key=lambda p:p.y);below=end(x,.610)
        aa,mid,bb=[end(x,z) for z in [.760,.820,.880]]
        rear.append(dict(x_m=x,lip_m=list(lip),bumper_below_m=list(below),lip_proud_m=lip.y-below.y,
                         concave_vertical_chord_depth_m=(aa.y+bb.y)/2-mid.y,concavity_points_m=[list(q) for q in [aa,mid,bb]]))
    plan=[]
    for z in [.80,.835,.87]:
        a,c,b=[end(x,z) for x in [-.45,0,.45]]
        plan.append(dict(z_m=z,center_recess_below_chord_m=(a.y+b.y)/2-c.y,points_m=[list(q) for q in [a,c,b]]))
    fascia=bpy.data.objects['Rear molded fascia'];areas={};zs={}
    for face in fascia.data.polygons:
        key=fascia.data.materials[face.material_index].name
        areas[key]=areas.get(key,0)+face.area
        zs.setdefault(key,[]).extend((fascia.matrix_world@fascia.data.vertices[i].co).z for i in face.vertices)
    from mathutils.bvhtree import BVHTree
    fascia_tree=BVHTree.FromPolygons(points(fascia),[tuple(f.vertices) for f in fascia.data.polygons])
    paint_band=[]
    for z in [.20+i*.001 for i in range(446)]:
        p,_,fi,_=fascia_tree.ray_cast(Vector((0,3,z)),Vector((0,-1,0)),2)
        if p is not None and fascia.data.polygons[fi].material_index==0:paint_band.append(list(p))
    black_width=[]
    for z in [.35,.45,.55]:
        hits=[]
        for i in range(901):
            p,_,fi,_=fascia_tree.ray_cast(Vector((i*.001,3,z)),Vector((0,-1,0)),2)
            if p is not None and fascia.data.polygons[fi].material_index==1:hits.append(list(p))
        black_width.append(dict(z_m=z,width_m=2*max(p[0] for p in hits)))
    mirrors={}
    for suffix in ['L','R']:
        cap=bpy.data.objects['Mirror housing_'+suffix];bb=bounds([cap]);ps=points(cap)
        # Orthographic front silhouette sampled as maxima, independent of rings.
        xs=sorted(set(round(abs(p.x),6) for p in ps));outline=[]
        for x in xs:
            column=[p for p in ps if abs(abs(p.x)-x)<.000001]
            outline.append([x,min(p.z for p in column),max(p.z for p in column)])
        mirrors[suffix]=dict(bounds_m=bb,front_outline_x_zmin_zmax_m=outline,
                              crown_height_above_inboard_top_m=max(p.z for p in ps)-max(p.z for p in ps if abs(p.x)<bb['size'][0]*.15+min(abs(q.x) for q in ps)))
        # Fit a circle through three ACTUAL front-outline vertices around the
        # outboard end, not the Bezier's design radius or a stored parameter.
        ring=[p for p in ps if abs(p.y+.612)<1e-6]
        tip=max(ring,key=lambda p:abs(p.x));upper=max((p for p in ring if p.z>tip.z+.020),key=lambda p:abs(p.x))
        lower=max((p for p in ring if p.z<tip.z-.020),key=lambda p:abs(p.x))
        a,b,c=[Vector((abs(p.x),p.z)) for p in [upper,tip,lower]]
        area2=abs((b-a).cross(c-a));radius=(a-b).length*(b-c).length*(c-a).length/(2*area2)
        mirrors[suffix]['front_outboard_three_point_radius_m']=radius
        mirrors[suffix]['radius_points_xz_m']=[list(p) for p in [a,b,c]]
    reflectors={o.name:bounds([o]) for o in obs if o.name.startswith('Rear reflector') and 'return' not in o.name}
    frame=points(bpy.data.objects['Grille proud surround']);lamp_gaps={}
    for ob in obs:
        if not ob.name.startswith('Headlamp opening'):continue
        ps=points(ob);tip=min(abs(p.x) for p in ps)
        candidates=[p for p in ps if abs(p.x)<tip+.025]
        a,b=min(((p,q) for p in candidates for q in frame),key=lambda pair:(pair[0]-pair[1]).length)
        lamp_gaps[ob.name]=dict(shortest_inner_lens_to_frame_m=(a-b).length,endpoints_m=[list(a),list(b)])
    counts={}
    for ob in obs:
        ob.data.calc_loop_triangles();key=ob['part_category'];counts[key]=counts.get(key,0)+len(ob.data.loop_triangles)
    errors=[]
    for row in sections:
        if not 15<=row['shoulder']['normal_turn_degrees']<=26:errors.append(row['name']+' shoulder turn')
        if not 10<=row['lower']['normal_turn_degrees']<=25:errors.append(row['name']+' lower turn')
    if not all(.020<=row['lip_proud_m']<=.041 for row in rear):errors.append('Gate lip proud of bumper')
    if not all(row['concave_vertical_chord_depth_m']>.010 for row in rear[:2]):errors.append('Gate vertical concave run')
    if sum(counts.values())>46881:errors.append('Accepted form allocation exceeded')
    return dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scope='Source form construction; actual game rays, corners and triangle counts. Photo pairs remain the visual judgment.',
                sections=sections,fender_crowns=crowns,gate=rear,gate_plan=plan,bumper_material_areas_m2=areas,bumper_material_z_ranges_m={k:[min(v),max(v)] for k,v in zs.items()},
                bumper_center_painted_band_z_m=[min(p[2] for p in paint_band),max(p[2] for p in paint_band)],bumper_black_widths=black_width,
                mirrors=mirrors,reflectors=reflectors,headlamp_frame_gaps=lamp_gaps,triangles_per_category=counts,triangles=sum(counts.values()),finished_plan=sum(counts.values())+12500,
                passed=not errors,errors=errors)


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--diagnostic',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    r=measure(Path(a.source));Path(a.out).write_text(json.dumps(r,indent=2));print(json.dumps({k:r[k] for k in ['sections','gate','gate_plan','triangles','errors']},indent=2))
    if r['errors'] and not a.diagnostic:raise AssertionError(r['errors'])
if __name__=='__main__':main()
