"""Kit finalization plus explicit seams for folded subpixel projection charts.

A Smart UV projection can put a very thin gauge triangle over its neighbor.
Split the smaller triangle's UV chart and repack; never relax overlap policy.
Geometry, materials and authored corner normals are preserved. Existing chart
scales stay proportional, except the explicitly logged subtexel-altitude repair.
"""
import sys,json,argparse,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import finalize,uv

original_islands=uv.islands
altitude_repairs=[]
print_charts=set()
def representable_islands(ob):
    """Retain micron-scale cut triangles with an explicit isolated UV chart."""
    layer=ob.data.uv_layers['BakeUV'];ob.data.calc_loop_triangles()
    # average_islands_scale inherits each source image's aspect even when
    # Smart UV's correct_aspect is disabled. A 4:1 badge consequently got a
    # 1:4 chart: only fourteen pixels along ALDER. Reconstruct print charts
    # from their physical metric before the kit applies density priorities.
    # BakeSourceUV still addresses the original artwork, independently.
    source=ob.data.attributes.get('BakeSourceUV')
    if ob.name not in print_charts and source and ob.data.uv_layers.get('PrintUV'):
        import numpy as np
        coordinates=np.array([list(r.vector)[:2]+[1.] for r in source.data])
        positions=np.array([list(ob.matrix_world@ob.data.vertices[l.vertex_index].co) for l in ob.data.loops])
        basis=np.linalg.lstsq(coordinates,positions,rcond=None)[0]
        width=float(np.linalg.norm(basis[0]));along=float(np.dot(basis[0],basis[1])/width)
        height=math.sqrt(max(0,float(np.dot(basis[1],basis[1]))-along**2))
        for row,q in zip(layer.data,coordinates):row.uv=(q[0]*width+q[1]*along,q[1]*height)
        print_charts.add(ob.name)
    for tri in ob.data.loop_triangles:
        coords=[layer.data[i].uv.copy() for i in tri.loops]
        if abs(uv.signed_area(coords))>1e-16:continue
        ps=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
        k=max(range(3),key=lambda i:(ps[(i+1)%3]-ps[i]).length)
        order=[k,(k+1)%3,(k+2)%3];a,b,c=[ps[i] for i in order]
        edge=b-a;length=edge.length
        if length<1e-12:raise ValueError('Zero-length source triangle '+ob.name)
        x=(c-a).dot(edge)/length;alt=(c-a).cross(edge).length/length
        center=sum(coords,Vector((0,0)))/3
        for index,q in zip(order,[(0,0),(length,0),(x,max(alt,2e-6))]):
            layer.data[tri.loops[index]].uv=center+Vector(q)
        altitude_repairs.append(dict(mesh=ob.name,triangle=tri.index,world_altitude_m=alt,minimum_uv_altitude=2e-6))
    return original_islands(ob)

