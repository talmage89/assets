"""Compare an independent H120 detail regeneration with the reviewed source."""
import argparse,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from compare_pickup import capture

def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);before=capture(Path(a.before));after=capture(Path(a.after));changes=[]
    if before.keys()!=after.keys():changes.append('object set')
    for name,row in before.items():
        if name not in after:continue
        for key,value in row.items():
            other=after[name][key]
            if not (np.array_equal(value,other) if isinstance(value,np.ndarray) else value==other):changes.append(name+'/'+key)
    report=dict(passed=not changes,objects=len(before),meshes=sum(r['type']=='MESH' for r in before.values()),changes=changes,
        scope='Independent source regeneration: transforms, hierarchy, vertices, faces, split normals and material names')
    Path(a.out).write_text(json.dumps(report,indent=2));print('H120_REPEAT',report)
    if changes:raise AssertionError(changes)
if __name__=='__main__':main()
