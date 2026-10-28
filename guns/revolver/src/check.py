"""Source topology, form, contacts and full motion sweep at the form gate."""
import argparse,sys,json
from pathlib import Path
import bpy,bmesh
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W,motion
import interface
from contacts import measure
from semantics import check as semantics
ALLOW=[]
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/revolver.blend');p.add_argument('--out',default='build/check.json');p.add_argument('--step',type=float,default=.5);p.add_argument('--clips')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
 if source.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source))
 else:
  from kit.weapon_verify import import_glb
  import_glb(source)
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 count=sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in parts)
 topology=[]
 for o in parts:
  bm=bmesh.new();bm.from_mesh(o.data)
  if source.suffix=='.glb':bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
  boundary=sum(e.is_boundary for e in bm.edges);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True)
  crossings=None
  if o.get('part_name',o.name) in ('Frame_Forging','Barrel','Cylinder_Fluted'):
   bm.verts.index_update();faces=[tuple(v.index for v in f.verts) for f in bm.faces]
   tree=BVHTree.FromPolygons([v.co for v in bm.verts],faces,all_triangles=True,epsilon=0)
   crossings=sum(a<b and not set(faces[a])&set(faces[b]) for a,b in tree.overlap(tree))
  bm.free()
  zero=sum(f.area<=1e-16 for f in o.data.polygons)
  topology.append(dict(part=o.get('part_name',o.name),boundary_edges=boundary,nonmanifold_edges=bad,volume_m3=volume,zero_area_faces=zero,disjoint_surface_crossings=crossings))
 report=dict(passed=True,stage='unbaked form checkpoint',triangles=count,topology=topology,
  semantics=semantics(arm),contacts=measure(arm))
 print('CONTACTS',report['contacts'],flush=True)
 report['all_clips']=not bool(a.clips)
 report['motion']=motion.sweep_clips(arm,a.clips.split(',') if a.clips else interface.CLIPS,step_frames=a.step,tolerance_m=.00020,allow=ALLOW)
 report['topology_passed']=all(r['nonmanifold_edges']==0 and r['volume_m3']>0 and r['zero_area_faces']==0 and r['disjoint_surface_crossings'] in (None,0) for r in topology)
 report['passed']=report['contacts']['passed'] and report['motion']['passed'] and 30000<=count<=40000 and report['topology_passed']
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(report,indent=2))
 print('CHECK',report['passed'],count,'triangles',flush=True)
 if not report['passed']:raise AssertionError('See '+a.out)
if __name__=='__main__':main()
