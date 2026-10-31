"""Before/after allocation proposal; no new maps are published or baked."""
import json
from pathlib import Path
from ranch_memory import check as family_memory
from PIL import Image
import numpy as np


def check():
    prior=family_memory();folder=Path('build/cape/materials/shingles');rows=[]
    for channel in ('BaseColor','Normal','ORM'):
        path=folder/f'T_CapeShingle_{channel}.png';size=Image.open(path).size;assert size==(512,512)
        pixels=np.asarray(Image.open(path))
        if channel=='BaseColor':assert np.ptp(pixels[:,:,0])>80,'Shingle base field lost its unit/keyway variation'
        if channel=='Normal':assert np.ptp(pixels[:,:,0])>30 and np.median(pixels[:,:,2])>200,'Shingle normal field is clamped/flat'
        if channel=='ORM':assert np.max(pixels[:,:,2])==0,'Cedar/cement must remain dielectric'
        rows.append(dict(path=str(path),size=size,preview_png_bytes=path.stat().st_size,gpu_mib=size[0]*size[1]*4/3/1048576))
    before=prior['planned_gpu_mib'];after=before+sum(r['gpu_mib'] for r in rows)
    units=json.loads((folder/'manufacture.json').read_text())['units']
    cedar=[u for u in units if u['kind']=='cedar'];cement=[u for u in units if u['kind']=='cement']
    assert all(.0762-1e-8<=u['width_m']<=.254+1e-8 and abs(u['exposure_m']-.1524)<1e-8 for u in cedar)
    assert all(abs(u['width_m']-.6096)<1e-8 and abs(u['exposure_m']-.3048)<1e-8 for u in cement)
    result=dict(passed=True,family_before_mib=before,planned_family_after_mib=after,addition_mib=after-before,new_images=rows,
        scope='Planned BC7 BaseColor / BC5 Normal / BC7 ORM with full mips. Original previews only; no delivery bake or image publication.',
        justification='One 512-square two-region tile for irregular cedar units and large asbestos-cement shingles. Existing lap siding cannot represent these joints. Wood, vinyl, aluminum, roof, brick, concrete, trim and storms reuse family fields; vertex tint varies paint and age.')
    result['cedar_unit_width_range_m']=[min(u['width_m'] for u in cedar),max(u['width_m'] for u in cedar)]
    Path('build/cape/memory.json').write_text(json.dumps(result,indent=2));print('CAPE_MEMORY',before,'->',after,'MiB; planned addition',after-before)
    return result

if __name__=='__main__':check()
