"""Retain fractional ammo keys alongside the established 60-Hz rig export.

Forced Blender sampling rounds pickup/pivot boundaries to whole source frames.
Native export retains those boundaries, but sparse Euler rotations on the
other controls need their existing 60-Hz sampling. Copy only ammo samplers;
all mesh, image, skin, socket and other animation data remain untouched.
"""
import json,struct,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB

AMMO={'CycleCase','ChamberRound','TopRound','ReserveRound','Follower'}

def merge(path,native):
    base,detail=GLB(Path(path)),GLB(Path(native));data=base.json;binary=bytearray(base.binary)
    names=lambda g:{n['name']:i for i,n in enumerate(g.json['nodes']) if 'name' in n}
    a,b=names(base),names(detail)
    for name in AMMO:
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
            if name not in AMMO:continue
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

def export(path,objects):
    from kit import weapon as W
    path=Path(path);native=path.with_name(path.stem+'-native-sampling.glb')
    W.export(path,objects)
    W.export(native,objects,animations={'force_sampling':False})
    report=merge(path,native)
    path.with_suffix('.sampling.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':
    import argparse,bpy
    from kit import weapon as W
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));arm=bpy.data.objects['B24Armature'];W.pose(arm,None,0)
    parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==arm and 'bone' in o]
    joined=W.joined_copy(parts,'AnimationSampling');joined.parent=arm
    mod=joined.modifiers.new('Rigid sampling skin','ARMATURE');mod.object=arm
    native=Path(a.source).parent/'native-ammo-sampling.glb'
    W.export(native,[arm,joined],animations={'force_sampling':False})
    report=merge(Path(a.out),native)
    (Path(a.source).parent/'animation-sampling.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PRESERVED',report['count'],'ammo channels; other channels keep established 60-Hz sampling')
