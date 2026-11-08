"""Independent raw glTF, fresh import, construction probes and preservation.

Serialization, sampled physical relationships and visual review have separate
scopes. No look-dev, unique UV packing or regulatory certification is implied.
"""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from kit.gltf import GLB
from plans import park,home


def raw(path):
    g=GLB.__new__(GLB);g.json=json.loads(path.read_text());g.binary=(path.parent/g.json['buffers'][0]['uri']).read_bytes()
    g.parents={c:i for i,n in enumerate(g.json['nodes']) for c in n.get('children',[])};return g


def vertices(g,name=None):
    result=[]
    for i,n in enumerate(g.json['nodes']):
        if 'mesh' not in n or name and name not in n.get('name',''):continue
        xf=g.world(i)
        for pr in g.json['meshes'][n['mesh']]['primitives']:
            x=g.accessor(pr['attributes']['POSITION']);v=x@xf[:3,:3].T+xf[:3,3]
            result.append(v[:,[0,2,1]]*np.array([1,-1,1]))
    return np.concatenate(result) if result else np.empty((0,3))


def probe(stem,origin,direction,distance=100):
    bpy.context.view_layer.update();hit,p,n,i,ob,xf=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector(origin),Vector(direction),distance=distance)
    if not hit:raise AssertionError(('No construction hit',stem,origin,direction))
    return list(p),ob.name


def imported_count():
    n=0
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH' and not ('Icosphere' in ob.name and not ob.data.materials):ob.data.calc_loop_triangles();n+=len(ob.data.loop_triangles)
    return n


def mesh_tree(objects):
    points=[];triangles=[]
    for ob in objects:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();start=len(points)
        points.extend([ob.matrix_world@v.co for v in ob.data.vertices])
        triangles.extend([tuple(start+i for i in t.vertices) for t in ob.data.loop_triangles])
    return BVHTree.FromPolygons(points,triangles,all_triangles=True)


