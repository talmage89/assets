"""Independent fresh-import construction audit, separate from source statistics.

Checks actual surface positions, marking widths and pitches, deck/bearing
contacts, driving paths and counts. This gate does not certify final UV/bakes,
structural capacity, crashworthiness or a traffic simulation.
"""
import sys,json,math,hashlib
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from external import bundle
from plan import plan,path_curvature

def import_file(path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()));bpy.context.view_layer.update()

def meshes(root):return [o for o in [root,*root.children_recursive] if o.type=='MESH']
def tri(root):return sum(sum(len(p.vertices)-2 for p in ob.data.polygons) for ob in meshes(root))

def vertices(obs,material=None):
    pts=[]
    for ob in obs:
        if ob.type!='MESH':continue
        ids=set()
        for f in ob.data.polygons:
            ma=ob.data.materials[f.material_index]
            if material is None or ma.name.split('.')[0] in material:
                ids.update(f.vertices)
        pts.extend(ob.matrix_world@ob.data.vertices[i].co for i in ids)
    return pts

def bvh(obs,material=None):
    vs=[];fs=[]
    for ob in obs:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();offset=len(vs);vs.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        for f in ob.data.loop_triangles:
            ma=ob.data.materials[f.material_index]
            if material is None or ma.name.split('.')[0] in material:fs.append(tuple(offset+i for i in f.vertices))
    return BVHTree.FromPolygons(vs,fs,all_triangles=True)

def ray(tree,x,y,z=100):
    hit=tree.ray_cast(Vector((x,y,z)),Vector((0,0,-1)),200)
    assert hit[0] is not None,('Missing support surface',x,y)
    return hit[0]

def base_checks():
    bad=[];normal_error=0;uv_degenerate=0;world_area_degenerate=0;triangles=0
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        assert all(math.isfinite(v) for vert in ob.data.vertices for v in vert.co)
        assert max(abs(v-1) for v in ob.scale)<1e-5,(ob.name,ob.scale)
        ob.data.calc_loop_triangles();triangles+=len(ob.data.loop_triangles)
        if ob.name.startswith(('SUV__','Hatch__')):
            for f in ob.data.loop_triangles:
                assert all(ob.data.corner_normals[i].vector.dot(f.normal)>-.01 for i in f.loops),('Opposed context car normals',ob.name)
        if ob.get('context_surface_kind'):
            expected=Vector(ob['context_expected_local_normal'])
            for f in ob.data.loop_triangles:
                a,b,c=[ob.data.vertices[v].co for v in f.vertices]
                n=(b-a).cross(c-a).normalized()
                assert n.dot(expected)>.999,('Reversed native context skin',ob.name)
                if ob['context_surface_kind']=='roof':assert n.z>.05
        for f in ob.data.loop_triangles:
            if f.area<1e-12:world_area_degenerate+=1
            if ob.name.startswith('Cut slopes and drainage'):
                a,b,c=[ob.matrix_world@ob.data.vertices[v].co for v in f.vertices]
                assert (b-a).cross(c-a).z>0,('Folded earthwork surface',ob.name,f.index)
        if ob.data.uv_layers:
            uv=ob.data.uv_layers.active
            for f in ob.data.loop_triangles:
                a,b,c=[uv.data[i].uv for i in f.loops]
                if abs((b-a).cross(c-a))<1e-14:uv_degenerate+=1
        else:bad.append(ob.name)
        if ob.data.corner_normals:
            normal_error=max(normal_error,max(abs(n.vector.length-1) for n in ob.data.corner_normals))
    assert not bad,('Missing UV channels',bad)
    assert world_area_degenerate==0,('Collapsed physical triangles',world_area_degenerate)
    assert normal_error<.002,normal_error
    return dict(triangles=triangles,normal_length_max_error=normal_error,degenerate_triangles=world_area_degenerate,degenerate_uv_triangles=uv_degenerate,uv_scope='Authored repeating terrain charts and quick constants; atlas overlap/density certification belongs to look-dev')

