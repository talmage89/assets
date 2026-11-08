"""Quick, stock glTF materials; only the sign sheet is new at this gate.

The road keeps Ground's canonical image bytes. New concrete and metal are
explicitly unbaked form colors. No source-only procedural nodes are exported.
"""
from pathlib import Path
import bpy
import geom as Q
from kit.tiling import material
ROOT=Path(__file__).resolve().parents[2]

def palette(stage='form'):
    from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
    get_settings_group()
    for name in ('Asphalt','Concrete','Lawn'):
        Q.M[name]=material(name,ROOT/'ground/textures/ship',tint=True)
    # GroundTrim's paint, patch and seal charts are reused, never repainted.
    Q.M['GroundTrim']=material('GroundTrim',ROOT/'ground/textures/ship',alpha=True,tint=True)
    Q.M['Fence']=material('FreewayFenceForm',Path('textures/checkpoint'),alpha=True)
    Q.M['Fence'].use_backface_culling=False
    for name,c,r,m in [
        ('Bridge',(.265,.265,.24),.92,0),('Barrier',(.29,.29,.265),.89,0),
        ('Steel',(.34,.37,.38),.43,1),('DarkSteel',(.075,.083,.083),.65,.8),
        ('Rubber',(.012,.013,.012),.9,0),('White',(.68,.68,.62),.72,0),
        ('Yellow',(.62,.40,.012),.7,0),('Joint',(.022,.023,.02),.94,0),
        ('Wood',(.16,.11,.063),.9,0),('Drain',(.075,.073,.055),.9,0),
        ('Earth',(.14,.10,.058),1,0),('Glass',(.025,.05,.055),.2,.15)]:
        Q.M[name]=Q.constant('Freeway_Form_'+name,c,r,m)
    m=Q.constant('Freeway_Checkpoint_Signs',(1,1,1),.65)
    tx=m.node_tree.nodes.new('ShaderNodeTexImage');tx.image=bpy.data.images.load(str(Path('textures/checkpoint/T_Freeway_Signs.png').resolve()))
    m.node_tree.links.new(tx.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
    Q.M['Signs']=m
    Q.LOOKDEV=stage=='look'
    if Q.LOOKDEV:
        from look_materials import install
        install()

