"""Rigid held-asset convention, generalized from the owner's procedural rifle.

Meters; grip origin; +Y forward, +Z up, +X right. This module contains visual
asset plumbing only. Asset-specific geometry and pose timings stay in families.
Existing prop/chain rigs and export entry points are unaffected.
"""
import math
from pathlib import Path
import bpy
from mathutils import Matrix, Vector
from kit.rig import bind


def armature(name, heads, parents=None, length=.02):
    """Parallel +Y bones, zero roll; unconnected children of Root by default."""
    bpy.ops.object.select_all(action='DESELECT')
    data=bpy.data.armatures.new(name)
    arm=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(arm)
    arm.select_set(True);bpy.context.view_layer.objects.active=arm
    bpy.ops.object.mode_set(mode='EDIT')
    bones={}
    for key,head in heads.items():
        b=data.edit_bones.new(key);b.head=head;b.tail=Vector(head)+Vector((0,length,0));b.roll=0
        bones[key]=b
    for key,b in bones.items():
        parent=(parents or {}).get(key,'Root' if key!='Root' else None)
        if parent:b.parent=bones[parent];b.use_connect=False
    bpy.ops.object.mode_set(mode='OBJECT');arm.select_set(False)
    arm['frame']='grip origin; +Y forward; +Z up; +X right; meters'
    return arm


def rigid_bind(ob,arm,bone,export_part=None):
    if bone not in arm.data.bones:raise ValueError(bone)
    bind(ob,arm,[{bone:1.0} for _ in ob.data.vertices],
         export_part=export_part or ob.name,modifier_name='Rigid weapon skin')
    ob['bone']=bone
    return ob


def sockets(arm,positions,riding=None):
    """Static sockets are scene-root nodes. Riding sockets retain their world rest pose."""
    output=[]
    for name,pos in positions.items():
        ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob)
        ob.empty_display_type='ARROWS';ob.empty_display_size=.009
        ob['socket_kind']=name.removeprefix('Socket_')
        ob.location=pos
        if name in (riding or {}):
            ob.parent=arm;ob.parent_type='BONE';ob.parent_bone=riding[name]
            bpy.context.view_layer.update();ob.matrix_world=Matrix.Translation(Vector(pos))
        output.append(ob)
    return output


def fcurves(action):
    if action.layers:
        return [fc for layer in action.layers for strip in layer.strips
                for bag in strip.channelbags for fc in bag.fcurves]
    return list(action.fcurves)


def hold(frame):
    """An explicit complete-pose hold boundary in an action schedule."""
    return frame,{}


def action(arm,name,keys,interpolation='LINEAR',fps=60,discrete=('scale',)):
    """Complete pose keys with explicit move/hold boundaries and step states.

    Every schedule entry keys EVERY bone/channel. Omitted values carry forward
    at that entry, so hold(frame) really inserts a boundary before a later move.
    Changes interpolate from the preceding boundary; callers supply the start
    of each move. Channels in discrete use CONSTANT interpolation (outgoing
    segment), so visibility never grows/shrinks between state changes.
    Pass discrete=() to deliberately animate scale. Unknown bones/channels and
    duplicate times fail rather than silently dropping schedule errors.
    """
    bpy.context.scene.render.fps=fps
    act=bpy.data.actions.new(name);act.use_fake_user=True
    arm.animation_data_create();arm.animation_data.action=act
    state={b.name:{} for b in arm.pose.bones};keys=sorted(keys,key=lambda row:row[0])
    if len({f for f,_ in keys})!=len(keys):raise ValueError('Duplicate action time')
    first,last=keys[0][0],keys[-1][0]
    for frame,overrides in keys:
        if set(overrides)-set(state):raise ValueError('Unknown bones: '+str(set(overrides)-set(state)))
        for bone in arm.pose.bones:
            if set(overrides.get(bone.name,{}))-{'loc','rot_deg','scale'}:raise ValueError('Unknown pose channel')
            state[bone.name].update(overrides.get(bone.name,{}));s=state[bone.name]
            bone.rotation_mode='XYZ';bone.location=s.get('loc',(0,0,0))
            bone.rotation_euler=tuple(math.radians(v) for v in s.get('rot_deg',(0,0,0)))
            bone.scale=s.get('scale',(1,1,1))
            for channel in ('location','rotation_euler','scale'):
                bone.keyframe_insert(channel,frame=frame,group=bone.name)
    for fc in fcurves(act):
        channel=fc.data_path.rsplit('.',1)[-1]
        for key in fc.keyframe_points:key.interpolation='CONSTANT' if channel in discrete else interpolation
    act.use_frame_range=True;act.frame_range=(first,last)
    track=arm.animation_data.nla_tracks.new();track.name=name
    track.strips.new(name,int(first),act);track.mute=True
    arm.animation_data.action=None
    pose(arm,None,0)
    return act


