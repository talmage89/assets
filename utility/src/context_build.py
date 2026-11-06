"""Prepare library context in utility/build; never write a neighboring delivery."""
import argparse,importlib.util,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from kit import model as G


def ground(out):
    sys.path.insert(0,str(ROOT/'ground/src'))
    spec=importlib.util.spec_from_file_location('utility_ground',ROOT/'ground/src/build.py')
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    for name,color in [('Asphalt',(.065,.072,.075)),('Concrete',(.37,.36,.32)),('Lawn',(.065,.105,.025)),('GroundTrim',(.04,.035,.026))]:
        m=bpy.data.materials.new('Context_'+name);m.use_nodes=True
        bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.9
        if name in ('Asphalt','Concrete','Lawn'):
            ns,ls=m.node_tree.nodes,m.node_tree.links
            ground_uv=None
            if name=='Lawn':
                position=ns.new('ShaderNodeNewGeometry');scale=ns.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs['Scale'].default_value=1/3.048
                ls.new(position.outputs['Position'],scale.inputs[0]);ground_uv=scale.outputs['Vector']
            for channel in ('BaseColor','ORM','Height'):
                path=out.parent/'ground-fields'/f'T_{name}_{channel}.png'
                n=ns.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(path.resolve()),check_existing=True);n.image.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
                if ground_uv:ls.new(ground_uv,n.inputs['Vector'])
                if channel=='BaseColor':ls.new(n.outputs['Color'],bs.inputs['Base Color'])
                elif channel=='ORM':
                    sep=ns.new('ShaderNodeSeparateColor');ls.new(n.outputs['Color'],sep.inputs[0]);ls.new(sep.outputs['Green'],bs.inputs['Roughness'])
                else:
                    bump=ns.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.004 if name!='Lawn' else .012
                    ls.new(n.outputs['Color'],bump.inputs['Height']);ls.new(bump.outputs['Normal'],bs.inputs['Normal'])
        module.MATS[name]=m
    roots=[module.road('Road_Straight_A',0),module.curb('Curb_Straight'),module.sidewalk('Sidewalk_A')]
    # Native modules include actual gutter profile, walk scores and lawn skin.
    # Lawn presentation below is a simple original plane, no downloaded maps.
    rt=G.pivot('Lawn_Field',(0,0,0));o=G.box('Grass soil skin',(0,0,-.025),(1,1,.05),module.MATS['Lawn'],0);o.parent=rt
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))


def pickup(out):
    # The retained pickup form entry omits several diagnostic material keys.
    # Supply a presentation-only fallback here; the car scripts stay unchanged.
    from collections import defaultdict
    sys.path.insert(0,str(ROOT/'cars/src'))
    spec=importlib.util.spec_from_file_location('utility_pickup',ROOT/'cars/src/build.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    b=module.Build(False,detail=False)
    b.m=defaultdict(lambda:b.m['wheel'],b.m)
    module.body.build(b);module.wheels.build(b,module.S)
    for o in bpy.context.scene.objects:
        if o.type=='MESH':G.apply(o)
    bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--role',default='ground');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    (pickup if a.role=='pickup' else ground)(a.out)
