"""Use the measured form cameras with neutral-balanced comparison images."""
import sys,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.photo_match import calibrate
from photo_matches import MATCHES
from white_balance import build
balanced=build();rows={}
for name in ('right_photo','left_photo','locked_photo','trigger_photo'):
 definition=dict(MATCHES[name]);definition['photo']=balanced[Path(definition['photo']).name]['output']
 rows[name]=calibrate(definition)
# A second locked view of the same daylight-issued gun supplies wear comparison.
(BASE/'build/cameras.json').write_text(json.dumps(rows,indent=2))
