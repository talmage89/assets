"""Construction, metric UV density, raw external PBR and fresh-import evidence.

Tiled/trim UV reuse is intentional. These checks do not certify full interiors,
continuous whole-assembly collision safety or historical code compliance.
"""
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
from mathutils import Matrix
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT)]
from kit.gltf import GLB
from plans import garden,row,complex_plan,COMPLEX_SEEDS,ROW_SEEDS
from context import parent_chain


def external(path):
    raw=object.__new__(GLB);raw.json=json.loads(path.read_text())
    assert len(raw.json['buffers'])==1
    raw.binary=(path.parent/raw.json['buffers'][0]['uri']).read_bytes()
    raw.parents={c:i for i,n in enumerate(raw.json['nodes']) for c in n.get('children',[])}
    return raw


def points():
    rows=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        xyz=np.empty(len(ob.data.vertices)*3);ob.data.vertices.foreach_get('co',xyz);xyz=xyz.reshape(-1,3)
        xf=np.array(ob.matrix_world);rows.append(xyz@xf[:3,:3].T+xf[:3,3])
    return np.concatenate(rows) if rows else np.empty((0,3))


def triangles(obs):
    total=0
    for ob in obs:
        ob.data.calc_loop_triangles();total+=len(ob.data.loop_triangles)
    return total


