"""Shared-map reduction: closed UV seams, source records, weighted fields, residency."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from kit.lod_shared import collapse
from kit.lod_mesh import topology
from kit.lod_io import residency


def main():
    from kit.lod_shells import exposed_backfaces,preserve,protect_powered
    # Two closed constructions meet at one corner and cross farther inside.
    # Their hidden source skins must not emerge after independent collapse.
    p=np.array([[0,0,0],[2,0,0],[0,2,0],[0,0,2],[1.5,1.5,-.5],[1.5,-.5,1.5],[-.5,1.5,1.5]],np.float32)
    tetra=np.array([[0,2,1],[0,1,3],[0,3,2],[1,2,3]],np.uint32)
    compound=np.concatenate([tetra,np.array([[0,4,5],[0,6,4],[0,5,6],[4,6,5]],np.uint32)])
    assert exposed_backfaces(dict(POSITION=p),tetra,dict(POSITION=p),tetra) is None
    assert exposed_backfaces(dict(POSITION=p),compound,dict(POSITION=p),compound) is None
    assert exposed_backfaces(dict(POSITION=p),compound,dict(POSITION=p),tetra[:,::-1]) is not None
    restored,rf,receipt=preserve(dict(POSITION=p),compound,dict(POSITION=p),tetra[:,::-1],dict(components=[dict(triangles=4)]))
    assert len(rf)==8 and len(receipt)==1 and len(restored['POSITION'])==7
    # A separate covering construction still occludes an internal back face.
    # Isolating the internal component would restore geometry unnecessarily.
    cube=np.array([[-3,-3,-3],[3,-3,-3],[3,3,-3],[-3,3,-3],[-3,-3,3],[3,-3,3],[3,3,3],[-3,3,3]],np.float32)
    cf=np.array([[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]],np.uint32)
    cover=dict(POSITION=np.concatenate([cube,p[:4]]));original=np.concatenate([cf,tetra+8]);inside_out=np.concatenate([cf,tetra[:,::-1]+8])
    assert exposed_backfaces(cover,original,cover,inside_out,face_indices=np.arange(12,16)) is None
    # A long subpixel strip has appreciable total area but cannot justify
    # retaining a whole construction. Broad exposures still trigger the guard.
    thin=dict(POSITION=np.array([[0,0,0],[10,0,0],[0,.02,0]],np.float32));one=np.array([[0,1,2]])
    assert exposed_backfaces(thin,one,thin,one[:,::-1],.1) is None
    broad=dict(POSITION=np.array([[0,0,0],[10,0,0],[0,1,0]],np.float32))
    assert exposed_backfaces(broad,one,broad,one[:,::-1],.1) is not None
    # A tiny dark shutter beside a powered lens still affects radiance. Keep
    # that assembly while an unrelated fitting farther away can simplify.
    tri=np.array([[0,0,0],[1,0,0],[0,1,0]],np.float32)
    aa=dict(POSITION=np.concatenate([tri+[0,0,.01],tri,tri+10]),
        _LOD_MATERIAL=np.array([[0]]*3+[[1]]*6,np.float32),_LOD_KEEP=np.array([[1]]*3+[[0]]*6,np.float32))
    receipts=protect_powered(aa,np.arange(9).reshape(3,3),[dict(emissiveFactor=[1,1,1]),{}],.04)
    assert aa['_LOD_KEEP'][:6].all() and not aa['_LOD_KEEP'][6:].any() and len(receipts)==1
    from kit.lod_shared import _uv_error
    limits={'TEXCOORD_0':.005,'TEXCOORD_1':.0002}
    source_uv={k:np.zeros((3,2)) for k in limits}
    point_uv={'TEXCOORD_0':np.array([.003,0]),'TEXCOORD_1':np.zeros(2)}
    assert abs(_uv_error(point_uv,source_uv,np.arange(3),np.array([1,0,0]),limits)-.6)<1e-8
    # Vertex agreement alone misses broad shading errors inside a long face.
    # A source triangle with exact UVs must still reject a 10-degree frame miss.
    from kit.lod_shared import _field_error,_frame_limits
    assert _frame_limits(thin['POSITION'],.1)==(45.,45.)
    assert _frame_limits(broad['POSITION'],.1)==(3.,5.)
    pp=np.array([[0,0,0],[1,0,0],[0,1,0]],float);fframe=np.array([[0,1,2]])
    original=dict(POSITION=pp,NORMAL=np.tile([0,0,1.],(3,1)),TEXCOORD_0=pp[:,:2],TANGENT=np.tile([1.,0,0,1],(3,1)))
    target=dict(NORMAL=np.array([0,0,1.]),TEXCOORD_0=np.array([.25,.25]),TANGENT=np.array([1.,0,0,1]))
    gradients=np.linalg.pinv(pp[fframe[:,1:]]-pp[fframe[:,:1]]);hits=[(np.array([.25,.25,0]),None,0,0.)]
    assert _field_error(target,original,fframe,pp,gradients,hits,dict(TEXCOORD_0=np.array([.01])))[0]<1
    target['NORMAL']=np.array([0,np.sin(np.radians(10)),np.cos(np.radians(10))])
    assert _field_error(target,original,fframe,pp,gradients,hits,dict(TEXCOORD_0=np.array([.01])))[0]>1
    target['NORMAL']=np.array([0,0,1.]);target['TANGENT']=np.array([np.cos(np.radians(10)),np.sin(np.radians(10)),0,1])
    assert _field_error(target,original,fframe,pp,gradients,hits,dict(TEXCOORD_0=np.array([.01])))[0]>1
    # Closed cylinder, split longitudinal UV seam and hard-normal cap wedges.
    points=[];uv=[];normals=[];faces=[];sides=32
    for j in range(5):
        for i in range(sides+1):
            a=2*np.pi*i/sides;points.append([np.cos(a),np.sin(a),j/4]);uv.append([i/sides,j/4]);normals.append([np.cos(a),np.sin(a),0])
    for j in range(4):
        for i in range(sides):
            a=j*(sides+1)+i;b=a+sides+1;faces.extend([[a,a+1,b+1],[a,b+1,b]])
    for j,sign in [(0,-1),(4,1)]:
        center=len(points);points.append([0,0,j/4]);uv.append([.5,.5]);normals.append([0,0,sign])
        ring=[]
        for i in range(sides):
            a=2*np.pi*i/sides;ring.append(len(points));points.append([np.cos(a),np.sin(a),j/4]);uv.append([.5+.4*np.cos(a),.5+.4*np.sin(a)]);normals.append([0,0,sign])
        for i in range(sides):
            f=[center,ring[i],ring[(i+1)%sides]];faces.append(f if sign>0 else f[::-1])
    attrs=dict(POSITION=np.array(points,np.float32),NORMAL=np.array(normals,np.float32),TEXCOORD_0=np.array(uv,np.float32));ff=np.array(faces,np.uint32)
    a,f,r=collapse(attrs,ff,.4)
    assert len(f)<len(ff)*.6,r
    for k,v in a.items():
        old={tuple(x) for x in attrs[k]};assert all(tuple(x) in old for x in v),k
    t=topology(a,f)[0];assert t['boundary_edges']==t['nonmanifold_edges']==t['winding_disagreements']==0,t
    # An open material boundary stays fixed while interior vertices reduce.
    original=attrs['POSITION'][ff[:256]];x,y,z=np.meshgrid(np.arange(6),np.arange(6),[0]);p=np.stack([x.ravel(),y.ravel(),z.ravel()],axis=1).astype(np.float32)
    tris=[]
    for j in range(5):
        for i in range(5):
            k=j*6+i;tris.extend([[k,k+1,k+7],[k,k+7,k+6]])
    aa=dict(POSITION=p,NORMAL=np.tile([0,0,1.],(len(p),1)),TEXCOORD_0=p[:,:2]/5)
    out,tf,_=collapse(aa,np.array(tris,np.uint32),.5)
    border=p[(p[:,0]==0)|(p[:,0]==5)|(p[:,1]==0)|(p[:,1]==5)]
    assert all(any(np.array_equal(v,q) for q in out['POSITION']) for v in border)
    image=dict(sha256='canonical',compressed_mip_bytes=1024)
    rows=[dict(level=0,images=[image],mesh_gpu_bytes=500),dict(level=1,images=[image],mesh_gpu_bytes=200),dict(level=2,proxy=True,images=[dict(sha256='proxy',compressed_mip_bytes=64)],mesh_gpu_bytes=50)]
    r=residency(rows);assert r['passed'] and r['total_gpu_bytes']==1838 and r['proxy_texture_gpu_bytes']==64,r
    rows[1]['images']=[dict(sha256='bad',compressed_mip_bytes=512)];assert not residency(rows)['passed']
    # Exercise the public builder, merged-node checks and canonical material
    # identity on a real external-map delivery, not only synthetic cost rows.
    import json
    from kit.lod import build,check
    from kit.lod_io import Document
    from kit.image_io import write_png
    from kit.lod_normals import audit
    root=Path(__file__).resolve().parents[1]/'build/lod-shared-test'
    (root/'src').mkdir(parents=True,exist_ok=True)
    write_png(root/'map.png',np.full((8,8,3),.35,np.float32))
    stub=root/'stub.gltf';stub.write_text(json.dumps(dict(asset=dict(version='2.0'),scene=0,scenes=[dict(nodes=[0])],nodes=[dict(name='Panel',mesh=0)],meshes=[dict(primitives=[dict(attributes={},indices=0,material=0)])],accessors=[],buffers=[],bufferViews=[],materials=[dict(name='Original',pbrMetallicRoughness=dict(baseColorTexture=dict(index=0)))],images=[dict(uri='map.png')],textures=[dict(source=0)])))
    doc=Document(stub);doc.replace(doc.data['meshes'][0]['primitives'][0],aa,np.array(tris,np.uint32));source=root/'source.gltf';doc.save(source)
    # A second material uses a different chart on the same geometric panel.
    # Shared seam vertices must stay synchronized after simplification.
    doc=Document(source);primitive=doc.data['meshes'][0]['primitives'][0]
    original_attrs,original_faces=doc.arrays(primitive)
    left=np.mean(original_attrs['POSITION'][original_faces,0],axis=1)<2
    doc.data['materials'].append(dict(name='Second chart',pbrMetallicRoughness=dict(baseColorTexture=dict(index=0))))
    doc.replace(primitive,original_attrs,original_faces[left])
    other=dict(attributes={},indices=0,material=1);shifted={k:v.copy() for k,v in original_attrs.items()};shifted['TEXCOORD_0'][:,0]+=2
    doc.replace(other,shifted,original_faces[~left]);doc.data['meshes'][0]['primitives'].append(other)
    source2=root/'two-material.gltf';doc.save(source2);source=source2
    before=Document(source).dependencies()
    config=root/'src/lod.json';config.write_text(json.dumps(dict(kind='shared fixture',source=source.name,screen_space=True,levels=[dict(ratio=.5,screen_height=.2)])))
    build(config);check(config,False);audit(config)
    m=json.loads((root/'export/lod/manifest.json').read_text())
    assert len(m['levels'][1]['canonical_material_bindings'])==2
    assert m['resident']['passed'] and m['resident']['proxy_texture_gpu_bytes']==0
    assert Document(source).dependencies()==before
    assert m['levels'][1]['triangles']<m['levels'][0]['triangles']
    print('LOD SHARED MAP FIXTURE PASS' ,len(ff),'->',len(f),flush=True)


if __name__=='__main__':main()
