"""Full declared module ranges, using the kit's actual solid-surface sampler."""
import json
import argparse
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit import motion


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--lookdev',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    prefix=Path('export/lookdev') if a.lookdev else Path('export')
    output=Path('build/lookdev/motion-check.json') if a.lookdev else Path('build/motion-check.json')
    rows=[]
    for name in ('Gate','Tower3','Tower','Tower5'):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(prefix/'modules'/(name+'.gltf')))
        specs=[]
        for pv in bpy.context.scene.objects:
            if pv.get('slide_axis'):
                specs.append(dict(node=pv.name,axis=pv['slide_axis'],kind='translation',range=list(pv['range_m']),step=.06,tolerance_m=.0005))
            elif pv.get('pivot_axis'):
                spec=dict(node=pv.name,axis=pv['pivot_axis'],range=list(pv['range_degrees']),step=5,tolerance_m=.0005)
                if 'GateArm' in pv.name:spec['allow']=[dict(moving='Gate__Arm',fixed='Gate__Housing',reason='Authored axle and sleeve occupy their actual shared hinge volume')]
                specs.append(spec)
        report=motion.sweep(dict(MOTIONS=specs));rows.append(dict(module=name,**report))
        output.write_text(json.dumps(dict(modules=rows,passed=all(r['passed'] for r in rows)),indent=2)+'\n')
    for seed in (101,202):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(prefix/(f'ParkingGarageLook-{seed}.gltf' if a.lookdev else f'ParkingGarage-{seed}.gltf')))
        specs=[]
        for pv in bpy.context.scene.objects:
            if not (pv.get('pivot_axis') or pv.get('slide_axis')):continue
            # Module checks cover every authored storey. Placed checks cover
            # the ground-level adjacency, where graded floors/public walks
            # differ from the isolated tower and the gate has a roof nearby.
            if 'GateArm' not in pv.name and 'StreetDoor' not in pv.name and '_L1' not in pv.name:continue
            if pv.get('slide_axis'):spec=dict(node=pv.name,axis=pv['slide_axis'],kind='translation',range=list(pv['range_m']),step=.06,tolerance_m=.0005)
            else:spec=dict(node=pv.name,axis=pv['pivot_axis'],range=list(pv['range_degrees']),step=5,tolerance_m=.0005)
            if 'GateArm' in pv.name:
                gate_prefix=pv.name.split('__')[0]
                spec['allow']=[dict(moving=gate_prefix+'__Gate__Arm',fixed=gate_prefix+'__Gate__Housing',reason='Authored axle and sleeve hinge volume')]
            specs.append(spec)
        rows.append(dict(module='PlacedGarage'+str(seed),**motion.sweep(dict(MOTIONS=specs))))
        output.write_text(json.dumps(dict(modules=rows,passed=all(r['passed'] for r in rows)),indent=2)+'\n')
    assert all(r['passed'] for r in rows),[r for r in rows if not r['passed']]
    print('MODULE MOTION PASS',sum(len(r['motions']) for r in rows),'pivots',flush=True)


if __name__=='__main__':main()
