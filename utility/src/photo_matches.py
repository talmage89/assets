"""Type comparisons: measured photo pixels, estimated original street cameras.

Photographic poles are not surveyed. 40-ft poles / typical level grade set the
working scale; absolute camera distance and lens remain estimates. No private
home plan or image is traced into any asset.
"""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]


def meta(seed):return json.loads(Path(f'build/street-{seed}.json').read_text())


a=meta(104);b=meta(101)
def pole(m,i,key):return m['sockets']['P'+str(i)][key]
def base(m,i):return m['plan']['poles'][i]['location']
def anchor(world,pixel,weight=1):return dict(world=world,pixel=pixel,weight=weight)
MATCHES=dict(
 nc_street=dict(seed=104,title='Residential NC / vertical three-phase construction, 2009',photo='refs/residential-a.jpg',crop=(0,0,1074,484),
   location=(8,-6,1.85),target=(-3,85,5.5),lens=35,lens_bounds_mm=(25,65),camera_height_m=(1.85,.10),
   landmarks=[anchor(base(a,1),(281,280),2),anchor(pole(a,1,'Primary_A'),(272,127),2),
      anchor(pole(a,1,'Primary_B'),(267,140)),anchor(pole(a,1,'Primary_C'),(280,155)),
      anchor(pole(a,1,'Neutral'),(280,179)),anchor(base(a,2),(300,264)),
      anchor(pole(a,2,'Primary_A'),(294,171)),anchor(pole(a,3,'Primary_A'),(307,198))]),
 md_street=dict(seed=101,title='Residential MD / maintained older distribution equipment',photo='refs/residential-b.jpg',crop=(0,0,2560,1920),
   location=(15,54,1.85),target=(-5,42,5.5),lens=30,lens_bounds_mm=(25,50),camera_height_m=(1.85,.15),
   landmarks=[anchor(base(b,1),(1110,1355),2),anchor(pole(b,1,'Primary_A'),(1058,252),2),
      anchor(pole(b,1,'Primary_C'),(977,228)),anchor(pole(b,1,'Primary_B'),(1112,318))],
   held_out=[anchor(pole(b,1,'Neutral'),(1074,493)),anchor(pole(b,1,'CommStrand'),(1086,710))]),
)


if __name__=='__main__':
    from kit.photo_match import solve
    out=sys.argv[1] if len(sys.argv)>1 else 'build/matched-cameras.json'
    solve(__file__,out);results=json.loads(Path(out).read_text())
    for name,row in results.items():
        row['seed']=MATCHES[name]['seed']
        if MATCHES[name].get('held_out'):
            import numpy as np,math
            from kit.photo_match import project
            shot=row['shot'];delta=np.array(shot['target'])-np.array(shot['location'])
            params=[math.atan2(delta[1],delta[0]),math.atan2(delta[2],np.linalg.norm(delta[:2])),*shot['location'],math.log(shot['lens']),shot['roll']]
            anchors=MATCHES[name]['held_out'];uv,_,_=project(params,np.array([a['world'] for a in anchors]),2560,1920)
            row['held_out_space_residuals_pixels']=np.linalg.norm(uv-np.array([a['pixel'] for a in anchors]),axis=1).tolist()
    Path(out).write_text(json.dumps(results,indent=2))
