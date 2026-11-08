"""Native-size correction evidence from explicitly frozen pass-4 cameras."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def compare(folder):
    before=Path('renders/checkpoint/pass4');out=Path('renders/fixes');out.mkdir(parents=True,exist_ok=True)
    receipts=[];font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),24)
    rows=json.loads((folder/'provenance.json').read_text())
    baselines=[r for r in rows if r['shot'].startswith('baseline_')]
    if baselines:
        for row in baselines:
            stem=row['stem'];name=row['shot'][9:];current=next(r for r in rows if r['stem']==stem and r['shot']==name)
            matrix_delta=max(abs(x-y) for a,b in zip(row['camera_matrix_world'],current['camera_matrix_world']) for x,y in zip(a,b))
            assert matrix_delta<1e-6,(stem,name,'camera matrix changed',matrix_delta)
            assert row['camera_parameters']==current['camera_parameters'],(stem,name,'camera parameters changed')
            light_keys=('direction','sun_energy','sky_strength','exposure','angle_degrees','sky_saturation','camera_sky_strength','camera_sky_saturation')
            for key in light_keys:assert row['light'][key]==current['light'][key],(stem,name,'changed light',key)
            a=folder/stem/(row['shot']+'.png');b=folder/stem/(name+'.png')
            left=Image.open(a).convert('RGB');right=Image.open(b).convert('RGB');assert left.size==right.size and left.width>=800
            im=Image.new('RGB',(left.width*2,left.height+58),(232,233,226));im.paste(left,(0,58));im.paste(right,(left.width,58));d=ImageDraw.Draw(im)
            d.text((18,15),'Prior form checkpoint / same camera and light',font=font,fill=(25,30,25))
            d.text((left.width+18,15),'Current exported asset / same camera and light',font=font,fill=(25,30,25))
            path=out/(stem+'-'+name+'.jpg');im.save(path,quality=95,optimize=True)
            receipts.append(dict(path=str(path),panel_size=left.size,camera_equal=True,light_equal=True,
                                 comparison_frame='world',before=str(a),after=str(b),camera_matrix_world=row['camera_matrix_world'],
                                 measured_max_camera_matrix_delta=matrix_delta,matrix_tolerance=1e-6))
        (out/'cameras.json').write_text(json.dumps(receipts,indent=2));print('IDENTICAL CAMERA/LIGHT PAIRS',len(receipts));return
    for row in rows:
        if not row['shot'].startswith('before_'):continue
        name=row['shot'][7:];stem=row['stem'];ref=row['camera'].get('baseline_reference');source_stem=ref['stem'] if ref else stem
        a=(before/'matches'/source_stem/(name+'.png')) if ref else (before/stem/(name+'.png'));b=folder/stem/(row['shot']+'.png')
        old=next(q for q in json.loads((before/'provenance.json').read_text()) if q['stem']==source_stem and q['shot']==name)
        for key in ('location','target','lens','ortho','roll','aspect'):
            assert (ref['camera'] if ref else row['camera']).get(key)==old['camera'].get(key),(stem,key)
        left=Image.open(a).convert('RGB');right=Image.open(b).convert('RGB');assert left.size==right.size and left.width>=800
        im=Image.new('RGB',(left.width*2,left.height+58),(232,233,226));im.paste(left,(0,58));im.paste(right,(left.width,58));d=ImageDraw.Draw(im)
        d.text((18,15),f'{source_stem} / pass 4',font=font,fill=(25,30,25));d.text((left.width+18,15),'Current park / same module-local camera' if ref else 'Current export / identical camera',font=font,fill=(25,30,25))
        path=out/(stem+'-'+name+'.jpg');im.save(path,quality=95,optimize=True)
        receipts.append(dict(path=str(path),panel_size=left.size,camera_equal=True,comparison_frame='module-local' if ref else 'world',before=str(a),after=str(b),camera=row['camera']))
    (out/'cameras.json').write_text(json.dumps(receipts,indent=2));print('FROZEN CAMERA PAIRS',len(receipts))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);a=p.parse_args();compare(a.folder)
