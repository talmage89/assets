"""Exact-surface material bake plus verified geometric normal projection.

The game skin already carries the dense subdivision parent's normal field.
Its procedural material channels can therefore bake on that exact surface.
Higher geometric detail is accepted only where independent partwise rays
show adequate correspondence; elsewhere the exact-surface shader normal wins.
"""
import argparse,hashlib,json,shutil,sys
from pathlib import Path
import bpy,numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'kit'))
from image_io import read_png,write_png


def main():
    p=argparse.ArgumentParser();p.add_argument('--low',required=True);p.add_argument('--game',required=True);p.add_argument('--material',required=True);p.add_argument('--geometry',required=True);p.add_argument('--projection',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    material=Path(a.material);geometry=Path(a.geometry);projection=json.loads(Path(a.projection).read_text())
    if projection['low_sha256']!=hashlib.sha256(Path(a.game).read_bytes()).hexdigest():raise ValueError('Stale projection correspondence')
    approved=[n for n,r in projection['parts'].items() if r['miss_area_fraction']<=.0001 and r['back_hit_area_fraction']<=.0001 and r['nearest_distance_max_m']<=.003]
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.low).resolve()))
    base=read_png(material/'T_AlderS240_Normal.png').astype(np.float32);high=read_png(geometry/'T_AlderS240_Normal.png').astype(np.float32)
    if base.shape!=high.shape:raise ValueError('Mismatched normal atlases')
    size=base.shape[0];mask=Image.new('L',(size,size),0);draw=ImageDraw.Draw(mask)
    for name in approved:
        ob=bpy.data.objects[name];ob.data.calc_loop_triangles();uv=ob.data.uv_layers['BakeUV']
        for triangle in ob.data.loop_triangles:
            draw.polygon([(float(uv.data[i].uv.x)*size,(1-float(uv.data[i].uv.y))*size) for i in triangle.loops],fill=255)
    # Reject reversed high-source texels even on an approved part. Direct
    # bake padding already surrounds each island; never dilate into a neighbor.
    chosen=(np.asarray(mask)>0)&(high[:,:,2]>=.5)
    base[chosen]=high[chosen];write_png(out/'T_AlderS240_Normal.png',base,16)
    for channel in ['BaseColor','ORM']:shutil.copyfile(material/('T_AlderS240_'+channel+'.png'),out/('T_AlderS240_'+channel+'.png'))
    exact=json.loads((material/'bake-report.json').read_text());geometric=json.loads((geometry/'bake-report.json').read_text())
    report=dict(method='Exact game-surface procedural channels; verified geometric normals where source correspondence passes',size=size,samples=exact['samples'],device=exact['device'],
        exact_surface=exact,geometric_source=geometric,normal_projection_policy=dict(max_miss_area_fraction=.0001,max_back_hit_area_fraction=.0001,max_nearest_distance_m=.003),
        approved_normal_parts=approved,approved_normal_atlas_fraction=float(chosen.mean()),game_sha256=projection['low_sha256'],high_sha256=projection['high_sha256'])
    (out/'bake-report.json').write_text(json.dumps(report,indent=2));print('S240_BAKE_MERGE',len(approved),'verified normal parts; exact RGB/ORM; projected atlas fraction',float(chosen.mean()))
if __name__=='__main__':main()
