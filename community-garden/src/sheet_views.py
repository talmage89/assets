"""Exported prototype catalogues with projected cells and measured dimensions.

Pieces use individual panel scales. Growth stages share a scale within each
species. All source meshes/maps remain unchanged; these are render transforms.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from render import setup,shot,bundle,RECIPE_SHA256
import geometry as Q
from kit.fonts import find_font
RECIPE=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
SPECIES=('tomato','pepper','squash','bean','corn','lettuce','kale','herb','sunflower','marigold','weed')
OFFSET=Vector((0,-26,32));UP=Vector((0,32,26)).normalized()


def points(root):
    return [ob.matrix_world@v.co for ob in [root,*root.children_recursive] if ob.type=='MESH' for v in ob.data.vertices]


def bounds(root):
    pp=points(root)
    xyz=[(min(p[a] for p in pp),max(p[a] for p in pp)) for a in range(3)]
    uv=[(min(p.x for p in pp),max(p.x for p in pp)),(min(p.dot(UP) for p in pp),max(p.dot(UP) for p in pp))]
    return xyz,uv


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/final');p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=96);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    source=Path('export/final/CommunityGardenPieces.gltf')
    for group in ('pieces','plants'):
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()));roots=[o for o in bpy.context.scene.objects if not o.parent];bpy.context.view_layer.update()
        Q.palette();cam=setup(a.samples);cells=[];labels=[]
        if group=='pieces':
            selected=sorted([r for r in roots if r.get('kind')!='plant'],key=lambda r:r.name)
            columns=5;rows=math.ceil(len(selected)/columns);cw,ch=3.4,3.3
            for j,root in enumerate(selected):
                xyz,uv=bounds(root);size=[hi-lo for lo,hi in xyz]
                scale=min(cw*.84/max(.001,uv[0][1]-uv[0][0]),ch*.66/max(.001,uv[1][1]-uv[1][0]))
                cells.append((root,j%columns,j//columns,scale))
                labels.append((j%columns,j//columns,root.name,' × '.join(f'{v:.2f}' for v in size)+' m'))
            title='Construction prototypes · individual panel scales · measured W × D × H'
        else:
            columns=9;rows=4;cw,ch=1.20,2.30;selected=[]
            for j,sp in enumerate(SPECIES):
                stages=[next(r for r in roots if r.name==f'{sp}_{stage}_0') for stage in range(3)]
                selected.extend(stages);bb=[bounds(r) for r in stages]
                scale=min(cw*.86/max(b[1][0][1]-b[1][0][0] for b in bb),ch*.67/max(b[1][1][1]-b[1][1][0] for b in bb))
                height=bb[2][0][2][1]-bb[2][0][2][0]
                for k,root in enumerate(stages):
                    column=(j%3)*3+k;row=j//3;cells.append((root,column,row,scale))
                    labels.append((column,row,('Seedling','Intermediate','Mature')[k],f'{sp} · {height:.2f} m mature' if k==1 else ''))
            title='Growth stages · common scale within each species · species panel scales differ'
        for root in roots:
            for ob in [root,*root.children_recursive]:ob.hide_render=root not in selected
        for root,column,row,scale in cells:
            root.scale*=scale;bpy.context.view_layer.update();xyz,uv=bounds(root);root.location.z-=xyz[2][0];bpy.context.view_layer.update();xyz,uv=bounds(root)
            u=(column+.5)*cw;v=-(row+.47)*ch
            root.location.x+=u-(uv[0][0]+uv[0][1])/2
            root.location.y+=(v-(uv[1][0]+uv[1][1])/2)/UP.y
        bpy.context.view_layer.update();span=columns*cw+.3;height=rows*ch+.55
        centre=Vector((columns*cw/2,-rows*ch/2/UP.y,0))
        floor=Q.root('Catalogue ground');Q.box('Neutral catalogue floor',(centre.x,centre.y,-.05),(span+70,height/UP.y+80,.08),floor,'Gravel')
        v=dict(location=tuple(centre+OFFSET),target=tuple(centre),ortho=span,aspect=span/height,exposure=0,sun_energy=4,sun_angle=5,sky_strength=.25,sun_direction=(-.4,.25,-1))
        path=out/(group+'.png');shot(cam,v,path,a.width)
        im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('Noto Sans'),max(14,a.width//100));small=ImageFont.truetype(find_font('Noto Sans'),max(12,a.width//120));px=a.width/span
        draw.rectangle((0,0,im.width,32),fill=(26,33,29));draw.text((12,6),title,font=font,fill='white')
        for column,row,name,dimensions in labels:
            x=(.15+(column+.5)*cw)*px;y=(.275+(row+.85)*ch)*px
            draw.text((x,y),name,font=font,anchor='mt',fill='white',stroke_width=2,stroke_fill=(20,25,20))
            if dimensions:draw.text((x,y+font.size+4),dimensions,font=small,anchor='mt',fill='white',stroke_width=2,stroke_fill=(20,25,20))
        im.save(path)
        path.with_suffix('.json').write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),render_script_sha256=RECIPE_SHA256,sheet_recipe_sha256=RECIPE,camera=v,engine='CYCLES',samples=a.samples,width=a.width,members=[r.name for r in selected],panel_scale='individual pieces; common stage scale within each species',source_dimensions_measured=True),indent=2))

if __name__=='__main__':main()
