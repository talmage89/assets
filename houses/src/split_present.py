"""Local source look-development sheets, provenance and memory accounting."""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.fonts import find_font
FONT=ImageFont.truetype(str(find_font('Noto Sans','Regular')),17)
ROOT=Path('renders/split/lookdev/checkpoint')


def sheet(paths,out,columns=2,tile=(780,480),titles=None):
    height=tile[1]+32;im=Image.new('RGB',(tile[0]*columns,height*((len(paths)+columns-1)//columns)),(235,235,229));draw=ImageDraw.Draw(im)
    for i,path in enumerate(paths):
        thumb=Image.open(path).convert('RGB');thumb.thumbnail(tile,Image.Resampling.LANCZOS)
        x=(i%columns)*tile[0];y=(i//columns)*height
        draw.text((x+8,y+3),titles[i] if titles else path.stem,font=FONT,fill=(35,38,32));im.paste(thumb,(x+(tile[0]-thumb.width)//2,y+32+(tile[1]-thumb.height)//2))
    out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91)


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def audit_row(row,image,recipe):
    assert image.exists(),image
    assert sha(row['source'])==row['source_sha256'],('Stale source',image)
    assert sha(Path(row['source']).with_suffix('.json'))==row['metadata_sha256'],('Stale metadata',image)
    for p,digest in row['map_sha256'].items():assert sha(p)==digest,('Stale map',image,p)
    assert row['recipe_sha256']==recipe,('Stale recipe',image)
    assert row['engine']=='CYCLES'


def audit_views(folder):
    names=('split_render.py','render.py','cape_reflections.py','ranch_render.py')
    recipe=hashlib.sha256(b''.join(n.encode()+(HERE/n).read_bytes() for n in names)).hexdigest();rows={}
    for path in sorted(folder.rglob('provenance.json')):
        for name,row in json.loads(path.read_text()).items():
            image=path.parent/(name+'.png');audit_row(row,image,recipe);rows[str(image)]=row['source_sha256']
    names=('split_value_render.py','split_render.py','cape_value_render.py','cape_render.py','cape_reflections.py','ranch_render.py','render.py')
    recipe=hashlib.sha256(b''.join((HERE/n).read_bytes() for n in names)).hexdigest()
    for name,row in json.loads((folder/'values'/'patches.json').read_text()).items():
        image=folder/'values'/(name+'.png');audit_row(row,image,recipe);rows[str(image)]=row['source_sha256']
    assert len(rows)>=62,len(rows)
    return rows


def check():
    files={};baseline=Path('build/split/accepted-files.json')
    if baseline.exists():
        for name,digest in json.loads(baseline.read_text()).items():
            assert sha(name)==digest,name
            files[name]=digest
    images=list(Path('export/textures').glob('*.png'))
    if images:
        memory=sum(Image.open(p).width*Image.open(p).height*4/3/1048576 for p in images)
        assert len(images)==39 and abs(memory-(48+1/3))<1e-7,(len(images),memory)
        scope='Dimensions read from 39 accepted canonical PNGs; BC7/BC5 8-bpp blocks plus full mips assumed'
    else:
        memory=48+1/3;scope='Accepted delivery allocation; source-only cold build does not run prior bakes'
    models=json.loads(Path('build/split/checks.json').read_text());assert models['passed']
    for row in models['rows']:assert 30000<=row['triangles']<=80000,(row['seed'],row['triangles'])
    stone=Path('build/split/materials/stone');addition=sum(Image.open(stone/('T_SplitStone_'+c+'.png')).width*Image.open(stone/('T_SplitStone_'+c+'.png')).height*4/3/1048576 for c in ('BaseColor','Normal'))
    assert abs(addition-2/3)<1e-7
    result=dict(passed=True,shared_images_present=len(images),accepted_shared_images=39,memory_scope=scope,existing_family_gpu_mib=memory,planned_addition_mib=addition,planned_family_gpu_mib=memory+addition,accepted_files_checked=len(files),justification='512 BaseColor/Normal fieldstone pair, including guarded brick coping strip. Existing family lacks irregular fieldstone; scalar roughness .91 and metallic 0 avoid an ORM map. No second brick, lap, trim, concrete or glass allocation.',stage='Source checkpoint before bake. Existing delivery allocation unchanged; addition is planned, not shipped.')
    Path('build/split/memory.json').write_text(json.dumps(result,indent=2));return result


def main(a):
    check()
    if a.check_only:return
    r=ROOT
    family=[r/'seeds'/str(s)/(v+'.png') for s in range(51,57) for v in ('front','rear')]
    sheet(family,r/'family.jpg',2,(780,350),[f'Seed {s} / {v}' for s in range(51,57) for v in ('front','rear')])
    details=[r/(v+'.png') for v in ('entry','eave','veneer','garage','tired','driveway')]+[r/'details'/'56'/'bay.png',r/'details'/'55'/'lower.png',r/'details'/'54'/'garage.png']
    sheet(details,r/'details.jpg',3,(650,470))
    paths=[r/'seeds'/str(s)/'veneer_face.png' for s in range(51,57)]
    sheet(paths,r/'veneers.jpg',3,(650,470),[f'Seed {s} / '+('fieldstone' if s==52 else 'brick') for s in range(51,57)])
    seeds=(51,52,53,55,56);sheet([r/'seeds'/str(s)/'siding.png' for s in seeds],r/'siding.jpg',3,(650,470),[f'Seed {s} / {n}' for s,n in zip(seeds,('wood lap','painted battens','8 in aluminum','vinyl','painted battens'))])
    for kind in ('clay','look'):
        paths=[r/kind/(n+'-pair.jpg') for n in ('side_pa','side_oh','foyer_pa','foyer_oh')]
        sheet(paths,r/(kind+'-pairs.jpg'),1,(1800,550))
    sheet(sorted((r/'values').glob('*-pair.jpg')),r/'material-pairs.jpg',3,(600,350))
    sheet([r/'hero.png',r/'back.png',r/'family.jpg',r/'details.jpg',r/'veneers.jpg',r/'siding.jpg',r/'clay-pairs.jpg',r/'look-pairs.jpg',r/'material-pairs.jpg'],r/'contact.jpg',3,(750,530))
    values=json.loads((r/'values'/'values.json').read_text());assert values['passed'],[k for k,v in values['rows'].items() if not v['passed']]
    views=audit_views(r)
    Path('build/split/view-check.json').write_text(json.dumps(dict(passed=True,views=views,scope='Source/metadata/map/recipe hashes and Cycles engine; fixed material-value gates. Visual critique separately in REVIEW.md.'),indent=2))
    print('SPLIT_REVIEW',len(views),'current Cycles views; planned family allocation 49 MiB')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check-only',action='store_true');main(p.parse_args())
