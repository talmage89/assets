"""Use the shared camera solver, retaining condition/crop uncertainty metadata."""
import argparse,json,runpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.photo_match import calibrate
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
results={}
for name,definition in runpy.run_path(str(Path(__file__).with_name('used_matches.py')))['MATCHES'].items():
    data=calibrate(definition);data['shot']['paint']=definition.get('paint','Carbon')
    for key in ['lens_status','calibration_note']:
        if key in definition:data[key]=definition[key]
    results[name]=data
    print(name,'estimated lens %.1f mm; native RMS %.2f px'%(data['shot']['lens'],data['residual_rms_pixels']))
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(results,indent=2))
