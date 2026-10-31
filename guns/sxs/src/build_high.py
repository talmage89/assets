"""Assign field finishes to accepted dense surfaces, without changing geometry."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path[:0]=[str(ROOT),str(BASE/'src')]
import lookdev

def main():
    p=argparse.ArgumentParser();p.add_argument('--wear',type=float,default=1)
    p.add_argument('--out',default='build/delivery/high.blend');p.add_argument('--disable',default='')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/dense.blend'))
    records=lookdev.assign(a.wear,[s for s in a.disable.split(',') if s])
    out=BASE/a.out;out.parent.mkdir(parents=True,exist_ok=True)
    bpy.context.scene['stage']='Original procedural field finishes on accepted dense source'
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    (out.with_suffix('.json')).write_text(json.dumps(dict(wear=a.wear,disabled=a.disable,parts=records,
      source_sha256={name:hashlib.sha256((BASE/'src'/name).read_bytes()).hexdigest() for name in ('lookdev.py','build_high.py')},
      dense_sha256=hashlib.sha256((BASE/'build/delivery/dense.blend').read_bytes()).hexdigest()),indent=2))
if __name__=='__main__':main()
