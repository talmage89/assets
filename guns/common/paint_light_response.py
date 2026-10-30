"""Optional receiver photographic lighting diagnostic, never a game output.

Render each physical card independently in scene-linear EXR. The fit is a
starting point only; acceptance uses a fresh full-resolution Cycles image.
"""
import json
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
i = sys.argv.index('--member'); member = sys.argv[i+1]; del sys.argv[i:i+2]
BASE = ROOT / 'guns' / member
sys.path[:0] = [str(ROOT), str(BASE/'src')]
from guns.common.render import main
from guns.common.photo_matches import camera_shots
import final_shots as F
import interface

roughness_override=None
albedo_override=None
if '--paint-albedo' in sys.argv:
    i=sys.argv.index('--paint-albedo');albedo_override=float(sys.argv[i+1]);del sys.argv[i:i+2]
if '--paint-roughness' in sys.argv:
    i=sys.argv.index('--paint-roughness');roughness_override=float(sys.argv[i+1]);del sys.argv[i:i+2]
if roughness_override is not None or albedo_override is not None:
    original_configure=F.configure_scene
    def configure(scene,source):
        original_configure(scene,source)
        for mat in {m for ob in scene.objects if ob.type=='MESH' and not ob.get('studio') for m in ob.data.materials if m and m.use_nodes}:
            nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
            if bs is None or not bs.inputs['Base Color'].links or not bs.inputs['Roughness'].links:continue
            image=bs.inputs['Base Color'].links[0].from_node
            if image.type!='TEX_IMAGE':continue
            old=bs.inputs['Roughness'].links[0].from_socket
            mask=nt.nodes.new('ShaderNodeMath');mask.operation='SUBTRACT';mask.inputs[1].default_value=.56;nt.links.new(image.outputs['Alpha'],mask.inputs[0])
            fraction=nt.nodes.new('ShaderNodeMath');fraction.operation='DIVIDE';fraction.inputs[1].default_value=.24;fraction.use_clamp=True;nt.links.new(mask.outputs[0],fraction.inputs[0])
            if roughness_override is not None:
                delta=nt.nodes.new('ShaderNodeMath');delta.operation='MULTIPLY';delta.inputs[1].default_value=roughness_override-.29;nt.links.new(fraction.outputs[0],delta.inputs[0])
                add=nt.nodes.new('ShaderNodeMath');add.operation='ADD';nt.links.new(old,add.inputs[0]);nt.links.new(delta.outputs[0],add.inputs[1]);nt.links.new(add.outputs[0],bs.inputs['Roughness'])
            if albedo_override is not None:
                delta=nt.nodes.new('ShaderNodeVectorMath');delta.operation='SCALE';delta.inputs[0].default_value=(albedo_override-.022,)*3;nt.links.new(fraction.outputs[0],delta.inputs['Scale'])
                add=nt.nodes.new('ShaderNodeVectorMath');add.operation='ADD';nt.links.new(image.outputs['Color'],add.inputs[0]);nt.links.new(delta.outputs[0],add.inputs[1]);nt.links.new(add.outputs[0],bs.inputs['Base Color'])
    F.configure_scene=configure
    F.RENDER_STAGE='REVIEW ONLY paint roughness override; never final acceptance'

i = sys.argv.index('--sets'); requested = sys.argv[i+1].split(','); del sys.argv[i:i+2]
sign = 1 if member == 'ak' else -1
BASES = [dict(world=True)]
for y in (-.5, .10, .7):
    for z in (-.30, .10, .65):
        BASES.append(dict(position=(sign*.65,y,z),size=(.65,.90)))
for x in (-sign*.65, 0):
    for z in (-.30,.65):
        BASES.append(dict(position=(x,.10,z),size=(.60,.80)))
for z in (.15,.28,.45):
    BASES.append(dict(position=(sign*.45,.10,z),size=(.70,.04)))
