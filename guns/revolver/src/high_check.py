"""Dense crescent clearance under the same tolerance; serialization is separate."""
import json,sys
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W,motion
from contacts import measure
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/high.blend'))
arm=bpy.data.objects['RevolverArmature']
contacts=measure(arm)
clearance=motion.sweep_clips(arm,['Idle','CockHammer'],step_frames=.5,tolerance_m=.00020,allow=[])
result=dict(passed=contacts['passed'] and clearance['passed'],scope='dense sculpted hammer rest and complete cocking arc; all 48 actual source contacts; full game/import clip sweeps are separate',contacts=contacts,motion=clearance)
(BASE/'build/delivery/high-critical.json').write_text(json.dumps(result,indent=2))
assert result['passed'],result
print('DENSE HAMMER AND SOURCE CONTACTS PASS')
