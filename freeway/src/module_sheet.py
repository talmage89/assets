"""Individually framed Cycles views of every exported reusable module."""
import argparse,json,sys,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import render
from kit.fonts import find_font

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=3000);ap.add_argument('--out',default='renders/lookdev');ap.add_argument('--samples',type=int,default=24);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    data=json.loads(Path('build/modules.json').read_text());cols=3;cell=max(800,round(a.width/cols));height=round(cell*.82)
    sheet=Image.new('RGB',(cell*cols,height*math.ceil(len(data)/cols)),(30,35,31));d=ImageDraw.Draw(sheet);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),14)
    metadata={}
    for i,(name,row) in enumerate(data.items()):
        lo,hi=map(Vector,row['bounds']);center=(lo+hi)/2;extent=hi-lo;size=max(extent);direction=Vector((1.0,-1.5,1.05)).normalized()
        shot=dict(location=list(center+direction*max(2,size)*2.0),target=list(center),lens=45,aspect=1.45,
                  stage_floor=dict(size=max(200,size*10),location=[center.x,center.y,lo.z-.02]))
        result=render('export/modules/'+name+'.gltf',str(Path(a.out)/'modules'),cell,a.samples,'CYCLES',custom={name:shot})
        metadata[name]=result[name]
        im=Image.open(str(Path(a.out)/'modules'/(name+'.png'))).convert('RGB');im.thumbnail((cell-10,height-54));x=i%cols*cell+5;y=i//cols*height+5
        sheet.paste(im,(x+(cell-10-im.width)//2,y));d.text((x,y+height-48),name+' / '+str(row['triangles'])+' tris',font=font,fill=(226,235,219))
        d.text((x,y+height-29),'%.2f x %.2f x %.2f m'%tuple(extent),font=font,fill=(184,200,180))
    sheet.save(Path(a.out)/'modules.png')
    (Path(a.out)/'modules.json').write_text(json.dumps(dict(source='export/FreewayModules.gltf',bundle_sha256=__import__('external').bundle('export/FreewayModules.gltf'),engine='CYCLES',individual=metadata),indent=2))
if __name__=='__main__':main()
