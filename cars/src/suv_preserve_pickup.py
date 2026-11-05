"""Compare an existing pickup delivery with the accepted pre-SUV hash.

This never regenerates, edits or re-exports the pickup. A fresh clone can have
no pickup delivery; that is reported as unavailable, not a byte-identity proof.
"""
import argparse,hashlib,json
from pathlib import Path
EXPECTED='ec70cde87fbe50fb814cc14c900ee324e254711b5bfa5d3735aef166b146de5b'


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',default='export/AlderC150.glb');p.add_argument('--out',required=True);a=p.parse_args()
    path=Path(a.source);r=dict(available=path.exists(),scope='Existing accepted delivery only; no pickup regeneration or GPU rebake')
    if path.exists():
        data=path.read_bytes();digest=hashlib.sha256(data).hexdigest()
        r.update(passed=digest==EXPECTED,bytes=len(data),sha256=digest,accepted_sha256=EXPECTED)
    else:r.update(passed=None,status='No pickup GLB in this clone; byte comparison unavailable')
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,indent=2));print(json.dumps(r))
    if r['passed'] is False:raise AssertionError('Pickup delivery changed')

if __name__=='__main__':main()
