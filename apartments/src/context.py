"""Immutable instancing of repository-generated construction context."""
from pathlib import Path
import hashlib
import math
import bpy
from mathutils import Matrix
from geometry import Assembly
CACHE={}
def parent_chain(ob):
    out=[];p=ob.parent
    while p:out.append(p);p=p.parent
    return out


def load(kind):
    if kind in CACHE:return CACHE[kind]
    p=Path('build/context')/kind/'source.blend'
    if kind=='ground':
        before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(p.with_suffix('.glb').resolve()));obs=list(set(bpy.context.scene.objects)-before)
    else:
        with bpy.data.libraries.load(str(p.resolve()),link=False) as (src,dst):dst.objects=src.objects
        obs=[o for o in dst.objects if o]
        for o in obs:bpy.context.collection.objects.link(o)
    # Evaluate modifiers once; source shaders are quick-material approximations
    # for this checkpoint. Preserve botanical alpha/shoot pixels and custom normals.
    bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
    for ob in obs:
        if ob.type=='MESH' and ob.modifiers:
            ob.data=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True);ob.modifiers.clear()
        if ob.type=='MESH':
            for mat in ob.data.materials:
                if not mat or not mat.use_nodes:continue
                if kind in ('car','fence'):
                    # Replace source microstructure with its base constant. Form
                    # review must not imply a completed material bake.
                    bs=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
                    if bs:
                        for socket in ('Normal','Roughness','Base Color'):
                            for link in list(bs.inputs[socket].links):mat.node_tree.links.remove(link)
                        color=(.19,.23,.26) if kind=='car' and 'paint' in mat.name.lower() else (.25,.22,.16) if kind=='fence' else tuple(bs.inputs['Base Color'].default_value[:3])
                        bs.inputs['Base Color'].default_value=(*color,1)
            if kind in ('tree','shrub'):
                for slot,old in enumerate(list(ob.data.materials)):
                    ma=bpy.data.materials.get('ApartmentContext_'+old.name)
                    if not ma:
                        ma=bpy.data.materials.new('ApartmentContext_'+old.name);ma.use_nodes=True
                        bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.8
                        imgs=[n.image for n in old.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and 'BaseColor' in n.image.name]
                        foliage=('leaf' in ob.name.lower() or 'leaves' in ob.name.lower())
                        if foliage and imgs:
                            im=imgs[0]
                            if max(im.size)>1024:im.scale(1024,1024)
                            tx=ma.node_tree.nodes.new('ShaderNodeTexImage');tx.image=im
                            ma.node_tree.links.new(tx.outputs['Color'],bs.inputs['Base Color']);ma.node_tree.links.new(tx.outputs['Alpha'],bs.inputs['Alpha'])
                            ma.surface_render_method='DITHERED';ma.use_backface_culling=False
                        else:bs.inputs['Base Color'].default_value=(.10,.070,.038,1)
                    ob.data.materials[slot]=ma
        if ob.type=='MESH' and (kind in ('car','fence') or kind in ('tree','shrub') and 'leaf' not in ob.name.lower()):
            # Source-only constant-color context has no finished atlas chart.
            # Give those faces finite metric charts; keep actual leaf masks.
            for uv in list(ob.data.uv_layers):ob.data.uv_layers.remove(uv)
            uv=ob.data.uv_layers.new(name='UVMap')
            for face in ob.data.polygons:
                axes=sorted(range(3),key=lambda k:abs(face.normal[k]))[:2]
                for li in face.loop_indices:
                    v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]],v[axes[1]])
        if ob.type=='MESH' and kind=='fence':
            for i,old in enumerate(list(ob.data.materials)):
                metal='zinc' in old.name.lower() or 'hardware' in old.name.lower()
                name='ApartmentContext_FenceSteel' if metal else 'ApartmentContext_FenceWood'
                ma=bpy.data.materials.get(name)
                if ma is None:
                    ma=bpy.data.materials.new(name);ma.use_nodes=True;bs=ma.node_tree.nodes.get('Principled BSDF')
                    bs.inputs['Base Color'].default_value=(.24,.26,.24,1) if metal else (.25,.22,.16,1)
                    bs.inputs['Roughness'].default_value=.8
                ob.data.materials[i]=ma
        if ob.type=='MESH' and kind in ('tree','shrub'):
            # Stock botanical cards use BakeUV; consolidate into the common
            # chart name before joining bark/card meshes. Otherwise the glTF
            # active UV can select the bark's zero-filled chart on foliage.
            keep=ob.data.uv_layers.get('BakeUV')
            if keep:
                for uv in list(ob.data.uv_layers):
                    if uv!=keep:ob.data.uv_layers.remove(uv)
                keep.name='UVMap'
            for attr in list(ob.data.color_attributes):ob.data.color_attributes.remove(attr)
        ob.hide_render=True;ob.hide_set(True)
    # Consolidate each library module ONCE before instancing it. Joining copies
    # that share mesh data mutates every copy and can multiply runtime geometry.
    roots=[o for o in obs if o.parent not in obs]
    for root in roots:
        parts=[o for o in [root,*root.children_recursive] if o.type=='MESH']
        if not parts:continue
        for ob in parts:
            if ob.data.users>1:ob.data=ob.data.copy()
        bpy.ops.object.select_all(action='DESELECT')
        for ob in parts:ob.hide_set(False);ob.select_set(True)
        bpy.context.view_layer.objects.active=parts[0]
        if len(parts)>1:bpy.ops.object.join()
        ob=bpy.context.object;world=ob.matrix_world.copy();ob.parent=root if ob!=root else None;ob.matrix_world=world
        if ob!=root:
            ob.data.transform(ob.matrix_basis);ob.matrix_basis=Matrix.Identity(4)
    obs=[o for root in roots for o in [root,*root.children_recursive]]
    for ob in obs:ob.hide_render=True;ob.hide_set(True)
    CACHE[kind]=obs;return obs