def source(path,stem):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));bpy.context.view_layer.update()
    pivots={o.name:np.array(o.matrix_world).tolist() for o in bpy.context.scene.objects if o.get('pivot_axis') or o.get('slide_axis') or o.get('motion_kind') or o.get('socket_kind')}
    stair_reports=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('component')!='stairs':continue
        pans=[]
        for face in ob.data.polygons:
            if face.normal.z<.99:continue
            vs=np.array([ob.data.vertices[i].co[:] for i in face.vertices]);span=np.ptp(vs,axis=0)
            # Pan crowns are the large horizontal 44 inch by ~12 inch faces.
            # Guards, base plates and the much larger landings cannot pass.
            if 1.10<span[0]<1.13 and .29<span[1]<.32:
                pans.append(dict(x=float(vs[:,0].mean()),y=float(vs[:,1].mean()),z=float(vs[:,2].mean()),width=float(span[0]),depth=float(span[1])))
        assert len(pans)==16,(ob.name,len(pans))
        flights=[]
        for x in sorted(set(round(q['x'],4) for q in pans)):
            q=sorted([v for v in pans if abs(v['x']-x)<.001],key=lambda v:v['z'])
            assert len(q)==8
            rises=np.diff([v['z'] for v in q]);goings=abs(np.diff([v['y'] for v in q]))
            assert abs(rises.mean()-.17145)<1e-5 and np.ptp(rises)<1e-5
            assert abs(goings.mean()-.2794)<1e-5 and np.ptp(goings)<1e-5
            flights.append(dict(pan_crowns_measured=len(q),riser_intervals_measured=len(rises),rise_m=float(rises.mean()),going_m=float(goings.mean()),
                                pan_crown_width_m=min(v['width'] for v in q),pan_crown_depth_m=min(v['depth'] for v in q)))
        stair_reports.append(dict(object=ob.name,flights=flights))
    # Conservative horizontal working-space bounds from actual placed meshes.
    service_gaps=[]
    for building in [o for o in bpy.context.scene.objects if o.get('building_kind')=='garden']:
        wings=sorted([o for o in building.children if o.get('access')],key=lambda o:o.name)
        if len(wings)!=2:continue
        inv=building.matrix_world.inverted()
        def bounds(ob):
            vv=np.array([(inv@ob.matrix_world@v.co)[:] for v in ob.data.vertices]);return vv.min(0),vv.max(0)
        bank=bpy.data.objects[wings[0].name+'__Meter_bank'];lo,hi=bounds(bank);near=[]
        for ob in wings[1].children_recursive:
            if ob.type!='MESH':continue
            a,c=bounds(ob)
            if a[1]<hi[1]+.1 and c[1]>lo[1]-.1 and a[2]<2.1 and c[2]>.1 and c[0]>hi[0]:near.append(float(a[0]))
        assert near;gap=min(near)-float(hi[0]);assert gap>=1.2192,(building.name,gap,'meter passage')
        service_gaps.append(dict(building=building.name,clear_horizontal_bound_m=gap,scope='Conservative mesh component bounds opposite the meter bank, through 2.1 m height; excludes the intended ground slab and canopy bearing ledgers.'))
    # Actual leaf/casing triangle intersections, sampled every ten degrees.
    # This proves the modeled jamb relationship, not whole-building clearance.
    motion_poses=0
    for pivot in list(bpy.context.scene.objects):
        if pivot.get('pivot_axis')!='Z':continue
        frame=bpy.data.objects.get(pivot.name+'_casing')
        moving=[o for o in pivot.children if o.type=='MESH' and o.get('component')=='door_leaf']
        if frame is None or not moving:continue
        fixed=BVHTree.FromPolygons([frame.matrix_world@v.co for v in frame.data.vertices],[f.vertices[:] for f in frame.data.polygons])
        rest=pivot.matrix_basis.copy()
        for angle in range(0,101,10):
            pivot.matrix_basis=rest@Matrix.Rotation(math.radians(angle),4,'Z');bpy.context.view_layer.update()
            for ob in moving:
                tree=BVHTree.FromPolygons([ob.matrix_world@v.co for v in ob.data.vertices],[f.vertices[:] for f in ob.data.polygons])
                assert not tree.overlap(fixed),(pivot.name,angle,'leaf/casing interference')
            motion_poses+=1
        pivot.matrix_basis=rest;bpy.context.view_layer.update()
    slider_poses=0
    for pivot in list(bpy.context.scene.objects):
        if pivot.get('slide_axis')!='X':continue
        moving=[o for o in pivot.children if o.type=='MESH' and o.get('component')=='slider']
        if not moving:continue
        frame=bpy.data.objects.get(pivot.name.removesuffix('_panel')+'_fixed');assert frame is not None,pivot.name
        fixed=BVHTree.FromPolygons([frame.matrix_world@v.co for v in frame.data.vertices],[f.vertices[:] for f in frame.data.polygons])
        rest=pivot.matrix_basis.copy()
        for distance in np.linspace(*pivot['range_m'],9):
            pivot.matrix_basis=rest@Matrix.Translation((float(distance),0,0));bpy.context.view_layer.update()
            for ob in moving:
                tree=BVHTree.FromPolygons([ob.matrix_world@v.co for v in ob.data.vertices],[f.vertices[:] for f in ob.data.polygons])
                assert not tree.overlap(fixed),(pivot.name,float(distance),'slider/fixed sash interference')
            slider_poses+=1
        pivot.matrix_basis=rest;bpy.context.view_layer.update()
    garage_nodes=[o for o in bpy.context.scene.objects if o.get('motion_kind')=='sectional_track']
    garage_poses=0;chord_error=0;ceiling_gap=100.;garage_open={}
    if garage_nodes:
        from garage_motion import pose
        for progress in np.linspace(0,1,21):
            frames=pose(float(progress));chord_error=max(chord_error,max(abs(v['chord_m']-v['section_height_m']) for v in frames.values()))
            moving=[]
            for node in garage_nodes:
                ob=next(c for c in node.children if c.type=='MESH');vv=[ob.matrix_world@v.co for v in ob.data.vertices]
                tree=BVHTree.FromPolygons(vv,[f.vertices[:] for f in ob.data.polygons]);moving.append((node,tree))
                frame=bpy.data.objects[node.parent.name+'__Garage_tracks_and_reveals']
                fixed=BVHTree.FromPolygons([frame.matrix_world@v.co for v in frame.data.vertices],[f.vertices[:] for f in frame.data.polygons])
                assert not tree.overlap(fixed),(node.name,float(progress),'garage fixed clearance')
                ceiling=[sum((frame.matrix_world@frame.data.vertices[i].co).z for i in f.vertices)/len(f.vertices) for f in frame.data.polygons if f.normal.z<-.99 and f.area>20]
                assert ceiling;ceiling_gap=min(ceiling_gap,min(ceiling)-max(v.z for v in vv));garage_poses+=1
            for i,(node,tree) in enumerate(moving):
                for other,other_tree in moving[i+1:]:
                    if node['garage_group']==other['garage_group']:assert not tree.overlap(other_tree),(node.name,other.name,float(progress),'section overlap')
        garage_open={o.name:np.array(o.matrix_world).tolist() for o in garage_nodes};pose(0)
        assert chord_error<1e-6 and ceiling_gap>.001
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH']
    # Engine sockets must sit in front of actual fixture lenses. This is a
    # geometric check, separate from the imported socket-frame comparison.
    lens_vertices=[];lens_faces=[]
    for ob in obs:
        if ob.get('component')!='entry':continue
        uv=ob.data.uv_layers.get('EmissionUV')
        if not uv:continue
        for face in ob.data.polygons:
            if not all(.5<uv.data[li].uv.x<.75 for li in face.loop_indices):continue
            start=len(lens_vertices);lens_vertices.extend(ob.matrix_world@ob.data.vertices[i].co for i in face.vertices)
            lens_faces.append(tuple(range(start,len(lens_vertices))))
    lens_tree=BVHTree.FromPolygons(lens_vertices,lens_faces) if lens_faces else None
    light_offsets=[]
    for ob in bpy.context.scene.objects:
        if ob.get('socket_kind')!='engine_light' or not ob.get('light_kind'):continue
        assert lens_tree
        near=lens_tree.find_nearest(ob.matrix_world.translation);distance=float(near[3])
        assert distance<.16,(ob.name,distance,'Socket displaced from fixture lens')
        light_offsets.append(dict(socket=ob.name,nearest_actual_lens_m=distance))
    dormer_hits=[]
    if stem=='Building-305':
        plan=garden(305);w,d=plan['width'],plan['depth'];uw=plan['unit_width'];cw=plan['core_width']
        x=cw/2+uw/2+uw*.25;z=plan['base']+plan['floor_height']+1.5
        for dx in (-.45,0,.45):
            for dz in (-.35,0,.35):
                hit,point,normal,face,ob,xf=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x+dx,-d/2-1.1,z+dz)),Vector((0,1,0)),distance=2.)
                assert hit and 'Bedroom_202' in ob.name,(dx,dz,ob.name if ob else 'void')
                dormer_hits.append(dict(object=ob.name,hit_m=list(point)))
    form=[]
    for wing in [o for o in bpy.context.scene.objects if o.get('access')]:
        bays=sorted([o for o in wing.children if o.type=='MESH' and '__Facade_-1_bay' in o.name],key=lambda o:o.name)
        planes=[min(v.co.y for v in ob.data.vertices) for ob in bays]
        assert planes and np.ptp(planes)>=.60,(wing.name,planes)
        row=dict(wing=wing.name,measured_front_planes_m=planes,measured_depth_range_m=float(np.ptp(planes)))
        if wing.get('access')=='breezeway':
            gallery=next(o for o in wing.children if o.type=='MESH' and o.get('component')=='gallery')
            tree=BVHTree.FromPolygons([gallery.matrix_world@v.co for v in gallery.data.vertices],[f.vertices[:] for f in gallery.data.polygons])
            probes=[]
            for pivot in wing.children:
                if pivot.get('pivot_axis')!='Z' or '__Unit_' not in pivot.name:continue
                station=pivot.matrix_world@Vector((.4572,-.25,.1));hit=tree.ray_cast(station,Vector((0,0,-1)),.6)
                assert hit[0] is not None,(pivot.name,'No gallery surface at the entry approach')
                gap=pivot.matrix_world.translation.z-hit[0].z;assert -.002<=gap<=.05,(pivot.name,gap)
                probes.append(dict(entry=pivot.name,gallery_surface_z_m=hit[0].z,hinge_to_surface_m=gap))
            row['measured_gallery_entry_supports']=probes
        roofs=[o for o in wing.children if o.type=='MESH' and o.get('component')=='roof' and o.name.endswith('__Roof')]
        if roofs and max(v.co.z for v in roofs[0].data.vertices)-min(v.co.z for v in roofs[0].data.vertices)<4:
            roof=roofs[0];height=max(v.co.z for v in roof.data.vertices)-min(v.co.z for v in roof.data.vertices)
            assert height>2.7432,(roof.name,height)
            row['measured_mansard_envelope_height_m']=height
        form.append(row)
    siteparts={o.name:triangles([o]) for o in obs if o.get('component') in ('site','carport','gate') or 'Dumpster_lid_' in o.name or 'Welded dumpster skin' in o.name}
    for name,count in siteparts.items():
        if 'Cluster_mailbox' in name:assert count<=3000,(name,count)
        if 'Carport_' in name or 'Pool_gate_leaf' in name:assert count<=2000,(name,count)
    dumpster_count=sum(n for name,n in siteparts.items() if 'Dumpster' in name or 'Welded dumpster skin' in name)
    assert dumpster_count<=8000,('New dumpster and pad, excluding native fences',dumpster_count)
    architecture=obs
    if stem.startswith('Row'):
        architecture=[o for o in obs if any('_Unit' in a.name for a in parent_chain(o))]
    archtris=triangles(architecture)
    report=dict(source_triangles=triangles(obs),architecture_triangles=archtris,stairs=stair_reports,articulation=form,light_socket_lens_offsets=light_offsets,rightmost_dormer_surface_hits=dormer_hits,
                service_passages=service_gaps,site_mesh_triangles=siteparts,sliding_panel_poses=slider_poses,garage_panel_poses=garage_poses,garage_chord_error_m=chord_error,garage_ceiling_gap_m=ceiling_gap if garage_nodes else None,garage_open_frames=garage_open,pivot_and_socket_count=len(pivots),leaf_casing_sampled_poses=motion_poses,motion_scope='Actual leaf/casing surfaces at 0–100 degrees in 10-degree increments, and slider/fixed sash surfaces at nine track positions; excludes other assemblies and continuous collision claims.',scope='Actual source mesh pan crowns; seven consecutive intervals per eight-riser flight. First-rise/landing/guard checks are separate design assertions, not inferred measurements.')
    return report,pivots,points()


