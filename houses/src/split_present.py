"""Local form-checkpoint sheets, provenance and unchanged-memory proof."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.fonts import find_font

FONT=ImageFont.truetype(str(find_font('Noto Sans','Regular')),17)


def sheet(paths,out,columns=2,tile=(780,480),titles=None):
    height=tile[1]+32;im=Image.new('RGB',(tile[0]*columns,height*((len(paths)+columns-1)//columns)),(235,235,229));draw=ImageDraw.Draw(im)
    for i,path in enumerate(paths):
        thumb=Image.open(path).convert('RGB');thumb.thumbnail(tile,Image.Resampling.LANCZOS)
        x=(i%columns)*tile[0];y=(i//columns)*height
        draw.text((x+8,y+3),titles[i] if titles else path.stem,font=FONT,fill=(35,38,32));im.paste(thumb,(x+(tile[0]-thumb.width)//2,y+32+(tile[1]-thumb.height)//2))
    out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91)


def audit_views(folder):
    rows={}
    for path in sorted(folder.rglob('provenance.json')):
        for name,row in json.loads(path.read_text()).items():
            image=path.parent/(name+'.png');assert image.exists(),image
            assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['source_sha256'],('Stale source',image)
            assert hashlib.sha256(Path(row['source']).with_suffix('.json').read_bytes()).hexdigest()==row['metadata_sha256'],('Stale metadata',image)
            for p,digest in row['map_sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==digest,('Stale map',image,p)
            assert row['recipe_sha256']==hashlib.sha256((HERE/'split_render.py').read_bytes()).hexdigest(),('Stale recipe',image)
            assert row['engine']=='CYCLES'
            rows[str(image)]=row['source_sha256']
    return rows


def check():
    baseline=Path('build/split/accepted-files.json');files={}
    if baseline.exists():
        for name,digest in json.loads(baseline.read_text()).items():
            assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
            files[name]=digest
    images=list(Path('export/textures').glob('*.png'))
    # All existing images are 8-bpp blocks under BC7/BC5; one image's full mip
    # chain costs width*height*4/3 bytes. Engine compression is an assumption.
    memory=sum(Image.open(p).width*Image.open(p).height*4/3/1048576 for p in images)
    assert len(images)==39 and abs(memory-(48+1/3))<1e-7,(len(images),memory)
    models=json.loads(Path('build/split/checks.json').read_text());assert models['passed']
    for row in models['rows']:assert 30000<=row['triangles']<=80000,(row['seed'],row['triangles'])
    result=dict(passed=True,shared_images=len(images),existing_family_gpu_mib=memory,planned_addition_mib=0,planned_family_gpu_mib=memory,accepted_files_checked=len(files),justification='Period modular brick, lap, painted battens, shingles, trim, glass and neutral concrete all reuse existing family sets. No stone or plywood map is allocated for this grammar.',stage='Form checkpoint only; procedural source age has not been baked.')
    Path('build/split/memory.json').write_text(json.dumps(result,indent=2));return result


def level_elevation(root):
    """Label authored floor datums on the actual Cycles side elevation."""
    import numpy as np
    meta=json.loads(Path('build/split/house-51.json').read_text())
    provenance=json.loads((root/'provenance.json').read_text())['side'];camera=provenance['camera']
    image=Image.open(root/'side.png').convert('RGB');draw=ImageDraw.Draw(image)
    forward=np.array(camera['target'])-np.array(camera['location']);forward/=np.linalg.norm(forward)
    right=np.cross(forward,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,forward)
    wing=next(b for b in meta['blocks'] if b['name']=='Wing')
    for name,z in meta['levels'].items():
        p=np.array([wing['x1'],(wing['y0']+wing['y1'])/2,z])-np.array(camera['location'])
        y=image.height/2-(p@up)/camera['ortho']*image.width
        y=round(y)
        for x in range(30,image.width-30,16):draw.line((x,y,x+8,y),fill=(232,178,68),width=2)
        label=f'{name}: {z:+.4f} m'
        draw.rectangle((30,y-26,315,y-3),fill=(30,35,34));draw.text((36,y-26),label,font=FONT,fill=(250,233,190))
    draw.rectangle((20,15,image.width-20,49),fill=(30,35,34));draw.text((30,21),'Side elevation / authored floor datums / lower floor partly below grade',font=FONT,fill=(245,245,232))
    image.save(root/'side-levels.jpg',quality=94)


def main(a):
    check()
    if a.check_only:return
    root=Path('renders/split/checkpoint')
    family=[root/'seeds'/str(s)/(v+'.png') for s in range(51,57) for v in ('front','rear')]
    titles=[f'Seed {s} / {v}' for s in range(51,57) for v in ('front','rear')]
    sheet(family,root/'family.jpg',2,(780,370),titles)
    details=[root/(v+'.png') for v in ('entry','eave','veneer','garage')]
    sheet(details,root/'details.jpg',2,(780,600))
    paths=[root/(v+'.png') for v in ('hero','back','side','levels','roof','scale')]+details
    sheet(paths,root/'contact.jpg',3,(600,410))
    level_elevation(root)
    matches=Path('renders/split/matches');sheet([matches/'split_side-pair.jpg',matches/'split_foyer-pair.jpg'],matches/'pairs.jpg',1,(1600,520))
    views={**audit_views(root),**audit_views(matches)}
    assert len(views)>=25,len(views)
    Path('build/split/view-check.json').write_text(json.dumps(dict(passed=True,views=views,scope='Source, metadata, image, recipe hashes and Cycles engine. Visual critique separately recorded in REVIEW.md.'),indent=2))
    print('SPLIT_REVIEW',len(views),'current Cycles views; +0 MiB shared textures')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check-only',action='store_true');main(p.parse_args())
