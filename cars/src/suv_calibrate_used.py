"""Shared kit camera solver with the SUV's explicit near-side/paint metadata."""
import argparse,json,sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[2]),str(Path(__file__).resolve().parent)]
from kit.photo_match import calibrate
from suv_used_matches import MATCHES


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);a=parser.parse_args()
    result={}
    for name,match in MATCHES.items():
        data=calibrate(match);data['shot']['paint']=match['paint']
        camera=data['shot']['location']
        if camera[0]<=0 or camera[1]*(1 if name=='used_rear' else -1)<=0:
            raise ValueError('Camera fitted on the hidden-wheel side: '+name)
        data['pick_uncertainty_preview_px']=4
        data['scope']='Chassis registration and disclosed height/lens priors; body silhouettes remain holdouts'
        result[name]=data
        print(name, 'RMS',data['residual_rms_pixels'],'lens',data['shot']['lens'],'camera',camera)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2))

if __name__=='__main__':main()
