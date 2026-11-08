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
    roots=('export/form','export/lookdev','textures/lookdev')
    files=[p for root in roots for p in Path(root).rglob('*') if p.is_file()]
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
    changed=[p for p,h in before.items() if digest(p)!=h]
    if changed:
        Path('build/lookdev/repeat-failure.json').write_text(json.dumps(changed,indent=2)+'\n')
        # Failed verification must not silently invalidate reviewed exports.
        for p in files:shutil.copy2(backup/p,p)
    assert not changed,changed
    for p,stamp in times.items():os.utime(p,ns=stamp)
    report=dict(passed=True,exact_source_fields=len(fields),exact_export_files=len(before),export_bytes=sum(Path(p).stat().st_size for p in before),
        source_scripts_sha256={str(p):digest(p) for p in sorted(Path('src').glob('*.py'))},
        texture_policy='Canonical 4096 GPU bake / 2048 maps unchanged. Repeats form construction, private comparison variants, town instancing, age, UV and export from accepted source blends. A fresh GPU bake is tested separately.')
    Path('build/lookdev/repeat.json').write_text(json.dumps(report,indent=2)+'\n');print('LOOK-DEV REPEAT PASS',report,flush=True)


if __name__=='__main__':main()
