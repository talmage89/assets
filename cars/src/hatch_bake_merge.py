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
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.low).resolve()))
    detail_categories={'wheels','tires','brakes','interior','hinges','underbody'}
    approved=[n for n,r in projection['parts'].items() if r['miss_area_fraction']<=.0001 and r['back_hit_area_fraction']<=.0001 and r['nearest_distance_max_m']<=.003
              and bpy.data.objects[n].get('part_category') in detail_categories]
    base=read_png(material/'T_AlderH120_Normal.png').astype(np.float32);high=read_png(geometry/'T_AlderH120_Normal.png').astype(np.float32)
    if base.shape!=high.shape:raise ValueError('Mismatched normal atlases')
    size=base.shape[0];mask=Image.new('L',(size,size),0);draw=ImageDraw.Draw(mask)
    glass_mask=Image.new('L',(size,size),0);gd=ImageDraw.Draw(glass_mask)
    paint_mask=Image.new('L',(size,size),0);pd=ImageDraw.Draw(paint_mask)
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or 'asset_set' not in ob:continue
        ob.data.calc_loop_triangles();uv=ob.data.uv_layers['BakeUV']
        for triangle in ob.data.loop_triangles:
            mat=ob.data.materials[ob.data.polygons[triangle.polygon_index].material_index]
            coords=[(float(uv.data[i].uv.x)*size,(1-float(uv.data[i].uv.y))*size) for i in triangle.loops]
            if mat.get('vehicle_paint'):pd.polygon(coords,fill=255)
            if mat.get('vehicle_glass'):
                gd.polygon([(float(uv.data[i].uv.x)*size,(1-float(uv.data[i].uv.y))*size) for i in triangle.loops],fill=255)
    for name in approved:
        ob=bpy.data.objects[name];ob.data.calc_loop_triangles();uv=ob.data.uv_layers['BakeUV']
        for triangle in ob.data.loop_triangles:
            if name.startswith('Tire_'):
                center=sum((ob.data.vertices[i].co for i in triangle.vertices),__import__('mathutils').Vector())/3
                # Higher tread blocks belong on the crown. Preserve the direct
                # procedural lettering and sidewall normal field below it.
                if (center.y**2+center.z**2)**.5<.300:continue
            draw.polygon([(float(uv.data[i].uv.x)*size,(1-float(uv.data[i].uv.y))*size) for i in triangle.loops],fill=255)
    # Reject reversed high-source texels even on an approved part. Direct
    # bake padding already surrounds each island; never dilate into a neighbor.
    chosen=(np.asarray(mask.filter(ImageFilter.MinFilter(5)))>0)&(high[:,:,2]>=.5)
    base[chosen]=high[chosen]
    # Glazing has no authored microrelief. Micron paint peel/flake is below
    # this atlas' Nyquist limit; its filtered response belongs in roughness,
    # not point-sampled, millimeter-scale normal noise. Both retain the actual
    # authored surface normal field through a neutral map and chart padding.
    smooth=(np.asarray(glass_mask.filter(ImageFilter.MaxFilter(5)))>0)|(np.asarray(paint_mask.filter(ImageFilter.MaxFilter(5)))>0)
    base[smooth,:3]=(.5,.5,1)
    write_png(out/'T_AlderH120_Normal.png',base,16)
    for channel in ['BaseColor','ORM']:shutil.copyfile(material/('T_AlderH120_'+channel+'.png'),out/('T_AlderH120_'+channel+'.png'))
    exact=json.loads((material/'bake-report.json').read_text());geometric=json.loads((geometry/'bake-report.json').read_text())
    report=dict(method='Exact game-surface procedural channels; verified geometric normals where source correspondence passes',size=size,samples=exact['samples'],device=exact['device'],
        exact_surface=exact,geometric_source=geometric,normal_projection_policy=dict(max_miss_area_fraction=.0001,max_back_hit_area_fraction=.0001,max_nearest_distance_m=.003),
        smooth_paint_normal_texels=int(np.count_nonzero(np.asarray(paint_mask))),smooth_glass_normal_texels=int(np.count_nonzero(np.asarray(glass_mask))),paint_normal_policy='Unresolved micron peel/flake filtered into roughness; Paint and Glass export normal scale zero to preserve authored normals without 8-bit neutral-map deflection',
        approved_normal_parts=approved,approved_normal_atlas_fraction=float(chosen.mean()),game_sha256=projection['low_sha256'],high_sha256=projection['high_sha256'])
    (out/'bake-report.json').write_text(json.dumps(report,indent=2));print('H120_BAKE_MERGE',len(approved),'verified normal parts; exact RGB/ORM; projected atlas fraction',float(chosen.mean()))
if __name__=='__main__':main()
