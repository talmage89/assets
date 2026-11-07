"""Authored shared manufacture charts, not unique overlapping islands.

Every face lies inside its declared atlas cell. Repetition within cells is
explicit and split at tile crossings; mip gutters retain 8 delivered pixels.
"""
import math
from pathlib import Path
import bpy
from mathutils import Vector
from kit.tiling import material
from textures import METAL,PLASTIC,SURFACE
M={}
CELLS=list(dict.fromkeys([*METAL,*PLASTIC,*SURFACE]))

def init():
    from io_scene_gltf2.blender.com.material_helpers import create_settings_group
    if bpy.data.node_groups.get('glTF Material Output') is None:create_settings_group('glTF Material Output')
    folder=Path('textures/ship')
    for key,name,alpha in [('Frame','PlayMetal',False),('Deck','PlayMetal',True),('Chain','PlayMetal',True),('Molded','PlayPlastic',False),('Site','PlaySurface',False)]:
        # The material name is independent of the canonical image stem.
        M[key]=material(name,folder,alpha=alpha,tint=True);M[key].name='Playground_'+key
        if alpha or key=='Molded':M[key].use_backface_culling=False
    M['Concrete']=material('Concrete',Path('../ground/textures/ship'))
    return M

def rect_uv(uv,rect,u,v,size=1024):
    a,b,c,d=rect;g=8/size
    uv.uv=(a+g+max(0,min(1,u))*(c-a-2*g),b+g+max(0,min(1,v))*(d-b-2*g))

def assign(ob,finish,family):
    if family=='Site' and finish in ('wood','rubber','zinc'):family='Frame'
    if family=='Site' and finish=='concrete':
        from kit.tiling import world_uv
        ob.data.materials.clear();ob.data.materials.append(M['Concrete'])
        world_uv(ob,3);return
    if family not in M:return
    from kit import model as G
    triangulator=ob.modifiers.new('Chart triangles before projection','TRIANGULATE');G.apply(ob)
    ob.data.materials.clear();ob.data.materials.append(M[family])
    for face in ob.data.polygons:face.material_index=0
    uv=ob.data.uv_layers.active
    ps=[ob.matrix_basis@v.co for v in ob.data.vertices];bb=[[f(p[k] for p in ps) for k in range(3)] for f in (min,max)]
    name=ob.name
    if family=='Molded':
        key='Clean'
        if 'chute' in name.lower() or 'barrel' in name.lower():key='Slide'
        elif 'hip roof' in name.lower():key='Chalk'
        elif 'bucket' in name.lower() or 'belt' in name.lower():key='Seat'
        elif 'molded infill' in name.lower():key='Initials'
        elif 'seam' in name.lower() or 'flange' in name.lower():key='Seam'
        rect=PLASTIC[key]
    elif family in ('Frame','Deck','Chain'):
        key={'zinc':'Zinc','rubber':'Rubber','wood':'Wood','deck':'Deck' if family=='Deck' else 'Black'}.get(finish,'Coat')
        if 'cast' in name.lower() or 'collar' in name.lower():key='Cast'
        if family=='Chain':key='Chain'
        rect=METAL[key]
    else:
        key='Fiber' if finish=='fiber' else 'EPDM';rect=SURFACE[key]
    ob['atlas_cell']=key
    chart=ob.data.attributes.get('ChartKind') or ob.data.attributes.new(name='ChartKind',type='INT',domain='FACE')
    for d in chart.data:d.value=CELLS.index(key)
    # Preserve explicit physical repeated chain coverage, remapped to its cell.
    if family=='Chain':
        for f in ob.data.polygons:
            for li in f.loop_indices:
                p=ps[ob.data.loops[li].vertex_index];top=bb[1][2];bottom=bb[0][2]
                u=(p[0]-bb[0][0])/max(1e-8,bb[1][0]-bb[0][0]) if bb[1][0]-bb[0][0]>.001 else (p[1]-bb[0][1])/max(1e-8,bb[1][1]-bb[0][1])
                tile=math.floor((top-f.center.z+1e-7)/.72)
                rect_uv(uv.data[li],rect,u,1-((top-p.z)/.72-tile))
        return
    for f in ob.data.polygons:
        # Slide charts follow the bed, allowing long longitudinal scratches.
        if family=='Deck' and abs(f.normal.z)>.9:
            rect=METAL['Deck']
            center=f.center+ob.location
            tx=math.floor((center.x+1e-6)/.4);ty=math.floor((center.y+1e-6)/.2)
            for li in f.loop_indices:
                p=ps[ob.data.loops[li].vertex_index]
                rect_uv(uv.data[li],rect,p.x/.4-tx,p.y/.2-ty)
            continue
        if family=='Deck':
            rect=METAL['Black'];chart.data[f.index].value=CELLS.index('Black')
        axes=(0,1) if family=='Molded' and key=='Slide' and abs((ob.matrix_basis.to_3x3()@f.normal).z)>.001 else sorted(range(3),key=lambda k:abs((ob.matrix_basis.to_3x3()@f.normal)[k]))[:2]
        for li in f.loop_indices:
            p=ps[ob.data.loops[li].vertex_index]
            u=(p[axes[0]]-bb[0][axes[0]])/max(1e-8,bb[1][axes[0]]-bb[0][axes[0]])
            v=(p[axes[1]]-bb[0][axes[1]])/max(1e-8,bb[1][axes[1]]-bb[0][axes[1]])
            rect_uv(uv.data[li],rect,u,v,2048 if family=='Site' else 1024)

def floor(ob,plan):
    """Placed 2m fiber/EPDM cells; source grid explicitly splits tile crossings."""
    uv=ob.data.uv_layers.active;tint=ob.data.color_attributes['Tint']
    for f in ob.data.polygons:
        center=f.center;tx=math.floor((center.x+1e-5)/2);ty=math.floor((center.y+1e-5)/2)
        if plan['inclusive']:
            key='WornEPDM' if any(((center.x-x)/.7)**2+((center.y-y)/1.1)**2<1.4 for x,y,w,h,d in plan['depressions_m']) else 'EPDM'
            # Two joined poured colors, with no coplanar overlay.
            inset=bool(ob.data.attributes['SurfaceInset'].data[f.index].value) if 'SurfaceInset' in ob.data.attributes else ((center.x-2)/5.9)**2+((center.y+1)/4.7)**2<1
            c=(.43,.21,.072,1) if inset else (.030,.17,.16,1)
        else:
            key='OldFiber' if plan['year']==1996 else 'Fiber'
            compact=min(.35,sum(.32*math.exp(-((center.x-x)/(w*.72))**2-((center.y-y)/(h*.82))**2) for x,y,w,h,d in plan['depressions_m']))
            c=(1-compact,1-compact*.93,1-compact*.82,1)
        for li in f.loop_indices:
            p=ob.data.vertices[ob.data.loops[li].vertex_index].co
            rect_uv(uv.data[li],SURFACE[key],p.x/2-tx,p.y/2-ty,2048)
            tint.data[li].color=c
