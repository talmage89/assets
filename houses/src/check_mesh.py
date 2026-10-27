"""Actual-surface construction audit, then independent checkpoint GLB import.

Roof rays and hole rays test the mesh, not just source constants. Raw GLB
attributes are read independently for triangles, unit normals and materials;
Blender reimport separately checks envelope and the hinge/socket transforms.
This explicitly does not certify final texture/trim UV readiness.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

import bpy
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree

HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from plan import load,roof_blocks,wall_frame
from kit import gltf


def surface(objects):
    vs=[];fs=[]
    for ob in objects:
        off=len(vs);ob.data.calc_loop_triangles()
        vs.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        fs.extend(tuple(i+off for i in t.vertices) for t in ob.data.loop_triangles)
    return BVHTree.FromPolygons(vs,fs,all_triangles=True)


def source_check(source):
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
    report=json.loads(source.with_suffix('.json').read_text())
    plan=load(report['seed']);from plan import generate
    plan=generate(report['seed'],report['spec'])
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH'];errors=[]
    total=0;nonfinite=0;tiny=0
    for ob in obs:
        ob.data.calc_loop_triangles();total+=len(ob.data.loop_triangles)
        nonfinite+=sum(not all(math.isfinite(v) for v in p.co) for p in ob.data.vertices)
        tiny+=sum(t.area<1e-12 for t in ob.data.loop_triangles)
    if tiny or nonfinite:errors.append(f'topology: tiny={tiny}, nonfinite={nonfinite}')
    if total!=report['triangles'] or not 30000<=total<=80000:errors.append('Triangle budget/count')
    roofs=surface([o for o in obs if o.get('component')=='roof'])
    blocks=roof_blocks(plan['blocks']);samples=[]
    lo=[min(p[k] for b in blocks for p in b.domain()) for k in (0,1)]
    hi=[max(p[k] for b in blocks for p in b.domain()) for k in (0,1)]
    for iy in range(57):
        y=lo[1]+(iy+.413)/57*(hi[1]-lo[1])
        for ix in range(101):
            x=lo[0]+(ix+.371)/101*(hi[0]-lo[0])
            active=[b for b in blocks if b.contains(x,y,b.overhang)]
            if active:samples.append((x,y,max(b.height(x,y) for b in active)))
    for b in blocks:
        if b.roof=='cricket':
            for f in (.01,.1,.25,.5,.75,.9,.99):
                x,y=b.cx,b.y0+b.depth*f;samples.append((x,y,max(v.height(x,y) for v in blocks if v.contains(x,y,v.overhang))))
    max_roof=0;missing=0
    for x,y,z in samples:
        hit=roofs.ray_cast(Vector((x,y,20)),Vector((0,0,-1)),25)
        if hit[0] is None:missing+=1;continue
        max_roof=max(max_roof,abs(hit[0].z-z))
        if hit[1].z<.05:errors.append('Inward top roof normal')
    if missing or max_roof>2e-5:errors.append(f'roof ray error {max_roof}, missing {missing}')
    walls=surface([o for o in obs if o.get('component')=='wall'])
    blocked=[]
    for o in report['openings']:
        b=next(v for v in plan['blocks'] if v.name==o['block']);origin,t,n,l=wall_frame(b,o['face'])
        center=Vector((origin[0]+t[0]*o['u'],origin[1]+t[1]*o['u'],o['z']+o['h']/2))
        normal=Vector((*n,0))
        # 3x3 samples catch strips of wall across an alleged window opening.
        for du in (-.25,0,.25):
            for dz in (.25,.5,.75):
                p=center+Vector((t[0]*du*o['w'],t[1]*du*o['w'],(dz-.5)*o['h']))+normal*.35
                hit=walls.ray_cast(p,-normal,.64)
                if hit[0] is not None:blocked.append(o['id'])
    if blocked:errors.append('Blocked openings '+str(sorted(set(blocked))))
    services=surface([o for o in obs if o.get('component')=='services']);occluded=[]
    for o in report['openings']:
        b=next(v for v in plan['blocks'] if v.name==o['block']);origin,t,n,l=wall_frame(b,o['face']);normal=Vector((*n,0))
        for du in (-.4,-.2,0,.2,.4):
            for dz in (.15,.35,.65,.85):
                p=Vector((origin[0]+t[0]*(o['u']+du*o['w']),origin[1]+t[1]*(o['u']+du*o['w']),o['z']+o['h']*dz))+normal*.40
                hit=services.ray_cast(p,-normal,.58)
                if hit[0] is not None:occluded.append(o['id'])
    if occluded:errors.append('A service blocks an opening '+str(sorted(set(occluded))))
    mount_gaps=[]
    main,garage=plan['blocks']
    mounts=[(main,'front',main.width/2+s*.82,2.08) for s in (-1,1)]+[(garage,'front',garage.width/2+s*2.85,2.40) for s in (-1,1)]+[(main,'back',main.width*.23,.67)]
    for block,face,u,z in mounts:
        origin,t,n,l=wall_frame(block,face)
        sample=Vector((origin[0]+t[0]*u+n[0]*.012,origin[1]+t[1]*u+n[1]*.012,z))
        actual=services.find_nearest(sample)[0]
        mount_gaps.append(walls.find_nearest(actual)[3])
    if max(mount_gaps)>.0001:errors.append('Fixture mounting plate floats off wall')
    roof_vents=surface([o for o in obs if o.get('component')=='roof_vent']);boot_gaps=[]
    for x,y in ((main.cx-2,main.cy+1.5),(main.cx+1.2,main.cy+2.5)):
        for sx,sy in ((-1,-1),(1,-1),(1,1),(-1,1)):
            xx,yy=x+sx*.15,y+sy*.19
            roof_hit=roofs.ray_cast(Vector((xx,yy,20)),Vector((0,0,-1)),25)[0]
            boot_hit=roof_vents.ray_cast(Vector((xx,yy,20)),Vector((0,0,-1)),25)[0]
            if roof_hit is None or boot_hit is None:errors.append('Vent flashing footprint miss')
            else:boot_gaps.append(boot_hit.z-roof_hit.z)
    if boot_gaps and (min(boot_gaps)<.0059 or max(boot_gaps)>.0061):errors.append('Vent flashing does not follow roof pitch')
    # Measure the actual framed entry opening, independent of nominal door size.
    main=plan['blocks'][0];doorx=plan['door_x']
    jamb=surface([o for o in obs if o.name.startswith('Main_front_') and o.get('component')=='door_frame'])
    center=Vector((doorx,main.y0+.01,1.5));ends=[]
    for s in (-1,1):
        hit=jamb.ray_cast(center,Vector((s,0,0)),2)
        if hit[0] is None:errors.append('Missing door jamb');ends.append(center)
        else:ends.append(hit[0])
    opening_width=math.dist(ends[0],ends[1])
    pivot=bpy.data.objects['FrontDoor'];leaf=bpy.data.objects['FrontDoor_Leaf']
    pose=pivot.matrix_world@Matrix.Rotation(math.pi/2,4,'Z')@leaf.matrix_local
    leaf_max=max((pose@v.co).x for v in leaf.data.vertices)
    clear90=ends[1].x-leaf_max
    if clear90<.8128:errors.append('Egress clear width sanity limit')
    frames=surface([o for o in obs if o.get('component')=='door_frame']);socket_gaps={}
    for name in ('FrontThreshold','GarageApron'):
        p=bpy.data.objects['Socket_'+name].matrix_world.translation
        socket_gaps[name]=frames.find_nearest(p)[3]
    if max(socket_gaps.values())>.0015:errors.append('Threshold/apron socket misses beveled sill edge')
    steps=surface([o for o in obs if o.get('component')=='porch_steps']);porch=plan['porch'];step_heights=[]
    for y in (porch.y0-.4572,porch.y0-.1524,porch.y0+.35):
        hit=steps.ray_cast(Vector((porch.cx,y,2.0)),Vector((0,0,-1)),3)
        if hit[0] is None:errors.append('Missing actual tread');continue
        step_heights.append(hit[0].z)
    risers=[step_heights[0]]+[c-a for a,c in zip(step_heights,step_heights[1:])]
    if max(risers)>.19685 or max(risers)-min(risers)>.009525:errors.append('Actual unequal stair risers')
    columns=surface([o for o in obs if o.get('component')=='porch_structure']);support=[]
    for x in (porch.x0+.21,porch.x1-.21):
        p=Vector((x,porch.y0+.20,.3))
        bottom=columns.ray_cast(p,Vector((0,0,1)),1)[0]
        landing=steps.ray_cast(p+Vector((0,0,1)),Vector((0,0,-1)),2)[0]
        if bottom is None or landing is None:errors.append('Column/landing miss')
        else:support.append(abs(bottom.z-landing.z))
    if support and max(support)>1e-5:errors.append('Unsupported porch column')
    # Downspout clearances are measured against the actual shell; the elbows
    # can pass through brackets, but the long wall run must stay outside it.
    pipe_clear=[]
    supports=surface([o for o in obs if o.get('component') in ('wall','porch_structure')]);support_dist=[]
    for row in report['drains']:
        path=row['centerline'];p=Vector(path[3]);q=Vector(path[4])
        for f in (.2,.5,.8):
            point=p.lerp(q,f);near=walls.find_nearest(point)
            if near[0] is not None:pipe_clear.append(near[3]-.0254)
            hit=supports.find_nearest(point)
            if hit[0] is not None:support_dist.append(hit[3])
        if row['outlet'][2]>.15:errors.append('Downspout ends in air')
    if pipe_clear and min(pipe_clear)<-.0005:errors.append('Downspout buried in wall')
    if support_dist and max(support_dist)>.12:errors.append('Downspout too far from a supporting wall/column')
    # Shallow foyer and usable kitchen landing are measured on their surfaces.
    foyer=surface([o for o in obs if o.get('component')=='foyer'])
    center=Vector((plan['door_x'],main.y0+.65,1.7))
    floor_hit=foyer.ray_cast(center,Vector((0,0,-1)),2)[0]
    ceiling_hit=foyer.ray_cast(center,Vector((0,0,1)),2)[0]
    back_hit=foyer.ray_cast(center,Vector((0,1,0)),2)[0]
    if any(v is None for v in (floor_hit,ceiling_hit,back_hit)):errors.append('Foyer enclosure missing')
    elif abs(floor_hit.z-main.floor)>1e-5 or ceiling_hit.z-floor_hit.z<2.4 or back_hit.y-main.y0<1.8:errors.append('Foyer scale')
    patio=next(o for o in report['openings'] if o['kind']=='patio')
    landing=surface([o for o in obs if o.get('component')=='rear_landing'])
    x=main.x0+patio['u'];y=main.y1
    top=landing.ray_cast(Vector((x,y+.4,1)),Vector((0,0,-1)),2)[0]
    if top is None or not 0<=patio['z']-top.z<.04:errors.append('Patio threshold/landing connection')
    deck=plan['spec']['rear_landing']=='deck';start=2.4384 if deck else .94
    rear_treads=[]
    for yy in (y+start+.1524,y+start+.4572):
        hit=landing.ray_cast(Vector((x,yy,1)),Vector((0,0,-1)),2)[0]
        if hit is None:errors.append('Rear stair tread missing')
        else:rear_treads.append(hit.z)
    if top and len(rear_treads)==2:
        rear_risers=[top.z-rear_treads[0],rear_treads[0]-rear_treads[1]]
        if max(rear_risers)>.19685 or max(rear_risers)-min(rear_risers)>.009525:errors.append('Rear stair rises')
    if errors:raise AssertionError('; '.join(sorted(set(errors))))
    return dict(passed=True,triangles=total,roof_rays=len(samples),roof_max_error_m=max_roof,
                roof_misses=missing,opening_rays=len(report['openings'])*9,blocked_openings=blocked,
                service_opening_rays=len(report['openings'])*20,service_occlusions=occluded,
                fixture_wall_mount_gaps_m=mount_gaps,roof_boot_to_roof_gauge_m=boot_gaps,
                socket_to_sill_surface_gap_m=socket_gaps,
                door_opening_measured_m=opening_width,door_clear_at_90_measured_m=clear90,
                door_clear_scope='Conservative posed leaf/handle envelope to measured jamb at 90 degrees',
                tread_top_heights_measured_m=step_heights,risers_measured_m=risers,
                column_landing_gap_measured_m=support,downspout_to_wall_clearance_m=min(pipe_clear),
                downspout_support_distance_max_m=max(support_dist),
                foyer_floor_measured_m=floor_hit.z,foyer_clear_height_measured_m=ceiling_hit.z-floor_hit.z,
                foyer_depth_measured_m=back_hit.y-main.y0,rear_landing_measured_m=top.z,
                rear_tread_top_heights_measured_m=rear_treads,rear_intermediate_risers_measured_m=rear_risers,
                scope='Actual source surfaces; mesh correctness, not serialization')


def delivery_check(source):
    path=source.with_suffix('.glb');expected=json.loads(source.with_suffix('.json').read_text())
    # kit.gltf has a deliberately independent accessor reader.
    raw=gltf.GLB(path);doc=raw.json
    triangles=0;max_normal=0;materials=set();colors=True;color_error=0
    source_colors=set(tuple(round(float(c),6) for c in row.color[:3]) for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.data.color_attributes.get('Tint') for row in ob.data.color_attributes['Tint'].data)
    import numpy as np
    color_table=np.array(list(source_colors))
    for mesh in doc.get('meshes',[]):
        for p in mesh['primitives']:
            indices=raw.accessor(p['indices']);triangles+=len(indices)//3
            normals=raw.accessor(p['attributes']['NORMAL'])
            for n in normals:max_normal=max(max_normal,abs(math.sqrt(sum(v*v for v in n))-1))
            materials.add(p['material']);colors &= 'COLOR_0' in p['attributes']
            if 'COLOR_0' in p['attributes']:
                for rgb in np.unique(np.round(raw.accessor(p['attributes']['COLOR_0'])[:,:3],6),axis=0):
                    color_error=max(color_error,float(np.max(np.abs(color_table-rgb),axis=1).min()))
    assert triangles==expected['triangles'] and triangles<=80000
    assert len(materials)<=6 and len(doc.get('images',[]))==0
    assert colors and max_normal<1e-4
    assert color_error<=.5/255+2e-6
    assert all(m.get('pbrMetallicRoughness',{}).get('baseColorFactor',[1,1,1,1])==[1,1,1,1] for m in doc['materials'])
    # Compare sorted actual surface positions, not just a constant bounds spec.
    source_points=sorted(tuple(ob.matrix_world@p.co) for ob in bpy.context.scene.objects if ob.type=='MESH' for p in ob.data.vertices)
    # Vertex splitting at UV/material seams changes multiplicity; compare sets.
    source_points=set(source_points)
    source_pivots={o.name:tuple(o.matrix_world.translation) for o in bpy.context.scene.objects if o.name in ('FrontDoor','PatioDoor','ServiceDoor') or o.get('socket_kind')}
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    imported=set(tuple(ob.matrix_world@p.co) for ob in bpy.context.scene.objects if ob.type=='MESH' for p in ob.data.vertices)
    # Compare actual float positions by nearest measured point distance,
    # allowing numerical transform error without rounding the observations.
    from mathutils.kdtree import KDTree
    tree=KDTree(len(imported))
    for i,p in enumerate(imported):tree.insert(p,i)
    tree.balance();max_position=max(tree.find(p)[2] for p in source_points)
    assert max_position<2e-5
    pivot_error=max(math.dist(bpy.data.objects[name].matrix_world.translation,p) for name,p in source_pivots.items())
    assert pivot_error<2e-5
    assert len(doc.get('meshes',[]))==4, 'Fixed shell plus three moving leaves'
    return dict(passed=True,triangles=triangles,materials=len(materials),images=0,meshes=len(doc['meshes']),
                primitives=sum(len(m['primitives']) for m in doc['meshes']),
                file_bytes=path.stat().st_size,normal_length_max_error=max_normal,
                vertex_tint_max_error=color_error,
                reimport_position_error_m=max_position,reimport_pivot_socket_error_m=pivot_error,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                scope='Serialization and material-factor/tint retention; no finished texture claim')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=Path('build/house.blend'));p.add_argument('--out',type=Path,default=Path('build/mesh-check.json'))
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);result=dict(source=source_check(a.source));result['glb']=delivery_check(a.source)
    result['pending']=['shared family texture bake','trim UVs and delivered density','used-object weathering','final photo look review']
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
