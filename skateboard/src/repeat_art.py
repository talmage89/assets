"""Independent original-field regeneration, compared byte for byte."""
import hashlib,json,subprocess
from pathlib import Path
parameters=dict(field.split('=',1) for field in Path('build/parameters.txt').read_text().split())
out=Path('build/repeat-art');subprocess.run(['python3','src/graphics.py','--out',str(out),'--seed',parameters['seed']],check=True)
result={}
for expected in sorted(Path('build/art').glob('*.png')):
    actual=out/expected.name
    assert expected.read_bytes()==actual.read_bytes(),'Source field differs: '+expected.name
    result[expected.name]=hashlib.sha256(actual.read_bytes()).hexdigest()
Path('build/repeat-art.json').write_text(json.dumps(result,indent=2));print('Byte-identical independently generated source images:',len(result))
