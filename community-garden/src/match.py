"""Three photo comparisons made only with freshly imported exported assets."""
import sys,json,argparse,math
from pathlib import Path
import bpy
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import geometry as Q
from render import setup,shot,render,context,bundle
from kit import photo_match


def references():
    folder=Path('build/photo-references');folder.mkdir(parents=True,exist_ok=True);rows={}
    # Frame neutrals: white cap, neutral gray apartment stucco,
    # light house siding. No clipping sky is used as a white point.
    regions={'oliver':(402,23,418,36),'wise':(790,275,804,284),'martin':(10,140,26,158)}
    for n,rect in regions.items():
        im=ImageOps.exif_transpose(Image.open(Path('refs')/(n+'.jpg'))).convert('RGB');im=im.resize((1024,round(im.height*1024/im.width)),Image.Resampling.LANCZOS)
        a=np.array(im,dtype=float)/255;lin=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
        x0,y0,x1,y1=rect;neutral=np.median(lin[y0:y1,x0:x1],axis=(0,1));gains=neutral.mean()/np.maximum(neutral,1e-5)
        balanced=lin*gains;srgb=np.where(balanced<=.0031308,balanced*12.92,1.055*np.maximum(balanced,0)**(1/2.4)-.055)
        Image.fromarray(np.uint8(np.clip(srgb,0,1)*255)).save(folder/(n+'.jpg'),quality=97)
        rows[n]=dict(neutral_rect_1024px=rect,linear_rgb_median=neutral.tolist(),linear_gains=gains.tolist(),description={'oliver':'white cap at upper centre; avoid clipped specular pixels','wise':'gray apartment stucco below window; assumed neutral, not a gray card','martin':'house siding at left; small JPEG-compressed neutral'}[n])
    (folder/'balance.json').write_text(json.dumps(rows,indent=2));return rows


def fixture(name):
    """Assemble comparison from exported library parts without changing vertices."""
    source=Path('export/checkpoint/CommunityGardenPieces.gltf');bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    roots={o.name:o for o in bpy.context.scene.objects if not o.parent};Q.palette();bed=roots['Raised4x8']
    keep=[bed]
    if name=='wise_bed':
        for sp,x,y,key in [('squash',-.22,-.74,'squash_2_0'),('herb',.15,-.1,'herb_2_0'),('tomato',0,.48,'tomato_2_0'),('pepper',.15,.91,'pepper_2_0')]:
            rt=Q.instance(roots[key],'Comparison '+sp,(x,y,.212),45,bed)
    else:
        for i in range(6):Q.instance(roots['lettuce_0_0'],'Young transplant',((i%2-.5)*.42,(i//2-1)*.65,.212),i*71,bed)
    for n,rt in roots.items():
        if rt not in keep:
            for ob in [*rt.children_recursive,rt]:bpy.data.objects.remove(ob,do_unlink=True)
    # Context geometry is original script-built library, not photographic data.
    if name=='wise_bed':
        p=dict(size=[18.288,21.336],archetype='city',bench=[-3.6,7]);context(p)
    else:
        rt=Q.root('Ground context');Q.box('Installation-day grass',(0,0,-.035),(80,80,.07),rt,'Lawn')
    return source


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/checkpoint/matches');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=40);p.add_argument('--calibrate-only',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    references();cal=Path('build/matched-cameras.json');photo_match.solve(str(HERE/'photo_matches.py'),cal)
    data=json.loads(cal.read_text());photo_match.verify(cal)
    if a.calibrate_only:return
    for name,row in data.items():
        v=dict(row['shot']);v['engine']='CYCLES';v['aspect']=1024/768
        if name=='wise_bed':v.update(sun_energy=2.0,sun_angle=6.0,sky_strength=.18)
        if name=='martin_place':render(229,out,a.width,a.samples,custom={name:v},with_context=True)
        else:
            source=fixture(name);cam=setup(a.samples);shot(cam,v,out/(name+'.png'),a.width)
            (out/(name+'.json')).write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),camera=v,engine='CYCLES',comparison='unmodified exported prototype assembly; photograph never an asset input'),indent=2))
    photo_match.compose(cal,out,out)
    notes=dict(bed_corners='WiseWords far-left/back corner is vegetation-occluded and weighted down; bed dimensions are inferred from a common 4x8 module, not surveyed.',
               construction='Oliver has people obscuring corners; along-edge phases are inferred and weighted down. This is a weaker construction/framing comparison, not a precision survey.',
               entrance='Martin sign/post rectangular corners are directly visible. Fictional sign text and site composition intentionally differ.')
    (out/'limitations.json').write_text(json.dumps(notes,indent=2))


if __name__=='__main__':main()
