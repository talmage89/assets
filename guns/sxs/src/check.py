"""Checkpoint topology, intended states, required contacts and all-clip clearance."""
import argparse,json,sys,hashlib
from pathlib import Path
import bpy,bmesh
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import motion,weapon_verify as V
from contacts import measure
from semantics import check as semantics
import interface
ALLOW=[]
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/sxs.blend');p.add_argument('--out',default='build/check.json')
 p.add_argument('--clips');p.add_argument('--step',type=float,default=.5);p.add_argument('--quick',action='store_true')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
 if source.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source))
 else:V.import_glb(source)
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 topology=[]
 for ob in parts:
  bm=bmesh.new();bm.from_mesh(ob.data)
  if source.suffix=='.glb':bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
  bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free()
  topology.append(dict(part=ob.get('part_name',ob.name),nonmanifold_edges=bad,volume_m3=volume,
   zero_area_faces=sum(f.area<1e-16 for f in ob.data.polygons)))
 count=sum(sum(len(f.vertices)-2 for f in ob.data.polygons) for ob in parts)
 result=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),all_clips=not bool(a.clips) and not a.quick,
  step_frames=a.step,triangles=count,topology=topology,semantics=semantics(arm))
 try:result['contacts']=measure(arm)
 except AssertionError as e:result['contacts']=dict(passed=False,error=str(e));print('CONTACT ERROR',e,flush=True)
 if not a.quick:result['motion']=motion.sweep_clips(arm,a.clips.split(',') if a.clips else interface.CLIPS,step_frames=a.step,tolerance_m=.00020,allow=ALLOW)
 result['passed']=25000<=count<=39000 and result['contacts']['passed'] and all(not r['nonmanifold_edges'] and r['volume_m3']>0 and not r['zero_area_faces'] for r in topology) and result.get('motion',{}).get('passed',True)
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(result,indent=2));print('CHECK',result['passed'],count,flush=True)
 if not result['passed']:raise AssertionError('See '+a.out)
if __name__=='__main__':main()
