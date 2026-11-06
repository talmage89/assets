"""Exercise plan invariants, not implementation-shaped snapshots."""
import json
from pathlib import Path
from plan import generate,validate,REGIONS

def main():
 rows={}
 for region in REGIONS:
  for seed in range(1000):
   p=validate(generate(seed,region,4+seed%9))
   assert p==generate(seed,region,4+seed%9)
  rows[region]=1000
 Path('build').mkdir(exist_ok=True);Path('build/plan-check.json').write_text(json.dumps(dict(passed=True,plans=rows),indent=2)+'\n')
 print('PLAN PASS',sum(rows.values()),'deterministic plans; lot joins, heights, bounds')
if __name__=='__main__':main()