if member == 'smg':
    # Narrow studio cards along the actual crown reflection directions.
    # Broad fill alone can match a histogram with the reflection on the
    # wrong flat; these fixtures resolve the photographed upper sheen.
    from guns.common.paint_review import geometry
    geo=geometry(BASE);index=list(geo['names']).index('Receiver_Shell')+1
    triangles=geo['xyz'][geo['ids']==index]
    view=np.asarray(camera_shots(BASE/'build/cameras.json')['left_photo']['location'])
    for y in (.04,.12):
        for z in (.112,.118,.124,.129):
            a,b,c=triangles.transpose(1,0,2)
            den=(b[:,2]-c[:,2])*(a[:,1]-c[:,1])+(c[:,1]-b[:,1])*(a[:,2]-c[:,2])
            valid=abs(den)>1e-12;safe=np.where(valid,den,1)
            wa=((b[:,2]-c[:,2])*(y-c[:,1])+(c[:,1]-b[:,1])*(z-c[:,2]))/safe
            wb=((c[:,2]-a[:,2])*(y-c[:,1])+(a[:,1]-c[:,1])*(z-c[:,2]))/safe;wc=1-wa-wb
            valid &= (wa>=0)&(wb>=0)&(wc>=0)
            if not valid.any():continue
            xx=wa*a[:,0]+wb*b[:,0]+wc*c[:,0];i=np.flatnonzero(valid)[np.argmin(xx[valid])]
            point=np.array((xx[i],y,z));normal=np.cross(b[i]-a[i],c[i]-a[i]);normal/=np.linalg.norm(normal)
            direction=view-point;direction/=np.linalg.norm(direction)
            reflected=2*normal*(normal@direction)-direction
            BASES.append(dict(position=(point+.35*reflected).tolist(),size=(.35,.025),target=point.tolist()))
original = F.prepare_shot


def exr(scene, *_):
    scene.render.image_settings.file_format = 'OPEN_EXR'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '32'
    scene.render.filepath = str(Path(scene.render.filepath).with_suffix('.exr'))


def prepare(scene, shot):
    original(scene, shot)
    scene.cycles.use_denoising = False
    for ob in scene.objects:
        if ob.type == 'LIGHT':
            ob.data.energy = 0
    bg = scene.world.node_tree.nodes['Background']
    bg.inputs['Strength'].default_value = 0
    bg.inputs['Color'].default_value = (.25,.25,.25,1)
    key = 'Independent paint basis'
    if key not in scene.objects:
        data = bpy.data.lights.new(key,'AREA'); data.shape = 'RECTANGLE'
        ob = bpy.data.objects.new(key,data); scene.collection.objects.link(ob)
    b = BASES[shot['basis_index']]
    if b.get('world'):
        bg.inputs['Strength'].default_value = 1
    else:
        ob=scene.objects[key]; ob.hide_render=False; ob.data.energy=1;ob.data.color=(1,1,1)
        ob.location=b['position']; ob.data.size,ob.data.size_y=b['size']
        ob.rotation_euler=(Vector(b.get('target',(0,.10,.09)))-ob.location).to_track_quat('-Z','Y').to_euler()
    if exr not in bpy.app.handlers.render_pre:
        bpy.app.handlers.render_pre.append(exr)


F.prepare_shot = prepare
matches = camera_shots(BASE/'build/cameras.json')
F.SHOTS = {name+'__'+str(i):dict(matches[name],**F.PHOTO_POSES[name],basis_index=i)
           for name in requested for i in range(len(BASES))}
F.DEFAULT_SHOTS = ','.join(F.SHOTS)
out = Path(sys.argv[sys.argv.index('--out')+1]);out.mkdir(parents=True,exist_ok=True)
main(F,interface)
(out/'bases.json').write_text(json.dumps(BASES,indent=2))
(out/'diagnostic-parameters.json').write_text(json.dumps(dict(paint_roughness_override=roughness_override,paint_albedo_override=albedo_override),indent=2))
for path in out.glob('*.png'):
    if path.read_bytes()[:4] == bytes((118,47,49,1)):
        path.rename(path.with_suffix('.exr'))
configs=[Path(bpy.utils.resource_path(k))/'datafiles/colormanagement/config.ocio' for k in ('LOCAL','SYSTEM')]
(out/'ocio-path.txt').write_text(str(next(p for p in configs if p.exists())))
