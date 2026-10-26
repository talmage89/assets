"""Consolidate identical texture views in our own exported GLB; keep BIN bytes intact."""
import json,struct
from pathlib import Path

def compact(path,scratch):
    path=Path(path);raw=path.read_bytes();magic,version,total=struct.unpack_from('<III',raw)
    if magic!=0x46546c67 or version!=2 or total!=len(raw):raise ValueError('Invalid exported GLB')
    chunks=[];offset=12
    while offset<len(raw):
        size,kind=struct.unpack_from('<II',raw,offset);chunks.append([kind,raw[offset+8:offset+8+size]]);offset+=8+size
    doc=next(c for c in chunks if c[0]==0x4e4f534a);data=json.loads(doc[1]);old=data.get('textures',[]);unique=[];lookup={};remap={}
    for i,texture in enumerate(old):
        key=json.dumps(texture,sort_keys=True,separators=(',',':'))
        if key not in lookup:lookup[key]=len(unique);unique.append(texture)
        remap[i]=lookup[key]
    if len(unique)==len(old):return dict(before=len(old),after=len(unique),binary_preserved=True)
    def rewrite(node):
        if isinstance(node,dict):
            for key,value in node.items():
                if key.endswith('Texture') and isinstance(value,dict) and 'index' in value:value['index']=remap[value['index']]
                else:rewrite(value)
        elif isinstance(node,list):
            for value in node:rewrite(value)
    rewrite(data.get('materials',[]));data['textures']=unique
    payload=json.dumps(data,separators=(',',':'),ensure_ascii=False).encode();doc[1]=payload+b' '*((-len(payload))%4)
    output=b''.join(struct.pack('<II',len(payload),kind)+payload for kind,payload in chunks)
    output=struct.pack('<III',magic,version,12+len(output))+output
    folder=Path(scratch);folder.mkdir(parents=True,exist_ok=True);temp=folder/(path.name+'.deduplicated');temp.write_bytes(output);temp.replace(path)
    return dict(before=len(old),after=len(unique),binary_preserved=True)
