"""Evenly spaced reflection lights in the held S240 gallery camera frames.

Diagnostic only: substitute a polished neutral material, retaining the actual
mesh, triangulation and corner normals. Neither maps nor a bake can hide a fold.
The studio floor and camera are the same as the finished gallery.
"""
import bpy
from mathutils import Vector


def setup():
    for ob in bpy.context.scene.objects:
        if ob.type=='LIGHT':ob.data.energy=0
    world=bpy.context.scene.world
    world.use_nodes=True
    bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND')
    bg.inputs['Color'].default_value=(.005,.005,.005,1)
    bg.inputs['Strength'].default_value=.1
    for orientation in ['ceiling','wall']:
        for index in range(15):
            d=bpy.data.lights.new(f'S240 zebra {orientation} {index:02d}','AREA')
            d.shape='RECTANGLE';d.energy=1800;d.size=.13;d.size_y=9
            ob=bpy.data.objects.new(d.name,d);bpy.context.scene.collection.objects.link(ob)
            ob.location=(-4.2+index*.60,0,4.0) if orientation=='ceiling' else (4.0,-4.2+index*.60,1.8)
            ob.rotation_euler=(0,0,0) if orientation=='ceiling' else (Vector((0,ob.location.y,1.8))-ob.location).to_track_quat('-Z','Y').to_euler()
            ob['studio']=True


def material():
    mat=bpy.data.materials.get('S240 reflection-line diagnostic')
    if mat is None:
        mat=bpy.data.materials.new('S240 reflection-line diagnostic');mat.use_nodes=True
        bs=mat.node_tree.nodes.get('Principled BSDF')
        bs.inputs['Base Color'].default_value=(.32,.32,.32,1)
        bs.inputs['Metallic'].default_value=1
        bs.inputs['Roughness'].default_value=.075
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('studio'):continue
        ob.data.materials.clear();ob.data.materials.append(mat)
        for face in ob.data.polygons:face.material_index=0
