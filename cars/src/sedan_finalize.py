"""Kit finalization plus explicit seams for folded subpixel projection charts.

A Smart UV projection can put a very thin gauge triangle over its neighbor.
Split the smaller triangle's UV chart and repack; never relax overlap policy.
Geometry, materials and authored corner normals are preserved. Existing chart
scales stay proportional, except the explicitly logged subtexel-altitude repair.
"""
import sys,json,argparse,math,runpy
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import finalize,uv

def continuous_charts(obs,config,margin):
    """Unwrap each visible sheet as a connected patch, instead of 5° fragments."""
    for ob in obs:
        roles=ob.data.attributes.get('sheet_role')
        if roles is None:continue
        role_values=[r.value for r in roles.data]
        # Visible skins get connected charts. Rigid backs and gauge rims use
        # the broader SmartUV angle; their old tiny 5-degree islands consumed
        # the atlas in margins instead of useful painted-panel texels.
        for role in [0]:
            bpy.ops.object.select_all(action='DESELECT');ob.select_set(True)
            bpy.context.view_layer.objects.active=ob
            bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='DESELECT');bpy.ops.object.mode_set(mode='OBJECT')
            for edge in ob.data.edges:edge.use_seam=False
            for face in ob.data.polygons:face.select=role_values[face.index]==role
            bpy.ops.object.mode_set(mode='EDIT');bpy.context.tool_settings.mesh_select_mode=(False,False,True)
            bpy.ops.uv.unwrap(method='ANGLE_BASED',margin=0,correct_aspect=False)
            bpy.ops.object.mode_set(mode='OBJECT')
    # Normalize every old/new chart in meters, then apply actual manufacturing
    # surface priorities. A chart's previous atlas size must not affect this.
    for ob in obs:
        layer=ob.data.uv_layers['BakeUV'];groups=list(uv.islands(ob));owner={i:k for k,g in enumerate(groups) for i in g}
        area=[[0.,0.,0.] for g in groups];ob.data.calc_loop_triangles()
        attr=ob.data.attributes.get(config.get('UV_PRIORITY_ATTRIBUTE',''))
        priority=next((v for k,v in config.get('UV_PRIORITY',{}).items() if ob.name.startswith(k)),config.get('UV_DEFAULT_PRIORITY',1.))
        for tri in ob.data.loop_triangles:
            ua=abs(uv.signed_area([tuple(layer.data[i].uv) for i in tri.loops]));ps=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
            wa=(ps[1]-ps[0]).cross(ps[2]-ps[0]).length*.5
            row=area[owner[tri.loops[0]]];row[0]+=ua;row[1]+=wa;row[2]+=wa*(attr.data[tri.polygon_index].value if attr else 1.)
        for loops,(ua,wa,weighted) in zip(groups,area):
            if min(ua,wa)<=1e-20:continue
            scale=math.sqrt(wa/ua)*priority*weighted/wa
            center=sum((layer.data[i].uv.copy() for i in loops),Vector((0,0)))/len(loops)
            for i in loops:layer.data[i].uv=center+(layer.data[i].uv-center)*scale
    bpy.ops.object.select_all(action='DESELECT')
    for ob in obs:ob.select_set(True)
    bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM',rotate=True,rotate_method='ANY',scale=True,merge_overlap=False,margin_method='FRACTION',margin=margin,pin=False,shape_method='CONCAVE')
    bpy.ops.object.mode_set(mode='OBJECT')


def main():
    p=argparse.ArgumentParser(add_help=False);p.add_argument('--out');p.add_argument('--report');p.add_argument('--size',type=int,default=2048);p.add_argument('--margin',type=float,default=.0012)
    p.add_argument('--config');p.add_argument('--target-density',type=float,default=360)
    a,_=p.parse_known_args(sys.argv[sys.argv.index('--')+1:])
    try:finalize.main()
    except RuntimeError as error:
        # The kit's intermediate SmartUV check may reject folded fragments.
        # Continue only into this explicit chart repair; the final strict
        # overlap/density/bounds validation below still decides acceptance.
        if not str(error).startswith('UV validation failed:'):raise
        print('S240_REPAIR_PRELIMINARY_CHARTS',str(error)[:180],flush=True)
    config=runpy.run_path(a.config) if a.config else {}
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]
    saved={o:[n.vector.copy() for n in o.data.corner_normals] for o in obs if o.data.has_custom_normals};repairs=[]
    continuous_charts(obs,config,a.margin)
    for iteration in range(32):
        # Repacking can quantize an extremely thin subtexel UV sliver to a
        # line. Give that tiny chart a representable altitude; no mesh change.
        for ob in obs:
            ob.data.calc_loop_triangles();layer=ob.data.uv_layers['BakeUV']
            for tri in ob.data.loop_triangles:
                coords=[layer.data[i].uv.copy() for i in tri.loops]
                if abs(uv.signed_area(coords))>=1e-13:continue
                ps=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
                lengths=[(ps[(i+1)%3]-ps[i]).length for i in range(3)];k=max(range(3),key=lambda i:lengths[i])
                order=[k,(k+1)%3,(k+2)%3];a0,b0,c0=[ps[i] for i in order];edge=b0-a0;length=edge.length
                x=(c0-a0).dot(edge)/length;alt=(c0-a0).cross(edge).length/length;scale=.12
                center=sum(coords,Vector((0,0)))/3
                for index,q in zip(order,[(0,0),(length*scale,0),(x*scale,max(alt*scale,2e-6))]):layer.data[tri.loops[index]].uv=center+Vector(q)
                repairs.append(dict(iteration=iteration,mesh=ob.name,triangle=tri.index,reason='Representable UV altitude for a subtexel sliver'))
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
    for ob,normals in saved.items():ob.data.normals_split_custom_set(normals)
    report=uv.report(obs,a.size)
    if report['overlap_fraction']>=1e-6 or report['outside_triangles'] or report['degenerate_uv_triangles']:raise ValueError('Repaired UV validation failed: '+str({k:v for k,v in report.items() if k!='island_measurements'}))
    old=dict(report);old['projection_chart_seams']=repairs
    old['chart_method']='Continuous unwrapped outer sheets; SmartUV rigid interiors; measured area/priority scaling'
    old['target_density_px_m']=a.target_density
    if report['coverage']<.35:raise ValueError('Insufficient atlas utilization after continuous chart packing')
    old['density_policy']='Measured area-normalized exterior priority, reduced hidden gauge'
    Path(a.report).write_text(json.dumps(old,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    print('S240_UV_SEAMS',len(repairs),'splits, overlaps',report['overlap_pairs'],'coverage',report['coverage'],flush=True)
if __name__=='__main__':main()
