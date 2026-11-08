"""One shared-GPU turn for source look probes and the dense-mold atlas bake.

Run through kit/with_gpu.sh after the CPU model, motion and UV checks.
No export, documentation or CPU build runs while this wrapper holds the GPU.
"""
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))

def main():
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1000)
    p.add_argument('--samples',type=int,default=24);p.add_argument('--size',type=int,default=4096)
    p.add_argument('--bake-samples',type=int,default=12)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);base=HERE.parent
    from render import render
    render(argparse.Namespace(source=str(base/'build/bus-101.blend'),
        out=str(base/'renders/round2-source-pass3'),shots='side,aisle,aisle_daylight,front_detail,interior',
        width=a.width,samples=a.samples,engine='CYCLES',school=None,calibration=None))
    import bake
    old=sys.argv
    try:
        sys.argv=[old[0],'--','--source',str(base/'build/finalized.blend'),
            '--out',str(base/'textures/4k'),'--size',str(a.size),'--samples',str(a.bake_samples)]
        bake.main()
    finally:sys.argv=old

if __name__=='__main__':main()
