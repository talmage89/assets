"""Original periodic fieldstone; photographs never enter this module.

One 512 BaseColor/Normal pair, scalar dielectric response: 2/3 MiB with
8-bpp blocks and full mip chains. This is the only planned shared addition.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from kit.image_io import write_png,linear_to_srgb
from textures import noise

COVERAGE=1.3716


def stone(folder,n=512):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(72519)
    yy,xx=np.mgrid[:n,:n];v=(n-.5-yy)/n
    x=(xx+.5)/n*COVERAGE
    y=v*COVERAGE
    geology=np.random.default_rng(40891)
    # Centimeter-scale broken edges and fractured faces are mineral structure,
    # not a weather/noise wash. Separate RNG preserves the stone palette.
    x=x+.028*(noise(n,18,geology)-.5)
    y=y+.028*(noise(n,19,geology)-.5)
    # Periodic jittered sites give polygonal field stones, not circular blobs.
    sites=np.array([((i+rng.uniform(.10,.90))/4*COVERAGE,
                     (j+rng.uniform(.10,.90))/5*COVERAGE) for j in range(5) for i in range(4)])
    candidates=[]
    for oy in (-1,0,1):
        for ox in (-1,0,1):
            for index,p in enumerate(sites):
                q=p+np.array((ox,oy))*COVERAGE
                candidates.append((q,index))
    distance=np.full((n,n),np.inf);nearest=np.zeros((n,n),dtype=int);cx=np.zeros((n,n));cy=cx.copy()
    for q,index in candidates:
        d=(x-q[0])**2+((y-q[1])*1.15)**2;keep=d<distance
        distance[keep]=d[keep];nearest[keep]=index;cx[keep]=q[0];cy[keep]=q[1]
    edge=np.full((n,n),np.inf)
    for q,index in candidates:
        dx=q[0]-cx;dy=(q[1]-cy)*1.15;length=np.sqrt(dx*dx+dy*dy)
        d=(x-q[0])**2+((y-q[1])*1.15)**2
        bisector=(d-distance)/np.maximum(2*length,1e-6)
        edge=np.minimum(edge,np.where(length>.001,bisector,np.inf))
    fine=noise(n,144,rng);mid=noise(n,48,rng)
    edge+=.0018*(mid-.5)
    body=np.clip((edge-.0075)/.005,0,1);body=body*body*(3-2*body)
    tones=np.array(((.25,.245,.205),(.33,.315,.26),(.20,.205,.18),(.38,.35,.28),(.29,.27,.225)))
    units=tones[rng.integers(0,len(tones),len(sites))]
    unit=units[nearest]*(rng.uniform(.68,1.30,len(sites))[nearest]*(.89+.22*mid))[:,:,None]
    mortar=np.array((.19,.185,.158))*(.94+.12*fine)[:,:,None]
    color=(unit*body[:,:,None]+mortar*(1-body[:,:,None]))*np.array((1.20,1.0,.85))
    slopes=rng.uniform(-.035,.035,(len(sites),2))
    facet=slopes[nearest,0]*(x-cx)+slopes[nearest,1]*(y-cy)
    # Intersect shallow cleavage planes inside each individual stone. Broad
    # interpolated height noise makes pillow-like lumps instead of rock.
    cuts=geology.uniform(-.065,.065,(len(sites),4,2));offsets=geology.uniform(0,.012,(len(sites),4))
    fracture=np.full((n,n),np.inf)
    for k in range(4):
        plane=offsets[nearest,k]+cuts[nearest,k,0]*(x-cx)+cuts[nearest,k,1]*(y-cy)
        fracture=np.minimum(fracture,plane)
    fracture-=offsets.min(axis=1)[nearest]
    cleavage=noise(n,67,geology)
    height=body*np.clip(.018+facet+.65*fracture+.0012*(cleavage-.5),.005,.040)+.00030*(fine-.5)
    # The original rowlock/coping brick occupies a small guarded strip in
    # the same pair. Stone walls and their brick cap remain one material.
    brick_height=round(n*52/512);stone_height=round(n*436/512);guard=round(n*6/512)
    by,bx=np.mgrid[:brick_height,:n];bu=(bx+.5)/n*.6096;bv=(brick_height-.5-by)/brick_height*(.2032/3)
    rowx=np.mod(bu,.2032);edgebrick=np.minimum.reduce((rowx,.2032-rowx,bv,.2032/3-bv))
    face=np.clip((edgebrick-.003)/.0015,0,1)
    col=np.floor(bu/.2032).astype(int)%3;tones=rng.uniform(.75,1.25,3)[col]
    brick_fine=noise(n,144,geology)[:brick_height]
    brickbody=np.array((.22,.125,.085))*(tones*(.94+.12*brick_fine))[:,:,None]
    brickcolor=brickbody*face[:,:,None]+np.array((.22,.22,.22))*(1-face[:,:,None])
    brickrelief=.002*face+.00018*(brick_fine-.5)
    def resize(a,h):
        if a.ndim==3:return np.stack([resize(a[:,:,i],h) for i in range(a.shape[2])],2)
        return np.asarray(Image.fromarray(a.astype('float32')).resize((n,h),Image.Resampling.BILINEAR))
    color=resize(color,stone_height);height=resize(height,stone_height)
    def normals(a,width,depth):
        dx=(np.roll(a,-1,1)-np.roll(a,1,1))/(2*width/a.shape[1]);dy=(np.roll(a,-1,0)-np.roll(a,1,0))/(2*depth/a.shape[0])
        result=np.stack((-dx,dy,np.ones_like(a)),2);return result/np.linalg.norm(result,axis=2,keepdims=True)
    def pack(wall,cap):
        result=np.zeros((n,n,3));start=guard;stop=start+stone_height
        result[start:stop]=wall;result[:start]=wall[-guard:];result[stop:stop+guard]=wall[:guard]
        first=stop+2*guard;last=first+brick_height
        result[first:last]=cap;result[first-guard:first]=cap[-guard:];result[last:]=cap[:guard]
        return result
    normal=pack(normals(height,COVERAGE,COVERAGE),normals(brickrelief,.6096,.2032/3))
    write_png(folder/'T_SplitStone_BaseColor.png',np.clip(linear_to_srgb(pack(color,brickcolor)),0,1))
    write_png(folder/'T_SplitStone_Normal.png',normal*.5+.5,bits=16)
    (folder/'stone.json').write_text(json.dumps(dict(coverage_m=COVERAGE,native=n,stones_per_repeat=len(sites),joint_width_m=.015,recess_m=.018,roughness=.91,stone_v=(70/512,506/512),coping_v=(6/512,58/512),guard_px=6,planned_shared_addition_mib=2/3),indent=2))


def stone_material(folder):
    import bpy
    from kit.materials import Nodes
    stone(folder);n=Nodes('SplitStone');uv=n.node('ShaderNodeTexCoord').outputs['UV']
    u,v,_=n.split(uv);coping=n.node('ShaderNodeAttribute',attribute_name='SplitCoping').outputs['Fac']
    wall_v=n.add(70/512,n.mul(n.math('FRACT',v),436/512));cap_v=n.add(6/512,n.mul(v,52/512))
    uv=n.combine(u,n.mix(coping,wall_v,cap_v),0)
    images={}
    for channel in ('BaseColor','Normal'):
        path=Path(folder)/('T_SplitStone_'+channel+'.png')
        im=bpy.data.images.load(str(path.resolve()),check_existing=True)
        im.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
        tex=n.node('ShaderNodeTexImage');tex.image=im;n.feed(tex.inputs['Vector'],uv);images[channel]=tex.outputs['Color']
    p=n.nt.nodes.get('Principled BSDF')
    if p is None:
        p=n.node('ShaderNodeBsdfPrincipled',name='Principled BSDF')
        output=n.node('ShaderNodeOutputMaterial',name='OUT');n.feed(output.inputs['Surface'],p.outputs[0])
    tint=n.node('ShaderNodeVertexColor',layer_name='Tint').outputs['Color']
    n.feed(p.inputs['Base Color'],n.vec('MULTIPLY',images['BaseColor'],tint))
    p.inputs['Roughness'].default_value=.91
    normal=n.node('ShaderNodeNormalMap');n.feed(normal.inputs['Color'],images['Normal']);normal.inputs['Strength'].default_value=.85;n.feed(p.inputs['Normal'],normal.outputs[0])
    return n.mat
