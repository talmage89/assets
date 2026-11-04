"""X220 procedural daylight and gloss-clay inspection environment."""
import bpy
from lighting import outdoor,conditions


def daylight(overcast=False):
    outdoor()
    description=conditions('used_front' if overcast else 'aged_front')
    bpy.data.objects['Studio seamless'].hide_render=True
    # A dark real plane supplies the lower reflected hemisphere. It remains
    # visible to glossy rays and receives shadows; no photographic environment.
    ground=bpy.data.objects['Comparison ground'];ground.visible_shadow=True
    return description


def gloss_clay():
    daylight()
    nt=bpy.context.scene.world.node_tree
    nt.nodes['Comparison sky saturation'].inputs['Saturation'].default_value=.15
    nt.nodes['Comparison environment'].inputs['Strength'].default_value=.35
    bpy.data.objects['Comparison sun'].data.energy=2.0
    bpy.data.objects['Comparison sun'].data.angle=.08
    for m in bpy.data.materials:
        if m.name=='Clay body':
            bs=m.node_tree.nodes['Principled BSDF']
            bs.inputs['Base Color'].default_value=(.18,.18,.18,1)
            bs.inputs['Roughness'].default_value=.22
            bs.inputs['Metallic'].default_value=.18
            bs.inputs['Coat Weight'].default_value=1
            bs.inputs['Coat Roughness'].default_value=.08
