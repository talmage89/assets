"""One serialized construction/inspection worker; diagnostics still get views."""
import json
from pathlib import Path
import runpy
import sys
import traceback

HERE=Path(__file__).resolve().parent


def run(name,args=()):
    sys.argv=[str(HERE/name),'--',*args]
    runpy.run_path(str(HERE/name),run_name='__main__')


def main():
    run('build.py',('--out','build/ParkingGarage.blend'))
    failures=[]
    for script in ('check.py','motion_check.py'):
        try:run(script)
        except Exception:
            failure=traceback.format_exc();failures.append(failure);Path('build/check-failure.txt').write_text('\n'.join(failures));print(failure,flush=True)
    run('site.py')
    run('render.py',('--out','renders/pass3','--width','900','--samples','12','--shots','hero,above,aisle'))
    from matches import solve
    solve()
    run('render.py',('--out','renders/matches','--width','900','--samples','12','--matches'))
    from kit import photo_match
    photo_match.compose('build/matches/calibration.json','renders/matches','renders/matches')
    if failures:raise RuntimeError('Construction check failed; inspect build/check-failure.txt and the preview images')


if __name__=='__main__':main()
