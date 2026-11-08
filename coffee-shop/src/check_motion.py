"""Actual door/window sweeps on modeled and fresh-imported cafe assemblies."""
import importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
import bpy
from kit import motion

# Reuse Downtown's established oriented-solid membership for abutting building
# members. Its source check uses a different plan module; isolate that import.
paths=list(sys.path);saved=sys.modules.pop('plan',None)
try:
    sys.path.insert(0,str(ROOT/'downtown/src'))
    spec=importlib.util.spec_from_file_location('coffee_downtown_surface_check',ROOT/'downtown/src/check.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
finally:
    sys.path[:]=paths;sys.modules.pop('plan',None)
    if saved is not None:sys.modules['plan']=saved

reports=[]
for seed in (117,228,339):
    for stage in ('modeled','exported'):
        if stage=='modeled':bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/shops/{seed}.blend').resolve()))
        else:
            bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(f'export/CoffeeShop-{seed}.gltf').resolve()))
        bpy.context.view_layer.update();specs=[]
        for ob in bpy.context.scene.objects:
            if ob.type=='MESH':
                if not ob.data.polygons:ob['allow_boundary']=True;continue
                used={ob.data.materials[f.material_index] for f in ob.data.polygons}
                if used and all('Cutout' in m.name for m in used):ob['allow_boundary']=True
            if ob.name.startswith('Host_') and ob.get('pivot_axis'):
                specs.append(dict(node=ob.name,axis=ob['pivot_axis'],range=list(ob['range_degrees']),step=5,tolerance_m=.001))
            elif ob.name.startswith('Host_') and ob.get('slide_axis'):
                specs.append(dict(node=ob.name,axis=ob['slide_axis'],range=list(ob['range_m']),step=.043,tolerance_m=.001,kind='translation'))
        old_surface,old_inside=motion.surface,motion.inside;membership=native.AssemblyMembership(old_surface)
        motion.surface,motion.inside=membership.surface,membership.inside
        try:result=motion.sweep(dict(MOTIONS=specs))
        finally:motion.surface,motion.inside=old_surface,old_inside
        reports.append(dict(seed=seed,stage=stage,**result))
        Path('build/coffee-motion.json').write_text(json.dumps(reports,indent=2)+'\n')
assert all(r['passed'] for r in reports),'Actual cafe door/window collision; see build/coffee-motion.json'
print('COFFEE MOTION PASS',[(r['seed'],r['stage'],len(r['motions'])) for r in reports])
