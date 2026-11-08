"""Stable Make invalidation without touching identical parameter files."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--width',type=int,required=True);p.add_argument('--samples',type=int,required=True);a=p.parse_args()
assert a.width>=800 and a.samples>0
dest=Path('build/lookdev/render-parameters.json');text=json.dumps(vars(a),sort_keys=True)+'\n'
if not dest.exists() or dest.read_text()!=text:dest.write_text(text)
