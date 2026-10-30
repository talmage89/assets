"""Geometry, required contacts, and sampled unwanted-penetration audit."""
import argparse,sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W,motion
from contacts import part,measure
from interface import CLIPS
from form import audit as form_audit
from trigger_check import measure as trigger_measure
def geometry(arm):
 W.pose(arm,'Idle',0)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==arm and 'bone' in o and not o.get('bake_only')]
 pts=[p for o in meshes if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001 for p in motion.surface(o)['points']]
 lo=[min(p[k] for p in pts) for k in range(3)];hi=[max(p[k] for p in pts) for k in range(3)];size=[b-a for a,b in zip(lo,hi)]
 barrel=motion.surface(part('Barrel'));length=barrel['hi'].y-barrel['lo'].y
 # Actual trigger contact and rubber-back intersections at a common Z station.
 tr=motion.surface(part('Trigger_Shoe'));pad=motion.surface(part('Recoil_Pad'))
 trigger=tr['tree'].ray_cast(Vector((0,.125,-.020)),Vector((0,-1,0)),.1)
 butt=pad['tree'].ray_cast(Vector((0,-.345,-.020)),Vector((0,1,0)),.15)
 assert trigger[0] is not None and butt[0] is not None
 pull=trigger[0].y-butt[0].y
 assert .977<size[1]<.980,size
 assert abs(length-.4699)<.00001,length
 assert .350<pull<.365,pull
 count=sum(len(o.data.polygons) for o in meshes)
 assert 30000<=count<=40000,count
 from feed_audit import dimensions as feed_dimensions
 return dict(feed_dimensions=feed_dimensions(arm),bounds_m=dict(lo=lo,hi=hi,size=size),barrel_length_m=length,length_of_pull_m=pull,
  trigger_contact_m=list(trigger[0]),pad_contact_m=list(butt[0]),triangles=count,form=form_audit(),trigger_surfaces=trigger_measure(arm))
def sweep(arm):
 # Every exception has a measured bound. No whole pair is skipped.
 allow=[dict(a='CarrierShell_Head',b='Carrier_Tray',max_penetration_m=.0004,reason='rim bears on the stamped concave cradle'),
  dict(a='Bolt_Lock',b='Barrel_LockSeat',max_penetration_m=.0002,reason='visual battery seat contact'),
  dict(a='ShellStop_Tip_',b='TubeShell1_Head',max_penetration_m=.0002,reason='rim retention face contact')]
 return motion.sweep_clips(arm,list(CLIPS),step_frames=.5,tolerance_m=.00025,allow=allow)
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/shotgun.blend');p.add_argument('--out',default='build/check.json');p.add_argument('--motion',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));arm=bpy.data.objects['ShotgunArmature']
 result=geometry(arm);result['contacts']=measure(arm)
 if a.motion:result['motion']=sweep(arm)
 result['passed']=result.get('motion',{}).get('passed',True)
 Path(a.out).write_text(json.dumps(result,indent=2));print('GEOMETRY',result['bounds_m']['size'],result['triangles'],flush=True)
 assert result['passed'],'Motion violations; see '+a.out
if __name__=='__main__':main()
