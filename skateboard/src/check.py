"""Independent mesh measurements, actual-surface clearance and fresh GLB import.
No UV/bake certification is made by this explicitly form-only check.
"""
import argparse,json,math,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import bpy,bmesh
from mathutils import Vector,Matrix
from kit.motion import surface,sweep,penetration
from kit.assembly import distance
from kit.gltf import GLB
from spec import spec,halfwidth
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(src));root=bpy.data.objects['Skateboard'];s=spec(int(root['seed']),root['age_state']);errors=[];proof={}
def require(ok,msg):
    if not ok:errors.append(msg)
def meshpoints(o):return [o.matrix_world@v.co for v in o.data.vertices]
def bounds(pts):
    lo=[min(v[k] for v in pts) for k in range(3)];hi=[max(v[k] for v in pts) for k in range(3)];return dict(min=lo,max=hi,size=[b-a for a,b in zip(lo,hi)])
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Skateboard'];deck=next(o for o in meshes if o.get('part')=='deck');dp=meshpoints(deck);db=bounds(dp)
counts={};topology={}
for o in meshes:
    o.data.calc_loop_triangles();counts[o.get('part')]=counts.get(o.get('part'),0)+len(o.data.loop_triangles)
    bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);zero=sum(f.calc_area()<1e-13 for f in bm.faces)
    topology[o.name]=dict(boundary_or_nonmanifold=bad,zero_area_faces=zero);bm.free()
    # Thin bearing shields/insert annuli/speed rings are intentionally open,
    # seated faces; structural deck and all manufactured solid castings must close.
    if o.get('part') in ('deck','hangers','baseplates','wheels','delamination'):require(bad==0,o.name+' structural topology is open')
    require(zero==0,o.name+' degenerate faces')
dense_counts={}
for o in bpy.context.scene.objects:
    if o.type=='MESH' and o.get('source_only'):
        o.data.calc_loop_triangles();dense_counts[o.name]=len(o.data.loop_triangles)
proof['retained_source_geometry_triangles']=dense_counts;proof['triangles_per_part']=counts;proof['triangles']=sum(counts.values());require(6000<=proof['triangles']<=14000,'Whole board outside authorized 6k–14k budget')
proof['deck_bounds_m']=db;require(abs(db['size'][1]-s.length)<.0002,'Deck length drift');require(abs(db['size'][0]-s.width)<.001,'Deck width drift')
# Vertical rays measure the actual top/bottom surfaces at the stance center and rails.
ds=surface(deck)
def rayheight(x,y,down=True):
    hit=ds['tree'].ray_cast(Vector((x,y,1 if down else -1)),Vector((0,0,-1 if down else 1)),2)
    return hit[0].z if hit[0] is not None else None
center=rayheight(0,0);rail=rayheight(halfwidth(s,0)-s.thickness/2-.0007,0);bottom=rayheight(0,0,False)
proof['center_thickness_including_grip_m']=center-bottom;proof['measured_concave_near_rail_m']=rail-center
require(abs((center-bottom)-(s.thickness+.00055))<.0001,'Measured center thickness incorrect');require(.0068<rail-center<.0085,'Actual concave outside class')
# Eight through bores: a ray through the deck only must pass without a hit.
bores=[]
for sign in (-1,1):
    for x in (-s.pitch_x/2,s.pitch_x/2):
        for y in (sign*s.plate_y-s.pitch_y/2,sign*s.plate_y+s.pitch_y/2):
            hit=ds['tree'].ray_cast(Vector((x,y,1)),Vector((0,0,-1)),2)
            bores.append(dict(x=x,y=y,deck_hit=hit[0] is not None));require(hit[0] is None,'Mount hole does not pass through deck')
proof['mounting_bores']=bores
heads=[o for o in meshes if o.name.startswith('Flush Allen bolt head')]
headcenters=[sum(meshpoints(o),Vector())/len(o.data.vertices) for o in heads]
proof['mount_pattern_centers_m']=[[round(v.x,7),round(v.y,7)] for v in headcenters]
# Kick angle from actual central top vertices along straight ramp, independent
# of the requested angle constant. Nearest centerline points from deck mesh.
angles={}
for sign,label in ((-1,'nose'),(1,'tail')):
    candidates=sorted([v for v in dp if abs(v.x)<1e-6 and sign*v.y>.32],key=lambda v:abs(v.y))
    require(len(candidates)>=2,'Missing kick stations')
    if len(candidates)>1:
        first=Vector((0,sign*.32,rayheight(0,sign*.32)));last=Vector((0,sign*.38,rayheight(0,sign*.38)));angle=math.degrees(math.atan2(last.z-first.z,abs(last.y-first.y)));angles[label]=angle;require(17.4<angle<20.0,label+' measured curved kick tangent outside mold class')
