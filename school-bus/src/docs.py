"""Five bounded JPGs from the reviewed exported gallery; no source rendering."""
import hashlib,json,shutil,sys
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path[:0]=[str(HERE),str(BASE.parent)]
from kit.contact import review_sheet
from kit.delivery_docs import jpg
from review import main as verify_gallery,signature

def main():
    verify_gallery()
    final=BASE/'renders/final';out=BASE/'docs';scratch=BASE/'build/doc-layouts'
    scratch.mkdir(parents=True,exist_ok=True)
    eevee=scratch/'Eevee.png'
    shutil.copyfile(BASE/'renders/eevee/hero.png',eevee)
    jpg(final/'hero.png',out/'hero.jpg')
    jpg(final/'turnaround.jpg',out/'turnaround.jpg')
    layouts={
        'details':('Morrow C75 / front, optics and mechanisms',[
            [final/'front_detail.png',final/'lamp_detail.png'],
            [final/'warning.png',final/'wheels.png']]),
        'cabin':('Morrow C75 / entrance, cabin and exits',[
            [final/'entrance.png',final/'interior.png'],
            [final/'aisle_daylight.png',final/'side_interior.png'],
            [final/'emergency.png',final/'roof.png']]),
        'fleet':('Morrow C75 / three exports, scale and Eevee',[
            [final/'fleet.png'],[final/'scale.png',eevee]])}
    for name,(title,rows) in layouts.items():
        path=scratch/(name+'.jpg')
        review_sheet(rows,path,width=1600,title=title)
        jpg(path,out/(name+'.jpg'))
    rows={}
    for name in ['hero','turnaround','details','cabin','fleet']:
        path=out/(name+'.jpg');size=Image.open(path).size
        if size[0]>1600 or path.stat().st_size>200000:raise ValueError('Oversized docs JPG: '+name)
        rows[path.name]=dict(size=list(size),bytes=path.stat().st_size,
            sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    report=dict(passed=True,source_exports={str(s):signature(BASE/f'export/C75-{s}.gltf') for s in [101,102,103]},
        images=rows,scope='Original exported-gallery images; current payload/pose provenance verified before composition')
    (BASE/'build/docs.json').write_text(json.dumps(report,indent=2))
    print('BUS_DOCS',json.dumps(rows),flush=True)

if __name__=='__main__':main()
