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
    lens=48;aspect=1.25
    for name,row in inventory.items():
        bpy.ops.wm.read_factory_settings(use_empty=True);path=Path(f'export/final/modules/{name}.gltf');glb=Path(f'build/final-glb/modules/{name}.glb')
        bpy.ops.import_scene.gltf(filepath=str(glb.resolve()));bpy.context.view_layer.update()
        points=[o.matrix_world@Vector(c) for o in bpy.context.scene.objects if o.type=='MESH' for c in o.bound_box]
        lo=Vector([min(v[k] for v in points) for k in range(3)]);hi=Vector([max(v[k] for v in points) for k in range(3)]);center=(lo+hi)/2
        underside=name in ('DoubleTee','StructuralBay','EndBay','RampBay')
        outward=Vector((-1.3,-1.8,-.65 if underside else 1.0)).normalized()
        rotation=(-outward).to_track_quat('-Z','Y')
        right=rotation@Vector((1,0,0));up=rotation@Vector((0,1,0))
        th=36/(2*lens);tv=th/aspect
        distance=max(max((v-center).dot(outward)+abs((v-center).dot(right))/(th*.85),(v-center).dot(outward)+abs((v-center).dot(up))/(tv*.85)) for v in points)
        # A neutral procedural studio makes dark metal legible, and the tee
        # views show the accepted stems instead of concealing them behind
        # the flange. Geometry and baked materials stay exactly as imported.
        world=bpy.data.worlds.new('Module studio neutral');world.use_nodes=True;bpy.context.scene.world=world
        bg=world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.18,.20,.23,1);bg.inputs['Strength'].default_value=.7
        extent=max(max(hi-lo),.4)
        for label,direction,power in [('key',outward+right*.5+up*.7,45),('fill',outward-right*.9,10)]:
            ld=bpy.data.lights.new('Module '+label,'AREA');ld.energy=power*extent**2;ld.shape='DISK';ld.size=extent
            ob=bpy.data.objects.new(ld.name,ld);bpy.context.scene.collection.objects.link(ob)
            ob.location=center+direction.normalized()*extent*1.5;ob.rotation_euler=(center-ob.location).to_track_quat('-Z','Y').to_euler()
        sc=bpy.context.scene;sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=0
        png=folder/'modules'/(name+'.png')
        r=render_shot(png,dict(location=list(center+outward*distance),target=list(center),lens=lens,aspect=aspect),800,samples,source=path)
        import hashlib
        r.update(name=name,triangles=row['triangles'],imported_glb=str(glb),imported_glb_sha256=hashlib.sha256(glb.read_bytes()).hexdigest());receipts.append(r)
        panel=Image.new('RGB',(400,356),(26,29,29));panel.paste(Image.open(png).convert('RGB').resize((400,320),Image.Resampling.LANCZOS))
        ImageDraw.Draw(panel).text((10,329),f"{name} / {row['triangles']:,} tris",font=ImageFont.truetype(find_font('DejaVu Sans','Book'),15),fill=(230,227,215));panels.append(panel)
    sheet=Image.new('RGB',(2000,356*math.ceil(len(panels)/5)),(26,29,29))
    for i,panel in enumerate(panels):sheet.paste(panel,((i%5)*400,(i//5)*356))
    sheet.save(folder/'modules.png');(folder/'module-views.json').write_text(json.dumps(receipts,indent=2)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='final');ap.add_argument('--width',default='1600');ap.add_argument('--samples',default='64');ap.add_argument('--checkpoint',action='store_true');ap.add_argument('--resume',action='store_true');ap.add_argument('--force-shots',default='');ap.add_argument('--pieces-only',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.pieces_only:
        pieces(Path('renders')/a.out,int(a.samples));sys.exit(0)
    shots='hero,aisle,top_deck,entry,tower,ramp_turn' if a.checkpoint else 'hero,above,aisle,tee_detail,ramp_turn,tower,tower_landing,tower_open,entry,top_deck,scale,eevee,plan_path,front,side,back,top'
    common=['--stage','final','--out','renders/'+a.out,'--width',a.width,'--samples',a.samples]
    if a.resume:
        receipt=Path('renders')/a.out/'views.json';existing=json.loads(receipt.read_text()) if receipt.exists() else []
        force=set(a.force_shots.split(','));done={(r['seed'],r['name']) for r in existing}
        for seed in (101,202):
            todo=[name for name in shots.split(',') if ((seed,name) not in done or name in force) and (name!='plan_path' or seed==101)]
            if todo:run('lookdev_render.py',common+['--seeds',str(seed),'--shots',','.join(todo),'--append'])
    else:run('lookdev_render.py',common+['--shots',shots])
    if not a.checkpoint:
        pieces(Path('renders')/a.out,int(a.samples))
        run('match_render.py',['--stage','final','--out','renders/'+a.out+'-matches','--width',a.width,'--samples',a.samples])
        run('match_render.py',['--stage','final','--out','renders/'+a.out+'-source-matches','--width',a.width,'--samples',a.samples,'--source-finish'])
