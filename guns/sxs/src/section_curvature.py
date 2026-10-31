"""Every-5-mm dense/export head cuts and measured local profile curvature.

Geometry is sampled from actual triangles. A 0.8 mm quadratic measurement
window rejects triangle tessellation chatter while resolving millimeter waves.
All sign reversals above the explicit 0.002/mm floor are reported, including
unexplained ones. No passing adjacent-face-angle statistic substitutes for it.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(BASE/'src'))

def capture(path,dense):
 import bpy
 from mathutils import Vector
 from mathutils.bvhtree import BVHTree
 from kit import weapon as W,weapon_verify as V
 if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path))
 else:V.import_glb(path)
 arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,'Idle',0)
 name='HIGH_Action_Body' if dense else 'Action_Body'
 ob=next(o for o in bpy.data.objects if o.get('part_name',o.name)==name)
 mesh=ob.data;mesh.calc_loop_triangles()
 world=[ob.matrix_world@v.co for v in mesh.vertices]
 tree=BVHTree.FromPolygons(world,[tuple(t.vertices) for t in mesh.loop_triangles],all_triangles=True)
 feature_trees={}
 ownership=mesh.attributes.get('head_region') if dense else None
 if ownership:
  for label,region in [('recess lip',2),('wood line',4)]:
   faces=[tuple(t.vertices) for t in mesh.loop_triangles if ownership.data[t.polygon_index].value==region]
   feature_trees[label]=BVHTree.FromPolygons(world,faces,all_triangles=True)
 rows=[]
 cuts=[('transverse',y) for y in range(85,116,5)]+[('longitudinal',x) for x in range(-25,26,5)]
 for direction,station in cuts:
  coordinate=np.arange(-25.9,25.901,.05) if direction=='transverse' else np.arange(85,114.901,.05)
  heights=[];feature_distances={name:[] for name in feature_trees}
  for t in coordinate:
   x,y=(t,min(station,114.8)) if direction=='transverse' else (station,t)
   p=tree.ray_cast(Vector((x*.001,y*.001,.080)),Vector((0,0,-1)),.08)[0]
   heights.append(float(p.z*1000) if p is not None else None)
   for name,bvh in feature_trees.items():feature_distances[name].append(float(bvh.find_nearest(p)[3]*1000) if p is not None else None)
  rows.append(dict(direction=direction,station_mm=station,coordinate_mm=coordinate.tolist(),height_mm=heights,feature_distances_mm=feature_distances))
 return rows

def analyze(row):
 t=np.array(row['coordinate_mm']);z=np.array([v if v is not None else np.nan for v in row['height_mm']]);curvature=np.full(len(t),np.nan)
 for i in range(8,len(t)-8):
  h=z[i-8:i+9]
  if not np.all(np.isfinite(h)) or np.ptp(h)>2:continue
  c=np.polynomial.polynomial.polyfit(t[i-8:i+9]-t[i],h,2)
  curvature[i]=2*c[2]/(1+c[1]**2)**1.5
 # Deadband retains the previous sign through nearly planar samples. Gaps
 # (vertical lip / external joint) split profiles instead of hiding changes.
 events=[];previous=None
 for i,k in enumerate(curvature):
  if not np.isfinite(k):previous=None;continue
  if abs(k)<.002:continue
  sign=1 if k>0 else -1
  if previous is not None and sign!=previous[1]:
   a=previous[0];events.append(dict(coordinate_mm=float((t[a]+t[i])*.5),from_sign=previous[1],to_sign=sign,bracket_mm=[float(t[a]),float(t[i])]))
  previous=i,sign
 for event in events:
  c=event['coordinate_mm'];i=int(np.argmin(abs(t-c)))
  candidates=[(values[i],name) for name,values in row.get('feature_distances_mm',{}).items() if values[i] is not None]
  distance,feature=min(candidates) if candidates else (float('inf'),'unassigned')
  if distance>.8:feature='unassigned: needs image/section review'
  event['construction_feature']=feature
  event['nearest_named_surface_mm']=float(distance) if np.isfinite(distance) else None
  event['photo_acceptance']='Actual lip/rear-cap proximity only; other features require explicit image review'
 row.update(curvature_per_mm=[float(v) if np.isfinite(v) else None for v in curvature],sign_changes=events,sign_change_count=len(events))
 return row

def plot(report,out):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 for direction in ('transverse','longitudinal'):
  rows=[r for r in report['dense'] if r['direction']==direction]
  fig,axes=plt.subplots(len(rows),2,figsize=(13,len(rows)*2.15),squeeze=False)
  for j,row in enumerate(rows):
   t=row['coordinate_mm'];z=row['height_mm'];k=row['curvature_per_mm']
   axes[j,0].plot(t,z,color='#147f80',lw=1);axes[j,1].plot(t,k,color='#343b8e',lw=1)
   game=next(r for r in report['export'] if r['direction']==direction and r['station_mm']==row['station_mm'])
   axes[j,0].plot(t,game['height_mm'],color='#ab592e',lw=.6,alpha=.75)
   axes[j,1].plot(t,game['curvature_per_mm'],color='#ab592e',lw=.5,alpha=.45)
   for event in row['sign_changes']:
    for ax in axes[j]:
     ax.axvline(event['coordinate_mm'],color='#b32949',lw=.6)
     if event['bracket_mm'][1]-event['bracket_mm'][0]>.2:ax.axvspan(*event['bracket_mm'],color='#b32949',alpha=.08)
   for ax in axes[j]:ax.grid(alpha=.2);ax.tick_params(labelsize=7)
   axes[j,0].set_ylabel('Z mm');axes[j,1].set_ylabel('curvature / mm');axes[j,1].axhline(0,color='gray',lw=.5)
   axes[j,0].set_title(f"{direction} {'Y' if direction=='transverse' else 'X'}={row['station_mm']} mm",fontsize=9)
   axes[j,1].set_title(f"sign changes: dense {row['sign_change_count']}, export {game['sign_change_count']}; red = dense",fontsize=9)
  axes[-1,0].set_xlabel('X mm' if direction=='transverse' else 'Y mm');axes[-1,1].set_xlabel('X mm' if direction=='transverse' else 'Y mm')
  fig.suptitle('Actual head sections / teal dense, brown export / local quadratic curvature',fontsize=12)
  fig.tight_layout(rect=(0,0,1,.98));fig.savefig(out/(direction+'.png'),dpi=120);plt.close(fig)

def main():
 p=argparse.ArgumentParser();p.add_argument('--plot',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
 out=BASE/'renders/checkpoint/curvature';out.mkdir(parents=True,exist_ok=True);dest=out/'sections.json'
 if a.plot:plot(json.loads(dest.read_text()),out);return
 source=BASE/'build/sxs.blend';game=BASE/'export/sxs.glb'
 report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),export_sha256=hashlib.sha256(game.read_bytes()).hexdigest(),
  sampling_mm=.05,quadratic_window_mm=.8,curvature_sign_floor_per_mm=.002,
  dense=[analyze(r) for r in capture(source,True)],export=[analyze(r) for r in capture(game,False)])
 dest.write_text(json.dumps(report,indent=2))
 for row in report['dense']:print(row['direction'],row['station_mm'],row['sign_change_count'],row['sign_changes'])
if __name__=='__main__':main()
