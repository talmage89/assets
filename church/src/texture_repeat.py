"""Independent exact regeneration of the family's analytic shipped maps."""
import hashlib,json,subprocess,sys
from pathlib import Path


def main():
    stage=Path('build/texture-repeat');(stage/'build').mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(Path('src/textures.py').resolve())],cwd=stage,check=True)
    rows=[]
    for p in sorted((stage/'textures/ship').glob('*.png')):
        current=Path('textures/ship')/p.name
        same=p.read_bytes()==current.read_bytes()
        rows.append(dict(file=p.name,bytes=p.stat().st_size,exact=same,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    assert len(rows)==10 and all(r['exact'] for r in rows),rows
    Path('build/texture-repeat.json').write_text(json.dumps(dict(passed=True,method='Independent analytic regeneration; no GPU bake exists in this family',files=rows),indent=2))
    print('PASS',len(rows),'maps repeat byte for byte')


if __name__=='__main__':main()
