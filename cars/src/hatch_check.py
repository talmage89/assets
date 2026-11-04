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
import hatch_spec as S

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
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--diagnostic',action='store_true')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(src));bpy.context.view_layer.update()
 obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')==S.ASSET_SET]
 skins=[o for o in obs if o.get('part_category') in ['body','doors','glass','pillars','fascia']];tree=mesh_tree(skins)
 from hatch_fairness import field
 ray=field(skins)
 def side(y,z):
  result=ray((2,y,z),(-1,0,0))
  if result is None:raise ValueError(('No side sample',y,z))
  return result
 def top(x,y):return tree.ray_cast(Vector((x,y,3)),Vector((0,0,-1)),4)[0]
 def end(x,z,front,which=tree):return which.ray_cast(Vector((x,-4 if front else 4,z)),Vector((0,1 if front else -1,0)),6)[0]
 parts={};categories={};parents={}
 for o in obs:
  o.data.calc_loop_triangles();n=len(o.data.loop_triangles);parts[o.name]=n
  cat=o['part_category'];categories[cat]=categories.get(cat,0)+n;parents[o.parent.name]=parents.get(o.parent.name,0)+n
 wheels={n:list(bpy.data.objects['Wheel_'+n].matrix_world.translation) for n in ['FL','FR','RL','RR']}
 bb=bounds([o for o in obs if o.get('part_category')!='mirrors'])
 report=dict(stage='source form only',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),quality=bpy.context.scene['quality'],
  surface_cage=json.loads(bpy.data.objects[S.NAME]['surface_cage']),triangles=sum(parts.values()),triangles_per_mesh=parts,triangles_per_category=categories,triangles_per_parent=parents,
  materials=sorted({m.name for o in obs for m in o.data.materials if m}),image_textures=len([im for im in bpy.data.images if im.users and im.source=='FILE']),
  bounds_m=bb,full_bounds_m=bounds(obs),wheel_centers_m=wheels,wheelbase_m=wheels['RL'][1]-wheels['FL'][1],tracks_m={e:wheels[e+'R'][0]-wheels[e+'L'][0] for e in ['F','R']},
  overhangs_m=dict(front=wheels['FL'][1]-bb['min'][1],rear=bb['max'][1]-wheels['RL'][1]))
 report['arches']=[]
 for code in wheels:
  tire=bounds([bpy.data.objects['Tire_'+code]]);lip=bounds([bpy.data.objects['Arch flange_'+code]])
  lip_out=max(abs(lip['min'][0]),abs(lip['max'][0]));tire_out=max(abs(tire['min'][0]),abs(tire['max'][0]))
  report['arches'].append(dict(wheel=code,tire_bounds_m=tire,arch_top_m=lip['max'][2],tire_to_arch_m=lip['max'][2]-tire['max'][2],arch_outer_x_m=lip_out,tire_outer_x_m=tire_out,arch_minus_tire_outboard_m=lip_out-tire_out))
 sections=[]
 for name,y in [('front_axle',S.FRONT_AXLE),('mid_front_door',(S.DOOR_FRONT+S.DOOR_SPLIT)/2),('b_pillar',S.DOOR_SPLIT+.035),('mid_rear_door',(S.DOOR_SPLIT+S.DOOR_REAR)/2),('rear_axle',S.REAR_AXLE)]:
  row=dict(name=name,y_m=y,segments_xz_m=plane_cut(skins,y))
  if name=='b_pillar':
   pa,pb=[side(y,z)[0] for z in [1.08,1.32]]
   row.update(tumblehome_degrees=math.degrees(math.atan2(pa.x-pb.x,pb.z-pa.z)),tumblehome_samples_m=[[pa.x,pa.z],[pb.x,pb.z]])
  sections.append(row)
 sections.append(dict(name='centerline',x_m=.001,segments_yz_m=plane_cut(skins,.001,axis=0)));report['sections']=sections
 def center_band(name,z):
  ob=bpy.data.objects[name];t=mesh_tree([ob]);segs=plane_cut([ob],.001,axis=0);ps=[]
  for aa,bb in segs:
   if (aa[1]-z)*(bb[1]-z)<=0 and abs(bb[1]-aa[1])>1e-8:ps.append(aa[0]+(bb[0]-aa[0])*(z-aa[1])/(bb[1]-aa[1]))
  if not ps:raise ValueError(('Glass sample absent',name,z))
  return Vector((.001,min(ps) if name=='Windshield' else max(ps),z))
 wa,wb=[center_band('Windshield',z) for z in [1.04,1.33]]
 ga,gb=[center_band('Backlight',z) for z in [1.12,1.34]]
 hood=points(bpy.data.objects['Hood outer']);roof=points(bpy.data.objects['Roof']);gate=points(bpy.data.objects['Liftgate outer'])
 he=min([q for q in hood if abs(q.x)<.02],key=lambda q:q.y);hc=max([q for q in hood if abs(q.x)<.02],key=lambda q:q.y)
 report.update(a_pillar_rake_from_vertical_degrees=math.degrees(math.atan2(wb.y-wa.y,wb.z-wa.z)),a_pillar_measured_points_m=[list(wa),list(wb)],
  hood_leading_center_m=list(he),roof_peak_m=list(max(roof,key=lambda q:q.z)),gate_upper_center_m=list(max([q for q in gate if abs(q.x)<.05],key=lambda q:q.z)))
 endtree=mesh_tree(skins+[o for o in obs if o.get('part_category')=='openings']);ends={}
 for front in [True,False]:
  curve=[p for i in range(550) if (p:=end(0,.15+.002*i,front,endtree)) is not None]
  bumper=(min if front else max)(curve,key=lambda q:q.y)
  ends['front' if front else 'rear']=dict(bumper_m=list(bumper),centerline_samples_m=[list(p) for p in curve])
 if end(.80,.50,True) is not None:ends['front']['plan_sweep_at_800mm_m']=end(.80,.50,True).y-end(0,.50,True,endtree).y
 if end(.80,.60,False) is not None:ends['rear']['plan_sweep_at_800mm_m']=end(0,.60,False,endtree).y-end(.80,.60,False).y
 ends['front'].update(hood_edge_m=list(he),cowl_m=list(hc),hood_rise_degrees=math.degrees(math.atan2(hc.z-he.z,hc.y-he.y)))
 ends['rear'].update(backlight_rake_from_vertical_degrees=math.degrees(math.atan2(ga.y-gb.y,gb.z-ga.z)),backlight_center_samples_m=[list(ga),list(gb)])
 glass=bpy.data.objects['Backlight'];gps=points(glass)
 gzlo,gzhi=min(p.z for p in gps),max(p.z for p in gps)
 def width_at(z):
  pts=[]
  glass.data.calc_loop_triangles()
  for tri in glass.data.loop_triangles:
   vs=[gps[i] for i in tri.vertices]
   for p,q in zip(vs,vs[1:]+vs[:1]):
    if (p.z-z)*(q.z-z)<0:pts.append(p+(q-p)*((z-p.z)/(q.z-p.z)))
  return max(p.x for p in pts)-min(p.x for p in pts)
 ends['rear']['backlight_widths_m']=dict(top=width_at(gzhi-.035),base=width_at(gzlo+.045),top_sample_z=gzhi-.035,base_sample_z=gzlo+.045)
 shoulder_width=2*side(1.60,1.015)[0].x
 ends['rear']['d_pillar_projected_width_m']=(shoulder_width-ends['rear']['backlight_widths_m']['base'])/2
 sp=bounds([bpy.data.objects['Roof spoiler']]);upper_glass=[p.y for p in gps if p.z>gzhi-.035]
 ends['rear']['spoiler_overhang_m']=sp['max'][1]-sum(upper_glass)/len(upper_glass)
 # Measure the lower stamped panel below the new garnish aperture. A ray at
 # z=.92 can pass through that real opening and hit the opposite end of the car.
 gate_samples=[end(0,z,False) for z in [.72,.84]]
 ends['rear']['lower_gate_rake_degrees']=math.degrees(math.atan2(gate_samples[0].y-gate_samples[1].y,gate_samples[1].z-gate_samples[0].z))
 ends['rear']['lower_gate_samples_m']=[list(q) for q in gate_samples]
 roof_samples=[top(0,y) for y in [.15,1.40]]
 report['roof_run']=dict(samples_m=[list(q) for q in roof_samples],drop_m=roof_samples[0].z-roof_samples[1].z,angle_degrees=math.degrees(math.atan2(roof_samples[0].z-roof_samples[1].z,1.25)))
 report['fender_swell']=[]
 for y,door_y in [(S.FRONT_AXLE,-.335),(S.REAR_AXLE,.755)]:
  rows=[]
  for i in range(101):
   z=.71+i*.002;ah,bh=ray((2,y,z),(-1,0,0)),ray((2,door_y,z),(-1,0,0))
   if ah is not None and bh is not None:
    aa,bb=ah[0],bh[0];rows.append((aa.x-bb.x,z,aa,bb))
  if len(rows)<25:raise ValueError('Insufficient above-arch flare coverage')
  swell,z,a0,b0=max(rows,key=lambda r:r[0])
  report['fender_swell'].append(dict(axle_y_m=y,door_y_m=door_y,z_m=z,swell_m=swell,samples_m=[list(a0),list(b0)],samples=len(rows),method='Peak above-arch outward swell relative to the same-height door surface; scanned z=.71-.91 m'))
 pocket=bpy.data.objects['Plate pocket opening'];raw=list(pocket['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
 ends['rear']['plate_bed_projected_size_m']=[max(p[k] for p in ps)-min(p[k] for p in ps) for k in [0,2]]
 raw=list(pocket['well_mouth_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
 ends['rear']['plate_mouth_projected_size_m']=[max(p[k] for p in ps)-min(p[k] for p in ps) for k in [0,2]]
 report['end_measurements']=ends
 report['mirrors']={o.name:bounds([o]) for o in obs if o.name.startswith('Mirror housing')};report['mirror_span_m']=bounds([o for o in obs if o.get('part_category')=='mirrors'])['size'][0]
 seams={}
 for suffix in ['L','R']:
  fo=bpy.data.objects['Door F_'+suffix];ro=bpy.data.objects['Door R_'+suffix];rt=mesh_tree([ro]);ps=points(fo);yy=max(q.y for q in ps)
  ds=[rt.find_nearest(q)[3] for q in ps if q.y>yy-.00001 and .4<q.z<.82]
  seams[suffix]=dict(samples=len(ds),min_m=min(ds),max_m=max(ds))
 report['door_seams']=seams
 lamps={}
 for o in obs:
  if not o.name.startswith(('Headlamp opening','Taillamp opening')):continue
  raw=list(o['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu,nv=o['form_columns'],o['form_rows'];mid=ps[(nv//2)*nu:(nv//2+1)*nu]
  lamps[o.name]=dict(surface_centerline_length_m=sum((b-a).length for a,b in zip(mid,mid[1:])),max_aperture_height_m=max((ps[(nv-1)*nu+i]-ps[i]).length for i in range(nu)),inner_aperture_height_m=(ps[(nv-1)*nu]-ps[0]).length,outer_minus_inner_height_m=mid[-1].z-mid[0].z,surface_centerline_m=[list(p) for p in mid])
 report['lamps']=lamps
 checks={}
 def check(name,v,lo,hi):checks[name]=dict(measured=v,minimum=lo,maximum=hi,passed=lo<=v<=hi)
 for k,v,target in zip(['width','length','height'],report['bounds_m']['size'],[S.WIDTH,S.LENGTH,S.HEIGHT]):check(k,v,target-.004,target+.004)
 check('game triangles',report['triangles'],0,46000 if report['quality']=='game' else 500000)
 check('windshield rake',report['a_pillar_rake_from_vertical_degrees'],58,62)
 # Round two explicitly permits more rake to follow the matched Corolla rear.
 check('backlight rake',ends['rear']['backlight_rake_from_vertical_degrees'],30,49)
 check('hood leading height',he.z,.70,.78);check('tumblehome',next(s['tumblehome_degrees'] for s in sections if 'tumblehome_degrees' in s),20,25)
 check('front upper leading tangent height',ends['front']['bumper_m'][2],.63,.78)
 check('rear overhang',report['overhangs_m']['rear'],.70,.85)
 for row in report['arches']:check(row['wheel']+' arch gap',row['tire_to_arch_m'],.030,.050)
 for name,row in lamps.items():
  if name.startswith('Headlamp'):
   check(name+' length',row['surface_centerline_length_m'],.50,.70);check(name+' height',row['max_aperture_height_m'],.08,.16)
 report.update(requirements=checks,passed=all(r['passed'] for r in checks.values()),errors=[k for k,r in checks.items() if not r['passed']],
  deferred=['interior','underbody and measured minimum ground clearance','motion sweeps','UV/bake/GLB','paint/wear'])
 Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['triangles','bounds_m','overhangs_m','a_pillar_rake_from_vertical_degrees','errors']},indent=2))
 if not report['passed'] and not a.diagnostic:raise AssertionError(report['errors'])
if __name__=='__main__':main()
