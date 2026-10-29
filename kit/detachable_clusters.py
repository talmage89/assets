"""Translate atlas neighborhoods without separating their existing UV islands.

The atlas itself supplies interior margins and filtering colors. Source regions
may overlap after a split: this duplicates source texels, never surface charts.
Destinations and their complete protected mip blocks are disjoint.
"""
import numpy as np

from kit.detachable_textures import _pack, _mask


def _expand(mask, pixels):
    """Square dilation without dependencies outside Blender's numpy."""
    h,w=mask.shape; padded=np.pad(mask,pixels)
    # Separable OR avoids constructing (2p+1)^2 full-size temporaries.
    horizontal=np.logical_or.reduce([padded[:,x:x+w] for x in range(2*pixels+1)])
    return np.logical_or.reduce([horizontal[y:y+h] for y in range(2*pixels+1)])


def neighborhoods(islands, source_size, layer, padding=6):
    """Connected components of touching/overlapping guarded sampling masks."""
    border=padding+4; owner=np.full((source_size+2*border,)*2,-1,np.int32)
    parents=list(range(len(islands)))
    def root(i):
        while parents[i]!=i:
            parents[i]=parents[parents[i]];i=parents[i]
        return i
    for index,island in enumerate(islands):
        mask=_mask(island['ob'].data,island['ob'].data.uv_layers[layer],
                   island['loops'],island['lo'],island['shape'],source_size)
        guard=_expand(np.pad(mask,padding),padding)
        # Inspect one extra ring for touching guards, but store only the guard.
        x,y=map(int,island['lo']-padding+border);h,w=guard.shape
        nearby=owner[y-1:y+h+1,x-1:x+w+1]
        touching=_expand(np.pad(guard,1),1)
        for previous in np.unique(nearby[touching]):
            if previous>=0:parents[root(int(previous))]=root(index)
        owner[y:y+h,x:x+w][guard]=index
    groups={}
    for index in range(len(islands)):groups.setdefault(root(index),[]).append(index)
    return list(groups.values())


def plan(islands, source_size, size, block, layer):
    """Try intact components, then whole-island bands for oversized components.

    Band membership uses each island's full extent, so the separating seam
    follows empty atlas margins around crossing islands, rather than cutting
    those islands at the nominal band height. Overlapping source copy halos
    retain the atlas on both sides of that seam. No rotation or scale occurs.
    """
    groups=neighborhoods(islands,source_size,layer)
    points=[np.array([i['ob'].data.uv_layers[layer].data[k].uv[:]
                      for k in i['loops']])*source_size for i in islands]
    lows=np.array([p.min(axis=0) for p in points]);highs=np.array([p.max(axis=0) for p in points])
    def region(ids,padding):
        lo=(np.floor(lows[ids].min(axis=0)-1).astype(int)//block)*block-padding
        hi=((np.ceil(highs[ids].max(axis=0)+1).astype(int)+block-1)//block)*block+padding
        # A full extra block preserves the exact source box/bilinear stencil.
        return dict(islands=ids,source_origin=lo,shape=hi-lo)
    padding=block
    parts=[];splits=[]
    for group in groups:
        whole=region(group,padding)
        if whole['shape'].max()<=size:
            parts.append(group);continue
        remaining=set(group);split=[]
        # Keep a block of halo plus the rounded bilinear footprint on both sides.
        span=size-4*block
        while remaining:
            start=min(lows[i,1] for i in remaining)
            ids=[i for i in sorted(remaining) if highs[i,1]<=start+span]
            if not ids:
                raise ValueError('An atlas island exceeds the cluster map; scaling is required')
            remaining.difference_update(ids);parts.append(ids);split.append(ids)
        splits.append(dict(original_islands=group,parts=split,
                           seam='Empty margins between intact islands; source filtering halos overlap'))
    regions=[region(ids,padding) for ids in parts]
    rectangles=[tuple(map(int,r['shape']//block)) for r in regions]
    positions=_pack(rectangles,size//block)
    if positions is None:
        raise ValueError(f'Atlas clusters cannot fit {size} at original density')
    for row,position in zip(regions,positions):row['destination_origin']=np.array(position)*block
    return dict(regions=regions,original_cluster_count=len(groups),splits=splits,padding=padding)


def copy(islands, arrays, size, block, layer):
    """Copy complete atlas regions and apply one integer offset per member."""
    source_size=next(iter(arrays.values())).shape[0]
    packed=plan(islands,source_size,size,block,layer)
    result={c:np.zeros((size,size,a.shape[2]),np.float32) for c,a in arrays.items()}
    occupied=np.zeros((size,size),bool);surface=np.zeros_like(occupied);records=[];regions=[]
    for index,row in enumerate(packed['regions']):
        ox,oy=map(int,row['source_origin']);x,y=map(int,row['destination_origin']);w,h=map(int,row['shape'])
        for channel,source in arrays.items():
            result[channel][y:y+h,x:x+w]=source[np.arange(oy,oy+h)%source_size][:,np.arange(ox,ox+w)%source_size]
        occupied[y:y+h,x:x+w]=True
        # Copied normals, including atlas margins, stay exact. Only background
        # normals generated by pull-push are subsequently renormalized.
        surface[y:y+h,x:x+w]=True
        offset=np.array((x-ox,y-oy))
        for i in row['islands']:
            island=islands[i];mesh=island['ob'].data;data=mesh.uv_layers[layer].data
            loops=set(island['loops'])
            triangles=[[[float(v) for v in np.array(data[k].uv)*source_size+offset]
                        for k in tri.loops] for tri in mesh.loop_triangles if tri.loops[0] in loops]
            records.append(dict(object=island['ob'].name,loops=island['loops'],cluster=index,
                source_origin=island['lo'].tolist(),shape=island['shape'].tolist(),
                destination_origin=(island['lo']+offset).tolist(),triangle_pixels=triangles))
            for k in island['loops']:data[k].uv=(np.array(data[k].uv)*source_size+offset)/size
        regions.append(dict(source_origin=[ox,oy],destination_origin=[x,y],shape=[w,h],
                            islands=row['islands'],padding=packed['padding']))
    return result,occupied,surface,records,dict(regions=regions,
        original_cluster_count=packed['original_cluster_count'],splits=packed['splits'])
