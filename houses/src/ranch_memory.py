"""Explicit source-map manifest and planned compressed full-family allocation.

Old experiments under build/ are not package inputs. This manifest names
only the original five sets and the sixteen ranch maps currently bound.
"""
from pathlib import Path
import json
from PIL import Image
from textures import SETS


def check(out=Path('build/ranch/memory.json')):
 rows=[]
 for name,(size,coverage) in SETS.items():
  for channel in ('BaseColor','Normal','ORM'):
   rows.append((Path('textures/source')/f'T_House{name}_{channel}.png',size,'original family'))
 for color in ('red','red_brown','buff','tan'):
  folder=Path('build/ranch/materials')/color
  if any(not (folder/f'T_RanchBrick_{c}.png').exists() for c in ('BaseColor','Normal','ORM')):
   from ranch_fields import brick
   brick(folder,color)
  for channel in ('BaseColor','Normal','ORM'):
   rows.append((Path('build/ranch/materials')/color/f'T_RanchBrick_{channel}.png',512,'ranch brick'))
 for channel in ('BaseColor','Normal','ORM'):rows.append((Path('build/ranch/materials/roof')/f'T_RanchRoof_{channel}.png',1024,'ranch roof'))
 rows.append((Path('build/ranch/materials/trim/T_RanchTrim_ORM.png'),1024,'ranch trim ORM'))
 images=[]
 for file,size,group in rows:
  im=Image.open(file);assert im.size==(size,size),(file,im.size)
  # BC7/BC5 each use 16 bytes per 4x4 block; full-mip estimate rounds
  # negligibly at the last few levels. No engine-specific residency claim.
  images.append(dict(path=str(file),size=size,png_bytes=file.stat().st_size,group=group,gpu_mib=size*size*4/3/1048576))
 total=sum(r['gpu_mib'] for r in images);assert len(images)==31 and total<=48
 result=dict(passed=True,unique_images=len(images),source_png_bytes=sum(r['png_bytes'] for r in images),planned_gpu_mib=total,images=images,
  scope='Before-bake source map sizes, planned BC7/BC5 full mips; unused experiments are not package inputs')
 out.write_text(json.dumps(result,indent=2));print('RANCH_MEMORY',len(images),'images;',round(total,6),'MiB compressed with mips')
 return result


if __name__=='__main__':check()
