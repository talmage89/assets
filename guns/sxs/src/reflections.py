"""Procedural parallel-band reflection test; exported normal map stays connected.

This diagnostic changes only the inspection shader's color/roughness/metal.
It never edits the gun, atlas or ordinary presentation lighting. Both stripe
orientations, all cameras and the loaded open pose are identical for source
and export. Full camera frames accompany pixel-exact crops of the head.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(Path(__file__).parent))
from kit import gpu, weapon_presentation as presentation
from shots import SHOTS

VIEWS = ('open', 'top', 'aimed', 'right', 'left')

def world_bands(sc, orientation):
    world = bpy.data.worlds.new('Procedural parallel bright bands ' + orientation)
    world.use_nodes = True; sc.world = world
    nt = world.node_tree; nt.nodes.clear()
    tc = nt.nodes.new('ShaderNodeTexCoord')
    split = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Normal'], split.inputs[0])
    # Parallel latitude bands have no meridian-pole singularity. An atan2
    # environment falsely pinches stripes together on a perfectly fair dome.
    frequency = nt.nodes.new('ShaderNodeMath'); frequency.operation = 'MULTIPLY'; frequency.inputs[1].default_value = 32
    nt.links.new(split.outputs['Y' if orientation == 'transverse' else 'X'], frequency.inputs[0])
    sine = nt.nodes.new('ShaderNodeMath'); sine.operation = 'SINE'; nt.links.new(frequency.outputs[0], sine.inputs[0])
    # Smooth boundaries reduce sampling noise without concealing a kink.
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'EASE'
    ramp.color_ramp.elements[0].position = .42; ramp.color_ramp.elements[0].color = (.012, .012, .012, 1)
    ramp.color_ramp.elements[1].position = .52; ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    nt.links.new(sine.outputs[0], ramp.inputs[0])
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 1
    nt.links.new(ramp.outputs[0], bg.inputs['Color'])
    out = nt.nodes.new('ShaderNodeOutputWorld'); nt.links.new(bg.outputs[0], out.inputs[0])

def main():
    p = argparse.ArgumentParser(); p.add_argument('--source', required=True); p.add_argument('--out', required=True)
    p.add_argument('--width', type=int, default=1440); p.add_argument('--samples', type=int, default=32)
    p.add_argument('--views', default=','.join(VIEWS)); p.add_argument('--orientations', default='transverse,longitudinal')
    a = p.parse_args(sys.argv[sys.argv.index('--') + 1:]); source = Path(a.source).resolve()
    out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if source.suffix == '.blend': bpy.ops.wm.open_mainfile(filepath=str(source))
    else: bpy.ops.import_scene.gltf(filepath=str(source))
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; gpu.enable()
    sc.cycles.samples = a.samples; sc.cycles.use_denoising = False; sc.cycles.max_bounces = 5
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.render.film_transparent = True; sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0
    sc.render.resolution_x = a.width
    # Use the export's tangent normal texture without modification. All
    # mesh/material slots receive the same diagnostic reflection response.
    for ob in [o for o in sc.objects if o.type == 'MESH' and o.get('bone')]:
        for slot in ob.material_slots:
            mat = slot.material.copy(); slot.material = mat
            bs = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
            head = ob.get('part_name', ob.name) == 'Action_Body'
            for key, value in [('Base Color', (.6, .6, .6, 1) if head else (.025, .025, .025, 1)),
                               ('Metallic', 1 if head else 0), ('Roughness', .045 if head else .85)]:
                socket = bs.inputs[key]
                for link in list(socket.links): mat.node_tree.links.remove(link)
                socket.default_value = value
    for ob in sc.objects:
        if ob.type == 'LIGHT' or ob.name.startswith('Icosphere'): ob.hide_render = True
    cam = bpy.data.objects.new('Reflection camera', bpy.data.cameras.new('Reflection camera'))
    sc.collection.objects.link(cam); sc.camera = cam; cam.data.sensor_width = 36; cam.data.sensor_fit = 'HORIZONTAL'
    cam.data.clip_start = .001; cam.data.clip_end = 20
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    specs = dict(open=SHOTS['open'], aimed=SHOTS['aimed'], right=SHOTS['action_rake_right'], left=SHOTS['action_rake_left'],
                 top=dict(location=(0, .106, .35), target=(0, .106, .04), ortho=.085, aspect=1.25, action='IdleOpenEmpty', frame=0))
    metadata = {}
    for orientation in a.orientations.split(','):
        world_bands(sc, orientation)
        for name in a.views.split(','):
            shot = dict(specs[name]); presentation.pose(arm, shot.get('action', 'Idle'), shot.get('frame', 0))
            cam.location = shot['location']; cam.rotation_euler = (Vector(shot['target'])-cam.location).to_track_quat('-Z', 'Y').to_euler()
            cam.data.type = 'ORTHO' if 'ortho' in shot else 'PERSP'; cam.data.ortho_scale = shot.get('ortho', 1); cam.data.lens = shot.get('lens', 70)
            if shot.get('aimed'): presentation.aimed_camera(cam, bpy.data.objects['Socket_Eye'])
            sc.render.resolution_y = round(a.width/shot.get('aspect', 1.5)); sc.render.filepath = str(out/(name+'-'+orientation+'.png'))
            bpy.context.view_layer.update(); bpy.ops.render.render(write_still=True)
            metadata[name+'-'+orientation] = dict(shot, source=str(source), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                normal_map_retained=source.suffix == '.glb', diagnostic_roughness=.045, environment='parallel bright bands, sin(32*unit_direction.'+('Y' if orientation=='transverse' else 'X')+')')
    (out/'shots.json').write_text(json.dumps(metadata, indent=2))

if __name__ == '__main__': main()
