"""Three delivered family guns photographed in one unmodified field studio."""
import argparse,hashlib,json,subprocess,sys,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font

def main():
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48);a=p.parse_args()
    out=BASE/'renders/final/family';out.mkdir(parents=True,exist_ok=True)
    models={'Covey 26':BASE/'export/sxs.glb','Hearth 12':BASE.parent/'shotgun/export/shotgun.glb','Bracken L20':BASE.parent/'lever/export/lever.glb'}
    signature=hashlib.sha256()
    for f in [BASE/'src/final_render.py',BASE/'src/final_shots.py',BASE.parent/'common/render.py']:signature.update(f.read_bytes())
    signature=signature.hexdigest();records={}
    for name,source in models.items():
        if not source.exists():
            asset=source.parents[1]
            with (BASE/'build'/('family-build-'+asset.name+'.log')).open('w') as log:
                subprocess.run(['make','-C',str(asset),'export'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        digest=hashlib.sha256(source.read_bytes()).hexdigest();folder=out/name.replace(' ','_')
        primary=BASE/'renders/final/beauty'
        if name=='Covey 26' and (primary/'shots.json').exists():
            shared=json.loads((primary/'shots.json').read_text()).get('hero',{})
            if (shared.get('sha256')==digest and shared.get('samples_used')==a.samples and
                shared.get('renderer_signature')==signature and Image.open(primary/'hero.png').width==a.width):
                folder.mkdir(parents=True,exist_ok=True);shutil.copy2(primary/'hero.png',folder/'hero.png')
                (folder/'shots.json').write_text(json.dumps(dict(hero=shared),indent=2))
        current=json.loads((folder/'shots.json').read_text()) if (folder/'shots.json').exists() else {}
        valid=current.get('hero',{}).get('sha256')==digest and current.get('hero',{}).get('samples_used')==a.samples and (folder/'hero.png').exists() and current.get('hero',{}).get('renderer_signature')==signature and (folder/'hero.png').exists() and Image.open(folder/'hero.png').width==a.width
        if not valid:
            with (BASE/'build'/('family-'+source.stem+'.log')).open('w') as log:
                subprocess.run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(BASE/'src/final_render.py'),
                    '--','--source',str(source),'--out',str(folder),'--width',str(a.width),'--samples',str(a.samples),'--shots','hero'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        records[name]=json.loads((folder/'shots.json').read_text())['hero']
        assert records[name]['sha256']==digest and records[name]['renderer_signature']==signature
    first=next(iter(records.values()))
    for r in records.values():
        for key in ('location','target','lens','exposure','aspect','engine'):assert r[key]==first[key]
    font=ImageFont.truetype(find_font('Noto Sans','Regular'),24)
    h=round(a.width/2.8);sheet=Image.new('RGB',(a.width,3*(h+50)+65),(160,160,158));d=ImageDraw.Draw(sheet)
    d.text((20,14),'Same studio, camera, exposure and scale — baked exports',fill=(25,25,25),font=font)
    for i,name in enumerate(models):
        im=Image.open(out/name.replace(' ','_')/'hero.png').convert('RGBA')
        bg=Image.new('RGBA',im.size,(160,160,158,255));bg.alpha_composite(im)
        y=65+i*(h+50);sheet.paste(bg.convert('RGB'),(0,y));d.text((20,y+5),name,fill=(25,25,25),font=font)
    sheet.save(out/'three-guns.jpg',quality=95,optimize=True)
    (out/'comparison.json').write_text(json.dumps(dict(method='No material overrides, per-gun exposure or image grading; exact same five field-studio lights, 36mm camera sensor, viewpoint and scale',models=records),indent=2))
    print('FAMILY',len(records),out/'three-guns.jpg')
if __name__=='__main__':main()