def check(stem):
    path=Path('export')/(stem+'.gltf');meta=json.loads(path.with_suffix('.json').read_text())
    physical,pivots,source_xyz=source(Path('build')/(stem+'.blend'),stem)
    d=external(path);doc=d.json
    assert len(d.binary)==doc['buffers'][0]['byteLength']
    allfiles=[path,path.with_suffix('.bin')]+[path.parent/i['uri'] for i in doc.get('images',[])]
    allfiles=list({p.resolve():p for p in allfiles}.values())
    assert all(p.exists() and not p.is_symlink() for p in allfiles)
    assert all(not Path(i['uri']).is_absolute() and 'bufferView' not in i and (path.parent/i['uri']).resolve().is_relative_to(ROOT) for i in doc.get('images',[]))
    runtime=0;normal_error=0;uv_zero=0;area_zero=0;rawrows=[];max_materials=0;density=[]
    # Count every mesh INSTANCE. Unique accessor counts alone hide instancing bugs.
    for ni,n in enumerate(doc['nodes']):
        if 'mesh' not in n:continue
        xf=d.world(ni)
        for q in doc['meshes'][n['mesh']]['primitives']:
            at=q['attributes'];v=d.accessor(at['POSITION']);norm=d.accessor(at['NORMAL']);uv=d.accessor(at['TEXCOORD_0'])
            assert np.isfinite(v).all() and np.isfinite(norm).all() and np.isfinite(uv).all()
            normal_error=max(normal_error,float(abs(np.linalg.norm(norm,axis=1)-1).max()))
            ind=d.accessor(q['indices']).reshape(-1,3);runtime+=len(ind)
            xyz=v[ind];area=np.linalg.norm(np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]),axis=1)/2
            tc=uv[ind];du=tc[:,1]-tc[:,0];dv=tc[:,2]-tc[:,0];ua=abs(du[:,0]*dv[:,1]-du[:,1]*dv[:,0])/2
            area_zero+=int(np.sum(area<1e-12));uv_zero+=int(np.sum(ua<1e-14))
            # Metric tiling/strip reuse intentionally overlaps UV space.
            # Measure actual image dimensions and chart area, not a constant
            # declared target. Glass has no map and is omitted.
            ma=doc['materials'][q['material']];tex=ma.get('pbrMetallicRoughness',{}).get('baseColorTexture')
            if tex:
                from PIL import Image
                im=doc['images'][doc['textures'][tex['index']]['source']]
                iw,ih=Image.open(path.parent/im['uri']).size
                ok=(area>1e-7)&(ua>1e-13)
                density.extend(zip(np.sqrt(ua[ok]/area[ok]*iw*ih).tolist(),area[ok].tolist()))
            vv=v@xf[:3,:3].T+xf[:3,3];vv=vv[:,[0,2,1]]*np.array([1,-1,1]);rawrows.append(vv)
    assert runtime==physical['source_triangles']==meta['triangles'],(stem,runtime,physical['source_triangles'],meta['triangles'])
    assert normal_error<1e-4,(stem,normal_error)
    assert area_zero==0,(stem,'zero-area geometry',area_zero)
    assert uv_zero==0,(stem,'zero-area staging charts',uv_zero)
    if stem.startswith('Building'):
        assert len(doc['materials'])<=6
        units=meta['plan']['units'];ratio=units/12
        assert 40000*ratio<=runtime<=90000*ratio,(stem,runtime,units)
        assert physical['stairs']
    elif stem.startswith('Row'):
        units=meta['plan']['count'];arch=physical['architecture_triangles']
        assert 40000*units/6<=arch<=80000*units/6,(stem,arch,units)
        assert meta['architecture']['triangles']==arch
    raw_xyz=np.concatenate(rawrows)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    imported_xyz=points();import_tris=triangles([o for o in bpy.context.scene.objects if o.type=='MESH'])
    assert import_tris==runtime,(stem,import_tris,runtime)
    pivot_error=0
    for name,xf in pivots.items():
        ob=bpy.data.objects.get(name);assert ob is not None,name
        pivot_error=max(pivot_error,float(abs(np.array(ob.matrix_world)-np.array(xf)).max()))
    assert pivot_error<2e-5,(stem,pivot_error)
    garage_pose_error=0
    if physical['garage_open_frames']:
        from garage_motion import pose
        pose(1)
        garage_pose_error=max(float(abs(np.array(bpy.data.objects[name].matrix_world)-np.array(xf)).max()) for name,xf in physical['garage_open_frames'].items())
        assert garage_pose_error<3e-5,(stem,garage_pose_error);pose(0)

    # Bidirectional point correspondence is useful for the standalone
    # buildings/rows. Complexes additionally share these exact published forms.
    import_error=0
    if not stem.startswith('Complex'):
        tree=KDTree(len(imported_xyz))
        for i,v in enumerate(imported_xyz):tree.insert(v,i)
        tree.balance();import_error=max(tree.find(v)[2] for v in source_xyz)
        reverse=KDTree(len(source_xyz))
        for i,v in enumerate(source_xyz):reverse.insert(v,i)
        reverse.balance();import_error=max(import_error,max(reverse.find(v)[2] for v in imported_xyz))
        assert import_error<3e-5,(stem,import_error)
    density.sort();dval=np.array([v for v,a in density]);da=np.cumsum([a for v,a in density]);da/=da[-1]
    percentiles=np.interp([.05,.5,.95],da,dval).tolist()
    assert percentiles[0]>40 and percentiles[2]<12000,(stem,percentiles)
    from PIL import Image
    images={str((path.parent/i['uri']).resolve()):Image.open(path.parent/i['uri']).size for i in doc.get('images',[])}
    gpu_mib=sum(w*h*4/3/1024**2 for w,h in images.values())
    return dict(passed=True,physical=physical,runtime_triangles=runtime,unique_mesh_triangles=sum(doc['accessors'][q['indices']]['count']//3 for me in doc['meshes'] for q in me['primitives']),
                materials=len(doc['materials']),images=len(doc.get('images',[])),normal_length_error=normal_error,
                degenerate_triangles=area_zero,degenerate_metric_uvs=uv_zero,garage_open_import_frame_error=garage_pose_error if physical['garage_open_frames'] else None,pivot_frame_error=pivot_error,source_import_point_error_m=import_error if not stem.startswith('Complex') else None,
                source_import_point_scope='Bidirectional nearest-vertex correspondence' if not stem.startswith('Complex') else 'Not measured for the whole site; forms are checked in standalone exports, with runtime counts and pivot/socket frames checked here.',
                bytes=sum(p.stat().st_size for p in allfiles),files={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in allfiles},
                density_area_weighted_p5_p50_p95_px_m=percentiles,gpu_mib_8bpp_full_mips=gpu_mib,draw_primitives=sum(len(doc['meshes'][n['mesh']]['primitives']) for n in doc['nodes'] if 'mesh' in n),
                uv_scope='Intentional metric material tiling and trim-sheet reuse; UV0 areas and density measured on raw accessors. UV1 is the constant emission routing chart. Overlap across repeated tile/trim instances is intentional; no unique atlas packing is claimed.')


def main():
    for s in range(1000):
        g=garden(301+s);r=row(401+s);assert 8<=g['units']<=24;assert 4<=r['count']<=8
    bad=0
    for f in (lambda:row(count=3),lambda:row(width_ft=25),lambda:garden(floors=4,shape='offset'),lambda:garden(nonexistent=1)):
        try:f()
        except (ValueError,AssertionError):bad+=1
    assert bad==4
    report=dict(plan_sweeps=1000,negative_controls=4,assets={})
    for stem in [*[f'{kind}-{s}' for s in COMPLEX_SEEDS for kind in ('Building','Complex')],'Building-305',*[f'Row-{s}' for s in ROW_SEEDS]]:
        report['assets'][stem]=check(stem);print('PASS',stem,report['assets'][stem]['runtime_triangles'],flush=True)
        Path('build/check.json').write_text(json.dumps(report,indent=2))
    baseline=Path('build/preservation.json')
    if baseline.exists():
        old=json.loads(baseline.read_text());changed=[p for p,h in old.items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
        assert not changed,changed;report['preserved_existing_files']=len(old)
    report['passed']=True;Path('build/check.json').write_text(json.dumps(report,indent=2));print('APARTMENTS CHECK PASS',flush=True)

if __name__=='__main__':main()
