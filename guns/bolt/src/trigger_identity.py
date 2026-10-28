"""Audit the trigger-only exception against the accepted pre-fix exports.

GLB joining necessarily shifts indices after a changed vertex count. Compare
the ordered triangle-corner attribute bytes instead, excluding only the rigid
Trigger bone. All rig/animation accessors and structural layout remain exact.
Run in Blender: --before build/trigger-before/export.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.gltf import GLB


def main():
    p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);rows={}
    for name in ('bolt','magazine_loaded','magazine_empty','case'):
        old=GLB(a.before/(name+'.glb'));new=GLB(BASE/'export'/(name+'.glb'))
        for key in ('nodes','skins','animations','scenes','scene','materials','textures','samplers','meshes'):
            assert old.json.get(key)==new.json.get(key),(name,key)
        attributes=set()
        trigger_joint=None
        if name=='bolt':
            skin=old.json['skins'][0]
            trigger_joint=next(i for i,n in enumerate(skin['joints']) if old.json['nodes'][n]['name']=='Trigger')
        triangles=[]
        for oi,ni in zip(old.json['meshes'],new.json['meshes']):
            for op,np_ in zip(oi['primitives'],ni['primitives']):
                indices=[g.accessor(pr['indices']).reshape(-1,3) for g,pr in ((old,op),(new,np_))]
                counts=[];masks=[]
                for g,pr,index in ((old,op,indices[0]),(new,np_,indices[1])):
                    mask=np.ones(len(index),dtype=bool)
                    if trigger_joint is not None:
                        joints=g.accessor(pr['attributes']['JOINTS_0']);weights=g.accessor(pr['attributes']['WEIGHTS_0'])
                        owners=np.take_along_axis(joints,np.argmax(weights,axis=1)[:,None],axis=1).ravel()
                        mask=np.all(owners[index]!=trigger_joint,axis=1)
                    counts.append(int((~mask).sum()));masks.append(mask)
                for key in op['attributes']:
                    oi_=op['attributes'][key];ni_=np_['attributes'][key];attributes.add(oi_)
                    left=old.accessor(oi_)[indices[0][masks[0]]].tobytes()
                    right=new.accessor(ni_)[indices[1][masks[1]]].tobytes()
                    assert left==right,(name,key,'non-trigger triangle bytes changed')
                attributes.add(op['indices']);triangles.append(counts)
        for i in range(len(old.json['accessors'])):
            if i not in attributes:
                assert old.accessor(i).tobytes()==new.accessor(i).tobytes(),(name,'rig/clip accessor',i)
        rows[name]=dict(passed=True,trigger_triangles_before_after=triangles,
            sha256=hashlib.sha256((BASE/'export'/(name+'.glb')).read_bytes()).hexdigest())
    report=dict(passed=True,scope='All non-trigger ordered triangle-corner bytes (position, normal, tangent, UV, joints, weights); rig, clips and layout exact. Images excluded.',outputs=rows)
    path=BASE/'build/trigger-identity.json';path.write_text(json.dumps(report,indent=2));print(path.read_text())


if __name__=='__main__':main()
