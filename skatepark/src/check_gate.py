"""Sample the relocated entry gate against actual fence and entry fixtures."""
import json,sys
from pathlib import Path
import bpy
from mathutils import Matrix
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.motion import sweep

def check(seed=202):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    path=Path(f'export/final/Park_{seed}.gltf');bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    roots=[o for o in bpy.context.scene.objects if not o.parent]
    fence=next(o for o in roots if o.name=='PerimeterFence')
    gate=next(o for o in fence.children_recursive if o.get('pivot_axis')=='Z')
    latch=next(o for o in gate.children_recursive if o.get('pivot_axis')=='Y')
    assert list(gate['range_degrees'])==[-110,0] and list(latch['range_degrees'])==[-95,0]
    for root in roots:
        relevant=root==fence or root.name.startswith(('RulesSign','BikeRack','DrinkingFountain','Litter'))
        for ob in [root,*root.children_recursive]:
            if ob.type!='MESH':continue
            if relevant:ob['asset_set']='EntryClearance'
            elif 'asset_set' in ob:del ob['asset_set']
    # Raise the fork before opening, as the real latch operates.
    latch.matrix_basis=latch.matrix_basis@Matrix.Rotation(-95*3.141592653589793/180,4,'Y')
    bpy.context.view_layer.update()
    cfg=dict(MOTIONS=[dict(node=gate.name,axis='Z',range=[-110,0],step=2,tolerance_m=.0005,
        allow=[dict(moving=gate.name.split('.')[0]+'_Mesh',fixed='Chain_GatePost_Hinge',reason='Native hinge barrels and their shared pin axis')])])
    result=sweep(cfg);result.update(seed=seed,scope='Actual imported gate frame, raised fork, fence and entry fixture solids. Two-degree sampling; not a continuous collision guarantee. Native hinge contact excluded explicitly.')
    Path('build/gate-clearance.json').write_text(json.dumps(result,indent=2));assert result['passed'],result
if __name__=='__main__':check()
