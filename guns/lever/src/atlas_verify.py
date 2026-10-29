"""Independent baked delivery audit: surfaces, UVs, textures and clips."""
import sys,json,hashlib,io,argparse
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree
from PIL import Image
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W,weapon_verify as V,uv
from kit.gltf import GLB
from interface import CLIPS
from check import geometry,contacts,semantics,sweep,parts
def named_reference(arm):
 W.pose(arm,None,0);records=[];templates={};trees={};corners={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or ob.parent!=arm or 'bone' not in ob or ob.get('bake_only'):continue
  templates[ob.name]={k:ob[k] for k in ob.keys()};ob.data.calc_loop_triangles()
  for face in ob.data.loop_triangles:
   points=[ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]
   corners[len(records)]=([ob.matrix_world.to_3x3()@ob.data.corner_normals[i].vector for i in face.loops],
                         [ob.data.uv_layers['BakeUV'].data[i].uv.copy() for i in face.loops])
   records.append((ob.name,ob['bone'],points))
 for bone in {r['bone'] for r in templates.values()}:
  selected=[(i,r) for i,r in enumerate(records) if r[1]==bone];tree=KDTree(len(selected))
  for i,row in selected:tree.insert(sum(row[2],Vector())/3,i)
  tree.balance();trees[bone]=tree
 return records,templates,trees,corners

def raw_corners(glb,reference):
 """Check delivered FLOAT normals before Blender re-encodes custom fans."""
 records,templates,trees,corners=reference;seen=set();maxn=maxp=maxuv=0.
 names=[glb.json['nodes'][i]['name'] for i in glb.json['skins'][0]['joints']]
 for node in glb.json['nodes']:
  if 'mesh' in node:assert not any(k in node for k in ('matrix','translation','rotation','scale'))
 for mesh in glb.json['meshes']:
  for primitive in mesh['primitives']:
   attrs=primitive['attributes'];position=glb.accessor(attrs['POSITION']);normal=glb.accessor(attrs['NORMAL'])
   tex=glb.accessor(attrs['TEXCOORD_0']);joints=glb.accessor(attrs['JOINTS_0']);weights=glb.accessor(attrs['WEIGHTS_0'])
   for tri in glb.accessor(primitive['indices']).reshape(-1,3):
    points=[Vector((position[i][0],-position[i][2],position[i][1])) for i in tri]
    normals=[Vector((normal[i][0],-normal[i][2],normal[i][1])) for i in tri]
    uvs=[Vector((tex[i][0],1-tex[i][1])) for i in tri]
    owners=[names[int(joints[i][weights[i].argmax()])] for i in tri];assert len(set(owners))==1
    matches=[]
    for _,index,distance in trees[owners[0]].find_range(sum(points,Vector())/3,2e-7):
     if index in seen:continue
     name,_,expected=records[index];source_n,source_uv=corners[index]
     for shift in range(3):
      pe=max((points[k]-expected[(k+shift)%3]).length for k in range(3))
      ne=max((normals[k]-source_n[(k+shift)%3]).length for k in range(3))
      ue=max((uvs[k]-source_uv[(k+shift)%3]).length for k in range(3))
      if pe<2e-7 and ne<1e-4 and ue<2e-6:matches.append((pe,ne,ue,index))
    assert matches,(owners[0],'raw delivered corner mismatch',list(sum(points,Vector())/3))
    pe,ne,ue,index=min(matches);seen.add(index);maxp=max(maxp,pe);maxn=max(maxn,ne);maxuv=max(maxuv,ue)
 assert len(seen)==len(records)
 return dict(triangles=len(seen),maximum_vertex_delta_m=maxp,maximum_normal_vector_delta=maxn,maximum_uv_delta=maxuv,
  scope='raw delivered FLOAT positions/normals and UVs, before Blender custom-normal fan re-encoding')

def restore_diagnostics(arm,reference,normal_tolerance=.01745):
 records,templates,trees,corners=reference;W.pose(arm,None,0);mapped={name:[] for name in templates};seen=set();maximum=0.;maxnormal=0.;maxuv=0.
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
  ob.data.calc_loop_triangles();normals=ob.data.corner_normals
  for triangle in ob.data.loop_triangles:
   points=[ob.matrix_world@ob.data.vertices[i].co for i in triangle.vertices]
   owners=[]
   for i in triangle.vertices:
    group=max(ob.data.vertices[i].groups,key=lambda g:g.weight);owners.append(ob.vertex_groups[group.group].name)
   assert len(set(owners))==1,owners
   bone=owners[0];center=sum(points,Vector())/3
   actual_normals=[ob.matrix_world.to_3x3()@normals[i].vector for i in triangle.loops]
   actual_uv=[ob.data.uv_layers.active.data[i].uv.copy() for i in triangle.loops]
   matches=[];rejected=[]
   for _,index,distance in trees[bone].find_range(center,2e-7):
    if index in seen:continue
    name,_,expected=records[index]
    for shift in range(3):
     error=max((points[k]-expected[(k+shift)%3]).length for k in range(3))
     if error>=2e-7:continue
     source_normals,source_uv=corners[index]
     normal_error=max((actual_normals[k]-source_normals[(k+shift)%3]).length for k in range(3))
     uv_error=max((actual_uv[k]-source_uv[(k+shift)%3]).length for k in range(3))
     rejected.append((name,index,shift,error,normal_error,uv_error))
     # The raw FLOAT check above retains the strict 0.006-degree bound.
     # Importer fan re-encoding amplifies error at near-degenerate Boolean
     # cuts; separately bound that reconstruction below one degree.
     if normal_error<normal_tolerance and uv_error<2e-6:matches.append((error,index,name,normal_error,uv_error))
   assert matches,(bone,'no unused oriented source triangle at imported centroid',list(center),rejected)
   error,index,name,normal_error,uv_error=min(matches);maximum=max(maximum,error);maxnormal=max(maxnormal,normal_error);maxuv=max(maxuv,uv_error);seen.add(index)
   mapped[name].append((points,[ob.matrix_world.to_3x3()@normals[i].vector for i in triangle.loops]))
  bpy.data.objects.remove(ob,do_unlink=True)
 assert len(seen)==len(records),(len(seen),len(records))
 for name,faces in mapped.items():
  vertices=[tuple(p) for points,n in faces for p in points]
  mesh=bpy.data.meshes.new('Imported diagnostic '+name)
  mesh.from_pydata(vertices,[],[(i*3,i*3+1,i*3+2) for i in range(len(faces))]);mesh.update()
  mesh.normals_split_custom_set([tuple(n) for points,normals in faces for n in normals])
  ob=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(ob)

  for key,value in templates[name].items():ob[key]=value
  # Restore indexed vertices for the independent manifold-solid audit. Corner
  # normals remain face-corner data, including discontinuous hard edges.
  attr=mesh.attributes.new('SavedNormal','FLOAT_VECTOR','CORNER')
  attr.data.foreach_set('vector',[a for r in mesh.corner_normals for a in r.vector])
  bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8);bm.to_mesh(mesh);bm.free()
  mesh.normals_split_custom_set([r.vector[:] for r in mesh.attributes['SavedNormal'].data]);mesh.attributes.remove(mesh.attributes['SavedNormal'])
  W.rigid_bind(ob,arm,templates[name]['bone'])
 return dict(parts=len(mapped),triangles=len(seen),maximum_vertex_delta_m=maximum,maximum_normal_vector_delta=maxnormal,maximum_uv_delta=maxuv,
  scope='actual imported triangles matched one-to-one by rigid owner, oriented vertices, corner normals and UVs')


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=('all','serialization','construction'),default='all')
 args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 stamp=dict(glb_sha256=hashlib.sha256((BASE/'export/lever.glb').read_bytes()).hexdigest(),
            finalized_sha256=hashlib.sha256((BASE/'build/delivery/finalized.blend').read_bytes()).hexdigest())
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 arm=bpy.data.objects['LeverArmature'];objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]
 W.pose(arm,None,0);u=uv.report(objects,size=2048)
 assert not u['outside_triangles'] and not u['degenerate_uv_triangles'] and u['overlap_fraction']<1e-5,u
 assert u['coverage']>.20,u['coverage']
 source_states=semantics(arm);reference=named_reference(arm)
 samples=[(c,i*.5) for c,s in CLIPS.items() for i in range(s['frames']*2+1)]
 expected=V.capture(arm,samples,[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]) if args.stage!='construction' else None
 surfaces={}
 if args.stage!='construction':
  for c,s in CLIPS.items():
   for frame in sorted({0,s['frames'],*s['events'].values()}):
    W.pose(arm,c,frame);surfaces[c,frame]=V.surface_points(parts())
 print('ATLAS AUDIT',args.stage,'source frames and UVs captured',flush=True)
 baked=json.loads((BASE/'build/baked/4k/bake-report.json').read_text())
 assert baked['size']==4096 and baked['samples']>=32
 for channel in ('BaseColor','Roughness','Metallic','AO','MaterialAO','Normal'):
  assert baked[channel]['alpha_missed_interior_texels']==0,(channel,baked[channel])
 channels=('BaseColor','Normal','ORM')
 canonical=sorted(hashlib.sha256((BASE/'textures'/('T_BrackenL20_'+c+'.png')).read_bytes()).hexdigest() for c in channels)
 # Wood has no metallic source anywhere. Test its complete reserved regions,
 # including padding and subpixel UV tips that interior-erosion checks omit.
 packed=np.asarray(Image.open(BASE/'textures/T_BrackenL20_ORM.png').convert('RGB'))
 wood_regions={}
 for name in ('stock','forend'):
  region=json.loads((BASE/'build/delivery'/(name+'-uv.json')).read_text())['unique_region']['rectangle']
  x0,y0,x1,y1=region
  values=packed[round((1-y1)*2048):round((1-y0)*2048),round(x0*2048):round(x1*2048),2]
  maximum=int(values.max());assert maximum<=2,(name,'metal contamination in walnut region',maximum)
  wood_regions[name]=dict(rectangle=region,maximum_metallic_byte=maximum,pixels=int(values.size))
 records={}
 for name,limit in [('lever',40000),('cartridge',1600),('case',1600)]:
  path=BASE/'export'/(name+'.glb');g=GLB(path)
  triangles=sum(len(g.accessor(p['indices']))//3 for m in g.json['meshes'] for p in m['primitives'])
  assert triangles<=limit and len(g.json['materials'])==1 and len(g.json['images'])==3
  assert sorted(hashlib.sha256(g.image(i)).hexdigest() for i in range(3))==canonical
  for i in range(3):assert Image.open(io.BytesIO(g.image(i))).size==(2048,2048)
  normal=V.normal_direction(g)
  for mesh in g.json['meshes']:
   for primitive in mesh['primitives']:
    attrs=primitive['attributes'];position=g.accessor(attrs['POSITION']);normals=g.accessor(attrs['NORMAL'])
    assert np.isfinite(position).all() and np.isfinite(normals).all()
    assert np.max(np.abs(np.linalg.norm(normals,axis=1)-1))<1e-5
    if name=='lever':
     weights=g.accessor(attrs['WEIGHTS_0'])
     assert np.all(np.sum(weights>1e-6,axis=1)==1) and np.max(np.abs(weights.sum(axis=1)-1))<1e-6
  if name=='lever':
   assert {a['name'] for a in g.json['animations']}==set(CLIPS)
   for clip in g.json['animations']:
    times=[g.accessor(s['input']) for s in clip['samplers']]
    duration=max(float(t.max()) for t in times)-min(float(t.min()) for t in times)
    assert abs(duration-CLIPS[clip['name']]['frames']/60)<1e-5
   raw_proof=raw_corners(g,reference)
   arm=V.import_glb(path)
   records[name]=dict(triangles=triangles,bytes=path.stat().st_size,materials=1,texture_images=3,normal_direction=normal,
    stage=args.stage,raw_corner_correspondence=raw_proof)
   if args.stage!='construction':
    affine=V.compare(arm,expected,position_tolerance_m=3e-6,linear_tolerance=2e-5)
    print('ATLAS AUDIT affine frames compared',len(affine),flush=True);deltas=[]
    for i,((clip,frame),points) in enumerate(surfaces.items()):
     W.pose(arm,clip,frame);delta=V.surface_delta(points,V.surface_points([o for o in bpy.context.scene.objects if o.type=='MESH']))
     assert delta<3e-6,(clip,frame,delta);deltas.append(delta)
     if i%40==0:print('ATLAS AUDIT posed surfaces',i+1,'/',len(surfaces),flush=True)
    records[name].update(affine_samples=len(affine),maximum_position_delta_m=max(r['position_delta_m'] for r in affine),maximum_surface_delta_m=max(deltas))
   if args.stage!='serialization':
    reconstruction=restore_diagnostics(arm,reference)
    print('ATLAS AUDIT actual imported triangle correspondence',reconstruction,flush=True)
    geo=geometry(arm);contact=contacts(arm);states=semantics(arm);motion=sweep(arm)
    assert all(row['passed'] for row in contact) and motion['passed'] and not geo['nonmanifold']
    records[name].update(imported_reconstruction=reconstruction,geometry=geo,contacts=contact,states=states,motion=motion)
  else:
   assert not g.json.get('skins') and not g.json.get('animations')
   V.import_glb(path);obs=[o for o in bpy.context.scene.objects if o.type=='MESH'];points=np.asarray(V.surface_points(obs))
   lo,hi=points.min(0),points.max(0);length=.06477 if name=='cartridge' else .0518
   assert abs(hi[1]-length)<1e-6 and -.00005<lo[1]<1e-6 and abs(hi[0]-lo[0]-.01285)<1e-6
   records[name]=dict(triangles=triangles,bytes=path.stat().st_size,materials=1,texture_images=3,normal_direction=normal,dimensions_m=(hi-lo).tolist())
 result=dict(passed=True,source_identity=stamp,uv=u,exports=records,canonical_sha256=canonical,wood_regions=wood_regions,
  textures={c:dict(bytes=(BASE/'textures'/('T_BrackenL20_'+c+'.png')).stat().st_size,size=[2048,2048]) for c in channels},
  compressed_three_map_mib_with_mips=16,
  scope='Independent imported-surface construction and clearance; affine/surface agreement separately proves serialization.')
 if args.stage=='serialization':
  (BASE/'build/delivery/verify-serialization.json').write_text(json.dumps(result,indent=2))
 else:
  if args.stage=='construction':
   earlier=json.loads((BASE/'build/delivery/verify-serialization.json').read_text());assert earlier['passed'] and earlier['source_identity']==stamp
   for name,row in records.items():earlier['exports'][name].update(row)
   result=earlier;result['exports']['lever']['stage']='serialization + independent imported construction'
  (BASE/'build/delivery/verify.json').write_text(json.dumps(result,indent=2))
 print('BRACKEN FINAL VERIFIED',[(n,r['triangles'],r['bytes']) for n,r in records.items()],flush=True)
if __name__=='__main__':main()
