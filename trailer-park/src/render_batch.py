"""One GPU lease, fresh serial Blender processes, resumable scene receipts."""
import argparse,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def merge(folder,rows):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);path=folder/'provenance.json'
    previous=json.loads(path.read_text()) if path.exists() else [];keys={(r['stem'],r['shot']) for r in rows}
    path.write_text(json.dumps([r for r in previous if (r['stem'],r['shot']) not in keys]+rows,indent=2))


def run_job(name,args,outputs,exports=Path('export'),camera=None):
    source=[]
    for stem in sorted({stem for stem,shot in outputs}):
        path=exports/(stem+'.gltf');doc=json.loads(path.read_text())
        source.extend([digest(path),digest(path.with_suffix('.json')),digest(path.parent/doc['buffers'][0]['uri'])])
        source.extend(digest(path.parent/im['uri']) for im in doc.get('images',[]))
    recipe=[digest(HERE/file) for file in ('render.py','town_context.py','geometry.py','traffic.py','inspection.py')]
    if camera:recipe.append(digest(camera))
    key=hashlib.sha256(json.dumps([source,recipe,args]).encode()).hexdigest()
    cache=Path('build/render-jobs')/(name+'.json');cache.parent.mkdir(parents=True,exist_ok=True)
    if cache.exists():
        old=json.loads(cache.read_text())
        if old['key']==key and all(Path(p).is_file() and digest(p)==sha for p,sha in old['files'].items()):
            print('REUSE',name,flush=True);merge(old['folder'],old['rows']);return
    command=[os.environ.get('BLENDER','blender'),'-b','-t','2','--factory-startup','--python-exit-code','1','--python','src/render.py','--',*args,'--exports',str(exports)]
    print('RENDER JOB',name,flush=True);subprocess.run(command,check=True)
    folder=Path(args[args.index('--out')+1]);rows=[];files={}
    for stem,shot in outputs:
        p=folder/stem/(shot+'.png')
        if not p.exists():p=folder/'matches'/stem/(shot+'.png')
        receipt=p.with_suffix('.receipt.json');row=json.loads(receipt.read_text())
        assert digest(p)==row['image_sha256'];assert digest(row['source'])==row['sha256']
        files[str(p)]=digest(p);files[str(receipt)]=digest(receipt);rows.append(row)
    cache.write_text(json.dumps(dict(key=key,folder=str(folder),files=files,rows=rows),indent=2))


def before_frames(after,width):
    """Reuse the supplied accepted frame bytes only after camera/light checks."""
    frozen=Path('build/round4-before');old_folder=Path('renders/age-pass3');out=Path('renders/finish-before')
    if not (frozen/'export/Park-101.gltf').exists():return False
    if not (old_folder/'provenance.json').exists():return False
    historical=json.loads((old_folder/'provenance.json').read_text());current=json.loads((after/'provenance.json').read_text());rows=[]
    keys=('direction','sun_energy','sky_strength','exposure','angle_degrees','sky_saturation','camera_sky_strength','camera_sky_saturation')
    for stem,shot in (('Park-101','hero'),('Park-101','row'),('Park-202','hero')):
        old=next(r for r in historical if r['stem']==stem and r['shot']==shot);new=next(r for r in current if r['stem']==stem and r['shot']==shot)
        source=frozen/'build/embedded'/(stem+'.glb');assert digest(source)==old['sha256']
        assert old['camera_parameters']==new['camera_parameters'] and old['width']==width
        assert max(abs(x-y) for p,q in zip(old['camera_matrix_world'],new['camera_matrix_world']) for x,y in zip(p,q))<1e-6
        assert all(old['light'][k]==new['light'][k] for k in keys)
        path=out/stem/(shot+'.png');path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(old_folder/stem/(shot+'.png'),path)
        meta=json.loads((frozen/'export'/(stem+'.json')).read_text())
        row=dict(old,delivery=str(frozen/'export'/(stem+'.gltf')),images=meta['images'],reused_verified_frame=str(old_folder/stem/(shot+'.png')),image_sha256=digest(path))
        path.with_suffix('.receipt.json').write_text(json.dumps(row,indent=2));rows.append(row)
    merge(out,rows);return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32)
    p.add_argument('--cameras',type=Path,default=Path('build/cameras.json'));p.add_argument('--delivery',action='store_true');p.add_argument('--source');p.add_argument('--eevee',action='store_true');a=p.parse_args()
    assert os.environ.get('ASSETS_GPU_HELD')=='1';os.environ['PYTHONDONTWRITEBYTECODE']='1'
    base=['--out',str(a.out),'--width',str(a.width),'--samples',str(a.samples)]
    jobs=[('Park-101',['hero','row']),('Park-202',['hero'])]
    if a.delivery:
        jobs=[(s,['hero','above','entrance','row']) for s in ('Park-101','Park-202')]
        jobs += [(s,['hero','front','side','back','top','skirt','entry','scale']) for s in ('SingleWide-120','DoubleWide-228')]
        jobs += [(s,['detail']) for s in ('Deck','Carport','UtilityService','EntranceSign','Modules','HomeForms')]
        jobs += [('SupportFrame',['detail','piers'])]
    for stem,shots in jobs:
        extra=['--eevee'] if a.delivery and stem=='Park-202' else []
        outputs=[(stem,s) for s in shots]+([(stem,'eevee')] if extra else [])
        run_job(a.out.name+'-'+stem,base+['--only',stem,'--shots',','.join(shots),*extra],outputs)
    cameras=json.loads(a.cameras.read_text());chosen=list(cameras) if a.delivery else ['street-2007'];street=None
    for name in chosen:
        path=Path('build/render-jobs')/(name+'-camera.json');path.write_text(json.dumps({name:cameras[name]},indent=2));stem=cameras[name]['asset']
        if name=='street-2007':street=path
        run_job(a.out.name+'-'+name,base+['--only',stem,'--shots','none','--cameras',str(path)],[(stem,name)],camera=path)
        if a.delivery:
            source=['--out','renders/source',*base[2:],'--only',stem,'--shots','none','--cameras',str(path),'--source-finish']
            run_job(a.out.name+'-source-'+name,source,[(stem,name)],camera=path)
    if before_frames(a.out,a.width):
        args=['--out','renders/finish-before','--width',str(a.width),'--samples',str(a.samples),'--only','Park-101','--shots','none','--cameras',str(street)]
        run_job(a.out.name+'-before-street',args,[('Park-101','street-2007')],Path('build/round4-before/export'),street)
    print('SERIAL BATCH COMPLETE',a.out,flush=True)


if __name__=='__main__':main()
