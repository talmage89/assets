"""Instance the repository's original boxwood faces and canonical maps.

Loaded after static consolidation. Bark and leaf faces share the stock mask
material (bark alpha is opaque), then join locally into one instanced mesh.
No library file or texture changes; no new botanical vertices or pixels.
"""
import hashlib,math,random
from pathlib import Path
import bpy
from geometry import root


def plant(p,station):
 path=Path(__file__).resolve().parents[2]/'shrubs/export/Shrubs.glb'
 if not path.exists():raise RuntimeError('Build shrubs with its own Makefile first')
 before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path))
 added=set(bpy.context.scene.objects)-before
 stock=sorted((o for o in added if o.type=='MESH' and o.name.startswith('Boxwood')),key=lambda o:o.name)
 assert len(stock)==2,'Stock shrub library layout changed'
 mask=bpy.data.materials['Shrubs .001']
 for ob in stock:
  ob.data.materials.clear();ob.data.materials.append(mask)
 bpy.ops.object.select_all(action='DESELECT')
 for ob in stock:ob.select_set(True)
 bpy.context.view_layer.objects.active=stock[0];bpy.ops.object.join()
 stock=[bpy.context.object];added=set(bpy.context.scene.objects)-before
 lib=[(o.data,o.matrix_world.copy()) for o in stock]
 for o in added:bpy.data.objects.remove(o,do_unlink=True)
 parent=root('Landscape',kind='Landscape',parent=station);parent['reusable_module']=True
 W,D=p['lot'];b=p['building'];rng=random.Random(4000+p['seed']);locations=[]
 for i in range(13):locations.append((W/2-.65,-D/2+2.2+i*(D-4.4)/12))
 start=-W/2+5.9
 for i in range(12):
  x=start+i*(W/2-1.8-start)/11
  if abs(x-b['center_x'])<b['width']/2+1:continue
  locations.append((x,D/2-.65))
 for i,(x,y) in enumerate(locations):
  rt=root('Boxwood_'+str(i),(x,y,.016),rng.uniform(0,360),parent=parent)
  rt.location.z-=rng.uniform(0,.025)
  for j,(mesh,xf) in enumerate(lib):
   ob=bpy.data.objects.new(f'Boxwood_{i}_{j}',mesh);bpy.context.collection.objects.link(ob)
   ob.parent=rt;ob.matrix_basis=xf;ob['asset_set']='Landscape';ob['module_root']='Landscape'
 return dict(source='shrubs/export/Shrubs.glb',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),instances=len(locations),shared_meshes=len(lib),shared_images=3,reused_gpu_mib=16)
