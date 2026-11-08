"""Measured construction and fresh-import delivery checks, kept distinct."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT),str(ROOT/'cars/src')]
from kit import uv
from kit.gltf import GLB
from sedan_front_check import measure
import spec as S

def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]
def bounds(obs):
    ps=[p for ob in obs for p in points(ob)];lo=np.min(ps,axis=0);hi=np.max(ps,axis=0)
    return dict(min=lo.tolist(),max=hi.tolist(),size=(hi-lo).tolist())
def section_y(ob,z):
    """Actual polygon-edge intersections with a horizontal seat measurement plane."""
    ps=points(ob);values=[]
    for edge in ob.data.edges:
        a,b=[ps[i] for i in edge.vertices]
        if abs(a.z-b.z)<1e-8:
            if abs(a.z-z)<1e-6:values.extend([a.y,b.y])
        elif min(a.z,b.z)-1e-7<=z<=max(a.z,b.z)+1e-7:
            values.append(a.y+(b.y-a.y)*(z-a.z)/(b.z-a.z))
    return [min(values),max(values)] if values else None
def landing_check(obs,steps):
    """Vertical probes across the upper landing, measured against actual floor."""
    vs=[];fs=[]
    for ob in obs:
        ob.data.calc_loop_triangles();offset=len(vs);vs.extend(points(ob))
        fs.extend(tuple(offset+i for i in tri.vertices) for tri in ob.data.loop_triangles)
    tree=BVHTree.FromPolygons(vs,fs,all_triangles=True)
    def hit(x,y):
        p=tree.ray_cast(Vector((x,y,1.25)),Vector((0,0,-1)),.4)[0]
        return p.z if p is not None else None
    reference=hit(0,-3.345);rows=[dict(x_m=x,y_m=y,hit_z_m=hit(x,y)) for x in [-.39,-.36,-.33,-.30] for y in [-3.60,-3.345,-3.10]]
    treads=[]
    for name,b in steps.items():
        cx=(b['min'][0]+b['max'][0])/2;expected=b['max'][2]
        for dx in [-.08,0,.08]:
            for y in [-3.60,-3.345,-3.10]:
                p=tree.ray_cast(Vector((cx+dx,y,expected+.03)),Vector((0,0,-1)),.06)[0]
                treads.append(dict(tread=name,x_m=cx+dx,y_m=y,measured_tread_top_m=expected,first_surface_z_m=p.z if p is not None else None))
    passed=reference is not None and all(r['hit_z_m'] is not None and abs(r['hit_z_m']-reference)<.002 for r in rows)
    passed &= all(r['first_surface_z_m'] is not None and abs(r['first_surface_z_m']-r['measured_tread_top_m'])<.002 for r in treads)
    return dict(passed=passed,reference_floor_z_m=reference,probes=rows,tread_probes=treads,method='Actual mesh union, vertical rays below dash/ceiling; landing continuity against actual floor and tread faces unobstructed by chassis, using measured part surfaces')
def hash_inputs():
    # Existing deliveries are immutable inputs. If absent, record absence instead of rebuilding cars.
    files=list((ROOT/'cars').rglob('*.glb'))+list((ROOT/'school/export').rglob('*'))
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file()}

def model(path):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));bpy.context.view_layer.update();sc=bpy.context.scene
    obs=[o for o in sc.objects if o.type=='MESH' and o.get('asset_set') and o.get('variant_id',101)==101]
    cats={};parts={};pivots={}
    for ob in obs:
        ob.data.calc_loop_triangles();n=len(ob.data.loop_triangles);parts[ob.name]=n;c=ob['part_category'];cats[c]=cats.get(c,0)+n
    for ob in sc.objects:
        if ob.get('pivot_axis'):pivots[ob.name]=dict(position=list(ob.matrix_world.translation),axis=ob['pivot_axis'],range=list(ob['range_degrees']))
    wb=abs(pivots['Wheel_FL']['position'][1]-pivots['Wheel_RL_outer']['position'][1]);tires={o.name:bounds([o]) for o in obs if o.name.startswith('Tire_')}
    crossing=bpy.data.objects['Crossing_arm'];hinge=crossing.matrix_world.translation
    deployed=Matrix.Translation(hinge)@Matrix.Rotation(math.radians(-90),4,'Z')@Matrix.Translation(-hinge)
    deployed_points=[deployed@p for ob in crossing.children_recursive if ob.type=='MESH' for p in points(ob)]
    crossing_extension=S.FRONT-min(p.y for p in deployed_points)
    steps={o.name:bounds([o]) for o in obs if o.name.startswith('Worn entrance tread')}
    roof=bounds([bpy.data.objects['Formed roof steel']]);shell=bounds([bpy.data.objects[n] for n in ['Formed roof steel','Front pressed bumper','Rear pressed bumper']])
    # Geometry checks use actual padded mesh bounds and actual pivot positions.
    benchbacks=[o for o in obs if o.name.startswith('Bench_') and o.name.endswith('padded back')]
    sockets=[o.name for o in sc.objects if o.get('socket_kind')]
    cushions=[o for o in obs if o.name.startswith('Bench_') and o.name.endswith('cushion')]
    seatwidths=[bounds([o])['size'][0] for o in cushions]
    capacity=sum(math.floor(w/.381+.5) for w in seatwidths)
    left=[bounds([o]) for o in cushions if o.matrix_world.translation.x>0 or sum(p.x for p in points(o))>0]
    right=[bounds([o]) for o in cushions if sum(p.x for p in points(o))<0]
    aisle=min(r['min'][0] for r in left)-max(r['max'][0] for r in right)
    spacing=[]
    for side in ['L','R']:
        backs=sorted([o for o in benchbacks if '_'+side+' padded' in o.name],key=lambda o:bounds([o])['min'][1])
        for i,back in enumerate(backs):
            ahead=backs[i-1] if i else bpy.data.objects.get('Front passenger barrier') if side=='R' else None
            if ahead is None:continue
            stations=sorted({p.z for o in [back,ahead] for p in points(o) if 1.654<=p.z<=2.335})
            stations+=list(np.linspace(1.654,2.334,35));samples=[]
            for z in stations:
                current,previous=section_y(back,z),section_y(ahead,z)
                if current and previous:samples.append(dict(z_m=float(z),gap_m=current[0]-previous[1]))
            spacing.append(dict(parts=[ahead.name,back.name],minimum_clear_m=min(s['gap_m'] for s in samples),samples=samples))
    from PIL import Image
    glyphs={}
    for image_name,object_name,mask in [('school','Front school legend','black'),('stop','Stop legend 1','white')]:
        pixels=np.asarray(Image.open(path.parent/'markings'/f'{image_name}.png'))
        active=pixels.max(2)<80 if mask=='black' else pixels.min(2)>170
        ys=np.where(active)[0];fraction=(ys.max()-ys.min()+1)/pixels.shape[0]
        glyphs[image_name]=float(bounds([bpy.data.objects[object_name]])['size'][2]*fraction)
    from kit.assembly import distance
    pairs=[]
    for ob in obs:
        if 'foot plate' in ob.name:pairs.append((ob.name,'Passenger floor',.0005))
        if ob.name.startswith('Ceiling dome'):pairs.append((ob.name,'Ceiling formed liner',.002))
        if ob.name.startswith(('Crossview primary foot','Crossview brace foot')):pairs.append((ob.name,'Compound hood shell',.002))
        if ob.name.startswith('Exhaust hanger'):pairs.append((ob.name,'Exhaust tailpipe',.001))
        if ob.name.startswith('Body floor bearer'):
            driver=ob.name.endswith('-3.4')
            pairs.append((ob.name,'Driver floor' if driver else 'Passenger floor',.0005))
            for sign in ([1] if driver else [-1,1]):pairs.append((ob.name,'Chassis C rail '+str(sign),.0005))
        if ob.name.startswith('Entrance ') and ' fixed foot ' in ob.name:
            side=ob.name.split()[1];base=ob.name.split(' fixed foot ')[0]
            pairs += [(ob.name,base+' fixed pin',.0005),(ob.name,'Entrance '+side+' fixed jamb',.0005)]
    pairs += [('Driver suspension pedestal','Driver floor',.0005),('Grab rail barrier flange','Front passenger barrier',.0005),('Entrance grab rail','Grab rail barrier flange',.0005),('Entrance grab rail','Worn entrance tread 0',.0005)]
    for x in [-1.04,-.34]:
        post='Barrier support '+str(x)
        pairs.extend([(post,'Barrier foot plate '+str(x),.001),(post,'Front passenger barrier',.001),
                      (post,'Entrance modesty lower panel',.001)])
    pairs += [('Passenger floor','Lower folded side -1 1',.001),('Passenger floor','Lower folded side 1 0 -3.92',.001),('Driver floor','Driver lower side',.001),
        ('Side emergency aft backed reveal','Body post 1 5',.001),('Front cap under-header','Front roof cap',.001),('Front cap under-header','Windshield header closure',.001)]
    pairs += [('Side emergency forward backed reveal','Lower folded side 1 0 -3.92',.001),('Side exit fixed underfloor skirt','Passenger floor',.001)]
    for side in ['front','rear']:
        pairs += [('Entrance '+side+' fixed jamb','Stepwell '+side+' wall',.001),('Stepwell '+side+' wall','Worn entrance tread 0',.001)]
        pairs += [('Stepwell '+side+' wall','Entrance top landing',.001),('Stepwell '+side+' wall','Driver floor',.001)]
    pairs += [('Entrance top landing','Driver floor',.001),('Entrance landing riser','Entrance top landing',.001),('Entrance landing riser','Worn entrance tread 3',.001)]
    for sign in [-1,1]:
        for end in ['Front','Rear']:
            bracket=end+' bumper frame bracket '+str(sign)
            pairs.extend([(bracket,end+' pressed bumper',.001),(bracket,'Chassis C rail '+str(sign),.001)])
    contacts=[]
    for a,b,limit in pairs:
        value,method=distance(bpy.data.objects[a],bpy.data.objects[b]);contacts.append(dict(parts=[a,b],distance_m=value,method=method,limit_m=limit))
    error=[];total=sum(cats.values());exterior=total-cats['interior']
    source_audits={ob.name:measure(ob) for ob in obs}
    failed_meshes=[name for name,row in source_audits.items() if not row['passed']]
    landing=landing_check(obs,steps)
    if not landing['passed']:error.append('Entrance landing continuity')
    if failed_meshes:error.append('Source full-face mesh check')
    if total>90000 or exterior>70000:error.append('Triangle budget')
    if abs(wb-S.WHEELBASE)>1e-5:error.append('Wheelbase')
    if abs(shell['size'][1]-S.LENGTH)>.002 or abs(roof['size'][0]-S.WIDTH)>.002:error.append('Bumper length / steel body width')
    if len(benchbacks)!=25:error.append('75-place bench layout')
    if capacity!=75 or aisle<.3048:error.append('Bench occupancy / aisle width')
    if min(r['minimum_clear_m'] for r in spacing)<.6096:error.append('24-inch actual seat/barrier spacing')
    if glyphs['school']<.2032 or glyphs['stop']<.150:error.append('Standard legend glyph height')
    if crossing_extension<1.778:error.append('70-inch deployed crossing gate extension')
    if any(row['distance_m']>row['limit_m'] for row in contacts):error.append('Measured static support')
    if any(abs(t['min'][2])>1e-5 for t in tires.values()):error.append('Tire ground contact')
    if abs(roof['max'][2]-S.HEIGHT)>.002:error.append('Roof height')
    if max(v['max'][2] for v in steps.values())>1.19:error.append('Step envelope')
    return dict(passed=not error,errors=error,triangles=total,exterior_triangles=exterior,interior_triangles=cats['interior'],wheels_triangles=cats['wheels'],
        mesh_audits=source_audits,failed_meshes=failed_meshes,
        entrance_landing=landing,
        categories=cats,triangles_per_mesh=parts,triangles_per_pivot={n:sum(parts.get(o.name,0) for o in bpy.data.objects[n].children_recursive) for n in pivots},
        roof_bounds_m=roof,body_bumper_bounds_m=shell,full_rest_bounds_m=bounds(obs),wheelbase_m=wb,tire_bounds_m=tires,step_bounds_m=steps,
        measured_deployed_crossing_extension_m=crossing_extension,
        measured_bench_widths_m=seatwidths,measured_passenger_capacity=capacity,measured_clear_aisle_m=aisle,measured_glyph_heights_m=glyphs,static_support_contacts=contacts,
        measured_seat_spacing=spacing,
        bench_count=len(benchbacks),passenger_socket_count=sum('_Place' in n for n in sockets),sockets=sockets,pivots=pivots,
        scope='Measured source construction and allocation. Does not prove export serialization or collision clearance.')

def delivery(path,parts_path):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH'];count=0;rows={}
    for ob in obs:ob.data.calc_loop_triangles();count+=len(ob.data.loop_triangles);rows[ob.name]=measure(ob)
    meshes={o.name:o for o in obs};materials={m.name for o in obs for m in o.data.materials}
    seen={};duplicates=[]
    for ob in obs:
        for tri in ob.data.loop_triangles:
            key=tuple(sorted(tuple(round(c,7) for c in ob.matrix_world@ob.data.vertices[i].co) for i in tri.vertices))
            if key in seen and seen[key]!=ob.name:duplicates.append([seen[key],ob.name,tri.index])
            seen[key]=ob.name
    uvr=uv.report(obs,2048,layer='UVMap');uvsummary={k:v for k,v in uvr.items() if k!='island_measurements'}
    d=json.loads(path.read_text());images={im['uri']:dict(bytes=(path.parent/im['uri']).stat().st_size,sha256=hashlib.sha256((path.parent/im['uri']).read_bytes()).hexdigest()) for im in d['images']}
    from PIL import Image
    for uri,row in images.items():row['size']=list(Image.open(path.parent/uri).size)
    export_pivots={o.name:list(o.matrix_world.translation) for o in bpy.context.scene.objects if o.get('pivot_axis')}
    sockets=[o.name for o in bpy.context.scene.objects if o.get('socket_kind')]
    body_bounds=bounds(obs);failed=[name for name,row in rows.items() if not row['passed']]
    report=dict(triangles=count,materials=sorted(materials),images=images,external_mesh_bytes=sum((path.parent/b['uri']).stat().st_size for b in d['buffers']),gltf_bytes=path.stat().st_size,
        imported_bounds_m=body_bounds,mesh_audits=rows,failed_meshes=failed,uv=uvsummary,pivots=export_pivots,sockets=sockets,
        scope='Fresh external glTF import, car-family full-face mesh audit and actual UV layout. Re-import proves serialization, not mechanics.')
    expected=json.loads((path.parent.parent/'build'/('export-'+path.stem.split('-')[-1]+'.json')).read_text())
    from mathutils.kdtree import KDTree
    differences=[]
    for name,record in expected['meshes'].items():
        ob=meshes[name];actual=points(ob);old=[Vector(p) for p in record['vertices_world']]
        for aa,bb in [(actual,old),(old,actual)]:
            tree=KDTree(len(bb))
            for i,point in enumerate(bb):tree.insert(point,i)
            tree.balance();differences.extend(tree.find(point)[2] for point in aa)
    pivot_errors={}
    for name,matrix in expected['nodes'].items():
        ob=bpy.data.objects.get(name)
        if ob is None:raise ValueError('Missing exported node '+name)
        expected_position=Vector([row[3] for row in matrix[:3]])
        pivot_errors[name]=(ob.matrix_world.translation-expected_position).length
    report['serialization']=dict(bidirectional_vertex_samples=len(differences),maximum_vertex_distance_m=max(differences),maximum_pivot_distance_m=max(pivot_errors.values()))
    report['duplicate_faces_across_parts']=len(duplicates)
    step_bounds=json.loads((path.parent.parent/'build/model-check.json').read_text())['step_bounds_m']
    report['entrance_landing']=landing_check(obs,step_bounds)
    errors=[]
    if count>90000:errors.append('Triangle budget')
    if len(materials)>4 or len(images)!=3:errors.append('Resource budget')
    if failed:errors.append('Car-family full-face mesh check')
    if duplicates:errors.append('Duplicate faces across parts')
    if not report['entrance_landing']['passed']:errors.append('Entrance landing continuity')
    if uvr['outside_triangles'] or uvr['degenerate_uv_triangles'] or uvr['overlap_fraction']>1e-5:errors.append('UV layout')
    import runpy
    policy=runpy.run_path(str(HERE/'config.py'));density={str(k):v for k,v in uvr['density_px_m'].items()};bands=policy['UV_DENSITY_BANDS']
    if uvr['coverage']<policy['UV_MIN_COVERAGE'] or density['5']<bands['p5_min'] or not bands['median_min']<=density['50']<=bands['median_max'] or density['95']>bands['p95_max']:errors.append('Measured UV coverage / density bands')
    if len(sockets)<100:errors.append('Missing sockets')
    if max(differences)>2e-5 or max(pivot_errors.values())>2e-5:errors.append('Geometry/pivot serialization')
    report['errors']=errors;report['passed']=not errors;return report

def main():
    p=argparse.ArgumentParser();p.add_argument('--model');p.add_argument('--gltf');p.add_argument('--parts');p.add_argument('--out',required=True);p.add_argument('--diagnose',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    r=model(Path(a.model)) if a.model else delivery(Path(a.gltf),a.parts);Path(a.out).write_text(json.dumps(r,indent=2));print('BUS_CHECK',r['passed'],r.get('triangles'),r.get('errors'),r.get('failed_meshes'),flush=True)
    if not r['passed'] and not a.diagnose:raise SystemExit(1)
if __name__=='__main__':main()
