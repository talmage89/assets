"""Family export with retained SUV corner fields and smooth optical shells.

The optical shader has no normal-height detail. Its real mesh normals carry
curvature; the shared normal image's quantization must not perturb refraction.
Only its standard glTF normalTexture scale changes; maps and geometry stay put.
"""
import argparse,json,struct,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import export
from kit.gltf import GLB


def main():
    p=argparse.ArgumentParser(add_help=False);p.add_argument('--out',required=True);p.add_argument('--report',required=True)
    a,_=p.parse_known_args(sys.argv[sys.argv.index('--')+1:])
    attach=export.G.attach
    def retained_attach(ob,parent,*args,**kwargs):
        result=attach(ob,parent,*args,**kwargs);field=ob.data.attributes.get('X220ExportNormal')
        if field:
            bpy.context.view_layer.update()
            inverse=ob.matrix_world.to_3x3().transposed()
            ob.data.normals_split_custom_set([inverse@d.vector for d in field.data])
        return result
    export.G.attach=retained_attach
    export.main()
    path=Path(a.out);g=GLB(path)
    for material in g.json['materials']:
        if material['name']=='AlderX220 Glass':
            material['normalTexture']['scale']=0
            material.setdefault('extras',{})['normal_policy']='Smooth molded shell; curvature from retained vertex normals, no texture perturbation'
    data=json.dumps(g.json,separators=(',',':')).encode();data+=b' '*((-len(data))%4)
    payload=struct.pack('<II',len(data),0x4e4f534a)+data+struct.pack('<II',len(g.binary),0x004e4942)+g.binary
    path.write_bytes(struct.pack('<III',0x46546c67,2,12+len(payload))+payload)
    report_path=Path(a.report);report=json.loads(report_path.read_text());report['bytes']=path.stat().st_size;report['optical_normal_texture_scale']=0
    report_path.write_text(json.dumps(report,indent=2));print('X220_EXPORTED',path.stat().st_size,'bytes; retained corner fields, smooth optical shell')


if __name__=='__main__':main()
