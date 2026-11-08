"""Native factory paint decoded from original PNG bytes, in linear light.

Blender's byte image pixel buffer is not the shader's scene-linear color output.
Read the original delivery's embedded PNG and neutral coverage explicitly.
The original GLBs and all their images remain immutable.
"""
import hashlib,io,json,struct,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.image_io import srgb_to_linear,linear_to_srgb,write_png
BODIES=('AlderH120','AlderX220','AlderC150')
# Local fleet options use the native coverage transfer and the same three maps.
# These three authored tints are not claimed as delivered car-family presets.
LOCAL_COLORS={'Garnet':(.29,.012,.016),'Spruce':(.032,.08,.052),'Sand':(.30,.23,.145)}
COLORS=('Porcelain','Carbon','Aluminum','Graphite',*LOCAL_COLORS)
FLEET=('Aluminum','Graphite','Carbon','Porcelain','Atlantic','Garnet','Spruce','Sand')
WEIGHTS=(22,16,22,12,12,10,4,2)
_sources={}

def palette(extras):return dict(json.loads(extras['paint_colors']),**LOCAL_COLORS)

def source(body):
    if body in _sources:return _sources[body]
    path=ROOT/'cars/export'/(body+'.glb');raw=path.read_bytes();offset=12;doc=None;binary=None
    while offset<len(raw):
        size,kind=struct.unpack_from('<II',raw,offset);chunk=raw[offset+8:offset+8+size];offset+=8+size
        if kind==0x4e4f534a:doc=json.loads(chunk)
        elif kind==0x004e4942:binary=chunk
    mat=next(m for m in doc['materials'] if m.get('extras',{}).get('paint_decode'))
    index=mat['pbrMetallicRoughness']['baseColorTexture']['index'];im=doc['images'][doc['textures'][index]['source']]
    if 'bufferView' in im:
        view=doc['bufferViews'][im['bufferView']];start=view.get('byteOffset',0);png=binary[start:start+view['byteLength']]
    else:png=(path.parent/im['uri']).read_bytes()
    rgba=np.asarray(Image.open(io.BytesIO(png)).convert('RGBA'),np.float32)/255
    result=(rgba,mat['extras'],hashlib.sha256(png).hexdigest());_sources[body]=result;return result

def expected(body,color):
    rgba,extras,h=source(body);colors=palette(extras);ref=np.asarray(extras['paint_reference_color'])
    linear=np.clip(srgb_to_linear(rgba[:,:,:3])+rgba[:,:,3,None]*(np.asarray(colors[color])-ref),0,1)
    reduced=np.stack([np.asarray(Image.fromarray(linear[:,:,i]).resize((1024,1024),Image.Resampling.LANCZOS)) for i in range(3)],axis=2)
    return linear_to_srgb(np.clip(reduced,0,1)),dict(source_png_sha256=h,color=colors[color],reference=ref.tolist(),size=1024)

