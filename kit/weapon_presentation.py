"""Action-aware held-asset presentation, independent of weapon anatomy."""
import math
from mathutils import Vector
from kit import weapon


def aimed_camera(camera,socket):
    """Socket +Y is the optical axis; +Z is image up (rifle frame)."""
    world=socket.matrix_world
    camera.location=world.translation
    forward=world.to_3x3()@Vector((0,1,0))
    up=world.to_3x3()@Vector((0,0,1))
    # Construct a camera basis without a look-at target or guessed eye offset.
    right=forward.cross(up).normalized();up=right.cross(forward).normalized()
    from mathutils import Matrix
    camera.rotation_euler=Matrix((right,up,-forward)).transposed().to_euler()


def strip_samples(duration_frames,*,fps=60,rate=15):
    """Uniform wall-clock samples including the endpoint; labels are seconds."""
    count=math.ceil(duration_frames/fps*rate)
    return [(min(i*fps/rate,duration_frames),min(i/rate,duration_frames/fps)) for i in range(count+1)]


def pose(armature,clip,frame,*,floor=None):
    weapon.pose(armature,clip,frame)
    if floor:
        # Withdrawn magazines must not disappear below a tabletop backdrop.
        floor.hide_render=bool(clip)
