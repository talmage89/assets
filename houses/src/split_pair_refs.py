"""Inspection-only neutral copies; native pixels, exposure preserved.

No photographic pixels enter source geometry or material authoring.
"""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fetch_refs import fetch
from kit.image_io import srgb_to_linear,linear_to_srgb

PHOTOS={
 'side_pa':dict(file='split-builder-used-pa.jpg',neutral=(580,259,584,301),why='white upper replacement-window casing, same facade light'),
 'side_oh':dict(file='split-oh-side-b.jpg',neutral=(291,189,330,206),why='white upper lap siding away from casing, tree and cast shadow'),
 'foyer_pa':dict(file='split-foyer-used-pa.webp',neutral=(336,172,341,249),why='white entry casing; true between-floor door crosses the material line'),
 'foyer_oh':dict(file='split-builder-used-oh.jpg',neutral=(759,166,765,218),why='white upper replacement-window casing, right sash'),
}


def prepare():
    fetch('refs',[v['file'] for v in PHOTOS.values()]+['split-pa-builder-c.jpg','split-pa-builder-d.jpg','split-used-bay.jpg','split-visions.pdf','split-oh-side-c.jpg','split-builder-used-oh.jpg'])
    rows={}
    for name,s in PHOTOS.items():
        p=Path('refs')/s['file'];im=ImageOps.exif_transpose(Image.open(p)).convert('RGB');a=srgb_to_linear(np.asarray(im)/255)
        x0,y0,x1,y1=s['neutral'];white=np.median(a[y0:y1,x0:x1],axis=(0,1));gain=white.mean()/white
        assert all(.6<g<1.7 for g in gain),(name,gain)
        out=Path('refs')/('split-pair-'+name+'.jpg');Image.fromarray(np.uint8(np.rint(np.clip(linear_to_srgb(a*gain),0,1)*255))).save(out,quality=98)
        rows[name]={**s,'native_size':im.size,'gains':gain.tolist(),'original_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'balanced':str(out),'exposure_changed':False}
    Path('build/split/pair-references.json').write_text(json.dumps(rows,indent=2));print('SPLIT_PAIR_REFS',len(rows))


if __name__=='__main__':prepare()
