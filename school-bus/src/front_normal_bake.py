"""Selected-to-active normal transfer from the independent dense hood mold."""
import time
import bpy,numpy as np
from PIL import Image,ImageDraw,ImageFilter

def project(low,high,size,samples):
    low.hide_render=False;high.hide_render=False
    bpy.ops.object.select_all(action='DESELECT');low.select_set(True);high.select_set(True)
    bpy.context.view_layer.objects.active=low
    mat=bpy.data.materials.new('Front projection target');mat.use_nodes=True
    low.data.materials.clear();low.data.materials.append(mat)
    for face in low.data.polygons:face.material_index=0
    neutral=bpy.data.materials.new('Dense fiberglass normal source');neutral.use_nodes=True
    high.data.materials.clear();high.data.materials.append(neutral)
    for face in high.data.polygons:face.material_index=0;face.use_smooth=True
    im=bpy.data.images.new('Dense front normals',size,size,alpha=True,float_buffer=True)
    im.colorspace_settings.name='Non-Color';node=mat.node_tree.nodes.new('ShaderNodeTexImage')
    node.image=im;mat.node_tree.nodes.active=node
    uv=low.data.uv_layers['BakeUV'];low.data.uv_layers.active=uv;uv.active_render=True
    mask=Image.new('L',(size,size),0);draw=ImageDraw.Draw(mask)
    approved=Image.new('L',(size,size),0);accept=ImageDraw.Draw(approved)
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    high.data.calc_loop_triangles()
    low.data.calc_loop_triangles()
    if len(high.data.loop_triangles)<len(low.data.loop_triangles)*4:
        raise ValueError('Dense hood source has lost its subdivision geometry')
    tree=BVHTree.FromPolygons([high.matrix_world@v.co for v in high.data.vertices],
                             [tuple(t.vertices) for t in high.data.loop_triangles],all_triangles=True)
    area_total=0;area_fallback=0;distances=[];misses=0;back_hits=0
    low.data.calc_loop_triangles()
    for tri in low.data.loop_triangles:
        polygon=[(uv.data[i].uv.x*size,(1-uv.data[i].uv.y)*size) for i in tri.loops]
        draw.polygon(polygon,fill=255)
        ps=[low.matrix_world@low.data.vertices[i].co for i in tri.vertices]
        center=sum(ps,Vector())/3;normal=(ps[1]-ps[0]).cross(ps[2]-ps[0]).normalized()
        hit,hn,_,_=tree.ray_cast(center+normal*.035,-normal,.080)
        area=(ps[1]-ps[0]).cross(ps[2]-ps[0]).length/2;area_total+=area
        good=hit is not None and hn.dot(normal)>.1 and (hit-center).length<.030
        if hit is None:misses+=1
        else:
            distances.append((hit-center).length)
            if hn.dot(normal)<=.1:back_hits+=1
        if good:accept.polygon(polygon,fill=255)
        else:area_fallback+=area
    interior=np.asarray(mask.filter(ImageFilter.MinFilter(5)))>0
    fraction=area_fallback/max(area_total,1e-12)
    print('FRONT_PROJECTION_PREFLIGHT',dict(high_triangles=len(high.data.loop_triangles),
        fallback_area_fraction=fraction,misses=misses,back_hits=back_hits),flush=True)
    if fraction>.08:
        raise ValueError('Dense mold projection misses more than 8% of the hood surface')
    sc=bpy.context.scene;sc.cycles.samples=samples
    sc.render.bake.use_selected_to_active=True;sc.render.bake.use_clear=True
    sc.render.bake.cage_extrusion=.035;sc.render.bake.max_ray_distance=.080
    sc.render.bake.margin=8;sc.render.bake.margin_type='EXTEND'
    started=time.time()
    bpy.ops.object.bake(type='NORMAL',normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z')
    values=np.empty(size*size*4,np.float32);im.pixels.foreach_get(values)
    values=np.flipud(values.reshape(size,size,4)).copy()
    valid=(values[:,:,3]>.5)&(values[:,:,2]>=.5)
    # The atlas patch is accepted only where the projection exists and faces
    # the low surface. Missing/back-facing interiors are explicitly reported.
    report=dict(method='Selected-to-active dense cage mold to game hood',
                seconds=time.time()-started,low_triangles=len(low.data.loop_triangles),
                high_triangles=sum(len(p.vertices)-2 for p in high.data.polygons),
                checked_interior_texels=int(interior.sum()),
                missed_or_backward_interior=int(np.count_nonzero(interior&~valid)),
                accepted_texels=int(np.count_nonzero((np.asarray(mask)>0)&valid)),
                cage_m=.035,ray_distance_m=.080)
    chosen=(np.asarray(approved)>0)&valid
    report['independent_triangle_center_rays']=dict(samples=len(low.data.loop_triangles),misses=misses,
        back_hits=back_hits,exact_surface_fallback_area_fraction=area_fallback/max(area_total,1e-12),
        hit_distance_p95_m=float(np.percentile(distances,95)) if distances else None,
        hit_distance_max_m=max(distances) if distances else None,
        scope='Each game triangle center against dense source triangles; bad triangles retain direct normals')
    report['accepted_texels']=int(chosen.sum())
    bpy.data.images.remove(im);bpy.data.objects.remove(low,do_unlink=True)
    bpy.data.objects.remove(high,do_unlink=True)
    return values,chosen,report
