"""Cycles review of the revised external glTFs, with source/image receipts."""
import argparse,json,math,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from render import render_shot,shots,overlays
from light_review import lighting,views


def main():
    a=argparse.ArgumentParser();a.add_argument('--stage',default='form');a.add_argument('--out',type=Path,default=Path('renders/form-pass1'));a.add_argument('--seeds',default='101,202');a.add_argument('--shots',default='hero,retained_hero,above,aisle,tower');a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=24);a.add_argument('--source-finish',action='store_true');a.add_argument('--append',action='store_true');args=a.parse_args(sys.argv[sys.argv.index('--')+1:]);receipts=[]
    if args.append and (args.out/'views.json').exists():
        from lookdev_review import verify_receipt
        receipts=json.loads((args.out/'views.json').read_text())
        for r in receipts:verify_receipt(r)
    for seed in map(int,args.seeds.split(',')):
        p=json.loads(Path(f'build/lookdev/garage-{seed}.json').read_text())
        bpy.ops.wm.read_factory_settings(use_empty=True)
        prefix={'form':'ParkingGarageFormSite','lookdev':'ParkingGarageLookSite','final':'ParkingGarageSite'}.get(args.stage,'ParkingGarageLookSite')
        path=Path(f'export/{args.stage}/sites/{prefix}-{seed}.gltf') if args.stage!='baseline' else Path(f'export/sites/ParkingGarageSite-{seed}.gltf')
        imported=Path('build/final-glb')/path.relative_to('export/final').with_suffix('.glb') if args.stage=='final' else path
        bpy.ops.import_scene.gltf(filepath=str(imported.resolve()));bpy.context.view_layer.update()
        if args.source_finish:
            from atlas_binding import source_finish
            source_finish()
        cache=Path(f'build/lookdev/render-{args.stage}-{seed}.blend').resolve();bpy.ops.wm.save_as_mainfile(filepath=str(cache))
        shotdefs=views(p,shots)
        for name in args.shots.split(','):
            if name=='plan_path' and seed!=101:continue
            shot=shotdefs[name];bpy.ops.wm.open_mainfile(filepath=str(cache))
            if shot.get('garage_only'):
                garage=next(o for o in bpy.context.scene.objects if o.name.startswith('Garage_') and o.get('system')==p['system'])
                keep={garage,*garage.children_recursive}
                for ob in list(bpy.context.scene.objects):
                    if ob not in keep:bpy.data.objects.remove(ob,do_unlink=True)
                import geometry as G
                G.M['StudioGround']=G.material('Turnaround neutral floor',(.13,.13,.12),.9)
                floor=G.Mesh('Turnaround ground');floor.box((0,0,-.25),(2000,2000,.1),'StudioGround');floor.finish()
            if shot.get('paths'):overlays(p)
            if args.stage=='baseline':
                from render import lighting as old_lighting
                old_lighting(interior=shot.get('interior',False))
                shot['max_bounces']=7
            else:
                direction=[shot['location'][i]-shot['target'][i] for i in range(2)]
                inspect=math.degrees(math.atan2(direction[1],direction[0]))+35 if name in ('front','side','back') else None
                lighting(interior=shot.get('interior',False),front_lit=name in ('above','plan_path','top_deck','top','entry','tower','eevee'),inspection_azimuth=inspect,
                         commercial_hero=seed==202 and name in ('hero','retained_hero'))
            culled=[]
            if shot.get('roof_inspection'):
                # These lights are beneath opaque slabs and cannot illuminate
                # the visible roof. Avoid their raster shadow-map passes.
                cutoff=(p['levels']-1)*p['floor_to_floor']+.05
                for ob in list(bpy.context.scene.objects):
                    if ob.type=='LIGHT' and ob.data.type=='AREA' and ob.location.z<cutoff:
                        culled.append(ob.name);bpy.data.objects.remove(ob,do_unlink=True)
            if shot.get('human'):
                from kit import studio
                from mathutils import Vector
                at=Vector(shot['human_at'])
                for ob in studio.human():ob.location+=at+Vector((1.03,-.24,0))
            presented=[]
            if shot.get('open_lift'):
                for pv in bpy.context.scene.objects:
                    if pv.get('slide_axis')=='X' and 'ElevatorDoor_L1_' in pv.name:
                        pv.location.x+=pv['range_m'][-1];presented.append(dict(name=pv.name,translation_m=pv['range_m'][-1]))
            output_name={'retained_hero':'hero','retained_aisle':'aisle'}.get(name,name) if args.stage=='baseline' else name
            r=render_shot(args.out/str(seed)/(output_name+'.png'),shot,args.width,args.samples,shot.get('engine','CYCLES'),path)
            from hashlib import sha256
            d=json.loads(path.read_text());r['images']={im['uri']:sha256((path.parent/im['uri']).read_bytes()).hexdigest() for im in d.get('images',[])}
            r.update(seed=seed,name=name,stage=args.stage,source_finish=args.source_finish,presented_pivots=presented,culled_hidden_roof_lights=culled)
            if args.stage=='final':r.update(imported_glb=str(imported),imported_glb_sha256=sha256(imported.read_bytes()).hexdigest())
            receipts=[old for old in receipts if (old['seed'],old['name'])!=(seed,name)]
            receipts.append(r);(args.out/'views.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print('EXPORTED REVIEW COMPLETE',args.out,len(receipts),flush=True)


if __name__=='__main__':main()
