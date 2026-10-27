"""Lossless geometry repack; only vertex tint is quantized (<= 0.5/255).

No compression extension or runtime dependency. Retain hard normals and UV0;
viewers generate MikkTSpace tangents for the eventual normal maps.
"""
import argparse
import copy
import json
from pathlib import Path
import struct
import numpy as np


def read(path):
    data=Path(path).read_bytes();offset=12;doc=None;binary=b''
    while offset<len(data):
        size,kind=struct.unpack_from('<II',data,offset);v=data[offset+8:offset+8+size];offset+=8+size
        if kind==0x4e4f534a:doc=json.loads(v)
        if kind==0x004e4942:binary=v
    return doc,binary


def audit(path):
    doc,binary=read(path);totals={};vertices=0
    for mesh in doc['meshes']:
        for p in mesh['primitives']:
            vertices+=doc['accessors'][p['attributes']['POSITION']]['count']
            for name,i in list(p['attributes'].items())+[('INDICES',p['indices'])]:
                a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']]
                totals[name]=totals.get(name,0)+v['byteLength']
    return dict(file_bytes=Path(path).stat().st_size,json_bytes=len(json.dumps(doc,separators=(',',':')).encode()),
                attribute_bytes=totals,export_vertices=vertices,meshes=len(doc['meshes']),
                primitives=sum(len(m['primitives']) for m in doc['meshes']))


def compact(path):
    path=Path(path);before=audit(path);doc,binary=read(path)
    assert not doc.get('animations') and not doc.get('skins')
    accessors=doc.pop('accessors');views=doc.pop('bufferViews');out=bytearray();new_views=[];new_acc=[]
    def view(payload,target=None):
        out.extend(b'\0'*(-len(out)%4));v=dict(buffer=0,byteOffset=len(out),byteLength=len(payload))
        if target:v['target']=target
        out.extend(payload);new_views.append(v);return len(new_views)-1
    cache={}
    def acc(index,semantic):
        key=(index,semantic)
        if key in cache:return cache[key]
        a=copy.deepcopy(accessors[index]);v=views[a['bufferView']]
        dt=np.dtype({5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']])
        n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
        arr=np.ndarray((a['count'],n),dtype=dt,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize)).copy()
        if semantic=='COLOR_0' and dt.kind=='f':
            arr=np.rint(np.clip(arr,0,1)*255).astype('u1');a['componentType']=5121;a['normalized']=True
            a.pop('min',None);a.pop('max',None)
        if semantic=='COLOR_0' and arr.dtype==np.dtype('u1') and arr.shape[1]==3:
            # Vertex attribute elements must start on four-byte boundaries.
            # RGBA8 costs one padding/alpha byte; tightly packed RGB8 is invalid.
            arr=np.column_stack((arr,np.full(len(arr),255,dtype='u1')));a['type']='VEC4'
        if semantic=='INDICES' and arr.max()<65536:
            arr=arr.astype('<u2');a['componentType']=5123
        if semantic!='INDICES':assert arr.shape[1]*arr.dtype.itemsize%4==0, 'glTF vertex attribute alignment'
        a.pop('byteOffset',None);a['bufferView']=view(arr.tobytes(),34963 if semantic=='INDICES' else 34962)
        new_acc.append(a);cache[key]=len(new_acc)-1;return cache[key]
    for mesh in doc['meshes']:
        for p in mesh['primitives']:
            p['attributes']={s:acc(i,s) for s,i in p['attributes'].items() if s!='TANGENT' and not s.startswith('TEXCOORD_1')}
            p['indices']=acc(p['indices'],'INDICES')
    for im in doc.get('images',[]):
        if 'bufferView' in im:
            v=views[im['bufferView']];start=v.get('byteOffset',0)
            im['bufferView']=view(binary[start:start+v['byteLength']])
    doc['accessors']=new_acc;doc['bufferViews']=new_views;doc['buffers']=[dict(byteLength=len(out))]
    out.extend(b'\0'*(-len(out)%4));j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*(-len(j)%4)
    payload=struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(out),0x004e4942)+out
    path.write_bytes(struct.pack('<III',0x46546c67,2,len(payload)+12)+payload)
    result=dict(before=before,after=audit(path),tint_max_quantization=.5/255)
    path.with_suffix('.size.json').write_text(json.dumps(result,indent=2));return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path',type=Path);p.add_argument('--compact',action='store_true');a=p.parse_args()
    print(json.dumps(compact(a.path) if a.compact else audit(a.path),indent=2))
