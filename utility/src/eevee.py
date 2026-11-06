"""Eevee checkpoint of the exported utility, with equivalent context shaders.

The Cape source keeps bake-channel branches and repeated attribute nodes.
Packing its scalar masks losslessly into RGBA attributes, consolidating
identical reads and dropping unreachable source-only branches
avoids Eevee's vertex-attribute compiler limit. No field is averaged or
recolored; exported Utility stock PBR and all context geometry are untouched.
"""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
import render as R


def compact(tree):
    nodes,links=tree.nodes,tree.links;before=len(nodes);alive=set();pending=[n for n in nodes if n.type=='OUTPUT_MATERIAL' and n.is_active_output]
    while pending:
        n=pending.pop()
        if n in alive:continue
        alive.add(n);pending.extend(l.from_node for i in n.inputs for l in i.links)
    for n in list(nodes):
        if n not in alive:nodes.remove(n)
    seen={};duplicates=0
    for n in list(nodes):
        if n.type=='ATTRIBUTE':key=(n.type,n.attribute_name,n.attribute_type)
        elif n.type=='VERTEX_COLOR':key=(n.type,n.layer_name)
        elif n.type=='UVMAP':key=(n.type,n.uv_map,n.from_instancer)
        elif n.type=='TEX_COORD':key=(n.type,n.object,n.from_instancer)
        else:continue
        if key not in seen:seen[key]=n;continue
        keep=seen[key]
        for i,out in enumerate(n.outputs):
            destinations=[l.to_socket for l in out.links]
            for l in list(out.links):links.remove(l)
            for socket in destinations:links.new(keep.outputs[i],socket)
        nodes.remove(n);duplicates+=1
    return dict(before=before,after=len(nodes),identical_reads_merged=duplicates)

def pack_scalars(objects,materials):
    """Exact Cape/Split scalar mask packing, only on staged context data."""
    import numpy as np
    references={}
    for m in materials:
        if not m.use_nodes:continue
        for n in m.node_tree.nodes:
            if n.type=='ATTRIBUTE' and n.attribute_type=='GEOMETRY':references.setdefault(n.attribute_name,[]).append((m,n))
    names=sorted(name for name,refs in references.items() if (name.startswith('Cape') or name=='SplitCoping') and all(n.outputs['Fac'].is_linked and not any(o.is_linked for o in n.outputs if o!=n.outputs['Fac']) for m,n in refs))
    groups=[names[i:i+4] for i in range(0,len(names),4)];referenced_materials={m for name in names for m,n in references[name]};meshes={o.data for o in objects if o.type=='MESH'};measured=[]
    for me in meshes:
        if not any(me.attributes.get(n) for n in names) and not any(m in referenced_materials for m in me.materials):continue
        vi=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',vi)
        for gi,group in enumerate(groups):
            packed=np.zeros((len(me.loops),4),np.float32)
            for ci,name in enumerate(group):
                attr=me.attributes.get(name)
                if attr is None:continue
                dtype={'FLOAT':np.float32,'INT':np.int32,'BOOLEAN':np.bool_}.get(attr.data_type)
                assert dtype is not None,(me.name,name,attr.data_type)
                values=np.empty(len(attr.data),dtype);attr.data.foreach_get('value',values)
                if attr.domain=='POINT':packed[:,ci]=values[vi]
                elif attr.domain=='CORNER':packed[:,ci]=values
                elif attr.domain=='FACE':
                    for face in me.polygons:packed[face.loop_start:face.loop_start+face.loop_total,ci]=values[face.index]
                else:raise ValueError((name,attr.domain))
            key='UtilityEeveeFields'+str(gi);out=me.color_attributes.new(name=key,type='FLOAT_COLOR',domain='CORNER');out.data.foreach_set('color',packed.ravel())
            actual=np.empty(packed.size,np.float32);out.data.foreach_get('color',actual)
            error=float(np.max(abs(actual-packed.ravel())));assert error==0
            measured.append(dict(mesh=me.name,pack=key,source_fields=group,maximum_roundtrip_error=error))
        for name in names:
            attr=me.attributes.get(name)
            if attr:me.attributes.remove(attr)
    for m in materials:
        if not m.use_nodes:continue
        ns,ls=m.node_tree.nodes,m.node_tree.links;cache={}
        for gi,group in enumerate(groups):
            relevant=[(name,n) for name in group for mat,n in references[name] if mat==m]
            if not relevant:continue
            color=ns.new('ShaderNodeVertexColor');color.layer_name='UtilityEeveeFields'+str(gi)
            separate=ns.new('ShaderNodeSeparateColor');separate.mode='RGB';ls.new(color.outputs['Color'],separate.inputs[0])
            for name,n in relevant:
                ci=group.index(name);output=separate.outputs[ci] if ci<3 else color.outputs['Alpha']
                targets=[l.to_socket for l in n.outputs['Fac'].links]
                for link in list(n.outputs['Fac'].links):ls.remove(link)
                for target in targets:ls.new(output,target)
                ns.remove(n)
    return dict(scalar_fields=names,packs=groups,mesh_roundtrips=measured)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/final-eevee'));p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=64)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.engine='BLENDER_EEVEE';a.camera_file=None;a.validate_only=False
    original_context=R.context
    def context(meta):
        obs,provenance=original_context(meta);materials={slot.material for o in obs if o.type=='MESH' for slot in o.material_slots if slot.material}
        rows={m.name:compact(m.node_tree) for m in materials if m.use_nodes and not m.name.startswith('Utility')}
        packing=pack_scalars(obs,materials)
        Path('build/eevee-context.json').write_text(json.dumps(dict(compaction=rows,packing=packing),indent=2))
        provenance.append(dict(scope='Eevee context-only equivalent shader DAG compaction; same fields, values and geometry; exported Utility unchanged',materials=rows,lossless_scalar_packing=packing))
        return obs,provenance
    R.context=context;R.render_run(101,a,['hero'])
