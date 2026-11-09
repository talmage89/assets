"""Guard one native PinOak tangent's four-decimal export rounding boundary.

The accepted tangent comes from the immutable native input, never a previous
garage/site delivery. Kit guards the exact position/normal/UV and permits only
one four-decimal tangent step. Geometry, UVs and every other tangent stay intact.
"""
import copy
import hashlib
import json
from pathlib import Path
import struct

import numpy as np
from kit.gltf import GLB,stabilize_tangents

ROOT=Path(__file__).resolve().parents[2]
SIGNATURE=dict(position=[.1928449273109436,3.4985604286193848,-.0159536711871624],
    normal=[.9714162945747375,.00920015387237072,-.23720398545265198],
    uv=[.48928847908973694,.29691773653030396])


def find(g):
    hits=[]
    for mi,mesh in enumerate(g.json['meshes']):
        for pi,primitive in enumerate(mesh['primitives']):
            attrs=primitive['attributes']
            if not all(k in attrs for k in ('POSITION','NORMAL','TEXCOORD_0','TANGENT')):continue
            count=g.json['accessors'][attrs['POSITION']]['count'];match=np.ones(count,dtype=bool)
            for key,attribute in (('position','POSITION'),('normal','NORMAL'),('uv','TEXCOORD_0')):
                match &= np.all(g.accessor(attrs[attribute])==np.asarray(SIGNATURE[key],dtype=np.float32),axis=1)
            for vi in np.flatnonzero(match):hits.append(dict(mesh=mi,primitive=pi,vertex=int(vi),**SIGNATURE))
    assert len(hits)==1,('Native rounding anchor must remain unique',len(hits))
    return hits[0]


def stabilize(path):
    path=Path(path);native=ROOT/'trees/export/PinOak.glb';source=GLB(native);source_anchor=find(source)
    primitive=source.json['meshes'][source_anchor['mesh']]['primitives'][source_anchor['primitive']]
    accepted=source.accessor(primitive['attributes']['TANGENT'])[source_anchor['vertex']].tolist()
    doc=json.loads(path.read_text());binary_path=path.parent/doc['buffers'][0]['uri'];binary=binary_path.read_bytes()
    # Give the existing kit guard a GLB envelope around the external BIN. The
    # envelope is diagnostic only; public JSON and canonical image URIs persist.
    packed=copy.deepcopy(doc);packed['buffers'][0].pop('uri')
    raw=json.dumps(packed,separators=(',',':')).encode();raw+=b' '*(-len(raw)%4)
    data=binary+b'\0'*(-len(binary)%4)
    payload=struct.pack('<II',len(raw),0x4e4f534a)+raw+struct.pack('<II',len(data),0x004e4942)+data
    folder=Path('build/tangent-rounding');folder.mkdir(parents=True,exist_ok=True);wrapper=folder/path.with_suffix('.glb').name
    wrapper.write_bytes(struct.pack('<III',0x46546c67,2,12+len(payload))+payload)
    anchor=find(GLB(wrapper));anchor['tangent']=accepted
    stabilize_tangents(wrapper,[anchor]);binary_path.write_bytes(GLB(wrapper).binary[:len(binary)])
    report=dict(source='trees/export/PinOak.glb',source_sha256=hashlib.sha256(native.read_bytes()).hexdigest(),
        anchor=anchor,scope='Only the guarded native tangent; exact position/normal/UV, one four-decimal-step maximum. Byte-exact repeat remains required.')
    (folder/path.with_suffix('.json').name).write_text(json.dumps(report,indent=2)+'\n')
    print('NATIVE TANGENT GUARD',path.name,1,'anchor',flush=True)
