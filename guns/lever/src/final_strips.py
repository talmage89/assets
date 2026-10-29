"""All 37 delivered clips at their real timing with the delivered atlas."""
import sys,os,fcntl
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from guns.common.strips import main
import interface
if __name__=='__main__':
 os.environ['PD_LEVER_FINAL']='1'
 base=Path(__file__).resolve().parents[1]
 # One short batch holds the real shared GPU lease throughout. The common
 # renderer retains its own guard on a nested local lock, avoiding recursive
 # acquisition of the parent's lease and 37 separate shared-queue waits.
 shared=Path(os.environ['ASSETS_GPU_LOCK']);shared.parent.mkdir(parents=True,exist_ok=True)
 with shared.open('a') as lease:
  fcntl.flock(lease,fcntl.LOCK_EX)
  os.environ['ASSETS_GPU_LOCK']=str(base/'build/strip-inner.lock')
  main(base,interface,source='export/lever.glb',output='renders/final/strips',engine='BLENDER_EEVEE')
