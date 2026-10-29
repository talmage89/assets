"""Kit UV/finalize and dense original sources for the form-normal bake."""
import sys,json,hashlib
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(BASE/'src'))
from kit import finalize,weapon as W

def main():
 out=BASE/'build/delivery';out.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/sxs.blend'))
 arm=bpy.data.objects['SXSArmature'];W.pose(arm,None,0)
 for ob in list(bpy.data.objects):
  if ob.get('bake_only'):bpy.data.objects.remove(ob,do_unlink=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'unpacked.blend'))
 # Unwrap the carved stock independently: a multi-object projection can
 # choose its clustering directions from unrelated action faces and fold
 # the stock's concave inlets. Regions share the same delivered atlas.
 master=[]
 for group,rect in [('stock',(.01,.01,.99,.47)),('assembly',(.01,.48,.99,.99))]:
  bpy.ops.wm.open_mainfile(filepath=str(out/'unpacked.blend'))
  for ob in list(bpy.context.scene.objects):
   if ob.type=='MESH' and (ob.name=='Stock_Walnut')!=(group=='stock'):
    bpy.data.objects.remove(ob,do_unlink=True)
  src=out/(group+'-source.blend');bpy.ops.wm.save_as_mainfile(filepath=str(src))
  cfg=out/(group+'-uv.py')
  cfg.write_text('from pathlib import Path\nimport runpy\nglobals().update(runpy.run_path('+repr(str(BASE/'src/config.py'))+'))\nUV_ATLAS_RECT='+repr(rect)+'\nUV_MIN_COVERAGE=.005\n'+("UV_SMART_ANGLE=20\n" if group=='stock' else ''))
  dst=out/(group+'-uv.blend')
  sys.argv=['blender','--','--source',str(src),'--out',str(dst),'--config',str(cfg),
   '--report',str(out/(group+'-uv.json')),'--size','2048','--target-density','100000','--margin','.002']
  finalize.main()
  master.append((dst,[(o.name,o.data.name) for o in bpy.context.scene.objects if o.type=='MESH']))
 bpy.ops.wm.open_mainfile(filepath=str(out/'unpacked.blend'))
 for path,mapping in master:
  with bpy.data.libraries.load(str(path),link=False) as (source,destination):destination.meshes=[mesh for name,mesh in mapping]
  for (name,_),mesh in zip(mapping,destination.meshes):bpy.data.objects[name].data=mesh
 from kit import uv
 report=uv.report([o for o in bpy.context.scene.objects if o.type=='MESH'],size=2048)
 assert report['overlap_fraction']<1e-5 and not report['outside_triangles'] and not report['degenerate_uv_triangles']
 (out/'uv.json').write_text(json.dumps(report,indent=2))
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'finalized.blend'))
 # Re-open the native source to retrieve our dense mesh datablocks, since the
 # finalizer loads a file and invalidates all Python RNA mesh references.
 with bpy.data.libraries.load(str(BASE/'build/sxs.blend'),link=False) as (source,destination):
  destination.objects=[name for name in source.objects if name.startswith('HIGH_')]
 for high in destination.objects:
  low=bpy.data.objects[high['low_target']];low.data=high.data.copy()
  low.vertex_groups.clear();g=low.vertex_groups.new(name=low['bone']);g.add(list(range(len(low.data.vertices))),1,'REPLACE')
  bpy.data.objects.remove(high,do_unlink=True)
 # Kit bake channel interface, entirely original constant inspection values.
 for mat in {m for ob in bpy.context.scene.objects if ob.type=='MESH' for m in ob.data.materials}:
  nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.name='SURFACE'
  nt.nodes.get('Material Output').name='OUT'
  for name,socket in [('base','Base Color'),('rough','Roughness'),('metal','Metallic')]:
   node=nt.nodes.new('ShaderNodeRGB' if name=='base' else 'ShaderNodeValue');node.name='OUT_'+name
   node.outputs[0].default_value=bs.inputs[socket].default_value
 bpy.context.scene['stage']='Original dense sources; constant form bake, finishes held'
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'high.blend'))
 (out/'prepare.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256((BASE/'build/sxs.blend').read_bytes()).hexdigest(),
  stage='form normal bake; no finish or wear acceptance'),indent=2))
if __name__=='__main__':main()
