"""Before/after allocation proposal; no new maps are published or baked."""
import json
from pathlib import Path
from ranch_memory import check as family_memory
from PIL import Image


def check():
    prior=family_memory();folder=Path('build/cape/materials/shingles');rows=[]
    for channel in ('BaseColor','Normal','ORM'):
        path=folder/f'T_CapeShingle_{channel}.png';size=Image.open(path).size;assert size==(512,512)
        rows.append(dict(path=str(path),size=size,preview_png_bytes=path.stat().st_size,gpu_mib=size[0]*size[1]*4/3/1048576))
    before=prior['planned_gpu_mib'];after=before+sum(r['gpu_mib'] for r in rows)
    result=dict(passed=True,family_before_mib=before,planned_family_after_mib=after,addition_mib=after-before,new_images=rows,
        scope='Planned BC7 BaseColor / BC5 Normal / BC7 ORM with full mips. Original previews only; no delivery bake or image publication.',
        justification='One 512-square two-region tile for irregular cedar units and large asbestos-cement shingles. Existing lap siding cannot represent these joints. Wood, vinyl, aluminum, roof, brick, concrete, trim and storms reuse family fields; vertex tint varies paint and age.')
    Path('build/cape/memory.json').write_text(json.dumps(result,indent=2));print('CAPE_MEMORY',before,'->',after,'MiB; planned addition',after-before)
    return result

if __name__=='__main__':check()
