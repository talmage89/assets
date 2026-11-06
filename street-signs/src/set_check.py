"""The additional library audit is separate from the existing final sign gate."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'street-furniture/src'))
from check import audit
report=audit(Path('export/set/RoadSigns.gltf'),json.loads(Path('build/set/manifest.json').read_text()),True)
Path('build/set/check.json').write_text(json.dumps(report,indent=2));print('SIGN CHECKPOINT PASSED',len(report['rows']),'assemblies')
