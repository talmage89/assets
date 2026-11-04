"""Actual split construction, surface, motion, raw delivery and image reuse."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from check_delivery import check
from cape_delivery_check import surfaces
from kit.motion import sweep
from kit.image_io import read_png


def preserved():
    from split_preserved import reference
    files,baseline,handoff=reference()
    changed=[name for name,digest in files.items() if not Path(name).exists() or hashlib.sha256(Path(name).read_bytes()).hexdigest()!=digest]
    assert not changed,changed
    return dict(passed=True,files=len(files),sha256=files,baseline=baseline,accepted_handoff_bytes=handoff,scope='All captured colonial, ranch, Cape exports, shared maps and committed docs; exact bytes')


def textures():
    rows=[]
    for path in sorted(Path('export/textures').glob('*.png')):
        a=read_png(path);h,w,c=a.shape;assert c==3 and np.isfinite(a).all()
        error=None
        if '_Normal' in path.name:
            error=float(abs(np.linalg.norm(a*2-1,axis=2)-1).max());assert error<.008,(path,error)
        rows.append(dict(path=str(path),size=[w,h],bytes=path.stat().st_size,gpu_mib=w*h*4/3/1048576,normal_length_error=error,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    assert len(rows)==41 and abs(sum(r['gpu_mib'] for r in rows)-49)<1e-6
    return rows


def reuse(seeds):
    bpy.ops.wm.read_factory_settings(use_empty=True);seen={};steps=[]
    paths=[Path(f'export/HearthfieldSplit-{s}.gltf') for s in seeds]+[Path('export/Hearthfield-27.gltf'),Path('export/HearthfieldRanch-12.gltf'),Path('export/HearthfieldCape-36.gltf'),Path(f'export/HearthfieldSplit-{seeds[0]}.gltf')]
    for path in paths:
        bpy.ops.import_scene.gltf(filepath=str(path.resolve()));current={}
        for im in bpy.data.images:
            if im.source!='FILE' or not im.filepath:continue
            key=str(Path(bpy.path.abspath(im.filepath)).resolve());assert key not in current
            current[key]=im.as_pointer()
            if key in seen:assert seen[key]==im.as_pointer()
            seen[key]=im.as_pointer()
        steps.append(dict(source=str(path),images=len(current)))
    assert len(seen)<=41
    return dict(passed=True,unique_images=len(seen),steps=steps,scope='Actual Blender image identity across four types and repeat split')


def main(seeds):
    rows=[]
    for seed in seeds:
        row=check(seed,split=True);assert 30000<=row['triangles']<=45000,(seed,row['triangles'])
        row['source_surfaces']=surfaces(seed,kind='split')
        path=Path(f'build/split/delivery/game-{seed}.blend');bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
        motion=sweep(dict(MOTIONS=[dict(node='FrontDoor',axis='Z',range=[0,105],step=3,tolerance_m=.0005),dict(node='ServiceDoor',axis='Z',range=[-100,0],step=5,tolerance_m=.0005)]));assert motion['passed'];row['motion']=motion
        from plan import generate
        from split_motion import check as garage_check
        meta=json.loads(path.with_suffix('.json').read_text());garage=garage_check(generate(seed,meta['spec'],house_type='split'));assert garage['passed'];row['garage_motion']=garage
        doc=json.loads(Path(f'export/HearthfieldSplit-{seed}.gltf').read_text())
        roof=next(m for m in doc['materials'] if m['name']=='RanchRoof')
        factor=roof['pbrMetallicRoughness'].get('baseColorFactor',[1,1,1,1])
        expected=meta['roof_color_precision']['material_factor'];assert max(abs(c-expected) for c in factor[:3])<1e-6
        assert abs(roof['pbrMetallicRoughness']['roughnessFactor']-.925)<1e-6 and roof['pbrMetallicRoughness'].get('metallicFactor',1)==0
        row['roof_color_precision']=dict(**meta['roof_color_precision'],exported_base_color_factor=factor)
        veneer=next(m for m in doc['materials'] if m['name']=='SplitStone');p=veneer['pbrMetallicRoughness']
        assert p.get('metallicFactor',1)==0 and abs(p.get('roughnessFactor',1)-.91)<1e-6
        assert 'metallicRoughnessTexture' not in p and 'occlusionTexture' not in veneer
        row['veneer_scalar_orm']=dict(roughness=p['roughnessFactor'],metallic=0,occlusion=1,no_extra_image=True)
        texture=veneer['normalTexture'];transform=texture['extensions']['KHR_texture_transform']
        from split_atlas import rect
        if meta['spec']['veneer']=='stone':scale=2.;offset=-1.;normal_name='T_SplitStone_Normal.png';normal_size=512
        else:
            r=rect(str(seed));scale=1/(r[3]-r[1]);offset=1-scale+r[1]/(r[3]-r[1]);normal_name='T_CapeBrick_Normal.png';normal_size=256
        assert max(abs(a-b) for a,b in zip(transform['scale'],[1,scale]))<1e-6
        assert max(abs(a-b) for a,b in zip(transform['offset'],[0,offset]))<1e-6
        image=doc['images'][doc['textures'][texture['index']]['source']]['uri'];assert image=='textures/'+normal_name
        row['veneer_normal_mapping']=dict(image=image,transform=transform,measured_median_normal_density_px_m=row['density_px_m']['SplitStone']['median']*(normal_size/512)*scale**.5)
        rows.append(row)
    maps=textures();result=dict(passed=True,rows=rows,textures=maps,family_gpu_mib=sum(r['gpu_mib'] for r in maps),family_png_bytes=sum(r['bytes'] for r in maps),preserved=preserved(),image_reuse=reuse(seeds))
    Path('build/split/delivery/check.json').write_text(json.dumps(result,indent=2));print('SPLIT_DELIVERY_CHECK',[(r['seed'],r['triangles']) for r in rows],result['family_gpu_mib'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seeds',default='51,52,53,54,55,56');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);main(list(map(int,a.seeds.split(','))))
