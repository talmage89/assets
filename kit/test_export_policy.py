"""No-GPU regression for composed tile/optics/variant export and studio aliases."""
import json
from pathlib import Path
import runpy
import sys

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from kit import export, gltf, model as G, studio

# Elevated front-facing print: solid normal recalculation previously reversed
# this particular open sheet, producing black AO and an inward normal bake.
printed=G.plane_uv('Front print fixture', [(-.032,-.0531,1.651),(.032,-.0531,1.651),
    (.032,-.0531,1.811),(-.032,-.0531,1.811)], None)
assert printed.data.polygons[0].normal.y < -.999
assert [tuple(printed.data.uv_layers['PrintUV'].data[i].uv) for i in range(4)] == [(0,0),(1,0),(1,1),(0,1)]
bpy.data.objects.remove(printed,do_unlink=True)
print('PASS: authored print front and corner UVs survive normal recalculation')

# Reuse the real finalize/export/import fixture and its original image generator.
runpy.run_path(str(ROOT / 'kit/test_atlas.py'))
folder = ROOT / 'build/atlas-test'
bpy.ops.wm.open_mainfile(filepath=str(folder / 'finalized.blend'))
root = bpy.data.objects['TileFixture']
frame = bpy.data.objects['Frame']
for name, offset, tag, value in [
    ('Glass', 3, None, None),
    ('Numeric selected', 5, 'variant_id', 1),
    ('Numeric rejected', 7, 'variant_id', 0),
]:
    ob = frame.copy();ob.data = frame.data.copy()
    bpy.context.collection.objects.link(ob);ob.name = name
    ob.location.x += offset
    if tag:ob[tag] = value
# Ancestor-based selection must remove its entire subtree and restore placement.
for value, offset in [('1', 10), ('other', 20)]:
    parent = G.pivot('Staged ' + value, (offset, 0, 0))
    parent['delivery_variant'] = value
    parent['atlas_staging_offset'] = (offset, 0, 0)
    parent['delivery_name'] = 'Selected pivot'
    ob = frame.copy();ob.data = frame.data.copy()
    bpy.context.collection.objects.link(ob);ob.name = 'Ancestor child ' + value
    ob.parent = parent
cfg = runpy.run_path(str(folder / 'config.py'))
cfg = {k: v for k, v in cfg.items() if not k.startswith('__')}
cfg.update(EXPORT_VARIANT=1, MATERIAL_OVERRIDES={
    'Glass': dict(transmission=1, ior=1.45),
    'Sheet_': dict(emission_strength=4),
})
config = folder / 'composed-config.py'
config.write_text('\n'.join(k + '=' + repr(v) for k, v in cfg.items()))
source = folder / 'composed.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(source))
for label, extra in [('config', []), ('cli', ['--variant', '1'])]:
    # Exercise both legacy untinted emission and the additive tint on the
    # same atlas/alpha/variant fixture; no new textures may be introduced.
    if label == 'cli':
        cfg['MATERIAL_OVERRIDES']['Sheet_']['emission_tint']=(1,.12,.008)
        config.write_text('\n'.join(k + '=' + repr(v) for k, v in cfg.items()))
    output = folder / (label + '.glb');report = folder / (label + '.json')
    sys.argv = ['blender', '--', '--source', str(source), '--textures', str(folder / 'textures'),
                '--asset', 'TileFixture', '--config', str(config), '--out', str(output),
                '--report', str(report), *extra]
    export.main()
    data = json.loads(report.read_text())
    assert data['triangles'] == 52, (label, data['triangles'])
    assert len(data['materials']) == 3, data['materials']
    assert 'Selected pivot' in data['nodes'] and 'Staged other' not in data['nodes']
    assert abs(data['nodes']['Selected pivot'][0][3]) < 1e-7
    doc = gltf.GLB(output).json
    assert sorted(m['name'] for m in doc['materials']) == data['materials']
    assert len(doc['images']) == len(doc['textures']) == 3
    assert sum(m.get('alphaMode') == 'MASK' for m in doc['materials']) == 1
    tile = next(m for m in doc['materials'] if m.get('alphaMode') == 'MASK')
    expected_tint = (1,.12,.008) if label == 'cli' else (1,1,1)
    assert tile['doubleSided'] and max(abs(a-b) for a,b in zip(tile['emissiveFactor'],expected_tint)) < 1e-6
    assert tile['extensions']['KHR_materials_emissive_strength']['emissiveStrength'] == 4
    glass = next(m for m in doc['materials'] if 'KHR_materials_transmission' in m.get('extensions', {}))
    assert glass['extensions']['KHR_materials_transmission']['transmissionFactor'] == 1
print('PASS: tile alpha + glass/emission + numeric/config/ancestor variants compose')


def studio_snapshot(**options):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    studio.add_studio(**options)
    bpy.context.view_layer.update()
    lights = {o.name: (tuple(o.location), o.data.energy, o.data.size, o.data.size_y)
              for o in bpy.context.scene.objects if o.type == 'LIGHT'}
    wall = max(v.co.z for v in bpy.data.objects['Studio seamless'].data.vertices)
    people = studio.human()
    bpy.context.view_layer.update()
    height = max((o.matrix_world @ Vector(c)).z for o in people for c in o.bound_box)
    return lights, wall, height

legacy = studio_snapshot(light_scale=3)
canonical = studio_snapshot(scale=3)
aliased = studio_snapshot(scale=3, light_scale=3)
assert legacy[0] == canonical[0] == aliased[0]
assert abs(legacy[1] - 6) < 1e-6
assert abs(canonical[1] - 18.004) < 1e-5
assert canonical == aliased
assert abs(canonical[2] - 1.8) < 1e-6
assert studio_snapshot(scale=3, backdrop_height=45)[1] == 45
try:
    studio_snapshot(scale=3, light_scale=2)
except ValueError:
    pass
else:
    raise AssertionError('Conflicting scale aliases were silently multiplied')
print('PASS: scale aliases apply once, legacy framing retained, human stays 1.8 m')
