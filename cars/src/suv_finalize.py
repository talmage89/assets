"""Kit atlas finalization with explicit seams on folded subpixel cut charts.

Only UVs change in the repair. Tiny cap/gauge triangles receive independent
charts instead of sharing a folded projection. Positions and corner normals
remain those of the accepted source.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import finalize,uv


def main():
    p=argparse.ArgumentParser(add_help=False);p.add_argument('--out',required=True);p.add_argument('--report',required=True);p.add_argument('--size',type=int,default=2048);p.add_argument('--margin',type=float,default=.0015)
    a,_=p.parse_known_args(sys.argv[sys.argv.index('--')+1:])
    try:finalize.main()
    except RuntimeError as error:
        if not str(error).startswith('UV validation failed:'):raise
        print('X220_UV_REPAIR',str(error),flush=True)
    all_objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='SUV']
    obs=[o for o in all_objects if not o.name.startswith('Tire_')]
    saved={o:[n.vector.copy() for n in o.data.corner_normals] for o in obs};repairs=[]
    for iteration in range(12):
        for ob in obs:
            me=ob.data;me.calc_loop_triangles();layer=me.uv_layers['BakeUV']
            for t in me.loop_triangles:
                coords=[layer.data[i].uv.copy() for i in t.loops]
                if abs(uv.signed_area(coords))>=1e-10:continue
                ps=[ob.matrix_world@me.vertices[i].co for i in t.vertices]
                edge=max(range(3),key=lambda i:(ps[(i+1)%3]-ps[i]).length_squared)
                order=[edge,(edge+1)%3,(edge+2)%3];p0,p1,p2=[ps[i] for i in order];d=p1-p0;length=d.length
                if length==0 or (p2-p0).cross(d).length*.5<1e-12:raise ValueError('Degenerate physical triangle '+ob.name+str(t.index))
                x=(p2-p0).dot(d)/length;alt=(p2-p0).cross(d).length/length
                center=sum(coords,Vector((0,0)))/3
                width=max(length*.1,2e-5);along=x/length*width
                for index,q in zip(order,[(0,0),(width,0),(along,max(alt*.1,2e-5))]):layer.data[t.loops[index]].uv=center+Vector(q)
                repairs.append(dict(mesh=ob.name,triangle=t.index,reason='Independent representable UV sliver',iteration=iteration))
        report=uv.report(obs,a.size)
        if not report['overlap_pairs'] and not report['degenerate_uv_triangles']:break
        triangles=[]
        for ob in obs:
            ob.data.calc_loop_triangles()
            for t in ob.data.loop_triangles:
                if t.area>=1e-12 and abs(uv.signed_area([tuple(ob.data.uv_layers['BakeUV'].data[i].uv) for i in t.loops]))>=1e-14:triangles.append((ob,t.index,tuple(t.loops)))
        def area(index):
            ob,_,loops=triangles[index]
            return abs(uv.signed_area([tuple(ob.data.uv_layers['BakeUV'].data[i].uv) for i in loops]))
        for index in sorted({min([x,y],key=area) for x,y,_ in report['overlap_examples']}):
            ob,ti,loops=triangles[index];layer=ob.data.uv_layers['BakeUV']
            for li in loops:layer.data[li].uv+=Vector((.00037+(index%53)*.000001,.00051+(index%67)*.000001))
            repairs.append(dict(mesh=ob.name,triangle=ti,reason='Separate folded projected triangle',iteration=iteration))
        bpy.ops.object.select_all(action='DESELECT')
        for ob in obs:ob.select_set(True)
        for ob in obs:
            for p in ob.data.uv_layers['BakeUV'].data:p.uv.y=(p.uv.y-.28)/.72
        bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM',rotate=True,rotate_method='ANY',scale=True,merge_overlap=False,margin_method='FRACTION',margin=a.margin,pin=False,shape_method='CONVEX')
        bpy.ops.object.mode_set(mode='OBJECT')
        # The kit reserved the lower band for the shared carcass tile. Repack
        # repaired unique charts into the same rectangular delivery region.
        for ob in obs:
            for p in ob.data.uv_layers['BakeUV'].data:p.uv.y=.28+p.uv.y*.72
    for ob,normals in saved.items():ob.data.normals_split_custom_set(normals)
    # Float corner directions survive the join/rebase smoothing-fan encoding.
    # Export reseeds them after the final attachment, in the owning node frame.
    for ob in all_objects:
        attr=ob.data.attributes.get('X220ExportNormal') or ob.data.attributes.new('X220ExportNormal','FLOAT_VECTOR','CORNER')
        matrix=ob.matrix_world.to_3x3().inverted().transposed()
        for d,n in zip(attr.data,ob.data.corner_normals):d.vector=(matrix@n.vector).normalized()
    report=uv.report(obs,a.size)
    if report['overlap_fraction']>=1e-6 or report['outside_triangles'] or report['degenerate_uv_triangles']:raise ValueError('UV repair failed')
    report['projection_chart_repairs']=repairs
    report['density_policy']='Measured area normalization, exterior face weights and manufacturing-part priorities'
    report['unique_rectangle']=[0,.28,1,1]
    report['shared_tire_rectangle']=[.005,.005,.995,.255]
    Path(a.report).parent.mkdir(parents=True,exist_ok=True);Path(a.report).write_text(json.dumps(report,indent=2))
    bpy.context.scene['stage']='finalized';bpy.context.scene['atlas_size']=a.size
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    print('X220_UV',len(repairs),'seams',report['coverage'],report['density_px_m'],flush=True)


if __name__=='__main__':main()
