"""Original stone plus five brick palettes in one 512 color/normal pair.

Full-width color bands retain horizontal repetition without chart seams.
Brick normals reuse the canonical Cape map through standard texture transforms;
stone normals retain the accepted full-resolution field. No older map changes.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from kit.image_io import read_png,write_png,srgb_to_linear,linear_to_srgb

REGIONS={'stone':(0,35,512,253),'coping':(0,3,512,29),
         '51':(0,264,512,296),'53':(0,312,512,344),
         '54':(0,360,512,392),'55':(0,408,512,440),'56':(0,456,512,488)}


def rect(name):return tuple(q/512 for q in REGIONS[str(name)])


def resized(a,w,h):
    return np.stack([np.asarray(Image.fromarray(a[:,:,i].astype('float32')).resize((w,h),Image.Resampling.BILINEAR)) for i in range(3)],2)


def author(folder):
    import bpy
    from kit.materials import Nodes
    from split_surfaces import brick_factor
    from cape_masonry import author as masonry
    from split_fields import stone
    folder=Path(folder);stone(folder/'stone');masonry(folder/'masonry')
    atlas_color=np.zeros((4096,4096,3))
    c=srgb_to_linear(read_png(folder/'stone/T_SplitStone_BaseColor.png'))
    atlas_color[2048:]=resized(c,4096,2048)
    normal=read_png(folder/'stone/T_SplitStone_Normal.png')*2-1
    normal=resized(normal,4096,4096);normal/=np.maximum(np.linalg.norm(normal,axis=2,keepdims=True),1e-8)
    bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=1;sc.render.bake.margin=0
    from kit import gpu
    gpu.enable();bpy.ops.mesh.primitive_plane_add(size=1);ob=bpy.context.object
    for seed in (51,53,54,55,56):
        node=Nodes('Split factory '+str(seed));uv=node.node('ShaderNodeTexCoord').outputs['UV'];u,v,_=node.split(uv)
        factor=brick_factor(node,dict(seed=seed),u,v)
        tex=node.node('ShaderNodeTexImage');tex.image=bpy.data.images.load(str((folder/'masonry/T_CapeBrick_BaseColor.png').resolve()),check_existing=True);tex.image.colorspace_settings.name='sRGB'
        base=node.vec('MULTIPLY',node.vec('MULTIPLY',tex.outputs['Color'],(.61,.464,.625)),factor)
        emit=node.node('ShaderNodeEmission');node.feed(emit.inputs['Color'],base);output=node.node('ShaderNodeOutputMaterial');node.feed(output.inputs['Surface'],emit.outputs[0])
        im=bpy.data.images.new('Factory color '+str(seed),width=1024,height=1024,float_buffer=True);im.colorspace_settings.name='Non-Color';target=node.node('ShaderNodeTexImage');target.image=im;node.nt.nodes.active=target
        ob.data.materials.clear();ob.data.materials.append(node.mat);bpy.ops.object.bake(type='EMIT')
        a=np.empty(1024*1024*4,dtype='float32');im.pixels.foreach_get(a);a=a.reshape(1024,1024,4)[::-1,:,:3]
        if seed==54:
            # The short shared repeat otherwise loses the accepted common
            # mix's dark fired-unit population through coarse color filtering.
            # Restore its factory spread; this uses no photographic pixels.
            y=a@np.array((.2126,.7152,.0722));target=np.maximum((y-.12)*1.60+.10,.001)
            a*=np.clip(target/np.maximum(y,1e-8),.35,1.25)[:,:,None]
            y=a@np.array((.2126,.7152,.0722));a*=1-.25*np.clip((.10-y)/.06,0,1)[:,:,None]
        # Vertical color filtering mixes neutral joints into the fired body.
        # Compensate its measured hue loss, retaining the original palettes.
        a*=np.array({51:(1.09,1.,.75),53:(1.03,.90,.74),54:(1.,1.,.80),55:(1.,1.,1.),56:(1.,1.,1.)}[seed])
        _,y0,_,y1=REGIONS[str(seed)];g=8*8;tile=resized(a,4096,(y1-y0)*8)
        padded=np.pad(tile,((g,g),(0,0),(0,0)),mode='wrap')
        atlas_color[(512-y1)*8-g:(512-y0)*8+g]=padded
    # Fill the remaining outer halo with its adjacent palette, never black.
    atlas_color[:128]=atlas_color[128:256]
    write_png(folder/'T_SplitStone_BaseColor.png',np.clip(linear_to_srgb(atlas_color),0,1))
    write_png(folder/'T_SplitStone_Normal.png',normal*.5+.5,bits=16)
    (folder/'atlas.json').write_text(json.dumps(dict(size=512,bake_size=4096,regions=REGIONS,gpu_mib=2/3,brick_guard_pixels=8,stone_color_guard_pixels=3,scope='Full-width original kiln color bands; full-resolution accepted stone normal; existing Cape brick normal via standard KHR_texture_transform'),indent=2))
