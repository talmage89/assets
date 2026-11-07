"""Independent fresh-import form checks. No claim of final UV/bake readiness."""
import sys,json,math,hashlib,subprocess,argparse
from collections import defaultdict
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from geometry import count
from plan import plan,SEEDS

def imported(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    return {o.name:o for o in bpy.context.scene.objects if not o.parent}

def material_vertices(rt,kind):
    out=[]
    for o in [rt,*rt.children_recursive]:
        if o.type!='MESH':continue
        ids={i for p in o.data.polygons if kind in o.data.materials[p.material_index].name or (kind=='Zinc' and o.data.materials[p.material_index].name.startswith('Skate_Trim_Steel')) for i in p.vertices}
        out += [rt.matrix_world.inverted()@o.matrix_world@o.data.vertices[i].co for i in ids]
    return out

def bvh(roots,material=None):
    verts=[];faces=[]
    for rt in roots:
        for ob in [rt,*rt.children_recursive]:
            if ob.type!='MESH':continue
            n=len(verts);verts += [ob.matrix_world@v.co for v in ob.data.vertices]
            ob.data.calc_loop_triangles()
            faces += [tuple(n+i for i in tri.vertices) for tri in ob.data.loop_triangles if material is None or material in ob.data.materials[tri.material_index].name]
    return BVHTree.FromPolygons(verts,faces,all_triangles=True)

def circle(points):
    q=np.asarray(points);A=np.c_[2*q,np.ones(len(q))];x=np.linalg.lstsq(A,(q*q).sum(axis=1),rcond=None)[0]
    r=math.sqrt(x[2]+sum(x[:2]**2));err=np.abs(np.linalg.norm(q-x[:2],axis=1)-r)
    return dict(center_m=x[:2].tolist(),radius_m=r,max_radial_error_m=float(err.max()),stations=len(q))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--folder',type=Path,default=Path('export/checkpoint'));args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);folder=args.folder
    source=json.loads(Path('build/Skatepark.json').read_text());lib=imported(folder/'SkateparkPieces.glb');report=dict(stage=source['stage'],pieces={},construction={},parks={},limitations=['Terrain UV reuse is intentional; density and accidental surface intersections are checked separately.','Contour phase matches are inferred, not surveyed correspondences.'])
    for name,expected in source['pieces'].items():
        n=count(lib[name]);assert n==expected['triangles'],(name,n,expected['triangles']);assert 0<n<=4000,(name,n)
        report['pieces'][name]=n
    for name,expected in [('Quarter_4ft',2.1336),('Quarter_5ft',2.4384)]:
        rt=lib[name];v=material_vertices(rt,'Concrete');pts=[(p.y,p.z) for p in v if .0001<p.z<float(rt['height_m'])-.0001 and p.y<float(rt['profile_run_m'])/2+.0001]
        data=circle(pts);assert abs(data['radius_m']-expected)<2e-5,data;assert data['max_radial_error_m']<2e-5;report['construction'][name]=data
        steel=material_vertices(rt,'Steel');diameter=max(p.z for p in steel)-min(p.z for p in steel);assert abs(diameter-.060325)<2e-5
        data['coping_od_m']=diameter
    groups=defaultdict(list);sections=[];down=0
    for k in range(16):
        rt=lib['Bowl_Sector_%02d'%k];ob=next(o for o in rt.children_recursive if o.type=='MESH')
        for f in ob.data.polygons:
            if 'Concrete' not in ob.data.materials[f.material_index].name or f.center.z>=-.0001:continue
            down+=int(f.normal.z<=0)
            for li in f.loop_indices:
                p=ob.data.vertices[ob.data.loops[li].vertex_index].co;key=tuple(round(x,5) for x in p)
                groups[key].append((k,ob.data.corner_normals[li].vector.copy()))
        sections += material_vertices(rt,'Concrete')
    assert down==0,('Folded or downward-facing bowl triangles',down)
    smallest=1.0;pairs=0
    for vals in groups.values():
        for k,n in vals:
            for j,m in vals:
                if k!=j:smallest=min(smallest,n.dot(m));pairs+=1
    assert pairs>1000 and smallest>.99998,(pairs,smallest)
    report['construction']['bowl_seams']=dict(shared_corner_comparisons=pairs,minimum_normal_dot=smallest,max_normal_angle_degrees=math.degrees(math.acos(min(1,smallest))),downward_triangles=down)
    for prefix in ('Bowl_Floor','SteelBowl_Floor'):
        floors=[rt for name,rt in lib.items() if name.startswith(prefix)]
        points=[v for rt in floors for v in material_vertices(rt,'Concrete')]
        drain=next(o for rt in floors for o in rt.children_recursive if o.get('socket_kind')=='drain')
        minimum=min(v.z for v in points);assert minimum>=drain.location.z-.00003,(prefix,minimum,drain.location.z)
        report['construction'][prefix+'_drain_grade']=dict(actual_minimum_floor_Z_m=minimum,actual_drain_socket_Z_m=drain.location.z,minimum_floor_above_drain_m=minimum-drain.location.z)
    # An actual mouth point and its nearest submerged section station define
    # the slicing plane. Fit exported vertices in that plane, independently of
    # the authored analytic radius and without using a declared circle center.
    for family,prefix,shallow_sector in [('kidney','Bowl_Sector_',8),('clover','SteelBowl_Sector_',6)]:
        for label,k,height in [('deep',0,2.1336),('shallow',shallow_sector,1.2192)]:
            rt=lib[prefix+'%02d'%k]
            mouth=next(o for o in rt.children_recursive if o.get('socket_kind')=='bowl_sector' and o.name.split('__')[-1]=='Seam_A').location.copy()
            v=material_vertices(rt,'Concrete');below=[p for p in v if p.z<-.01]
            near=min(below,key=lambda p:(p-mouth).length)
            radial=Vector((mouth.x-near.x,mouth.y-near.y,0)).normalized();tangent=Vector((-radial.y,radial.x,0))
            pts=[((p-mouth).dot(radial),p.z) for p in v if p.z<-.0001 and abs((p-mouth).dot(tangent))<1e-5]
            data=circle(pts);assert abs(data['radius_m']-2.4384)<3e-5,data
            measured=-min(p[1] for p in pts);assert abs(measured-height)<2e-5,(family,label,measured)
            data['measured_depth_m']=measured;data['actual_mouth_m']=list(mouth);report['construction'][family+'_'+label]=data
    rt=lib['Bank_3ft'];ob=next(o for o in rt.children_recursive if o.type=='MESH');slopes=[]
    for f in ob.data.polygons:
        if .8<f.normal.z<.99 and abs(f.normal.x)<.01:
            slopes.append(math.degrees(math.acos(f.normal.z)))
    assert any(abs(s-20)<.05 for s in slopes),slopes;report['construction']['bank_measured_degrees']=max(slopes)
    # Rail contact is checked on imported triangle surfaces, independent of
    # copied source heights: paired rays measure the real rail centerline.
    rt=lib['Stairs_5'];tree=bvh([rt],material='Steel');samples=[]
    dots=[]
    for ob in rt.children_recursive:
        if ob.type!='MESH':continue
        for face in ob.data.polygons:
            if face.area>.025 and 'Steel' in ob.data.materials[face.material_index].name:
                dots += [face.normal.dot(ob.data.corner_normals[li].vector) for li in face.loop_indices]
    assert dots and min(dots)>.999,('Armor normal transformed into wrong frame',dots)
    report['construction']['hubba_armor_minimum_normal_dot']=min(dots)
    for y in (-.45,.35):
        hi=tree.ray_cast(Vector((0,y,3)),Vector((0,0,-1)))[0];lo=tree.ray_cast(Vector((0,y,-1)),Vector((0,0,1)))[0]
        assert hi is not None and lo is not None;samples.append((y,(hi.z+lo.z)/2))
    ypost=-.762+.12;slope=(samples[1][1]-samples[0][1])/(samples[1][0]-samples[0][0]);railcenter=samples[0][1]+slope*(ypost-samples[0][0])
    ob=next(o for o in rt.children_recursive if o.type=='MESH');tops=[]
    for f in ob.data.polygons:
        p=f.center
        if abs(p.x)<.025 and abs(p.y-ypost)<.025 and f.normal.z>.99 and p.z>.5:tops.append(p.z)
    assert tops,'No post end cap';posttop=max(tops);error=abs(railcenter-posttop);assert error<.001,(railcenter,posttop,error)
    report['construction']['front_stair_post']=dict(ray_measured_rail_center_m=railcenter,post_top_m=posttop,center_contact_error_m=error)
    # The actual toe plate is three millimeters; inspect the independent mesh.
    zinc=material_vertices(lib['Prefab_Quarter'],'Zinc');front=min(p.y for p in zinc);zs=[p.z for p in zinc if abs(p.y-front)<1e-5]
    report['construction']['prefab_toe_plate_gauge_m']=max(zs)-min(zs);assert abs(max(zs)-min(zs)-.003)<2e-5,(min(zs),max(zs),sorted(set(round(z,6) for z in zs)))
    for seed in SEEDS:
        path=folder/('Park_'+str(seed)+'.gltf');roots=imported(path.with_suffix('.glb'));expected=source['parks'][str(seed)];n=sum(count(r) for r in roots.values());assert n==expected['whole_site_triangles'],(seed,n,expected['whole_site_triangles'])
        assert 40000<=expected['skating_triangles']<=120000,(seed,expected['skating_triangles'])
        doc=json.loads(path.read_text());uris=[im['uri'] for im in doc.get('images',[])];assert all(u.startswith('shared/') for u in uris)
        imagebytes={u:hashlib.sha256((path.parent/u).read_bytes()).hexdigest() for u in uris}
        maximum=0;degenerate=0
        for ob in bpy.context.scene.objects:
            if ob.type!='MESH':continue
            ob.data.calc_loop_triangles()
            degenerate+=sum(t.area<1e-12 for t in ob.data.loop_triangles)
            for cn in ob.data.corner_normals:maximum=max(maximum,abs(cn.vector.length-1))
        assert maximum<.002,maximum
        # Honest exposed skins may contain tiny triangulation slivers at tile
        # ends; wholly zero-area triangles are always a construction failure.
        assert degenerate==0,(seed,degenerate)
        checks={}
        # Inspect actual fabric planes and post-bottom rings in world space.
        # Quaternion-mode imports previously ignored Euler placement yaw,
        # leaving crosswise panels and unsupported fabric at the corners.
        fence=roots['PerimeterFence'];post_centers=[];panels=[]
        for rt in fence.children:
            if rt.name.startswith(('Chain post','Chain side post')):
                points=[rt.matrix_world@v for v in material_vertices(rt,'Zinc')]
                bottom=min(v.z for v in points);ring=[v for v in points if v.z<bottom+.0001]
                post_centers.append([(min(v[k] for v in ring)+max(v[k] for v in ring))/2 for k in (0,1)])
            elif rt.name.startswith('Chain side'):
                panels.append([rt.matrix_world@v for v in material_vertices(rt,'ChainLink')])
        endpoint_error=0
        for points in panels:
            xmin,xmax=min(v.x for v in points),max(v.x for v in points)
            ymin,ymax=min(v.y for v in points),max(v.y for v in points)
            assert xmax-xmin<.0001 and abs(ymax-ymin-3.048)<.0001,('Crosswise side fabric',seed,xmax-xmin,ymax-ymin)
            for y in (ymin,ymax):
                error=min(math.hypot((xmin+xmax)/2-.034-x,y-py) for x,py in post_centers)
                endpoint_error=max(endpoint_error,error)
        assert len(panels)>=20 and endpoint_error<.001,(seed,len(panels),endpoint_error)
        checks['side_fence_surface_check']=dict(panels=len(panels),maximum_post_endpoint_error_m=endpoint_error)
        if seed in (101,202):
            tree=bvh(list(roots.values()));stair=next(m for m in expected['plan']['placements'] if m['piece'].startswith('Stairs'))
            x,y,_=stair['location'];nstep=5 if seed==101 else 4;toe=-nstep*.3048/2
            probes=[]
            for px,py,z in ((x+.45,y+toe-.3,0),(x+2.5,y+nstep*.3048/2+1.4,expected['plan']['plaza']['height'])):
                hit=tree.ray_cast(Vector((px,py,z+.10)),Vector((0,0,-1)))[0]
                assert hit is not None and abs(hit.z-z)<.0001,('Missing stair approach paving',seed,px,py,hit)
                probes.append(list(hit))
            checks['actual_stair_approach_floor_hits_m']=probes
            bx,by,_=expected['plan']['bowl']['location'];corners=[]
            for sx in (-1,1):
                for sy in (-1,1):
                    px=bx+sx*(9.144-.01);py=by+sy*(7.3152-.01)
                    hit=tree.ray_cast(Vector((px,py,.04)),Vector((0,0,-1)),.1)[0]
                    assert hit is not None and abs(hit.z)<.0001,('Open bowl deck corner',seed,px,py,hit)
                    corners.append(list(hit))
            checks['actual_bowl_deck_corner_floor_hits_m']=corners
        if seed==303:
            tree=bvh(list(roots.values()));maxheight=-1
            for x in (-14.6304,14.6304):
                for y in np.linspace(-3.85,3.85,41):
                    hit=tree.ray_cast(Vector((x,float(y),.25)),Vector((0,0,-1)))[0];assert hit is not None
                    maxheight=max(maxheight,hit.z)
            assert maxheight<.006,maxheight;checks['mini_ramp_flat_max_height_m']=maxheight
        report['parks'][str(seed)]=dict(imported_triangles=n,skating_triangles=expected['skating_triangles'],materials=len(doc['materials']),material_primitives=sum(len(m['primitives']) for m in doc['meshes']),max_normal_length_error=maximum,degenerate_triangles=degenerate,images=imagebytes,**checks)
    for seed in range(1000):
        p=plan(seed);assert p==plan(seed);assert all(math.isfinite(v) for m in p['placements'] for v in m['location']);assert p['type'] in ('poured','prefab')
    report['deterministic_plans']=1000
    # A family-local checkpoint must leave all other tracked deliveries/scripts
    # byte-identical, and cannot certify final repo-wide product readiness.
    changed=subprocess.check_output(['git','diff','--name-only','HEAD','--','.'],cwd=HERE.parents[1],text=True).splitlines();assert all(p.startswith('skatepark/') for p in changed),changed
    report['preserved_other_tracked_files']=True;report['passed']=True
    Path('build/checks.json').write_text(json.dumps(report,indent=2));print('CHECKPOINT CHECK PASS',json.dumps({s:{k:v for k,v in d.items() if k!='images'} for s,d in report['parks'].items()}))

if __name__=='__main__':main()
