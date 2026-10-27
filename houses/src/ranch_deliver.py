"""Add ranch seeds and sixteen new maps to the unchanged colonial delivery."""
import argparse,json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import tiling
from lookdev import materials
from deliver import externalize
from glb_budget import compact,read
from ranch_uv import resolve


def export_house(seed):
 source=Path(f'build/ranch/house-{seed}.blend');bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
 meta=json.loads(source.with_suffix('.json').read_text());ship=Path('textures/ranch-ship')
 from ranch_reduce import reduce as reduce_weather
 meta['weather_reduction']={}
 optimize=meta['triangles']>40000
 meta['weather_reduction_enabled']=optimize
 from mathutils import Vector
 chimney=bpy.data.objects.get('Brick_Chimney')
 if chimney:
  points=[chimney.matrix_world@v.co for v in chimney.data.vertices]
  lo=Vector(tuple(min(p[k] for p in points) for k in range(3)));hi=Vector(tuple(max(p[k] for p in points) for k in range(3)))
  center=(lo+hi)/2;center.z=hi.z-.45
  meta['chimney_camera']=dict(location=tuple(center+Vector((3,-4,2))),target=tuple(center),lens=52,aspect=1.3)
 original=materials(Path('textures/ship'))
 brick=tiling.material('RanchBrick_'+meta['spec']['brick_color'],ship,tint=True)
 roof=tiling.material('RanchRoof',ship,tint=True)
 for node in original['Trim'].node_tree.nodes:
  if node.type=='TEX_IMAGE' and node.image and '_ORM' in node.image.name:
   node.image=bpy.data.images.load(str((ship/'T_RanchTrim_ORM.png').resolve()),check_existing=True);node.image.colorspace_settings.name='Non-Color'
 glass=original['Glass'];p=glass.node_tree.nodes.get('Principled BSDF')
 for socket in ('Base Color',):
  for link in list(p.inputs[socket].links):glass.node_tree.links.remove(link)
 # Keep the canonical ORM on glass; glTF's ordinary roughness factor brings
 # its 9/255 clear strip to the accepted .025 without repacking that image.
 rough=p.inputs['Roughness'].links[0].from_socket
 mul=glass.node_tree.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=.025/(9/255)
 glass.node_tree.links.new(rough,mul.inputs[0]);glass.node_tree.links.new(mul.outputs[0],p.inputs['Roughness'])
 p.inputs['Base Color'].default_value=(.94,.97,.94,1);p.inputs['Roughness'].default_value=.025
 charts={}
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH':continue
  has_roof=any(ob.data.materials[p.material_index].name=='RanchRoof' for p in ob.data.polygons)
  if has_roof:charts[ob.name]=resolve(ob,meta['spec']['roof_age']=='newer',optimize)
  reduced=reduce_weather(ob,meta) if optimize else None
  if reduced:meta['weather_reduction'][ob.name]=reduced
  for i,mat in enumerate(ob.data.materials):
   name=mat.name.split('.')[0]
   if name=='RanchBrick':ob.data.materials[i]=brick
   elif name=='RanchRoof':ob.data.materials[i]=roof
   else:
    role=name.removeprefix('House')
    assert role in original,(ob.name,name)
    ob.data.materials[i]=original[role]
 # Moderately detailed houses retain their original packet addressing. Stop
 # coarsening as soon as their delivered count reaches the median target.
 if not optimize:
  objects=sorted((o for o in bpy.context.scene.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons),reverse=True)
  total=sum(len(o.data.polygons) for o in objects)
  for ob in objects:
   if total<=55000:break
   reduced=reduce_weather(ob,meta)
   if reduced:
    meta['weather_reduction'][ob.name]=reduced;total+=reduced['after']-reduced['before']
 # Drop unbound source shaders before assigning stable material IDs.
 keep=set(original.values())|{roof,brick}|{m for o in bpy.context.scene.objects if o.type=='MESH' for m in o.data.materials}
 for mat in list(bpy.data.materials):
  if mat not in keep:bpy.data.materials.remove(mat,do_unlink=True)
 for key,mat in original.items():mat.name='House'+key
 roof.name='RanchRoof';brick.name='RanchBrick_'+meta['spec']['brick_color']
 triangles=sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH')
 meta.update(stage='baked ranch delivery; shared external images',triangles=triangles,roof_charts=charts)
 game=Path(f'build/ranch/delivery/game-{seed}.blend');game.with_suffix('.json').write_text(json.dumps(meta,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(game.resolve()))
 moving={o for o in bpy.context.scene.objects if o.name in ('FrontDoor','PatioDoor','ServiceDoor')}
 static=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent not in moving]
 bpy.ops.object.select_all(action='DESELECT')
 for o in static:o.select_set(True)
 bpy.context.view_layer.objects.active=static[0];bpy.ops.object.join();static[0].name='House_Static'
 embedded=Path(f'build/ranch/delivery/house-{seed}.glb');tiling.export(embedded);compact(embedded)
 # Image names are matched by content against both canonical baked folders.
 folder=Path('build/ranch/delivery/images');folder.mkdir(parents=True,exist_ok=True)
 for parent in (Path('textures/ship'),ship):
  for file in parent.glob('*.png'):
   target=folder/file.name
   if not target.exists() or target.read_bytes()!=file.read_bytes():target.write_bytes(file.read_bytes())
 out=Path(f'export/HearthfieldRanch-{seed}.gltf');sizes=externalize(embedded,out,folder,max_images=16)
 out.with_suffix('.json').write_text(json.dumps(meta,indent=2))
 doc,_=read(embedded);row=dict(seed=seed,triangles=triangles,materials=len(doc['materials']),meshes=len(doc['meshes']),roof_charts=charts,**sizes)
 print('RANCH_DELIVERED',seed,triangles,sizes['gltf_bytes']+sizes['bin_bytes'],flush=True)
 return row


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seeds',default='11,12,13,14,15,16');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 folder=Path('export/textures');folder.mkdir(parents=True,exist_ok=True)
 for parent in (Path('textures/ship'),Path('textures/ranch-ship')):
  for file in parent.glob('T_*.png'):
   target=folder/file.name
   if not target.exists() or target.read_bytes()!=file.read_bytes():target.write_bytes(file.read_bytes())
 rows=[export_house(s) for s in dict.fromkeys(map(int,a.seeds.split(',')))]
 files=list(folder.glob('*.png'));assert len(files)==31
 Path('build/ranch/delivery/delivery.json').write_text(json.dumps(dict(rows=rows,shared_images=len(files),shared_png_bytes=sum(f.stat().st_size for f in files),total_geometry_bytes=sum(r['gltf_bytes']+r['bin_bytes'] for r in rows)),indent=2))
