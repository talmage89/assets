"""Independent X220 atlas, normal-field and hierarchy delivery measurements."""
import argparse,hashlib,io,json,math,sys
from pathlib import Path
import bpy,numpy as np
from PIL import Image,ImageDraw,ImageFilter
from mathutils import Vector
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.gltf import GLB
from kit.uv import signed_area


def percentiles(rows):
    total=sum(w for _,w in rows);acc=0;result={}
    for value,weight in sorted(rows):
        acc+=weight
        for q in [5,50,95]:
            if str(q) not in result and acc>=total*q/100:result[str(q)]=value
    return result


def source(path):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));bpy.context.view_layer.update()
    normals=[];paint={};paint_rows=[];unique_area=tile_area=0
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('asset_set')!='SUV':continue
        me=ob.data;me.calc_loop_triangles();matrix=ob.matrix_world;nm=matrix.to_3x3().inverted().transposed();uv=me.uv_layers['BakeUV'];role=me.attributes.get('skin_face_role')
        for li,row in enumerate(me.corner_normals):normals.append((matrix@me.vertices[me.loops[li].vertex_index].co,(nm@row.vector).normalized()))
        rows=[];ua=wa=0
        for t in me.loop_triangles:
            atlas=abs(signed_area([tuple(uv.data[i].uv) for i in t.loops]))
            if ob.name=='Tire_FR':tile_area+=atlas
            elif not ob.name.startswith('Tire_'):unique_area+=atlas
            f=me.polygons[t.polygon_index]
            if not me.materials[f.material_index].get('vehicle_paint') or role and role.data[f.index].value!=0:continue
            points=[matrix@me.vertices[i].co for i in t.vertices];area=(points[1]-points[0]).cross(points[2]-points[0]).length*.5
            if area<=0 or atlas<=0:continue
            row=(2048*math.sqrt(atlas/area),atlas);rows.append(row);paint_rows.append(row);ua+=atlas;wa+=area
        if rows:paint[ob.name]=dict(triangles=len(rows),surface_m2=wa,atlas_fraction=ua,density_px_m=percentiles(rows))
    atlas_summary=dict(unique_fraction=unique_area,shared_tire_fraction_counted_once=tile_area,total_occupied_fraction=unique_area+tile_area,
        painted_density_px_m=percentiles(paint_rows),density_percentile_weight='UV area',coverage_scope='Triangle UV areas; unique region non-overlap is gated independently by kit.verify, canonical tyre tile counted once')
    return normals,paint,atlas_summary


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--finalized',required=True);p.add_argument('--counts',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(a.source);g=GLB(path);doc=g.json;errors=[]
    def check(ok,message):
        if not ok:errors.append(message)
    check(len(doc['materials'])==4,'Expected family Paint/Opaque/Glass/Lamps palette')
    check(len(doc['images'])==3 and len(doc['textures'])==3,'Atlas images or texture views duplicated')
    check(not any('COLOR_0' in p['attributes'] for m in doc['meshes'] for p in m['primitives']),'Data mask exported as albedo colors')
    images=[]
    for i,row in enumerate(doc['images']):
        im=Image.open(io.BytesIO(g.image(i)));check(im.size==(2048,2048),'Wrong map size')
        images.append(dict(name=row.get('name'),bytes=len(g.image(i)),size=list(im.size),mode=im.mode))
    mats={m['name'].split()[-1]:m for m in doc['materials']};paint=mats['Paint'];extras=paint['extras']
    check(set(json.loads(extras['paint_colors']))=={'Porcelain','Carbon','Graphite','Aluminum','Atlantic'},'Factory colors lost')
    check('KHR_materials_clearcoat' in paint.get('extensions',{}),'Clearcoat lost')
    check('KHR_materials_transmission' in mats['Glass'].get('extensions',{}),'Transmission lost')
    normals,panels,atlas_summary=source(Path(a.finalized));tree=KDTree(len(normals))
    for name,panel in panels.items():
        if panel['surface_m2']>.02:check(panel['density_px_m']['50']>=100,'Painted panel underallocated: '+name)
    for i,(pos,_) in enumerate(normals):tree.insert(pos,i)
    tree.balance();angles=[];max_distance=0;bounds_points=[];worst=[]
    for node_index,node in enumerate(doc['nodes']):
        if 'mesh' not in node:continue
        from mathutils import Matrix
        matrix=Matrix(g.world(node_index).tolist());conversion=Matrix(((1,0,0,0),(0,0,-1,0),(0,1,0,0),(0,0,0,1)));matrix=conversion@matrix
        nm=matrix.to_3x3().inverted().transposed()
        for prim in doc['meshes'][node['mesh']]['primitives']:
            ps=g.accessor(prim['attributes']['POSITION']);ns=g.accessor(prim['attributes']['NORMAL'])
            for pos,normal in zip(ps,ns):
                pos=matrix@Vector(pos);bounds_points.append(tuple(pos));normal=(nm@Vector(normal)).normalized();near=tree.find_range(pos,2e-5)
                if not near:errors.append('Imported normal position has no source');continue
                angle=min(math.degrees(normal.angle(normals[i][1],0)) for _,i,_ in near)
                angles.append(angle);max_distance=max(max_distance,min(d for _,_,d in near))
                if angle>.09:worst.append(dict(node=node['name'],material=doc['materials'][prim['material']]['name'],point=list(pos),angle_degrees=angle))
    check(bool(angles) and max(angles)<.10,'Normal field changed through UV/export')
    bounds=np.ptp(np.asarray(bounds_points),axis=0)
    check(bool(np.all(np.abs(bounds-[2.117,4.59883,1.735])<.002)),'Actual vertex envelope changed')
    names={n['name']:i for i,n in enumerate(doc['nodes'])}
    drivers=[n for n in names if n.endswith(' driver') and 'strut' in n]
    check(len(drivers)==8,'Telescoping support drivers were consolidated')
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    from suv_mechanics import update_supports
    support_error=0
    for name in drivers:
        ob=bpy.data.objects[name];before=ob.matrix_world.copy();update_supports();support_error=max(support_error,max(abs(before[i][j]-ob.matrix_world[i][j]) for i in range(4) for j in range(4)))
    check(support_error<2e-5,'Support rest frames changed during export')
    counts=json.loads(Path(a.counts).read_text());delivered={}
    for node in doc['nodes']:
        if 'mesh' in node:delivered[node['name']]=sum(doc['accessors'][p['indices']]['count']//3 for p in doc['meshes'][node['mesh']]['primitives'])
    check(sum(delivered.values())==counts['triangles'],'Part budget changed')
    result=dict(passed=not errors,errors=errors,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size,
        triangles=sum(delivered.values()),triangles_by_exported_part=delivered,triangles_by_manufacturing_category=counts['categories'],images=images,materials=4,
        actual_vertex_bounds_m=bounds.tolist(),atlas=atlas_summary,painted_panels=panels,painted_atlas_fraction=sum(r['atlas_fraction'] for r in panels.values()),normal_samples=len(angles),normal_angle_p50_p95_max_degrees=np.percentile(angles,[50,95,100]).tolist(),normal_position_error_m=max_distance,
        normal_disagreements=sorted(worst,key=lambda r:-r['angle_degrees'])[:40],support_drivers=drivers,support_rest_matrix_error=support_error,gpu_texture_mib_8bpp_with_mips=16,
        scope='Raw accessors, exact source normal field, measured painted-panel UV areas/density and re-imported support rest frames; clearance is independently sampled in source sweeps')
    Path(a.out).write_text(json.dumps(result,indent=2));print('X220_DELIVERY_CHECK',result['passed'],result['errors'],result['triangles'],result['normal_angle_p50_p95_max_degrees'])
    if errors:raise ValueError(errors)


if __name__=='__main__':main()
