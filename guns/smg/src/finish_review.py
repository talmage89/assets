"""Shipping hero values, native crop and accepted geometry/layout invariants."""
from pathlib import Path
import json,math,hashlib,struct,sys,argparse
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.photo_match import project
from white_balance import stats

def signature(path):
    data=path.read_bytes();n=struct.unpack_from('<I',data,12)[0]
    gltf=json.loads(data[20:20+n]);binary=data[20+n+8:]
    images={im['bufferView'] for im in gltf['images']}
    # Blender recomputes and rounds tangents on export. The immutable-data
    # fingerprint concerns positions, normals, UVs, skin and animation data.
    tangents={gltf['accessors'][p['attributes']['TANGENT']]['bufferView']
              for m in gltf['meshes'] for p in m['primitives'] if 'TANGENT' in p['attributes']}
    chunks=[]
    for i,v in enumerate(gltf['bufferViews']):
        if i in images|tangents:continue
        chunk=binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
        chunks.append(chunk)
    structure={k:gltf[k] for k in ('nodes','skins','animations','meshes','accessors','scenes') if k in gltf}
    return dict(non_image_buffer_hash=hashlib.sha256(b''.join(chunks)).hexdigest(),
                structure_hash=hashlib.sha256(json.dumps(structure,sort_keys=True).encode()).hexdigest())

def camera(row):
    loc=np.array(row['location']);direction=np.array(row['target'])-loc
    return [math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),
            *loc,math.log(row['lens']),row.get('roll',0)]

def layout():
    accepted=json.loads((BASE/'src/accepted_layout.json').read_text())
    signatures={name:signature(BASE/'export'/(name+'.glb')) for name in accepted}
    assert signatures==accepted,'Accepted geometry, normals, UVs, rig, clips or delivery layout changed'
    return signatures

def heroes(beauty):
    beauty=Path(beauty);meta=json.loads((beauty/'shots.json').read_text())
    loci=json.loads((BASE/'build/value-loci.json').read_text());values={}
    for name,side in [('hero','left_photo'),('hero_right','right_photo')]:
        im=Image.open(beauty/(name+'.png')).convert('RGB');draw=ImageDraw.Draw(im)
        values[name]={}
        for key,row in loci[side].items():
            points=project(camera(meta[name]),np.array(row['points_m']),im.width,im.height)[0].tolist()
            values[name][key]=dict(stats(im,points),surface=row,render_polygon=points)
            draw.line(points+[points[0]],fill='lime' if key.startswith('polymer') else 'orange',width=1)
        im.save(beauty/(name+'-values.jpg'),quality=95)
    return values

def build():
    signatures=layout()
    out=BASE/'renders/final';meta=json.loads((out/'beauty/shots.json').read_text())
    values=heroes(out/'beauty')
    im=Image.open(out/'beauty/hero.png')
    corners=np.array([(x,y,z) for x in (-.027,.027) for y in (-.043,.220) for z in (-.110,.165)])
    pixels=project(camera(meta['hero']),corners,im.width,im.height)[0]
    lo=np.maximum(0,np.floor(pixels.min(0)).astype(int)-8)
    hi=np.minimum(im.size,np.ceil(pixels.max(0)).astype(int)+8)
    box=tuple(map(int,(*lo,*hi)))
    gray=Image.new('RGBA',im.size,(108,111,114,255));gray.alpha_composite(im.convert('RGBA'))
    gray.convert('RGB').save(out/'beauty/hero-gray.png')
    gray.convert('RGB').crop(box).save(out/'beauty/hero-receiver-magazine-native.png')
    result=dict(passed=True,hero_values=values,accepted_layout_signatures=signatures,
                native_crop=dict(source_size=list(im.size),rectangle=list(box),resized=False),
                scope='Actual triangle-ray patches projected into both hero views under the unchanged studio lights; display luma, not albedo.')
    (out/'finish-values.json').write_text(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--layout-only',action='store_true');parser.add_argument('--beauty');args=parser.parse_args()
    if args.layout_only:
        layout();print('Accepted position / normal / UV / weight / rig / clip / layout bytes: identical in all five exports; tangent data regenerated');sys.exit(0)
    row=dict(hero_values=heroes(args.beauty)) if args.beauty else build()
    print(json.dumps({name:{k:dict(luma=v['median_luma_255'],rgb=v['median_rgb_255']) for k,v in patches.items()}
                      for name,patches in row['hero_values'].items()},indent=2))
