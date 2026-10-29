"""Family renderer entry point; every checkpoint beauty loads the exported GLB."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
from guns.common.render import main
from kit import weapon_presentation as P
import interface,shots
if any('/export/' in arg or arg.startswith('export/') for arg in sys.argv):
 import final_shots as shots
base_samples=P.strip_samples
def samples(duration_frames,*,fps=60,rate=15):
 return base_samples(duration_frames,fps=fps,rate=60 if duration_frames<=12 else rate)
P.strip_samples=samples
if __name__=='__main__':main(shots,interface)
