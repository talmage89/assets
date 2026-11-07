"""Independent exported geometry, layout, resource and sampled motion checks.

This checkpoint certifies script construction/serialization, not a physical
playground, surfacing impact attenuation, final UV atlases or baked look-dev.
"""
import argparse,hashlib,itertools,json,math,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.motion import sweep,surface as motion_surface


def imported(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];pts=[];count=0
    for o in meshes:
        o.data.calc_loop_triangles();count+=len(o.data.loop_triangles)
        pts.extend(o.matrix_world@v.co for v in o.data.vertices)
        assert all(math.isfinite(v) for p in o.data.vertices for v in p.co)
        assert all(.99<loop.normal.length<1.01 for loop in o.data.loops),o.name
        assert o.data.uv_layers,o.name
        assert all(math.isfinite(v) for uv in o.data.uv_layers.active.data for v in uv.uv),o.name
    bounds=[[float(f(p[k] for p in pts)) for k in range(3)] for f in (min,max)]
    return meshes,count,bounds


def raw(path):
    doc=json.loads(path.read_text());buffers=[(path.parent/b['uri']).read_bytes() for b in doc['buffers']]
    comps={5126:np.float32,5125:np.uint32,5123:np.uint16,5121:np.uint8};sizes={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
    def accessor(i):
        a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];dt=np.dtype(comps[a['componentType']]);n=sizes[a['type']];offset=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',dt.itemsize*n)
        return np.ndarray((a['count'],n),dtype=dt,buffer=buffers[v['buffer']],offset=offset,strides=(stride,dt.itemsize))
    for mesh in doc['meshes']:
        for p in mesh['primitives']:
            v=accessor(p['attributes']['POSITION']);idx=accessor(p['indices']).ravel();assert idx.max()<len(v)
            n=accessor(p['attributes']['NORMAL']);assert np.max(abs(np.linalg.norm(n,axis=1)-1))<.003
            assert 'TEXCOORD_0' in p['attributes'];assert len(idx)%3==0
    images=[]
    for im in doc.get('images',[]):
        assert 'uri' in im and not im['uri'].startswith('data:');p=path.parent/im['uri'];assert p.exists(),p
        images.append(dict(uri=im['uri'],bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    return dict(gltf_bytes=path.stat().st_size,bin_bytes=sum(len(b) for b in buffers),materials=len(doc.get('materials',[])),images=images)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/check.json'));args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);args.out.unlink(missing_ok=True);manifest=json.loads(Path('build/manifest.json').read_text());result=dict(stage=manifest['stage'],pieces={},sites={},scope='Measured imported meshes/resources and sampled motion; authored shared manufacture UV repetition is intentional. Bake/UV checks are separate.')
    for name,source in manifest['pieces'].items():
        path=Path('export')/(name+'.gltf');meshes,n,bb=imported(path);cap=3916 if name.startswith('Slide') else 1954
        assert n<=cap,(name,n,cap);assert n==source['triangles'],(name,n,source['triangles']);assert np.max(abs(np.array(bb)-source['bounds_m']))<3e-5,(name,bb,source['bounds_m'])
        row=dict(triangles=n,bounds_m=bb,**raw(path));result['pieces'][name]=row
        if name=='Post2339':
            coords=[o.matrix_world@v.co for o in meshes for v in o.data.vertices];ring=[p for p in coords if abs(p.z)<1e-5];r=sorted(set(round(math.hypot(p.x,p.y),7) for p in ring));row['measured_post_od_m']=2*max(r);row['measured_wall_m']=max(r)-min(r);assert abs(2*max(r)-.127)<1e-5
        if name=='Deck':
            zz=sorted(set(round((o.matrix_world@v.co).z,7) for o in meshes for v in o.data.vertices if abs((o.matrix_world@v.co).x)<.54 and abs((o.matrix_world@v.co).y)<.54));row['standing_skin_z_levels_m']=zz
        if name.startswith('Slide'):
            root=next(o for o in bpy.context.scene.objects if 'slide_kind' in o);pts=np.array(root['path_m']);ds=np.linalg.norm(np.diff(pts[:,:2],axis=0),axis=1);dz=np.diff(pts[:,2]);slopes=np.degrees(np.arctan2(abs(dz),ds));row['centerline_max_slope_degrees']=float(max(slopes));row['exit_height_m']=float(pts[-1,2]);row['last_flat_region_m']=float(sum(ds[-3:]));assert max(slopes)<50;assert .177<=pts[-1,2]<=.2795;assert row['last_flat_region_m']>=.2794
        if name in ('SlideWave72','SlideTube48'):
            # Section the imported molded triangles at three centerline stations.
            # These are measured surfaces, not copies of the generating profile.
            profiles=[]
            for index in (3,len(pts)//2,len(pts)-5):
                origin=Vector(pts[index]);normal=Vector(pts[index+1]-pts[index-1]).normalized();u=Vector((1,0,0));v=normal.cross(u).normalized();segments=[]
                for ob in meshes:
                    ob.data.calc_loop_triangles()
                    for tri in ob.data.loop_triangles:
                        if not any(k in ob.data.materials[tri.material_index].name for k in ('QuickMolded','Playground_Molded')):continue
                        vv=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices];signed=[(p-origin).dot(normal) for p in vv];cross=[]
                        for i in range(3):
                            j=(i+1)%3
                            if abs(signed[i])<1e-7 and not any((vv[i]-q).length<1e-7 for q in cross):cross.append(vv[i])
                            if signed[i]*signed[j]<0:
                                point=vv[i].lerp(vv[j],signed[i]/(signed[i]-signed[j]))
                                if not any((point-q).length<1e-7 for q in cross):cross.append(point)
                        if len(cross)==2:segments.append([[float((p-origin).dot(u)),float((p-origin).dot(v))] for p in cross])
                assert segments,(name,index)
                profiles.append(dict(station=index,center_m=list(origin),segments_m=segments))
            row['imported_molded_sections']=profiles
        if name in ('Ladder72','VerticalLadder48'):
            root=next(o for o in bpy.context.scene.objects if o.type=='EMPTY' and o.get('module')==name);limit=max(o.matrix_world.translation.z for o in root.children_recursive if o.get('socket_kind')=='child_hand_foot');sample=[]
            for ob in meshes:
                sample.extend((ob.matrix_world@v.co).z for v in ob.data.vertices if .34<abs((ob.matrix_world@v.co).x)<.40 and abs((ob.matrix_world@v.co).y)<.025 and .05<(ob.matrix_world@v.co).z<limit+.025)
            groups=[]
            for z in sorted(sample):
                if groups and z-groups[-1][-1]<.10:groups[-1].append(z)
                else:groups.append([z])
            levels=[(min(g)+max(g))/2 for g in groups];intervals=[b-a for a,b in zip([0]+levels,levels)];row['measured_rung_rises_m']=intervals;assert max(intervals)<=.3049,(name,intervals)
        if name=='RampSegment':
            points=[]
            for o in meshes:
                for poly in o.data.polygons:
                    if any(k in o.data.materials[poly.material_index].name for k in ('QuickPerforated','Playground_Deck')) and (o.matrix_world.to_3x3().inverted().transposed()@poly.normal).normalized().z>.8:
                        points.extend(o.matrix_world@o.data.vertices[v].co for v in poly.vertices)
            lo=min(p.y for p in points);hi=max(p.y for p in points);z0=max(p.z for p in points if abs(p.y-lo)<1e-5);z1=max(p.z for p in points if abs(p.y-hi)<1e-5)
            row['measured_slope']=(z1-z0)/(hi-lo);assert abs(row['measured_slope']-1/12)<1e-5
            row['nominal_infill_clear_m']=1.2192/12-.019;assert row['nominal_infill_clear_m']<.0889
    for source in manifest['sites']:
        seed=source['seed'];path=Path(f'export/Playground-{seed}.gltf');meshes,n,bb=imported(path);assert n<120000,(seed,n);assert n==source['total_triangles'],(seed,n,source['total_triangles']);row=dict(total_triangles=n,equipment_triangles=source['equipment_triangles'],**raw(path));zones=source['zones'];surface=source['surface'];gaps=[]
        for z in zones:
            a0,b0,a1,b1=z['rect'];assert surface[0]<=a0 and surface[1]<=b0 and surface[2]>=a1 and surface[3]>=b1,(seed,z,surface)
        for left,right in itertools.combinations(zones,2):
            a,b,c,d=left['rect'];e,f,g,h=right['rect'];dx=max(a-e if a>g else e-c,0);dy=max(b-f if b>h else f-d,0)
            overlap=max(0,min(c,g)-max(a,e))*max(0,min(d,h)-max(b,f));assert overlap<1e-7,(seed,left['name'],right['name'],overlap)
            gaps.append(dict(groups=[left['group'],right['group']],envelope_gap_m=math.hypot(max(a-g,e-c,0),max(b-h,f-d,0))))
        row['zone_gaps']=gaps
        roofs=[o for o in bpy.context.scene.objects if o.type=='EMPTY' and o.get('module') in ('HipRoof','Shade') and o.get('zone_group')=='composite']
        roof_pairs=[]
        for a,b in itertools.combinations(roofs,2):
            sa=motion_surface(next(o for o in a.children_recursive if o.type=='MESH'));sb=motion_surface(next(o for o in b.children_recursive if o.type=='MESH'))
            crossings=len(sa['tree'].overlap(sb['tree']));assert crossings==0,(seed,'intersecting roofs',a.name,b.name,crossings)
            roof_pairs.append(dict(roofs=[a.name,b.name],actual_triangle_crossings=crossings))
        row['roof_pairs']=roof_pairs
        # Independent real-surface contacts, separate from serialization.
        decks=[o for o in bpy.context.scene.objects if o.type=='EMPTY' and o.get('module') in ('Deck','Deck72') and o.get('zone_group')=='composite']
        ds={r.name:motion_surface(next(o for o in r.children_recursive if o.type=='MESH')) for r in decks};contacts=[]
        attachments=('Slide','Stairs','Transfer','Arch','Ladder','VerticalLadder','ChainNet','RockWall','RampHeadBridge')
        for rt in [o for o in bpy.context.scene.objects if o.type=='EMPTY' and o.get('zone_group')=='composite' and str(o.get('module','')).startswith(attachments)]:
            from mathutils.bvhtree import BVHTree
            entry=next(o for o in rt.children_recursive if o.get('socket_kind') in ('deck_interface','slide_entry'))
            inverse=rt.matrix_world.inverted();height=(inverse@entry.matrix_world.translation).z
            ob=next(o for o in rt.children_recursive if o.type=='MESH');ob.data.calc_loop_triangles();points=[ob.matrix_world@v.co for v in ob.data.vertices];local=[inverse@p for p in points]
            faces=[tuple(t.vertices) for t in ob.data.loop_triangles if all(-.025<=local[v].y<=.201 and abs(local[v].z-height)<.031 for v in t.vertices)]
            assert faces,('no actual entry faces',rt.name)
            tree=BVHTree.FromPolygons(points,faces,all_triangles=True);hits={name:len(tree.overlap(other['tree'])) for name,other in ds.items()};assert any(hits.values()),(seed,'unsupported event entry',rt.name)
            contacts.append(dict(event=rt.name,deck_triangle_crossings={k:v for k,v in hits.items() if v},scope='Actual exported fastened-interface crossings; not load/strength testing'))
        row['event_deck_contacts']=contacts
        # Fire-pole reach is measured to the real deck top edge, not the grid line.
        for rt in [o for o in bpy.context.scene.objects if o.get('module')=='FirePole' and o.get('zone_group')=='composite']:
            inv=rt.matrix_world.inverted();entry=next(o for o in rt.children_recursive if o.get('socket_kind')=='deck_entry');height=(inv@entry.matrix_world.translation).z
            ob=next(o for o in rt.children_recursive if o.type=='MESH');pv=[inv@ob.matrix_world@v.co for v in ob.data.vertices];base=[p for p in pv if abs(p.x)<.10 and abs(p.z)<.03];axis_y=(min(p.y for p in base)+max(p.y for p in base))/2
            edge=[]
            for root in decks:
                ob=next(o for o in root.children_recursive if o.type=='MESH')
                for poly in ob.data.polygons:
                    if any(k in ob.data.materials[poly.material_index].name for k in ('QuickPerforated','Playground_Deck')) and (ob.matrix_world.to_3x3().inverted().transposed()@poly.normal).normalized().z>.9:
                        edge.extend(inv@ob.matrix_world@ob.data.vertices[v].co for v in poly.vertices)
            edge=[p for p in edge if abs(p.z-height)<1e-4 and abs(p.x)<.60 and 0<=p.y<1.3];reach=min(p.y for p in edge)-axis_y
            assert .4572<=reach<=.508,(seed,'pole reach',reach)
            row['fire_pole_measured_reach_m']=reach;row['fire_pole_above_deck_m']=max(p.z for p in pv)-height;assert row['fire_pole_above_deck_m']>=1.524
        # Actual seat-to-leg and seat-to-seat transverse clearances at rest.
        frame=next(o for o in bpy.context.scene.objects if o.get('module') in ('SwingFrame','SwingArchFrame') and o.get('zone_group')=='swing');fm=next(o for o in frame.children_recursive if o.type=='MESH');fp=[fm.matrix_world@v.co for v in fm.data.vertices]
        groups=[]
        for x in sorted(p.x for p in fp if abs(p.z)<.06):
            if groups and x-groups[-1][-1]<.2:groups[-1].append(x)
            else:groups.append([x])
        assert len(groups)==3;supports=[(min(g),max(g)) for g in groups];seats=[]
        for root in [o for o in bpy.context.scene.objects if o.get('module') in ('SwingBelt','SwingBucket') and o.get('zone_group')=='swing']:
            ob=next(o for o in root.children_recursive if o.type=='MESH');ss=[]
            for ob in root.children_recursive:
                if ob.type!='MESH':continue
                for poly in ob.data.polygons:
                    if any(k in ob.data.materials[poly.material_index].name for k in ('QuickMolded','Playground_Molded')):ss.extend(ob.matrix_world@ob.data.vertices[v].co for v in poly.vertices)
            seats.append((min(p.x for p in ss),max(p.x for p in ss)))
        seats.sort();sides=[]
        for left,right in seats:
            bay=next(i for i in range(2) if supports[i][1]<left and right<supports[i+1][0]);sides.append(min(left-supports[bay][1],supports[bay+1][0]-right))
        gaps_between=[seats[i+1][0]-seats[i][1] for i in (0,2)];assert min(sides)>=.762,(seed,'seat to leg',sides);assert min(gaps_between)>=.6096,(seed,'seat separation',gaps_between)
        swing_zone=next(z['rect'] for z in zones if z['group']=='swing');lateral=[min(p.x for p in fp)-swing_zone[0],swing_zone[2]-max(p.x for p in fp)];assert min(lateral)>=1.8287
        row['measured_swing_clearances_m']=dict(seat_to_leg=min(sides),between_seats=min(gaps_between),lateral_use_zone=lateral)
        ground=next(o for o in bpy.context.scene.objects if o.get('module')=='Siteworks');gm=next(o for o in ground.children_recursive if o.type=='MESH');gp=[gm.matrix_world@v.co for v in gm.data.vertices];cy=frame.matrix_world.translation.y
        band=[p.z for p in gp if min(q.x for q in fp)<=p.x<=max(q.x for q in fp) and abs(p.y-cy)<1.5 and p.z<.01];low=min(band)
        pivz=[o.matrix_world.translation.z for o in bpy.context.scene.objects if o.get('motion_kind')=='rigid_swing_with_chains'];twice=2*(max(pivz)-low);front_back=[cy-swing_zone[1],swing_zone[3]-cy];assert min(front_back)>=twice
        row['measured_swing_clearances_m'].update(twice_pivot_to_low_surface=twice,front_back_use_zone=front_back)
        # Sample real imported swing assemblies against the frame and one another.
        # Hangers belong to the fixed frame; chains are near-clearance surfaces.
        def ancestry(o):
            while o:
                yield o;o=o.parent
        for o in meshes:
            if any('Swing' in p.name for p in ancestry(o)):o['asset_set']='Playground'
            elif 'asset_set' in o:del o['asset_set']
        pivots=[o for o in bpy.context.scene.objects if o.get('motion_kind')=='rigid_swing_with_chains']
        specs=[]
        for pivot in pivots:
            ownermesh=next(o for o in pivot.children if o.type=='MESH');fixed=next(o for o in pivot.parent.children if o.type=='MESH')
            specs.append(dict(node=pivot.name,axis='X',range=[-55,55],step=11,tolerance_m=.001,allow=[dict(moving=ownermesh.name,fixed=fixed.name,reason='Intentional hanger bearing articulation at the pivot')]))
        motion=sweep(dict(MOTIONS=specs));assert motion['passed'],motion;row['swing_motion']=motion;result['sites'][str(seed)]=row
    protected=Path('build/protected.json')
    if protected.exists():
        inventory=json.loads(protected.read_text());assert all((ROOT/k).exists() and hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in inventory.items());result['protected_existing_deliveries']=len(inventory)
    result['passed']=True;args.out.write_text(json.dumps(result,indent=2));print('CHECK PASSED',len(result['pieces']),'modules;',[(k,v['total_triangles']) for k,v in result['sites'].items()])
if __name__=='__main__':main()
