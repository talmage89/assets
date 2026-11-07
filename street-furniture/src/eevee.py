"""Interpret the imported transmission mask for Eevee's per-material sorting.

The glTF evaluates transmission per texel. Eevee's refraction pass is selected
per material instead, so opaque print needs an equivalent opaque state. This
presentation adapter keeps every imported vertex, UV, map and PBR value; it
does not write an export or increase the delivery's image allocation.
"""
import bpy

def setup(scene):
    scene.eevee.use_raytracing=True
    scene.eevee.ray_tracing_options.resolution_scale='1'
    scene.eevee.ray_tracing_options.screen_trace_quality=.75
    scene.eevee.ray_tracing_options.trace_max_roughness=.7
    opaque={};processed=set()
    for ob in scene.objects:
        if ob.type!='MESH' or ob.data in processed:continue
        processed.add(ob.data);me=ob.data
        for face in me.polygons:
            mat=me.materials[face.material_index]
            if 'StreetFurniture_GraphicsGlazing' not in mat.name:continue
            uv=me.uv_layers['UVMap']
            if sum(uv.data[i].uv.x for i in face.loop_indices)/len(face.loop_indices)<.5:continue
            if mat not in opaque:
                copy=mat.copy();copy.name=mat.name+'_EeveeOpaquePrint'
                p=copy.node_tree.nodes.get('Principled BSDF');weight=p.inputs['Transmission Weight']
                for link in list(weight.links):copy.node_tree.links.remove(link)
                weight.default_value=0;copy.use_raytrace_refraction=False;opaque[mat]=copy
            copy=opaque[mat]
            if copy.name not in me.materials:me.materials.append(copy)
            face.material_index=me.materials.find(copy.name)
    for mat in bpy.data.materials:
        bs=mat.node_tree.nodes.get('Principled BSDF') if mat.use_nodes else None
        if bs and (bs.inputs['Transmission Weight'].is_linked or bs.inputs['Transmission Weight'].default_value>0):
            mat.use_raytrace_refraction=True;mat.thickness_mode='SLAB'
            val=mat.node_tree.nodes.new('ShaderNodeValue');val.outputs[0].default_value=.004
            out=next(n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL')
            mat.node_tree.links.new(val.outputs[0],out.inputs['Thickness'])
