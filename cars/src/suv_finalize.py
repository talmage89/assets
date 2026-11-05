"""Kit atlas finalization with explicit seams on folded subpixel cut charts.

Only UVs change in the repair. Tiny cap/gauge triangles receive independent
charts instead of sharing a folded projection. Positions and corner normals
remain those of the accepted source.
"""
import argparse,json,sys
from pathlib import Path
import bpy,numpy as np
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
    # Blender's UV averaging/packing inherited the marking images' 4:1 aspect.
    # Area normalization could not repair that anisotropy: the 96x22 mm front
    # badge became a 17.7x46.8 pixel chart, with its word on the SHORT axis.
    # Reconstruct print metrics from the actual geometry and authored print
    # coordinates; keep their allocated area. Repack against a square atlas,
    # then restore every original image/node before the procedural bake.
    square=bpy.data.images.new('X220 square UV packing target',width=a.size,height=a.size)
    image_sources=[];helpers=[]
    for mat in {m for ob in obs for m in ob.data.materials if m and m.use_nodes}:
        nt=mat.node_tree;active=nt.nodes.active
        for node in nt.nodes:
            if node.type=='TEX_IMAGE':image_sources.append((node,node.image));node.image=square
        helper=nt.nodes.new('ShaderNodeTexImage');helper.image=square;nt.nodes.active=helper;helpers.append((nt,helper,active))
    print_repairs=[]
    for ob in obs:
        me=ob.data;source=me.attributes.get('BakeSourceUV')
        if source is None or not me.uv_layers.get('PrintUV'):continue
        me.calc_loop_triangles();t=me.loop_triangles[0];layer=me.uv_layers['BakeUV']
        coords=np.array([tuple(source.data[i].vector)[:2] for i in t.loops])
        ps=np.array([tuple(ob.matrix_world@me.vertices[i].co) for i in t.vertices])
        metric=np.linalg.solve(coords[1:]-coords[0],ps[1:]-ps[0]);width,height=np.linalg.norm(metric,axis=1)
        area=sum(abs(uv.signed_area([tuple(layer.data[i].uv) for i in tri.loops])) for tri in me.loop_triangles)
        factor=(area/(width*height))**.5;center=sum((q.uv.copy() for q in layer.data),Vector((0,0)))/len(layer.data)
        for li,q in enumerate(layer.data):
            u,v=source.data[li].vector[:2];q.uv=center+Vector(((u-.5)*width*factor,(v-.5)*height*factor))
        print_repairs.append(dict(mesh=ob.name,physical_width_height_m=[width,height],retained_uv_area=area))
    saved={o:[n.vector.copy() for n in o.data.corner_normals] for o in obs};repairs=[]
    for iteration in range(12):
        footprint_changes=iteration==0 and bool(print_repairs)
        for ob in obs:
            layer=ob.data.uv_layers['BakeUV'];groups=list(uv.islands(ob))
            owner={li:j for j,loops in enumerate(groups) for li in loops};areas=[0.]*len(groups)
            ob.data.calc_loop_triangles()
            for t in ob.data.loop_triangles:areas[owner[t.loops[0]]]+=abs(uv.signed_area([tuple(layer.data[i].uv) for i in t.loops]))
            for loops,area in zip(groups,areas):
                if area<1e-14:continue  # The independent triangle repair below separates these.
                coords=np.array([tuple(layer.data[i].uv) for i in loops]);center=coords.mean(axis=0)
                _,axes=np.linalg.eigh((coords-center).T@(coords-center));local=(coords-center)@axes;extent=np.ptp(local,axis=0)
                if area*a.size*a.size>=4 and min(extent)*a.size>=.75:continue
                # A valid but subpixel chart cannot retain its own material:
                # filtering samples another part's gutter. Give each island a
                # sampled footprint before repacking, with room for pack scale.
                stretch=np.maximum(1,1.5/a.size/np.maximum(extent,1e-14));local*=stretch
                factor=max(1,(16/(a.size*a.size*area*np.prod(stretch)))**.5);local*=factor
                for li,co in zip(loops,center+local@axes.T):layer.data[li].uv=co
                repairs.append(dict(mesh=ob.name,reason='Representable material footprint',iteration=iteration))
                footprint_changes=True
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
        if not report['overlap_pairs'] and not report['degenerate_uv_triangles'] and not footprint_changes:break
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
    for rec in print_repairs:
        ob=bpy.data.objects[rec['mesh']];me=ob.data;source=me.attributes['BakeSourceUV'];layer=me.uv_layers['BakeUV'];t=me.loop_triangles[0]
        original=np.array([tuple(source.data[i].vector)[:2] for i in t.loops]);packed=np.array([tuple(layer.data[i].uv) for i in t.loops])
        axes=np.linalg.solve(original[1:]-original[0],packed[1:]-packed[0]);width,height=rec['physical_width_height_m']
        center=np.mean(packed-original@axes,axis=0)+np.array([.5,.5])@axes
        # A rectangular-region pack can rotate a chart before the final .72
        # Y transform. Preserve its word-axis pixels, shrink only surplus
        # cross-word extent to recover physical aspect. Every new UV stays
        # inside its packed parallelogram, so no other chart loses its gutter.
        shrink=min(1,np.linalg.norm(axes[0])*height/(np.linalg.norm(axes[1])*width));axes[1]*=shrink
        for li,q in enumerate(layer.data):q.uv=center+(np.array(tuple(source.data[li].vector)[:2])-.5)@axes
        rec['post_pack_cross_word_scale']=float(shrink)
    for ob,normals in saved.items():ob.data.normals_split_custom_set(normals)
    for node,original in image_sources:node.image=original
    for nt,helper,active in helpers:nt.nodes.remove(helper);nt.nodes.active=active
    bpy.data.images.remove(square)
    # Float corner directions survive the join/rebase smoothing-fan encoding.
    # Export reseeds them after the final attachment, in the owning node frame.
    for ob in all_objects:
        attr=ob.data.attributes.get('X220ExportNormal') or ob.data.attributes.new('X220ExportNormal','FLOAT_VECTOR','CORNER')
        matrix=ob.matrix_world.to_3x3().inverted().transposed()
        for d,n in zip(attr.data,ob.data.corner_normals):d.vector=(matrix@n.vector).normalized()
    report=uv.report(obs,a.size)
    if report['overlap_fraction']>=1e-6 or report['outside_triangles'] or report['degenerate_uv_triangles']:raise ValueError('UV repair failed')
    report['projection_chart_repairs']=repairs
    report['print_metric_repairs']=print_repairs
    report['density_policy']='Measured area normalization, exterior face weights and manufacturing-part priorities'
    report['unique_rectangle']=[0,.28,1,1]
    report['shared_tire_rectangle']=[.005,.005,.995,.255]
    Path(a.report).parent.mkdir(parents=True,exist_ok=True);Path(a.report).write_text(json.dumps(report,indent=2))
    bpy.context.scene['stage']='finalized';bpy.context.scene['atlas_size']=a.size
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    print('X220_UV',len(repairs),'seams',report['coverage'],report['density_px_m'],flush=True)


if __name__=='__main__':main()
