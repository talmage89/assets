"""Real-speed GLB strips and timed playback, using the stable family tool."""
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]));sys.path.insert(0,str(BASE/'src'))
from guns.common.strips import main
import interface
if __name__=='__main__':
 main(BASE,interface,source='build/smg.glb')
 import json
 p=BASE/'renders/checkpoint/strips/timing.json';data=json.loads(p.read_text())
 for name,row in data.items():row['strip_rate_hz']=60 if interface.CLIPS[name]['frames']<=15 else 15
 p.write_text(json.dumps(data,indent=2))
