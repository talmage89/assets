"""Whole-gun and action-detail strips, preserving each clip's real duration."""
import os
import sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from guns.common.strips import main
import interface

DETAIL_CLIPS=('Cycle','CycleLast','Chamber','Reload','ReloadSeveral','ReloadEmpty',
              'HammerSafe','HammerCock','Fire','FireLast','Inspect')

if __name__=='__main__':
    base=Path(__file__).resolve().parents[1]
    os.environ.pop('PD_LEVER_DETAIL_STRIP',None)
    main(base,interface,source='build/lever.glb',
         output='renders/checkpoint/strips',engine='BLENDER_WORKBENCH')
    os.environ['PD_LEVER_DETAIL_STRIP']='1'
    detail=SimpleNamespace(FPS=interface.FPS,CLIPS={n:interface.CLIPS[n] for n in DETAIL_CLIPS})
    main(base,detail,source='build/lever.glb',
         output='renders/checkpoint/detail-strips',engine='BLENDER_WORKBENCH')
