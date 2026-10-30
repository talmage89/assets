"""Standalone checkpoint views, all loaded from their inspection GLBs."""
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path[:0]=[str(ROOT),str(BASE/'src')]
from guns.common.render import main
import shots,interface
for name in ('box_loaded','box_empty','cartridge','case','link'):
 sys.argv=['render_extra.py','--','--source',str(BASE/'build'/f'{name}.glb'),
  '--out',str(BASE/'renders/checkpoint/detachables'/name),'--shots',name,'--width','900','--samples','32']
 main(shots,interface)
