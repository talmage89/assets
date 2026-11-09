"""Generate existing library source forms inside downtown's ignored build only."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from kit.blender_command import with_threads
CASES=(('pickup','cars/src/build.py',['--quality','game','--form-only']),('crossover','cars/src/suv_build.py',['--quality','game']),('hatchback','cars/src/hatch_build.py',['--quality','game']),('light','street-light/src/build.py',['--quality','game']),('maple','trees/src/build.py',['--quality','game','--species','maple']),('house','houses/src/build.py',['--seed','27','--no-export']))
def ensure():
 folder=Path('build/context');folder.mkdir(parents=True,exist_ok=True);rows=[]
 for name,script,args in CASES:
  dest=folder/(name+'.blend');log=folder/(name+'.log')
  if name in ('pickup','crossover','hatchback'):
   script='downtown/src/context_build.py';args=['--kind',name]
  recipe=hashlib.sha256((ROOT/'downtown/src/context_build.py').read_bytes() if name in ('pickup','crossover','hatchback') else (ROOT/script).read_bytes()).hexdigest()
  if name in ('pickup','crossover','hatchback'):recipe=hashlib.sha256((recipe+' threads=1').encode()).hexdigest()
  receipt=dest.with_suffix('.recipe')
  if not dest.exists() or not receipt.exists() or receipt.read_text()!=recipe:
   command=[str(ROOT/'downtown/src/blender.sh'),'-b','--factory-startup','--python-exit-code','1','--python',str(ROOT/script),'--',*args,'--out',str(dest.resolve())]
   if name in ('pickup','crossover','hatchback'):command=with_threads(command,1)
   with log.open('w') as out:subprocess.run(command,stdout=out,stderr=subprocess.STDOUT,check=True,cwd=ROOT/'downtown')
   receipt.write_text(recipe)
  rows.append(dict(name=name,path=str(dest),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),stage='existing original family source with procedural materials; presentation only'))
 (folder/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n');print('CONTEXT ready',len(rows))
if __name__=='__main__':ensure()
