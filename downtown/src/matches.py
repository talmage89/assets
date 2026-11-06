"""The kit's camera solver, plus a family/region routing field."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.photo_match import calibrate
from photo_matches import MATCHES
out={name:dict(**calibrate(m),region=m['region']) for name,m in MATCHES.items()}
Path('build/cameras.json').write_text(json.dumps(out,indent=2)+'\n')
for n,d in out.items():print('CAMERA',n,'lens',round(d['shot']['lens'],2),'RMS px',round(d['residual_rms_pixels'],2))
