"""Physical source measurements and independent raw-GLB/fresh-import audit.

This gate deliberately does not certify final UV density, material count, bake
fidelity, wear or a finished game package. Quick palettes and text sheets remain.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy,numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
from kit.gltf import GLB
from kit.motion import sweep
from plan import PROOF_SEEDS,rotate


def meshes_under(node):
 def owned(o):
  while o:
   if o==node:return True
   o=o.parent
  return False
 return [o for o in bpy.context.scene.objects if o.type=='MESH' and owned(o)]


def surface(obs):
 vs=[];fs=[]
 for ob in obs:
  off=len(vs);vs.extend(ob.matrix_world@v.co for v in ob.data.vertices);ob.data.calc_loop_triangles()
  fs.extend(tuple(i+off for i in t.vertices) for t in ob.data.loop_triangles)
 return BVHTree.FromPolygons(vs,fs,all_triangles=True)


def ray(tree,origin,direction,length=100):
 hit=tree.ray_cast(Vector(origin),Vector(direction),length)
 if hit[0] is None:raise AssertionError('Missing surface at '+repr(origin))
 return list(hit[0])


def points(obs):return np.array([tuple(o.matrix_world@v.co) for o in obs for v in o.data.vertices])


def run(seed,motions=False):
 source=Path(f'build/station-{seed}.blend');p=json.loads(source.with_suffix('.json').read_text())
 bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update();obs=[o for o in bpy.context.scene.objects if o.type=='MESH'];srcpoints=points(obs)
 assert sum(len(o.data.polygons) for o in obs)==p['total_triangles'],'Source count'
 tiny=sum(t.area<1e-12 for o in obs for t in o.data.loop_triangles)
 assert tiny==0,f'{tiny} degenerate source triangles'
 tree=surface(obs);b=p['building'];c=p['canopy'];store=bpy.data.objects['Store'];roof=surface(meshes_under(store))
 # Actual roof/parapet rays are measured in the store's local construction frame.
 inv=store.matrix_world.inverted()
 def sr(local,direction):
  a=store.matrix_world@Vector(local);vec=store.matrix_world.to_3x3()@Vector(direction)
  return list(inv@Vector(ray(roof,a,vec)))
 roof_samples=[]
 for x in (-b['width']*.38,0,b['width']*.38):
  for offset in (.5,1.0,1.5):
   # Keep the independent membrane samples clear of rooftop equipment.
   roof_samples.append(sr((x,-b['depth']/2+offset,10),(0,0,-1))[2])
 assert max(abs(v-(b['roof']+.0225)) for v in roof_samples)<2e-5,'Roof membrane height'
 cap=sr((0,-b['depth']/2,10),(0,0,-1))[2]
 # Top-down canopy clearance probe away from columns, lights and seams.
 can=bpy.data.objects['Canopy'];ctree=surface(meshes_under(can));ci=can.matrix_world.inverted()
 pos=can.matrix_world@Vector((c['pitch']*.34,-1.12,0));vec=can.matrix_world.to_3x3()@Vector((0,0,1))
 hit=ci@Vector(ray(ctree,pos,vec));clear=float(hit.z)
 assert abs(clear-c['clear'])<2e-5,(clear,c['clear'])
 fascia_top=float((ci@Vector(ray(ctree,can.matrix_world@Vector((c['width']/2-.025,0,10)),can.matrix_world.to_3x3()@Vector((0,0,-1))))).z)
 island_measurements=[]
 for i in range(c['count']):
  xx=(i-(c['count']-1)/2)*c['pitch']
  def cr(origin,direction):return ci@Vector(ray(ctree,can.matrix_world@Vector(origin),can.matrix_world.to_3x3()@Vector(direction)))
  left=cr((xx-2,0,.09),(1,0,0)).x;right=cr((xx+2,0,.09),(-1,0,0)).x
  front=cr((xx,-4,.09),(0,1,0)).y;back=cr((xx,4,.09),(0,-1,0)).y
  top=cr((xx,0,.24),(0,0,-1)).z
  assert abs(right-left-c['island'][0])<2e-5 and abs(back-front-c['island'][1])<2e-5,'Actual island circulation envelope'
  island_measurements.append(dict(width_m=right-left,length_m=back-front,top_m=top))
 hose_rows=[]
 for hose in p.get('hoses',[]):
  # Nearest actual source triangle distances at three curve ring centers.
  ds=[tree.find_nearest(Vector(hose['centerline_m'][i]))[3] for i in (7,12,18)]
  hose_rows.append(dict(name=hose['name'],sampled_inscribed_radii_m=ds,minimum_center_height_m=min(v[2] for v in hose['centerline_m'])))
  assert max(ds)<.016 and min(ds)>.011,'Hose wall thickness/surface'
 srcnodes={o.name:np.array(o.matrix_world).tolist() for o in bpy.context.scene.objects if o.get('socket_kind') or o.get('pivot_axis') or o.get('detachable')}
 source_mats=len({m.name for o in obs for m in o.data.materials})
 static_store=surface([bpy.data.objects['Store__Mesh']])
 for zz in (.7,1.5):
  start=store.matrix_world@Vector((0,-b['depth']/2-.4,zz));direction=store.matrix_world.to_3x3()@Vector((0,1,0))
  assert static_store.ray_cast(start,direction,.70)[0] is None,'Entry is blocked by fixed construction'
 # Physical leaf sweeps use actual source triangles, distinct from serialization.
 motion=None
 if motions:
  specs=[]
  for ob in bpy.context.scene.objects:
   if ob.get('pivot_axis'):
    limits=list(ob['range_degrees']);specs.append(dict(node=ob.name,axis=ob['pivot_axis'],range=limits,step=5,tolerance_m=.001))
  motion=sweep(dict(MOTIONS=specs))
  Path(f'build/motion-{seed}.json').write_text(json.dumps(motion,indent=2))
  assert motion['passed'],'Actual leaf sweep failed'
 from check_ground import audit as ground_audit
 paving=surface([bpy.data.objects['SitePaving__Mesh']]);station=bpy.data.objects['Station_'+str(seed)].matrix_world.copy();si=station.inverted()
 ground=ground_audit(p,paving,station)
 # Actual ramp and top landing, not a nominal accessible-stall label.
 access=p['access'];start=b['front']-p['walk'];ramp=[];landing=[]
 def paving_z(x,y):
  return float((si@Vector(ray(paving,station@Vector((x,y,2)),station.to_3x3()@Vector((0,0,-1))))).z)
 for t in (.1,.5,.9):
  z=paving_z(access['center_x'],start+access['run']*t);ramp.append(z)
  assert abs(z-.1524*t)<2e-5,'Ramp surface does not follow its 1:12 run'
 for t in (.1,.5,.9):
  z=paving_z(access['center_x'],start+access['run']+access['landing_depth']*t);landing.append(z)
  assert abs(z-.1524)<2e-5,'Top landing is not level'
 access_measurement=dict(ramp_height_samples_m=ramp,level_landing_height_samples_m=landing,scope='Source ray heights along the actual ramp and level top landing; width/run are authored plan dimensions, not a permit audit.')
 # Raw glTF geometry does not depend on Blender's importer.
 g=GLB(source.with_suffix('.glb'));raw_tri=0;normal_error=0;degenerate_uv=0
 for me in g.json['meshes']:
  for pr in me['primitives']:
   raw_tri+=len(g.accessor(pr['indices']))//3
   n=g.accessor(pr['attributes']['NORMAL']);normal_error=max(normal_error,float(np.max(abs(np.linalg.norm(n,axis=1)-1))))
 assert raw_tri==p['total_triangles'],(raw_tri,p['total_triangles'])
 assert normal_error<1e-5,'Non-unit raw normals'
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.with_suffix('.glb').resolve()));bpy.context.view_layer.update()
 imported=[o for o in bpy.context.scene.objects if o.type=='MESH'];pp=points(imported)
 kd=KDTree(len(pp))
 for i,v in enumerate(pp):kd.insert(v,i)
 kd.balance();maxerr=max(kd.find(v)[2] for v in srcpoints)
 assert maxerr<2e-5,'GLB changed source surface'
 node_error=0
 for name,frame in srcnodes.items():
  ob=bpy.data.objects.get(name);assert ob is not None,'Missing pivot/socket '+name
  node_error=max(node_error,float(np.max(abs(np.array(ob.matrix_world)-frame))))
 assert node_error<1e-5,'Pivot/socket frame import error'
 counts=p['triangles'];assert counts['Store']<=45000 and counts['Canopy']<=18000
 assert all(v<=6000 for k,v in counts.items() if k.startswith('Dispenser_'))
 assert counts['PriceSign']<=5000
 result=dict(seed=seed,passed=True,source_triangle_count=p['total_triangles'],raw_glb_triangle_count=raw_tri,materials_quick=source_mats,raw_glb_materials=len(g.json['materials']),
  roof_height_samples_m=roof_samples,parapet_cap_top_m=cap,actual_canopy_clearance_m=clear,actual_islands=island_measurements,
  fascia_top_m=fascia_top,hoses=hose_rows,normal_unit_max_error=normal_error,
  import_position_max_error_m=maxerr,pivot_socket_matrix_max_error=node_error,motion=motion,
  ground_interface=ground,accessible_approach=access_measurement,scope='source surface/ray and sampled motion construction proof; separate raw/accessor/import serialization proof. No final UV/bake certification.')
 return result

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)));a.add_argument('--motion',action='store_true');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
 rows=[]
 for s in map(int,a.seeds.split(',')):
  row=run(s,a.motion);rows.append(row);print('CHECK',s,row['passed'],row['source_triangle_count'],'triangles',row['import_position_max_error_m'],'m import error',flush=True)
 Path('build/checks.json').write_text(json.dumps(rows,indent=2))
