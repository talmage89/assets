"""Independent external bytes, UV charts, tangent normals and fresh imports.

Physical construction remains in check.py. This audit proves serialization,
stock-PBR/map reuse and the explicit reused-chart allocation, not realism.
"""
import hashlib,json,math,sys
from pathlib import Path
import bpy,numpy as np
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.gltf import GLB
from kit.image_io import read_png
from atlas import RECTS,rect
from deliver import bundle


def external(path):
    g=object.__new__(GLB);g.json=json.loads(path.read_text());g.binary=(path.parent/g.json['buffers'][0]['uri']).read_bytes()
    g.parents={c:i for i,n in enumerate(g.json['nodes']) for c in n.get('children',[])}
    return g


def weighted(rows):
    a=np.asarray(rows);a=a[np.argsort(a[:,0])];weights=np.cumsum(a[:,1]);weights/=weights[-1]
    return dict(zip(('p5','median','p95'),map(float,np.interp([.05,.5,.95],weights,a[:,0]))))


def check():
    delivery=json.loads(Path('build/delivery.json').read_text());rows=[]
    for row in delivery['rows']:
        path=Path(row['delivery']);g=external(path);original=GLB(Path(row['source']))
        assert bundle(path)==row['bundle_sha256']
        assert len(g.json.get('materials',[]))<=3
        assert len(g.json.get('images',[]))==3
        images=[]
        for i,im in enumerate(g.json['images']):
            assert im['uri'].startswith('textures/T_Utility_')
            raw=(path.parent/im['uri']).read_bytes();assert raw==original.image(i)
            a=read_png(raw);assert a.shape==(2048,2048,3)
            images.append(dict(uri=im['uri'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
        family=next(i for i,m in enumerate(g.json['materials']) if m['name']=='Utility')
        mat=g.json['materials'][family];assert mat.get('doubleSided')
        assert mat['normalTexture'].get('scale',1)>0
        # Verify two sources have identical numeric vertex/index payloads.
        for i in range(len(g.json['accessors'])):assert np.array_equal(g.accessor(i),original.accessor(i)),(path,i)
        density={role:[] for role in RECTS};degenerate_uv=0;triangles=0;normal_error=0.;tangent_error=0.
        contacts=[]
        for mesh in g.json['meshes']:
            chart_geometry={}
            for p in mesh['primitives']:
                pos=g.accessor(p['attributes']['POSITION']);ix=g.accessor(p['indices']).ravel().reshape(-1,3);triangles+=len(ix)
                normals=g.accessor(p['attributes']['NORMAL']);normal_error=max(normal_error,float(np.max(abs(np.linalg.norm(normals,axis=1)-1))))
                if p['material']!=family:continue
                assert 'TEXCOORD_0' in p['attributes'] and 'TANGENT' in p['attributes']
                uv=g.accessor(p['attributes']['TEXCOORD_0']);uv[:,1]=1-uv[:,1] # glTF top-down -> authored Blender charts
                tangents=g.accessor(p['attributes']['TANGENT'])
                tangent_error=max(tangent_error,float(abs(np.linalg.norm(tangents[:,:3],axis=1)-1).max()),float(abs(np.sum(tangents[:,:3]*normals,axis=1)).max()))
                xyz=pos[ix];q=uv[ix];world_area=np.linalg.norm(np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]),axis=1)/2
                d1=q[:,1]-q[:,0];d2=q[:,2]-q[:,0];uv_area=abs(d1[:,0]*d2[:,1]-d1[:,1]*d2[:,0])/2
                degenerate_uv+=int((uv_area<1e-14).sum())
                lo=q.min(axis=1);hi=q.max(axis=1);classified=np.zeros(len(ix),bool)
                for role in RECTS:
                    a,b,c,d=rect(role);selected=(lo[:,0]>=a-1e-6)&(lo[:,1]>=b-1e-6)&(hi[:,0]<=c+1e-6)&(hi[:,1]<=d+1e-6)
                    assert not np.any(classified&selected);classified|=selected
                    if selected.any():chart_geometry.setdefault(role,[]).extend(xyz[selected].tolist())
                    for ua,wa in zip(uv_area[selected],world_area[selected]):
                        if wa>1e-12 and ua>1e-14:density[role].append((2048*math.sqrt(float(ua/wa)),float(wa)))
                assert classified.all(),(path,'Triangle crosses a stock chart boundary',q[~classified][:3].tolist())
            # Contacts are measured on distinct exported surface triangles,
            # never by comparing the export to its authoring constants.
            from mathutils import Vector
            from mathutils.bvhtree import BVHTree
            for marking,support in (('Brand',('PoleA','PoleB')),('Rating',('Tank',))):
                if marking not in chart_geometry:continue
                target=[t for r in support for t in chart_geometry.get(r,[])]
                assert target,(path,mesh.get('name'),marking,'Missing support')
                vs=[p for t in target for p in t];fs=[(3*i,3*i+1,3*i+2) for i in range(len(target))]
                bvh=BVHTree.FromPolygons(vs,fs,all_triangles=True);distances=[]
                for t in chart_geometry[marking]:
                    points=[Vector(p) for p in t];points.append(sum(points,Vector())/3)
                    for p in points:distances.append(bvh.find_nearest(p)[3])
                assert min(distances)>1e-5 and max(distances)<.001,(path,mesh.get('name'),marking,min(distances),max(distances))
                contacts.append(dict(mesh=mesh.get('name'),marking=marking,support_charts=support,samples=len(distances),minimum_gap_m=min(distances),maximum_gap_m=max(distances)))
        assert triangles==row['triangles'];assert normal_error<.001 and tangent_error<.001,(path,normal_error,tangent_error,degenerate_uv)
        assert degenerate_uv==0,(path,'degenerate UV triangles',degenerate_uv)
        densities={k:weighted(v) for k,v in density.items() if v}
        for role in ('PoleA','PoleB'):
            if role in densities:assert 120<densities[role]['median']<600,(path,role,densities[role])
        # An ordinary fresh import must preserve count and all socket extras.
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
        imported=0
        for ob in bpy.context.scene.objects:
            if ob.type=='MESH':ob.data.calc_loop_triangles();imported+=len(ob.data.loop_triangles)
        assert imported==triangles
        source_sockets={n['name'] for n in g.json['nodes'] if n.get('extras',{}).get('socket_kind')}
        actual_sockets={o.name for o in bpy.context.scene.objects if o.get('socket_kind')};assert actual_sockets==source_sockets
        if 'Street' in path.name:assert triangles<=49000,(path,triangles)
        rows.append(dict(delivery=str(path),triangles=triangles,materials=len(g.json['materials']),draw_primitives=sum(len(m['primitives']) for m in g.json['meshes']),
            images=images,degenerate_uv_triangles=degenerate_uv,unit_normal_error=normal_error,tangent_error=tangent_error,density_px_m=densities,sockets=len(source_sockets),
            marking_support_contacts=contacts,
            uv_policy='16 disjoint charts with eight delivered pixels of own-edge guard. Reuse within each stock chart is deliberate; triangles cannot cross chart boundaries.'))
    # The three external URI identities are actually shared in one scene.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for row in delivery['rows']:bpy.ops.import_scene.gltf(filepath=str(Path(row['delivery']).resolve()))
    loaded=[i for i in bpy.data.images if i.source=='FILE' and i.filepath]
    identities={str(Path(bpy.path.abspath(i.filepath)).resolve()) for i in loaded}
    assert len(identities)==3,(len(identities),identities)
    # Count Blender datablocks too: a repeated path alone does not prove cache reuse.
    assert len(loaded)==3,[(i.name,i.filepath) for i in loaded]
    normal=read_png(Path('textures/ship/T_Utility_Normal.png'))*2-1
    normal_map_error=float(abs(np.linalg.norm(normal,axis=2)-1).max());assert normal_map_error<.008
    protected=json.loads((HERE.parents[1]/'build/utility-preservation.json').read_text()) if (HERE.parents[1]/'build/utility-preservation.json').exists() else {}
    for p,digest in protected.items():assert hashlib.sha256((HERE.parents[1]/p).read_bytes()).hexdigest()==digest
    output=dict(rows=rows,normal_map_unit_error=normal_map_error,simultaneously_loaded_image_datablocks=len(loaded),canonical_images=len(identities),compressed_mipmapped_texture_mib=16,
                existing_delivery_files=len(protected),existing_files_preserved=True,scope='External bytes and numeric serialization, chart allocation/density, raw normals and fresh imports. Physical construction: checks.json. Look: photo pairs and REVIEW.md.')
    Path('build/delivery-check.json').write_text(json.dumps(output,indent=2));print('UTILITY DELIVERY PASS',[(r['delivery'],r['triangles']) for r in rows])


if __name__=='__main__':check()
