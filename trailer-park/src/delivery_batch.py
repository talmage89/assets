"""Additional serial render sets under the caller's single GPU lock."""
import os,sys
from pathlib import Path


def extra(main,args):
    assert os.environ.get('ASSETS_GPU_HELD')=='1'
    previous=sys.argv[:];source=args.out.parent/'source'
    try:
        sys.argv=['render.py','--','--out',str(source),'--width',str(args.width),'--samples',str(args.samples),
                  '--only','Park-101,Park-202','--shots','none','--cameras',str(args.cameras),'--source-finish']
        main()
    finally:sys.argv=previous
    from age_baseline import render_before,ASSET
    render_before(ASSET/'build/age-baseline/repo/trailer-park',args.out/'provenance.json',args.out.parent/'age-before',args.width,args.samples)
