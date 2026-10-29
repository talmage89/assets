"""All 37 delivered clips at their real timing with the delivered atlas."""
import sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from guns.common.strips import main
import interface
if __name__=='__main__':
 os.environ['PD_LEVER_FINAL']='1'
 main(Path(__file__).resolve().parents[1],interface,source='export/lever.glb',
      output='renders/final/strips',engine='BLENDER_EEVEE')
