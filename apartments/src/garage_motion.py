"""Townhouse sectional doors reuse the houses' rigid-chord guide mathematics."""
import importlib.util
import math
from pathlib import Path
import bpy
from mathutils import Vector
spec=importlib.util.spec_from_file_location('_apartments_house_track',Path(__file__).resolve().parents[2]/'houses/src/split_motion.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
track=module.track


def pose(progress):
    groups={}
    for o in bpy.context.scene.objects:
        if o.get('motion_kind')=='sectional_track':groups.setdefault(o['garage_group'],[]).append(o)
    frames={}
    for name,nodes in groups.items():
        nodes.sort(key=lambda o:o['section']);h=nodes[0]['section_height_m'];height=4*h;radius=nodes[0]['track_radius_m']
        origin=Vector(nodes[0]['closed_top_m'])-Vector((0,0,h));distance=height+progress*(height+.55)
        for node in reversed(nodes):
            top=track(distance,height,radius);lo=distance-2*h;hi=distance
            for _ in range(40):
                mid=(lo+hi)/2
                if (top-track(mid,height,radius)).length>h:lo=mid
                else:hi=mid
            lower=track((lo+hi)/2,height,radius);delta=(top-lower).normalized()
            node.location=origin+top;node.rotation_mode='XYZ';node.rotation_euler=(-math.atan2(delta.y,delta.z),0,0)
            frames[node.name]=dict(chord_m=(top-lower).length,section_height_m=h);distance=(lo+hi)/2
    bpy.context.view_layer.update();return frames
