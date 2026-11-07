"""Additional source-versus-export evidence; primary reviews use exported glTF.

Reconstruct the live scripted assembly before serialization under the same
calibrated cameras/light. No source blend or photographic texture is loaded.
"""
import sys,json,argparse
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import build as B,geometry as F
from render import stage,camera,save
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
    context(plan)
    sun=next(o for o in sc.objects if o.type=='LIGHT' and o.data.type=='SUN')
    if 'swings' in name:sun.data.energy=.15;sc.world.node_tree.nodes['Background'].inputs[1].default_value=.32
    elif 'stair' in name:sun.data.energy=.35;sc.world.node_tree.nodes['Background'].inputs[1].default_value=.28
    else:sun.data.energy=2.2
    camera(sc,shot['location'],shot['target'],shot['lens'],roll=shot['roll'])
    output=Path('renders/source-matches')/(name+'.png');save(sc,output,source,name)
    meta=json.loads(output.with_suffix('.json').read_text());meta['stage']='LIVE script-generated source before glTF serialization';meta['scope']='Reference source URI identifies matching export/maps, not the rendered equipment meshes';output.with_suffix('.json').write_text(json.dumps(meta,indent=2))
