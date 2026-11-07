"""Fixed-camera look comparisons against the accepted form handoff."""
import sys,json,argparse
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parent)]
CASES={101:['hero','ledge','stairs','bowl','deep_end','above','transition','walk','tag'],202:['hero','above'],303:['prefab','plate','hero','prefab_side']}

def compose(out):
    from PIL import Image,ImageDraw
    rows=[]
    for seed,names in CASES.items():
        for name in names:
            before=Path(f'renders/lookdev/{seed}/{name}.png')
            rerendered=out/'before'/str(seed)/(name+'.png')
            if rerendered.exists():before=rerendered
            after=out/str(seed)/(name+'.png')
            if not after.exists():continue
            a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB')
            assert a.size==b.size and a.width>=800,(seed,name,a.size,b.size)
            old=json.loads(before.with_suffix('.json').read_text());new=json.loads(after.with_suffix('.json').read_text())
            for key in ('location','target','lens','aspect'):assert old['camera'][key]==new['camera'][key]
            for key in ('roll','shift_y'):assert old['camera'].get(key,0)==new['camera'].get(key,0)
            if name not in ('hero','above'):
                for key in old['effective_lighting'].keys() & new['effective_lighting'].keys():
                    assert old['effective_lighting'][key]==new['effective_lighting'][key],(seed,name,key)
            from external import bundle
            assert new['source'].endswith('.gltf') and new['bundle_sha256']==bundle(Path(new['source'])),(seed,name,'stale exported crop')
            canvas=Image.new('RGB',(a.width*2,a.height+32),(26,29,27));d=ImageDraw.Draw(canvas)
            canvas.paste(a,(0,32));canvas.paste(b,(a.width,32));d.text((15,10),f'{seed}/{name}: before / 1b6c91a',fill='white');d.text((a.width+15,10),'after / external glTF + shipped textures / sun exposure',fill='white')
            target=out/f'{seed}-{name}-before-after.jpg';canvas.save(target,quality=96,optimize=True)
            rows.append(dict(seed=seed,shot=name,path=str(target),native_panel=list(a.size),before=old,after=new))
    Path('build/delivery-fixes.json').write_text(json.dumps(rows,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--compose',action='store_true');ap.add_argument('--seed',type=int);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--out',type=Path,default=Path('renders/delivery-fixes'));a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if not a.compose:
        from render import render
        from PIL import Image
        for seed,names in CASES.items():
            if a.seed and seed!=a.seed:continue
            from render import views
            old_plan=json.loads(Path(f'build/revision-before/park-{seed}.json').read_text())['plan']
            current_plan=json.loads(Path(f'build/park-{seed}.json').read_text())['plan']
            current_views=views(current_plan);shots={}
            for n in names:
                record=Path(f'renders/lookdev/{seed}/{n}.json')
                shot=json.loads(record.read_text())['camera'] if record.exists() else views(old_plan)[n]
                # Preserve projection. Material comparisons use identical new
                # illumination on both exports; heroes/above retain the actual
                # archived washed exposure as the lighting correction evidence.
                for key in ('sun_direction','sun_energy','sky_strength'):
                    if key in current_views[n]:shot[key]=current_views[n][key]
                # JSON receipts store lists; normalize tuple-valued view
                # defaults before comparing the retained baseline camera.
                shot=json.loads(json.dumps(shot))
                shots[n]=shot
                if n not in ('hero','above'):
                    before=a.out/'before'/str(seed)/(n+'.json')
                    from external import bundle
                    cached=json.loads(before.read_text()) if before.exists() else {}
                    if cached.get('camera')!=shot or cached.get('samples')!=a.samples or cached.get('bundle_sha256')!=bundle(Path(f'export/lookdev/Park_{seed}.gltf')):
                        render(seed,'export/lookdev',a.out/'before'/str(seed),1440,a.samples,custom={n:shot},manifest=f'build/revision-before/park-{seed}.json')
            width=Image.open(f'renders/lookdev/{seed}/{names[0]}.png').width
            render(seed,'export/final',a.out/str(seed),width,a.samples,custom=shots)
    compose(a.out)