proof['measured_kick_angles_degrees']=angles
# Open bearing face windings must face out of the wheel, not into the bore.
# Unit-length normals alone cannot prove that manufacturing orientation.
bearing_normals=[]
for o in meshes:
    if o.get('part')!='bearings':continue
    axis=Vector((-1 if '-1' in o.name else 1,0,0))
    normal=(o.matrix_world.to_3x3()@o.data.polygons[0].normal).normalized()
    dot=normal.dot(axis);bearing_normals.append(dict(name=o.name,outward_dot=dot))
    require(dot>.99,o.name+' face winding points into wheel bore')
proof['bearing_face_windings']=bearing_normals
# Wheel diameter, contact band and bearing seats are measured from exported
# mesh-space vertex stations, not reprinted from the input spec.
wheelproof=[]
for o in meshes:
    if o.get('part')!='wheels':continue
    ps=meshpoints(o);b=bounds(ps);wheelproof.append(dict(name=o.name,bounds=b,min_ground_z=b['min'][2]))
    require(abs(b['size'][0]-.032)<1e-5,'Wheel width incorrect');require(abs(b['size'][2]-s.wheel_diameter)<1e-5,'Wheel diameter incorrect');require(abs(b['min'][2])<1e-5,'Rest wheel not grounded')
proof['wheels']=wheelproof
if s.state=='beat':
    # Measure the delivered-source plane, rather than echoing its depth tag.
    wheel=bpy.data.objects['Urethane Front L'];direction=Vector((0,-math.sqrt(.5),math.sqrt(.5)))
    maximum=max(v.co.dot(direction) for v in wheel.data.vertices)
    plane=[v.co for v in wheel.data.vertices if abs(v.co.dot(direction)-maximum)<1e-7]
    span=max(p.x for p in plane)-min(p.x for p in plane)
    flat_area=sum(f.area for f in wheel.data.polygons if all(abs(wheel.data.vertices[i].co.dot(direction)-maximum)<1e-7 for i in f.vertices))
    proof['flat_spot']=dict(wheel=wheel.name,measured_plane_radius_m=maximum,measured_depth_m=s.wheel_diameter/2-maximum,coplanar_vertices=len(plane),axial_span_m=span,planar_area_m2=flat_area)
    require(.0013<s.wheel_diameter/2-maximum<.0015 and flat_area>.00002 and span>.014,'Beat wheel has no measurable skid flat')
# Measured plate/deck support and pivot-cup geometry. Source sculpt normals and
# serialization checks cannot substitute for these physical surface checks.
contacts=[]
for label in ('Front','Rear'):
    base=bpy.data.objects[label+' cast baseplate'];support=bpy.data.objects[label+' riser pad'] if s.riser else deck;gap,method=distance(base,support);contacts.append(dict(a=base.name,b=support.name,gap_m=gap,method=method))
    if s.riser:
        pad_gap,pad_method=distance(support,deck);contacts.append(dict(a=support.name,b=deck.name,gap_m=pad_gap,method=pad_method));require(pad_gap<.0002,'Riser pad not seated on deck')
    # Small curvature/decimation uncertainty is allowed, no unsupported 10 mm gaps.
    require(gap<.001,base.name+' unsupported at mounting face')
    h=bpy.data.objects['Hanger_'+label];axis=(h.matrix_world.to_3x3()@Vector((0,0,1))).normalized()
    cup=Vector(h['pivot_cup_m']);yoke=Vector(h['yoke_center_m']);error=axis.cross(yoke-cup).length
    proof[label+'_steering_axis']=dict(axis=list(axis),angle_to_deck_plane_deg=math.degrees(math.asin(abs(axis.z))),cup_to_yoke_axis_error_m=error,pivot=list(h.matrix_world.translation))
    require(error<1e-5,'Steering axis misses yoke')
# Nut clearance is a construction check within the static assembly; it is
# not covered by moving-root sweeps or import-preservation comparisons.
for nut in [o for o in meshes if o.name.startswith('Mount locknut') and 'insert' not in o.name]:
    center=sum(meshpoints(nut),Vector())/len(nut.data.vertices)
    label='Front' if center.y<0 else 'Rear';base=bpy.data.objects[label+' cast baseplate']
    depth,_=penetration(surface(nut),surface(base),.00015)
    contacts.append(dict(a=nut.name,b=base.name,solid_penetration_m=depth))
    require(depth<.00015,'Mount locknut intersects cast pedestal')
