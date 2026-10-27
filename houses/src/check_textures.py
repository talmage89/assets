"""Independent stored-image checks for the source look-development fields."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.image_io import read_png,srgb_to_linear
from textures import SETS


def main():
    folder=Path('textures/source');rows={}
    for name,(n,coverage) in SETS.items():
        paths={c:folder/f'T_House{name}_{c}.png' for c in ('BaseColor','Normal','ORM')}
        maps={c:read_png(p) for c,p in paths.items()}
        assert all(a.shape==(n,n,3) and np.isfinite(a).all() for a in maps.values())
        normals=maps['Normal']*2-1;error=float(np.max(np.abs(np.linalg.norm(normals,axis=-1)-1)))
        assert error<.007
        color=srgb_to_linear(maps['BaseColor']);mean=color.mean(axis=(0,1))
        if name=='Shingles':assert .08<float(mean.mean())<.12
        if name=='Trim':
            # Lower two image strips correspond to glass's atlas V=.75..1.
            assert float(maps['ORM'][:n//4,:,2].max())==0
        rows[name]=dict(size=n,observed_linear_albedo_mean=list(map(float,mean)),normal_length_error=error,
            png_bytes=sum(p.stat().st_size for p in paths.values()),gpu_mib=n*n*4/1048576,
            sha256={c:hashlib.sha256(p.read_bytes()).hexdigest() for c,p in paths.items()})
    result=dict(passed=True,sets=rows,gpu_total_mib=sum(r['gpu_mib'] for r in rows.values()),
        scope='Stored original source images, resolutions/finite values/unit normals/albedo; BC7+BC5+BC7 with full mip chain estimate, not measured engine allocation')
    assert result['gpu_total_mib']==38
    Path('build/texture-check.json').write_text(json.dumps(result,indent=2));print('TEXTURE_FIELDS 5 sets / 15 images / 38 MiB compressed with mips')


if __name__=='__main__':main()
