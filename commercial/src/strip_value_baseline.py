"""Reframe the accepted geometry with its original procedural deposit sheet.

The immutable takeover capture remains untouched. This ignored diagnostic
reproduces only comparison inputs; it never writes a shipping file.
"""
import json,subprocess,sys,types
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from PIL import Image


def prepare():
    baseline=Path('build/strip-value/before/export/CommercialStrip-202.gltf')
    if not baseline.exists():return None
    folder=Path('build/strip-value/reframed-source');folder.mkdir(parents=True,exist_ok=True)
    old=types.ModuleType('_baseline_strip_art');exec(compile(subprocess.check_output(['git','show','f204c56:commercial/src/strip_art.py']),'<accepted strip artwork>','exec'),old.__dict__)
    image=Image.new('RGBA',(2048,2048));records={};old.populate(image,records,folder);image.save(folder/'T_StripSigns_BaseColor.png')
    # Verify the regenerated old art against its actual accepted GLB payload,
    # mapping the binary rather than reading the whole package into memory.
    accepted=Path('build/strip-value/before/embedded-201.glb')
    if accepted.exists():
        import hashlib
        from strip_value_controls import document,digest
        olddoc,binary=document(accepted);proof=[]
        for item in olddoc['images']:
            if not item.get('name','').startswith('T_StripSigns_'):continue
            view=olddoc['bufferViews'][item['bufferView']];start=view.get('byteOffset',0)
            expected=hashlib.sha256(binary[start:start+view['byteLength']]).hexdigest();path=folder/(item['name']+'.png')
            assert digest(path)==expected,('Original chart reproduction differs',path)
            proof.append(dict(image=path.name,sha256=expected))
        assert len(proof)==2,proof
        (folder/'chart-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
    doc=json.loads(baseline.read_text())
    for item in doc['images']:
        path=(Path('export')/item['uri']).resolve()
        if path.name.startswith('T_StripSigns_'):path=(folder/path.name).resolve()
        item['uri']=str(path)
    doc['buffers'][0]['uri']=str(baseline.with_suffix('.bin').resolve())
    out=folder/baseline.name;out.write_text(json.dumps(doc));out.with_suffix('.json').write_bytes(baseline.with_suffix('.json').read_bytes())
    return out


if __name__=='__main__':
    source=prepare()
    if source:
        from strip_render import render,sha,recipe
        from strip_photo_matches import LIGHTING
        from strip_matches import EXPOSURE
        cameras=json.loads(Path('build/strip/cameras.json').read_text());row=cameras['period_lot'];row['shot'].update(LIGHTING['period_lot']);row['shot']['exposure']=EXPOSURE['period_lot']
        out=Path('renders/strip/value-before-reframed');receipt=out/'provenance.json'
        old=json.loads(receipt.read_text()).get('period_lot',{}) if receipt.exists() else {}
        current=(out/'period_lot.png').exists() and old.get('sha256')==sha(source) and old.get('recipe_sha256')==recipe() and old.get('shot')==json.loads(json.dumps(row['shot'])) and old.get('image_sha256')==sha(out/'period_lot.png')
        if current:print('REFRAMED BASELINE cached current source, camera, recipe and image PASS')
        else:render(202,Path('build/strip-look'),out,['period_lot'],1600,40,{'period_lot':row},source_override=source)