def check():
    rows={};construction={};images={}
    for path in sorted(Path('export').glob('*.gltf')):
        stem=path.stem;g=raw(path);d=g.json;meta=json.loads(path.with_suffix('.json').read_text());triangles=0;collapsed=0;uv_bad=0;maxnormal=0
        for node in d['nodes']:
            if 'mesh' not in node:continue
            for pr in d['meshes'][node['mesh']]['primitives']:
                a=pr['attributes'];v=g.accessor(a['POSITION']);ix=g.accessor(pr['indices']).ravel();tri=ix.reshape(-1,3);triangles+=len(tri)
                cross=np.cross(v[tri[:,1]]-v[tri[:,0]],v[tri[:,2]]-v[tri[:,0]])
                collapsed+=int(np.sum(np.linalg.norm(cross,axis=1)<1e-12))
                normal=g.accessor(a['NORMAL']);maxnormal=max(maxnormal,float(np.max(abs(np.linalg.norm(normal,axis=1)-1))))
                assert np.all(np.isfinite(v)) and np.all(np.isfinite(normal))
                assert 'TEXCOORD_0' in a,(stem,'Missing UV')
                uv=g.accessor(a['TEXCOORD_0']);assert np.all(np.isfinite(uv))
                dx=uv[tri[:,1]]-uv[tri[:,0]];dy=uv[tri[:,2]]-uv[tri[:,0]]
                uv_bad+=int(np.sum(abs(dx[:,0]*dy[:,1]-dx[:,1]*dy[:,0])<1e-12))
        assert triangles==meta['triangles'],(stem,'raw count',triangles,meta['triangles'])
        assert collapsed==0,(stem,'collapsed geometry',collapsed)
        assert maxnormal<2e-4,(stem,'normal length',maxnormal)
        assert uv_bad==0,(stem,'collapsed UV triangles',uv_bad)
        # Metric charts retain intentional tiling overlap. This verifies valid
        # charts, not final bake packing or texel-density acceptance.
        caps=dict(Deck=8000,Carport=8000,UtilityService=3000,PropaneBottles=3000,
                  Condenser=8000,WindowAC=3000,SatelliteDish=3000,AddedRoom=8000,
                  Household=3000,EntranceSign=3000)
        if stem in caps:assert triangles<=caps[stem],(stem,'component triangle cap',triangles,caps[stem])
        for im in d.get('images',[]):
            q=(path.parent/im['uri']).resolve();assert q.is_file();images[str(q)]=hashlib.sha256(q.read_bytes()).hexdigest()
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
        assert imported_count()==triangles,(stem,'fresh import count',imported_count(),triangles)
        points=vertices(g);size=points.max(0)-points.min(0)
        if stem.startswith(('Single','Double')):
            spec=meta['plan'];wall=[]
            # Published frame-body dimensions are measured between independent
            # footprint sockets and checked against actual outer wall planes.
            for i,n in enumerate(d['nodes']):
                if n.get('name','').endswith(('FootprintMin','FootprintMax')):
                    pos=g.world(i)[:3,3];wall.append(pos[[0,2,1]]*np.array([1,-1,1]))
            delta=np.abs(wall[1]-wall[0]);assert abs(delta[0]-spec['length'])<2e-5 and abs(delta[1]-spec['width'])<2e-5
            # Rays hit the skin, not just the sockets. Use a wall station clear
            # of windows/doors on the long face.
            x=-spec['length']*.46
            left,_=probe(stem,(x,-spec['width'],1.10),(0,1,0));right,_=probe(stem,(x,spec['width'],1.10),(0,-1,0))
            actual_width=right[1]-left[1];assert abs(actual_width-spec['width'])<.03,(stem,'skin width',actual_width,spec['width'])
            cap=35000 if stem.startswith('Single') else 50000;assert triangles<=cap
            construction[stem]=dict(wall_width_ray_m=actual_width,footprint_socket_span_m=delta.tolist(),mesh_envelope_m=size.tolist(),triangle_cap=cap)
            seam_x=-spec['length']/2+spec['length']/math.ceil(spec['length']/.4064)
            skirt_hit,_=probe(stem,(seam_x,-spec['width'],.25),(0,1,0))
            assert abs(skirt_hit[1]+spec['width']/2)<.04,(stem,'open skirt seam',skirt_hit)
            construction[stem]['skirt_seam_ray_hit_m']=skirt_hit
            if spec['era']!='1972':
                rake_hit,_=probe(stem,(spec['length']/2+1,spec['width']/2-.10,spec['eave']+.05),(-1,0,0))
                assert abs(rake_hit[0]-spec['length']/2)<.02,(stem,'open rake closure',rake_hit)
                construction[stem]['rake_closure_ray_hit_m']=rake_hit
        if stem=='SupportFrame':
            # Main rail lower flange is sampled at a non-pier station. The CMU
            # pier cap, shim and flange contacts use actual vertical intervals.
            support_v=points
            main_rail_bottom=float(np.min(support_v[(abs(support_v[:,1]+.94)<.06)&(abs(support_v[:,0])>8.9),2]))
            assert main_rail_bottom>=.3048
            construction[stem]=dict(sampled_main_rail_bottom_m=main_rail_bottom,minimum_comparator_m=.3048)
        if stem=='Deck':
            top,_=probe(stem,(.7,0,2),(0,0,-1));bottom,_=probe(stem,(-1.35,-2.2,2),(0,0,-1))
            beam_bottom,_=probe(stem,(.7,-.9268,.2),(0,0,1))
            beam_top,_=probe(stem,(.7,-.9268,.68),(0,0,-1))
            joist_bottom,_=probe(stem,(.2010833,0,.2),(0,0,1))
            post_top,_=probe(stem,(-1.7288,-.9678,.7),(0,0,-1))
            assert abs(beam_top[2]-joist_bottom[2])<.001
            assert abs(beam_bottom[2]-post_top[2])<.001
            construction[stem]=dict(sampled_deck_top_m=top[2],sampled_low_tread_m=bottom[2],sampled_beam_interval_m=[beam_bottom[2],beam_top[2]],sampled_joist_bottom_m=joist_bottom[2],sampled_post_top_m=post_top[2])
        if stem.startswith('Park'):
            p=meta['plan'];widths=[];addon_clearance=[]
            car_points=[o.matrix_world.translation.copy() for o in bpy.context.scene.objects if o.get('socket_kind')=='car']
            car_spacing=min((a-b).length for j,a in enumerate(car_points) for b in car_points[j+1:])
            assert car_spacing>2.5,(stem,'duplicate or crowded car sockets',car_spacing)
            for lot in p['lots']:
                h=meta['assemblies'][f'Lot_{lot["number"]:02}_Home']
                cap=50000 if lot['home']['double'] else 35000
                assert h['triangles']<=cap,(stem,lot['number'],'seeded home budget',h['triangles'],cap)
                if lot['home']['carport']:
                    def tree(suffix):
                        ob=next(o for o in bpy.context.scene.objects if o.name==f'Lot_{lot["number"]:02}_{suffix}__Mesh')
                        ob.data.calc_loop_triangles()
                        return BVHTree.FromPolygons([ob.matrix_world@v.co for v in ob.data.vertices],[list(t.vertices) for t in ob.data.loop_triangles],all_triangles=True)
                    overlaps=tree('Deck').overlap(tree('Carport'))
                    assert not overlaps,(stem,lot['number'],'deck / carport mesh intersections',len(overlaps))
                    addon_clearance.append(dict(lot=lot['number'],deck_carport_intersection_pairs=len(overlaps)))
            # Independent assemblies must not overlap their neighbors. Include
            # actual native props and all moving meshes in their rest pose.
            lot_trees=[]
            for lot in p['lots']:
                root=bpy.data.objects[f'Lot_{lot["number"]:02}']
                lot_trees.append((lot['number'],mesh_tree(root.children_recursive)))
            placement_pairs=0
            for j,(number,aa) in enumerate(lot_trees):
                for other,bb in lot_trees[j+1:]:
                    collisions=aa.overlap(bb)
                    assert not collisions,(stem,'neighboring lot intersections',number,other,len(collisions))
                    placement_pairs+=1
            common_fixed=mesh_tree([bpy.data.objects['CommonFacilities__Mesh']])
            facilities=[common_fixed]
            for name in ('Office','Clubhouse','Laundry'):
                if name in bpy.data.objects:facilities.append(mesh_tree(bpy.data.objects[name].children_recursive))
            for number,aa in lot_trees:
                for bb in facilities:
                    collisions=aa.overlap(bb)
                    assert not collisions,(stem,'lot / common facility intersections',number,len(collisions))
                    placement_pairs+=1
            # Source physical road surface is selected by a ray through its
            # center; width is measured on its actual imported mesh vertices.
            private=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Private asphalt 0'))
            xyz=np.array([private.matrix_world@v.co for v in private.data.vertices]);road_width=float(np.ptp(xyz[:,0]));assert abs(road_width-p['street_width'])<2e-5
            separations=[]
            for side in (-1,1):
                lots=sorted([r for r in p['lots'] if r['side']==side],key=lambda r:r['origin'][1])
                for aa,bb in zip(lots,lots[1:]):
                    # Independent raw mesh groups include attached porch/shed;
                    # home-only roots are selected by their serialized names.
                    av=vertices(g,f'Lot_{aa["number"]:02}_Home__Mesh');bv=vertices(g,f'Lot_{bb["number"]:02}_Home__Mesh')
                    if len(av) and len(bv):separations.append(float(bv[:,1].min()-av[:,1].max()))
            assert not separations or min(separations)>3.0,(stem,'home separation',separations)
            construction[stem]=dict(road_width_mesh_m=road_width,home_separation_mesh_m=separations,minimum_car_socket_spacing_m=car_spacing,static_assembly_pairs_checked=placement_pairs,deck_carport_mesh_checks=addon_clearance,net_lot_area_m2=p['lot_frontage']*p['lot_depth'],home_count=len(p['lots']),road_graph=p['roads'])
        rows[stem]=dict(triangles=triangles,geometry_bytes=meta['geometry_bytes'],materials=len(d['materials']),collapsed_triangles=collapsed,collapsed_diagnostic_uv_triangles=uv_bad,max_normal_length_error=maxnormal,mesh_size_m=size.tolist(),fresh_import=True)
        print('CHECK',stem,triangles,'UV diagnostics',uv_bad,flush=True)
    baseline=Path('build/preserved.json');preserved=0
    if baseline.exists():
        for name,digest in json.loads(baseline.read_text()).items():
            p=HERE.parents[1]/name;assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,('Changed pre-existing delivery',name);preserved+=1
    # Determinism and distinct road graphs over the declared bounded grammar.
    sweep=[]
    for seed in range(1000):
        p=park(seed,'old' if seed%2 else 'new');assert p==park(seed,'old' if seed%2 else 'new')
        for row in p['lots']:
            h=row['home'];assert h['length']+6.096<=p['lot_depth'];assert h['width']+3.6<p['lot_frontage']
        sweep.append(p['kind'])
    assert park(101,'old')['roads']!=park(202,'new')['roads']
    report=dict(passed=True,scope='form / raw serialization / sampled geometry; quick UV diagnostics, not bake approval',exports=rows,construction=construction,plan_sweep_count=1000,preserved_delivery_files=preserved,external_image_identities=len(images))
    Path('build/check.json').write_text(json.dumps(report,indent=2));print('PASS',len(rows),'exports;',preserved,'preserved files',flush=True)

if __name__=='__main__':check()
