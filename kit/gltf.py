"""Raw GLB accessors and guarded export-rounding stabilization."""
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


def stabilize_tangents(path, anchors):
    """Restore explicitly accepted rounded tangents at guarded source corners.

    MikkTSpace's final four-decimal export can straddle a rounding boundary.
    Callers supply asset-owned anchors, never a previous binary dependency.
    Exact position/normal/UV signatures and a one-rounding-step bound protect
    against masking geometry changes. Only the anchored tangent bytes change.
    """
    from pathlib import Path
    path=Path(path);g=GLB(path);payload=bytearray(path.read_bytes());offset=12
    while offset<len(payload):
        size,kind=struct.unpack_from('<II',payload,offset)
        if kind==0x004e4942:break
        offset+=8+size
    else:raise ValueError('GLB contains no BIN chunk')
    for anchor in anchors:
        primitive=g.json['meshes'][anchor['mesh']]['primitives'][anchor['primitive']]
        attributes=primitive['attributes'];vertex=anchor['vertex']
        for key,attribute in [('position','POSITION'),('normal','NORMAL'),('uv','TEXCOORD_0')]:
            actual=g.accessor(attributes[attribute])[vertex]
            if not np.array_equal(actual,np.asarray(anchor[key],dtype=np.float32)):
                raise ValueError('Tangent rounding anchor differs: '+key)
        index=attributes['TANGENT'];accessor=g.json['accessors'][index]
        view=g.json['bufferViews'][accessor['bufferView']]
        if accessor['componentType']!=5126 or accessor['type']!='VEC4':
            raise ValueError('Expected FLOAT VEC4 tangents')
        actual=g.accessor(index)[vertex];expected=np.asarray(anchor['tangent'],dtype=np.float32)
        if np.max(np.abs(actual-expected))>.00011:
            raise ValueError('Tangent differs by more than one rounding step')
        start=offset+8+view.get('byteOffset',0)+accessor.get('byteOffset',0)+vertex*view.get('byteStride',16)
        struct.pack_into('<4f',payload,start,*expected)
    path.write_bytes(payload)
    return len(anchors)


if __name__=='__main__':
    import argparse,runpy,sys
    from pathlib import Path
    parser=argparse.ArgumentParser(description='Guarded tangent export-rounding stabilization')
    parser.add_argument('--source',required=True);parser.add_argument('--config',required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    config=runpy.run_path(args.config)
    count=stabilize_tangents(Path(args.source),config['EXPORT_TANGENT_ROUNDING'])
    print('STABILIZED',count,'guarded tangent corners')
