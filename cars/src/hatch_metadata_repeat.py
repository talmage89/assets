"""Prove volatile form-container receipts cannot change the H120 delivery.

Run in Blender at one thread with --source (accepted finalized blend),
--textures, --baseline (accepted GLB), --forms (three cold form blends), --out.
Reuses accepted mesh/UV/maps to isolate provenance; performs no GPU rebake.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import bpy

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'cars/src'),str(ROOT)]
from hatch_detail import form_source_receipt
from kit import export


def glb(path):
    raw=path.read_bytes();length=int.from_bytes(raw[12:16],'little')
    return json.loads(raw[20:20+length]),raw[28+length:]


def main():
    parser=argparse.ArgumentParser()
    for key in ('source','textures','baseline','out'):parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--forms',nargs=3,type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    args.out.mkdir(parents=True,exist_ok=True)
    reference,binary=glb(args.baseline);expected=copy.deepcopy(reference)
    del expected['scenes'][0]['extras']['form_source_sha256']
    receipts=[]
    for index,form in enumerate(args.forms):
        bpy.ops.wm.open_mainfile(filepath=str(args.source.resolve()))
        scene=bpy.context.scene
        # Reproduce each cold source's varying value at the original leak.
        scene['form_source_sha256']=hashlib.sha256(form.read_bytes()).hexdigest()
        receipt=form_source_receipt(scene,form)
        assert 'form_source_sha256' not in scene
        assert receipt==hashlib.sha256(form.read_bytes()).hexdigest()
        source=args.out/f'finalized-{index}.blend'
        bpy.ops.wm.save_as_mainfile(filepath=str(source.resolve()))
        target=args.out/f'hatch-{index}.glb';report=args.out/f'export-{index}.json'
        sys.argv=['export.py','--','--source',str(source),'--textures',str(args.textures),
                  '--asset','AlderH120','--out',str(target),'--report',str(report),
                  '--config',str(ROOT/'cars/src/hatch_detail_config.py')]
        export.main()
        document,payload=glb(target)
        assert document==expected,('Unexpected GLB JSON change',index)
        assert payload==binary,('Geometry/maps changed',index)
        receipts.append(dict(form_source_sha256=receipt,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                             bytes=target.stat().st_size,triangles=json.loads(report.read_text())['triangles']))
    assert len({r['form_source_sha256'] for r in receipts})==3
    assert len({r['sha256'] for r in receipts})==1
    result=dict(passed=True,files=receipts,binary_payload_identical=True,
                only_change='Removed Scene extras form_source_sha256',
                scope='Three independent exports with three cold form receipts; accepted finalized mesh/UV/maps reused')
    (args.out/'repeat.json').write_text(json.dumps(result,indent=2)+'\n')
    print('H120 METADATA REPEAT PASS',result,flush=True)


if __name__=='__main__':main()
