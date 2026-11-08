"""Independent serialized attribute error and shared-node storage audit."""
import json
import struct
from pathlib import Path
import numpy as np


def array(d,b,index):
    a=d['accessors'][index];v=d['bufferViews'][a['bufferView']]
    dt={5126:'<f4',5125:'<u4',5123:'<u2',5120:'i1',5121:'u1'}[a['componentType']]
    n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];size=np.dtype(dt).itemsize
    result=np.ndarray((a['count'],n),dtype=dt,buffer=b,
        offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',size*n),size)).astype(float)
    if a.get('normalized'):result=np.maximum(-1,result/{5120:127,5121:255,5123:65535}[a['componentType']])
    return result


def compare(d,b,path):
    raw=Path(path).read_bytes();size=struct.unpack_from('<I',raw,12)[0]
    old=json.loads(raw[20:20+size]);length=struct.unpack_from('<I',raw,20+size)[0]
    original=raw[28+size:28+size+length]
    lookup={n['name']:n for n in d['nodes'] if 'mesh' in n};seen=set()
    worst_position=worst_normal=worst_color=worst_uv=0.;vertices=triangles=0
    for node in old['nodes']:
        if 'mesh' not in node:continue
        target=lookup[node['name']];key=(node['mesh'],target['mesh'])
        if key in seen:continue
        seen.add(key);before=old['meshes'][node['mesh']];after=d['meshes'][target['mesh']]
        assert len(before['primitives'])==len(after['primitives'])
        for p,q in zip(before['primitives'],after['primitives']):
            assert np.array_equal(array(old,original,p['indices']),array(d,b,q['indices']))
            triangles+=old['accessors'][p['indices']]['count']//3
            for name in ('POSITION','NORMAL','COLOR_0','TEXCOORD_0','TEXCOORD_1'):
                if name not in q['attributes']:continue
                a=array(old,original,p['attributes'][name]);z=array(d,b,q['attributes'][name])
                assert a.shape==z.shape
                if name=='POSITION':
                    decode=after.get('extras',{}).get('river_position_decode')
                    if decode:z=z*decode[1]+decode[0]
                    worst_position=max(worst_position,float(abs(a-z).max()));vertices+=len(a)
                    if node.get('extras',{}).get('river_category')=='bridge':assert np.array_equal(a,z)
                elif name=='NORMAL':
                    a/=np.linalg.norm(a,axis=1)[:,None];z/=np.linalg.norm(z,axis=1)[:,None]
                    worst_normal=max(worst_normal,float(np.degrees(np.arccos(np.clip((a*z).sum(axis=1),-1,1))).max()))
                elif name=='COLOR_0':worst_color=max(worst_color,float(abs(a-z).max()))
                else:
                    decode=d['materials'][q['material']].get('extras',{}).get('river_uv_decode_'+name[-1])
                    if decode:z=z*np.array(decode[1])+np.array(decode[0])
                    worst_uv=max(worst_uv,float(abs(a-z).max()))
    assert worst_position<.0005 and worst_normal<.5 and worst_color<.002 and worst_uv<.0005
    return dict(compared_mesh_pairs=len(seen),compared_vertices=vertices,index_exact_triangles=triangles,
        maximum_position_axis_error_m=worst_position,maximum_normal_angle_degrees=worst_normal,
        maximum_linear_color_error=worst_color,maximum_uv_error=worst_uv,structural_positions_exact=True)


def audit(path):
    d=json.loads(Path(path).read_text());binary=Path(path).with_suffix('.bin').read_bytes()
    mesh_nodes=[n for n in d['nodes'] if 'mesh' in n]
    counts={i:0 for i in range(len(d['meshes']))}
    for n in mesh_nodes:counts[n['mesh']]+=1
    assert max(counts.values())>100,('No repeated mesh references',path)
    # Decode scales are measured from actual accessor ranges, independently
    # of the exporter receipt. All structural positions remain full precision.
    error=0;quantized=0
    for me in d['meshes']:
        decode=me.get('extras',{}).get('river_position_decode')
        if decode:
            quantized+=1;error=max(error,decode[1]/65535/2)
        for pr in me['primitives']:
            a=d['accessors'][pr['attributes']['POSITION']]
            assert a['componentType']==(5123 if decode else 5126)
    assert error<.0005
    total=Path(path).stat().st_size+len(binary)
    assert total<120_000_000,(path,total)
    source=Path('build/embedded')/(Path(path).stem+'.glb')
    correspondence=compare(d,binary,source) if source.exists() else None
    return dict(package_bytes=total,mesh_nodes=len(mesh_nodes),unique_meshes=len(counts),serialization=correspondence,
                maximum_mesh_references=max(counts.values()),quantized_context_meshes=quantized,
                maximum_context_position_half_step_m=error)


if __name__=='__main__':
    rows={str(s):audit(f'export/RiverCrossing-{s}.gltf') for s in (101,202)}
    Path('build/storage-check.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('STORAGE_CHECK_PASS',rows)
