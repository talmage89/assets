"""Baked GLB clips at real speed; Eevee preserves the delivered maps."""
import sys,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from guns.common.strips import main
import interface
# The shared strip tool invokes the member's render.py. Select its final mode
# explicitly through the member entry point without changing the common tool.
if __name__=='__main__':
 main(BASE,interface,source='export/smg.glb',output='renders/final/strips',engine='BLENDER_EEVEE',samples=16)
 path=BASE/'renders/final/strips/timing.json';rows=json.loads(path.read_text())
 for clip,row in rows.items():row['strip_rate_hz']=60 if interface.CLIPS[clip]['frames']<=15 else 15
 path.write_text(json.dumps(rows,indent=2))
