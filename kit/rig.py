"""Small rigid/flexible chain helpers; meters and explicit normalized weights."""
import math
import bpy
from mathutils import Vector,Matrix,Quaternion


def chain(name,points,parent,prefix='Hose'):
    data=bpy.data.armatures.new(name)
    arm=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(arm)
    arm.parent=parent;arm.show_in_front=True;arm['asset_rig']=True
    bpy.ops.object.select_all(action='DESELECT');arm.select_set(True)
    bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
    previous=None;previous_z=Vector((0,0,1))
    for i,(a,b) in enumerate(zip(points,points[1:]),1):
        bone=data.edit_bones.new(f'{prefix}_{i:02d}');bone.head=a;bone.tail=b
        bone.parent=previous;bone.use_connect=previous is not None
        tangent=(bone.tail-bone.head).normalized()
        z=previous_z-tangent*previous_z.dot(tangent)
        if z.length<1e-5:z=Vector((1,0,0))-tangent*tangent.x
        z.normalize();bone.align_roll(z);previous_z=z;previous=bone
    bpy.ops.object.mode_set(mode='OBJECT');arm.select_set(False)
    return arm


def bind(ob,arm,weights,export_part='HoseAssembly',modifier_name='Hose skin'):
    """Rebase into armature rest coordinates and bind per-vertex bone weights."""
    bpy.context.view_layer.update()
    transform=arm.matrix_world.inverted()@ob.matrix_world
    ob.data.transform(transform);ob.parent=arm
    ob.matrix_parent_inverse=Matrix.Identity(4);ob.matrix_basis=Matrix.Identity(4)
    ob.vertex_groups.clear()
    groups={b.name:ob.vertex_groups.new(name=b.name) for b in arm.data.bones}
    for index,row in enumerate(weights):
        total=sum(row.values())
        if abs(total-1)>1e-6:raise ValueError(f'{ob.name} vertex {index}: weights sum {total}')
        # Match the portable exporter threshold explicitly, then normalize.
        row={name:weight for name,weight in row.items() if weight>=1e-4}
        total=sum(row.values())
        if total<=0:raise ValueError('Vertex has no retained influences')
        for name,weight in row.items():groups[name].add([index],weight/total,'REPLACE')
    modifier=ob.modifiers.new(modifier_name,'ARMATURE');modifier.object=arm
    modifier.use_deform_preserve_volume=False
    ob['export_part']=export_part
    return ob


def arc_samples(points,fractions):
    points=list(map(Vector,points));distances=[0.0]
    for a,b in zip(points,points[1:]):distances.append(distances[-1]+(b-a).length)
    output=[]
    for fraction in fractions:
        distance=fraction*distances[-1]
        for i in range(len(points)-1):
            if distances[i+1]>=distance:
                t=(distance-distances[i])/(distances[i+1]-distances[i])
                output.append(points[i].lerp(points[i+1],t));break
    return output,distances


def reset(arm):
    for bone in arm.pose.bones:bone.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update()


def dangling(arm,angles=None,lateral=-.08,twist_step=24,initial_z=(0,-1,0)):
    """A free-hanging demonstration with ordinary glTF linear skinning.

    Connected heads preserve chain lengths. The wide shallow S bend keeps the
    fitting above the floor and the hose clear of the cart's front upright.
    """
    reset(arm)
    previous_z=Vector(initial_z)
    for index,(bone,degrees) in enumerate(zip(arm.pose.bones,angles if angles is not None else [55,28,0,-28,-55,-70])):
        angle=math.radians(degrees)
        direction=Vector((math.sin(angle),lateral,-math.cos(angle))).normalized()
        z=previous_z-direction*previous_z.dot(direction);z.normalize()
        previous_z=z.copy()
        # A distributed untwist presents the diaphragm outward when stowed;
        # each adjacent pair differs by only 24 degrees of roll.
        z=Quaternion(direction,math.radians(index*twist_step))@z
        x=direction.cross(z).normalized()
        rotation=Matrix((x,direction,z)).transposed().to_4x4()
        if 'rest_frames' in arm:
            values=arm['rest_frames'][index*16:(index+1)*16]
            source=Matrix([values[i:i+4] for i in range(0,16,4)]).to_3x3()
            correction=source.inverted()@bone.bone.matrix_local.to_3x3()
            rotation=(rotation.to_3x3()@correction).to_4x4()
        rotation.translation=bone.head.copy();bone.matrix=rotation
        bpy.context.view_layer.update()