def animation_options(policy):
    """Opt-in settings shared by inspection and established atlas exporters."""
    if not policy:return dict(export_animations=False)
    policy={} if policy is True else policy
    return dict(export_animations=True,export_animation_mode=policy.get('mode','ACTIONS'),
                export_force_sampling=policy.get('force_sampling',True),
                export_optimize_animation_size=False,export_anim_single_armature=True,
                export_def_bones=False)


def pose(arm,name,frame):
    arm.animation_data_create()
    for track in arm.animation_data.nla_tracks:track.mute=True
    arm.animation_data.action=None
    for b in arm.pose.bones:b.matrix_basis=Matrix.Identity(4)
    if name:
        act=bpy.data.actions.get(name) or next(a for a in bpy.data.actions if a.name.startswith(name+'_'))
        arm.animation_data.action=act
        if act.slots:arm.animation_data.action_slot=act.slots[0]
    whole=math.floor(frame);bpy.context.scene.frame_set(whole,subframe=frame-whole)
    bpy.context.view_layer.update()


def export(path,objects,animations=True):
    """Selected GLB with rifle-compatible named NLA clips and sockets.

    Materials are supplied by the caller (checkpoint constants or baked atlas).
    Does not silently bake/replace them, pack UVs, or certify final delivery.
    """
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLB',use_selection=True,
        export_yup=True,export_apply=False,export_texcoords=True,export_normals=True,
        export_skins=True,export_extras=True,export_cameras=False,export_lights=False,
        **animation_options(animations))


def joined_copy(parts,name):
    """Join copies in rest space; preserve rigid weights and original source parts."""
    copies=[]
    for ob in parts:
        copy=ob.copy();copy.data=ob.data.copy();bpy.context.collection.objects.link(copy)
        copy.modifiers.clear();copies.append(copy)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in copies:ob.select_set(True)
    bpy.context.view_layer.objects.active=copies[0]
    if len(copies)>1:bpy.ops.object.join()
    result=copies[0];result.name=name;result.data.name=name
    return result


def detachable(parts,arm,bone,name,*,minimum_scale=.001):
    """Snapshot evaluated rigid parts in a bone's full posed spawn frame.

    Zero-scale discrete parts are omitted. Mesh data is copied; source skin,
    materials/UVs and pose remain untouched. The returned unskinned mesh has
    identity transform and can be spawned with the matching socket matrix.
    Works in rest, rotated reloads, and nested moving-parent assemblies.
    """
    frame=arm.matrix_world@arm.pose.bones[bone].matrix
    copies=[];deps=bpy.context.evaluated_depsgraph_get()
    for ob in parts:
        owner=ob.get('bone')
        if owner and min(abs(v) for v in arm.pose.bones[owner].matrix.to_scale())<minimum_scale:continue
        ev=ob.evaluated_get(deps)
        data=bpy.data.meshes.new_from_object(ev,preserve_all_data_layers=True,depsgraph=deps)
        data.transform(frame.inverted()@ev.matrix_world)
        copy=bpy.data.objects.new(name+' part',data);bpy.context.collection.objects.link(copy)
        copies.append(copy)
    if not copies:raise ValueError('Detachable contains no visible surfaces')
    bpy.ops.object.select_all(action='DESELECT')
    for ob in copies:ob.select_set(True)
    bpy.context.view_layer.objects.active=copies[0]
    if len(copies)>1:bpy.ops.object.join()
    result=copies[0];result.name=result.data.name=name
    result['spawn_bone']=bone
    return result
