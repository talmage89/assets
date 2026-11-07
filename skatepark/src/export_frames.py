"""Guarded normal-map frame repair on this family's serialized copies.

MikkTSpace can emit a zero tangent at small bevel/cap fan junctions, including
a few vertices in the canonical trees. Keep geometry, UVs, images and valid
frames unchanged except two explicitly guarded Mikk rounding corners. Derive
missing frames from the largest incident UV triangle.
Untextured context does not consume tangent attributes and is left alone.
"""
import json,struct
from pathlib import Path
import numpy as np
from kit.gltf import GLB,stabilize_tangents

PIN_OAK_ROUNDING=dict(vertex=10396,
    position=[.1928449273109436,3.4985604286193848,-.0159536711871624],
    normal=[.9714162945747375,.00920015387237072,-.23720398545265198],
    uv=[.48928847908973694,.29691773653030396],
    tangent=[-.2372,.0031,-.9715,1.])

PIN_OAK_ROUNDINGS=[PIN_OAK_ROUNDING,dict(vertex=1703,
    position=[-.0946817547082901,4.496119976043701,.2046363651752472],
    normal=[-.6127699613571167,.00019999020150862634,.7902612686157227],
    uv=[.739832878112793,.22091996669769287],
    tangent=[.7898,-.0359,.6124,1.])]

def rounding_anchors(g):
    """Native oak corners straddling Mikk's fourth-decimal boundaries."""
    anchors=[]
    for mi,mesh in enumerate(g.json['meshes']):
        if not mesh.get('name','').startswith('Trunk and branches'):continue
        for pi,prim in enumerate(mesh['primitives']):
            attr=prim['attributes']
            if g.json['accessors'][attr['POSITION']]['count']!=14746:continue
            for accepted in PIN_OAK_ROUNDINGS:
                a=dict(accepted,mesh=mi,primitive=pi)
                for key,semantic in [('position','POSITION'),('normal','NORMAL'),('uv','TEXCOORD_0')]:
                    assert np.array_equal(g.accessor(attr[semantic])[a['vertex']],np.asarray(a[key],dtype=np.float32)),('Changed native rounding corner',key)
                actual=g.accessor(attr['TANGENT'])[a['vertex']]
                assert np.max(np.abs(actual-np.asarray(a['tangent'],dtype=np.float32)))<.00011,actual
                anchors.append(a)
    return anchors

def repair(path):
    path=Path(path);raw=bytearray(path.read_bytes());embedded=path.suffix=='.glb'
    if embedded:
        g=GLB(path);offset=12
        while True:
            length,kind=struct.unpack_from('<II',raw,offset)
            if kind==0x004e4942:bin_start=offset+8;break
            offset+=length+8
    else:
        g=object.__new__(GLB);g.json=json.loads(raw);g.binary=(path.parent/g.json['buffers'][0]['uri']).read_bytes();bin_start=0
    binary=bytearray(g.binary);receipts=[];visited=set()
    for mi,mesh in enumerate(g.json['meshes']):
        for pi,prim in enumerate(mesh['primitives']):
            mat=g.json['materials'][prim['material']]
            if 'normalTexture' not in mat:continue
            attr=prim['attributes'];ai=attr['TANGENT'];channel=mat['normalTexture'].get('texCoord',0)
            if (ai,channel) in visited:continue
            visited.add((ai,channel));n=g.accessor(attr['NORMAL']);t=g.accessor(ai);v=g.accessor(attr['POSITION']);uv=g.accessor(attr['TEXCOORD_'+str(channel)])
            ids=np.concatenate([g.accessor(p['indices']).reshape(-1,3) for p in mesh['primitives'] if p['attributes'].get('TANGENT')==ai and g.json['materials'][p['material']].get('normalTexture',{}).get('texCoord',0)==channel and 'normalTexture' in g.json['materials'][p['material']]])
            lengths=np.linalg.norm(t[:,:3],axis=1);dots=(n*t[:,:3]).sum(axis=1)
            bad=np.intersect1d(np.flatnonzero((np.abs(lengths-1)>.002)|(np.abs(dots)>.003)),np.unique(ids))
            if not len(bad):continue
            accessor=g.json['accessors'][ai];view=g.json['bufferViews'][accessor['bufferView']]
            assert accessor['componentType']==5126 and accessor['type']=='VEC4'
            for vertex in bad:
                normal=n[vertex].astype(float);normal/=np.linalg.norm(normal)
                incident=ids[np.any(ids==vertex,axis=1)];best=None
                for tri in incident:
                    p=v[tri].astype(float);q=uv[tri].astype(float);e1,e2=p[1]-p[0],p[2]-p[0];d1,d2=q[1]-q[0],q[2]-q[0];det=d1[0]*d2[1]-d1[1]*d2[0]
                    if abs(det)<1e-18:continue
                    tangent=(e1*d2[1]-e2*d1[1])/det;bitangent=(e2*d1[0]-e1*d2[0])/det
                    tangent-=normal*np.dot(normal,tangent);length=np.linalg.norm(tangent)
                    if length<1e-12:continue
                    score=np.linalg.norm(np.cross(e1,e2))
                    if best is None or score>best[0]:best=(score,tangent/length,bitangent)
                if best is None:
                    axis=np.eye(3)[np.argmin(abs(normal))];tangent=axis-normal*np.dot(normal,axis);tangent/=np.linalg.norm(tangent);hand=1.
                else:
                    tangent=best[1];hand=1. if np.dot(np.cross(normal,tangent),best[2])>=0 else -1.
                start=view.get('byteOffset',0)+accessor.get('byteOffset',0)+int(vertex)*view.get('byteStride',16)
                struct.pack_into('<4f',binary,start,*tangent,hand)
            receipts.append(dict(mesh=mesh.get('name',str(mi)),primitive=pi,vertices=len(bad),method='UV-derived unit tangent orthogonal to exported normal; axis fallback only at collapsed native cap charts'))
    anchors=rounding_anchors(g)
    if embedded:
        raw[bin_start:bin_start+len(binary)]=binary;path.write_bytes(raw)
        stabilize_tangents(path,anchors)
    else:
        # The kit helper consumes GLB. Apply its same exact-signature and
        # one-rounding-step guard to the companion external BIN as well.
        for a in anchors:
            attr=g.json['meshes'][a['mesh']]['primitives'][a['primitive']]['attributes'];accessor=g.json['accessors'][attr['TANGENT']];view=g.json['bufferViews'][accessor['bufferView']]
            start=view.get('byteOffset',0)+accessor.get('byteOffset',0)+a['vertex']*view.get('byteStride',16)
            struct.pack_into('<4f',binary,start,*a['tangent'])
        (path.parent/g.json['buffers'][0]['uri']).write_bytes(binary)
    path.with_suffix('.frames.json').write_text(json.dumps(dict(repaired_vertices=sum(r['vertices'] for r in receipts),guarded_rounding_corners=len(anchors),normal_mapped_primitives_only=True,geometry_and_UV_unchanged=True,repairs=receipts),indent=2))
    return receipts