def modules():
    report={}
    for path in sorted(Path('export/modules').glob('*.gltf')):
        import_file(path);stats=base_checks();n=path.stem
        limit=50000 if n=='Overpass' else 8000 if n in ('SignTruss','Cantilever') else 2000
        assert stats['triangles']<=limit,(n,stats['triangles'])
        pts=vertices(bpy.context.scene.objects);stats['bounds']=[[float(op(p[k] for p in pts)) for k in range(3)] for op in (min,max)]
        stats['gltf_bytes']=path.stat().st_size;stats['bin_bytes']=path.with_suffix('.bin').stat().st_size
        stats['bundle_sha256']=bundle(path);report[n]=stats
        if n in ('MedianF','WBeam','GuardrailEnd','CableBay','PierBent','PrestressedGirder24'):
            volume=0.
            for ob in bpy.context.scene.objects:
                if ob.type!='MESH':continue
                ob.data.calc_loop_triangles()
                for f in ob.data.loop_triangles:
                    a,b,c=[ob.matrix_world@ob.data.vertices[v].co for v in f.vertices]
                    volume+=a.dot(b.cross(c))/6
            stats['signed_closed_component_volume_m3']=volume
            assert volume>0,('Inward manufactured sections',n,volume)
        if n=='MedianF':
            assert abs(stats['bounds'][1][2]-.8128)<1e-5
            tree=bvh(bpy.context.scene.objects)
            # Rays through the slot and adjacent solid prove an actual opening.
            assert tree.ray_cast(Vector((-1,0,.04)),Vector((1,0,0)),2)[0] is None
            assert tree.ray_cast(Vector((-1,.30,.04)),Vector((1,0,0)),2)[0] is not None
        if n=='WBeam':
            steel=vertices(bpy.context.scene.objects,{'Freeway_Form_Steel'})
            stats['measured_rail_top_m']=max(v.z for v in steel)
            assert abs(stats['measured_rail_top_m']-.7874)<1e-5
        if n=='Overpass':
            rubber=bvh(bpy.context.scene.objects,{'Freeway_Form_Rubber'})
            concrete=bvh(bpy.context.scene.objects,{'Freeway_Form_Bridge'})
            samples=[]
            for x in (-23.6,-.65,.65,23.6):
                for y in (-9.144,-6.096,-3.048,0,3.048,6.096,9.144):
                    padtop=ray(rubber,x,y,6.)
                    # Separate BVHs: cast downward from inside the lower flange
                    # to its underside, then compare with actual pad top.
                    hit=concrete.ray_cast(Vector((x,y,6.0)),Vector((0,0,-1)),1)[0]
                    assert hit is not None,('Unsupported girder',x,y)
                    samples.append(float(hit.z-padtop.z))
            stats['bearing_top_to_girder_gap_m']=dict(min=min(samples),max=max(samples),samples=len(samples))
            assert max(abs(v) for v in samples)<.00002
            all_surfaces=bvh(bpy.context.scene.objects)
            origin=Vector((0,9.5,7.22))
            inner=all_surfaces.ray_cast(origin,Vector((0,-1,0)),3)[0]
            outer=all_surfaces.ray_cast(origin,Vector((0,1,0)),3)[0]
            assert inner is not None and outer is not None
            stats['measured_walk_clear_width_m']=outer.y-inner.y
            assert abs(stats['measured_walk_clear_width_m']-1.524)<2e-5
    return report

