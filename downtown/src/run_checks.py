"""Serial fresh-process checks under one inherited shared lock."""
import subprocess,sys
from pathlib import Path
for script in ('check.py','check_resources.py','check_charts.py'):
 log=Path('build')/(script[:-3]+'.log')
 with log.open('w') as out:
  result=subprocess.run(['blender','-b','--factory-startup','--python-exit-code','1','--python','src/'+script],stdout=out,stderr=subprocess.STDOUT)
 lines=log.read_text().splitlines()
 print('\n'.join(lines[-8:]),flush=True)
 if result.returncode:raise SystemExit(result.returncode)
subprocess.run([sys.executable,'src/check_textures.py'],check=True)
