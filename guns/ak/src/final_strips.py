"""Real-duration strips and playback, with native samples for short cycles."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from guns.common.strips import main
import interface
if __name__=='__main__':
 import json
 base=Path(__file__).resolve().parents[1]
 main(base,interface,source='export/ak.glb',output='renders/final/strips',engine='BLENDER_EEVEE',samples=16)
 path=base/'renders/final/strips/timing.json';data=json.loads(path.read_text())
 for name,row in data.items():row['strip_rate_hz']=60 if interface.CLIPS[name]['frames']<=12 else 15
 path.write_text(json.dumps(data,indent=2))
