"""Native fixed-camera comparisons against the ed8953f gate candidate."""
import sys,json,shutil,argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE)]
CASES={101:['transition','ledge','hero','bowl','deep_end'],202:['hero'],303:['hero','prefab']}
OUT=Path('renders/gate-fixes')

def compose():
    from PIL import Image,ImageDraw
    from external import bundle
    rows=[]
    for seed,names in CASES.items():
        for name in names:
            before=OUT/'before'/str(seed)/(name+'.png');after=OUT/str(seed)/(name+'.png')
            a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB');assert a.size==b.size and a.width>=800
            old=json.loads(before.with_suffix('.json').read_text());new=json.loads(after.with_suffix('.json').read_text())
            for key in ('location','target','lens','aspect','roll','shift_y'):
                assert old['camera'].get(key,0)==new['camera'].get(key,0),(seed,name,'changed projection',key)
            for key in ('exposure','sun_energy','sun_direction_world','sky_strength','sky_saturation','view_transform','look'):
                if seed==303 and name=='hero' and key=='sun_direction_world':continue
                assert old['effective_lighting'][key]==new['effective_lighting'][key],(seed,name,key)
            assert abs(old['effective_lighting']['sun_elevation_degrees']-new['effective_lighting']['sun_elevation_degrees'])<.0001
            assert new['bundle_sha256']==bundle(Path(new['source'])),(seed,name,'stale export')
            c=Image.new('RGB',(a.width*2,a.height+32),(26,29,27));c.paste(a,(0,32));c.paste(b,(a.width,32));d=ImageDraw.Draw(c)
            d.text((15,10),f'{seed}/{name}: before / ed8953f',fill='white');d.text((a.width+15,10),'after / placement wear / shared external glTF',fill='white')
            target=OUT/f'{seed}-{name}-before-after.jpg';c.save(target,quality=96,optimize=True)
            rows.append(dict(seed=seed,view=name,native_panel=list(a.size),comparison=str(target),after=new))
            crops=[]
            if seed==101 and name=='hero':crops.append(('101-toe-before-after.jpg',(0,465,1200,778),'101: warm wall / airbrushed toe, before','after / gray concrete, burnished toe, floor deposits'))
            if seed==303 and name=='hero':crops.append(('303-blob-before-after.jpg',(640,100,1440,700),'303: isolated sun patch / before','after / sun azimuth +12 deg, same low elevation'))
            for filename,crop,left,right in crops:
                aa=a.crop(crop);bb=b.crop(crop);assert aa.width>=800
                c=Image.new('RGB',(aa.width*2,aa.height+32),(26,29,27));c.paste(aa,(0,32));c.paste(bb,(aa.width,32));d=ImageDraw.Draw(c)
                d.text((15,10),left,fill='white');d.text((aa.width+15,10),right,fill='white')
                c.save(OUT/filename,quality=96,optimize=True)
                rows[-1].setdefault('crops',[]).append(dict(path=str(OUT/filename),native_panel=list(aa.size),crop=crop))
    Path('build/gate-fixes.json').write_text(json.dumps(rows,indent=2))
    from review import sheet
    sheet([OUT/str(s)/(n+'.png') for s,ns in CASES.items() for n in ns],OUT/'contact.jpg')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--compose',action='store_true');p.add_argument('--from-final',action='store_true');p.add_argument('--samples',type=int,default=40);p.add_argument('--seed',type=int,choices=CASES);a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if a.from_final:
        for seed,names in CASES.items():
            for name in names:
                for ext in ('.png','.json'):
                    target=OUT/str(seed)/(name+ext);target.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copy2(Path('renders/final')/str(seed)/(name+ext),target)
    elif not a.compose:
        from render import render,views
        for seed,names in CASES.items():
            if a.seed is not None and seed!=a.seed:continue
            shots={n:json.loads((OUT/'before'/str(seed)/(n+'.json')).read_text())['camera'] for n in names}
            if seed==303:
                plan=json.loads(Path('build/park-303.json').read_text())['plan']
                shots['hero']['sun_direction']=views(plan)['hero']['sun_direction']
            render(seed,'export/final',OUT/str(seed),1440,a.samples,custom=shots)
    compose()
