"""Fixed chart borders, FLOAT UV area, and opt-in isolation regressions."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from kit import lod_regions as regions
from kit.lod_shared import collapse


def main():
    folded=dict(POSITION=np.array([[0,0,0],[1,0,0],[1,1,0],[0,1,0]],np.float32),
        TEXCOORD_0=np.array([[0,0],[1,0],[1,1],[1,.5]],np.float32))
    fold_faces=np.array([[0,1,2],[0,2,3]],np.uint32)
    assert (0,2) in regions.boundaries(folded,fold_faces,np.arange(4)), 'UV fold must be a domain boundary'
    # Concave domain with a hole, an internal atlas seam, and two UV layers.
    # Legacy boundary sliding changes this domain even with exact affine UVs.
    points=[];faces=[]
    for j in range(7):
        for i in range(7):points.append([i, j, 0])
    for j in range(6):
        for i in range(6):
            if (i>=4 and j>=4) or (i==2 and j==2):continue
            k=j*7+i
            faces.extend([[k,k+1,k+8],[k,k+8,k+7]])
    faces=np.array(faces,np.uint32)
    used, remap=np.unique(faces,return_inverse=True)
    points=np.array(points,np.float32)[used];faces=remap.reshape(-1,3).astype(np.uint32)
    attrs=dict(POSITION=points,NORMAL=np.tile([0,0,1],(len(points),1)).astype(np.float32),
               TANGENT=np.tile([1,0,0,1],(len(points),1)).astype(np.float32),
               TEXCOORD_0=points[:,:2]/16+.01,TEXCOORD_1=points[:,:2]/32+.5)
    right=points[faces,0].mean(axis=1)>=3
    other={k:v.copy() for k,v in attrs.items()}
    other['TEXCOORD_0'][:,0]+=.5
    count=len(points)
    attrs={k:np.concatenate([v,other[k]]) for k,v in attrs.items()}
    faces=faces.copy();faces[right]+=count
    legacy, lf, _=collapse(attrs,faces,.2,max_error=.5,uv_limit=.1,meters_per_pixel=.25)
    assert not regions.audit(attrs,faces,legacy,lf)['passed'],'Fixture must expose old boundary movement'
    with regions.policy(True):
        out, tri, report=collapse(attrs,faces,.2,max_error=.5,uv_limit=.1,meters_per_pixel=.25)
        assert regions.audit(attrs,faces,out,tri)['passed']
        assert len(tri)<len(faces),(len(tri),len(faces))
        assert report['uv_region_pins']>0
        for key in ('TEXCOORD_0','TEXCOORD_1'):
            assert np.all(np.abs(regions.determinant(out[key][tri]))>1e-12)
        try:
            with regions.policy(False):
                assert not regions.enabled()
                raise RuntimeError('fixture')
        except RuntimeError:pass
        assert regions.enabled()
    assert not regions.enabled()
    repeat, rf, _=collapse(attrs,faces,.2,max_error=.5,uv_limit=.1,meters_per_pixel=.25)
    assert np.array_equal(lf,rf)
    assert all(np.array_equal(legacy[k],repeat[k]) for k in legacy)
    # A nonzero double-precision area can flatten in shipped FLOAT UVs.
    old=dict(TEXCOORD_0=np.array([[.5,.5],[.6,.5],[.5,.6]]))
    flat=dict(TEXCOORD_0=np.array([[.5,.5],[.6,.5],[.5,.5+1e-10]]))
    assert not regions.valid_face(old,flat)
    assert not regions.valid_face(old,dict(TEXCOORD_0=old['TEXCOORD_0'][[0,2,1]]))
    # Per-triangle preservation of inherited flats, not an aggregate allowance.
    assert regions.valid_face(flat,flat)
    assert not regions.valid_face(flat,old)
    bad={**old,'NORMAL':np.tile([0,0,1],(3,1)), 'TANGENT':np.zeros((3,4))}
    assert not regions.valid_face(old,bad)
    for value in (1,None,'true'):
        try:
            with regions.policy(value):pass
        except ValueError:pass
        else:raise AssertionError('Non-boolean accepted')
    # Exercise the public level option, cache separation and independent audit
    # on serialized accessors, then deliberately move a delivered chart edge.
    import json
    from kit.lod_io import Document
    from kit.lod import build,check,configuration
    from kit.lod_normals import audit
    folder=Path(__file__).resolve().parents[1]/'build/lod-regions-test'
    (folder/'src').mkdir(parents=True,exist_ok=True)
    stub=folder/'stub.gltf'
    stub.write_text(json.dumps(dict(asset=dict(version='2.0'),scene=0,
        scenes=[dict(nodes=[0])],nodes=[dict(name='Concave',mesh=0)],
        meshes=[dict(primitives=[dict(attributes={},indices=0,material=0)])],
        materials=[dict(name='Original')],buffers=[],accessors=[],bufferViews=[])))
    doc=Document(stub)
    doc.replace(doc.data['meshes'][0]['primitives'][0],attrs,faces)
    source=folder/'source.gltf';doc.save(source)
    receipt=Document(source).dependencies()
    config=folder/'src/lod.json'
    cfg=dict(kind='fixed region fixture',source=source.name,screen_space=True,
        levels=[dict(ratio=.2,screen_height=.09,preserve_uv_regions=True)])
    config.write_text(json.dumps(cfg))
    build(config);check(config,False);audit(config)
    delivered=folder/'export/lod/source_LOD1.gltf'
    saved=Document(delivered)
    primitive=saved.data['meshes'][0]['primitives'][0]
    arrays,ix=saved.arrays(primitive)
    arrays['TEXCOORD_0'][0,0]+=.001
    saved.replace(primitive,arrays,ix)
    tampered=delivered.with_name('tampered.gltf');saved.save(tampered)
    delivered.write_bytes(tampered.read_bytes())
    try:audit(config)
    except RuntimeError as error:assert 'UV region boundary changed' in str(error)
    else:raise AssertionError('Changed exported boundary was accepted')
    assert Document(source).dependencies()==receipt
    cfg['levels'][0]['preserve_uv_regions']='yes'
    config.write_text(json.dumps(cfg))
    try:configuration(config)
    except ValueError:pass
    else:raise AssertionError('Invalid public level option accepted')
    print('UV REGION FIXTURES PASS',len(faces),'->',len(tri),'legacy',len(lf),flush=True)


if __name__=='__main__':main()
