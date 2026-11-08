"""Family presentation controller: serial Blender, one GPU lease per small set.

The kit calls the full renderer under with_gpu.sh. Release that initial lease
before any work; child sets each acquire their own. The controller owns no GPU
context. Receipts allow an interrupted set to resume only current, equal-quality
views. Scene assembly and camera calibration happen outside the GPU lease.
"""
import argparse,fcntl,hashlib,json,os,subprocess,sys
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(ROOT),str(HERE)]


def bundle(path):
    path=Path(path);d=json.loads(path.read_text());files=[path]+[path.parent/r['uri'] for k in ('buffers','images') for r in d.get(k,[]) if r.get('uri')]
    return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in files)).hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--out',default='renders/final');p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=96);p.add_argument('--seeds',nargs='+',type=int,default=[117,229,341]);p.add_argument('--lookdev',action='store_true');p.add_argument('--final',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if os.environ.pop('ASSETS_GPU_HELD','0')=='1':
        assert os.fstat(9).st_ino==os.stat(os.environ['ASSETS_GPU_LOCK']).st_ino
        fcntl.flock(9,fcntl.LOCK_UN);os.close(9)
    blender=[os.environ.get('BLENDER_REAL','blender'),'-b','--factory-startup','--python-exit-code','1','-t','4']
    lock=[str(ROOT/'kit/with_gpu.sh')];out=Path(a.out)
    recipe=hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest();botanical=hashlib.sha256((HERE/'look_batch.py').read_bytes()).hexdigest()
    digests={}
    def current(path,source,samples,botany=False):
        meta=path.with_suffix('.json')
        if not path.exists() or not meta.exists():return False
        r=json.loads(meta.read_text());key=str(source)
        if key not in digests:digests[key]=bundle(source)
        return (r.get('bundle_sha256')==digests[key] and r.get('render_script_sha256')==recipe and r.get('samples',0)>=samples and Image.open(path).width==a.width and (not botany or r.get('botanical_recipe_sha256')==botanical))
    for seed in a.seeds:
        plan=json.loads(Path(f'build/garden-{seed}.json').read_text())['plan']
        for names,inspection in [(['hero','above'],False),(['corner','compost','water','shed'],False),(['tomato','bean','squash'],False),(['turf','before-camera','scale','eevee','accessible'],False),(['front','side','back'],True)]:
            names=[n for n in names if not (n in ('scale','eevee') and seed!=117) and not (n=='accessible' and plan['archetype']!='accessible')]
            source=Path(f'export/final/{"Garden" if inspection else "Site"}_{seed}.gltf')
            needed=[n for n in names if not current(out/str(seed)/(n+'.png'),source,max(a.samples,192) if a.final and n=='hero' else a.samples)]
            if not needed:continue
            cmd=lock+blender+['--python',str(HERE/'render.py'),'--','--out',str(out),'--width',str(a.width),'--samples',str(a.samples),'--seeds',str(seed),'--shots',*needed]
            if a.final:cmd.append('--final')
            if inspection:cmd.append('--no-context')
            print('RENDER SET',seed,','.join(needed),flush=True);subprocess.run(cmd,check=True)
    source=Path('export/final/CommunityGardenPieces.gltf')
    if not all(current(out/(name+'.png'),source,a.samples) for name in ('pieces','plants')):
        subprocess.run(lock+blender+['--python',str(HERE/'render.py'),'--','--sheet','--out',str(out),'--width',str(a.width),'--samples',str(a.samples)],check=True)
    for species in (['tomato','squash'],['bean','corn','marigold']):
        needed=[sp for sp in species if not current(out/'plants'/(sp+'.png'),source,a.samples,True)]
        if needed:subprocess.run(lock+blender+['--python',str(HERE/'look_batch.py'),'--','--specimens-only','--species',*needed,'--out',str(out),'--width',str(a.width),'--samples',str(a.samples)],check=True)
    if not current(out/'plants/corn-ear.png',source,a.samples,True):
        subprocess.run(lock+blender+['--python',str(HERE/'look_batch.py'),'--','--ear-only','--out',str(out),'--width',str(a.width),'--samples',str(a.samples)],check=True)
    # Recompute the white balance/lens fit with no GPU context or lease.
    subprocess.run(blender+['--python',str(HERE/'match.py'),'--','--calibrate-only'],check=True)
    match_recipe=hashlib.sha256((HERE/'match.py').read_bytes()+(HERE/'photo_matches.py').read_bytes()).hexdigest()
    needed=False
    for name,seed in [('wise_bed',117),('cityhall_mature',117),('martin_place',229)]:
        path=out/'matches'/(name+'.png');meta=path.with_suffix('.json')
        needed|=not current(path,Path(f'export/final/Site_{seed}.gltf'),a.samples) or not meta.exists() or json.loads(meta.read_text()).get('match_recipe_sha256')!=match_recipe
    if needed:subprocess.run(lock+blender+['--python',str(HERE/'match.py'),'--','--prepared','--render-only','--out',str(out/'matches'),'--width',str(a.width),'--samples',str(a.samples)],check=True)
    from kit.photo_match import compose
    compose('build/matched-cameras.json',out/'matches',out/'matches')

if __name__=='__main__':main()
