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
from mathutils import Matrix

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit.lod_io import Document
from kit.lod_render import setup


def build(source,out):
    source=Path(source).resolve();out=Path(out).resolve();dest=out.parent/'impostor'
    dest.mkdir(parents=True,exist_ok=True);base=Document(source);bounds=base.bounds()
    lo,hi=bounds;center=(lo+hi)*.5;extent=float(hi[1]-lo[1])*1.04
    sectors,columns,rows=32,8,4
    atlas=Image.new('RGBA',(columns*256,rows*256))
    for i in range(sectors):
        sc=setup(source,bounds,i*360/sectors,extent*3,size=(256,256),foliage=True)
        sc.camera.data.type='ORTHO';sc.camera.data.ortho_scale=extent
        # Bake scene-linear radiance encoded as sRGB, avoiding a second AgX
        # transform when the shipped unlit billboard is finally displayed.
        sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
        sc.cycles.samples=32
        path=dest/f'sector-{i}.png';sc.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        frame=Image.open(path).convert('RGBA')
        # Fill transparent RGB from the tree's own rendered colors before
        # ordinary straight-alpha mip filtering; retain alpha exactly.
        rgba=np.asarray(frame).astype(np.float32)/255
        from kit.detachable_textures import _pull_push
        from kit.image_io import srgb_to_linear,linear_to_srgb
        mask=rgba[:,:,3]>0
        rgba[:,:,:3]=linear_to_srgb(_pull_push(srgb_to_linear(rgba[:,:,:3]),mask))
        frame=Image.fromarray(np.uint8(np.clip(rgba*255+.5,0,255)))
        atlas.paste(frame,(i%columns*256,i//columns*256))
    texture=dest/'billboard.png';atlas.save(texture)
    doc=Document(source)
    nodes=copy.deepcopy(base.data['nodes'])
    for n in nodes:n.pop('mesh',None)
    node=dict(name='LOD_Billboard',mesh=0,extras=dict(lod_billboard=True,sectors=sectors,columns=columns,rows=rows,
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
    doc.replace(doc.data['meshes'][0]['primitives'][0],attrs,np.array([[0,1,2],[0,2,3]],np.uint32))
    doc.save(out)
    print('LOD IMPOSTOR',out,'2 triangles /',atlas.size,'RGBA /',sectors,'sectors')


def pose(azimuth):
    """Reference controller for comparison renders; port to the target engine."""
    for ob in bpy.context.scene.objects:
        if not ob.get('lod_billboard'):continue
        bpy.context.view_layer.update()
        ob.matrix_world=Matrix.Rotation(math.radians(azimuth),4,'Z')@ob.matrix_world
        sectors,cols,rows=ob['sectors'],ob['columns'],ob['rows']
        sector=int(math.floor((azimuth%360)/(360/sectors)+.5))%sectors
        col,row=sector%cols,sector//cols
        # Blender UV is bottom-up; raw glTF atlas UV is top-down.
        uv=ob.data.uv_layers.active
        for item in uv.data:
            item.uv.x+=col/cols;item.uv.y-=row/rows


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);build(a.source,a.out)
