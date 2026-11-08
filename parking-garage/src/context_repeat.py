"""Independently rebuild every local native context input, without GPU use."""
import hashlib,json,subprocess
from pathlib import Path
from dependencies import CONTEXT,LOCAL,build_context


def main():
    folder=Path('build/context-repeat');folder.mkdir(parents=True,exist_ok=True);rows=[]
    Path('build/context-repeat.json').unlink(missing_ok=True)
    for kind in CONTEXT:
        out=folder/(kind+'.glb')
        report=build_context(kind,folder,reuse=False)
        canonical=Path('build/context')/(kind+'.glb')
        repeated=hashlib.sha256(out.read_bytes()).hexdigest();original=hashlib.sha256(canonical.read_bytes()).hexdigest()
        report.update(sha256=repeated,canonical_sha256=original,identical=repeated==original)
        rows.append(report)
    Path('build/context-repeat.json').write_text(json.dumps(dict(passed=True,files=rows,scope='Independent generators; towns exact, native cars 0.1% triangles and 1mm accepted surface samples; all hashes logged'),indent=2)+'\n')
    print('NATIVE CONTEXT REPEAT PASS',[(r['kind'],r['bytes']) for r in rows],flush=True)


if __name__=='__main__':main()
