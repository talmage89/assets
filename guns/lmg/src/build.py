"""Clean-scene form checkpoint; source plus unbaked rigged inspection GLBs."""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as M,weapon as W
from guns.common.ammo556_visual import cartridge,link
import geometry as G,interface
from clips import build_clips
from belt import COUNT
HEADS={'Root':(0,0,0),'Bolt':(0,150,95),'OperatingRod':(0,150,70),'ChargingHandle':(28,195,78),
 'Trigger':(0,47,48),'Safety':(0,0,52),'FeedCover':(0,236,127),
 'CoverLatch':(0,-50,127),'FeedTray':(0,231,118),'FeedPawls':(-22,149,136),
 'CarryHandle':(0,255,105),'BarrelLatch':(-41,235,124),'ShoulderRest':(0,-321,109),
 'BipodL':(-28,531,46),'BipodR':(28,531,46),
 'BipodSplayL':(-28,531,46),'BipodSplayR':(28,531,46),
 'BipodExtendL':(-28,305,40),'BipodExtendR':(28,305,40),
 'Magazine':(0,164,51),'MagRelease':(0,164,52),'BoxLid':(64,164,36),
 'BeltRoot':(0,145,124),'ChamberRound':(0,197,105),'EjectedCase':(55,150,90),'EjectedLink':(45,192,112)}
PARENTS={'CoverLatch':'FeedCover','FeedPawls':'FeedCover','BoxLid':'Magazine',
 'BipodSplayL':'BipodL','BipodSplayR':'BipodR','BipodExtendL':'BipodSplayL','BipodExtendR':'BipodSplayR'}
for i in range(COUNT):
 HEADS[f'BeltLink{i:02d}']=(0,145,124);HEADS[f'BeltRound{i:02d}']=(0,145,124)
 PARENTS[f'BeltLink{i:02d}']='BeltRoot';PARENTS[f'BeltRound{i:02d}']=f'BeltLink{i:02d}'
SOCKETS={'Socket_Muzzle':(0,710,105),'Socket_Foregrip':(-26,344,62),'Socket_Butt':(0,-330,47),
 'Socket_Eye':(0,-97.5,176),'Socket_Ejection':(26,150,91),'Socket_MagWell':(0,164,53),
 'Socket_Magazine':HEADS['Magazine'],'Socket_ChargingHandle':(49,190,83),
 'Socket_BeltEntry':(0,145,124),'Socket_LinkEjection':(28,200,112),
 'Socket_FeedCover':(0,-40,144),'Socket_BoxMouth':(-55,145,39)}
RIDING={'Socket_Magazine':'Magazine','Socket_ChargingHandle':'ChargingHandle',
 'Socket_FeedCover':'FeedCover','Socket_BoxMouth':'Magazine'}

def triangulate(o):
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.0001)
 bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 t=o.modifiers.new('Checkpoint triangles','TRIANGULATE');t.keep_custom_normals=True;M.apply(o)
 ns=[n.vector.copy() for n in o.data.corner_normals]
 for f in o.data.polygons:
  for j in f.loop_indices:
   if ns[j].dot(f.normal)<.05:ns[j]=f.normal.copy()
 o.data.normals_split_custom_set(ns)
 o.data.transform(Matrix.Scale(.001,4));o.matrix_world=Matrix.Identity(4)

def ammo():
 base=len(G.PARTS)
 cartridge(G.lathe,'CartridgeTemplate',(0,0,0),'Root',sides=16)
 pieces=G.PARTS[base:];round_ob=W.joined_copy(pieces,'CartridgeTemplate')
 for o in pieces:G.PARTS.remove(o);bpy.data.objects.remove(o,do_unlink=True)
 link_ob=link(M.mesh,G.MAT['phosphate']);G.reg(link_ob)
 # Template data is shared by nineteen displayed instances; bindings live on objects.
 for i in range(COUNT):
  for template,kind in [(round_ob,'Round'),(link_ob,'Link')]:
   o=template.copy();o.data=template.data;bpy.context.collection.objects.link(o)
   o.name=f'Belt_{kind}_{i:02d}';o.data=template.data
   o['bone']=f'Belt{kind}{i:02d}';o['asset_set']='LMG';o['part_name']=o.name
   # Give each instance vertices at its common rest-bone location. Transform
   # shared data ONCE below, never once per instance.
   G.PARTS.append(o)
 round_ob.data.transform(Matrix.Translation((0,145,124)))
 link_ob.data.transform(Matrix.Translation((0,145,124)))
 G.PARTS.remove(link_ob);bpy.data.objects.remove(round_ob,do_unlink=True);bpy.data.objects.remove(link_ob,do_unlink=True)
 # Hidden chamber occupancy is a semantic owner; no intersecting render mesh.
 cartridge(G.lathe,'EjectedCase',(55,150,90),'EjectedCase',fired=True,sides=24)
 o=link(M.mesh,G.MAT['phosphate'],'EjectedLink');o.data.transform(Matrix.Translation((45,192,112)));G.reg(o,'EjectedLink')


