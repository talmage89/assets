"""Screen acceptance, feature pruning, merge and real proxy appearance bake.

Run via kit/with_gpu.sh in a fresh process; writes only build/lod-proxy-test.
"""
import copy
import json
import sys
from pathlib import Path
import bpy
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit.lod_mesh import uv_budget,reduce_screen,topology
from kit.lod_scene import merge_static,proxy,shell_static,planar_groups
from kit.lod_atlas import bake
from kit.lod_io import Document,digest
from kit.detachable_verify import _image
from kit.lod_render import compare


def main():
    out=ROOT/'build/lod-proxy-test';out.mkdir(parents=True,exist_ok=True)
    # A quarter-meter cube plus a truly subpixel bolt. At the closer switch it
    # must stay; farther away it may go. Long visible bars must never disappear
    # merely because one dimension is thin.
    pos=np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],np.float32)*.125
    faces=np.array([[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[3,7,6],[3,6,2],[0,4,7],[0,7,3],[1,2,6],[1,6,5]],np.uint32)
    flat=pos[faces.ravel()];normals=np.repeat(np.cross(pos[faces[:,1]]-pos[faces[:,0]],pos[faces[:,2]]-pos[faces[:,0]]),3,axis=0)
    normals/=np.linalg.norm(normals,axis=1,keepdims=True)
    ff=np.arange(len(flat),dtype=np.uint32).reshape(-1,3)
    a=dict(POSITION=flat,NORMAL=normals,TEXCOORD_0=np.tile([[0,0],[1,0],[1,1]],(12,1)).astype(np.float32))
    tiny={k:v.copy() for k,v in a.items()};tiny['POSITION']=tiny['POSITION']*.02+[.15,0,0]
    combined={k:np.concatenate([a[k],tiny[k]]) for k in a};tri=np.concatenate([ff,ff+len(flat)])
    aa,tf,r=reduce_screen(combined,tri,.9,.02,rebake=True)
    assert len(r['removed_features'])==1 and r['removed_features'][0]['triangles']==12,r
    aa,tf,r=reduce_screen(combined,tri,.9,.001,rebake=True)
    assert len(r['removed_features'])==0,r
    long_bar={k:v.copy() for k,v in a.items()};long_bar['POSITION']=long_bar['POSITION']*[8,.04,.04]+[.6,0,0]
    trim={k:v.copy() for k,v in a.items()};trim['POSITION']=trim['POSITION']*[1.6,.04,.04]+[0,.2,0]
    pieces=[a,tiny,long_bar,trim]
    aa,tf,r=reduce_screen({k:np.concatenate([v[k] for v in pieces]) for k in a},np.concatenate([ff+i*len(flat) for i in range(4)]),.9,.02,rebake=True)
    assert len(r['removed_features'])==2 and all(x['diameter_pixels']<48 for x in r['removed_features']),r
    # Separate adjacent siding boards must become one simplifiable surface;
    # coplanar geometry on another module must not bridge empty space.
    board=a['POSITION']*np.array([2,.1,.004])+[0,0,.3]
    other=board+[0,.026,0]
    boards=dict(POSITION=np.concatenate([board,other]));bt=np.concatenate([ff,ff+len(flat)])
    joined=planar_groups(boards,bt,.02)
    assert len(joined)==1 and joined[0][1]==2,joined
    for shift in ([0,2,0],[0,0,.1]):
        separate=dict(POSITION=np.concatenate([board,other+shift]))
        assert len(planar_groups(separate,bt,.02))==2
    # Discrete joint IDs must not be averaged. Affine influence transport on a
    # tessellated panel should reduce and retain the same physical field.
    grid=np.array([(x/6,y/6,0) for y in range(7) for x in range(7)],np.float32);faces=[]
    for y in range(6):
        for x in range(6):
            i=y*7+x;faces.extend([(i,i+1,i+8),(i,i+8,i+7)])
    skin=dict(POSITION=grid,NORMAL=np.tile([0,0,1],(49,1)).astype(np.float32),TEXCOORD_0=grid[:,:2],
              JOINTS_0=np.tile([0,3,0,0],(49,1)).astype(np.uint16),
              WEIGHTS_0=np.column_stack([1-grid[:,0],grid[:,0],np.zeros((49,2))]).astype(np.float32))
    aa,tf,r=reduce_screen(skin,np.array(faces,np.uint32),.3,.1,rebake=True)
    assert len(tf)<len(faces)*.5,r
    assert np.all(aa['JOINTS_0']==np.rint(aa['JOINTS_0']))
    assert np.max(np.abs(aa['WEIGHTS_0'].sum(axis=1)-1))<1e-6
    influence=(aa['WEIGHTS_0']*(aa['JOINTS_0']==3)).sum(axis=1)
    assert np.max(np.abs(influence-aa['POSITION'][:,0]))<1e-5
    b1=uv_budget(a,ff,.02,512)['TEXCOORD_0'];b2=uv_budget(a,ff,.04,512)['TEXCOORD_0']
    assert abs(b2['sampled_mip']-b1['sampled_mip']-1)<1e-6
    assert abs(b2['normalized_tolerance']/b1['normalized_tolerance']-2)<1e-6
    image=np.zeros((24,24,4),np.float32);image[4:20,4:20]=1
    metric,_=compare(image,image);assert metric['silhouette_loss']==0
    changed=image.copy();changed[4:8,4:20]=0
    metric,_=compare(image,changed);assert .24<metric['silhouette_loss']<.26
    from kit.image_io import write_png
    label=np.zeros((8,8,4),np.float32);label[:,:,0]=1;label[:,:4,3]=.5
    write_png(out/'label.png',label)
    y,x=np.mgrid[:16,:16];normal=np.stack([.18*np.sin(x/16*np.pi*2),.12*np.cos(y/16*np.pi*2),np.ones_like(x)],axis=2)
    normal/=np.linalg.norm(normal,axis=2,keepdims=True);write_png(out/'normal.png',normal*.5+.5)
    emission=np.zeros((8,8,3),np.float32);emission[4:,4:,1]=1;write_png(out/'emission.png',emission)
    orm=np.zeros((8,8,3),np.float32);orm[:,:,0]=1;orm[:,:,1]=.65;write_png(out/'orm.png',orm)
    stub=out/'stub.gltf';stub.write_text(json.dumps(dict(asset=dict(version='2.0'),scene=0,scenes=[dict(nodes=[0,1,2,3])],
        nodes=[dict(name='StaticA',mesh=0),dict(name='StaticB',mesh=1,translation=[.2,0,0]),
               dict(name='Door',mesh=2,translation=[0,0,-.4],extras=dict(pivot_axis='Y',range_degrees=[0,90])),dict(name='Label',mesh=3)],
        meshes=[dict(name=n,primitives=[dict(attributes={},indices=0,material=1 if n=='Label' else 0)]) for n in ['A','B','C','Label']],
        accessors=[],bufferViews=[],buffers=[],materials=[dict(name='Brown',normalTexture=dict(index=1),extensions={'KHR_materials_clearcoat':dict(clearcoatFactor=1,clearcoatRoughnessFactor=.08)},pbrMetallicRoughness=dict(baseColorFactor=[.22,.12,.06,1],metallicRoughnessTexture=dict(index=3),roughnessFactor=1,metallicFactor=1)),
            dict(name='Label',alphaMode='BLEND',emissiveFactor=[0,.2,0],emissiveTexture=dict(index=2,texCoord=1),pbrMetallicRoughness=dict(baseColorTexture=dict(index=0),metallicFactor=0,roughnessFactor=.65))],
        images=[dict(name='BaseColor',uri='label.png'),dict(name='Normal',uri='normal.png'),dict(name='Emission',uri='emission.png'),dict(name='ORM',uri='orm.png')],textures=[dict(source=0),dict(source=1),dict(source=2),dict(source=3)],extensionsUsed=['KHR_materials_clearcoat'])))
    d=Document(stub)
    for m in d.data['meshes'][:3]:d.replace(m['primitives'][0],a,ff)
    decal=dict(POSITION=np.array([[-.08,-.08,.127],[.08,-.08,.127],[.08,.08,.127],[-.08,.08,.127]],np.float32),
               NORMAL=np.tile([0,0,1],(4,1)).astype(np.float32),TEXCOORD_0=np.array([[0,1],[1,1],[1,0],[0,0]],np.float32))
    decal['TEXCOORD_1']=np.tile([.75,.75],(4,1)).astype(np.float32)
    d.replace(d.data['meshes'][3]['primitives'][0],decal,np.array([[0,1,2],[0,2,3]],np.uint32))
    source=out/'source.gltf';d.save(source);before=Document(source).dependencies();d=Document(source)
    animated=Document(source);animated.data['animations']=[dict(channels=[dict(target=dict(node=1,path='translation'))])]
    assert 'StaticB' in merge_static(animated)['separate_nodes'],'animation-only moving part was merged'
    transforms=[d.world(i).copy() for i in range(3)]
    receipt=merge_static(d)
    assert len(receipt['static_groups'])==1 and receipt['separate_nodes']==['Door']
    assert 'mesh' not in d.data['nodes'][0] and 'mesh' not in d.data['nodes'][1]
    assert 'mesh' in d.data['nodes'][2] and d.data['nodes'][2]['name']=='Door'
    for i,m in enumerate(transforms):assert np.array_equal(d.world(i),m)
    merged=out/'merged.gltf';d.save(merged)
    assert Document(merged).stats()['draw_calls']==3
    trial=Document(merged);door=copy.deepcopy(trial.arrays(trial.data['meshes'][trial.data['nodes'][2]['mesh']]['primitives'][0]))
    shells=shell_static(trial,.4,.02)
    assert shells and trial.data['nodes'][2]['name']=='Door'
    preserved=trial.arrays(trial.data['meshes'][trial.data['nodes'][2]['mesh']]['primitives'][0])
    assert np.array_equal(door[0]['POSITION'],preserved[0]['POSITION']) and np.array_equal(door[1],preserved[1])
    assert all(x['topology']['boundary_edges']==0 for x in shells)
    d=Document(source);r=proxy(d,150,.075)
    assert r['triangles']<=150 and not r['topology']['boundary_edges'] and not r['topology']['nonmanifold_edges'],r
    path=out/'proxy.gltf';result=bake(d,source,path,128,proxy=True,projection_m=.08);d.save(path)
    delivered=Document(path);stats=delivered.stats()
    assert stats['materials']==stats['draw_calls']==1 and len(stats['images'])==5,stats
    assert all(i['size']==[128,128] for i in stats['images'])
    assert result['zero_alpha_interior_texels']<=result['uv_covered_texels']*.001,result
    # The sub-0.1% UV-edge raster discrepancy is reported, not filled over.
    base=_image(delivered.image(0))
    from kit.image_io import linear_to_srgb
    assert np.max(np.abs(np.median(base[:,:,:3].reshape(-1,3),axis=0)-linear_to_srgb(np.array([.22,.12,.06]))))<.01
    assert result['used_underlay'],'proxy did not composite transparent source graphics'
    # Independently project two physical points onto the exported cage and
    # sample its actual atlas. The half-opacity label and fully transparent half both have red RGB: without the
    # backing pass the right-hand point becomes a solid red rectangle.
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    from kit.lod_mesh import barycentric
    from kit.detachable_verify import sample
    p=delivered.data['meshes'][0]['primitives'][0];aa,tf=delivered.arrays(p)
    tree=BVHTree.FromPolygons([Vector(v) for v in aa['POSITION']],tf.tolist(),all_triangles=True)
    for x,expected in [(-.04,linear_to_srgb(np.array([.61,.06,.03]))),(.04,linear_to_srgb(np.array([.22,.12,.06])))]:
        q,n,fi,dist=tree.find_nearest(Vector((x,0,.2)))
        w=barycentric(np.array(q),aa['POSITION'][tf[fi]].astype(float));uv=w@aa['TEXCOORD_0'][tf[fi]]
        actual=sample(base,uv[None,:])[0,:3]
        assert np.max(np.abs(actual-expected))<.1,(x,actual,expected)
    normal=_image(delivered.image(2))*2-1
    emission=_image(delivered.image(3));coat=_image(delivered.image(4))
    # Emission uses constant UV1 while alpha/base remain UV0. Its transparent
    # half must not become an emissive green rectangle on the backing.
    for x,wanted in [(-.04,True),(.04,False)]:
        q,n,fi,dist=tree.find_nearest(Vector((x,0,.2)));w=barycentric(np.array(q),aa['POSITION'][tf[fi]].astype(float));uv=w@aa['TEXCOORD_0'][tf[fi]]
        green=sample(emission,uv[None,:])[0,1]
        assert (green>.3 if wanted else green<.03),(x,green)
        clear=sample(coat,uv[None,:])[0,:2]
        assert (abs(clear[0]-.5)<.06 if wanted else np.max(np.abs(clear-[1,.08]))<.03),(x,clear)
    assert np.max(np.abs(np.linalg.norm(normal[:,:,:3],axis=2)-1))<.007
    assert Document(source).dependencies()==before,'proxy bake modified LOD0'
    # A real normal map must carry face changes; a constant blue stand-in fails.
    assert np.std(normal[:,:,:2])>.01
    print('LOD PROXY FIXTURE PASS: projected pruning, mip-relative UV budget, silhouette IoU, material merge, pivot preservation, closed budgeted shell, real immutable-source PBR/normal bake')

if __name__=='__main__':main()
