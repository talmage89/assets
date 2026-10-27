"""Build optional main-library street props without changing their docs.

The initial completion run used full `make` in all five folders. Reproduction
needs their export and checks, not their unrelated studio documentation.
"""
import argparse,json,subprocess
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/context-props.json'));a=p.parse_args()
results={};a.out.parent.mkdir(parents=True,exist_ok=True)
for asset in ('fire-hydrant','mailbox','trash-cart','street-signs','street-light'):
    folder=Path('..')/asset;log=a.out.parent/('context-'+asset+'.log')
    if not (folder/'Makefile').exists():
        results[asset]=dict(returncode=1,reason='Library folder unavailable');continue
    with log.open('w') as out:
        result=subprocess.run(['make','-C',str(folder),'export','check'],stdout=out,stderr=subprocess.STDOUT)
    results[asset]=dict(returncode=result.returncode,log=str(log))
    print('CONTEXT',asset,'passed' if result.returncode==0 else 'unavailable; see '+str(log),flush=True)
a.out.write_text(json.dumps(results,indent=2))
