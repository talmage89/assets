"""Gather independently generated checkpoints; never turns failures into passes."""
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def main():
    paths=[BASE/'build/model-check.json',BASE/'build/motion.json',BASE/'renders/seethrough/counts.json']+[BASE/f'build/delivery-{s}.json' for s in [101,102,103]]
    rows={str(p.relative_to(BASE)):json.loads(p.read_text())['passed'] for p in paths}
    before=BASE/'build/preservation-before.json'
    if before.exists():
        hashes=json.loads(before.read_text());unchanged=all((BASE.parent/p).exists() and hashlib.sha256((BASE.parent/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
        rows['existing_delivery_bytes']=unchanged
    result=dict(passed=all(rows.values()),checks=rows,scope='Form/construction checkpoint, quick baked maps; final look development remains outstanding')
    (BASE/'build/checkpoint-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if not result['passed']:raise SystemExit(1)
if __name__=='__main__':main()
