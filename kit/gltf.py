"""Read-only GLB accessors for independent delivery/skin checks."""
import json,struct
import numpy as np
from mathutils import Matrix,Quaternion,Vector


class GLB:
    def __init__(self,path):
        data=path.read_bytes();magic,version,length=struct.unpack_from('<III',data)
        if magic!=0x46546c67 or version!=2 or length!=len(data):raise ValueError('Invalid GLB header')
        offset=12;self.binary=b''
        while offset<len(data):
            size,kind=struct.unpack_from('<II',data,offset);payload=data[offset+8:offset+8+size];offset+=8+size
            if kind==0x4e4f534a:self.json=json.loads(payload)
            elif kind==0x004e4942:self.binary=payload
        self.parents={child:i for i,node in enumerate(self.json['nodes']) for child in node.get('children',[])}
    def accessor(self,index):
        accessor=self.json['accessors'][index];view=self.json['bufferViews'][accessor['bufferView']]
        dtype=np.dtype({5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}[accessor['componentType']])
        components={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[accessor['type']]
        offset=view.get('byteOffset',0)+accessor.get('byteOffset',0);stride=view.get('byteStride',components*dtype.itemsize)
        array=np.ndarray((accessor['count'],components),dtype=dtype,buffer=self.binary,offset=offset,strides=(stride,dtype.itemsize)).copy()
        if accessor.get('normalized'):
            array=array.astype(float)/np.iinfo(dtype).max
        return array
    def local(self,index):
        node=self.json['nodes'][index]
        if 'matrix' in node:return np.array(node['matrix']).reshape(4,4).T
        translation=Matrix.Translation(node.get('translation',(0,0,0)))
        x,y,z,w=node.get('rotation',(0,0,0,1));rotation=Quaternion((w,x,y,z)).to_matrix().to_4x4()
        return np.array(translation@rotation@Matrix.Diagonal((*node.get('scale',(1,1,1)),1)))
    def world(self,index):
        local=self.local(index)
        return self.world(self.parents[index])@local if index in self.parents else local
    def image(self,index):
        image=self.json['images'][index]
        if 'uri' in image:raise ValueError('Delivery images must be embedded')
        view=self.json['bufferViews'][image['bufferView']];start=view.get('byteOffset',0)
        return self.binary[start:start+view['byteLength']]
