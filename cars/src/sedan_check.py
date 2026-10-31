"""Actual source surfaces, plane cuts and static form measurements.

No motion, UV, bake or delivery certification. The kit audit supplies topology;
these rays/cuts independently measure the requested proportions and sections.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import sedan_spec as S

def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]
def bounds(obs):
    ps=[p for ob in obs for p in points(ob)]
    lo=[min(p[k] for p in ps) for k in range(3)];hi=[max(p[k] for p in ps) for k in range(3)]
    return dict(min=lo,max=hi,size=[b-a for a,b in zip(lo,hi)])
def mesh_tree(obs):
    ps=[];fs=[]
    for ob in obs:
        offset=len(ps);ps+=points(ob);fs.extend(tuple(offset+i for i in f.vertices) for f in ob.data.polygons)
    return BVHTree.FromPolygons(ps,fs)
def plane_cut(obs,y,axis=1):
    result=[]
    for ob in obs:
        ps=points(ob);ob.data.calc_loop_triangles()
        for tri in ob.data.loop_triangles:
            hits=[];vs=[ps[i] for i in tri.vertices]
            for a,b in zip(vs,vs[1:]+vs[:1]):
                if abs(a[axis]-y)<1e-7:hits.append([a[1-axis],a.z])
                if (a[axis]-y)*(b[axis]-y)<0:
                    p=a+(b-a)*((y-a[axis])/(b[axis]-a[axis]));hits.append([p[1-axis],p.z])
            unique=[]
            for hit in hits:
                if not any(math.dist(hit,h)<1e-7 for h in unique):unique.append(hit)
            if len(unique)==2:result.append(unique)
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Sedan'];categories={};parts={};parents={}
    for ob in obs:
        ob.data.calc_loop_triangles();num=len(ob.data.loop_triangles);parts[ob.name]=num
        key=ob['part_category'];categories[key]=categories.get(key,0)+num;parents[ob.parent.name]=parents.get(ob.parent.name,0)+num
    skins=[o for o in obs if o['part_category'] in ['body','doors','glass','pillars','fascia']];tree=mesh_tree(skins)
    def side(y,z):
        hit=tree.ray_cast(Vector((2,y,z)),Vector((-1,0,0)),3)[0]
        if hit is None:raise ValueError(('No section hit',y,z))
        return hit.x
    profiles=[]
    for name,y in [('front_axle',S.FRONT_AXLE),('b_pillar',S.DOOR_SPLIT),('rear_axle',S.REAR_AXLE)]:
        segments=plane_cut(skins,y);record=dict(name=name,y_m=y,segments_xz_m=segments)
        if name=='b_pillar':
            lo,hi=1.040,1.340;xl,xh=side(y,lo),side(y,hi)
            record.update(tumblehome_degrees=math.degrees(math.atan2(xl-xh,hi-lo)),tumblehome_samples_m=[[xl,lo],[xh,hi]])
        profiles.append(record)
    wheels={n:list(bpy.data.objects['Wheel_'+n].matrix_world.translation) for n in ['FL','FR','RL','RR']}
    wheelbase=wheels['RL'][1]-wheels['FL'][1];tracks={e:wheels[e+'R'][0]-wheels[e+'L'][0] for e in ['F','R']}
    arches=[]
    for code in wheels:
        tire=bounds([bpy.data.objects['Tire_'+code]]);lip=bounds([bpy.data.objects['Arch flange_'+code]])
        arches.append(dict(wheel=code,tire_bounds_m=tire,arch_top_m=lip['max'][2],tire_to_arch_m=lip['max'][2]-tire['max'][2]))
    hood=points(bpy.data.objects['Hood outer']);roof=points(bpy.data.objects['Roof']);trunk=points(bpy.data.objects['Trunk outer'])
    # Probe physical outer A-pillar stations from the evaluated greenhouse.
    pillar=points(bpy.data.objects['Greenhouse_R']);low=min(pillar,key=lambda p:abs(p.z-.99)+abs(p.y-(-.93+S.CORE_SHIFT)));high=min(pillar,key=lambda p:abs(p.z-1.38)+abs(p.y-(-.27+S.CORE_SHIFT)))
    rake=math.degrees(math.atan2(high.y-low.y,high.z-low.z))
    # Actual exposed body crown in the door, relative to its endpoints.
    lower,mid,upper=[side(-.4,z) for z in [.37,.58,.82]]
    crown=mid-(lower+(upper-lower)*(.58-.37)/(.82-.37))
    # Nearest distances from the outer front-door seam to the rear panel.
    seams={}
    for side_name in ['L','R']:
        front=bpy.data.objects['Door F_'+side_name];rear=bpy.data.objects['Door R_'+side_name];rt=mesh_tree([rear])
        ps=points(front);back=max(p.y for p in ps);selected=[p for p in ps if p.y>back-.012 and .42<p.z<.85]
        ds=[rt.find_nearest(p)[3] for p in selected]
        seams[side_name]=dict(samples=len(ds),min_m=min(ds),max_m=max(ds))
    report=dict(stage='source form only',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),quality=bpy.context.scene['quality'],
       triangles=sum(parts.values()),triangles_per_category=categories,triangles_per_mesh=parts,triangles_per_parent=parents,
       materials=sorted({m.name for o in obs for m in o.data.materials if m}),image_textures=len([im for im in bpy.data.images if im.users and im.source=='FILE']),bounds_m=bounds(obs),
       wheel_centers_m=wheels,wheelbase_m=wheelbase,tracks_m=tracks,arches=arches,sections=profiles,
       a_pillar_rake_from_vertical_degrees=rake,a_pillar_measured_points_m=[list(low),list(high)],
       hood_leading_center_m=list(min([p for p in hood if abs(p.x)<.05],key=lambda p:p.y)),
       roof_peak_m=list(max(roof,key=lambda p:p.z)),deck_trailing_peak_m=list(max([p for p in trunk if p.y>2.2],key=lambda p:p.z)),
       door_crown_above_370_820_chord_m=crown,door_side_rays_m=[[lower,.37],[mid,.58],[upper,.82]],door_seams=seams,
       deferred=['interior','underbody and measured ground clearance','motion sweeps','UV/bake/GLB','final materials and docs'])
    # Independent centerline intersections and surface rays, never the cage
    # design controls. Keep the sampled curves with the measurements so that a
    # reviewer can reproduce exactly which physical tangent was measured.
    center=plane_cut(skins,0,axis=0)
    profiles.append(dict(name='centerline',x_m=0,segments_yz_m=center))
    def end(x,z,front):
        point=tree.ray_cast(Vector((x,-4 if front else 4,z)),Vector((0,1 if front else -1,0)),5)[0]
        if point is None:raise ValueError(('End ray missed',x,z,front))
        return point
    def top(x,y):
        p=tree.ray_cast(Vector((x,y,3)),Vector((0,0,-1)),3)[0]
        if p is None:raise ValueError(('Top ray missed',x,y))
        return p
    curves={}
    for front in [True,False]:
        key='front' if front else 'rear'
        curve=[]
        for i in range(390 if not front else 270):
            try:curve.append(end(0,.220+i*.002,front))
            except ValueError:pass  # a physical shut-line can lie at the sampled height
        bumper=(min if front else max)(curve,key=lambda p:p.y)
        if front:
            edge=Vector(report['hood_leading_center_m'])
            cowl=max([p for p in hood if abs(p.x)<.05],key=lambda p:p.y)
            chin=min([p for p in points(bpy.data.objects['Front molded fascia']) if abs(p.x)<.05],key=lambda p:p.z)
            crown0,crownL,crownR=[top(x,-1.65) for x in [0,-.80,.80]]
            curves[key]=dict(bumper_leading_m=list(bumper),hood_edge_m=list(edge),cowl_m=list(cowl),chin_m=list(chin),
              upper_face_degrees_from_vertical=math.degrees(math.atan2(edge.y-bumper.y,edge.z-bumper.z)),
              hood_edge_setback_m=edge.y-bumper.y,chin_tuck_m=chin.y-bumper.y,
              hood_rise_degrees=math.degrees(math.atan2(cowl.z-edge.z,cowl.y-edge.y)),
              hood_transverse_crown_m=crown0.z-(crownL.z+crownR.z)/2,
              hood_crown_samples_m=[list(p) for p in [crown0,crownL,crownR]],
              plan_sweep_at_850mm_m=end(.850,bumper.z,True).y-bumper.y)
        else:
            edge=max([p for p in trunk if abs(p.x)<.05 and p.y>2.15],key=lambda p:p.z)
            glass=points(bpy.data.objects['Backlight']);base=max([p for p in glass if abs(p.x)<.05],key=lambda p:p.y)
            lower=end(0,.300,False)
            dc,dl,dr=[top(x,2.15) for x in [0,-.60,.60]]
            curves[key]=dict(bumper_rearmost_m=list(bumper),deck_trailing_edge_m=list(edge),backlight_base_m=list(base),diffuser_m=list(lower),
              upper_panel_degrees_from_vertical=math.degrees(math.atan2(bumper.y-edge.y,edge.z-bumper.z)),
              lower_tuck_m=bumper.y-lower.y,deck_length_m=edge.y-base.y,deck_rise_degrees=math.degrees(math.atan2(edge.z-base.z,edge.y-base.y)),
              deck_transverse_crown_m=dc.z-(dl.z+dr.z)/2,plan_sweep_at_850mm_m=bumper.y-end(.850,bumper.z,False).y)
        curves[key]['centerline_samples_m']=[list(p) for p in curve]
    lamps={}
    for ob in obs:
        if not ob.name.startswith(('Headlamp opening','Taillamp opening')):continue
        raw=list(ob['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu=ob['form_columns'];nr=ob['form_rows'];middle=ps[(nr//2)*nu:(nr//2+1)*nu]
        lengths=[(b-a).length for a,b in zip(middle,middle[1:])]
        heights=[(ps[(nr-1)*nu+i]-ps[i]).length for i in range(nu)]
        corner=min(range(nu),key=lambda i:abs(abs(middle[i].x)-.85))
        actual=mesh_tree([ob]);sample_error=max(actual.find_nearest(p)[3] for p in ps)
        if sample_error>1e-6:raise AssertionError(('Aperture guides are not actual mesh points',ob.name,sample_error))
        lamps[ob.name]=dict(max_sample_distance_to_actual_mesh_m=sample_error,surface_centerline_length_m=sum(lengths),max_aperture_height_m=max(heights),
            corner_return_y_m=abs(middle[-1].y-middle[corner].y),surface_centerline_m=[list(p) for p in middle])
    report.update(end_measurements=curves,lamps=lamps,
        overhangs_m=dict(front=wheels['FL'][1]-report['bounds_m']['min'][1],rear=report['bounds_m']['max'][1]-wheels['RL'][1]))
    errors=[]
    if report['quality']=='game' and report['triangles']>55000:errors.append('Form allocation above 55k')
    if abs(wheelbase-S.WHEELBASE)>1e-5:errors.append('Wheelbase')
    if any(abs(tracks[e]-getattr(S,'FRONT_TRACK' if e=='F' else 'REAR_TRACK'))>1e-5 for e in tracks):errors.append('Track')
    if not 20<=profiles[1]['tumblehome_degrees']<=26:errors.append('Tumblehome')
    if any(not .030<=row['tire_to_arch_m']<=.050 for row in arches):errors.append('Arch crown clearance')
    if crown<.003:errors.append('Door crown absent')
    f,r=curves['front'],curves['rear']
    ranges={
      'front bumper height':(f['bumper_leading_m'][2],.45,.55),
      'front rake':(f['upper_face_degrees_from_vertical'],30,45),
      'hood edge setback':(f['hood_edge_setback_m'],.15,.25),
      'hood edge height':(f['hood_edge_m'][2],.72,.80),
      'front chin height':(f['chin_m'][2],.15,.20),
      'front chin tuck':(f['chin_tuck_m'],.10,.15),
      'hood rise':(f['hood_rise_degrees'],8,12),
      'cowl height':(f['cowl_m'][2],.95,1),
      'hood crown':(f['hood_transverse_crown_m'],.02,.04),
      'front plan sweep':(f['plan_sweep_at_850mm_m'],.25,.35),
      'rear plan sweep':(r['plan_sweep_at_850mm_m'],.15,.25),
      'deck edge height':(r['deck_trailing_edge_m'][2],1,1.05),
      'rear upper lean':(r['upper_panel_degrees_from_vertical'],5,15),
      'rear bumper height':(r['bumper_rearmost_m'][2],.55,.65),
      'rear lower tuck':(r['lower_tuck_m'],.15,.20),
      'diffuser height':(r['diffuser_m'][2],.25,.35),
      'deck length':(r['deck_length_m'],.35,.45)}
    for name,values in lamps.items():
        if name.startswith('Headlamp'):
            for label,field,lo,hi in [('length','surface_centerline_length_m',.60,.70),('height','max_aperture_height_m',.12,.18),('return','corner_return_y_m',.20,.30)]:
                ranges[name+' '+label]=(values[field],lo,hi)
    report['numeric_end_requirements']={name:dict(measured=value,minimum=lo,maximum=hi,passed=lo<=value<=hi) for name,(value,lo,hi) in ranges.items()}
    errors += [name+' outside requested range' for name,record in report['numeric_end_requirements'].items() if not record['passed']]
    report.update(passed=not errors,errors=errors)
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['triangles','bounds_m','a_pillar_rake_from_vertical_degrees','door_crown_above_370_820_chord_m','errors']},indent=2))
    if errors:raise AssertionError(errors)
if __name__=='__main__':main()
