"""Cape construction, raw glTF, fresh import, surfaces, motion and family bytes."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from check_delivery import check
from check_mesh import surface
from kit.motion import sweep
from kit.image_io import read_png


def preserved():
    baseline=Path('build/cape/accepted-files.json')
    if not baseline.exists():baseline=Path('build/cape/delivery/legacy-before.json')
    files=json.loads(baseline.read_text());changed=[]
    for name,digest in files.items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=digest:changed.append(name)
    assert not changed,('Existing family files changed',changed)
    return dict(passed=True,files=len(files),sha256=files)


def surfaces(seed,kind='cape'):
    path=Path(f'build/{kind}/delivery/game-{seed}.blend');bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
    game={o.name:o for o in bpy.context.scene.objects if o.type=='MESH'}
    target={name:surface([ob]) for name,ob in game.items()}
    triangles={}
    exact={}
    for name,ob in game.items():
        ob.data.calc_loop_triangles()
        triangles[name]=np.array([[tuple(ob.matrix_world@ob.data.vertices[i].co) for i in t.vertices] for t in ob.data.loop_triangles],dtype='float64')
        exact[name]={tuple(sorted(tuple(round(float(x),6) for x in p) for p in t)):t for t in triangles[name]}
    # Fresh source geometry, compared on actual triangle interiors and vertices.
    bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/{kind}/house-{seed}.blend').resolve()))
    assert {o.name for o in bpy.context.scene.objects if o.type=='MESH'}==set(target),'Source/game object names differ'
    maximum=0;points=0;by_object={};raw_maximum=0;refined=0;matched=0
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.name not in target:continue
        ob.data.calc_loop_triangles();tree=target[ob.name]
        for tri in ob.data.loop_triangles:
            xyz=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
            key=tuple(sorted(tuple(round(float(x),6) for x in p) for p in xyz))
            if key in exact[ob.name]:
                corresponding=exact[ob.name][key];delta=max(min(np.linalg.norm(np.array(p)-q) for q in corresponding) for p in xyz)
                maximum=max(maximum,float(delta));points+=4;matched+=4;continue
            for p in [sum(xyz,Vector())/3,*xyz]:
                hit=tree.find_nearest(p);assert hit[0] is not None
                distance=float(hit[3]);raw_maximum=max(raw_maximum,distance)
                if distance>2e-6:
                    # Blender's float BVH closest-point calculation is poorly
                    # conditioned on millimeter-wide, multi-meter gauge faces.
                    # Keep its candidates, then solve their actual triangles
                    # in float64. The raw residual remains in the report.
                    ids={h[2] for h in tree.find_nearest_range(p,.025)}|{hit[2]}
                    tri=triangles[ob.name][sorted(ids)];a=tri[:,0];e=tri[:,1]-a;f=tri[:,2]-a;v=np.array(p,dtype='float64')-a;n=np.cross(e,f);n2=np.sum(n*n,axis=1)
                    u=np.sum(np.cross(v,f)*n,axis=1)/n2;w=np.sum(np.cross(e,v)*n,axis=1)/n2
                    inside=(u>=-1e-8)&(w>=-1e-8)&(u+w<=1+1e-8)
                    distances=np.where(inside,abs(np.sum(v*n,axis=1))/np.sqrt(n2),np.inf)
                    for i,j in ((0,1),(1,2),(2,0)):
                        start=tri[:,i];edge=tri[:,j]-start;q=np.array(p)-start;t=np.clip(np.sum(q*edge,axis=1)/np.sum(edge*edge,axis=1),0,1)
                        distances=np.minimum(distances,np.linalg.norm(q-edge*t[:,None],axis=1))
                    distance=float(distances.min());refined+=1
                maximum=max(maximum,distance);points+=1;by_object[ob.name]=max(by_object.get(ob.name,0),distance)
    print('CAPE_SURFACE_RESIDUALS',seed,sorted(by_object.items(),key=lambda kv:kv[1],reverse=True)[:6],flush=True)
    assert maximum<5e-6,(seed,maximum)
    return dict(passed=True,source_surface_samples=points,source_to_chart_surface_max_m=maximum,raw_float_bvh_max_m=raw_maximum,float64_refined_samples=refined,matched_triangle_samples=matched,scope='Actual source and delivery surfaces, independent of serialization; matched triangle vertices and float64 triangle refinement for ill-conditioned thin faces; tiny ridge-cap area tolerances still require this displacement bound')


def scalar_orm(seeds):
    from cape_masonry import ROUGHNESS
    rows=[]
    for seed in seeds:
        doc=json.loads(Path(f'export/HearthfieldCape-{seed}.gltf').read_text())
        for mat in doc['materials']:
            name=mat['name'].split('.')[0]
            if name not in ROUGHNESS:continue
            p=mat['pbrMetallicRoughness'];assert 'metallicRoughnessTexture' not in p and 'occlusionTexture' not in mat
            assert p.get('metallicFactor',1)==0 and abs(p.get('roughnessFactor',1)-ROUGHNESS[name])<1e-6
            rows.append(dict(seed=seed,material=name,roughness=p['roughnessFactor'],metallic=0,occlusion=1,scope='Actual exported scalar parameters; authored uniform dielectric parameters; no ORM image or packed-region boundary bleed'))
    return rows


def textures():
    rows=[]
    for path in sorted(Path('export/textures').glob('*.png')):
        if path.name.startswith('T_Split'):continue
        a=read_png(path);assert a.ndim==3 and a.shape[2]==3 and np.isfinite(a).all()
        if path.name.startswith(('T_CapeCedar_','T_CapeCement_')):assert a.shape[:2]==(256,512)
        else:assert a.shape[0]==a.shape[1]
        error=None
        if '_Normal' in path.name:
            error=float(abs(np.linalg.norm(a*2-1,axis=2)-1).max());assert error<.008
        h,w=a.shape[:2];rows.append(dict(path=str(path),size=[w,h],bytes=path.stat().st_size,gpu_mib=w*h*4/3/1048576,normal_length_error=error,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    assert len(rows)==39 and abs(sum(r['gpu_mib'] for r in rows)-(48+1/3))<1e-6
    return rows


def reuse(seeds):
    bpy.ops.wm.read_factory_settings(use_empty=True);seen={};steps=[]
    paths=[Path(f'export/HearthfieldCape-{s}.gltf') for s in seeds]+[Path('export/Hearthfield-27.gltf'),Path('export/HearthfieldRanch-12.gltf'),Path(f'export/HearthfieldCape-{seeds[0]}.gltf')]
    for path in paths:
        bpy.ops.import_scene.gltf(filepath=str(path.resolve()));current={}
        for im in bpy.data.images:
            if im.source!='FILE' or not im.filepath:continue
            key=str(Path(bpy.path.abspath(im.filepath)).resolve());assert key not in current
            current[key]=im.as_pointer()
            if key in seen:assert seen[key]==im.as_pointer()
            seen[key]=im.as_pointer()
        steps.append(dict(source=str(path),images=len(current)))
    assert len(seen)<=39
    return dict(passed=True,unique_images=len(seen),steps=steps,scope='Actual Blender image identity across all three types and a repeated Cape')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seeds',default='31,32,33,34,35,36');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);seeds=list(map(int,a.seeds.split(',')));rows=[]
    for seed in seeds:
        row=check(seed,cape=True);assert 30000<=row['triangles']<=45000,(seed,row['triangles'])
        row['source_surfaces']=surfaces(seed)
        bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/cape/delivery/game-{seed}.blend').resolve()))
        motion=sweep(dict(MOTIONS=[dict(node='FrontDoor',axis='Z',range=[0,105],step=3,tolerance_m=.0005),dict(node='ServiceDoor',axis='Z',range=[-100,0],step=5,tolerance_m=.0005)]));assert motion['passed'];row['motion']=motion;rows.append(row)
    control=check('34-control',cape=True) if 34 in seeds else None
    maps=textures();result=dict(passed=True,scalar_orm=scalar_orm(seeds),auxiliary_paint_control=control,rows=rows,textures=maps,family_gpu_mib=sum(r['gpu_mib'] for r in maps),family_png_bytes=sum(r['bytes'] for r in maps),preserved=preserved(),image_reuse=reuse(seeds))
    Path('build/cape/delivery/check.json').write_text(json.dumps(result,indent=2));print('CAPE_DELIVERY_CHECK',[(r['seed'],r['triangles']) for r in rows],result['family_gpu_mib'],flush=True)
