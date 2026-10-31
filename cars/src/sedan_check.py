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
def plane_cut(obs,y):
    result=[]
    for ob in obs:
        ps=points(ob);ob.data.calc_loop_triangles()
        for tri in ob.data.loop_triangles:
            hits=[];vs=[ps[i] for i in tri.vertices]
            for a,b in zip(vs,vs[1:]+vs[:1]):
                if (a.y-y)*(b.y-y)<0:
                    p=a+(b-a)*((y-a.y)/(b.y-a.y));hits.append([p.x,p.z])
            if len(hits)==2:result.append(hits)
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
    pillar=points(bpy.data.objects['Greenhouse_R']);low=min(pillar,key=lambda p:abs(p.z-.99)+abs(p.y+.93));high=min(pillar,key=lambda p:abs(p.z-1.38)+abs(p.y+.20))
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
    errors=[]
    if report['quality']=='game' and report['triangles']>55000:errors.append('Form allocation above 55k')
    if abs(wheelbase-S.WHEELBASE)>1e-5:errors.append('Wheelbase')
    if any(abs(tracks[e]-getattr(S,'FRONT_TRACK' if e=='F' else 'REAR_TRACK'))>1e-5 for e in tracks):errors.append('Track')
    if not 20<=profiles[1]['tumblehome_degrees']<=26:errors.append('Tumblehome')
    if any(not .030<=row['tire_to_arch_m']<=.050 for row in arches):errors.append('Arch crown clearance')
    if crown<.003:errors.append('Door crown absent')
    report.update(passed=not errors,errors=errors)
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['triangles','bounds_m','a_pillar_rake_from_vertical_degrees','door_crown_above_370_820_chord_m','errors']},indent=2))
    if errors:raise AssertionError(errors)
if __name__=='__main__':main()
