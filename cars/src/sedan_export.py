"""Sedan export: fair optical/coated skins use their actual limit normals.

The laminate/optic form already lives in the exported corner normals. Sampling
an 8-bit tangent normal adds chart-dependent angular quantization, visible as
a torn softbox reflection. Glass uses its continuous mesh normals; the other
opaque detail retains the shared normal atlas. Binary geometry/images are untouched.
"""
import argparse,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import export
from kit.gltf import GLB


def main():
    parser=argparse.ArgumentParser(add_help=False);parser.add_argument('--out',required=True);parser.add_argument('--report',required=True)
    args,_=parser.parse_known_args(sys.argv[sys.argv.index('--')+1:]);export.main()
    path=Path(args.out);glb=GLB(path);changed=[]
    for material in glb.json['materials']:
        if material['name'] in ['AlderS240 Glass','AlderS240 Paint']:
            material.pop('normalTexture',None);changed.append(material['name'])
            material.get('extensions',{}).get('KHR_materials_clearcoat',{}).pop('clearcoatNormalTexture',None)
    if sorted(changed)!=['AlderS240 Glass','AlderS240 Paint']:raise ValueError('Missing or duplicated fair delivery surface')
    document=json.dumps(glb.json,separators=(',',':')).encode();document+=b' '*((-len(document))%4)
    payload=struct.pack('<II',len(document),0x4e4f534a)+document+struct.pack('<II',len(glb.binary),0x004e4942)+glb.binary
    path.write_bytes(struct.pack('<III',0x46546c67,2,12+len(payload))+payload)
    report=json.loads(Path(args.report).read_text());report['bytes']=path.stat().st_size
    report['smooth_limit_materials']=changed;report['smooth_normal_policy']='Continuous exported limit normals; no unresolved tangent relief on glass or paint'
    Path(args.report).write_text(json.dumps(report,indent=2));print('S240_SMOOTH_OPTICAL_EXPORT',changed,report['bytes'],flush=True)
if __name__=='__main__':main()
