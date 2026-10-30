"""Retain fractional ammo keys alongside the established 60-Hz rig export.

Forced Blender sampling rounds pickup/pivot boundaries to whole source frames.
Native export retains those boundaries, but sparse Euler rotations on the
other controls need their existing 60-Hz sampling. Copy only ammo samplers;
all mesh, image, skin, socket and other animation data remain untouched.
"""
import json,struct,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB


def merge(path,native,bones):
    base,detail=GLB(Path(path)),GLB(Path(native));data=base.json;binary=bytearray(base.binary)
    names=lambda g:{n['name']:i for i,n in enumerate(g.json['nodes']) if 'name' in n}
    a,b=names(base),names(detail)
    for name in bones:
        assert np.max(abs(base.local(a[name])-detail.local(b[name])))<1e-6,(name,'rest frame')
    def append(index):
        source=detail.json['accessors'][index];arr=detail.accessor(index)
        assert source['componentType']==5126 and not source.get('normalized')
        while len(binary)%4:binary.append(0)
        view=len(data['bufferViews']);payload=arr.astype('<f4').tobytes()
        data['bufferViews'].append(dict(buffer=0,byteOffset=len(binary),byteLength=len(payload)));binary.extend(payload)
        entry=dict(bufferView=view,componentType=5126,count=len(arr),type=source['type'])
        for key in ('min','max'):
            if key in source:entry[key]=source[key]
        result=len(data['accessors']);data['accessors'].append(entry);return result
    changed=[]
    native_actions={a['name']:a for a in detail.json['animations']}
    for animation in data['animations']:
        native_action=native_actions[animation['name']]
        channels={(detail.json['nodes'][c['target']['node']]['name'],c['target']['path']):c
                  for c in native_action['channels']}
        for channel in animation['channels']:
            name=data['nodes'][channel['target']['node']]['name']
            if name not in bones:continue
            key=(name,channel['target']['path'])
            if key not in channels:continue
            sm=native_action['samplers'][channels[key]['sampler']]
            sampler=dict(input=append(sm['input']),output=append(sm['output']),
                         interpolation=sm.get('interpolation','LINEAR'))
            channel['sampler']=len(animation['samplers']);animation['samplers'].append(sampler)
            changed.append([animation['name'],name,key[1]])
    data['buffers'][0]['byteLength']=len(binary)
    encoded=json.dumps(data,separators=(',',':')).encode()
    encoded+=b' '*((-len(encoded))%4);binary+=b'\0'*((-len(binary))%4)
    body=struct.pack('<II',len(encoded),0x4e4f534a)+encoded+struct.pack('<II',len(binary),0x004e4942)+binary
    Path(path).write_bytes(struct.pack('<III',0x46546c67,2,12+len(body))+body)
    return dict(channels=changed,count=len(changed),scope='ammo input/output accessors only; all other data retained')

def export(path,objects,bones):
    from kit import weapon as W
    path=Path(path);native=path.with_name(path.stem+'-native-sampling.glb')
    W.export(path,objects)
    densify(bones)
    W.export(native,objects,animations={'force_sampling':False})
    report=merge(path,native,bones)
    path.with_suffix('.sampling.json').write_text(json.dumps(report,indent=2)+'\n')


def densify(bones):
    """Retain native boundaries, with exact quarter-frame affine checkpoints.

    A sparse Euler segment becomes quaternion interpolation in glTF. Blender's
    importer linearly evaluates quaternion components, so that segment alone
    need not reproduce intermediate source angles. Subdivide its original
    component curves without changing their evaluated values or STEP meaning.
    This operates on the temporary export scene, after saving modeled source.
    """
    import bpy,bisect
    from kit import weapon as W
    for action in bpy.data.actions:
        curves=[fc for fc in W.fcurves(action) if any(
            fc.data_path.startswith('pose.bones["'+n+'"]') for n in bones)]
        if not curves:continue
        begin=min(k.co.x for fc in curves for k in fc.keyframe_points)
        end=max(k.co.x for fc in curves for k in fc.keyframe_points)
        frames=[i/4 for i in range(int(np.ceil(begin*4)),int(np.floor(end*4))+1)]
        for fc in curves:
            keys=list(fc.keyframe_points);times=[float(k.co.x) for k in keys]
            existing={round(t,5) for t in times}
            samples=[(f,float(fc.evaluate(f)),keys[max(0,bisect.bisect_right(times,f)-1)].interpolation)
                     for f in frames if round(f,5) not in existing]
            for f,value,interpolation in samples:
                key=fc.keyframe_points.insert(f,value,options={'FAST'});key.interpolation=interpolation
            fc.update()

if __name__=='__main__':
    import argparse,bpy
    from kit import weapon as W
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--bones',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');W.pose(arm,None,0)
    parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==arm and 'bone' in o]
    joined=W.joined_copy(parts,'AnimationSampling');joined.parent=arm
    mod=joined.modifiers.new('Rigid sampling skin','ARMATURE');mod.object=arm
    native=Path(a.source).parent/'native-feed-sampling.glb'
    densify(set(a.bones.split(',')))
    W.export(native,[arm,joined],animations={'force_sampling':False})
    report=merge(Path(a.out),native,set(a.bones.split(',')))
    (Path(a.source).parent/'feed-sampling.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PRESERVED',report['count'],'feed channels; other channels keep established 60-Hz sampling')
