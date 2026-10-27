"""Independently inspect embedded surfaces, moving hierarchy and shipped normals.

Source BVH sweeps establish mechanical clearance. Re-import pose comparisons
below establish that the same articulation survived consolidation and export.
"""
import argparse,hashlib,io,json,math,runpy,sys
from pathlib import Path
import bpy,numpy as np
from PIL import Image,ImageDraw,ImageFilter
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.gltf import GLB
from forms import side_x


def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(a.source);g=GLB(path);doc=g.json;errors=[]
 def check(ok,message):
  if not ok:errors.append(message)
 cfg=runpy.run_path(str(Path(__file__).with_name('config.py')))
 check(len(doc['materials'])==4,'Expected exactly four delivery surfaces')
 check(len(doc['images'])==3,'Expected exactly three shared images')
 check(len(doc['textures'])==3,'Duplicate texture views')
 def strings(value):
  if isinstance(value,str):yield value
  elif isinstance(value,dict):
   for item in value.values():yield from strings(item)
  elif isinstance(value,list):
   for item in value:yield from strings(item)
 check(not any(s.startswith(('~','file:')) or Path(s).is_absolute() for s in strings(doc)),'Machine path in GLB')
 images=[]
 for i,row in enumerate(doc['images']):
  im=Image.open(io.BytesIO(g.image(i)));check(im.size==(2048,2048),'Wrong embedded texture size')
  images.append(dict(name=row.get('name'),mode=im.mode,size=list(im.size),bytes=len(g.image(i))))
  if 'BaseColor' in row.get('name',''):
   check(im.mode=='RGBA','Missing paint coverage and emitter power alpha')
   alpha=np.asarray(im)[...,3];check(alpha.min()<100 and alpha.max()==255,'Coverage/power channel is flat')
 names={n['name']:i for i,n in enumerate(doc['nodes'])};parents={n:doc['nodes'][g.parents[i]]['name'] if i in g.parents else None for n,i in names.items()}
 for name in cfg['REQUIRED_NODES']:check(name in names,'Missing '+name)
 for name in [m['node'] for m in cfg['MOTIONS']]:
  check(parents.get(name+'Mesh')==name,'Rigid mesh detached from '+name)
 for side in ['L','R']:
  check(parents.get('Mirror_'+side)=='Door_F'+side,'Mirror detached from door')
  check(parents.get('Wheel_F'+side)=='Steer_F'+side,'Front wheel detached from kingpin')
 paint=next(m for m in doc['materials'] if m.get('extras',{}).get('paint_decode'))
 extras=paint['extras'];colors=json.loads(extras['paint_colors']);metals=json.loads(extras['paint_metallic'])
 check(set(colors)=={'Porcelain','Carbon','Aluminum','Graphite','Atlantic'},'Missing paint preset')
 check(abs(paint['pbrMetallicRoughness'].get('metallicFactor',1)-.12)<1e-6,'Lost factory metal factor')
 check('KHR_materials_clearcoat' in paint.get('extensions',{}),'Lost clearcoat')
 check(set(colors)==set(metals),'Missing metal preset')
 # Inspect actual paint atlas interiors. Clean texels must retain the default
 # factory tint, while low-body contamination must occupy the coverage channel.
 image_id=doc['textures'][paint['pbrMetallicRoughness']['baseColorTexture']['index']]['source']
 rgba=np.asarray(Image.open(io.BytesIO(g.image(image_id))),dtype=float)/255
 mask=Image.new('L',(2048,2048),0);draw=ImageDraw.Draw(mask);paint_index=doc['materials'].index(paint)
 for mesh in doc['meshes']:
  for primitive in mesh['primitives']:
   if primitive['material']!=paint_index:continue
   uv=g.accessor(primitive['attributes']['TEXCOORD_0']);indices=g.accessor(primitive['indices']).reshape(-1,3)
   for triangle in indices:draw.polygon([tuple(p*2048) for p in uv[triangle]],fill=255)
 valid=np.asarray(mask.filter(ImageFilter.MinFilter(5)))>0
 rgb=rgba[...,:3];linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
 alpha=rgba[...,3];clean=valid&(alpha==1);ref=np.array(extras['paint_reference_color'])
 tint_error=np.abs(np.median(linear[clean],axis=0)-ref)
 check(int(clean.sum())>10000 and float(tint_error.max())<.002,'Default factory tint lost in shared RGB')
 check(float(np.mean(alpha[valid]<.95))>.002,'Causal wear coverage lost in paint atlas')
 paint_texels=dict(interior_samples=int(valid.sum()),clean_samples=int(clean.sum()),clean_linear_median=np.median(linear[clean],axis=0).tolist(),tint_error=tint_error.tolist(),coverage_p5_p50_p95=np.percentile(alpha[valid],[5,50,95]).tolist(),fraction_below_95_percent=float(np.mean(alpha[valid]<.95)))
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
 imported={o.name:o for o in bpy.context.scene.objects};expected=json.loads(Path('build/export-report.json').read_text())
 axes={};basis={name:o.matrix_basis.copy() for name,o in imported.items() if o.type=='EMPTY'}
 for side in ['L','R']:
  node=imported['Steer_F'+side];v=(node.matrix_world.to_3x3()@Vector((0,0,1))).normalized();origin=node.matrix_world.translation
  ground=origin-v*(origin.z/v.z);hub=imported['Wheel_F'+side].matrix_world.translation
  axes[side]=dict(world_axis=list(v),origin_m=list(origin),sai_degrees=math.degrees(math.atan(abs(v.x)/v.z)),caster_degrees=math.degrees(math.atan(v.y/v.z)),scrub_m=abs(hub.x-ground.x),trail_m=hub.y-ground.y)
  check(abs(axes[side]['sai_degrees']-12)<.001 and abs(axes[side]['caster_degrees']-6.5)<.001,'Kingpin angles changed')
  check(abs(axes[side]['scrub_m']-.040)<1e-5 and abs(axes[side]['trail_m']-.045)<1e-5,'Kingpin ground geometry changed')
 pose=[]
 for spec in cfg['MOTIONS']:
  node=imported[spec['node']];rest=node.matrix_world.copy();source=Matrix(expected['nodes'][node.name]);maximum=0;tested=0
  descendants=[o for o in node.children_recursive if o.type=='MESH']
  points={o:[o.matrix_world@v.co for v in o.data.vertices] for o in descendants}
  lo,hi=spec['range'];count=math.ceil((hi-lo)/spec['step']);values=[lo+(hi-lo)*i/count for i in range(count+1)]
  # Check each complete swept range, sampling each mesh's spatial extremes.
  for angle in values:
   rotation=Matrix.Rotation(math.radians(angle),4,spec['axis']);node.matrix_basis=basis[node.name]@rotation;bpy.context.view_layer.update()
   intended=source@rotation@source.inverted()
   for ob in descendants:
    stride=max(1,len(ob.data.vertices)//64)
    for v in list(ob.data.vertices)[::stride]:
     wanted=intended@points[ob][v.index];actual=ob.matrix_world@v.co;maximum=max(maximum,(wanted-actual).length);tested+=1
  node.matrix_basis=basis[node.name];bpy.context.view_layer.update()
  check(maximum<2e-5,'Exported articulation differs: '+node.name)
  pose.append(dict(node=node.name,samples=len(values),vertex_samples=tested,max_error_m=maximum))
 normals=[]
 for ob in imported.values():
  if ob.type!='MESH':continue
  for face in ob.data.polygons:
   for li in face.loop_indices:
    p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
    n=ob.matrix_world.to_3x3()@ob.data.corner_normals[li].vector
    if not (.90<p.z<1.20 and -2.35<p.y<2.65) or n.x<.5 or abs(p.x-side_x(p.y,p.z))>.00001:continue
    e=1e-5;dy=(side_x(p.y+e,p.z)-side_x(p.y-e,p.z))/(2*e);dz=(side_x(p.y,p.z+e)-side_x(p.y,p.z-e))/(2*e)
    normals.append(math.degrees(n.angle(Vector((1,-dy,-dz)).normalized())))
 check(len(normals)>400 and max(normals)<.10,'Shipped side normals lost analytic continuity')
 sweeps={}
 for name in ['game','high']:
  row=json.loads(Path('build/motion-'+name+'.json').read_text());check(row['passed'] and len(row['motions'])==17,'Source sweep failed or incomplete')
  sweeps[name]=dict(passed=row['passed'],motions=len(row['motions']),samples=sum(m['samples'] for m in row['motions']),max_penetration_m=max(m['max_penetration_m'] for m in row['motions']))
 views={doc['accessors'][accessor]['bufferView'] for mesh in doc['meshes'] for primitive in mesh['primitives'] for accessor in [primitive['indices'],*primitive['attributes'].values()]}
 geometry_bytes=sum(doc['bufferViews'][i]['byteLength'] for i in views)
 primitives=sum(len(mesh['primitives']) for mesh in doc['meshes'])
 result=dict(passed=not errors,errors=errors,source=str(path),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),images=images,materials=len(doc['materials']),geometry_buffer_bytes=geometry_bytes,mesh_primitives=primitives,parents=parents,kingpins=axes,exported_motion=pose,source_clearance=sweeps,analytic_normal_max_degrees=max(normals),analytic_normal_samples=len(normals),paint_atlas_measurements=paint_texels,
  gpu_texture_mib_8bpp_with_mips=3*2048**2*4/3/1024**2,gpu_texture_mib_rgba8_with_mips=3*2048**2*4*4/3/1024**2)
 Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
 if errors:raise RuntimeError('Car delivery validation failed')
if __name__=='__main__':main()
