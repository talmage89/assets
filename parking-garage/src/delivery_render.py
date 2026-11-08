"""One serial render lease for final exported views, pieces and photo pairs."""
import argparse,json,runpy,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from render import render_shot
from light_review import lighting


def run(script,args):
    sys.argv=[str(HERE/script),'--',*args];runpy.run_path(str(HERE/script),run_name='__main__')


def pieces(folder,samples):
    from PIL import Image,ImageDraw,ImageFont
    from kit.fonts import find_font
    inventory=json.loads(Path('build/lookdev/modules.json').read_text());panels=[];receipts=[]
    outward=Vector((-1.3,-1.8,1.0)).normalized();rotation=(-outward).to_track_quat('-Z','Y')
    right=rotation@Vector((1,0,0));up=rotation@Vector((0,1,0));lens=48;aspect=1.25
    for name,row in inventory.items():
        bpy.ops.wm.read_factory_settings(use_empty=True);path=Path(f'export/final/modules/{name}.gltf');glb=Path(f'build/final-glb/modules/{name}.glb')
        bpy.ops.import_scene.gltf(filepath=str(glb.resolve()));bpy.context.view_layer.update()
        points=[o.matrix_world@Vector(c) for o in bpy.context.scene.objects if o.type=='MESH' for c in o.bound_box]
        lo=Vector([min(v[k] for v in points) for k in range(3)]);hi=Vector([max(v[k] for v in points) for k in range(3)]);center=(lo+hi)/2
        th=36/(2*lens);tv=th/aspect
        distance=max(max((v-center).dot(outward)+abs((v-center).dot(right))/(th*.85),(v-center).dot(outward)+abs((v-center).dot(up))/(tv*.85)) for v in points)
        lighting();png=folder/'modules'/(name+'.png')
        r=render_shot(png,dict(location=list(center+outward*distance),target=list(center),lens=lens,aspect=aspect),800,samples,source=path)
        import hashlib
        r.update(name=name,triangles=row['triangles'],imported_glb=str(glb),imported_glb_sha256=hashlib.sha256(glb.read_bytes()).hexdigest());receipts.append(r)
        panel=Image.new('RGB',(400,356),(26,29,29));panel.paste(Image.open(png).convert('RGB').resize((400,320),Image.Resampling.LANCZOS))
        ImageDraw.Draw(panel).text((10,329),f"{name} / {row['triangles']:,} tris",font=ImageFont.truetype(find_font('DejaVu Sans','Book'),15),fill=(230,227,215));panels.append(panel)
    sheet=Image.new('RGB',(2000,356*math.ceil(len(panels)/5)),(26,29,29))
    for i,panel in enumerate(panels):sheet.paste(panel,((i%5)*400,(i//5)*356))
    sheet.save(folder/'modules.png');(folder/'module-views.json').write_text(json.dumps(receipts,indent=2)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='final');ap.add_argument('--width',default='1600');ap.add_argument('--samples',default='64');ap.add_argument('--checkpoint',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    shots='hero,aisle,top_deck,entry,tower,ramp_turn' if a.checkpoint else 'hero,above,aisle,tee_detail,ramp_turn,tower,tower_landing,tower_open,entry,top_deck,scale,eevee,plan_path,front,side,back,top'
    run('lookdev_render.py',['--stage','final','--out','renders/'+a.out,'--shots',shots,'--width',a.width,'--samples',a.samples])
    if not a.checkpoint:
        pieces(Path('renders')/a.out,int(a.samples))
        run('match_render.py',['--stage','final','--out','renders/'+a.out+'-matches','--width',a.width,'--samples',a.samples])
        run('match_render.py',['--stage','final','--out','renders/'+a.out+'-source-matches','--width',a.width,'--samples',a.samples,'--source-finish'])
