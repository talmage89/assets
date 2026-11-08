"""A single shared-lock turn for the front repair and source look probes."""
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))

def main():
    from render import render
    p=argparse.ArgumentParser();p.add_argument('--source',required=True)
    p.add_argument('--out',required=True);p.add_argument('--front-step2',action='store_true')
    p.add_argument('--width',type=int,default=1000);p.add_argument('--samples',type=int,default=24)
    p.add_argument('--engine',default='CYCLES',choices=['CYCLES','BLENDER_EEVEE'])
    p.add_argument('--shots',default='front_detail,side,interior,aisle')
    p.add_argument('--school');p.add_argument('--matches',action='store_true')
    p.add_argument('--bake',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.front_step2:
        import form_preview
        old=sys.argv
        try:
            sys.argv=[old[0],'--','--source',str(HERE.parent/'build/front-step2.blend'),
                      '--out',str(HERE.parent/'renders/round2-front-step2')]
            form_preview.main()
        finally:sys.argv=old
    render(argparse.Namespace(source=a.source,out=a.out,shots=a.shots,
                              width=a.width,samples=a.samples,engine=a.engine,school=a.school,calibration=None))
    if a.matches:
        import render_matches
        old=sys.argv
        try:
            sys.argv=[old[0],'--','--width',str(a.width),'--samples',str(a.samples)]
            render_matches.main()
        finally:sys.argv=old
    if a.bake:
        import bake
        old=sys.argv
        try:
            sys.argv=[old[0],'--','--source',str(HERE.parent/'build/finalized.blend'),
                      '--out',str(HERE.parent/'textures/4k'),'--size','4096','--samples','12']
            bake.main()
        finally:sys.argv=old

if __name__=='__main__':main()
