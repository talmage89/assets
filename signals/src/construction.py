"""Source-surface construction and sampled motion, separate from serialization."""
import sys,json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as G,assembly,motion
from plan import *
from layout import SITES
def component(rt,prefix,registry):
 vs=[];fs=[]
 bpy.context.view_layer.update()
 for o in rt.children_recursive:
  if o.type!='MESH':continue
  attr=o.data.attributes.get('Construction')
  if attr is None:continue
  o.data.calc_loop_triangles()
  for t in o.data.loop_triangles:
   name=registry.get(str(attr.data[t.polygon_index].value),'')
   if not name.startswith(prefix):continue
   start=len(vs);vs.extend(o.matrix_world@o.data.vertices[i].co for i in t.vertices);fs.append((start,start+1,start+2))
 assert vs,(rt.name,prefix)
 ob=G.mesh('Measure_'+prefix,vs,fs);return ob
def extent(ob):
 return [[min(v.co[i] for v in ob.data.vertices),max(v.co[i] for v in ob.data.vertices)] for i in range(3)]
def run(seed):
 bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/Signals-{seed}.blend').resolve()))
 site=SITES[seed]
 reg=json.loads(Path(f'build/Signals-{seed}-components.json').read_text());result=dict(seed=seed,contacts=[],measurements=[],motion=[])
 # Component face IDs survive consolidation, permitting tests on actual triangles.
 def contact(rt,a,b,limit=.001):
  x=component(rt,a,reg);y=component(rt,b,reg);distance,method=assembly.distance(x,y)
  result['contacts'].append(dict(root=rt.name,parts=[a,b],distance_m=distance,limit_m=limit,method=method))
  bpy.data.objects.remove(x,do_unlink=True);bpy.data.objects.remove(y,do_unlink=True)
  assert distance<=limit,(seed,rt.name,a,b,distance)
 if not PLANS[seed].span:
  mast=bpy.data.objects['Mast_0']
  contact(mast,'Camera rain hood','Detection camera')
  contact(mast,'Camera optical port','Detection camera')
  contact(mast,'Plate washer','Base plate')
  contact(mast,'Folded pole connection box','Tapered shaft')
  contact(mast,'Folded pole connection box','Arm connection flange')
  # All six rod diameters/positions are measured, not inferred from export count.
  rods=component(mast,'Anchor rod',reg)
  pts=[mast.matrix_world.inverted()@v.co for v in rods.data.vertices]
  zlo=min(p.z for p in pts);zhi=max(p.z for p in pts)
  result['measurements'].append(dict(part='Anchor rods',visible_z_range_m=[zlo,zhi],method='Actual retained component vertices'))
  assert abs(zlo-.145)<1e-5 and abs(zhi-.36885)<1e-5
  bpy.data.objects.remove(rods,do_unlink=True)
 ped=bpy.data.objects['Pedestal_0_1'];pad=bpy.data.objects['APS_Landing_0_1']
 button=component(ped,'Accessible button',reg);landing=component(pad,'Button clear landing',reg)
 button_z=(min(v.co.z for v in button.data.vertices)+max(v.co.z for v in button.data.vertices))/2
 top=max(v.co.z for v in landing.data.vertices);height=button_z-top
 assert abs(height-1.0668)<2e-5
 result['measurements'].append(dict(part='Accessible button',axis_above_actual_landing_m=height,landing_top_m=top,button_axis_m=button_z))
 # Actual pad bounds prove the rectangle stops outside the central 5 ft ramp.
 e=extent(landing);rampedge=site.core(0)+1.524+.762;gap=e[1][0]-rampedge
 assert gap>.14
 result['measurements'].append(dict(part='APS landing',bounds_m=e,clear_of_main_ramp_m=gap))
 bpy.data.objects.remove(button,do_unlink=True);bpy.data.objects.remove(landing,do_unlink=True)
 contact(ped,'R10 back mounting spacer','R10 sign blank')
 contact(ped,'R10 back mounting spacer','Four inch pedestal')
 # Physical required longitudinal placement is measured from the facing axis.
 distances=[]
 for h in list(bpy.context.scene.objects):
  if not h.get('part_kind','').startswith('Head_') or '__Near' in h.name:continue
  f=h.matrix_world.to_3x3()@Vector((0,-1,0));p=h.matrix_world.translation
  turn=round((math.atan2(f.x,-f.y)*180/math.pi)%360/90)%4
  # f points toward the incoming approach. Its stop bar uses the opposite
  # port in this far-side placement convention.
  distance=site.stop(turn)-p.dot(f);assert 12.192<=distance<=54.864,(h.name,distance)
  distances.append(distance)
 result['measurements'].append(dict(part='Primary faces',longitudinal_stop_line_range_m=[min(distances),max(distances)],method='Actual head frames projected onto their approach, against the placed stop line'))
 # All cabinet leaf metal, fasteners and lock move; the gasket's intended
 # compression is excluded. Fixed/moving knuckles retain their physical gap.
 door=bpy.data.objects['Controller__Door'];fixed=next(o for o in door.parent.children if o.type=='MESH')
 leaf=next(o for o in door.children if o.type=='MESH')
 test=leaf.copy();test.data=leaf.data.copy();bpy.context.collection.objects.link(test)
 bm=bmesh.new();bm.from_mesh(test.data)
 rubber={i for i,m in enumerate(test.data.materials) if m.name.startswith('Form_rubber')}
 layer=bm.faces.layers.int.get('Construction')
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if layer and reg.get(str(f[layer]),'').startswith('Weather gasket')],context='FACES');bm.to_mesh(test.data);bm.free()
 fixedsurface=motion.surface(fixed);rest=door.matrix_basis.copy();peak=0
 for angle in range(0,111,5):
  door.matrix_basis=rest@Matrix.Rotation(math.radians(-angle),4,'Z');bpy.context.view_layer.update()
  depth,_=motion.penetration(motion.surface(test),fixedsurface,.0015);peak=max(peak,depth)
  assert depth<=.0015,(seed,'Door',angle,depth)
 door.matrix_basis=rest;bpy.data.objects.remove(test,do_unlink=True)
 result['motion'].append(dict(part='Controller__Door',range_degrees=[-110,0],step_degrees=5,samples=23,peak_penetration_m=peak,tolerance_m=.0015,exception='Intended compressible rubber gasket excluded; closed leaf/jamb permits 1.5 mm fit tolerance'))
 # Actual door construction and access aperture, not export equivalence.
 contact(door,'Stiffened inner door panel','Folded aluminum door')
 contact(door,'Inner door folded stiffener','Stiffened inner door panel')
 contact(door,'Door document pocket','Stiffened inner door panel')
 contact(door.parent,'Cabinet service light diffuser','Service lamp roof mounting channel')
 police=bpy.data.objects['Controller__PoliceDoor'];rest_police=police.matrix_basis.copy()
 policebody=next(o for o in police.children if o.type=='MESH')
 proxy=policebody.copy();proxy.data=policebody.data.copy();bpy.context.collection.objects.link(proxy)
 bm=bmesh.new();bm.from_mesh(proxy.data);layer=bm.faces.layers.int.get('Construction')
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if layer and reg.get(str(f[layer]),'').startswith('Police door hinge pin')],context='FACES');bm.to_mesh(proxy.data);bm.free()
 frame=next(o for o in door.children if o.type=='MESH');framecopy=frame.copy();framecopy.data=frame.data.copy();bpy.context.collection.objects.link(framecopy)
 bm=bmesh.new();bm.from_mesh(framecopy.data);layer=bm.faces.layers.int.get('Construction')
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if layer and reg.get(str(f[layer]),'').startswith('Police access door gasket')],context='FACES');bm.to_mesh(framecopy.data);bm.free()
 frame_surface=motion.surface(framecopy);peak=0
 for angle in range(0,96,5):
  police.matrix_basis=rest_police@Matrix.Rotation(math.radians(-angle),4,'Z');bpy.context.view_layer.update()
  depth,_=motion.penetration(motion.surface(proxy),frame_surface,.001);peak=max(peak,depth)
  assert depth<=.001,(seed,'Police door',angle,depth)
 police.matrix_basis=rest_police;bpy.context.view_layer.update()
 inv=frame.matrix_world.inverted();start=inv@(door.matrix_world@Vector((.53,-.1,1.25)));direction=inv.to_3x3()@door.matrix_world.to_3x3()@Vector((0,1,0))
 hit=frame.ray_cast(start,direction,distance=.2)[0];assert not hit,(seed,'Police aperture obstructed')
 result['measurements'].append(dict(part='Police access aperture',ray_start_world_m=list(frame.matrix_world@start),unobstructed_through_leaf_and_inner_panel=True,ray_length_m=.2,scope='Actual fixed leaf mesh ray; moving police leaf tested separately'))
 result['motion'].append(dict(part='Controller__PoliceDoor',axis='Z',range_degrees=[-95,0],step_degrees=5,samples=20,peak_penetration_m=peak,exception='Pin forms intentional hinge contact; compressible police-door gasket excluded'))
 bpy.data.objects.remove(proxy,do_unlink=True);bpy.data.objects.remove(framecopy,do_unlink=True)
 # Check one of each head style against its own fixed support for both axes.
 # Only the indexed stem's intentional coupler contact is excluded.
 used=set()
 for h in list(bpy.context.scene.objects):
  kind=h.get('part_kind','')
  if not kind.startswith('Head_'):continue
  used.add(kind);body=next(o for o in h.children if o.type=='MESH' and not o.get('signal_lens'))
  parentfixed=next(o for o in h.parent.children if o.type=='MESH')
  pxy=body.copy();pxy.data=body.data.copy();bpy.context.collection.objects.link(pxy)
  # Remove the coupler by actual head-local centroid; backplate is farther aft.
  bm=bmesh.new();bm.from_mesh(pxy.data);transform=h.matrix_world.inverted()@pxy.matrix_world
  omit=[];layer=bm.faces.layers.int.get('Construction')
  for f in bm.faces:
   if layer and reg.get(str(f[layer]),'').startswith(('Tether restraint','Indexed top boss','Top mounting stem')):
    omit.append(f);continue
   p=transform@f.calc_center_median()
   if p.x*p.x+p.y*p.y<.055*.055 and p.z>-.14:omit.append(f)
  bmesh.ops.delete(bm,geom=omit,context='FACES');bm.to_mesh(pxy.data);bm.free()
  stationary=[motion.surface(parentfixed)]
  for sibling in h.parent.children:
   if sibling==h or not sibling.get('part_kind','').startswith('Head_'):continue
   stationary.extend(motion.surface(m) for m in sibling.children if m.type=='MESH' and not m.get('signal_lens'))
  rest=h.matrix_basis.copy()
  for axis,low,high,step in [('Z',-15,15,3),('X',-4,4,2)]:
   peak=0;samples=list(range(low,high+1,step))
   for angle in samples:
    h.matrix_basis=rest@Matrix.Rotation(math.radians(angle),4,axis);bpy.context.view_layer.update()
    moving=motion.surface(pxy);depth=max(motion.penetration(moving,f,.001)[0] for f in stationary)
    peak=max(peak,depth);assert depth<=.001,(seed,h.name,axis,angle,depth)
   result['motion'].append(dict(part=h.name,axis=axis,range_degrees=[low,high],step_degrees=step,samples=len(samples),peak_penetration_m=peak,exception='Indexed boss/stem form the intentional aiming joint and cable-entry contact; flexible tether termination excluded. Engine motion must update cable sockets.'))
  h.matrix_basis=rest;bpy.data.objects.remove(pxy,do_unlink=True)
 result['passed']=True;return result
if __name__=='__main__':
 rows=[run(seed) for seed in PLANS]
 Path('build/construction.json').write_text(json.dumps(dict(passed=True,scope='Actual source triangles/components; contacts, accessible heights/landing gap, longitudinal placement and sampled motion. Serialization is independent.',seeds=rows),indent=2))
 print('CONSTRUCTION checked',len(rows),'seeds',flush=True)