def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/lmg.blend')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.read_factory_settings(use_empty=True);G.palette()
 for f in (G.receiver,G.feed,G.sights_barrel,G.furniture,G.bipod,G.ammo_box,ammo):f()
 for o in G.PARTS:
  if o.name.startswith('Bipod_Foot_'):o.data.transform(Matrix.Translation((0,10,0)))
  if o.name.startswith('Box_') and o.name not in ('Box_Suspension','Box_Latch','Box_LatchSeat'):
   o.data.transform(Matrix.Translation((0,0,43)))
 # Flat shield lands and covered surfaces do not warrant dense triangles.
 for o in G.PARTS:
  target={'HeatShield':700,'Stock_Sculpt':2200,'Handguard_Sculpt':2250,
   'PistolGrip_Sculpt':1600,'Receiver_Sheet':1700,'FlashHider':700,
   'SideWell_Housing':400,'FeedCover_Shell':850,'Barrel_Exterior':700,
   'TriggerGuard_Band':500,'CarryHandle_Grip':600,'ChargingHandle_Paddle':500,
   'FrontSight_Tower':450}.get(o.name)
  if target:G.reduce(o,target)
 # Apply geometric work once per shared block, preserving round/link reuse.
 seen={}
 for o in G.PARTS:
  key=o.data.as_pointer()
  if key in seen:o.data=seen[key]
  else:triangulate(o);seen[key]=o.data
 high=bpy.data.collections.new('High_Sources');bpy.context.scene.collection.children.link(high)
 for o in G.HIGH:
  o.data.transform(Matrix.Scale(.001,4))
  for c in list(o.users_collection):c.objects.unlink(o)
  high.objects.link(o);o.hide_render=True;o.hide_set(True)
 arm=W.armature('HarrowArmature',{k:tuple(v*.001 for v in h) for k,h in HEADS.items()},PARENTS)
 arm['interface_version']='1.8.0';arm['capabilities']=json.dumps(interface.CAPABILITIES,sort_keys=True)
 for o in G.PARTS:
  if o.name.startswith('Belt_'):
   # Rigid bone-parented instances preserve ONE mesh. Blender 5.2 stores
   # linked-data deform-group names with the mesh, so different skinned
   # owners would overwrite each other despite separate objects.
   o.vertex_groups.clear();o.parent=arm;o.parent_type='BONE';o.parent_bone=o['bone']
   bpy.context.view_layer.update();o.matrix_world=Matrix.Identity(4)
   o['export_part']=o.name
  else:W.rigid_bind(o,arm,o['bone'])
 sockets=W.sockets(arm,{k:tuple(v*.001 for v in h) for k,h in SOCKETS.items()},RIDING)
 build_clips(arm);W.pose(arm,'Idle',0)
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['maker']='Propane Defense';sc['model']='Harrow 56'
 sc['stage']='Form checkpoint / unbaked inspection constants / nonfunctional display internals'
 bpy.ops.wm.save_as_mainfile(filepath=str(out));W.export(out.with_suffix('.glb'),[arm,*G.PARTS,*sockets])
 report=dict(stage=sc['stage'],triangles=sum(len(o.data.polygons) for o in G.PARTS),
  parts={o.name:len(o.data.polygons) for o in G.PARTS},bones=len(HEADS),clips=len(interface.CLIPS),
  sockets=len(SOCKETS),shared_belt_round_meshes=len({o.data.as_pointer() for o in G.PARTS if o.name.startswith('Belt_Round')}),
  shared_belt_link_meshes=len({o.data.as_pointer() for o in G.PARTS if o.name.startswith('Belt_Link')}),standalones={})
 for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]:
  W.pose(arm,clip,0);mp=[o for o in G.PARTS if o['bone'] in ('Magazine','BoxLid') or (state=='loaded' and o['bone'] in [f'Belt{k}{i:02d}' for k in ('Link','Round') for i in (15,16,17,18)])]
  ob=W.detachable(mp,arm,'Magazine','Box');W.export(out.parent/('box_'+state+'.glb'),[ob],animations=False)
  report['standalones']['box_'+state]=dict(triangles=len(ob.data.polygons),bytes=(out.parent/('box_'+state+'.glb')).stat().st_size)
  bpy.data.objects.remove(ob,do_unlink=True)
 for name,fired in [('cartridge',False),('case',True),('link',None)]:
  before=len(G.PARTS)
  if fired is None:G.reg(link(M.mesh,G.MAT['phosphate'],'StandaloneLink'))
  else:cartridge(G.lathe,name,(0,0,0),'Root',fired=fired,sides=32)
  pieces=G.PARTS[before:]
  for o in pieces:triangulate(o)
  ob=W.joined_copy(pieces,name.title());ob.parent=None
  W.export(out.parent/(name+'.glb'),[ob],animations=False)
  report['standalones'][name]=dict(triangles=len(ob.data.polygons),bytes=(out.parent/(name+'.glb')).stat().st_size)
  bpy.data.objects.remove(ob,do_unlink=True)
  for o in pieces:bpy.data.objects.remove(o,do_unlink=True)
 W.pose(arm,'Idle',0)
 (out.parent/'triangles.json').write_text(json.dumps(report,indent=2))
 (out.parent/'interface.json').write_text(json.dumps(dict(version='1.8.0',capabilities=interface.CAPABILITIES,states=interface.STATES,clips=interface.CLIPS,sockets_mm=SOCKETS),indent=2))
 print('LMG CHECKPOINT',report['triangles'],'triangles,',len(HEADS),'bones,',len(interface.CLIPS),'clips')
if __name__=='__main__':main()
