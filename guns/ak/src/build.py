"""Clean-scene scripted checkpoint, rig and five inspection exports."""
import argparse,hashlib,json,sys,subprocess
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as M,weapon as W
import geometry as G,interface
from clips import build_clips
HEADS={'Root':(0,0,0),'BoltCarrier':(0,170,93),'Bolt':(0,170,85),
 'ChargingHandle':(20,164,91),'Selector':(0,5,69),'Trigger':(0,49,53),
 'Hammer':(0,70,56),'Magazine':(0,166,67),'MagRelease':(0,84,41),'MagCatch':(0,93,41),
 'Follower':(0,130,52),'TopRound':(5.15,103,70),
 'SecondRound':(-5.15,103,64.4),'ThirdRound':(5.15,104,58.8),
 'ChamberRound':(0,170,85),'CaseTravel':(0,126,85),'EjectedCase':(0,126,85)}
PARENTS={**{n:'Magazine' for n in ('Follower','TopRound','SecondRound','ThirdRound')},
 'ChargingHandle':'BoltCarrier','Bolt':'BoltCarrier','EjectedCase':'CaseTravel'}
SOCKETS={'Socket_Muzzle':(0,595,85),'Socket_Foregrip':(-20,296,64),
 'Socket_Butt':(0,-285,35),'Socket_Eye':(0,-107,128),
 'Socket_Ejection':(19,126,94),'Socket_MagWell':(0,135,40),
 'Socket_Magazine':HEADS['Magazine'],'Socket_ChargingHandle':(32,164,91)}