def instance(kind,parent,name,p,yaw=0,select=None,scale=(1,1,1)):
    obs=load(kind)
    if select:
        roots=[o for o in obs if o.name.split('.')[0]==select]
        if not roots:raise ValueError('Missing library module '+select)
        chosen=[o for o in obs if o==roots[0] or roots[0] in parent_chain(o)]
        anchor=roots[0];base=anchor.matrix_world.copy().inverted()
    else:
        chosen=obs;anchor=None;base=Matrix.Identity(4)
    rt=Assembly(name,parent=parent,loc=p,yaw=yaw).root;rt.scale=scale;rt['context_family']=kind
    copies={o:o.copy() for o in chosen}
    for ob,cp in copies.items():
        bpy.context.collection.objects.link(cp);cp.hide_render=False;cp.hide_set(False)
        cp.name=name+'__'+ob.name;cp.parent=copies.get(ob.parent,rt)
        cp.matrix_basis=ob.matrix_basis.copy() if ob.parent in chosen else base@ob.matrix_world
        cp['context_family']=kind
        # Stock floor origins and root positions are preserved; each placement
        # applies one explicit parent transform, never inherits a prior instance.
    if scale!=(1,1,1):
        # Carry scale through template empties into copied mesh coordinates.
        # Socket positions move with it, while every exported frame is unit scale.
        bpy.context.view_layer.update()
        def apply_scale(ob):
            loc,rot,sc=ob.matrix_basis.decompose();matrix=Matrix.Diagonal((*sc,1))
            ob.matrix_basis=Matrix.Translation(loc)@rot.to_matrix().to_4x4()
            if ob.type=='MESH':ob.data=ob.data.copy();ob.data.transform(matrix)
            for child in ob.children:
                child.matrix_basis=matrix@child.matrix_basis;apply_scale(child)
        apply_scale(rt)
    return rt


def clear_templates():
    for obs in CACHE.values():
        for ob in obs:
            if ob.name in bpy.data.objects:bpy.data.objects.remove(ob,do_unlink=True)
    CACHE.clear()
