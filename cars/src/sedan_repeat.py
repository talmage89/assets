"""Compare two independently generated sedan sources, without blend-byte claims."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from compare_pickup import capture


def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);before=capture(Path(a.before));after=capture(Path(a.after));changes=[]
    if before.keys()!=after.keys():changes.append('Object set')
    for name,row in before.items():
        if name not in after:continue
        for key,value in row.items():
            other=after[name][key];same=np.array_equal(value,other) if isinstance(value,np.ndarray) else value==other
            if not same:changes.append(name+' / '+key)
    report=dict(passed=not changes,objects=len(before),meshes=sum(r['type']=='MESH' for r in before.values()),changes=changes,
        scope='Independent master/sill and detail regeneration: exact vertices, polygons, corner normals, transforms, parents and material assignments; not a repeated GPU bake')
    Path(a.out).write_text(json.dumps(report,indent=2));print('S240_REPEAT',report)
    if changes:raise AssertionError('Independent regeneration differs')
if __name__=='__main__':main()
