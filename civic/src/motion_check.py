"""Sample actual source and imported door surfaces; guide contact is explicit."""
import json,sys,importlib.util
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from kit.motion import sweep,surface,penetration
from kit import motion
from door_motion import pose
saved=sys.path[:];sys.path.insert(0,str(HERE.parents[1]/'downtown/src'))
spec=importlib.util.spec_from_file_location('_civic_native_membership',HERE.parents[1]/'downtown/src/check.py')
DS=importlib.util.module_from_spec(spec);spec.loader.exec_module(DS);sys.path[:]=saved


def check():
    rows=[];old_inside=motion.inside;fixtures=DS.membership_fixtures()
    for seed in (101,202):
        for stage in ('source','export'):
            bpy.ops.wm.read_factory_settings(use_empty=True)
            if stage=='source':bpy.ops.wm.open_mainfile(filepath=str(Path('build',f'Civic-{seed}-source.blend').resolve()))
            else:bpy.ops.import_scene.gltf(filepath=str(Path('build/review',f'Civic-{seed}.glb').resolve()))
            membership=DS.AssemblyMembership(surface);measure=membership.surface
            motion.surface=measure;motion.inside=membership.inside
            # Only genuine door leaves rotate as rigid pivots. The entire
            # sectional chain has its own measured/chord-length sweep below.
            pivots=[o for o in bpy.context.scene.objects if o.get('pivot_axis')=='Z' and '_Door' in o.name and 'range_degrees' in o]
            config=dict(MOTIONS=[dict(node=o.name,axis='Z',range=list(o['range_degrees']),step=5,tolerance_m=.001) for o in pivots])
            measured=sweep(config);rows.append(dict(seed=seed,stage=stage,kind='front_doors',**measured))
            if seed!=202:continue
            panels=[o for o in bpy.context.scene.objects if o.get('overhead_door')]
            moving=[o for p in panels for o in p.children_recursive if o.type=='MESH']
            fixed=[o for o in bpy.context.scene.objects if o.type=='MESH' and o not in moving and not o.get('kinematic_guide')]
            stationary={o.name:measure(o) for o in fixed};rest=None;violations=[];maximum=0
            for j in range(21):
                rest=pose(panels,j/20,rest);bpy.context.view_layer.update();current={o.name:measure(o) for o in moving}
                for ob in moving:
                    for other in fixed:
                        depth,crossings=penetration(current[ob.name],stationary[other.name],.001);maximum=max(maximum,depth)
                        if depth>.001:violations.append(dict(step=j,moving=ob.name,fixed=other.name,depth_m=depth))
                for i,ob in enumerate(moving):
                    for other in moving[i+1:]:
                        depth,crossings=penetration(current[ob.name],current[other.name],.001);maximum=max(maximum,depth)
                        if depth>.001:violations.append(dict(step=j,moving=ob.name,fixed=other.name,depth_m=depth))
            rows.append(dict(seed=seed,stage=stage,kind='sectional_chain',samples=21,maximum_penetration_m=maximum,violations=violations,passed=not violations,guide_exception='Roller/guide rolling contact excluded by explicit kinematic_guide tag; every other fixed surface retained'))
    motion.surface=surface;motion.inside=old_inside
    result=dict(passed=all(r['passed'] for r in rows),checks=rows,membership_fixtures=fixtures,method='Existing Downtown oriented-solid-angle membership on kit BVH/edge-interval penetration; source and actual imported surfaces',scope='Sampled surfaces, not a continuous collision or engineering certificate')
    Path('build/motion-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print('CIVIC MOTION',result['passed']);assert result['passed'],'See build/motion-check.json for measured violations'


if __name__=='__main__':check()
