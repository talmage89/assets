"""Rebuild original fields and exported geometry; canonical bakes stay frozen.

GPU bake repeat is a separate tolerance-based operation, never claimed byte
deterministic. This checkpoint requires exact source and geometry identity.
"""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
from atlas_source import generate


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    Path('build/lookdev/repeat.json').unlink(missing_ok=True)
    source=Path('build/lookdev/atlas-source');repeat=Path('build/lookdev/repeat-source')
    generate(repeat,Path('build/lookdev/repeat-layout.json'))
    fields={p.name:digest(p) for p in source.glob('*.png')}
    assert all(digest(repeat/n)==h for n,h in fields.items())
    assert Path('build/lookdev/atlas-layout.json').read_bytes()==Path('build/lookdev/repeat-layout.json').read_bytes()
    roots=('export/form','export/lookdev','export/final','build/final-glb','textures/lookdev')
    files=[p for root in roots for p in Path(root).rglob('*') if p.is_file()]
    manifests=['form-sites','sites','modules','comparison-precast','comparison-harmon']
    manifests += [f'{kind}-{seed}' for kind in ('garage','actors','look','traffic') for seed in (101,202)]
    files += [Path('build/lookdev')/(name+'.json') for name in manifests]
    files.append(Path('build/final-package.json'))
    before={str(p):digest(p) for p in files}
    # Exact rebuilds must not invalidate the already reviewed render inputs.
    times={str(p):(p.stat().st_atime_ns,p.stat().st_mtime_ns) for p in files}
    for pattern in ('*.blend','*.json'):
        for p in Path('build/lookdev').glob(pattern):times[str(p)]=(p.stat().st_atime_ns,p.stat().st_mtime_ns)
    backup=Path('build/lookdev/repeat-original')
    for p in files:
        target=backup/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    with Path('build/lookdev/repeat-build.log').open('w') as log:
        for script in ('form_build','comparison_build','lookdev_build'):
            subprocess.run(['blender','-b','-t','2','--factory-startup','--python-exit-code','1','--python',f'src/{script}.py','--'],stdout=log,stderr=subprocess.STDOUT,check=True)
        subprocess.run(['python3','src/delivery_package.py'],stdout=log,stderr=subprocess.STDOUT,check=True)
    changed=[p for p,h in before.items() if digest(p)!=h]
    # Mixed sites carry native cars. Their garage/town nodes remain exact;
    # only car surfaces receive the owner's explicit tolerance exception.
    embedded=[];pairs=[]
    for p in files:
        if 'sites' in p.parts and p.suffix in ('.gltf','.bin','.glb'):
            embedded.append(str(p))
            if p.suffix=='.gltf':pairs.append([str(backup/p),str(p)])
    pairfile=Path('build/lookdev/embedded-repeat-pairs.json');pairfile.write_text(json.dumps(pairs)+'\n')
    with Path('build/lookdev/embedded-repeat.log').open('w') as log:
        subprocess.run(['blender','-t','2','-b','--factory-startup','--python-exit-code','1','--python','src/embedded_repeat.py','--',
            '--pairs',str(pairfile),'--out','build/lookdev/embedded-repeat.json'],stdout=log,stderr=subprocess.STDOUT,check=True)
    from repeat import compare_manifest
    for name in ('form-sites','sites','actors-101','actors-202','traffic-101','traffic-202'):
        p=Path('build/lookdev')/(name+'.json')
        if str(p) in changed:
            compare_manifest(json.loads((backup/p).read_text()),json.loads(p.read_text()))
            embedded.append(str(p))
    package=Path('build/final-package.json')
    if str(package) in changed:
        a=json.loads((backup/package).read_text());b=json.loads(package.read_text())
        for x,y in zip(a['files'],b['files']):
            if '/sites/' in x['gltf']:
                for key in ('gltf_sha256','bin_sha256','review_glb_sha256','review_glb_bytes'):x.pop(key);y.pop(key)
            assert x==y,('Final package changed beyond car sites',x['gltf'])
        embedded.append(str(package))
    changed=[p for p in changed if p not in embedded]
    if changed:
        Path('build/lookdev/repeat-failure.json').write_text(json.dumps(changed,indent=2)+'\n')
        # Failed verification must not silently invalidate reviewed exports.
        for p in files:shutil.copy2(backup/p,p)
    assert not changed,changed
    for p,stamp in times.items():os.utime(p,ns=stamp)
    report=dict(passed=True,exact_source_fields=len(fields),exact_export_and_manifest_files=len(before)-len(embedded),embedded_context_files=len(embedded),export_and_manifest_bytes=sum(Path(p).stat().st_size for p in before),
        source_scripts_sha256={str(p):digest(p) for p in sorted(Path('src').glob('*.py'))},
        texture_policy='Canonical 4096 GPU bake / 2048 maps unchanged. Repeats form construction, private comparison variants, town instancing, age, UV and export from accepted source blends. A fresh GPU bake is tested separately.')
    Path('build/lookdev/repeat.json').write_text(json.dumps(report,indent=2)+'\n');print('LOOK-DEV REPEAT PASS',report,flush=True)


if __name__=='__main__':main()
