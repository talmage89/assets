"""GLB-only final studio entry point."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
from guns.common.render import main
from kit import weapon_presentation as P
import interface,final_shots
base_samples=P.strip_samples
def samples(duration_frames,*,fps=60,rate=15):
 return base_samples(duration_frames,fps=fps,rate=60 if duration_frames<=12 else rate)
P.strip_samples=samples
if __name__=='__main__':main(final_shots,interface)
