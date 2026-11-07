"""Byte repeat proof for local glTF geometry and shared checkpoint images."""
import sys,json,hashlib,shutil
from pathlib import Path
def hashes(folder):
    result={str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.rglob('*')) if p.is_file()}
    embedded=folder.parent.parent/'build/embedded'
    for p in embedded.glob('*.glb'):result['embedded/'+p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    for p in folder.glob('*.gltf'):
        for row in json.loads(p.read_text()).get('images',[]):
            target=(p.parent/row['uri']).resolve();result['image:'+row['uri']]=hashlib.sha256(target.read_bytes()).hexdigest()
    return result
path=Path('build/repeat-before.json')
if sys.argv[1]=='snapshot':
    Path('build/repeat-check.json').write_text(json.dumps(dict(passed=False,status='incomplete',scope='Fresh procedural/bake/export repeat started; no successful comparison yet'),indent=2))
    path.write_text(json.dumps(hashes(Path('export/final')),indent=2))
    folder=Path('build/repeat');shutil.rmtree(folder,ignore_errors=True);(folder/'build').mkdir(parents=True)
    (folder/'build/context').symlink_to(Path('build/context').resolve(),target_is_directory=True)
    for name in ('ground','trees','fences'):
        shared=Path('build')/name;target=(Path('..')/name).resolve()
        if shared.exists():assert shared.is_symlink() and shared.resolve()==target,shared
        else:shared.symlink_to(target,target_is_directory=True)
    (folder/'textures').mkdir()
else:
    before=json.loads(path.read_text());after=hashes(Path('build/repeat/export/final'));different=[p for p in set(before)|set(after) if before.get(p)!=after.get(p)]
    preserved=hashes(Path('export/final'))==before
    report=dict(passed=not different and preserved,files=len(after),different=different,original_exports_unchanged=preserved,scope='Isolated procedural generation, fresh Cycles tile bake, filter and factory-startup geometry rebuild, shared read-only context inputs; every glTF/BIN/image compared byte for byte');Path('build/repeat-check.json').write_text(json.dumps(report,indent=2));assert report['passed'],report;print('REPEAT PASS',len(after),'byte-identical files')
