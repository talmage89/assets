"""Source-preview allocation audit; cape_delivery_check audits shipped maps."""
import json
from pathlib import Path
from ranch_memory import check as family_memory
from PIL import Image
import numpy as np


def check():
    # These ignored neighbors may not have been built on a fresh clone yet.
    # Recreate only missing source fields; never overwrite accepted maps.
    roof_folder=Path('build/ranch/materials/roof')
    if any(not (roof_folder/f'T_RanchRoof_{c}.png').exists() for c in ('BaseColor','Normal','ORM')):
        from ranch_fields import roof
        roof(roof_folder)
    trim=Path('build/ranch/materials/trim')
    if not (trim/'T_RanchTrim_ORM.png').exists():
        from ranch_fields import trim_orm
        trim_orm(trim,Path('textures/source/T_HouseTrim_ORM.png'))
    prior=family_memory();folder=Path('build/cape/materials/shingles');rows=[]
    for channel in ('BaseColor','Normal','ORM'):
        path=folder/f'T_CapeShingle_{channel}.png';size=Image.open(path).size;assert size==(512,512)
        pixels=np.asarray(Image.open(path))
        if channel=='BaseColor':assert np.ptp(pixels[:,:,0])>80,'Shingle base field lost its unit/keyway variation'
        if channel=='Normal':assert np.ptp(pixels[:,:,0])>30 and np.median(pixels[:,:,2])>200,'Shingle normal field is clamped/flat'
        if channel=='ORM':assert np.max(pixels[:,:,2])==0,'Cedar/cement must remain dielectric'
        rows.append(dict(path=str(path),size=size,preview_png_bytes=path.stat().st_size,gpu_mib=size[0]*size[1]*4/3/1048576))
    previews=rows;rows=[]
    for name,w,h in (('CapeCedar',512,256),('CapeCement',512,256),('CapeBrick',256,256),('CapeConcrete',256,256)):
        for channel in ('BaseColor','Normal'):rows.append(dict(name=f'T_{name}_{channel}.png',size=[w,h],gpu_mib=w*h*4/3/1048576))
    before=prior['planned_gpu_mib'];after=before+sum(r['gpu_mib'] for r in rows)
    reused_roof=[]
    for channel in ('BaseColor','Normal','ORM'):
        name=f'T_RanchRoof_{channel}.png';original=Path('build/ranch/materials/roof')/name;copy=Path('build/cape/materials/roof')/name
        assert original.read_bytes()==copy.read_bytes(),f'Cape must reuse the existing family roof: {channel}'
        reused_roof.append(str(original))
    units=json.loads((folder/'manufacture.json').read_text())['units']
    cedar=[u for u in units if u['kind']=='cedar'];cement=[u for u in units if u['kind']=='cement']
    assert all(.0762-1e-8<=u['width_m']<=.254+1e-8 and abs(u['exposure_m']-.1524)<1e-8 for u in cedar)
    assert all(abs(u['width_m']-.6096)<1e-8 and abs(u['exposure_m']-.2794)<1e-8 for u in cement)
    result=dict(passed=True,family_before_mib=before,planned_family_after_mib=after,addition_mib=after-before,new_images=rows,
        scope='BC7 BaseColor / BC5 Normal with full mips; exact scalar dielectric ORM frees the masonry allocation. Delivery audit reads actual published files.',
        justification='Four 512x256 wall-shingle color/normal images plus four 256-square masonry color/normal images total 1 MiB. Constant ORM needs no images. All accepted original maps stay unchanged.')
    result['cedar_unit_width_range_m']=[min(u['width_m'] for u in cedar),max(u['width_m'] for u in cedar)]
    result['byte_identical_reused_roof_maps']=reused_roof
    Path('build/cape/memory.json').write_text(json.dumps(result,indent=2));print('CAPE_MEMORY',before,'->',after,'MiB; planned addition',after-before)
    return result

if __name__=='__main__':check()