def scene(seed):
    path=Path('export/Freeway-'+str(seed)+'.gltf');import_file(path);stats=base_checks();p=plan(seed)
    assert stats['triangles']<400000,stats['triangles']
    roads=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent and o.parent.get('module_kind')=='roadway']
    roadtree=bvh(roads,{'Asphalt','Concrete'})
    # Surface-derived section: actual ray hits, no metadata used as a result.
    x0,y0,_=p.xyz(0,6);x1,y1,_=p.xyz(0,9)
    z0=ray(roadtree,x0,y0)[2];z1=ray(roadtree,x1,y1)[2]
    cross=(z1-z0)/3;stats['measured_cross_slope']=cross
    assert abs(cross-(-.02 if seed==101 else -.04))<2e-5,cross
    # The central module has no speed-change lane. Measure actual painted
    # edges in its exported vertex positions, then infer clear lane centerlines.
    central=min(roads,key=lambda ob:abs(float(ob.parent.get('station_start',1e9))))
    def xs(role):return sorted(set(round(float(v.x),5) for v in vertices([central],{role}) if v.x>0))
    if seed==101:
        yellow=xs('Freeway_Form_Yellow');white=xs('Freeway_Form_White')
        left=(min(yellow)+max(yellow))/2;right=(max(white)+max(white)-.1524)/2
        dash=sorted(v for v in white if left+1<v<right-1);middle=(dash[0]+dash[-1])/2
        skin=vertices([central],{'Asphalt','Concrete'});edge=max(v.x for v in skin);inner=min(v.x for v in skin if v.x>0)
        stats['measured_section_m']=dict(inner_lane=middle-left,outer_lane=right-middle,left_shoulder=left-inner,right_shoulder=edge-right,line_width=yellow[-1]-yellow[0])
        for value in (middle-left,right-middle):assert abs(value-3.6576)<3e-5,value
        assert abs(edge-right-3.048)<3e-5
        assert abs(left-inner-1.2192)<3e-5
        bridge=[]
        for ob in bpy.context.scene.objects:
            if ob.type!='MESH':continue
            ancestor=ob
            while ancestor.parent:ancestor=ancestor.parent
            if ancestor.get('module_kind')=='bridge':bridge.append(ob)
        solid=bvh(bridge,{'Freeway_Form_Bridge'})
        gaps=[]
        for x in (-9.,-6.,-3.,3.,6.,9.):
            # Upward ray at the actual middle girder web.
            a=ray(roadtree,x,0)
            hit=solid.ray_cast(a+Vector((0,0,.02)),Vector((0,0,1)),20)[0]
            assert hit is not None
            gaps.append(float(hit.z-a.z))
        stats['measured_bridge_clearance_m']=dict(min=min(gaps),max=max(gaps),samples=len(gaps))
        assert min(gaps)>5.18
        earth=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Cut slopes and drainage')]
        paving=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Five lane arterial and approaches')]
        soil=bvh(earth)
        if not any(o for o in paving):raise AssertionError('Missing arterial pavement section')
        base=bvh(paving)
        support=[]
        for x in (-36.,-31.,31.,36.):
            for y in (-5.,5.):
                top=ray(soil,x,y,7.1)
                hit=base.ray_cast(Vector((x,y,7.0)),Vector((0,0,1)),1)[0]
                assert hit is not None
                support.append(float(hit.z-top.z))
        assert max(abs(v) for v in support)<.00002,('Unsupported arterial approach',support)
        stats['approach_base_to_soil_gap_m']=dict(min=min(support),max=max(support),samples=len(support))
    soil=bvh([o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Cut slopes and drainage')])
    burial=[]
    for truss in [o for o in bpy.context.scene.objects if o.get('module_kind')=='sign_structure']:
        concrete=bvh(truss.children_recursive,{'Freeway_Form_Bridge'})
        for x in (-17.,17.):
            point=truss.matrix_world@Vector((x,0,0));surface=ray(soil,point.x,point.y)
            hit=concrete.ray_cast(surface-Vector((0,0,1)),Vector((0,0,1)),2)[0]
            assert hit is not None,('Missing sign foundation',truss.name,x)
            burial.append(float(surface.z-hit.z))
    assert len(burial)==(4 if seed==101 else 2)
    assert max(abs(v-.30) for v in burial)<.00002,('Floating sign foundations',burial)
    stats['sign_foundation_embedment_m']=dict(min=min(burial),max=max(burial),samples=len(burial))
    paths=[]
    for ob in bpy.context.scene.objects:
        if ob.get('socket_kind')!='drive_path':continue
        points=json.loads(ob['points_blender_json'])
        grade=max(abs(b[2]-a[2])/math.dist(a[:2],b[:2]) for a,b in zip(points,points[1:]))
        radius=path_curvature(points)
        paths.append(dict(name=ob.name,points=len(points),length_m=sum(math.dist(a,b) for a,b in zip(points,points[1:])),maximum_grade=grade,minimum_plan_radius_m=radius))
        if 'Ramp' in ob.name:assert grade<.05 and radius>100,(grade,radius)
    assert len(paths)==(8 if seed==101 else 4),len(paths)
    stats['driving_paths']=paths;stats['bundle_sha256']=bundle(path)
    contacts=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ('Tire_' in ob.name or 'Hatch__Wheel_' in ob.name):continue
        pts=[ob.matrix_world@v.co for v in ob.data.vertices]
        # Inspect the lower part of each actual delivered tire, not its hub
        # transform or a claimed nominal radius.
        low=min(p.z for p in pts);candidates=[p for p in pts if p.z<low+.09]
        gaps=[]
        for point in candidates:
            h=roadtree.ray_cast(Vector((point.x,point.y,30)),Vector((0,0,-1)),60)[0]
            if h is not None:gaps.append(float(point.z-h.z))
        if gaps:contacts.append(dict(wheel=ob.name,minimum_gap_m=min(gaps)))
    stats['traffic_wheel_surface_contacts']=contacts
    assert len(contacts)==24,len(contacts)
    assert min(r['minimum_gap_m'] for r in contacts)>-.03,contacts
    assert max(r['minimum_gap_m'] for r in contacts)<.04,contacts
    stats['gltf_bytes']=path.stat().st_size;stats['bin_bytes']=path.with_suffix('.bin').stat().st_size
    # Ordinary glTF material allocation deduplicated by actual image URI/hash.
    d=json.loads(path.read_text());image_rows=[]
    from PIL import Image
    for im in d.get('images',[]):
        q=(path.parent/im['uri']).resolve();assert q.is_file();assert not im['uri'].startswith(('data:','/','http'))
        with Image.open(q) as f:w,h=f.size
        image_rows.append(dict(uri=im['uri'],size=[w,h],bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest(),estimated_bc_mips_mib=w*h*4/3/2**20))
    unique={r['sha256']:r for r in image_rows}
    stats['images']=image_rows;stats['materials']=len(d.get('materials',[]));stats['unique_images']=len(unique)
    stats['compressed_images_mib']=sum(r['estimated_bc_mips_mib'] for r in unique.values())
    return stats

def main():
    rows=modules();scenes={str(seed):scene(seed) for seed in (101,202)}
    previous=Path('build/existing-deliveries.json')
    if previous.exists():
        for path,h in json.loads(previous.read_text()).items():
            q=HERE.parents[1]/path
            assert hashlib.sha256(q.read_bytes()).hexdigest()==h,('Existing delivery changed',path)
    report=dict(stage='Form/construction checkpoint; quick materials, no final bake certification',modules=rows,scenes=scenes,existing_delivery_hashes_checked=len(json.loads(previous.read_text())) if previous.exists() else 0)
    Path('build/check.json').write_text(json.dumps(report,indent=2));print('CHECK PASSED',[(k,v['triangles']) for k,v in scenes.items()])
if __name__=='__main__':main()
