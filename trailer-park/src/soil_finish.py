"""Feathered deposited/compacted soil on the existing Concrete images."""
import bpy
from terrain import mesh


def material(source):
    name='ManufacturedSoilFringe';ma=bpy.data.materials.get(name)
    if ma:return ma
    ma=source.copy();ma.name=name;ma['tiling_vertex_tint']=True
    nodes,links=ma.node_tree.nodes,ma.node_tree.links
    vc=next(n for n in nodes if n.type=='VERTEX_COLOR');bs=next(n for n in nodes if n.type=='BSDF_PRINCIPLED')
    links.new(vc.outputs['Alpha'],bs.inputs['Alpha']);ma.surface_render_method='DITHERED'
    ma.use_backface_culling=False
    return ma


def patch(parent,name,points,ma,color,coverage=.7):
    n=len(points);center=tuple(sum(p[k] for p in points)/n for k in range(3))
    inner=[tuple(center[k]+.62*(p[k]-center[k]) for k in range(3)) for p in points]
    vertices=points+inner+[center];faces=[]
    for i in range(n):
        j=(i+1)%n;faces.extend([(i,j,n+j,n+i),(n+i,n+j,2*n)])
    ob=mesh(parent,name,vertices,faces,ma,coverage)
    for index,row in enumerate(ob.data.color_attributes.active_color.data):row.color=(*color,0 if index<n else .94)
    return ob
