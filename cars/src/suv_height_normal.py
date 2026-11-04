"""Meter-height atlas to OpenGL tangent normals using measured UV Jacobians.

Frozen rest-coordinate attributes preserve colors through joining, but Cycles
can drop their screen differentials in a normal bake. Emitted height samples
remain correct. Differentiate those at bake resolution, in physical meters,
within each connected UV chart. The shipped mesh already carries body curvature.
"""
import math
import numpy as np
from PIL import Image,ImageDraw
from mathutils import Vector
from kit.uv import islands


def derive(ob,height,strength=.65,padding=12,sample_valid=None):
    size=height.shape[0];me=ob.data;me.calc_loop_triangles();uv=me.uv_layers['BakeUV']
    ids=Image.new('I',(size,size),0);draw=ImageDraw.Draw(ids);metrics=[[0,0,0,0]];charts=[0]
    owners={li:j+1 for j,loops in enumerate(islands(ob)) for li in loops}
    nm=ob.matrix_world.to_3x3().inverted().transposed()
    for t in me.loop_triangles:
        xy=np.array([(uv.data[i].uv.x*size,(1-uv.data[i].uv.y)*size) for i in t.loops])
        ps=[ob.matrix_world@me.vertices[i].co for i in t.vertices]
        uv_delta=np.stack([xy[1]-xy[0],xy[2]-xy[0]])
        if abs(np.linalg.det(uv_delta))<1e-12:raise ValueError('Degenerate height chart')
        dp=np.linalg.solve(uv_delta,np.array([tuple(ps[1]-ps[0]),tuple(ps[2]-ps[0])]))
        n=sum((nm@me.corner_normals[i].vector for i in t.loops),Vector()).normalized()
        dx,dy=map(Vector,dp);tangent=(dx-n*dx.dot(n)).normalized()
        sign=1 if tangent.cross(-dy).dot(n)>=0 else -1
        bitangent=n.cross(tangent).normalized()*sign
        matrix=np.array([[dx.dot(tangent),dx.dot(bitangent)],[dy.dot(tangent),dy.dot(bitangent)]])
        if abs(np.linalg.det(matrix))<1e-18:raise ValueError('Singular physical UV Jacobian')
        metrics.append(np.linalg.inv(matrix).reshape(-1));charts.append(owners[t.loops[0]])
        draw.polygon([tuple(p) for p in xy],fill=len(metrics)-1)
    ids=np.asarray(ids,dtype=np.int32);metrics=np.asarray(metrics,dtype=np.float32);charts=np.asarray(charts,dtype=np.int32)[ids]
    valid_height=(ids>0) if sample_valid is None else (ids>0)&sample_valid
    # A missing chart neighbor uses a one-sided difference. A different atlas
    # island is never mistaken for a neighboring point on the physical sheet.
    def derivative(axis):
        left=np.roll(height,1,axis);right=np.roll(height,-1,axis)
        same_l=(charts==np.roll(charts,1,axis))&valid_height&np.roll(valid_height,1,axis)
        same_r=(charts==np.roll(charts,-1,axis))&valid_height&np.roll(valid_height,-1,axis)
        if axis==0:same_l[0]=False;same_r[-1]=False
        else:same_l[:,0]=False;same_r[:,-1]=False
        return np.where(same_l&same_r,(right-left)*.5,np.where(same_r,right-height,np.where(same_l,height-left,0)))
    hx=derivative(1);hy=derivative(0);normal=np.zeros((*height.shape,3),np.float32);normal[:,:,2]=1
    minimum_z=1
    for start in range(0,size,128):
        sl=slice(start,min(size,start+128));m=metrics[ids[sl]]
        gx=m[:,:,0]*hx[sl]+m[:,:,1]*hy[sl];gy=m[:,:,2]*hx[sl]+m[:,:,3]*hy[sl]
        v=np.stack([-strength*gx,-strength*gy,np.ones_like(gx)],axis=2);v/=np.linalg.norm(v,axis=2,keepdims=True)
        normal[sl]=v;minimum_z=min(minimum_z,float(v[:,:,2].min()))
    valid=ids>0
    # Extend only into empty gutters; existing islands never change. Average
    # competing margins as the ordinary filtered atlas does, then renormalize.
    for _ in range(padding):
        total=np.zeros_like(normal);count=np.zeros(height.shape,np.uint8)
        for axis in [0,1]:
            for shift in [-1,1]:
                mask=np.roll(valid,shift,axis);values=np.roll(normal,shift,axis)
                if axis==0:mask[0 if shift==1 else -1]=False
                else:mask[:,0 if shift==1 else -1]=False
                total+=values*mask[:,:,None];count+=mask
        fill=(~valid)&(count>0)
        v=total[fill];v/=np.maximum(np.linalg.norm(v,axis=1,keepdims=True),1e-12)
        normal[fill]=v;valid[fill]=True
    return normal*.5+.5,dict(method='Finite differences of emitted meter height within UV charts, measured physical tangent Jacobians',charts=int(charts.max()),height_min_max_m=[float(height[valid_height].min()),float(height[valid_height].max())],raster_border_pixels_without_bake_sample=int(((ids>0)&~valid_height).sum()),minimum_tangent_z=minimum_z,strength=strength,padding_pixels=padding)
