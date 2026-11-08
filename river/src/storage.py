"""Bounded storage quantization for native context; bridge positions stay FLOAT.

Uniform position decode preserves normal directions. UV decode composes with
each existing texture transform, retaining tiling and material image identity.
"""
import copy
import math
import numpy as np


def compact(d,binary):
    payload=bytearray(binary)
    def read(index):
        a=d['accessors'][index];v=d['bufferViews'][a['bufferView']]
        n={'VEC2':2,'VEC3':3}[a['type']]
        assert a['componentType']==5126
        return np.ndarray((a['count'],n),dtype='<f4',buffer=binary,
            offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',4*n),4))
    def write(values,kind):
        n=values.shape[1];packed=np.zeros((len(values),4 if n==3 else 2),dtype='<u2')
        packed[:,:n]=np.rint(np.clip(values,0,1)*65535)
        payload.extend(b'\0'*(-len(payload)%4));offset=len(payload);payload.extend(packed.tobytes())
        index=len(d['accessors']);a=dict(bufferView=len(d['bufferViews']),componentType=5123,
            normalized=True,count=len(values),type=kind)
        if kind=='VEC3':a.update(min=packed[:,:n].min(axis=0).tolist(),max=packed[:,:n].max(axis=0).tolist())
        d['accessors'].append(a)
        d['bufferViews'].append(dict(buffer=0,byteOffset=offset,byteLength=packed.nbytes,byteStride=packed.shape[1]*2,target=34962))
        return index
    def textures(value):
        if isinstance(value,dict):
            if 'index' in value:yield value
            else:
                for v in value.values():yield from textures(v)
        elif isinstance(value,list):
            for v in value:yield from textures(v)
    # A common UV decode for every use of one material/channel.
    groups={}
    for mesh in d['meshes']:
        for pr in mesh['primitives']:
            for key,index in pr['attributes'].items():
                if key.startswith('TEXCOORD_'):groups.setdefault((pr['material'],int(key[9:])),set()).add(index)
    for (material,channel),indices in groups.items():
        samples=[read(i) for i in sorted(indices)];lo=np.min([v.min(axis=0) for v in samples],axis=0)
        extent=np.maximum(np.max([v.max(axis=0) for v in samples],axis=0)-lo,1e-6)
        # Keep long terrain charts exact; native building charts fit below 64.
        if extent.max()>64:continue
        remap={i:write((read(i)-lo)/extent,'VEC2') for i in sorted(indices)}
        for mesh in d['meshes']:
            for pr in mesh['primitives']:
                key='TEXCOORD_'+str(channel)
                if pr['material']==material and key in pr['attributes']:pr['attributes'][key]=remap[pr['attributes'][key]]
        ma=d['materials'][material]
        ma.setdefault('extras',{})['river_uv_decode_'+str(channel)]=[lo.tolist(),extent.tolist()]
        for tex in textures(ma):
            ext=tex.get('extensions',{}).get('KHR_texture_transform',{})
            if ext.get('texCoord',tex.get('texCoord',0))!=channel:continue
            scale=np.array(ext.get('scale',[1,1]));offset=np.array(ext.get('offset',[0,0]));angle=ext.get('rotation',0)
            rotation=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
            ext.update(scale=(scale*extent).tolist(),offset=(offset+rotation@(scale*lo)).tolist())
            tex.setdefault('extensions',{})['KHR_texture_transform']=ext
    # Quantize only context/cars, with a measured maximum half-step < 0.5mm.
    mesh_ids={n['mesh'] for n in d['nodes'] if 'mesh' in n and n.get('extras',{}).get('river_category') in ('context','cars')}
    decodes={};worst=0
    for mi in sorted(mesh_ids):
        mesh=d['meshes'][mi];indices={pr['attributes']['POSITION'] for pr in mesh['primitives']}
        lo=np.min([read(i).min(axis=0) for i in indices],axis=0)
        span=float(np.max([read(i).max(axis=0)-lo for i in indices]))
        if span/65535/2>.0005 or span<1e-6:continue
        remap={i:write((read(i)-lo)/span,'VEC3') for i in sorted(indices)}
        for pr in mesh['primitives']:pr['attributes']['POSITION']=remap[pr['attributes']['POSITION']]
        decodes[mi]=(lo,span);worst=max(worst,span/65535/2)
        mesh.setdefault('extras',{})['river_position_decode']=[lo.tolist(),span]
    # Decode below the original transform/pivot, leaving child placements intact.
    for node in list(d['nodes']):
        if node.get('mesh') not in decodes:continue
        lo,span=decodes[node['mesh']]
        wrapper=copy.deepcopy(node);wrapper.pop('mesh');wrapper['name']=node.get('name','Geometry')+'__Placement'
        index=len(d['nodes']);d['nodes'].append(wrapper)
        original=d['nodes'].index(node)
        for parent in d['nodes']:
            if 'children' in parent:parent['children']=[index if i==original else i for i in parent['children']]
        for scene in d.get('scenes',[]):scene['nodes']=[index if i==original else i for i in scene['nodes']]
        wrapper['children']=[original]+wrapper.get('children',[])
        for key in ('matrix','translation','rotation','scale','children'):node.pop(key,None)
        node.update(translation=lo.tolist(),scale=[span]*3)
    d.setdefault('extensionsUsed',[])
    if 'KHR_texture_transform' not in d['extensionsUsed']:d['extensionsUsed'].append('KHR_texture_transform')
    d.setdefault('asset',{}).setdefault('extras',{})['maximum_context_position_half_step_m']=worst
    return payload
