"""Byte repeat proof for local glTF geometry and shared checkpoint images."""
import sys,json,hashlib,shutil
from pathlib import Path
def hashes(folder):return {str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.rglob('*')) if p.is_file()}
path=Path('build/repeat-before.json')
if sys.argv[1]=='snapshot':
    path.write_text(json.dumps(hashes(Path('export/lookdev')),indent=2))
    folder=Path('build/repeat');shutil.rmtree(folder,ignore_errors=True);(folder/'build').mkdir(parents=True)
    (folder/'build/context').symlink_to(Path('build/context').resolve(),target_is_directory=True)
    (folder/'textures').symlink_to(Path('textures').resolve(),target_is_directory=True)
else:
    before=json.loads(path.read_text());after=hashes(Path('build/repeat/export/lookdev'));different=[p for p in set(before)|set(after) if before.get(p)!=after.get(p)]
    preserved=hashes(Path('export/lookdev'))==before
    report=dict(passed=not different and preserved,files=len(after),different=different,original_exports_unchanged=preserved,scope='Isolated rebuild from a fresh Blender process, shared read-only context inputs; every glTF/BIN/image compared byte for byte');Path('build/repeat-check.json').write_text(json.dumps(report,indent=2));assert report['passed'],report;print('REPEAT PASS',len(after),'byte-identical files')
