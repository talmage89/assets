"""Measured shared-image/effective-asphalt values, using memory-mapped accessors.

No delivery is changed. Vertex samples describe actual exported PBR inputs,
not an exposure-independent photographic reflectance measurement.
"""
import argparse,json,struct,hashlib
from pathlib import Path
import numpy as np
from PIL import Image


def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def document(path):
    path=Path(path)
    if path.suffix=='.glb':
        with path.open('rb') as f:
            f.seek(12);length,kind=struct.unpack('<II',f.read(8));assert kind==0x4e4f534a
            doc=json.loads(f.read(length));length,kind=struct.unpack('<II',f.read(8));assert kind==0x004e4942
            offset=f.tell()
        return doc,np.memmap(path,mode='r',dtype='u1',offset=offset,shape=(length,))
    doc=json.loads(path.read_text());return doc,np.memmap(path.parent/doc['buffers'][0]['uri'],mode='r',dtype='u1')


def accessor(doc,binary,index):
    a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']];dt=np.dtype({5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    values=np.ndarray((a['count'],n),dtype=dt,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize))
    if a.get('normalized') and dt.kind=='u':return values.astype('float32')/np.iinfo(dt).max
    return values


def sample(path,texture):
    doc,binary=document(path);all_color=[];all_tint=[];specular=set();roughness=set();rough_texture=set()
    for mesh in doc['meshes']:
        for pr in mesh['primitives']:
            mat=doc['materials'][pr['material']]
            if not mat['name'].startswith('Asphalt'):continue
            roughness.add(mat.get('pbrMetallicRoughness',{}).get('roughnessFactor',1));rough_texture.add('metallicRoughnessTexture' in mat.get('pbrMetallicRoughness',{}))
            specular.add(mat.get('extensions',{}).get('KHR_materials_specular',{}).get('specularFactor',1))
            at=pr['attributes'];uv=accessor(doc,binary,at['TEXCOORD_0']);tint=accessor(doc,binary,at['COLOR_0'])[:,:3] if 'COLOR_0' in at else np.ones((len(uv),3),dtype='float32')
            y=np.floor((uv[:,1]%1)*texture.shape[0]).astype(int)%texture.shape[0];x=np.floor((uv[:,0]%1)*texture.shape[1]).astype(int)%texture.shape[1]
            base=np.array(mat.get('pbrMetallicRoughness',{}).get('baseColorFactor',[1,1,1,1])[:3]);color=texture[y,x]*tint*base
            all_tint.append(tint);all_color.append(color)
    colors=np.concatenate(all_color);tints=np.concatenate(all_tint);values=colors@np.array([.2126,.7152,.0722]);median=np.median(tints,axis=0)
    return dict(source=str(path),source_sha256=digest(path),vertices=len(colors),specular_factors=sorted(specular),roughness_factors=sorted(roughness),roughness_texture_used=any(rough_texture),median_tint_rgb=median.tolist(),effective_linear_Y_percentiles=np.percentile(values,[10,50,90]).tolist())


def run(out):
    path=Path('../ground/textures/ship/T_Asphalt_BaseColor.png');a=np.asarray(Image.open(path).convert('RGB'),dtype='float32')/255
    lin=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);y=a@np.array([.2126,.7152,.0722]);rows={}
    for key,p in (('Ground',Path('../ground/export/Ground.glb')),('Gas',Path('export/CommercialGas-101.gltf')),('Strip',Path('export/CommercialStrip-201.gltf'))):rows[key]=sample(p,lin)
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(dict(shared_map_sha256=digest(path),shared_map_median_Yprime=float(np.median(y)),shared_map_median_linear_Y=float(np.median(lin@np.array([.2126,.7152,.0722]))),rows=rows,scope=__doc__),indent=2)+'\n')
    for key,row in rows.items():print(key,'actual median Tint',row['median_tint_rgb'],'effective linear Y p10/50/90',row['effective_linear_Y_percentiles'])

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',default='build/strip-value/material-values.json');run(a.parse_args().out)
