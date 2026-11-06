"""Build absent original presentation exports in dependency order.

The legacy house exporters expect complete older families. Starting a cold
split build with SEEDS=51 leaks that override to its nested colonial make;
prebuilding older defaults avoids that without changing any house code/file.
"""
import subprocess
from pathlib import Path
from context import ensure
REPO=Path(__file__).resolve().parents[2]
steps=[('builder_colonial',[27,2,3,6,8,14],'Hearthfield-'),('ranch',list(range(11,17)),'HearthfieldRanch-'),('cape',list(range(31,37)),'HearthfieldCape-')]
for kind,seeds,prefix in steps:
    if all((REPO/'houses/export'/f'{prefix}{s}.gltf').exists() for s in seeds):continue
    log=Path('build/strip-look')/('context-'+kind+'.log');log.parent.mkdir(parents=True,exist_ok=True)
    with log.open('w') as f:subprocess.run(['make','-C',str(REPO/'houses'),'TYPE='+kind,'SEEDS='+','.join(map(str,seeds)),'export'],stdout=f,stderr=subprocess.STDOUT,check=True)
ensure(street=True)