for label in ('Front','Rear'):
    hanger=bpy.data.objects[label+' sculpted hanger']
    for kind in ('barrel bushing','cone bushing'):
        bushing=bpy.data.objects[label+' '+kind];gap,method=distance(bushing,hanger)
        contacts.append(dict(a=bushing.name,b=hanger.name,gap_m=gap,method=method));require(gap<.0005,'Bushing not supported by annular seat')
seat_gauges=[]
for label,sign in (('Front',-1),('Rear',1)):
    h=bpy.data.objects['Hanger_'+label];yc=Vector(h['yoke_center_m']);axis=Vector((0,sign*math.sin(math.radians(20)),-math.cos(math.radians(20))))
    hs=surface(bpy.data.objects[label+' sculpted hanger']);gauge=yc+Vector((.0094,0,0))
    low=hs['tree'].ray_cast(gauge-axis*.04,axis,.08)[0];high=hs['tree'].ray_cast(gauge+axis*.04,-axis,.08)[0]
    measured=(high-low).dot(axis) if low is not None and high is not None else 0
    seat_gauges.append(dict(truck=label,actual_mesh_annular_web_thickness_m=measured,gauge_radial_offset_m=.0094));require(.0073<measured<.0083,'Measured bushing seat web thickness incorrect')
proof['bushing_seat_gauges']=seat_gauges
for flap in [o for o in meshes if o.get('part')=='delamination']:
    gap,method=distance(flap,deck);contacts.append(dict(a=flap.name,b=deck.name,gap_m=gap,method=method));require(gap<.0002,'Delaminated ply has no attachment')
proof['mount_contacts']=contacts
# Kit surface sweep focuses on wheel-bite and mounting hardware clearance.
# Bushings are deformable in reality, so they and the kingpin/cup interfaces
# are documented exceptions, rather than claimed rigid-body steering solutions.
motions=[]
for label in ('Front','Rear'):
    motions.append(dict(node='Hanger_'+label,axis='Z',range=[-s.lean_limit,s.lean_limit],step=1,tolerance_m=.0002,
      exclude_fixed=[('Rear' if label=='Front' else 'Front')],
      allow=[dict(moving='',fixed=label+' barrel bushing',reason='Urethane compresses/shears in the real truck; no flex solver at form checkpoint'),
             dict(moving='',fixed=label+' cone bushing',reason='Urethane compliance'),
             dict(moving=label+' sculpted hanger',fixed=label+' pivot cup',reason='Retained stem rotates within rubber pivot cup'),
]))
for label in ('Front','Rear'):
    for side in ('L','R'):
        motions.append(dict(node='Wheel_'+label+'_'+side,axis='X',range=[0,360],step=15,tolerance_m=.0001,
          allow=[dict(moving='608 ',fixed=label+' continuous axle',reason='Bearing inner race seats on the steel axle'),
                 dict(moving='608 ',fixed='Bearing spacer '+label+side,reason='Spacer contacts bearing inner race ends'),
                 dict(moving='608 ',fixed='Axle speed ring '+label+side,reason='Speed rings bear on inner races only')]))
proof['hanger_motion']=sweep({'MOTIONS':motions});require(proof['hanger_motion']['passed'],'Hanger interference outside declared compliant interfaces')
# Wheel spinning: bearing-inner-ring/axle contact is intended. Spacers and
# locknuts are checked by actual axial face separation, invariant under X spin.
axial=[]
for o in meshes:
    if o.get('part')!='wheels':continue
    wb=bounds(meshpoints(o));positive=wb['min'][0]>0;label='Front' if 'Front' in o.name else 'Rear';suffix='R' if positive else 'L'
    nut=bpy.data.objects['Axle nut '+label+suffix];nb=bounds(meshpoints(nut))
    gap=nb['min'][0]-wb['max'][0] if positive else wb['min'][0]-nb['max'][0]
    # Wheel outer rim overhangs the recessed bearing/locknut. Compare radial
    # ranges: the nut fits inside that recess rather than outside wheel width.
    local=surface(o);sample=surface(nut);depth,_=penetration(local,sample,.0001)
    axial.append(dict(wheel=o.name,nut=nut.name,envelope_overlap_m=max(0,-gap),solid_penetration_m=depth))
    require(depth<.0001,'Axle nut intersects urethane recess')
