"""Numerical wrap checks, source/bake color check, and honest 3x3 sheets."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from kit.image_io import read_png,srgb_to_linear
from dimensions import ASPHALT_TILE,CONCRETE_TILE,LAWN_TILE


def main():
    report={};folder=Path('renders/tiles');folder.mkdir(parents=True,exist_ok=True)
    for name,coverage in [('Asphalt',ASPHALT_TILE),('Concrete',CONCRETE_TILE),('Lawn',LAWN_TILE)]:
        result={}
        for channel in ('BaseColor','Normal','ORM'):
            a=read_png(Path(f'textures/ship/T_{name}_{channel}.png'))
            seams=np.concatenate([np.abs(a[0]-a[-1]).ravel(),np.abs(a[:,0]-a[:,-1]).ravel()])
            interior=np.r_[np.abs(a[1:]-a[:-1]).ravel()[::13],np.abs(a[:,1:]-a[:,:-1]).ravel()[::13]]
            ratio=float(seams.mean()/max(interior.mean(),1e-7))
            assert ratio<1.55,(name,channel,'wrap discontinuity',ratio)
            result[channel]=dict(edge_neighbor_mean=float(seams.mean()),interior_neighbor_mean=float(interior.mean()),ratio=ratio)
            if channel=='Normal':
                lengths=np.linalg.norm(a*2-1,axis=-1);err=float(np.max(np.abs(lengths-1)));assert err<.015
                result[channel]['max_normal_length_error']=err
            if channel=='ORM':assert float(a[:,:,2].max())<.005
        source=read_png(Path(f'build/procedural/T_{name}_BaseColor.png'))
        baked=read_png(Path(f'textures/bake/T_{name}_BaseColor.png'))
        err=float(np.max(np.abs(source-baked)));mae=float(np.abs(source-baked).mean());bias=float(np.max(np.abs(source.mean(axis=(0,1),dtype=np.float64)-baked.mean(axis=(0,1),dtype=np.float64))))
        assert mae<.008 and bias<.002,(name,'color space',mae,bias)
        result['source_bake_color_max_delta']=err;result['source_bake_color_mean_delta']=mae;result['source_bake_color_mean_bias']=bias
        im=Image.open(f'textures/ship/T_{name}_BaseColor.png');im=im.resize((512,512),Image.Resampling.LANCZOS)
        sheet=Image.new('RGB',(1536,1600),(235,235,231));draw=ImageDraw.Draw(sheet)
        for y in range(3):
            for x in range(3):sheet.paste(im,(x*512,64+y*512))
        draw.text((18,17),f'{name} / 3 x 3 / {coverage*3:.3f} m across / no seam overlays',fill=(30,38,31),font=ImageFont.truetype(find_font('Noto Sans', 'Regular'),22))
        sheet.save(folder/f'{name}-3x3.jpg',quality=94,optimize=True)
        result['coverage_m']=coverage;result['density_px_m']=a.shape[0]/coverage;report[name]=result
    report['memory']=dict(unique_maps=12,materials=6,compressed_mipmapped_MiB=12*a.shape[0]**2*4/3/2**20,rgba8_mipmapped_MiB=12*a.shape[0]**2*4*4/3/2**20,note='3 maps x 4 sets at 2K; BC7 BaseColor, BC5 Normal, BC7 ORM; 16 MiB per set including mip chain. Foliage MASK and opaque iron share the trim images. Runtime engine compression is not embedded in PNG GLBs.')
    Path('build/tiling-check.json').write_text(json.dumps(dict(passed=True,sets=report),indent=2));print('PASS wrap-neighbor, normal-length, dielectric ORM and source/bake color tests')

if __name__=='__main__':main()
