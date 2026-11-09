"""Byte identity of pre-existing original deliveries. No source rewriting."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'river/build/preservation.json'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def capture():
    rows={}
    for folder in ROOT.iterdir():
        if not folder.is_dir() or folder.name in ('river','build','.git'):continue
        for sub in ('export','textures','docs'):
            for p in (folder/sub).rglob('*'):
                if p.is_file():rows[str(p.relative_to(ROOT))]=sha(p)
    OUT.write_text(json.dumps(rows,indent=2)+'\n');print('PRESERVE_CAPTURE',len(rows))


def check():
    rows=json.loads(OUT.read_text());bad=[p for p,h in rows.items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
    if bad:raise ValueError(('Changed existing delivery',bad))
    print('PRESERVE_PASS',len(rows));return len(rows)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--capture',action='store_true');a=ap.parse_args()
    capture() if a.capture else check()
