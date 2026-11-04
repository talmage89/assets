"""Read-only byte comparison of all three accepted house deliveries."""
import hashlib,json
from pathlib import Path


def reference():
    accepted=json.loads(Path('src/split_legacy_hashes.json').read_text())
    cold=Path('build/split/delivery/cold-legacy-baseline.json')
    if not cold.exists():return accepted,'accepted handoff',True
    record=json.loads(cold.read_text());assert set(record['sha256'])==set(accepted)
    return record['sha256'],'fresh-clone rebuild',record['sha256']==accepted


def check():
    files,baseline,handoff=reference()
    changed=[name for name,sha in files.items() if not Path(name).is_file() or hashlib.sha256(Path(name).read_bytes()).hexdigest()!=sha]
    assert not changed,changed
    result=dict(passed=True,files=len(files),changed=changed,baseline=baseline,accepted_handoff_bytes=handoff,sha256=files)
    out=Path('build/split/delivery/preserved.json');out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2))
    print('SPLIT_PRESERVED',len(files),baseline,'export/map/docs files byte-identical')
    return result


if __name__=='__main__':check()