def finish(ob):
 # Tiny numeric welds only; no topology repair concealed in the audit.
 if not ob.name.endswith('_Sculpt'):
  bm=bmesh.new();bm.from_mesh(ob.data)
  bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.001)
  bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.001)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
  if ob.name=='Receiver_Sheet':
   bm=bmesh.new();bm.from_mesh(ob.data)
   bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001)
   bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.0001)
   edges=[e for e in bm.edges if e.is_boundary]
   if edges:
    assert sum(e.calc_length() for e in edges)<.15,'Unexpected receiver boundary'
    bmesh.ops.holes_fill(bm,edges=edges,sides=0)
   bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
 t=ob.modifiers.new('Checkpoint triangles','TRIANGULATE');t.keep_custom_normals=True;M.apply(ob)
 ns=[n.vector.copy() for n in ob.data.corner_normals]
 for f in ob.data.polygons:
  for j in f.loop_indices:
   if ns[j].dot(f.normal)<.08:ns[j]=f.normal.copy()
   if ob.name=='TopCover_RearCap' and abs(f.normal.y)>.7:ns[j]=f.normal.copy()
 ob.data.normals_split_custom_set(ns)
 if 'Handguard_Sculpt' in ob.name:G.hand_normals(ob)
 ob.data.transform(Matrix.Scale(.001,4));ob.matrix_world=Matrix.Identity(4)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/ak.blend');p.add_argument('--preview',action='store_true')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.read_factory_settings(use_empty=True);G.palette()
 for f in (G.receiver,G.cover,G.furniture,G.guard_controls,G.action_barrel,G.sights,G.magazine,G.receiver_sources,G.visible_seating):f()
 for ob in [*G.PARTS,*G.HIGH]:
  if ob.name.startswith('Trigger_'):ob.data.transform(Matrix.Translation((0,20,0)))
  if ob.name.startswith('Hammer_'):ob.data.transform(Matrix.Translation((0,15,4)))
  if ob.name.removeprefix('HIGH_')=='PistolGrip_Sculpt' or ob.name.startswith('HIGH_GripStrap'):
   for v in ob.data.vertices:v.co.z=52+(v.co.z-40)*.85
  if ob.name.startswith(('Trigger_','TriggerGuard_','Guard_','Release_Housing','MagRelease_','Magazine_RearCatch','Grip_HeelScrew')):
   if ob.name=='Grip_HeelScrew':
    for v in ob.data.vertices:v.co.z=52+(v.co.z-40)*.85
   else:ob.data.transform(Matrix.Translation((0,0,8)))
 # Flat sheet lands and covered representations do not warrant dense triangles.
 # The first-person sight and control silhouettes retain their full allocation.
 for name,target in [('Receiver_Sheet',1900),('Stock_Sculpt',3000),('TopCover_Pressed',2600),('TopCover_RearCap',180),('Barrel',700),
  ('LowerHandguard_Sculpt',2400),('UpperHandguard_Sculpt',1700),('PistolGrip_Sculpt',2200),
  ('Magazine_Sheet',2700),('TriggerGuard_Stamping',450),('Buttplate',380),
  ('Handguard_Retainer221',230),('Handguard_Retainer363',230),('Release_Housing',280),
  ('Sight_FrontHood',800),('TopCover_ButtonLip',220),('Sight_WindageDrum',360),
  ('Sight_RearNotch',240),('Sight_LeafSpring',180),('Sight_TangentLeaf',280),
  ('Sight_SliderBridge',220),('Sight_RodSeat',250),('Receiver_FrontLugSlot',340),('Front_InsertUpperShoulder',220)]:
  G.reduce(bpy.data.objects[name],target)
 for o in G.PARTS:finish(o)
 hc=bpy.data.collections.new('High_Sources');bpy.context.scene.collection.children.link(hc)
 for o in G.HIGH:
  if 'Handguard_Sculpt' in o.name:G.hand_normals(o)
  o.data.transform(Matrix.Scale(.001,4))
  for c in list(o.users_collection):c.objects.unlink(o)
  hc.objects.link(o);o.hide_render=True;o.hide_set(True)
 arm=W.armature('R39Armature',{k:tuple(v*.001 for v in h) for k,h in HEADS.items()},PARENTS)
 arm['interface_version']=interface.VERSION;arm['capabilities']=json.dumps(interface.CAPABILITIES,sort_keys=True)
 for o in G.PARTS:W.rigid_bind(o,arm,o['bone'])
 sockets=W.sockets(arm,{k:tuple(v*.001 for v in h) for k,h in SOCKETS.items()},
  {'Socket_Magazine':'Magazine','Socket_ChargingHandle':'ChargingHandle'})
 build_clips(arm);W.pose(arm,'Idle',0)
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
 sc['stage']='Form checkpoint / quick materials / nonfunctional visual internals'
 sc['maker']='Propane Defense';sc['model']='Rill 39';sc['interface_version']='1.6.0'
 sc['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 bpy.ops.wm.save_as_mainfile(filepath=str(out));W.export(out.with_suffix('.glb'),[arm,*G.PARTS,*sockets])
 counts={o.name:len(o.data.polygons) for o in G.PARTS};report=dict(total=sum(counts.values()),parts=counts,standalones={})
 mp=[o for o in G.PARTS if o['bone'] in ('Magazine','Follower','TopRound','SecondRound','ThirdRound')]
 for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]:
  W.pose(arm,clip,0);ob=W.detachable(mp,arm,'Magazine','Magazine')
  W.export(out.parent/('magazine_'+state+'.glb'),[ob],animations=False)
  report['standalones']['magazine_'+state]=len(ob.data.polygons);bpy.data.objects.remove(ob,do_unlink=True)
 W.pose(arm,None,0)
 for name,fired in [('cartridge',False),('case',True)]:
  before=len(G.PARTS);G.cartridge(G.lathe,name,(0,0,0),'Root',fired=fired,sides=32)
  pieces=G.PARTS[before:]
  for o in pieces:finish(o)
  ob=W.joined_copy(pieces,name.title());ob.parent=None
  W.export(out.parent/(name+'.glb'),[ob],animations=False)
  report['standalones'][name]=len(ob.data.polygons);bpy.data.objects.remove(ob,do_unlink=True)
  for o in pieces:bpy.data.objects.remove(o,do_unlink=True)
 (out.parent/'triangles.json').write_text(json.dumps(report,indent=2))
 (out.parent/'interface.json').write_text(json.dumps(dict(version=interface.VERSION,fps=60,
  capabilities=interface.CAPABILITIES,states=interface.STATES,clips=interface.CLIPS,sockets_mm=SOCKETS),indent=2))
 if not a.preview:
  # This checkpoint bakes only original geometric relief, never finish/wear.
  # The child owns the shared GPU lock and exports the textured inspection set.
  subprocess.run([str(ROOT/'kit/with_gpu.sh'),bpy.app.binary_path,'-b','--factory-startup',
   '--python-exit-code','1','--python',str(Path(__file__).with_name('form_normals.py')),
   '--','--source',str(out)],check=True)
 print('R39 TRIANGLES',report['total'],'DETACHABLES',report['standalones'],flush=True)
if __name__=='__main__':main()
