"""Independent crown measurements from retained alpha texels and source meshes."""
import math
import numpy as np
from PIL import Image


def hull(points):
    points=sorted(set(points))
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower=[]
    for p in points:
        while len(lower)>1 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
        lower.append(p)
    upper=[]
    for p in reversed(points):
        while len(upper)>1 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]


def retained_bounds(ob,image,rects):
    """Pixel-center support hulls, transformed onto every actual branchlet card.

    Convexification is exact for axis-extreme support of a planar card. It does
    not fill the holes for rendering or turn pixel hulls into model geometry.
    """
    alpha=np.asarray(Image.open(image).convert('RGBA'))[:,:,3];H,W=alpha.shape
    supports=[]
    for u0,v0,u1,v1 in rects:
        x0=math.floor(u0*W);x1=math.ceil(u1*W);y0=math.floor((1-v1)*H);y1=math.ceil((1-v0)*H)
        patch=alpha[y0:y1,x0:x1];edges=[]
        for j,row in enumerate(patch):
            xs=np.flatnonzero(row>127)
            if len(xs):
                for k in (xs[0],xs[-1]):
                    edges.append((((x0+k+.5)/W-u0)/(u1-u0),(1-(y0+j+.5)/H-v0)/(v1-v0)))
        supports.append(np.array(hull(edges)))
    lo=np.full(3,np.inf);hi=-lo;uv=ob.data.uv_layers.active
    for face in ob.data.polygons:
        pts=np.array([ob.matrix_world@ob.data.vertices[i].co for i in face.vertices])
        uv0=np.array(uv.data[face.loop_start].uv)
        k=min(range(len(rects)),key=lambda i:np.linalg.norm(uv0-np.array(rects[i][:2])))
        q=supports[k];p=pts[0]+q[:,0,None]*(pts[1]-pts[0])+q[:,1,None]*(pts[3]-pts[0])
        lo=np.minimum(lo,p.min(axis=0));hi=np.maximum(hi,p.max(axis=0))
    size=hi-lo
    return dict(min=lo.tolist(),max=hi.tolist(),size=size.tolist(),width_height_x=float(size[0]/size[2]),
                width_height_y=float(size[1]/size[2]),base_m=float(lo[2]),
                scope='Retained alpha pixel centers on actual planar card surfaces; glancing view fade excluded')


def projected_image(path):
    im=np.array(Image.open(path).convert('RGBA'))
    # Transparent photo-match render: reject sky without using green/brightness
    # as a geometry mask. Dark foliage still contributes to the silhouette.
    foreground=im[:,:,3]>127
    green=(im[:,:,1]>im[:,:,0]*1.10)&(im[:,:,1]>im[:,:,2]*1.08)&foreground
    # Reject isolated greenish denoising pixels on the neutral bole. The photo
    # landmarks likewise describe the continuous crown, not single stray tips.
    row_counts=green.sum(axis=1)
    dense_rows=row_counts>=max(8,round(im.shape[1]*.01))
    green &= dense_rows[:,None]
    ys,xs=np.nonzero(green)
    # Twig/leaf surfaces only; bark is neutral and excluded from crown.
    box=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
    ground=int(np.nonzero(foreground)[0].max())
    spans=np.zeros(im.shape[0])
    for y in range(box[1],box[3]+1):
        x=np.flatnonzero(green[y])
        if len(x)>8:spans[y]=np.percentile(x,99)-np.percentile(x,1)
    # A 3% crown-height window rejects one projecting leaf/tuft. Photos use
    # a manually inspected broad horizontal band with ±30 px uncertainty.
    window=max(3,round((box[3]-box[1])*.03));smooth=np.convolve(spans,np.ones(window)/window,mode='same')
    widest_y=int(np.argmax(smooth))
    lum=(im[:,:,:3]/255)[green]@np.array([.2126,.7152,.0722])
    return dict(crown_box_px=box,ground_y=ground,base_fraction_of_tree=(ground-box[3])/(ground-box[1]),width_height=(box[2]-box[0])/(box[3]-box[1]),
                widest_y_px=widest_y,widest_height_fraction_of_crown=(box[3]-widest_y)/(box[3]-box[1]),
                widest_height_fraction_of_tree=(ground-widest_y)/(ground-box[1]),
                widest_height_at_12_4m=(ground-widest_y)/(ground-box[1])*12.4,
                green_luminance_p5_p50_p95=np.percentile(lum,[5,50,95]).tolist(),
                near_black_green_fraction=float(np.mean(lum<.02)),clipped_green_fraction=float(np.mean(np.any(im[:,:,:3][green]>=254,axis=1))))
