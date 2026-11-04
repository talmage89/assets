"""Measured rigid sweeps using kit.motion solids, including telescoping supports.

Concealed reverse faces are reconstructed at the declared physical gauge for
collision queries only. These faces are not added to the delivery budget.
Labels are open print surfaces; all load-bearing sheets are measured as solids.
"""
import argparse,json,math,sys,hashlib
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.motion import surface,penetration,owned
from kit import model as G
from suv_mechanics import update_supports


def collision_gauges():
 result={}
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH' or not ob.get('collision_gauge_m'):continue
  old=ob.data;role=old.attributes['skin_face_role']
  faces=[tuple(f.vertices) for f in old.polygons if role.data[f.index].value==0]
  me=bpy.data.meshes.new(ob.name+' collision gauge');me.from_pydata([v.co for v in old.vertices],[],faces);me.update();ob.data=me
  sol=ob.modifiers.new('Physical gauge for collision only','SOLIDIFY');sol.thickness=ob['collision_gauge_m'];sol.offset=-1;sol.use_even_offset=True;G.apply(ob)
  bm=bmesh.new();bm.from_mesh(ob.data);nonmanifold=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free()
  if nonmanifold or volume<=0:raise ValueError(('Invalid reconstructed collision gauge',ob.name,nonmanifold,volume))
  ob['allow_boundary']=False;result[ob.name]=dict(gauge_m=ob['collision_gauge_m'],source_exterior_faces=len(faces),nonmanifold_edges=nonmanifold,volume_m3=volume)
 return result


def motions(coarse=False):
 rows=[]
 for side,sgn in [('L',1),('R',-1)]:
  for end in ['F','R']:rows.append(dict(node='Door_'+end+side,axis='Z',range=[0,60*sgn],step=30 if coarse else 2))
 for n,angle in [('Hood',-65),('Liftgate',75)]:rows.append(dict(node=n,axis='X',range=[0,angle],step=abs(angle)/2 if coarse else 2))
 for n in ['FL','FR','RL','RR']:rows.append(dict(node='Wheel_'+n,axis='X',range=[0,360],step=90 if coarse else 15))
 for n in ['FL','FR']:rows.append(dict(node='Steer_'+n,axis='Z',range=[-35,35],step=35 if coarse else 2))
 rows.append(dict(node='FuelDoor',axis='Z',range=[0,85],step=42.5 if coarse else 2))
 for row in rows:
  name=row['node'];row['allow']=[]
  if name in ['Hood','Liftgate']:
   for sign in [-1,1]:
    label=('Hood' if name=='Hood' else 'Gate')+' strut '+str(sign)
    row['allow'].append(dict(moving=label+' barrel',fixed=label+' body ball seat',reason='Strut barrel eye articulates on its fixed ball stud'))
  if name=='Liftgate':
   for sign in [-1,1]:row['allow'].append(dict(moving='Gate strut '+str(sign)+' barrel',fixed='Gate strut body return '+str(sign),reason='Fixed strut ball stud and its steel body return share the barrel eye seat'))
  if name.startswith('Steer_'):
   sign=-1 if name.endswith('L') else 1
   for fixed,reason in [('Control arm ','Knuckle ball joint at the control-arm end'),('Halfshaft ','Outer CV joint inside the hub spindle')]:row['allow'].append(dict(moving='Hub spindle F'+str(sign),fixed=fixed+'F'+str(sign),reason=reason))
 return rows


def run(config):
 gauges=collision_gauges();meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o and not o.get('allow_boundary',False)]
 result=dict(passed=True,method='kit.motion evaluated BVH crossings, solid parity and edge-interval penetration; dynamic support endpoints evaluated at every pose',units='meters',collision_gauges=gauges,motions=[])
 for spec in config:
  allowed=set()
  pivot=bpy.data.objects[spec['node']];rest=pivot.matrix_basis.copy()
  moving=[o for o in meshes if owned(o,pivot) or o.get('support_pivot')==pivot.name]
  fixed=[o for o in meshes if o not in moving];stationary={o.name:surface(o) for o in fixed}
  lo,hi=spec['range'];count=math.ceil(abs(hi-lo)/spec['step']);samples=[lo+(hi-lo)*i/count for i in range(count+1)]
  tolerance=.0005;violations={};maximum=0.;support_lengths={}
  for value in samples:
   pivot.matrix_basis=rest@Matrix.Rotation(math.radians(value),4,spec['axis']);bpy.context.view_layer.update();update_supports()
   for ob in moving:
    current=surface(ob)
    if ob.get('support_kind')=='barrel':
     d=(pivot.matrix_world@Vector(ob['support_moving_local'])-Vector(ob['support_fixed'])).length
     old=support_lengths.setdefault(ob.name,[d,d]);old[0]=min(old[0],d);old[1]=max(old[1],d)
    for fixed_ob in fixed:
     # Only explicit ball-joint contact is expected; collars must still clear
     # the body, adjacent moving panel, glass, roof and spoiler independently.
     contact=next((r for r in spec.get('allow',[]) if ob.name==r['moving'] and fixed_ob.name==r['fixed']),None)
     if contact:
      allowed.add((contact['moving'],contact['fixed'],contact['reason']));continue
     depth,crossings=penetration(current,stationary[fixed_ob.name],tolerance);maximum=max(maximum,depth)
     if depth>tolerance:
      key=(ob.name,fixed_ob.name)
      if key not in violations or depth>violations[key]['depth_m']:violations[key]=dict(moving=ob.name,fixed=fixed_ob.name,angle_degrees=value,depth_m=depth,triangle_crossings=crossings)
   print('POSE',pivot.name,value,len(violations),flush=True)
  pivot.matrix_basis=rest;bpy.context.view_layer.update();update_supports()
  row=dict(spec,samples=len(samples),sampled_angles_degrees=samples,tolerance_m=tolerance,max_penetration_m=maximum,support_attachment_distances_m=support_lengths,allowed_contacts=[dict(moving=x,fixed=y,reason=z) for x,y,z in sorted(allowed)],violations=list(violations.values()))
  result['motions'].append(row);result['passed'] &= not bool(violations)
  print('SUV_MOTION',pivot.name,maximum,len(violations),flush=True)
 return result


def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--coarse',action='store_true');p.add_argument('--nodes');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));rows=motions(a.coarse)
 if a.nodes:rows=[r for r in rows if r['node'] in a.nodes.split(',')]
 result=run(rows);result['source_sha256']=hashlib.sha256(Path(a.source).read_bytes()).hexdigest();result['quality']=bpy.context.scene['quality'];Path(a.out).write_text(json.dumps(result,indent=2))
 if not result['passed']:raise RuntimeError('SUV articulation requires correction: '+a.out)
if __name__=='__main__':main()
