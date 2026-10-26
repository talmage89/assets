"""Light the far seamless at the low, oblique calibrated photo camera.

Ray checks show its upper-left rays hit the backdrop 17-26 m away, beyond
the main softboxes' useful illumination. A broad wash faces the backdrop;
the asset is behind that light. No delivered surface or camera changes.
"""
import sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import studio
add_studio=studio.add_studio

def photo_studio(**kwargs):
 camera=add_studio(**kwargs)
 light=bpy.data.lights.new('Comparison backdrop wash','AREA');light.energy=20000
 light.shape='RECTANGLE';light.size=80;light.size_y=10
 ob=bpy.data.objects.new(light.name,light);bpy.context.scene.collection.objects.link(ob)
 ob.location=(0,1.5,3);ob.rotation_euler=Vector((0,1,0)).to_track_quat('-Z','Y').to_euler();ob['studio']=True
 return camera

studio.add_studio=photo_studio
if __name__=='__main__':studio.main()