proof['wheel_nut_clearance']=axial
# Minimum actual vertex to deck distance at every steering sample; a sampled
# distance report complements the penetration sweep, not a continuous proof.
clearances=[]
for label in ('Front','Rear'):
    h=bpy.data.objects['Hanger_'+label];rest=h.matrix_basis.copy();minimum=1e9;worst=None
    wheels=[o for o in meshes if o.get('part')=='wheels' and label in o.name]
    for value in range(-int(s.lean_limit),int(s.lean_limit)+1):
        h.matrix_basis=rest@Matrix.Rotation(math.radians(value),4,'Z');bpy.context.view_layer.update()
        for o in wheels:
            d=min(ds['tree'].find_nearest(v)[3] for v in meshpoints(o))
            if d<minimum:minimum=d;worst=value
    h.matrix_basis=rest;bpy.context.view_layer.update();clearances.append(dict(truck=label,minimum_sampled_wheel_vertex_to_deck_m=minimum,at_degrees=worst))
proof['wheel_deck_clearance']=clearances
# Apply the wall socket's complete alignment transform, then measure actual
# floor/wall contacts and penetration. This is not an authored pose constant.
wall_socket=bpy.data.objects['Socket_Rest_Wall'];rest=root.matrix_world.copy()
root.matrix_world=Matrix.Translation((0,0,float(wall_socket['wall_alignment_height_m'])))@Matrix.Rotation(-math.pi/2,4,'X')@wall_socket.matrix_world.inverted();bpy.context.view_layer.update()
posed_bounds={o.name:bounds(meshpoints(o)) for o in meshes};floor=min(b['min'][2] for b in posed_bounds.values());wall=min(b['min'][1] for b in posed_bounds.values())
proof['wall_rest']=dict(min_ground_z_m=floor,min_wall_y_m=wall,alignment_height_m=float(wall_socket['wall_alignment_height_m']),floor_contacts=[n for n,b in posed_bounds.items() if abs(b['min'][2]-floor)<1e-5],wall_contacts=[n for n,b in posed_bounds.items() if abs(b['min'][1]-wall)<1e-5])
require(abs(floor)<1e-5 and abs(wall)<1e-5,'Wall socket does not seat on actual floor/wall surfaces');root.matrix_world=rest;bpy.context.view_layer.update()
# Fresh GLB import: only serialization, names, count, bounds and pivot preservation.
expected={o.name:bounds(meshpoints(o)) for o in meshes};expected_pivots={o.name:o.matrix_world.copy() for o in bpy.context.scene.objects if o.type=='EMPTY'}
glb=src.with_suffix('.glb');g=GLB(glb);rawtris=sum(g.accessor(q['indices']).size//3 for m in g.json['meshes'] for q in m['primitives']);require(rawtris==proof['triangles'],'Raw GLB triangle count mismatch')
normal_error=max(float(abs((g.accessor(q['attributes']['NORMAL'])**2).sum(axis=1)-1).max()) for m in g.json['meshes'] for q in m['primitives']);proof['raw_glb_max_normal_length_squared_error']=normal_error;require(normal_error<.002,'Non-unit GLB normals')
require(not g.json.get('images'),'Checkpoint unexpectedly embeds textures')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb));imported=[o for o in bpy.context.scene.objects if o.type=='MESH'];maxerror=0
for o in imported:
    require(o.name in expected,'Unexpected imported mesh '+o.name)
    if o.name in expected:
        b=bounds(meshpoints(o));e=expected[o.name];maxerror=max(maxerror,max(abs(x-y) for key in ('min','max') for x,y in zip(b[key],e[key])))
require(len(imported)==len(expected),'Fresh import mesh count mismatch');require(maxerror<1e-5,'Fresh import bounds drift')
pivoterror=0
for name,m in expected_pivots.items():
    o=bpy.data.objects.get(name);require(o is not None,'Missing pivot/socket '+name)
    if o:pivoterror=max(pivoterror,max(abs(m[i][j]-o.matrix_world[i][j]) for i in range(4) for j in range(4)))
require(pivoterror<1e-5,'Pivot matrix serialization drift')
proof['serialization']=dict(raw_glb_triangles=rawtris,imported_meshes=len(imported),bounds_error_m=maxerror,pivot_matrix_max_error=pivoterror,glb_bytes=glb.stat().st_size,glb_sha256=hashlib.sha256(glb.read_bytes()).hexdigest(),materials=len(g.json.get('materials',[])),images=len(g.json.get('images',[])))
result=dict(passed=not errors,scope='FORM ONLY: measured source construction and sampled clearance; separate fresh GLB preservation. No baked atlas / UV validation.',measurements=proof,topology=topology,errors=errors)
Path(a.out).write_text(json.dumps(result,indent=2));print('FORM CHECK',result['passed'],proof['triangles'],'triangles',errors)
if errors:raise SystemExit(1)
