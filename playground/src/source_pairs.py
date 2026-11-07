"""Additional source-versus-export evidence; primary reviews use exported glTF.

Reconstruct the live scripted assembly before serialization under the same
calibrated cameras/light. No source blend or photographic texture is loaded.
"""
import sys,json,argparse,hashlib
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import build as B,geometry as F
from render import stage,camera,save,match_lighting
from setting import context
from labels import build as labels

p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=24)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for name,row in json.loads(Path('build/cameras.json').read_text()).items():
    source=Path('export')/row['source'];plan=json.loads(source.with_suffix('.json').read_text());shot=row['shot']
    sc=stage(source,a.width,a.samples,shot['aspect'])
    # Keep only the lighting configuration. All equipment below is generated
    # live by the source functions, independently of the imported glTF meshes.
    for ob in list(sc.objects):
        if ob.type!='LIGHT':bpy.data.objects.remove(ob,do_unlink=True)
    F.init(True);roots,report=B.library();rt=F.root('Live source '+str(plan['seed']))
    for i,m in enumerate(plan['modules']):
        ob=F.clone(roots[m['kind']],f'{m["kind"]}_{i:03}',m['pos'],m['yaw'],tint=plan);ob.parent=rt;ob['zone_group']=m['group']
    ground=F.root('Siteworks');ground.parent=rt;B.surface(ground,plan);F.finish(ground);labels(rt,plan);B.context(rt,plan)
    for root in roots.values():
        for ob in B.members(root):bpy.data.objects.remove(ob,do_unlink=True)
    context(plan,photo_view=name)
    # Compare source manufacture fields against the shipped filtered maps.
    # The analytic source and game geometry are the same here. Color/ORM use
    # the original generated 4096 fields; normals use the calibrated 4096
    # bake before filtering, so this exposes filtering/serialization loss,
    # rather than pretending there was a high-poly projection step.
    source_maps={}
    for mat in bpy.data.materials:
        if not mat.use_nodes:continue
        for node in mat.node_tree.nodes:
            if node.type!='TEX_IMAGE' or node.image is None:continue
            im=node.image;filename=Path(im.filepath).name
            if not filename.startswith('T_Play') or not filename.endswith('.png'):continue
            folder=Path('textures/bake') if '_Normal' in filename else Path('build/procedural')
            path=folder/filename
            if not path.exists():continue
            # glTF's importer can retain a packed copy. Load a distinct source
            # image rather than reloading that packed 1024/2048 datablock.
            high=bpy.data.images.load(str(path.resolve()),check_existing=True)
            high.colorspace_settings.name=im.colorspace_settings.name;node.image=high
            assert tuple(high.size)==(4096,4096),(filename,tuple(high.size))
            source_maps[str(path)]=dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),size=list(high.size))
    assert len(source_maps)==9,list(source_maps)
    match_lighting(sc,name)
    camera(sc,shot['location'],shot['target'],shot['lens'],roll=shot['roll'])
    output=Path('renders/source-matches')/(name+'.png');save(sc,output,source,name)
    meta=json.loads(output.with_suffix('.json').read_text());meta['stage']='LIVE scripted source / original 4096 fields and prefilter normals';meta['scope']='Source URI identifies matching export; rendered equipment is generated live, color/ORM are original fields, normals are the 4096 bake before filtering. Analytic geometry is shared, with no high-poly projection step.';meta['source_map_inputs']=list(source_maps.values());output.with_suffix('.json').write_text(json.dumps(meta,indent=2))
