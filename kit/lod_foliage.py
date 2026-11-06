"""Deterministic spatially stratified, enlarged leaf-card levels."""
import numpy as np
from kit.lod_mesh import components,simplify


def cards(attrs,faces,target_triangles,scale_exponent=.4,selection="balanced"):
    if selection not in ("balanced","density"):raise ValueError("Unknown leaf card selection: "+selection)
    groups=components(attrs,faces)
    centers=np.array([attrs['POSITION'][np.unique(faces[g])].mean(axis=0) for g in groups])
    desired=max(1,min(len(groups),target_triangles//2))
    # Quantized crown cells support balanced or density-proportional sampling.
    # Stable hashing avoids directional selection stripes within each cell.
    lo=centers.min(axis=0);span=np.maximum(np.ptp(centers,axis=0),1e-6)
    divisions=max(1,int(round(desired**(1/3))))
    cells=np.floor((centers-lo)/span*divisions).astype(np.int64)
    hashed=((np.arange(len(groups),dtype=np.uint64)+37)*np.uint64(2654435761))%np.uint64(4294967291)
    bins={}
    for i,key in enumerate(map(tuple,cells)):bins.setdefault(key,[]).append(i)
    ordered=[sorted(ids,key=lambda i:int(hashed[i])) for key,ids in sorted(bins.items())]
    if selection=="density":
        # Equal quotas overrepresent sparse outer cells. Largest remainders
        # preserve the original crown's spatial mass and the exact card count.
        quota=np.array([len(ids)*desired/len(groups) for ids in ordered])
        counts=np.floor(quota).astype(int)
        for index in np.argsort(-(quota-counts),kind='stable')[:desired-int(counts.sum())]:counts[index]+=1
        chosen=[i for ids,count in zip(ordered,counts) for i in ids[:count]]
    else:
        chosen=[];depth=0
        while len(chosen)<desired:
            for ids in ordered:
                if depth<len(ids):chosen.append(ids[depth])
                if len(chosen)>=desired:break
            depth+=1
    # Equal total card area overfills the visible crown: larger cards overlap
    # less often. Slightly sublinear compensation preserves visible coverage.
    scale=(len(groups)/len(chosen))**scale_exponent
    fields={k:[] for k in attrs};triangles=[];offset=0
    for i in sorted(chosen):
        f=faces[groups[i]];ids,remap=np.unique(f,return_inverse=True)
        for k,v in attrs.items():
            a=v[ids].copy()
            if k=='POSITION':a=np.clip(centers[i]+(a-centers[i])*scale,attrs['POSITION'].min(axis=0),attrs['POSITION'].max(axis=0))
            fields[k].append(a)
        triangles.append(remap.reshape(-1,3).astype(np.uint32)+offset);offset+=len(ids)
    return {k:np.concatenate(v) for k,v in fields.items()},np.concatenate(triangles),dict(original_cards=len(groups),cards=len(chosen),area_scale=scale*scale,linear_scale=scale,scale_exponent=scale_exponent,spatial_cells=len(bins),selection=selection)


def build(doc,target,meters_per_pixel,scale_exponent=.4,selection="balanced"):
    reports=[]
    wood=[];leaves=[]
    for mi,pi,p in doc.primitives():
        mat=doc.data['materials'][p.get('material',0)]
        (leaves if mat.get('alphaMode') in ('MASK','BLEND') else wood).append(p)
    wood_target=max(160,round(target*.2));wood_count=0
    for p in wood:
        a,f=doc.arrays(p)
        # Retain bark chart hints and interpolated Wind; source field is
        # transported onto the decimated branch stations. Card coverage gets
        # the majority of the distant budget.
        aa,ff,row=simplify(a,f,wood_target/max(1,len(f)),meters_per_pixel*.75,max_uv_error=1,screen_space=True,rebake=True)
        doc.replace(p,aa,ff);wood_count+=len(ff);reports.append(dict(wood=row))
    if wood_count>=target-2:raise ValueError('Branch reduction did not leave a viable leaf-card budget; refusing a giant-card fallback')
    leaf_target=target-wood_count
    for p in leaves:
        a,f=doc.arrays(p);aa,ff,row=cards(a,f,leaf_target,scale_exponent,selection);doc.replace(p,aa,ff);reports.append(dict(leaves=row))
    return reports
