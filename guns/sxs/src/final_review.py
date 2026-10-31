"""Contact sheets and provenance of the delivered look round; no docs JPGs."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20)

def sheet(items,path,columns=3,width=1800,cell_height=300):
    cw=width//columns;rows=(len(items)+columns-1)//columns
    out=Image.new('RGB',(width,rows*cell_height),(160,160,158));d=ImageDraw.Draw(out)
    for i,(label,p) in enumerate(items):
        im=Image.open(p).convert('RGBA');im.thumbnail((cw-16,cell_height-42),Image.Resampling.LANCZOS)
        x=(i%columns)*cw;y=(i//columns)*cell_height
        bg=Image.new('RGBA',im.size,(160,160,158,255));bg.alpha_composite(im)
        out.paste(bg.convert('RGB'),(x+(cw-im.width)//2,y+32+(cell_height-42-im.height)//2))
        d.text((x+10,y+6),label,font=FONT,fill=(20,20,20))
    out.save(path,quality=94,optimize=True)

def main():
    root=BASE/'renders/final';digest=hashlib.sha256((BASE/'export/sxs.glb').read_bytes()).hexdigest()
    beauty=json.loads((root/'beauty/shots.json').read_text())
    for name,r in beauty.items():assert r['sha256']==digest and r['source'].endswith('.glb'),name
    hero=Image.open(root/'beauty/hero.png').convert('RGBA');bg=Image.new('RGBA',hero.size,(160,160,158,255));bg.alpha_composite(hero);bg.convert('RGB').save(root/'hero-gray.png')
    rgb=np.asarray(hero);foreground=rgb[:,:,3]>250;values=rgb[:,:,:3][foreground].astype(float);luma=values@np.array((.2126,.7152,.0722))
    tonal=dict(luma_percentiles={str(p):float(np.percentile(luma,p)) for p in (1,5,10,50,90,95,99)},
       all_channels_clipped_fraction=float(np.mean(values.min(1)>=254)),any_channel_clipped_fraction=float(np.mean(values.max(1)>=254)),
       shadow_below_8_fraction=float(np.mean(luma<8)),method='Actual ungraded foreground, alpha>250; Rec709 display luma. Range check, not photographic look proof.')
    items=[(name,root/'beauty'/(name+'.png')) for name in beauty]
    items += [('Eevee hero',root/'eevee/hero.png'),('Shell 512 subset',root/'shell/shell.png'),('Fired hull 512 subset',root/'hull/hull.png')]
    sheet([(n,root/'beauty'/(n+'.png')) for n in ('action','wrist','forend','stock','muzzle','top_controls','triggers')],root/'details.jpg',columns=2,cell_height=430)
    sheet([(n,root/'beauty'/(n+'.png')) for n in ('shooter_three_quarter','aimed','open','breech')],root/'player-views.jpg',columns=2,cell_height=430)
    sheet([(n,root/'beauty'/(n+'.png')) for n in ('side','front','left','back','top')],root/'turnaround.jpg',columns=2,cell_height=380)
    pairs=sorted((root/'look-review').glob('*-pair.jpg'));sheet([(p.stem,p) for p in pairs],root/'finish-contact.jpg',columns=2,cell_height=500)
    wear=sorted((root/'wear').glob('*-on-off-pair.jpg'));sheet([(p.stem,p) for p in wear],root/'wear-contact.jpg',columns=2,cell_height=650)
    native=sorted((root/'wear-native').glob('*-native-2d-pair.jpg'))
    sheet([(p.stem,p) for p in native],root/'wear-native-contact.jpg',columns=2,cell_height=600)
    all_items=items+[(p.stem,p) for p in pairs+wear+native]+[('Same studio family',root/'family/three-guns.jpg')]
    sheet(all_items,root/'contact-sheet.jpg')
    # An old contact sheet can look plausible: require every piece of evidence
    # to identify this exact export, including auxiliary engines and ammo.
    finish_data=json.loads((root/'look-review/values.json').read_text())
    wear_data=json.loads((root/'wear/measurements.json').read_text())
    assert len(finish_data['finishes'])==10 and len(wear_data['sites'])==9
    assert all(r['model_sha256']==digest for r in finish_data['finishes'].values())
    assert all(r['model_sha256']==digest for r in wear_data['sites'].values())
    for folder,model in [('eevee','sxs'),('shell','shell'),('hull','hull')]:
        expected=hashlib.sha256((BASE/'export'/(model+'.glb')).read_bytes()).hexdigest()
        auxiliary=json.loads((root/folder/'shots.json').read_text())
        assert auxiliary and all(r['sha256']==expected for r in auxiliary.values())
    native_data=json.loads((root/'wear-native/measurements.json').read_text())
    assert all(r['model_sha256']==digest for r in native_data['sites'].values())
    source_data=json.loads((root/'source/bake-loss.json').read_text())
    source_digest=hashlib.sha256((BASE/'build/delivery/high.blend').read_bytes()).hexdigest()
    assert len(source_data)==10 and all(r['export_sha256']==digest and r['source_sha256']==source_digest for r in source_data.values())
    family=json.loads((root/'family/comparison.json').read_text())
    assert family['models']['Covey 26']['sha256']==digest
    records={}
    for p in (BASE/'export').glob('*.glb'):records[str(p.relative_to(BASE))]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    for p in (BASE/'textures').glob('*.png'):records[str(p.relative_to(BASE))]=dict(bytes=p.stat().st_size,size=Image.open(p).size,bits_per_channel=p.read_bytes()[24],sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    (root/'delivery.json').write_text(json.dumps(dict(files=records,model_sha256=digest,views=list(beauty),hero_tonal_range=tonal,
        finish_acceptance=finish_data,wear=wear_data,native_wear=native_data,source_bake_loss=source_data,family=family),indent=2))
    print('FINAL',len(items),'views;',len(pairs),'finish pairs;',len(wear),'wear pairs;',len(native),'native 2D pairs;',root/'contact-sheet.jpg')
if __name__=='__main__':main()
