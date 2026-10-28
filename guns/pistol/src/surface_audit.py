"""Measure shipped texels on actual surfaces; optionally prove texture-only edits.

Run in Blender after export. --before points to a saved export/ directory.
--keep-tangents preserves accepted tangent bytes for a texture-only refresh,
after checking every other non-image buffer and the complete delivery JSON.
No reference pixels enter the asset. Values are PNG sRGB bytes and ORM bytes.
"""
import argparse, hashlib, json, math, struct, sys
from pathlib import Path
import bpy
import numpy as np
from PIL import Image
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]))
from kit.gltf import GLB


def unchanged(before,keep_tangents=False):
 assert before.is_dir(),'Missing accepted export directory: '+str(before)
 assert {p.name for p in before.glob('*.glb')}=={p.name for p in (BASE/'export').glob('*.glb')},'Baseline must contain every delivery GLB'
 result={}
 for path in sorted(before.glob('*.glb')):
  old,new=GLB(path),GLB(BASE/'export'/path.name)
  image_views={row['bufferView'] for row in old.json['images']}
  assert len(old.json['bufferViews'])==len(new.json['bufferViews'])
  payload=[];repairs=[]
  tangent_views={old.json['accessors'][p['attributes']['TANGENT']]['bufferView']
    for mesh in old.json['meshes'] for p in mesh['primitives'] if 'TANGENT' in p['attributes']}
  for i,(a,b) in enumerate(zip(old.json['bufferViews'],new.json['bufferViews'])):
   if i in image_views:continue
   def extract(glb,row):
    start=row.get('byteOffset',0)
    return glb.binary[start:start+row['byteLength']]
   x,y=extract(old,a),extract(new,b)
   if x!=y and keep_tangents and i in tangent_views:
    aa,bb=np.frombuffer(x,dtype='<f4'),np.frombuffer(y,dtype='<f4')
    assert aa.shape==bb.shape and np.isfinite(bb).all()
    delta=float(np.max(np.abs(aa-bb)))
    assert delta<=.000101,(path.name,'tangent drift exceeds exporter rounding')
    repairs.append((b.get('byteOffset',0),x,dict(components=int(np.count_nonzero(aa!=bb)),max_delta=delta)))
   else:assert x==y,(path.name,i,'non-image bytes changed')
   payload.append(x)
  for glb in (old,new):
   glb.json.pop('buffers')
   for view in glb.json['bufferViews']:view.pop('byteOffset',None)
   for i in image_views:glb.json['bufferViews'][i]['byteLength']=0
  assert old.json==new.json,(path.name,'delivery JSON changed')
  if repairs:
   destination=BASE/'export'/path.name;raw=bytearray(destination.read_bytes())
   offset=12
   while offset<len(raw):
    size,kind=struct.unpack_from('<II',raw,offset)
    if kind==0x004e4942:break
    offset+=8+size
   assert kind==0x004e4942
   for start,preserved,record in repairs:raw[offset+8+start:offset+8+start+len(preserved)]=preserved
   destination.write_bytes(raw)
   check=GLB(destination)
   for index in tangent_views:
    row=check.json['bufferViews'][index];start=row.get('byteOffset',0)
    original=GLB(path);prior=original.json['bufferViews'][index];previous=prior.get('byteOffset',0)
    assert check.binary[start:start+row['byteLength']]==original.binary[previous:previous+prior['byteLength']]
  result[path.name]=dict(non_image_bytes_identical=True,
   json_except_image_lengths_and_offsets_identical=True,
   non_image_sha256=hashlib.sha256(b''.join(payload)).hexdigest(),
   tangent_rounding_preserved=[row[2] for row in repairs])
 return result


