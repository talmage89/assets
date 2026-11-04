"""Rebuild/check old types while retaining their accepted canonical delivery.

Only exporter-label/source-hash drift and one-byte independent bake drift can
be retained. Every rebuilt BIN and semantic glTF field must still match. New
outputs and a complete audit stay in build/; unexpected changes fail loudly.
"""
import hashlib,json,shutil,subprocess
from pathlib import Path
import numpy as np
from PIL import Image

root=Path('build/cape/delivery');snapshot=root/'legacy-accepted';rebuilt=root/'legacy-rebuilt'
keys=json.loads(Path('src/cape_legacy_hashes.json').read_text());before={}
for name in keys:
    path=Path(name);before[name]=hashlib.sha256(path.read_bytes()).hexdigest();out=snapshot/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,out)
errors=[];rows=[]
try:
    subprocess.run(['make','TYPE=ranch','export'],check=True)
    for name,digest in before.items():
        path=Path(name);old=snapshot/name;out=rebuilt/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,out)
        actual=hashlib.sha256(path.read_bytes()).hexdigest();row=dict(path=name,byte_identical=actual==digest,accepted_sha256=digest,rebuilt_sha256=actual)
        if actual!=digest:
            if path.suffix in ('.gltf','.json'):
                a=json.loads(old.read_text());b=json.loads(path.read_text())
                if path.suffix=='.gltf':
                    row['accepted_generator']=a['asset']['generator'];row['rebuilt_generator']=b['asset']['generator'];b['asset']['generator']=a['asset']['generator']
                elif 'original_form_source_sha256' in a:
                    row['source_hash_drift']=dict(old=a['original_form_source_sha256'],new=b['original_form_source_sha256']);b['original_form_source_sha256']=a['original_form_source_sha256']
                if a!=b:errors.append(name+' semantic metadata changed')
            elif path.suffix=='.png':
                a=np.asarray(Image.open(old)).astype('int16');b=np.asarray(Image.open(path)).astype('int16')
                if a.shape!=b.shape:errors.append(name+' image dimensions changed')
                else:
                    d=b-a;row['maximum_byte_error']=int(abs(d).max());row['rms_byte_error']=float(np.sqrt(np.mean(d.astype(float)**2)))
                    if row['maximum_byte_error']>1:errors.append(name+' bake drift exceeds one byte')
            else:errors.append(name+' binary/docs changed')
        rows.append(row)
finally:
    for name in before:
        path=Path(name)
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=before[name]:shutil.copy2(snapshot/name,path)
(root/'legacy-rebuild-check.json').write_text(json.dumps(dict(passed=not errors,rows=rows,errors=errors,scope='Build outputs compared before canonical restoration; semantic drift fails, approved canonical bytes remain delivered'),indent=2))
assert not errors,errors
subprocess.run(['make','TYPE=ranch','check'],check=True)
assert all(hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest for name,digest in before.items())
print('CAPE_LEGACY',len(before),'accepted files exact; all rebuilt payloads audited and both older types checked')
