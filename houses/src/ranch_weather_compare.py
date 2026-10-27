"""Independent old/new linear vertex-weather comparison on actual surfaces."""
import argparse,json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from ranch_chart_check import nearest64


def read(path):
 bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));result={}
 for ob in bpy.context.scene.objects:
  comp=ob.get('component')
  if ob.type!='MESH' or comp not in ('roof','wall','eave_rake_soffit','ridge'):continue
  if comp=='wall' and ob.get('face')=='front':continue
  me=ob.data;me.calc_loop_triangles();vertices=np.array([ob.matrix_world@v.co for v in me.vertices],dtype='float64');colors=np.array([v.color[:3] for v in me.color_attributes['Tint'].data]);groups={}
  outward=dict(back=Vector((0,1,0)),left=Vector((-1,0,0)),right=Vector((1,0,0))).get(ob.get('face'))
  for t in me.loop_triangles:
   if t.area<1e-6:continue
   n=(ob.matrix_world.to_3x3()@t.normal).normalized()
   if comp=='roof' and n.z<.4:continue
   if comp=='wall' and (outward is None or n.dot(outward)<.9):continue
   axis=max(range(3),key=lambda k:abs(n[k]));material=me.materials[t.material_index].name
   finish=int(np.floor(np.mean([me.uv_layers.active.data[li].uv.y for li in t.loops])*8)) if 'Trim' in material else -1
   key=(t.material_index,axis,n[axis]>0,finish)
   groups.setdefault(key,[]).append(tuple(t.vertices))
  for key,triangles in groups.items():
   ind=np.array(triangles);xyz=vertices[ind];area=np.linalg.norm(np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]),axis=1)/2
   tree=BVHTree.FromPolygons([Vector(p) for p in vertices],triangles,all_triangles=True)
   result[(ob.name,key)]=dict(xyz=xyz,colors=colors[ind],area=area,tree=tree,component=comp)
 return result


def compare(seed,before):
 old=read(before/f'game-{seed}.blend');new=read(Path(f'build/ranch/delivery/game-{seed}.blend'));rows=[]
 for direction,a,b in [('new-to-old',new,old),('old-to-new',old,new)]:
  for key,data in a.items():
   assert key in b,key
   target=b[key];errors=[];weights=[];distances=[];ambiguous=0;raw_maximum=0
   for xyz,rgb,area in zip(data['xyz'],data['colors'],data['area']):
    center=xyz.mean(axis=0);hit=target['tree'].find_nearest(Vector(center));point,idx,distance=hit[0],hit[2],hit[3]
    if distance>2e-5:point,idx,distance=nearest64(center,target['xyz'])
    p,q,r=target['xyz'][idx];ab=q-p;ac=r-p;n=np.cross(ab,ac);nn=np.dot(n,n);d=np.array(point)-p
    u=np.dot(np.cross(d,ac),n)/nn;v=np.dot(np.cross(ab,d),n)/nn
    c=target['colors'][idx];value=c[0]*(1-u-v)+c[1]*u+c[2]*v
    error=float(abs(rgb.mean(axis=0)-value).max());raw_maximum=max(raw_maximum,error)
    if error>.02:
     candidates=nearest64(center,target['xyz'],all_within=2e-5)
     if len(candidates)>1:ambiguous+=1
     for point2,idx2,_ in candidates:
      a2,b2,c2=target['xyz'][idx2];ab2=b2-a2;ac2=c2-a2;n2=np.cross(ab2,ac2);nn2=np.dot(n2,n2);d2=np.array(point2)-a2
      u2=np.dot(np.cross(d2,ac2),n2)/nn2;v2=np.dot(np.cross(ab2,d2),n2)/nn2;c=target['colors'][idx2]
      value2=c[0]*(1-u2-v2)+c[1]*u2+c[2]*v2;error=min(error,float(abs(rgb.mean(axis=0)-value2).max()))
    errors.append(error);weights.append(float(area));distances.append(distance)
   weights=np.array(weights);errors=np.array(errors);order=np.argsort(errors);cdf=np.cumsum(weights[order]);cdf/=cdf[-1]
   rows.append(dict(object=key[0],surface=str(key[1]),direction=direction,component=data['component'],samples=len(errors),area_m2=float(weights.sum()),mean_absolute_max_channel=float(np.average(errors,weights=weights)),p99=float(np.interp(.99,cdf,errors[order])),maximum=float(errors.max()),raw_nearest_maximum=raw_maximum,coincident_facet_samples=ambiguous,max_surface_distance_m=float(max(distances))))
 total=sum(r['area_m2'] for r in rows);mean=sum(r['mean_absolute_max_channel']*r['area_m2'] for r in rows)/total
 means={}
 for label,dataset in [('before',old),('after',new)]:
  means[label]={}
  for component in sorted({d['component'] for d in dataset.values()}):
   parts=[d for d in dataset.values() if d['component']==component];area=sum(d['area'].sum() for d in parts)
   means[label][component]=list(map(float,sum((d['colors'].mean(axis=1)*d['area'][:,None]).sum(axis=0) for d in parts)/area))
 result=dict(seed=seed,rows=rows,factor_mean_linear_rgb=means,area_weighted_mean_max_channel_error=mean,maximum=max(r['maximum'] for r in rows),samples=sum(r['samples'] for r in rows))
 assert mean<.004,(seed,mean)
 print('WEATHER_COMPARE',seed,mean,result['maximum'],result['samples'],flush=True);return result


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seeds',default='11,12,13,15,16');p.add_argument('--before',type=Path,default=Path('build/ranch/revision2/before/delivery'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);rows=[compare(int(s),a.before) for s in a.seeds.split(',')]
 Path('build/ranch/revision2/weather-comparison.json').write_text(json.dumps(dict(passed=True,rows=rows,scope='Linear RGB weather factors at both triangulations triangle centers; area weighted; coincident trim/gauge facets matched within 20 micrometers with raw nearest errors also retained; shared texture bytes separately unchanged'),indent=2))
