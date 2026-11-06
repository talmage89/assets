"""Same-light swatches from measured exported asphalt vertex-color medians.

This isolates shared PBR value from building shadows and different cameras.
It is a diagnostic, not a replacement for the actual-export photo pair.
"""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy,runpy
if Path('build/strip-value/before/export/CommercialStrip-202.gltf').exists():
    runpy.run_path(str(HERE/'strip_value_baseline.py'),run_name='__main__')
from mathutils import Vector
from render import setup
from surfaces import pbr
from kit.tiling import world_uv
from strip_value_controls import run as measure

measure('build/strip-value/material-values.json')
after=json.loads(Path('build/strip-value/material-values.json').read_text())
before_path=Path('build/strip-value/before-materials.json');before=json.loads(before_path.read_text()) if before_path.exists() else after
colors={name:before['rows'][name]['median_tint_rgb'] for name in ('Ground','Gas')}
if before_path.exists():colors['StripBefore']=before['rows']['Strip']['median_tint_rgb']
colors['StripAfter']=after['rows']['Strip']['median_tint_rgb']
bpy.ops.wm.read_factory_settings(use_empty=True);camera=setup(24);camera.location=(0,-8,3);camera.rotation_euler=(Vector((0,0,0))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=4
mat=pbr('Asphalt',Path('../ground/textures/ship'))
bpy.ops.mesh.primitive_plane_add(size=30);plane=bpy.context.object;plane.name='Unchanged PBR asphalt sample';plane.data.materials.append(mat);world_uv(plane,6.096)
shader=mat.node_tree.nodes.get('Principled BSDF');rough_source=shader.inputs['Roughness'].links[0].from_socket;metal_source=shader.inputs['Metallic'].links[0].from_socket
rough_scale=mat.node_tree.nodes.new('ShaderNodeMath');rough_scale.operation='MULTIPLY';mat.node_tree.links.new(rough_source,rough_scale.inputs[0])
tint=plane.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');plane.data.color_attributes.active_color=tint
sc=bpy.context.scene;sc.render.resolution_x=480;sc.render.resolution_y=320;sc.render.resolution_percentage=100
sun=bpy.data.objects['Sun'];sun.rotation_euler=Vector((.72,-.75,-.62)).to_track_quat('-Z','Y').to_euler();sun.data.energy=6
import math
sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY');sky.sun_elevation=math.atan2(.62,math.hypot(.72,.75));sky.sun_rotation=math.atan2(.75,-.72)
next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.035;sc.view_settings.exposure=1.75
out=Path('renders/strip/values');out.mkdir(parents=True,exist_ok=True)
import numpy as np
from PIL import Image
rows={}
for key,color in colors.items():
    source=before['rows'][key] if key in ('Ground','Gas') else (before if key=='StripBefore' else after)['rows']['Strip']
    mat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.5*source.get('specular_factors',[1])[0]
    for key_in,value,socket in (('Roughness',source.get('roughness_factors',[1])[0],rough_source),('Metallic',0,metal_source)):
        for link in list(shader.inputs[key_in].links):mat.node_tree.links.remove(link)
        if source.get('roughness_texture_used',True):
            # glTF multiplies the texture by roughnessFactor; preserve both.
            if key_in=='Roughness':rough_scale.inputs[1].default_value=value;socket=rough_scale.outputs[0]
            mat.node_tree.links.new(socket,shader.inputs[key_in])
        else:shader.inputs[key_in].default_value=value
    for val in tint.data:val.color=(*color,1)
    path=out/(key+'.png');sc.render.filepath=str(path.resolve());bpy.ops.render.render(write_still=True)
    a=np.asarray(Image.open(path).convert('RGB'),dtype=float)/255;y=a@[.2126,.7152,.0722]
    rows[key]=dict(median_Yprime=float(np.median(y)),tint_rgb=color)
(out/'control-values.json').write_text(json.dumps(dict(rows=rows,scope=__doc__,lighting=dict(sun_direction=[.72,-.75,-.62],sun_energy=6,sky_strength=.035,exposure=1.75)),indent=2)+'\n')
from kit.contact import review_sheet
review_sheet([[out/(key+'.png') for key in colors]],out/'same-light.jpg',width=1600,title='Same light and asphalt maps / Ground, gas, strip before (when captured), strip after')
print('SAME LIGHT VALUES',rows)
