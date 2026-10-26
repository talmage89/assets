"""Measure physical evaluated surfaces, separately from the GLB serializer proof."""
import argparse,json,sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import bpy
from mathutils import Vector
from kit.assembly import distance
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));bpy.context.view_layer.update()
errors=[];measurements={};contacts=[]
def verts(ob):
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();points=[ob.matrix_world@v.co for v in me.vertices];ev.to_mesh_clear();return points

def named(prefix):return next(o for o in bpy.context.scene.objects if o.name.startswith(prefix))
for root_name,prefix in [('Chair','Chair foot'),('Table','Table foot'),('Chaise','Chaise foot'),('Umbrella_Open','Open rubber ground ring'),('Umbrella_Closed','Closed rubber ground ring')]:
 root=bpy.data.objects[root_name];feet=[o for o in root.children_recursive if o.type=='MESH' and o.name.startswith(prefix)]
 minima=[min(v.z for v in verts(o)) for o in feet]
 points=[v for o in feet for v in verts(o) if abs(v.z)<1e-5]
 center=Vector(((min(v.x for v in points)+max(v.x for v in points))/2,(min(v.y for v in points)+max(v.y for v in points))/2,0))
 error=(center-root.matrix_world.translation).length
 measurements[root_name]=dict(feet=len(feet),foot_min_z_m=minima,footprint_origin_error_m=error)
 if max(abs(z) for z in minima)>1e-5 or error>1e-5:errors.append(root_name+' ground/origin error')
# Conservative radial separation: exact 2D edge distance for the polygonal bore,
# less the maximum radius of the actual polygonal shaft. It bounds every angle.
ring=named('Table umbrella insert');root=bpy.data.objects['Table'];pole=named('Open aluminum pole')
rv=[root.matrix_world.inverted()@v for v in verts(ring)]
ring.data.calc_loop_triangles()
def radial_segment(a,b):
 a=Vector((a.x,a.y));b=Vector((b.x,b.y));d=b-a
 t=max(0,min(1,-a.dot(d)/d.length_squared)) if d.length_squared>1e-16 else 0
 return (a+t*d).length
minimum=min(radial_segment(rv[e.vertices[0]],rv[e.vertices[1]]) for e in ring.data.edges)
pr=[bpy.data.objects['Umbrella_Open'].matrix_world.inverted()@v for v in verts(pole)]
maximum=max(math.hypot(v.x,v.y) for v in pr)
# The table and open umbrella origins coincide. Check the real root axes too.
center_offset=(root.matrix_world.translation-bpy.data.objects['Umbrella_Open'].matrix_world.translation).length
clearance=minimum-maximum-center_offset
measurements['umbrella_hole']=dict(minimum_bore_polygon_radius_m=minimum,maximum_pole_radius_m=maximum,axis_offset_m=center_offset,radial_clearance_lower_bound_m=clearance)
if clearance<.006:errors.append('Pole touches table or has less than 6 mm clearance')
pairs=[('Chair seat mounting boss -1','Chair arm and front leg -1',.001),
 ('Chair seat mounting boss 1','Chair sling spline rail 1',.001),
 ('Chair rear leg -1','Chair arm and front leg -1',.001),
 ('Chair foot -1 -0.334','Chair arm and front leg -1',.0001),
 ('Table foot -1 -1','Table leg -1 -1',.0001),
 ('Chaise foot -1 -0.79','Chaise splayed leg -1 -0.79',.0001),
 ('Table drainage slat 01','Table long perimeter extrusion',.001),
 ('Table leg -1 -1','Table cast corner socket -1 -1',.001),
 ('Chaise fixed sling','Chaise seat spline -1',.002),
 ('Chaise hinge chassis bracket 1','Chaise long chassis 1',.001),
 ('Chaise backrest rail 1','Chaise rotating hinge boss 1',.001),
 ('Chaise hinge lock shaft 1','Chaise hinge handwheel 1',.0001),
 ('Chaise fixed hinge quadrant 1','Chaise hinge chassis bracket 1',.0001),
 ('Chaise hinge handwheel 1','Chaise fixed hinge quadrant 1',.0001),
 ('Open aluminum pole','Open socket bottom stop',.0001),
 ('Closed aluminum pole','Closed socket bottom stop',.0001),
 ('Open eight-panel canopy','Open underside rib pocket 0',.003),
 ('Open underside rib pocket 0','Open rib 0',.003),
 ('Open floating wind vent','Open finial',.001),
 ('Closed gathered eight-gore canopy','Closed woven tie band',.003)]
for left,right,limit in pairs:
 d,method=distance(named(left),named(right));contacts.append(dict(parts=[left,right],distance_m=d,method=method,limit_m=limit))
 if d>limit:errors.append(f'Unsupported {left}: {d} m')
from kit.motion import surface,penetration
# Quantify actual cloth silhouette and the vent's open air gap.
cloth=named('Open eight-panel canopy');cv=verts(cloth)
def around(points,angle,minr):
 return [v for v in points if math.hypot(v.x,v.y)>minr and abs(math.atan2(v.y,v.x)-angle)<.003]
tip=max(v.z for v in around(cv,0,1.2));mid=max(v.z for v in around(cv,math.pi/8,1.1))
sag=tip-mid;vent=named('Open floating wind vent');vv=verts(vent);tree=surface(cloth)['tree']
gaps=[]
for v in vv:
 if v.z<2.444 and math.hypot(v.x,v.y)>.265:
  hit=tree.ray_cast(v,Vector((0,0,-1)),.2)
  if hit[0] is not None:gaps.append(v.z-hit[0].z)
measurements['sewn_canopy']=dict(measured_hem_drop_m=sag,vent_gap_min_m=min(gaps),vent_gap_max_m=max(gaps),gap_rays=len(gaps))
if sag<.06 or min(gaps)<.015:errors.append('Canopy scallop/vent construction inadequate')

max_depth=0.0;hits=[]
for ob in bpy.context.scene.objects:
 if ob.type=='MESH' and ob.get('asset_set')=='Table':
  for other in bpy.context.scene.objects:
   if other.type=='MESH' and other.get('asset_set')=='Umbrella_Open':
    depth,crossings=penetration(surface(ob),surface(other),.0005)
    max_depth=max(max_depth,depth)
    if depth>.0005:hits.append(dict(table=ob.name,umbrella=other.name,depth_m=depth))
measurements['table_umbrella']=dict(max_penetration_m=max_depth,violations=hits)
if hits:errors.append('Table/umbrella interference')
# Independent per-module counts, with moving objects included by asset_set.
counts={}
for ob in bpy.context.scene.objects:
 if ob.type=='MESH' and 'asset_set' in ob:
  ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();counts[ob['asset_set']]=counts.get(ob['asset_set'],0)+len(me.loop_triangles);ev.to_mesh_clear()
measurements['module_triangles']=counts
if bpy.context.scene.get('quality')=='game':
 for name,(lo,hi) in {'Chair':(1000,3000),'Table':(1500,4000),'Chaise':(2000,4000),'Umbrella_Open':(2000,4000),'Umbrella_Closed':(2000,4000)}.items():
  if not lo<=counts[name]<=hi:errors.append(f'{name} triangles {counts[name]} outside {lo}–{hi}')
report=dict(passed=not errors,source=a.source,scope='physical evaluated rest surfaces; GLB preservation is checked separately',measurements=measurements,contacts=contacts,errors=errors)
Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if errors:raise RuntimeError('Construction check failed')