def main():
    p=argparse.ArgumentParser(add_help=False);p.add_argument('--out');p.add_argument('--report');p.add_argument('--size',type=int,default=2048);p.add_argument('--margin',type=float,default=.0012)
    a,_=p.parse_known_args(sys.argv[sys.argv.index('--')+1:]);uv.islands=representable_islands
    try:finalize.main()
    except RuntimeError as error:
        if not str(error).startswith('UV validation failed:'):raise
        # The kit has completed its geometry/normal work. Diagnose and split
        # any remaining folded chart below under the same strict limits.
        Path(a.report).write_text(json.dumps(uv.report([o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o],a.size)))
    finally:uv.islands=original_islands
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]
    saved={o:[n.vector.copy() for n in o.data.corner_normals] for o in obs if o.data.has_custom_normals};repairs=[]
    # The kit restores source images after its pack. The extra cut-sliver
    # repacks below must also see the square delivery aspect, not print aspect.
    aspect=bpy.data.images.new('H120 UV repair aspect',8,8);sources=[]
    for mat in {m for ob in obs for m in ob.data.materials if m and m.use_nodes}:
        for node in mat.node_tree.nodes:
            if node.type=='TEX_IMAGE':sources.append((node,node.image));node.image=aspect
    for iteration in range(8):
        # Repacking can quantize an extremely thin subtexel UV sliver to a
        # line. Give that tiny chart a representable altitude; no mesh change.
        for ob in obs:
            ob.data.calc_loop_triangles();layer=ob.data.uv_layers['BakeUV']
            for tri in ob.data.loop_triangles:
                coords=[layer.data[i].uv.copy() for i in tri.loops]
                longest=max((coords[(i+1)%3]-coords[i]).length for i in range(3))
                altitude=2*abs(uv.signed_area(coords))/max(longest,1e-15)
                # glTF stores float32 UVs and flips V. A merely nonzero
                # sliver can collapse in that subtraction on re-import.
                if altitude>=5e-7:continue
                ps=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
                lengths=[(ps[(i+1)%3]-ps[i]).length for i in range(3)];k=max(range(3),key=lambda i:lengths[i])
                order=[k,(k+1)%3,(k+2)%3];a0,b0,c0=[ps[i] for i in order];edge=b0-a0;length=edge.length
                x=(c0-a0).dot(edge)/length;alt=(c0-a0).cross(edge).length/length;scale=.12
                center=sum(coords,Vector((0,0)))/3
                for index,q in zip(order,[(0,0),(length*scale,0),(x*scale,max(alt*scale,2e-6))]):layer.data[tri.loops[index]].uv=center+Vector(q)
                repairs.append(dict(iteration=iteration,mesh=ob.name,triangle=tri.index,reason='Float32-safe UV altitude for a subtexel sliver',uv_altitude_before=altitude))
        report=uv.report(obs,a.size)
        if not report['overlap_pairs']:break
        triangles=[]
        for ob in obs:
            ob.data.calc_loop_triangles()
            for tri in ob.data.loop_triangles:
                if abs(uv.signed_area([tuple(ob.data.uv_layers['BakeUV'].data[i].uv) for i in tri.loops]))>=1e-14 and tri.area>=1e-12:triangles.append((ob,tuple(tri.loops)))
        def area(index):
            ob,loops=triangles[index];return abs(uv.signed_area([tuple(ob.data.uv_layers['BakeUV'].data[i].uv) for i in loops]))
        chosen={min([x,y],key=area) for x,y,_ in report['overlap_examples']}
        for index in sorted(chosen):
            ob,loops=triangles[index];layer=ob.data.uv_layers['BakeUV']
            for i in loops:layer.data[i].uv+=Vector((.00037+(index%53)*.000001,.00051+(index%67)*.000001))
            repairs.append(dict(iteration=iteration,mesh=ob.name,triangle=index,uv_area_before=area(index)))
        bpy.ops.object.select_all(action='DESELECT')
        for ob in obs:ob.select_set(True)
        bpy.context.view_layer.objects.active=obs[0]
        bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM',rotate=True,rotate_method='ANY',scale=True,merge_overlap=False,margin_method='FRACTION',margin=a.margin,pin=False,shape_method='CONCAVE')
        bpy.ops.object.mode_set(mode='OBJECT')
    for node,image in sources:node.image=image
    bpy.data.images.remove(aspect)
    for ob,normals in saved.items():ob.data.normals_split_custom_set(normals)
    report=uv.report(obs,a.size)
    if report['coverage']<.35 or report['overlap_fraction']>=1e-6 or report['outside_triangles'] or report['degenerate_uv_triangles']:raise ValueError('Repaired UV validation failed: '+str({k:v for k,v in report.items() if k!='island_measurements'}))
    old=json.loads(Path(a.report).read_text());old.update(report);old['projection_chart_seams']=repairs;old['representable_slivers']=altitude_repairs
    old['print_charts']={}
    for ob in obs:
        source=ob.data.attributes.get('BakeSourceUV')
        if ob.name not in print_charts or source is None:continue
        import numpy as np
        coords=np.array([list(r.vector)[:2]+[1.] for r in source.data])
        packed=np.array([list(r.uv) for r in ob.data.uv_layers['BakeUV'].data])
        positions=np.array([list(ob.matrix_world@ob.data.vertices[l.vertex_index].co) for l in ob.data.loops])
        atlas=np.linalg.lstsq(coords,packed,rcond=None)[0]
        physical=np.linalg.lstsq(coords,positions,rcond=None)[0]
        pixels=np.linalg.norm(atlas[:2],axis=1)*a.size
        density=pixels/np.linalg.norm(physical[:2],axis=1)
        old['print_charts'][ob.name]=dict(pixels_u_v=pixels.tolist(),density_u_v_px_m=density.tolist())
        if max(density)/min(density)>1.02:raise ValueError('Stretched printed atlas chart: '+ob.name)
    old['paint_panel_density_px_m']={}
    for name in sorted({r['object'] for r in report['island_measurements']}):
        if not name.startswith(('Door ','Hood outer','Roof','Front fender','Rear quarter','Front molded fascia','Rear molded fascia','Liftgate outer')):continue
        rows=[r for r in report['island_measurements'] if r['object']==name]
        old['paint_panel_density_px_m'][name]=a.size*math.sqrt(sum(r['uv_area'] for r in rows)/sum(r['surface_m2'] for r in rows))
    bpy.context.scene['stage']='finalized';bpy.context.scene['atlas_size']=a.size
    Path(a.report).write_text(json.dumps(old,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    print('H120_UV_SEAMS',len(repairs),'splits, overlaps',report['overlap_pairs'],'coverage',report['coverage'],flush=True)
if __name__=='__main__':main()
