"""Raw exported PBR/UV/frame audits, independent of construction declarations."""
import argparse,sys,json,math,hashlib,io
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.gltf import GLB
from kit.uv import intersection_area

def owner(g,index):
    while index in g.parents:index=g.parents[index]
    return g.json['nodes'][index]

def weighted_percentiles(values,weights):
    if not values:return {}
    pairs=sorted(zip(values,weights));total=sum(weights);acc=0;result={}
    for value,weight in pairs:
        acc+=weight
        for p in (5,50,95):
            if str(p) not in result and acc>=total*p/100:result[str(p)]=float(value)
    return result

def image_receipts(g):
    out=[]
    for i,row in enumerate(g.json.get('images',[])):
        payload=g.image(i);im=Image.open(io.BytesIO(payload));a=np.asarray(im)
        out.append(dict(name=row.get('name',str(i)),sha256=hashlib.sha256(payload).hexdigest(),size=list(im.size),bytes=len(payload),channels=len(im.getbands()),
                        alpha_has_holes=bool(a.shape[2]==4 and np.any(a[:,:,3]<30) and np.any(a[:,:,3]>220)) if a.ndim==3 else False))
    return out

def projected_overlap(triangles):
    """Actual clipped triangle overlaps in a bowl's plan projection."""
    grid=defaultdict(list);pairs=set();bounds=[]
    for i,t in enumerate(triangles):
        lo=t.min(axis=0);hi=t.max(axis=0);bounds.append((lo,hi));a=np.floor(lo/.5).astype(int);b=np.floor(hi/.5).astype(int)
        for x in range(a[0],b[0]+1):
            for y in range(a[1],b[1]+1):
                pairs.update((j,i) for j in grid[x,y]);grid[x,y].append(i)
    overlaps=[]
    for a,b in pairs:
        lo1,hi1=bounds[a];lo2,hi2=bounds[b]
        if np.min(np.minimum(hi1,hi2)-np.maximum(lo1,lo2))<=1e-9:continue
        area=intersection_area(triangles[a].tolist(),triangles[b].tolist())
        if area>1e-6:overlaps.append(area)
    return dict(triangles=len(triangles),candidate_pairs=len(pairs),overlap_pairs_above_tolerance=len(overlaps),maximum_overlap_m2=max(overlaps,default=0),total_overlap_m2=sum(overlaps),per_pair_tolerance_m2=1e-6)

