"""Four unique Main Street rows from the unchanged downtown generator.

Run separately in a fresh Blender. All generated files live under river/build;
the native baked surfaces are read-only inputs. No other delivery is rebuilt.
"""
import os
import sys
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
sys.path[:0]=[str(REPO/'downtown/src'),str(REPO)]
import bpy
from build import build_block


def main():
    out=(REPO/'river/build/town').resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'textures').mkdir(exist_ok=True)
    link=out/'textures/ship'
    if not link.exists():link.symlink_to(os.path.relpath(REPO/'downtown/textures/ship',link.parent),target_is_directory=True)
    os.chdir(out)
    rows=[]
    for seed in range(811,819):
        row=build_block(seed,'midwest',12,context=True)
        block=Path('build/context/blocks')/('midwest-'+str(seed))/'block.json'
        rows.append(dict(seed=seed,block=str(block),buildings=row['buildings']))
    Path('manifest.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()
