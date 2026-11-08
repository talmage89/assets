"""Rebuild b0dbccc privately, then compare it with today's exact cameras.

Only the old family's code is extracted. Native deliveries and maps are
read-only inputs; no other worktree or sibling build is touched.
"""
import argparse,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,tarfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ASSET=HERE.parent;ROOT=HERE.parents[1]


def prepare():
    stage=ASSET/'build/age-baseline/repo';family=stage/'trailer-park';stage.mkdir(parents=True,exist_ok=True)
    if not (family/'src/build.py').exists():
        data=subprocess.check_output(['git','archive','b0dbccc','trailer-park'],cwd=ROOT)
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(stage,filter='data')
    for p in ROOT.iterdir():
        if not p.is_dir() or p.name.startswith('.') or p.name in ('build','trailer-park'):continue
        q=stage/p.name
        if not q.exists():q.symlink_to(p,target_is_directory=True)
    for dest,source in ((family/'textures',ASSET/'textures'),(family/'build/native',ASSET/'build/native'),(family/'build/library',ASSET/'build/library')):
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():dest.symlink_to(source,target_is_directory=True)
    cached=ASSET/'build/accepted-age'
    if (cached/'export/Park-202.gltf').exists() and not (family/'export/Park-202.gltf').exists():
        assert (cached/'src/build.py').read_bytes()==subprocess.check_output(['git','show','b0dbccc:trailer-park/src/build.py'],cwd=ROOT)
        dest=family/'export';dest.mkdir(parents=True,exist_ok=True)
        for stem in ('Park-101','Park-202'):
            path=cached/'export'/(stem+'.gltf');doc=json.loads(path.read_text());meta=json.loads(path.with_suffix('.json').read_text())
            for im,record in zip(doc['images'],meta['images']):
                original=ASSET/'export'/im['uri'];assert hashlib.sha256(original.read_bytes()).hexdigest()==record['sha256']
                im['uri']=os.path.relpath(original.resolve(),dest);record['uri']=im['uri']
            shutil.copy2(path.parent/doc['buffers'][0]['uri'],dest/doc['buffers'][0]['uri'])
            (dest/path.name).write_text(json.dumps(doc,separators=(',',':'))+'\n');(dest/path.with_suffix('.json').name).write_text(json.dumps(meta,indent=2))
    if not (family/'export/Park-202.gltf').exists():
        with (ASSET/'build/age-baseline/model.log').open('w') as log:
            subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','2','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out','build/family.blend'],cwd=family,stdout=log,stderr=subprocess.STDOUT,check=True)
    return family


def render_before(family,receipt,out,width,samples):
    sys.path[:0]=[str(HERE),str(ROOT)]
    import render as renderer
    spec=importlib.util.spec_from_file_location('_accepted_town',family/'src/town_context.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
    renderer.context=legacy.context;rows=json.loads(receipt.read_text());all_=[]
    for stem in ('Park-101','Park-202'):
        views={r['shot']:dict(r['camera'],light=r['light'],fixed_camera=True,fixed_matrix=r['camera_matrix_world'])
               for r in rows if r['stem']==stem and r['shot'] in ('hero','row','above','street-2007')}
        path=family/'export'/(stem+'.gltf');meta=json.loads(path.with_suffix('.json').read_text())
        all_+=renderer.render(stem,path,meta,views,out,width,samples,True)
    out.mkdir(parents=True,exist_ok=True);(out/'provenance.json').write_text(json.dumps(all_,indent=2))


if __name__=='__main__':
    if '--' in sys.argv:sys.argv=sys.argv[:1]+sys.argv[sys.argv.index('--')+1:]
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--receipt',type=Path,default=Path('renders/final/provenance.json'))
    p.add_argument('--out',type=Path,default=Path('renders/age-before'));p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);a=p.parse_args()
    if a.prepare:prepare()
    else:render_before(ASSET/'build/age-baseline/repo/trailer-park',a.receipt,a.out,a.width,a.samples)
