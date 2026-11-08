"""Thirty-two-view cylindrical billboard rendered exclusively from delivered glTF.

Unlit prelit RGBA, frozen wind; the runtime rotates the quad toward the camera
and selects the nearest atlas sector. Extras document that explicit controller.
No source geometry, procedural asset shader or reference image is loaded.
"""
import argparse
import copy
import json
import math
import os
import sys
from pathlib import Path

import bpy
import numpy as np
from PIL import Image
from mathutils import Matrix,Vector

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit.lod_io import Document,digest
from kit.lod_render import setup


def build(source,out,crossed=False):
    source=Path(source).resolve();out=Path(out).resolve();dest=out.parent/('crossed' if crossed else 'impostor')
    dest.mkdir(parents=True,exist_ok=True);base=Document(source);bounds=base.bounds()
    lo,hi=bounds;center=(lo+hi)*.5;extent=float(hi[1]-lo[1])*1.04
    sectors,columns,rows=(4,4,1) if crossed else (32,8,4)
    atlas=Image.new('RGBA',(columns*256,rows*256))
    captures=out.parent/'impostor-captures';captures.mkdir(parents=True,exist_ok=True)
    receipt=captures/'capture.json'
    recipe=dict(source_dependencies=base.dependencies(),renderer_sha256=digest(ROOT/'kit/lod_render.py'),
                capture_sha256=digest(Path(__file__)),size=256,samples=32,views=32)
    old=json.loads(receipt.read_text()) if receipt.exists() else {}
    valid=old.get('recipe')==recipe and all((captures/f'sector-{i}.png').exists() and digest(captures/f'sector-{i}.png')==old.get('files',{}).get(str(i)) for i in range(32))
    frames=[]
    from kit.detachable_textures import _pull_push
    from kit.image_io import srgb_to_linear,linear_to_srgb
    for i in range(32):
        path=captures/f'sector-{i}.png'
        if not valid:
            sc=setup(source,bounds,i*360/32,extent*3,size=(256,256),foliage=True)
            sc.camera.data.type='ORTHO';sc.camera.data.ortho_scale=extent
            sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.cycles.samples=32
            sc.render.filepath=str(path);bpy.ops.render.render(write_still=True)
            rgba=np.asarray(Image.open(path).convert('RGBA')).astype(np.float32)/255
            rgba[:,:,:3]=linear_to_srgb(_pull_push(srgb_to_linear(rgba[:,:,:3]),rgba[:,:,3]>0))
            Image.fromarray(np.uint8(np.clip(rgba*255+.5,0,255))).save(path)
        frames.append(np.asarray(Image.open(path).convert('RGBA')))
    receipt.write_text(json.dumps(dict(recipe=recipe,files={str(i):digest(captures/f'sector-{i}.png') for i in range(32)}),indent=2)+'\n')
    if crossed:
        from kit.lod_impostor_fit import fit
        fitted,report=fit(frames)
        for i,pixels in enumerate(fitted):
            rgba=pixels.astype(np.float32)/255
            rgba[:,:,:3]=linear_to_srgb(_pull_push(srgb_to_linear(rgba[:,:,:3]),rgba[:,:,3]>0))
            frame=Image.fromarray(np.uint8(np.clip(rgba*255+.5,0,255))).resize((256,256),Image.Resampling.BILINEAR)
            atlas.paste(frame,(i*256,0))
        (dest/'fit.json').write_text(json.dumps(report,indent=2)+'\n')
    else:
        for i,pixels in enumerate(frames):atlas.paste(Image.fromarray(pixels),(i%columns*256,i//columns*256))
    texture=dest/'billboard.png';atlas.save(texture)
    doc=Document(source)
    nodes=copy.deepcopy(base.data['nodes'])
    for n in nodes:n.pop('mesh',None)
    node=dict(name='LOD_Billboard',mesh=0,extras=dict(lod_billboard=not crossed,lod_crossed=crossed,sectors=sectors,columns=columns,rows=rows,
               rotation_axis='glTF +Y',sector_degrees=360/sectors,wind='frozen',lighting='prelit procedural daylight'))
    nodes.append(node)
    scenes=copy.deepcopy(base.data['scenes'])
    scenes[base.data.get('scene',0)].setdefault('nodes',[]).append(len(nodes)-1)
    doc.data=dict(asset=copy.deepcopy(base.data['asset']),scene=base.data.get('scene',0),scenes=scenes,nodes=nodes,
       meshes=[dict(name='LOD_Billboard',primitives=[dict(attributes={},indices=0,material=0)])],
       accessors=[],bufferViews=[],buffers=[],
       materials=[dict(name='LOD_Billboard_Prelit',doubleSided=True,alphaMode='BLEND',
          pbrMetallicRoughness=dict(baseColorTexture=dict(index=0),metallicFactor=0,roughnessFactor=1),
          extensions={'KHR_materials_unlit':{}},extras=copy.deepcopy(node['extras']))],
       images=[dict(name='LOD_Billboard',uri=os.path.relpath(texture,source.parent))],
       textures=[dict(source=0,sampler=0)],samplers=[dict(magFilter=9729,minFilter=9987,wrapS=33071,wrapT=33071)],
       extensionsUsed=['KHR_materials_unlit'])
    half=extent/2;x,y,z=center
    attrs=dict(POSITION=np.array([[x-half,y-half,z],[x+half,y-half,z],[x+half,y+half,z],[x-half,y+half,z]],np.float32),
               NORMAL=np.array([[0,0,1]]*4,np.float32),
               TEXCOORD_0=np.array([[0,1/rows],[1/columns,1/rows],[1/columns,0],[0,0]],np.float32),
               _WIND=np.zeros((4,4),np.float32))
    if crossed:
        positions=[];normals=[];uvs=[];faces=[]
        for i in range(sectors):
            theta=math.pi*i/sectors;direction=np.array([math.cos(theta),0,-math.sin(theta)])
            up=np.array([0,half,0]);side=direction*half;c=np.array(center)
            positions.extend([c-side-up,c+side-up,c+side+up,c-side+up])
            normals.extend([[math.sin(theta),0,math.cos(theta)]]*4)
            uvs.extend([[i/columns,1],[(i+1)/columns,1],[(i+1)/columns,0],[i/columns,0]])
            faces.extend([[4*i,4*i+1,4*i+2],[4*i,4*i+2,4*i+3]])
        attrs=dict(POSITION=np.array(positions,np.float32),NORMAL=np.array(normals,np.float32),TEXCOORD_0=np.array(uvs,np.float32),_WIND=np.zeros((len(positions),4),np.float32))
        faces=np.array(faces,np.uint32)
    else:faces=np.array([[0,1,2],[0,2,3]],np.uint32)
    doc.replace(doc.data['meshes'][0]['primitives'][0],attrs,faces)
    doc.save(out)
    print('LOD IMPOSTOR',out,len(faces),'triangles /',atlas.size,'RGBA /',sectors,'sectors')
    if crossed:build(source,out.with_name(out.stem+'_CameraFacing.gltf'),False)


def pose(azimuth):
    """Reference controller for comparison renders; port to the target engine."""
    for ob in bpy.context.scene.objects:
        if not ob.get('lod_billboard'):continue
        bpy.context.view_layer.update()
        uv=ob.data.uv_layers.active
        if '_lod_pose_matrix' not in ob:
            ob['_lod_pose_matrix']=np.array(ob.matrix_world).ravel().tolist()
            ob['_lod_pose_uv']=np.array([v.uv[:] for v in uv.data]).ravel().tolist()
        base=Matrix(np.array(ob['_lod_pose_matrix']).reshape(4,4).tolist())
        positions=np.array([v.co[:] for v in ob.data.vertices]);center=(positions.min(axis=0)+positions.max(axis=0))*.5
        pivot=base@Vector(center)
        ob.matrix_world=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(azimuth),4,'Z')@Matrix.Translation(-pivot)@base
        sectors,cols,rows=ob['sectors'],ob['columns'],ob['rows']
        sector=int(math.floor((azimuth%360)/(360/sectors)+.5))%sectors
        col,row=sector%cols,sector//cols
        # Absolute pose/UV assignment: repeated runtime calls must not drift.
        rest=np.array(ob['_lod_pose_uv']).reshape(-1,2)
        for i,item in enumerate(uv.data):item.uv=(rest[i,0]+col/cols,rest[i,1]-row/rows)



if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--crossed',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);build(a.source,a.out,a.crossed)