def main():
 p=argparse.ArgumentParser();p.add_argument('--before',type=Path)
 p.add_argument('--keep-tangents',action='store_true')
 p.add_argument('--out',type=Path,default=BASE/'build/surface-audit.json')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 maps={key:np.asarray(Image.open(BASE/'textures'/f'T_C9_{key}.png'))
       for key in ('BaseColor','Normal','ORM')}
 result=dict(units='sRGB BaseColor bytes; linear ORM/Normal bytes; density at 2048',surfaces={})
 def surface(name,origins,direction):
  ob=bpy.data.objects[name];me=ob.data;me.calc_loop_triangles()
  triangles=list(me.loop_triangles);uv=me.uv_layers['BakeUV']
  tree=BVHTree.FromPolygons([v.co for v in me.vertices],[t.vertices for t in triangles],all_triangles=True)
  samples={k:[] for k in maps};densities=[];coords=[]
  for origin in origins:
   pos,normal,index,dist=tree.ray_cast(Vector(origin),Vector(direction))
   if index is None:continue
   tri=triangles[index];verts=[me.vertices[i].co for i in tri.vertices]
   tex=[Vector((*uv.data[i].uv,0)) for i in tri.loops]
   t=barycentric_transform(pos,*verts,*tex)
   coords.append([float(t.x),float(t.y)])
   for key,im in maps.items():
    x=min(im.shape[1]-1,max(0,int(t.x*im.shape[1])))
    y=min(im.shape[0]-1,max(0,int((1-t.y)*im.shape[0])))
    samples[key].append(im[y,x,:3])
   ua=abs((tex[1]-tex[0]).cross(tex[2]-tex[0]).z)/2
   densities.append(math.sqrt(ua/tri.area)*2048)
  assert densities,(name,'no surface hits')
  return dict(hits=len(densities),density_px_m_p0_p50_p100=np.percentile(densities,[0,50,100]).round(3).tolist(),
   uv_bounds=np.array([np.min(coords,axis=0),np.max(coords,axis=0)]).round(7).tolist(),
   channels={k:dict(p10_p50_p90=np.percentile(v,[10,50,90],axis=0).round(3).tolist()) for k,v in samples.items()})
 def grid(xs,ys,z):return [(x,y,z) for x in xs for y in ys]
 result['surfaces']['hood_center']=surface('Barrel_Hood',grid(np.linspace(-.005,.006,31),np.linspace(.040,.060,51),.070),(0,0,-1))
 result['surfaces']['hood_front_contact']=surface('Barrel_Hood',grid(np.linspace(-.005,.006,31),np.linspace(.0650,.06535,9),.070),(0,0,-1))
 result['surfaces']['slide_flat']=surface('Slide_Shell',[(.020,y,z) for y in np.linspace(.010,.024,31) for z in np.linspace(.054,.059,11)],(-1,0,0))
 result['surfaces']['slide_front_crests']=surface('Slide_Shell',[(.020,y+(z-.0417)*1.97/25.1+.0015,z) for y in np.arange(.090,.121,.003) for z in np.linspace(.045,.063,31)],(-1,0,0))
 result['surfaces']['release_pad']=surface('MagRelease_Button',[(-.020,y,z) for y in np.linspace(.014,.019,11) for z in np.linspace(.006,.014,17)],(1,0,0))
 result['surfaces']['release_edge']=surface('MagRelease_Button',[(-.020,y,z) for y in np.linspace(.01215,.0127,9) for z in np.linspace(.006,.014,17)],(1,0,0))
 result['surfaces']['front_sight_top']=surface('Sight_Front',grid(np.linspace(-.001,.001,11),np.linspace(.1223,.1257,17),.075),(0,0,-1))
 result['surfaces']['palm_web']=surface('Frame_Grip',[(.030,y,z) for y in np.linspace(-.035,-.018,25) for z in np.linspace(.016,.030,25)],(-1,0,0))
 result['bake_ray_coverage']={k:v['alpha_missed_interior_texels'] for k,v in json.loads((BASE/'build/baked/4k/bake-report.json').read_text()).items() if isinstance(v,dict) and 'alpha_missed_interior_texels' in v}
 assert not a.keep_tangents or a.before,'--keep-tangents requires --before'
 if a.before:result['unchanged_delivery']=unchanged(a.before,a.keep_tangents)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2))
 print('SURFACE AUDIT',a.out,flush=True)


if __name__=='__main__':main()
