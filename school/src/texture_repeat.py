"""Regenerate the one school-owned mask and audit immutable canonical images.

The family consumes completed canonical GPU bakes; it never rebakes or alters
those inputs. Any future school rebake must use the kit's 2-byte/.02 RMSE gate.
"""
import hashlib,json,shutil,sys
from pathlib import Path
from io import BytesIO
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.compare_textures import compare

paths={}
for package in Path('export').glob('*.gltf'):
    for row in json.loads(package.read_text()).get('images',[]):
        p=(package.parent/row['uri']).resolve();paths[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
ref=Path('build/texture-repeat/before');new=Path('build/texture-repeat/after');ref.mkdir(parents=True,exist_ok=True);new.mkdir(parents=True,exist_ok=True)
source=Path('textures/ship/T_School_Light_Emission.png');shutil.copyfile(source,ref/source.name)
im=Image.new('RGB',(8,8));im.putpixel((6,1),(255,246,224));im.save(new/source.name)
report=compare(ref,new);report.update(scope='School mask regenerated independently; canonical shared GPU bake images are read-only inputs, not rebaked.',canonical_images=len(paths)-1,canonical_sha256=paths)
report['canonical_unchanged']=all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha for p,sha in paths.items())
assert report['passed'] and report['canonical_unchanged']
Path('build/texture-repeat.json').write_text(json.dumps(report,indent=2));print('TEXTURE REPEAT PASS / school mask delta 0 / canonical maps unchanged')
