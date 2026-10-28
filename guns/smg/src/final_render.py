"""Only exported baked GLBs may enter the finals."""
import sys,json
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
from guns.common.render import main
import final_shots,interface
from kit import weapon_presentation as presentation
base_samples=presentation.strip_samples
def member_samples(duration_frames,*,fps=60,rate=15):
 return base_samples(duration_frames,fps=fps,rate=60 if duration_frames<=15 else rate)
presentation.strip_samples=member_samples
if __name__=='__main__':
 # Keep current-source rows when regenerating a single inspected view.
 # Provenance review independently rejects any stale source hashes.
 output=Path(sys.argv[sys.argv.index('--out')+1])/'shots.json'
 previous=json.loads(output.read_text()) if output.exists() else {}
 main(final_shots,interface)
 current=json.loads(output.read_text());previous.update(current)
 output.write_text(json.dumps(previous,indent=2))
