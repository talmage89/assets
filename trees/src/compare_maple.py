"""Compare a preserved pre-refactor maple with rebuilt source and delivery.

Before editing: copy trees/{build,textures,export} into a worktree-local build
folder. Keep an original-map re-export separate from the new GPU rebake. This
checks actual bytes; it does not mislabel GPU rounding noise as exact equality.
"""
import argparse,hashlib,json,struct
from pathlib import Path
import numpy as np
from PIL import Image

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def glb(path):
    data=path.read_bytes();size=struct.unpack_from('<I',data,12)[0]
    return json.loads(data[20:20+size]),data[28+size:]
def main():
    p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--trees',type=Path,required=True)
    p.add_argument('--original-map-glb',type=Path,required=True);p.add_argument('--control-ship',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    old=a.baseline/'export/RedMaple.glb';new=a.trees/'export/RedMaple.glb'
    A,ab=glb(old);B,bb=glb(new);accessors=[]
    for i,(x,y) in enumerate(zip(A['accessors'],B['accessors'])):
        assert x==y, 'Accessor schema changed'
        va=A['bufferViews'][x['bufferView']];vb=B['bufferViews'][y['bufferView']]
        oa=va.get('byteOffset',0);ob=vb.get('byteOffset',0)
        equal=ab[oa:oa+va['byteLength']]==bb[ob:ob+vb['byteLength']]
        accessors.append(dict(index=i,type=x['type'],count=x['count'],byte_identical=equal));assert equal
    assert len(A['accessors'])==len(B['accessors'])
    assert old.read_bytes()==a.original_map_glb.read_bytes(), 'GLB differs with original map inputs'
    maps=[]
    for file in sorted((a.baseline/'textures/ship').glob('*.png')):
        candidate=a.trees/'textures/ship'/file.name
        x=np.asarray(Image.open(file)).astype(int);y=np.asarray(Image.open(candidate)).astype(int);d=np.abs(x-y)
        channels=np.argwhere(d>0)
        maps.append(dict(file=file.name,byte_identical=file.read_bytes()==candidate.read_bytes(),
                         original_bytes=file.stat().st_size,rebuilt_bytes=candidate.stat().st_size,
                         original_sha256=sha(file),rebuilt_sha256=sha(candidate),
                         max_channel_delta=int(d.max()),changed_channels=int((d>0).sum()),
                         changed_pixel_channels_yxc=channels.tolist(),rmse_bytes=float(np.sqrt(np.mean(d.astype(float)**2)))))
        assert d.max()<=1 and (d>0).sum()<100, 'Unexpected rebake regression'
    original_growth=a.baseline/'growth.json'
    if not original_growth.exists():original_growth=a.baseline/'build/growth.json'
    assert original_growth.read_bytes()==(a.trees/'build/growth.json').read_bytes(), 'Growth graph changed'
    report=dict(passed=True,growth_json_byte_identical=True,accessors=accessors,
                original_map_reexport_byte_identical=True,original_glb_sha256=sha(old),original_map_reexport_sha256=sha(a.original_map_glb),
                rebuilt_glb_sha256=sha(new),original_glb_bytes=old.stat().st_size,rebuilt_glb_bytes=new.stat().st_size,
                maps=maps,scope='All geometry/UV/normal/tangent/Wind/index accessor bytes and unchanged-map GLB; fresh GPU bake rounding reported explicitly')
    if a.control_ship:
        control=[]
        for row in maps:
            x=np.asarray(Image.open(a.baseline/'textures/ship'/row['file'])).astype(int)
            y=np.asarray(Image.open(a.control_ship/row['file'])).astype(int);d=np.abs(x-y)
            control.append(dict(file=row['file'],max_channel_delta=int(d.max()),changed_channels=int((d>0).sum())))
        report['unchanged_source_gpu_control']=control
    a.out.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
