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
from kit.lod_scene import merge_static,proxy,shell_static,planar_groups,clean_slivers,construction_components
from kit.lod_atlas import bake,object_from_arrays
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
    # A material patch is an open subset of a larger closed assembly. Its
    # small size alone must not punch a hole through that assembly.
    patch={k:v[:3].copy() for k,v in a.items()};patch['POSITION']=patch['POSITION']*.02+[.15,0,0]
    combined={k:np.concatenate([a[k],patch[k]]) for k in a}
    aa,tf,r=reduce_screen(combined,np.concatenate([ff,[[36,37,38]]]),.9,.02,rebake=True)
    assert not r['removed_features'],'open material patch was discarded'
    # Face-on panels can be very thin in depth while remaining many pixels
    # wide. They are surfaces, rather than subpixel trim lines.
    panel={k:v.copy() for k,v in a.items()};panel['POSITION']=panel['POSITION']*[.4,.4,.001]+[0,.2,0]
    aa,tf,r=reduce_screen({k:np.concatenate([a[k],panel[k]]) for k in a},np.concatenate([ff,ff+36]),.9,.02,rebake=True)
    assert not r['removed_features'],'visible thin panel was discarded'
    # A near-coincident vertex along a closed box edge must be dissolved and
    # retriangulated without opening the shell or retaining a zero-area sliver.
    split=np.vstack([pos,pos[0]+(pos[1]-pos[0])*1e-6]);sf=[]
    for face in faces:
        cycle=list(map(int,face))
        for j in range(3):
            u,v,w=cycle[j],cycle[(j+1)%3],cycle[(j+2)%3]
            if {u,v}=={0,1}:sf.extend([(u,8,w),(8,v,w)]);break
        else:sf.append(cycle)
    mesh=bpy.data.meshes.new('sliver fixture');mesh.from_pydata(split.tolist(),[],sf);mesh.update()
    assert topology(dict(POSITION=split),np.array(sf,np.uint32))[0]['slivers']>0
    clean_slivers(mesh,.02)
    cleaned=topology(dict(POSITION=np.array([v.co[:] for v in mesh.vertices])),np.array([p.vertices[:] for p in mesh.polygons],np.uint32))[0]
    assert all(cleaned[k]==0 for k in ('slivers','degenerate','boundary_edges','nonmanifold_edges')),cleaned
    bpy.data.meshes.remove(mesh)
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
    # Closed construction shells touching at an edge remain distinct until
    # an explicit planar merge, rather than becoming one giant convex hull.
    touching=dict(POSITION=np.concatenate([a['POSITION'],a['POSITION']+[.25,.25,0]]))
    separate=construction_components(touching,np.concatenate([ff,ff+36]))
    assert sorted(map(len,separate))==[12,12],separate
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
    # The same curved structure may change by millimeters far away, while
    # a near switch rejects that displacement. This specifically distinguishes
    # switch-sized acceptance from the former LOD0-precision veto.
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.125)
    sphere=bpy.context.object;sm=sphere.data;sm.calc_loop_triangles()
    sp=np.array([v.co[:] for v in sm.vertices],np.float32)
    sn=sp/np.linalg.norm(sp,axis=1,keepdims=True)
    sf=np.array([t.vertices[:] for t in sm.loop_triangles],np.uint32)
    curved=dict(POSITION=sp,NORMAL=sn)
    near,nf,nr=reduce_screen(curved,sf,.4,.00001,rebake=True)
    far,farf,fr=reduce_screen(curved,sf,.4,.02,rebake=True)
    assert len(farf)<len(nf),(len(sf),len(nf),len(farf))
    accepted=[attempt for component in fr['component_trials']['components_tested'] for attempt in component['attempts'] if attempt['status']=='simplified' and attempt['surface_error_m']>3e-6]
    assert accepted and all(r['surface_error_m']<=.02*2 for r in accepted),fr
    bpy.data.objects.remove(sphere,do_unlink=True);bpy.data.meshes.remove(sm)
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
    # Equal surfaces with four times the original UV frequency require 16x
    # chart area. Uniform world-area packing loses deliberately dense detail.
    from kit.lod_layout import unwrap,charts
    quad=dict(POSITION=np.array([[0,0,0],[1,0,0],[1,1,0],[0,0,0],[1,1,0],[0,1,0]],np.float32),
              NORMAL=np.array([[0,0,1]]*3+[[.2,0,.9797959]]*3,np.float32))
    ob=object_from_arrays('discontinuous cage',quad,np.arange(6,dtype=np.uint32).reshape(-1,3))
    layer=ob.data.uv_layers.new(name='UVMap');layer.data.foreach_set('uv',quad['POSITION'][:,:2].ravel())
    assert len(charts(ob.data))==2,'hard cage normals shared filtered tangent texels'
    mesh=ob.data;bpy.data.objects.remove(ob,do_unlink=True);bpy.data.meshes.remove(mesh)
    material=bpy.data.materials.new('Brown');src=[];dst=[]
    for i,multiple in enumerate((1,4)):
        ref=object_from_arrays('density source '+str(i),a,ff);ref.location.x=i*.6
        layer=ref.data.uv_layers.new(name='LOD_SourceUV0');layer.data.foreach_set('uv',(a['TEXCOORD_0'][ff.ravel()]*multiple).ravel())
        ref.data.materials.append(material);src.append(ref)
        target=object_from_arrays('density target '+str(i),a,ff);target.location.x=i*.6;dst.append(target)
    layout=unwrap(dst,src,Document(source),256,.02);areas=[]
    for ob in dst:
        ob.data.calc_loop_triangles();uv=ob.data.uv_layers.active.data;total=0
        for triangle in ob.data.loop_triangles:
            u=np.array([uv[j].uv[:] for j in triangle.loops]);e=u[1:]-u[:1]
            total+=abs(e[0,0]*e[1,1]-e[0,1]*e[1,0])*.5
        coords=np.array([v.uv[:] for v in uv]);assert coords.min()>-1e-5 and coords.max()<1.00001
        areas.append(total)
    assert 14<areas[1]/areas[0]<18,(areas,layout)
    assert layout['gutter_pixels']>=4 and layout['uv_area']>.1,layout
    for ob in src+dst:
        data=ob.data;bpy.data.objects.remove(ob,do_unlink=True);bpy.data.meshes.remove(data)
    # Many small charts must retain positive texel area. An unconstrained
    # mip gutter can otherwise consume the complete far atlas silently.
    many=[];muv=[];mn=[];mf=[]
    for i in range(128):
        x=(i%16)*.1;y=(i//16)*.1;offset=len(many)
        many.extend([[x,y,0],[x+.08,y,0],[x+.08,y+.08,0],[x,y+.08,0]])
        muv.extend([[0,0],[1,0],[1,1],[0,1]]);mn.extend([[0,0,1]]*4);mf.extend([[offset,offset+1,offset+2],[offset,offset+2,offset+3]])
    ma=dict(POSITION=np.array(many,np.float32),NORMAL=np.array(mn,np.float32));mf=np.array(mf,np.uint32)
    ref=object_from_arrays('many source charts',ma,mf);ref.data.materials.append(material)
    layer=ref.data.uv_layers.new(name='LOD_SourceUV0');layer.data.foreach_set('uv',np.array(muv,np.float32)[mf.ravel()].ravel())
    target=object_from_arrays('many target charts',ma,mf)
    dense_layout=unwrap([target],[ref],Document(source),256,.05)
    assert dense_layout['gutter_pixels']==dense_layout['gutter_cap_pixels']==4,dense_layout
    assert dense_layout['gutter_capped'] and dense_layout['uv_area']>.05,dense_layout
    for ob in [ref,target]:
        data=ob.data;bpy.data.objects.remove(ob,do_unlink=True);bpy.data.meshes.remove(data)
    bpy.data.materials.remove(material)
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
    # A nonplanar curved tube must keep its void, even though an outer convex
    # envelope would be cheaper. Source rigs or explicit node patterns opt in.
    theta=np.linspace(-.9*np.pi,.9*np.pi,16);tube=[]
    for angle in theta:
        center=np.array([.2*np.cos(angle),.2*np.sin(angle),.1*np.sin(2*angle)])
        tangent=np.array([-.2*np.sin(angle),.2*np.cos(angle),.2*np.cos(2*angle)]);tangent/=np.linalg.norm(tangent)
        first=np.cross(tangent,[0,0,1]);first/=np.linalg.norm(first);second=np.cross(tangent,first)
        for turn in np.arange(6)*np.pi/3:tube.append(center+.008*(first*np.cos(turn)+second*np.sin(turn)))
    tube=np.array(tube,np.float32);tf=[]
    for ring in range(15):
        for side in range(6):
            a0=ring*6+side;b0=ring*6+(side+1)%6;c0=(ring+1)*6+side;d0=(ring+1)*6+(side+1)%6
            tf.extend([(a0,b0,d0),(a0,d0,c0)])
    for side in range(1,5):tf.extend([(0,side+1,side),(90,90+side,91+side)])
    tf=np.array(tf,np.uint32);normal=np.cross(tube[tf[:,1]]-tube[tf[:,0]],tube[tf[:,2]]-tube[tf[:,0]]);normal/=np.linalg.norm(normal,axis=1,keepdims=True)
    trial=Document(source)
    for node in trial.data['nodes'][1:]:node.pop('mesh',None)
    trial.data['nodes'][0]['name']='CurvedHose'
    tube_uv=np.column_stack([np.tile(np.arange(6)/6,16),np.repeat(np.linspace(0,1,16),6)]).astype(np.float32)
    trial.replace(trial.data['meshes'][0]['primitives'][0],dict(POSITION=tube[tf.ravel()],NORMAL=np.repeat(normal,3,axis=0),TEXCOORD_0=tube_uv[tf.ravel()]),np.arange(tf.size,dtype=np.uint32).reshape(-1,3))
    kept=proxy(trial,220,.01,['CurvedHose'])
    assert kept['concave_parts']==1 and kept['triangles']==len(tf),kept
    # A thick annulus can contain >60% of its convex envelope's volume. An
    # explicit wheel rule must still preserve the visible hole (Euler chi=0).
    angle=np.arange(8)*np.pi/4;ring=np.array([(r*np.cos(t),r*np.sin(t),z) for z,r in [(-.03,.1),(.03,.1),(-.03,.05),(.03,.05)] for t in angle],np.float32)
    rf=[]
    for side in range(8):
        j=(side+1)%8
        for quad in [(side,j,8+j,8+side),(16+side,24+side,24+j,16+j),(side,16+side,16+j,j),(8+side,8+j,24+j,24+side)]:
            rf.extend([(quad[0],quad[1],quad[2]),(quad[0],quad[2],quad[3])])
    rf=np.array(rf,np.uint32);rn=np.cross(ring[rf[:,1]]-ring[rf[:,0]],ring[rf[:,2]]-ring[rf[:,0]]);rn/=np.linalg.norm(rn,axis=1,keepdims=True)
    trial=Document(source)
    for node in trial.data['nodes'][1:]:node.pop('mesh',None)
    trial.data['nodes'][0]['name']='Wheel_Test'
    trial.replace(trial.data['meshes'][0]['primitives'][0],dict(POSITION=ring[rf.ravel()],NORMAL=np.repeat(rn,3,axis=0),TEXCOORD_0=np.zeros((rf.size,2),np.float32)),np.arange(rf.size,dtype=np.uint32).reshape(-1,3))
    kept=proxy(trial,100,.01,['Wheel*']);assert kept['concave_parts']==1,kept
    ra,rr=trial.arrays(trial.data['meshes'][0]['primitives'][0]);vertices,inverse=np.unique(np.round(ra['POSITION'],6),axis=0,return_inverse=True);rr=inverse[rr]
    edges={tuple(sorted((int(face[a]),int(face[b])))) for face in rr for a,b in [(0,1),(1,2),(2,0)]}
    assert len(vertices)-len(edges)+len(rr)==0,'wheel hole was filled'
    # Preserve a building's concave footprint, including closing an open
    # bottom boundary. A convex envelope would bridge its roof valley.
    footprint=[(0,0),(2,0),(2,1),(1,1),(1,2),(0,2)]
    building=np.array([(x,y,z) for y in [0,1] for x,z in footprint],np.float32)
    for bottom in (True,False):
        mesh=bpy.data.meshes.new('concave building');polygons=[tuple(range(11,5,-1))]
        if bottom:polygons.append(tuple(range(6)))
        for i in range(6):j=(i+1)%6;polygons.append((i,i+6,j+6,j))
        mesh.from_pydata(building.tolist(),[],polygons);mesh.update();mesh.calc_loop_triangles()
        bf=np.array([t.vertices[:] for t in mesh.loop_triangles],np.uint32)
        bn=np.cross(building[bf[:,1]]-building[bf[:,0]],building[bf[:,2]]-building[bf[:,0]]);bn/=np.linalg.norm(bn,axis=1,keepdims=True)
        trial=Document(source)
        for node in trial.data['nodes'][1:]:node.pop('mesh',None)
        trial.replace(trial.data['meshes'][0]['primitives'][0],dict(POSITION=building[bf.ravel()],NORMAL=np.repeat(bn,3,axis=0),TEXCOORD_0=np.zeros((bf.size,2),np.float32)),np.arange(bf.size,dtype=np.uint32).reshape(-1,3))
        bpy.data.meshes.remove(mesh)
        kept=proxy(trial,100,.05);assert kept['concave_parts']==1,kept
        aa,tt=trial.arrays(trial.data['meshes'][0]['primitives'][0])
        from mathutils import Vector
        from mathutils.bvhtree import BVHTree
        tree=BVHTree.FromPolygons([Vector(v) for v in aa['POSITION']],tt.tolist(),all_triangles=True)
        assert tree.find_nearest(Vector((1.4,.5,1.4)))[3]>.3,'roof valley was bridged'
        assert kept['topology']['boundary_edges']==0 and kept['topology']['nonmanifold_edges']==0,kept
        if not bottom:assert kept['closed_source_boundary_edges']>0,kept
    # Backing size belongs to the complete construction component, rather
    # than a single tiny triangle in a densely tessellated body panel.
    import bmesh
    mesh=bpy.data.meshes.new('dense backing');mesh.from_pydata(a['POSITION'].tolist(),[],ff.tolist());mesh.update()
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    bmesh.ops.subdivide_edges(bm,edges=list(bm.edges),cuts=7,use_grid_fill=True);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();mesh.update()
    dp=np.array([v.co[:] for v in mesh.vertices],np.float32);df=np.array([p.vertices[:] for p in mesh.polygons],np.uint32)
    dn=np.cross(dp[df[:,1]]-dp[df[:,0]],dp[df[:,2]]-dp[df[:,0]]);dn/=np.linalg.norm(dn,axis=1,keepdims=True)
    dense=dict(POSITION=dp[df.ravel()],NORMAL=np.repeat(dn,3,axis=0),TEXCOORD_0=np.zeros((df.size,2),np.float32));dt=np.arange(df.size,dtype=np.uint32).reshape(-1,3)
    trim={k:v.copy() for k,v in a.items()};trim['POSITION']=trim['POSITION']*[.8,.02,.02]+[0,0,.129]
    trial=Document(source)
    for node in trial.data['nodes'][1:]:node.pop('mesh',None)
    trial.replace(trial.data['meshes'][0]['primitives'][0],{k:np.concatenate([dense[k],trim[k]]) for k in dense},np.concatenate([dt,ff+len(dense['POSITION'])]))
    bpy.data.meshes.remove(mesh)
    kept=proxy(trial,100,.02);assert any(v['reason']=='thin attached feature' for v in kept['removed_features']),kept
    # A support touching floor and body only at its ends remains. Vertex-only
    # samples put every box corner at an attachment and incorrectly delete it.
    leg={k:v.copy() for k,v in a.items()};leg['POSITION']=leg['POSITION']*[.04,.04,2]+[0,0,-.375]
    floor={k:v.copy() for k,v in a.items()};floor['POSITION']=floor['POSITION']*[4,4,.04]+[0,0,-.63]
    trial=Document(source)
    for node in trial.data['nodes'][1:]:node.pop('mesh',None)
    trial.replace(trial.data['meshes'][0]['primitives'][0],{k:np.concatenate([a[k],leg[k],floor[k]]) for k in a},np.concatenate([ff,ff+36,ff+72]))
    kept=proxy(trial,100,.02);assert not kept['removed_features'],'freestanding support was removed'
    d=Document(source);r=proxy(d,150,.075)
    assert r['triangles']<=150 and not r['topology']['boundary_edges'] and not r['topology']['nonmanifold_edges'],r
    path=out/'proxy.gltf';result=bake(d,source,path,128,proxy=True,projection_m=.08);d.save(path)
    delivered=Document(path);stats=delivered.stats()
    assert stats['materials']==stats['draw_calls']==1 and len(stats['images'])==6,stats
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
    coatnormal=_image(delivered.image(5))*2-1
    assert np.max(np.abs(np.linalg.norm(coatnormal[:,:,:3],axis=2)-1))<.007
    assert np.max(np.abs(coatnormal-normal))>.02,'base bump was incorrectly reused for clearcoat'
    # Near HDR atlases must not make an originally non-emitting material
    # emit. A bright neighboring label can otherwise bleed across chart mips.
    near=Document(source);nearpath=out/'near.gltf'
    bake(near,source,nearpath,128,projection_m=.08,composite_alpha=True);near.save(nearpath)
    assert near.data['materials'][0].get('emissiveFactor')==[0,0,0]
    assert 'emissiveTexture' not in near.data['materials'][0]
    assert near.data['materials'][1].get('emissiveTexture') is not None
    coat=near.data['materials'][0]['extensions']['KHR_materials_clearcoat']
    assert coat['clearcoatNormalTexture']['index']!=near.data['materials'][0]['normalTexture']['index']
    print('LOD PROXY FIXTURE PASS: projected pruning, mip-relative UV budget, silhouette IoU, material merge, pivot preservation, closed budgeted shell, real immutable-source PBR/normal bake')

if __name__=='__main__':main()
