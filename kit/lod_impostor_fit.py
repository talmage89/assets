"""Fit fixed crossed planes to an asset's own multi-view RGBA renders.

CPU-only deterministic least squares. Opacity is fitted jointly, so overlapping
planes represent one crown rather than four superimposed complete trees.
Colors fit premultiplied scene-linear radiance with actual plane depth order.
No photographs or external textures enter this fit.
"""
import numpy as np
from kit.image_io import srgb_to_linear,linear_to_srgb


def fit(frames,planes=4,size=64,iterations=160):
    """Equally spaced full-circle, square, straight-alpha sRGB input frames."""
    frames=np.asarray(frames,dtype=np.float64)/255
    count,height,width,channels=frames.shape
    if height!=width or height%size or channels!=4:raise ValueError('Expected equal square RGBA captures with integral fit scale')
    factor=height//size
    alpha=frames[:,:,:,3]
    premul=srgb_to_linear(frames[:,:,:,:3])*alpha[:,:,:,None]
    target_a=alpha.reshape(count,size,factor,size,factor).mean(axis=(2,4))
    target_c=premul.reshape(count,size,factor,size,factor,3).mean(axis=(2,4))
    picks=[round(i*count/(2*planes))%count for i in range(planes)]
    a=np.minimum(.95,1-(1-target_a[picks])**(1/2.4))
    c=target_c[picks]/np.maximum(target_a[picks,:,:,None],1e-6)
    prior=a.copy();models=[];yy=np.broadcast_to(np.arange(size)[:,None],(size,size))
    x=(np.arange(size)+.5)/size-.5
    for vi in range(count):
        maps=[];depths=[]
        for pi in range(planes):
            delta=vi*2*np.pi/count-pi*np.pi/planes;cos=np.cos(delta)
            coord=x/(cos if abs(cos)>1e-8 else 1e-8)+.5
            valid=(coord>=0)&(coord<=1)&(abs(cos)>1e-6)
            texel=coord*size-.5;left=np.floor(texel).astype(int);blend=np.clip(texel-left,0,1)
            left=np.clip(left,0,size-1);right=np.clip(left+1,0,size-1)
            maps.append((left,right,blend,valid));depths.append(x*np.tan(delta))
        order=np.argsort(-np.array(depths),axis=0)
        models.append((maps,order))
    def gather(array,mapping):
        left,right,t,valid=mapping
        if array.ndim==2:return (array[:,left]*(1-t)+array[:,right]*t)*valid
        return (array[:,left]*(1-t[None,:,None])+array[:,right]*t[None,:,None])*valid[None,:,None]
    def scatter(dest,value,mapping):
        left,right,t,valid=mapping
        if value.ndim==2:
            np.add.at(dest,(yy.ravel(),np.broadcast_to(left,(size,size)).ravel()),(value*(1-t)*valid).ravel())
            np.add.at(dest,(yy.ravel(),np.broadcast_to(right,(size,size)).ravel()),(value*t*valid).ravel())
        else:
            for ch in range(3):scatter(dest[:,:,ch],value[:,:,ch],mapping)
    def alpha_loss():
        return float(np.mean([np.mean((1-np.prod(1-np.array([gather(a[i],mp) for i,mp in enumerate(maps)]),axis=0)-target_a[vi])**2) for vi,(maps,order) in enumerate(models)]))
    initial=alpha_loss();mom=np.zeros_like(a);variance=np.zeros_like(a)
    for step in range(1,iterations+1):
        grad=np.zeros_like(a)
        for vi,(maps,order) in enumerate(models):
            aa=np.array([gather(a[i],mp) for i,mp in enumerate(maps)])
            error=1-np.prod(1-aa,axis=0)-target_a[vi]
            for pi,mp in enumerate(maps):scatter(grad[pi],error*np.prod(1-np.delete(aa,pi,axis=0),axis=0),mp)
        grad/=count;grad+=.0002*(a-prior)
        mom=.9*mom+.1*grad;variance=.999*variance+.001*grad*grad
        a-=.02*(mom/(1-.9**step))/(np.sqrt(variance/(1-.999**step))+1e-8)
        a=np.clip(a,0,.9999)
    final=alpha_loss();mom=np.zeros_like(c);variance=np.zeros_like(c)
    weights=[]
    for vi,(maps,order) in enumerate(models):
        aa=np.array([gather(a[i],mp) for i,mp in enumerate(maps)])
        trans=np.ones((size,size));ww=np.zeros_like(aa)
        for rank in range(planes):
            ids=order[rank];al=np.take_along_axis(aa,np.broadcast_to(ids,(1,size,size)),axis=0)[0]
            for pi in range(planes):ww[pi]+=trans*al*(ids==pi)[None,:]
            trans*=1-al
        weights.append(ww)
    color_initial=None;color_final=None
    for step in range(1,iterations+1):
        grad=np.zeros_like(c);loss=0.
        for vi,(maps,order) in enumerate(models):
            ww=weights[vi];render=sum(gather(c[i],mp)*ww[i,:,:,None] for i,mp in enumerate(maps))
            error=render-target_c[vi];loss+=float(np.mean(error*error))
            for pi,mp in enumerate(maps):scatter(grad[pi],error*ww[pi,:,:,None],mp)
        if step==1:color_initial=loss/count
        color_final=loss/count
        grad/=count;mom=.9*mom+.1*grad;variance=.999*variance+.001*grad*grad
        c-=.008*(mom/(1-.9**step))/(np.sqrt(variance/(1-.999**step))+1e-8);c=np.clip(c,0,1)
    rgba=np.concatenate([linear_to_srgb(c),a[:,:,:,None]],axis=3)
    return np.uint8(np.clip(rgba*255+.5,0,255)),dict(planes=planes,fit_size=size,training_views=count,iterations=iterations,
          alpha_mse_before=initial,alpha_mse_after=final,premultiplied_linear_rgb_mse_before=color_initial,premultiplied_linear_rgb_mse_after=color_final)
