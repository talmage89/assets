"""Exact independent source-array comparison; binary blend identity is irrelevant."""
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from compare_pickup import capture

def main():
    parser=argparse.ArgumentParser()
    for name in ['source','repeat','out']:parser.add_argument('--'+name,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    before,after=[capture(Path(p).resolve()) for p in [args.source,args.repeat]]
    changes=[]
    if before.keys()!=after.keys():changes.append('Object set')
    for name,row in before.items():
        if name not in after:continue
        for key,value in row.items():
            equal=np.array_equal(value,after[name][key]) if isinstance(value,np.ndarray) else value==after[name][key]
            if not equal:changes.append(name+' / '+key)
    report=dict(passed=not changes,source_objects=len(before),source_meshes=sum(r['type']=='MESH' for r in before.values()),changes=changes,
        scope='Exact positions, polygons, corner normals, matrices, parents and material names from independent one-thread builds; no binary blend identity claim')
    Path(args.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    if changes:raise AssertionError(changes)

if __name__=='__main__':main()
