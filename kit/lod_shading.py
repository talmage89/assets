"""Honor delivered glTF rest-frame normals/tangents in temporary LOD previews.

Blender's importer reads NORMAL but discards TANGENT. Its reconstructed Mikk
basis can differ on a reduced surface. Core glTF explicitly supplies that basis;
this adapter changes only the imported comparison scene, never delivery bytes.
The attributes are in world space so material evaluation is independent of
object-local shader coordinates. Call again after a different rest placement;
this is not a skin/animation controller.
"""
import numpy as np

CONVERT=np.array([[1,0,0],[0,0,-1],[0,1,0]],float)
TANGENT='_LOD_DeliveredTangentWorld'
SIGN='_LOD_DeliveredTangentSign'
PRESENT='_LOD_DeliveredTangentPresent'


def restore(doc):
    """Restore raw corner normals and evaluate normal maps in the given frame.

    Validate face/corner order against independent world positions before
    assigning data. Missing tangents keep the native Mikk path. Normal-map
    strength scales X/Y as specified by core glTF; all source pilot scales are
    one. Both base and coat Normal Map nodes use their own original texture.
    """
    import bpy
    bpy.context.view_layer.update()
    meshes=0;provided=0;max_position_error=0.;materials=set()
    for ni,node in enumerate(doc.data['nodes']):
        if 'mesh' not in node:continue
        ob=bpy.data.objects.get(node.get('name',''))
        if ob is None or ob.type!='MESH':raise ValueError('Missing imported LOD mesh '+str(node.get('name')))
        # A shared mesh can have differently oriented instances. World-frame
        # temporary attributes therefore belong to this imported object only.
        if ob.data.users>1:ob.data=ob.data.copy()
        mesh=ob.data;matrix=np.eye(4) if 'skin' in node else doc.world(ni)
        object_matrix=np.asarray(ob.matrix_world,dtype=float)
        xyz=[];normals=[];tangents=[];signs=[];present=[]
        for primitive in doc.data['meshes'][node['mesh']]['primitives']:
            a,f=doc.arrays(primitive);ids=f.ravel()
            xyz.append((a['POSITION'][ids]@matrix[:3,:3].T+matrix[:3,3])@CONVERT.T)
            nn=a['NORMAL'][ids].astype(float)@np.linalg.inv(matrix[:3,:3])@CONVERT.T
            nn/=np.maximum(np.linalg.norm(nn,axis=1,keepdims=True),1e-20)
            local=nn@object_matrix[:3,:3];local/=np.maximum(np.linalg.norm(local,axis=1,keepdims=True),1e-20);normals.append(local)
            if 'TANGENT' in a:
                tt=a['TANGENT'][ids]
                world_tangent=tt[:,:3]@matrix[:3,:3].T@CONVERT.T
                world_tangent/=np.maximum(np.linalg.norm(world_tangent,axis=1,keepdims=True),1e-20)
                tangents.append(world_tangent)
                signs.append(tt[:,3]*np.sign(np.linalg.det(matrix[:3,:3])));present.append(np.ones(len(ids)));provided+=len(ids)
            else:tangents.append(np.zeros((len(ids),3)));signs.append(np.ones(len(ids)));present.append(np.zeros(len(ids)))
        xyz=np.concatenate(xyz);normals=np.concatenate(normals)
        if len(mesh.loops)!=len(xyz) or any(len(p.vertices)!=3 for p in mesh.polygons):raise ValueError('Imported LOD triangle/corner order changed')
        actual=np.array([mesh.vertices[l.vertex_index].co[:] for l in mesh.loops],float)
        actual=actual@object_matrix[:3,:3].T+object_matrix[:3,3]
        error=float(np.linalg.norm(actual-xyz,axis=1).max(initial=0));max_position_error=max(max_position_error,error)
        if error>2e-5:raise ValueError('Imported LOD corner order/rest placement does not match delivered accessors')
        for polygon in mesh.polygons:polygon.use_smooth=True
        mesh.normals_split_custom_set(normals.tolist())
        for name,kind,values,property_name in [(TANGENT,'FLOAT_VECTOR',np.concatenate(tangents),'vector'),
                                                (SIGN,'FLOAT',np.concatenate(signs),'value'),
                                                (PRESENT,'FLOAT',np.concatenate(present),'value')]:
            attribute=mesh.attributes.get(name) or mesh.attributes.new(name,kind,'CORNER')
            attribute.data.foreach_set(property_name,np.asarray(values,np.float32).ravel())
        mesh.update()
        materials.update(m for m in mesh.materials if m);meshes+=1
    nodes=0;culled=0
    for material in materials:
        if not material.use_nodes or material.get('_lod_delivered_frame'):continue
        nt=material.node_tree
        def vector(operation,a=None,b=None):
            n=nt.nodes.new('ShaderNodeVectorMath');n.operation=operation
            for socket,value in zip(n.inputs,(a,b)):
                if value is None:continue
                if hasattr(value,'node'):nt.links.new(value,socket)
                else:socket.default_value=value
            return n.outputs[0]
        tangent=nt.nodes.new('ShaderNodeAttribute');tangent.attribute_name=TANGENT
        sign=nt.nodes.new('ShaderNodeAttribute');sign.attribute_name=SIGN
        present=nt.nodes.new('ShaderNodeAttribute');present.attribute_name=PRESENT
        geometry=nt.nodes.new('ShaderNodeNewGeometry');normal=geometry.outputs['Normal']
        bitangent=vector('CROSS_PRODUCT',normal,tangent.outputs['Vector'])
        # Vector SCALE has a scalar third input, unlike MULTIPLY's vector input.
        scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='SCALE'
        nt.links.new(bitangent,scale.inputs[0]);nt.links.new(sign.outputs['Fac'],scale.inputs['Scale']);bitangent=scale.outputs[0]
        for original in list(nt.nodes):
            if original.type!='NORMAL_MAP' or original.space!='TANGENT':continue
            consumers=list(original.outputs['Normal'].links)
            if not consumers:continue
            color=original.inputs['Color'];decode=nt.nodes.new('ShaderNodeVectorMath');decode.operation='MULTIPLY_ADD'
            if color.is_linked:nt.links.new(color.links[0].from_socket,decode.inputs[0])
            else:decode.inputs[0].default_value=color.default_value[:3]
            decode.inputs[1].default_value=(2,2,2);decode.inputs[2].default_value=(-1,-1,-1)
            separate=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(decode.outputs[0],separate.inputs[0])
            parts=[]
            for channel,basis in [('X',tangent.outputs['Vector']),('Y',bitangent),('Z',normal)]:
                value=separate.outputs[channel]
                if channel!='Z':
                    strength=nt.nodes.new('ShaderNodeMath');strength.operation='MULTIPLY';nt.links.new(value,strength.inputs[0])
                    source=original.inputs['Strength']
                    if source.is_linked:nt.links.new(source.links[0].from_socket,strength.inputs[1])
                    else:strength.inputs[1].default_value=source.default_value
                    value=strength.outputs[0]
                term=nt.nodes.new('ShaderNodeVectorMath');term.operation='SCALE';nt.links.new(basis,term.inputs[0]);nt.links.new(value,term.inputs['Scale']);parts.append(term.outputs[0])
            field=vector('NORMALIZE',vector('ADD',vector('ADD',parts[0],parts[1]),parts[2]))
            mix=nt.nodes.new('ShaderNodeMix');mix.data_type='VECTOR'
            nt.links.new(present.outputs['Fac'],mix.inputs[0]);nt.links.new(original.outputs['Normal'],mix.inputs[4]);nt.links.new(field,mix.inputs[5])
            for link in consumers:nt.links.new(mix.outputs[1],link.to_socket)
            nodes+=1
        if material.use_backface_culling:
            # Cycles ignores the importer's viewport culling flag. Core glTF
            # single-sided materials must also disappear from back-side rays.
            transparent=nt.nodes.new('ShaderNodeBsdfTransparent')
            for output in [n for n in nt.nodes if n.type=='OUTPUT_MATERIAL']:
                surface=output.inputs['Surface']
                if not surface.is_linked:continue
                original=surface.links[0].from_socket
                mix=nt.nodes.new('ShaderNodeMixShader')
                nt.links.new(geometry.outputs['Backfacing'],mix.inputs[0])
                nt.links.new(original,mix.inputs[1])
                nt.links.new(transparent.outputs[0],mix.inputs[2])
                nt.links.new(mix.outputs[0],surface)
            culled+=1
        material['_lod_delivered_frame']=True
    return dict(meshes=meshes,provided_tangent_corners=provided,normal_map_nodes=nodes,
                one_sided_materials=culled,max_position_error_m=max_position_error)
