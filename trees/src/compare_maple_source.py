"""Independent pre/post-refactor source geometry, normals, Wind and image audit.

BLEND container bytes contain paths/save state and are not the equality target.
The field arrays and packed PNG inputs are compared as exact byte strings.
"""
import argparse,hashlib,json,sys
from pathlib import Path
from array import array
import bpy

def floats(rows):
    return array('f',[v for row in rows for v in row]).tobytes()
def signature(path):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
    result={}
    for ob in sorted((o for o in bpy.context.scene.objects if o.type=='MESH'),key=lambda o:o.name):
        me=ob.data;me.calc_loop_triangles()
        fields=dict(position=floats([v.co for v in me.vertices]),
                    normals=floats([n.vector for n in me.corner_normals]),
                    wind=floats([v.color for v in me.color_attributes['Wind'].data]),
                    triangles=array('I',[i for t in me.loop_triangles for i in t.vertices]).tobytes())
        if me.uv_layers:fields['uv']=floats([v.uv for v in me.uv_layers.active.data])
        result[ob.name]={k:hashlib.sha256(v).hexdigest() for k,v in fields.items()}
    result['packed_pngs']={im.name:hashlib.sha256(bytes(im.packed_file.data)).hexdigest() for im in bpy.data.images if im.packed_file}
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);before=signature(a.before);after=signature(a.after)
    report=dict(passed=before==after,before=before,after=after,
                scope='Exact source position/triangle/UV/split-normal/Wind bytes and four packed procedural PNG files; BLEND save containers excluded')
    a.out.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));assert report['passed'],'Maple source regression'
if __name__=='__main__':main()
