"""Extend matched horizontal fields with neutral margins, without changing a fit.

The reference crop is pasted unchanged into a wider comparison canvas. Camera
pose/roll and vertical FOV stay fixed; equivalent 36 mm focal length changes
with the wider horizontal field. No reference pixels enter modeling or textures.
"""
import argparse,json,copy
from pathlib import Path
from PIL import Image,ImageOps


def frame(source,out):
    source=Path(source);out=Path(out);folder=out.parent/'reference-frames';folder.mkdir(parents=True,exist_ok=True)
    data=copy.deepcopy(json.loads(source.read_text()))
    for name,row in data.items():
        im=ImageOps.exif_transpose(Image.open(row['photo'])).convert('RGB').crop(row['crop'])
        margin=round(im.width*.16);width=im.width+2*margin;factor=width/im.width
        canvas=Image.new('RGB',(width,im.height),(238,239,236));canvas.paste(im,(margin,0))
        photo=(folder/(name+'.png')).resolve();canvas.save(photo)
        row['unframed_lens_mm']=row['shot']['lens'];row['horizontal_frame_factor']=factor
        row['shot']['lens']/=factor;row['shot']['aspect']=width/im.height
        row['photo']=str(photo);row['crop']=[0,0,width,im.height]
        row['title']+=' / neutral study margins'
        for key in ['projected_pixels','measured_pixels']:
            row[key]=[[x+margin,y] for x,y in row[key]]
    out.write_text(json.dumps(data,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args();frame(a.source,a.out)
