"""Original Cape-only masonry fields; constant ORM values free their memory.

The 256-square tiles retain the existing family's brick/concrete texel density.
No photographs or existing image pixels enter their generation.
"""
from pathlib import Path
import json
import numpy as np
from textures import noise,fields
from kit.image_io import write_png,linear_to_srgb

COVERAGE={'CapeBrick':(.6096,.2032/3*8),'CapeConcrete':(1.2192,1.2192)}
ROUGHNESS={'CapeBrick':.91,'CapeConcrete':.89,'CapeCedar':219/255,'CapeCement':235/255}


def author(folder,n=512):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);rng=np.random.default_rng(61478)
    for name,(sx,sy) in COVERAGE.items():
        yy,xx=np.mgrid[:n,:n];x=(xx+.5)/n*sx;y=(n-.5-yy)/n*sy
        fine=noise(n,128,rng);mid=noise(n,48,rng)
        if name=='CapeBrick':
            cw=.2032;ch=cw/3
            # Millimeter-scale waviness and unit-specific bed/head joint widths.
            warped_y=y+.00085*np.sin(x/sx*2*np.pi*7)+.00035*np.sin(x/sx*2*np.pi*19)
            row=np.floor(warped_y/ch).astype(int)%8;local_y=np.mod(warped_y,ch)
            warped_x=x+(row%2)*cw/2+.00070*np.sin(y/sy*2*np.pi*13)
            col=np.floor(warped_x/cw).astype(int)%3;local_x=np.mod(warped_x,cw)
            widths=rng.uniform(.0023,.0038,(8,3))[row,col]
            edge=np.minimum.reduce((local_x,cw-local_x,local_y,ch-local_y))
            mask=np.clip((edge-widths)/.0018,0,1);mask=mask*mask*(3-2*mask)
            tone=rng.uniform(.60,1.40,(8,3))[row,col]
            flashed=rng.random((8,3))[row,col]<.15
            tone*=1-.23*flashed*np.exp(-local_x/.045)
            chroma=rng.uniform(.94,1.06,(8,3,3))[row,col]
            body=np.array((.29,.205,.135))/.72*(tone*(.92+.16*mid))[:,:,None]*chroma
            # Compensate the unchanged whole-brick palette factor so mortar
            # remains neutral after its tint, rather than turning slate blue.
            mortar=np.array((.22/.61,.22/.464,.22/.625))*(.96+.08*mid)[:,:,None]
            color=body*mask[:,:,None]+mortar*(1-mask[:,:,None])
            height=.0018*mask+.00065*(mid-.5)*mask+.00020*(fine-.5)
        else:
            color,height,_,_,_=fields('Concrete',n,sx)
            # Form bugholes and exposed aggregate are manufacturing features.
            # Their scale survives filtering; broad weather remains causal C0.
            color*=((.70+.60*fine)[:,:,None])
            for i in range(145):
                px,py=rng.uniform(0,sx,2);radius=rng.uniform(.0018,.0060)
                dx=np.minimum(abs(x-px),sx-abs(x-px));dy=np.minimum(abs(y-py),sy-abs(y-py))
                pit=np.exp(-(dx*dx+dy*dy)/(radius*radius))
                height-=rng.uniform(.0005,.0017)*pit;color*=1-rng.uniform(.12,.35)*pit[:,:,None]
            height+=.00050*(fine-.5)
            # Groundwater salts precipitate low, broken by the pore field;
            # the concrete UV datum is world Z + 304.8 mm.
            height_above_grade=y-.3048
            salts=np.clip((.25-height_above_grade)/.16,0,1)*np.clip((height_above_grade-.012)/.06,0,1)*np.clip((mid-.52)/.20,0,1)*.18
            color=color*(1-salts[:,:,None])+np.array((.49,.49,.47))*salts[:,:,None]
        dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(2*sx/n)
        dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(2*sy/n)
        normal=np.stack((-dx,dy,np.ones_like(height)),2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
        write_png(folder/f'T_{name}_BaseColor.png',np.clip(linear_to_srgb(color),0,1))
        write_png(folder/f'T_{name}_Normal.png',normal*.5+.5,bits=16)
    (folder/'masonry.json').write_text(json.dumps(dict(native=n,coverage_m=COVERAGE,roughness=ROUGHNESS,brick_recess_m=.0018,concrete_bugholes=145),indent=2))


def dielectric(name,folder,roughness=None):
    """Use the kit material, then replace its constant ORM by authored scalars.

    The temporary one-pixel input exists only to use the established builder;
    its node and AO group are removed and it is never a delivered image.
    """
    import bpy
    from kit import tiling
    folder=Path(folder);roughness=ROUGHNESS[name] if roughness is None else roughness
    write_png(folder/f'T_{name}_ORM.png',np.array([[[1.,roughness,0.]]]))
    mat=tiling.material(name,folder,tint=True);nt=mat.node_tree;p=nt.nodes.get('Principled BSDF')
    for key,value in (('Roughness',roughness),('Metallic',0.)):
        for link in list(p.inputs[key].links):nt.links.remove(link)
        p.inputs[key].default_value=value
    for node in list(nt.nodes):
        if node.type=='GROUP' and node.node_tree.name=='glTF Material Output' or node.type=='TEX_IMAGE' and node.image and '_ORM' in node.image.name or node.type=='SEPARATE_COLOR':nt.nodes.remove(node)
    return mat
