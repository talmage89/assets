"""One GPU-lock acquisition per serial export review set."""
import argparse,hashlib,json,struct,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import render as renderer
from render import render_modules,shots

_render_file=renderer.render_file
RESUME=False
PACKAGES={}


def render_file(source,out,name,spec,width,samples,engine):
    png=out/(name+'.png');receipt=out/(name+'.json')
    if RESUME and png.exists() and receipt.exists():
        d=json.loads(receipt.read_text());raw=png.read_bytes();i=8;meta={}
        while i+12<=len(raw):
            length,kind=struct.unpack_from('>I4s',raw,i);chunk=raw[i+8:i+8+length];i+=length+12
            if kind==b'tEXt':
                key,_,value=chunk.partition(b'\0');meta[key.decode()]=value.decode()
        count=int(meta.get('cycles.ViewLayer.samples',d.get('capture_samples',-1)))
        if source not in PACKAGES:PACKAGES[source]=renderer.digest(source)
        recipe=hashlib.sha256(Path(renderer.__file__).read_bytes()).hexdigest()
        normalized=json.loads(json.dumps(spec))
        if 'photo_size' in spec:
            sw,sh=spec['photo_size'];factor=max(1,round(width/sw));size=[sw*factor,sh*factor]
        else:size=[width,round(width/spec.get('aspect',1.5))]
        imported=Path(d.get('imported_source','build/missing-import'))
        import_current=imported.is_file() and d.get('imported_sha256')==hashlib.sha256(imported.read_bytes()).hexdigest()
        if (import_current and count==samples and d.get('source')==str(source) and d.get('package_sha256')==PACKAGES[source]
                and d.get('render_recipe_sha256')==recipe and d.get('engine')==engine
                and all(d.get(k)==v for k,v in normalized.items())
                and d['resolution']==size and list(struct.unpack_from('>II',raw,16))==size):
            print('REUSE verified capture',png,flush=True);return
    _render_file(source,out,name,spec,width,samples,engine)
    d=json.loads(receipt.read_text());d['capture_samples']=samples;receipt.write_text(json.dumps(d,indent=2))


def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/look-a'))
    p.add_argument('--width',type=int,default=1000);p.add_argument('--samples',type=int,default=20)
    p.add_argument('--shots',default='hero,above,window,window_dusk');p.add_argument('--matches',action='store_true')
    p.add_argument('--source-matches',action='store_true');p.add_argument('--range',action='store_true');p.add_argument('--full',action='store_true');p.add_argument('--resume',action='store_true');a=p.parse_args(argv if argv is not None else sys.argv[sys.argv.index('--')+1:])
    global RESUME
    RESUME=a.resume;renderer.render_file=render_file
    if a.full:a.shots='hero,above,doors,window,window_dusk,tower,wing,sign,scale,age,north_roof';a.matches=True;a.source_matches=True;a.range=True
    for seed in (101,202):
        for name in filter(None,a.shots.split(',')):
            render_file(Path(f'export/ChurchSite-{seed}.gltf'),a.out/str(seed),name,shots(seed)[name],a.width,a.samples,'CYCLES')
    if a.matches:
        for name,data in json.loads(Path('build/matched-cameras.json').read_text()).items():
            spec=dict(data['shot']);spec.update(landmarks_world_m=data['landmarks_world_m'],expected_pixels=data['projected_pixels'],photo_size=[data['crop'][2]-data['crop'][0],data['crop'][3]-data['crop'][1]])
            render_file(Path(data['source']),Path('renders/matches') if a.full else a.out/'matches',name,spec,a.width,a.samples,'CYCLES')
            if a.source_matches:
                render_file(Path(f'build/site-{data["seed"]}.blend'),Path('renders/source-matches') if a.full else a.out/'source-matches',name,spec,a.width,a.samples,'CYCLES')
    if a.range:
        render_file(Path('export/Range.gltf'),a.out,'range',dict(location=(60,-170,90),target=(16,0,6),lens=42,ortho=166,module_studio=True),a.width,a.samples,'CYCLES')
    if a.full:
        render_modules(Path('renders/modules'),720,32,'CYCLES')
        for seed in (101,202):render_file(Path(f'export/ChurchSite-{seed}.gltf'),Path('renders/eevee')/str(seed),'hero',shots(seed)['hero'],a.width,a.samples,'BLENDER_EEVEE')


if __name__=='__main__':main()
