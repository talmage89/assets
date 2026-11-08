"""Three photo comparisons made only with freshly imported exported assets."""
import sys,json,argparse,math,hashlib
from pathlib import Path
import bpy
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import geometry as Q
from render import setup,shot,render,context,bundle,RECIPE_SHA256
from kit import photo_match


def references():
    folder=Path('build/photo-references');folder.mkdir(parents=True,exist_ok=True);rows={}
    # Frame neutrals: white cap, neutral gray apartment stucco,
    # light house siding. No clipping sky is used as a white point.
    regions={'oliver':(402,23,418,36),'wise':(790,275,804,284),'martin':(10,140,26,158),'cityhall':(878,1018,910,1026)}
    for n,rect in regions.items():
        im=ImageOps.exif_transpose(Image.open(Path('refs')/(n+'.jpg'))).convert('RGB');im=im.resize((1024,round(im.height*1024/im.width)),Image.Resampling.LANCZOS)
        a=np.array(im,dtype=float)/255;lin=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
        x0,y0,x1,y1=rect;neutral=np.median(lin[y0:y1,x0:x1],axis=(0,1));gains=neutral.mean()/np.maximum(neutral,1e-5)
        balanced=lin*gains;srgb=np.where(balanced<=.0031308,balanced*12.92,1.055*np.maximum(balanced,0)**(1/2.4)-.055)
        Image.fromarray(np.uint8(np.clip(srgb,0,1)*255)).save(folder/(n+'.jpg'),quality=97)
        rows[n]=dict(neutral_rect_1024px=rect,linear_rgb_median=neutral.tolist(),linear_gains=gains.tolist(),description={'oliver':'white cap at upper centre; avoid clipped specular pixels','wise':'gray apartment stucco below window; assumed neutral, not a gray card','martin':'house siding at left; small JPEG-compressed neutral','cityhall':'gray weathered board cap on near bed, assumed neutral in shade'}[n])
    (folder/'balance.json').write_text(json.dumps(rows,indent=2));return rows


def fixture(name):
    """Fresh full exported site; no isolated bed or invented empty lawn."""
    seed={'wise_bed':117,'cityhall_mature':341,'martin_place':229}[name]
    source=Path(f'export/final/Site_{seed}.gltf')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    return source


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/checkpoint/matches');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=40);p.add_argument('--calibrate-only',action='store_true');p.add_argument('--prepared',action='store_true');p.add_argument('--render-only',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    cal=Path('build/matched-cameras.json')
    if not a.prepared:references();photo_match.solve(str(HERE/'photo_matches.py'),cal);photo_match.verify(cal)
    data=json.loads(cal.read_text())
    if a.calibrate_only:return
    for name,row in data.items():
        if name=='oliver_construction':continue
        v=dict(row['shot']);v['engine']='CYCLES';v['aspect']=1024/1365 if name=='cityhall_mature' else 1024/768
        if name in ('wise_bed','cityhall_mature'):v.update(sun_energy=3.0,sun_angle=20.0,sky_strength=.55,exposure=.05,overcast=True)
        if name=='cityhall_mature':v.update(overcast=False,sun_energy=7.5,sun_angle=2,sky_strength=.22,sun_direction=(-.6,.5,-.75),exposure=.10)
        if name=='martin_place':v.update(sky_strength=.22,exposure=.05)
        source=fixture(name);cam=setup(a.samples);shot(cam,v,out/(name+'.png'),a.width)
        (out/(name+'.json')).write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),render_script_sha256=RECIPE_SHA256,match_recipe_sha256=hashlib.sha256(Path(__file__).read_bytes()+(HERE/'photo_matches.py').read_bytes()).hexdigest(),camera=v,engine='CYCLES',samples=a.samples,comparison='entire delivered garden and neighborhood; photo landmarks on actual bed/cage or entry sign; no isolated staging'),indent=2))
    if not a.render_only:photo_match.compose(cal,out,out)
    notes=dict(bed_corners='WiseWords far-left/back corner is vegetation-occluded and weighted down; 4x8 dimensions are inferred, not surveyed. Compare the complete delivered city garden around tomato Plot10 with a mature mixed-crop garden: crop identities and surrounding architecture differ.',
               construction='Oliver has people obscuring corners; along-edge phases are inferred and weighted down. This is a weaker construction/framing comparison, not a precision survey.',
               entrance='Martin sign/post rectangular corners are directly visible. Fictional sign text and site composition intentionally differ.')
    (out/'limitations.json').write_text(json.dumps(notes,indent=2))


if __name__=='__main__':main()
