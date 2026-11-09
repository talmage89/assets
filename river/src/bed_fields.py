"""Original periodic packed alluvial gravel, with rounded crowns and silt seams."""
import numpy as np


def gravel(n=1024):
    rng=np.random.default_rng(716);count=38
    y,x=np.mgrid[:n,:n]/n*count;ix=np.floor(x).astype(int);iy=np.floor(y).astype(int)
    centers=rng.uniform(.12,.88,(count,count,2))
    aspect=rng.uniform(.74,1.28,(count,count,2))
    first=np.full((n,n),100.);identity=np.zeros((n,n),int)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            a=(iy+dy)%count;b=(ix+dx)%count
            q=((x-(ix+dx+centers[a,b,0]))/aspect[a,b,0])**2
            q+=((y-(iy+dy+centers[a,b,1]))/aspect[a,b,1])**2
            nearer=q<first
            identity=np.where(nearer,a*count+b,identity);first=np.minimum(first,q)
    # Rounded crowns stop short of each other's cell boundaries. Fines fill
    # those narrow interstices; no isolated clast silhouette painted on mud.
    rounded=np.clip((.57-np.sqrt(first))/.08,0,1)
    margin=rounded
    crown=np.maximum(0,1-first/.325)**.65
    hues=rng.uniform(.40,.62,count*count);brown=rng.uniform(-.03,.025,count*count)
    value=hues[identity];tint=brown[identity];grain=rng.random((n,n))-.5
    stone=np.stack((value+tint+.012,value,value-tint*.8-.018),axis=2)
    stone+=((crown-.5)*.025+grain*.025)[:,:,None]
    fines=grain*.035
    silt=np.empty_like(stone);silt[:]=(.355,.34,.305);silt+=fines[:,:,None]
    color=silt*(1-margin[:,:,None])+stone*margin[:,:,None]
    height=crown*(.0025+.0015*(value-.4)/.22)+grain*.0001
    occlusion=.59+.41*margin
    rough=.74+.17*(1-margin)+grain*.025
    return color,height,occlusion,rough
