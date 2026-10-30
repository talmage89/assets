"""Deterministic B24 form checkpoint, authored entirely from scripts."""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,model as M
import geometry as G
from mechanism import action_barrel,optic,bipod,feed_details
from clips import build_clips
import interface

HEADS={'Root':(0,0,0),'BoltTravel':(0,18,65),'Bolt':(0,18,65),
 'CockingPiece':(0,-22,65),'Trigger':(0,26.69,23),'Safety':(18,14,62),
 'BoltRelease':(-3,20,20),'MagRelease':(0,98,25),'Magazine':(0,147,46),
 'Follower':(0,147,32.5),'TopRound':(0,107.5,50.5),'ReserveRound':(3.7,107.5,38.7),
 'ChamberRound':(0,209.5,65),'CycleCase':(0,209.5,65),'PowerRing':(0,-74,113),'Diopter':(0,-115,113),
 'Elevation':(0,62,129),'Windage':(16.5,62,113),'Parallax':(-16.5,62,113),
 'Reticle':(0,-108,113),'BipodL':(-24,410,2),'BipodR':(24,410,2),
 'BipodSplayL':(-24,410,2),'BipodSplayR':(24,410,2),
 'BipodExtendL':(-24,510,2),'BipodExtendR':(24,510,2)}
SOCKETS={'Socket_Muzzle':(0,819.6,65),'Socket_Foregrip':(-22,290,26),
 'Socket_Butt':(0,-310,20),'Socket_Eye':(0,-213.9,113),
 'Socket_Ejection':(14,130,68),'Socket_MagWell':(0,147,17),
 'Socket_Magazine':HEADS['Magazine'],'Socket_OpticObjective':(0,232,113)}
PARENTS={'Bolt':'BoltTravel','CockingPiece':'BoltTravel','Follower':'Magazine',
 'TopRound':'Magazine','ReserveRound':'Magazine','BipodSplayL':'BipodL','BipodSplayR':'BipodR',
 'BipodExtendL':'BipodSplayL','BipodExtendR':'BipodSplayR'}

def finish(ob):
 tri=ob.modifiers.new('Export triangles','TRIANGULATE');tri.keep_custom_normals=True;M.apply(ob)
 # Keep manufactured smooth fields except when they oppose actual winding.
 normals=[n.vector.copy() for n in ob.data.corner_normals]
 for f in ob.data.polygons:
  for j in f.loop_indices:
   if normals[j].dot(f.normal)<.06:normals[j]=f.normal.copy()
 ob.data.normals_split_custom_set(normals)
 ob.data.transform(Matrix.Scale(.001,4));ob.matrix_world=Matrix.Identity(4)

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/bolt.blend')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.read_factory_settings(use_empty=True);G.palette();G.sculpt_stock();action_barrel();G.magazine();G.correct_feed_box();feed_details();optic();bipod()
 for ob in G.PARTS:finish(ob)
 arm=W.armature('B24Armature',{k:tuple(v*.001 for v in h) for k,h in HEADS.items()},PARENTS)
 arm['base_interface_version']=interface.VERSION;arm['interface_version']=interface.SUPPLEMENT_VERSION
 arm['capabilities']=json.dumps(interface.CAPABILITIES,sort_keys=True)
 for ob in G.PARTS:W.rigid_bind(ob,arm,ob['bone'])
 sockets=W.sockets(arm,{k:tuple(v*.001 for v in h) for k,h in SOCKETS.items()},{'Socket_Magazine':'Magazine'})
 build_clips(arm);sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
 (out.parent/'interface.json').write_text(json.dumps(dict(version=interface.SUPPLEMENT_VERSION,
    base_version=interface.VERSION,fps=60,capabilities=interface.CAPABILITIES,states=interface.STATES,
    clips=interface.CLIPS,sockets_mm=SOCKETS),indent=2))
 sc['stage']='Form checkpoint; quick constants, no look-dev or baked texture claim'
 bpy.ops.wm.save_as_mainfile(filepath=str(out))
 low={}
 for name,mesh in G.HIGH.items():
  ob=bpy.data.objects[name];low[name]=ob.data;mesh.transform(Matrix.Scale(.001,4));ob.data=mesh
  ob.vertex_groups.clear();vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(mesh.vertices))),1,'REPLACE')
 bpy.ops.wm.save_as_mainfile(filepath=str(out.parent/'sculpt.blend'))
 for name,mesh in low.items():
  ob=bpy.data.objects[name];ob.data=mesh;ob.vertex_groups.clear()
  vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(mesh.vertices))),1,'REPLACE')
 joined=W.joined_copy(G.PARTS,'VesperB24');joined.parent=arm
 mod=joined.modifiers.new('Rigid weapon skin','ARMATURE');mod.object=arm
 from animation_sampling import export as export_animation
 export_animation(out.with_suffix('.glb'),[arm,joined]+sockets);bpy.data.objects.remove(joined,do_unlink=True)
 magparts=[o for o in G.PARTS if o['bone'] in ('Magazine','Follower','TopRound','ReserveRound')]
 for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]:
  W.pose(arm,clip,0);mag=W.detachable(magparts,arm,'Magazine','Magazine')
  W.export(out.parent/('magazine_'+state+'.glb'),[mag],animations=False);bpy.data.objects.remove(mag,do_unlink=True)
 W.pose(arm,None,0)
 counts={o.name:len(o.data.polygons) for o in G.PARTS};old=list(G.PARTS)
 G.ammunition('FiredCase',(0,0,0),'Root',fired=True)
 cases=[o for o in G.PARTS if o not in old]
 for ob in cases:finish(ob)
 case=W.joined_copy(cases,'FiredCase');case.parent=None;W.export(out.parent/'case.glb',[case],animations=False)
 data=dict(total=sum(counts.values()),parts=counts,fired_case=len(case.data.polygons))
 (out.parent/'triangles.json').write_text(json.dumps(data,indent=2));print('B24 TRIANGLES',data['total'],'CASE',data['fired_case'],flush=True)
if __name__=='__main__':main()
