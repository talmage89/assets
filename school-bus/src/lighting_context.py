"""Original studio horizon flags for transparent-object review, no image plates."""
import bpy
from mathutils import Vector
from kit import model as G

def flags(camera_location):
    normal=Vector((camera_location[0],camera_location[1],0)).normalized()
    mat=bpy.data.materials.new('Charcoal horizon flags');mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(.028,.035,.029,1)
    bs.inputs['Roughness'].default_value=.96
    obs=[]
    for distance in [max(Vector(camera_location).length+15,36),-28]:
        ob=G.box('Studio dark horizon',normal*distance+Vector((0,0,7)),(.05,140,14),mat,0)
        ob.rotation_euler=normal.to_track_quat('X','Z').to_euler();obs.append(ob)
    return obs