def ensure(material_name,color):
    body=next(b for b in BODIES if b in material_name);path=Path('textures/context')/(body+'Paint_'+color+'.png');receipt=path.with_suffix('.json')
    rgba,extras,h=source(body);sig=dict(source_png_sha256=h,color=palette(extras)[color],reference=list(extras['paint_reference_color']),size=1024,recipe=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    old=json.loads(receipt.read_text()) if receipt.exists() else {}
    if path.exists() and old.get('inputs')==sig and old.get('output_sha256')==hashlib.sha256(path.read_bytes()).hexdigest():return path
    pixels,_=expected(body,color);scratch=Path('build/context-colors')/path.name;scratch.parent.mkdir(parents=True,exist_ok=True)
    write_png(scratch,pixels,bits=8);path.parent.mkdir(parents=True,exist_ok=True);data=scratch.read_bytes()
    if not path.exists() or path.read_bytes()!=data:path.write_bytes(data)
    scratch.unlink();receipt.write_text(json.dumps(dict(inputs=sig,output_sha256=hashlib.sha256(data).hexdigest()),indent=2));return path

def audit_exports():
    """Invert the documented native transfer on actual exported image bindings.

    The check compares linear delivery pixels minus coverage*factory_delta
    against filtered Atlantic source pixels. It does not call the generator's
    expected() function. Eroded unclipped regions avoid clamp/mip boundaries.
    """
    from PIL import ImageFilter
    import math
    checked={};rows=[]
    for seed in (101,202):
        export=Path(f'export/Traffic-{seed}.gltf');doc=json.loads(export.read_text())
        for mat in doc['materials']:
            color=mat.get('extras',{}).get('factory_color')
            if 'factory_metallic' in mat.get('extras',{}):
                assert abs(mat.get('pbrMetallicRoughness',{}).get('metallicFactor',1)-mat['extras']['factory_metallic'])<1e-5,(seed,mat['name'],'Factory metallic factor lost')
            if color not in COLORS:continue
            body=next(b for b in BODIES if b in mat['name']);index=mat['pbrMetallicRoughness']['baseColorTexture']['index']
            path=export.parent/doc['images'][doc['textures'][index]['source']]['uri'];key=(body,color,str(path.resolve()))
            if key in checked:continue
            checked[key]=True;rgba,extras,h=source(body);native=srgb_to_linear(rgba[:,:,:3]);alpha=rgba[:,:,3]
            delta=np.asarray(palette(extras)[color])-np.asarray(extras['paint_reference_color'])
            predicted=native+alpha[:,:,None]*delta
            valid=((predicted>.0005)&(predicted<.995)).all(axis=2)&(alpha>.2)
            radius=math.ceil(3*rgba.shape[1]/1024)+1
            mask=np.asarray(Image.fromarray(np.uint8(valid)*255).filter(ImageFilter.MinFilter(2*radius+1)).resize((1024,1024),Image.Resampling.NEAREST))>0
            if mask.sum()<32:
                rows.append(dict(body=body,color=color,unclipped_pixels=int(mask.sum()),scope='Too few unclipped interior pixels for inverse audit'));continue
            base=np.stack([np.asarray(Image.fromarray(native[:,:,i]).resize((1024,1024),Image.Resampling.LANCZOS)) for i in range(3)],axis=2)
            coverage=np.asarray(Image.fromarray(alpha).resize((1024,1024),Image.Resampling.LANCZOS))
            actual=srgb_to_linear(np.asarray(Image.open(path).convert('RGB'),np.float32)/255)
            # Lanczos can overshoot at an otherwise unclipped edge. Such a
            # destination pixel no longer has an invertible linear transfer.
            mask &= ((actual>.01)&(actual<.98)).all(axis=2)
            if mask.sum()<32:continue
            error=np.abs(actual-base-coverage[:,:,None]*delta)[mask]
            maximum=float(error.max());mean=float(error.mean());assert maximum<.0065 and mean<.002,(body,color,maximum,mean)
            rows.append(dict(body=body,color=color,unclipped_pixels=int(mask.sum()),max_linear_error=maximum,mean_linear_error=mean,source_png_sha256=h,exported_image=str(path)))
    assert all(any(r['body']==b and 'max_linear_error' in r for r in rows) for b in BODIES)
    Path('build/native-color-transfer.json').write_text(json.dumps(rows,indent=2));print('EXPORTED NATIVE COLOR TRANSFER PASSED',len(rows),flush=True)

def generate():
    rows=[]
    for body in BODIES:
        for color in COLORS:
            p=ensure(body,color);want,_=expected(body,color);actual=np.asarray(Image.open(p).convert('RGB'),np.float32)
            delta=np.abs(actual-np.round(want*255));maximum=float(delta.max());mean=float(delta.mean())
            assert maximum<=1 and mean<.02,(p,maximum,mean)
            rows.append(dict(file=str(p),source='original embedded native PNG, coverage delta in linear light',max_byte_error=maximum,mean_byte_error=mean,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
            # Attest the make recipe's validated inputs, not every model read.
            p.touch()
    Path('build/context-colors-audit.json').write_text(json.dumps(rows,indent=2));print('NATIVE COLOR DECODE PASSED',len(rows),'maps',flush=True)
if __name__=='__main__':generate()
