"""Build absent original-library presentation exports; preserve existing bytes."""
import json,subprocess
from pathlib import Path
from preserve import check,sha
REPO=Path(__file__).resolve().parents[2]
check();rows=[]
for folder,name,options in (('trees','RedMaple.glb',['SPECIES=maple']),('shrubs','Shrubs.glb',[])):
 source=REPO/folder/'export'/name
 if not source.exists():
  log=Path('build')/('context-'+folder+'.log');log.parent.mkdir(parents=True,exist_ok=True)
  with log.open('w') as f:subprocess.run(['make','-C',str(REPO/folder),*options,'export'],stdout=f,stderr=subprocess.STDOUT,check=True)
 rows.append(dict(source=str(source.relative_to(REPO)),sha256=sha(source)))
Path('build/context-sources.json').write_text(json.dumps(rows,indent=2));check()
