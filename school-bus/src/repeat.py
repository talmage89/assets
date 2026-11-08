"""Regenerate deterministic sources, packing and all three deliveries exactly.

GPU bakes are independent stochastic inputs checked by texture_repeat.py;
Blender container timestamps and sampled render noise are excluded.
"""
import argparse,hashlib,json,os,shlex,shutil,subprocess
from pathlib import Path

def snapshot():
    files=list(Path('export').glob('C75-*.*'))+list(Path('export/shared').glob('*.png'))
    files+=list(Path('build/markings').glob('*.png'))+list(Path('textures/2k').glob('*.png'))
    files+=[Path('build/bus-101.counts.json')]
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--blender',default='blender -t 4');a=p.parse_args()
    bp=shlex.split(a.blender)+['-b','--factory-startup','--python-exit-code','1']
    old=snapshot()
    reference=Path('build/repeat-reference');reference.mkdir(exist_ok=True)
    for name in old:
        target=reference/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(name,target)
    cache=[Path(n) for n in old]+[Path('build')/n for n in [
        'bus-101.blend','prepared.blend','finalized.blend','uv.json','export-source.blend']]
    cache+=list(Path('build').glob('export-*.json'))+list(Path('build').glob('export-*.blend'))
    times={p:(p.stat().st_atime_ns,p.stat().st_mtime_ns) for p in cache if p.exists()}
    containers=Path('build/repeat-containers');containers.mkdir(exist_ok=True)
    saved={p:containers/p.name for p in times if p.suffix=='.blend'}
    for source,target in saved.items():shutil.copy2(source,target)
    commands=[['python3','src/markings.py','build/markings']]
    stages=[('src/build.py',['--seed','101','--out','build/bus-101.blend']),
            ('../cars/src/prepare_bake.py',['--source','build/bus-101.blend','--out','build/prepared.blend']),
            ('src/finalize.py',['--source','build/prepared.blend','--out','build/finalized.blend',
              '--config','src/config.py','--report','build/uv.json','--size','2048',
              '--target-density','300','--margin','.0012'])]
    stages += [('src/export.py',['--source','build/finalized.blend','--textures','textures/2k',
               '--asset','SchoolBus','--out',f'export/C75-{seed}.glb','--report',f'build/export-{seed}.json',
               '--config','src/config.py','--variant',str(seed)]) for seed in [101,102,103]]
    commands += [bp+['--python',script,'--']+args for script,args in stages]
    with Path('build/repeat.log').open('w') as log:
        for command in commands:
            print('REPEAT',shlex.join(command),flush=True)
            subprocess.run(command,check=True,stdout=log,stderr=subprocess.STDOUT)
    new=snapshot();changed=sorted(p for p in old.keys()|new.keys() if old.get(p)!=new.get(p))
    result=dict(passed=not changed,changed=changed,files=new,reference_files=old,reference_root=str(reference),
                scope='Exact independent source-counts, generated marking PNGs, re-packed/re-exported GLB/glTF/BIN and shared PNG bytes. GPU rebakes and Blender timestamped containers excluded.')
    Path('build/repeat.json').write_text(json.dumps(result,indent=2))
    if changed:raise SystemExit('Non-identical deterministic files: '+', '.join(changed))
    # Source-photo receipts hash the authoring containers too. Their timestamps
    # are intentionally outside byte determinism; keep the already reviewed
    # canonical containers once the independent export comparison has passed.
    for target,source in saved.items():shutil.copy2(source,target)
    # Same canonical data, freshly rebuilt and compared. Preserve Make's
    # known-good dependency times so this CPU proof does not request a rebake.
    for path,ns in times.items():os.utime(path,ns=ns)
    print('REPEAT PASS',len(new),'files',flush=True)

if __name__=='__main__':main()