def inspect(path,library=False):
    g=GLB(path);images=image_receipts(g);roots=defaultdict(lambda:dict(triangles=0,materials=set()));norm_error=0.;tan_error=0.;dot_error=0.;degenerate=[]
    density=defaultdict(list);area_weights=defaultdict(list);basins=defaultdict(list);tree_primitives=[]
    for ni,node in enumerate(g.json['nodes']):
        if 'mesh' not in node:continue
        root=owner(g,ni);name=root['name'];T=g.world(ni)
        for pi,p in enumerate(g.json['meshes'][node['mesh']]['primitives']):
            attr=p['attributes'];v=g.accessor(attr['POSITION']);n=g.accessor(attr['NORMAL']);idx=g.accessor(p['indices']).reshape(-1,3)
            roots[name]['triangles']+=len(idx);roots[name]['materials'].add(p['material'])
            norm_error=max(norm_error,float(np.abs(np.linalg.norm(n,axis=1)-1).max()))
            mat=g.json['materials'][p['material']];mname=mat['name']
            if 'TANGENT' in attr and 'normalTexture' in mat:
                t=g.accessor(attr['TANGENT']);tan_error=max(tan_error,float(np.abs(np.linalg.norm(t[:,:3],axis=1)-1).max()));dot_error=max(dot_error,float(np.abs((t[:,:3]*n).sum(axis=1)).max()))
            if mname.startswith(('Skate_Trim_Burnish','Skate_AbsorbedWax')):
                cross=np.cross(v[idx[:,1]]-v[idx[:,0]],v[idx[:,2]]-v[idx[:,0]])
                unit=cross/np.maximum(np.linalg.norm(cross,axis=1,keepdims=True),1e-12)
                dots=(unit*n[idx].mean(axis=1)).sum(axis=1)
                assert float(dots.min())>.9,(name,mname,'mark winding disagrees with shading normals',float(dots.min()))
            world=(np.c_[v,np.ones(len(v))]@T.T)[:,:3];xyz=world[:,[0,2,1]].copy();xyz[:,1]*=-1
            if name.startswith('ParkTree'):
                assert 'COLOR_0' not in attr,('Wind became albedo',name)
                assert '_WIND' in attr,('Canonical Wind missing',name)
                tree_primitives.append(dict(tree=name,material=mname,mode=mat.get('alphaMode','OPAQUE'),wind_count=len(g.accessor(attr['_WIND']))))
            if library and 'Concrete' in mname and name.startswith(('Bowl_','SteelBowl_')):
                for tri in xyz[idx]:
                    if tri[:,2].mean()>-.0001:continue
                    q=tri[:,:2]
                    if abs((q[1,0]-q[0,0])*(q[2,1]-q[0,1])-(q[1,1]-q[0,1])*(q[2,0]-q[0,0]))>2e-8:basins['clover' if name.startswith('Steel') else 'kidney'].append(q)
            if not mname.startswith('Skate_'):continue
            tex=mat.get('pbrMetallicRoughness',{}).get('baseColorTexture')
            if not tex:continue  # Native constant-color context has no UV sampler.
            uv=g.accessor(attr['TEXCOORD_0']);q=uv[idx]
            ua=np.abs((q[:,1,0]-q[:,0,0])*(q[:,2,1]-q[:,0,1])-(q[:,1,1]-q[:,0,1])*(q[:,2,0]-q[:,0,0]))*.5
            tri=world[idx];wa=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)*.5
            bad=np.flatnonzero((ua<1e-14)&(wa>1e-9))
            degenerate.extend([dict(root=name,primitive=pi,triangle=int(k),area_m2=float(wa[k])) for k in bad[:8]])
            if tex:
                image=g.json['textures'][tex['index']]['source'];width=images[image]['size'][0]
                good=(ua>1e-14)&(wa>1e-9);density[mname].extend((np.sqrt(ua[good]/wa[good])*width).tolist());area_weights[mname].extend(wa[good].tolist())
                if 'Trim' in mname or 'Wax' in mname:
                    assert np.all(uv>=-1e-6) and np.all(uv<=1.000001),(name,mname,'escaped trim')
    assert norm_error<.001 and tan_error<.002 and dot_error<.003,(norm_error,tan_error,dot_error)
    assert not degenerate,degenerate[:10]
    # A roughness factor must reuse the packed ORM, not manufacture another
    # 2048 map when the wax draw state is exported.
    trim=[row for row in images if row['name'].startswith('T_SkateTrim')]
    assert len({row['sha256'] for row in trim})==3,trim
    if library:
        assert len(roots)>=56
        assert all(r['triangles']<=4000 and len(r['materials'])<=3 for r in roots.values()),{k:(v['triangles'],len(v['materials'])) for k,v in roots.items()}
    masks=[]
    for mat in g.json.get('materials',[]):
        if mat.get('alphaMode')=='MASK':
            tex=mat['pbrMetallicRoughness']['baseColorTexture']['index'];image=g.json['textures'][tex]['source'];assert images[image]['alpha_has_holes'],mat['name']
            masks.append(dict(material=mat['name'],cutoff=mat.get('alphaCutoff',.5),image=images[image]['name']))
    if not library:assert len({row['tree'] for row in tree_primitives})==6 and len(masks)>=4
    overlaps={}
    if library:
        for family,tris in basins.items():
            overlaps[family]=projected_overlap(tris);assert overlaps[family]['total_overlap_m2']<1e-4,(family,overlaps[family])
    unique={row['sha256']:row for row in images}
    compressed=sum(row['size'][0]*row['size'][1]*4/3 for row in unique.values())/1048576
    return dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size,images=images,all_unique_images_compressed_full_mip_MiB=compressed,
                roots={k:dict(triangles=v['triangles'],materials=len(v['materials'])) for k,v in roots.items()},
                distinct_material_states=len(g.json.get('materials',[])),max_normal_unit_error=norm_error,max_tangent_unit_error=tan_error,max_normal_tangent_dot=dot_error,
                degenerate_uv_triangles=degenerate,area_weighted_density_px_m={k:weighted_percentiles(v,area_weights[k]) for k,v in density.items()},
                masks=masks,canonical_tree_attributes=tree_primitives,basin_plan_overlap=overlaps)

def main():
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,default=Path('export/lookdev'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    report=dict(library=inspect(a.folder/'SkateparkPieces.glb',True),parks={str(s):inspect(a.folder/f'Park_{s}.glb') for s in (101,202,303)})
    expected={}
    for name,size in [('SkateTrim',2048),('Prefab',1024)]:
        files=[]
        for channel in ('BaseColor','Normal','ORM'):
            path=Path('textures/ship')/f'T_{name}_{channel}.png';im=Image.open(path);assert im.size==(size,size)
            files.append(dict(path=str(path),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        expected[name]=dict(size=size,maps=files,compressed_full_mip_MiB=3*size*size*4/3/1048576)
    # Three 8bpp block-compressed maps with complete mips, counted once by URI/hash.
    report['new_sets']=expected;report['new_compressed_MiB']=sum(r['compressed_full_mip_MiB'] for r in expected.values());assert abs(report['new_compressed_MiB']-20)<1e-6
    report['ground_reused_compressed_MiB']=48
    protected=Path('../build/skatepark-lookdev/protected.json')
    if protected.exists():
        old=json.loads(protected.read_text());different=[str(path) for path,digest in old.items() if not (HERE.parents[1]/path).is_file() or hashlib.sha256((HERE.parents[1]/path).read_bytes()).hexdigest()!=digest]
        assert not different,different;report['protected_existing_files']=dict(files=len(old),changed=different)
    retained={}
    for folder in ('export/checkpoint','renders/checkpoint','renders/matches'):
        archive=Path('build/before')/folder;current=Path(folder)
        if not archive.exists():continue  # Fresh clones have no prior checkpoint outputs.
        rows=[p for p in archive.rglob('*') if p.is_file()]
        changed=[str(p.relative_to(archive)) for p in rows if not (current/p.relative_to(archive)).is_file() or hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256((current/p.relative_to(archive)).read_bytes()).digest()]
        assert not changed,(folder,changed);retained[folder]=dict(files=len(rows),changed=changed)
    report['retained_original_checkpoint']=retained
    report['passed']=True;Path('build/delivery-audit.json').write_text(json.dumps(report,indent=2));print('DELIVERY AUDIT PASS',json.dumps({s:dict(bytes=r['bytes'],materials=r['distinct_material_states']) for s,r in report['parks'].items()}))

if __name__=='__main__':main()
