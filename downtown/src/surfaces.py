"""Shared material and authored strip-chart contract, stock glTF only."""
import json,math
from pathlib import Path
from mathutils import Vector
from kit import tiling

MASONRY_COVERAGE=4.8768
BRICK_TILE_H=1.2192
GUARD=8/2048


def palette(sheet):
    import bpy
    folder=Path('textures/ship')
    if not (folder/'T_DowntownMasonry_BaseColor.png').exists():return None
    masonry=tiling.material('DowntownMasonry',folder,tint=True)
    mineral=tiling.material('DowntownMineralRoof',folder,tint=True)
    finish=tiling.material('DowntownFinish',folder,tint=True);finish.use_backface_culling=False
    glass=bpy.data.materials.new('Downtown_Glass');glass.use_nodes=True;glass['tiling_vertex_tint']=False
    p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.96,.98,.97,1);p.inputs['Roughness'].default_value=.014;p.inputs['IOR'].default_value=1.50;p.inputs['Transmission Weight'].default_value=1
    graphics=bpy.data.materials.new('Downtown_Graphics');graphics.use_nodes=True;graphics['tiling_vertex_tint']=False
    p=graphics.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.79
    n=graphics.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(sheet.resolve()),check_existing=True)
    graphics.node_tree.links.new(n.outputs['Color'],p.inputs['Base Color']);graphics.node_tree.links.new(n.outputs['Alpha'],p.inputs['Alpha']);graphics.surface_render_method='DITHERED'
    interior=bpy.data.materials.new('Downtown_Interior');interior.use_nodes=True;interior['tiling_vertex_tint']=True
    p=interior.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.85
    n=interior.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str((folder/'T_DowntownInterior_BaseColor.png').resolve()),check_existing=True)
    vc=interior.node_tree.nodes.new('ShaderNodeVertexColor');vc.layer_name='Tint'
    mix=interior.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
    l=interior.node_tree.links;l.new(n.outputs['Color'],mix.inputs[1]);l.new(vc.outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
    e=interior.node_tree.nodes.new('ShaderNodeTexImage');e.image=n.image
    u=interior.node_tree.nodes.new('ShaderNodeUVMap');u.uv_map='LightUV';l.new(u.outputs[0],e.inputs['Vector']);l.new(e.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=.13
    return [masonry,mineral,finish,mineral,glass,graphics,interior]


def strip_uv(points,strip,count,coverage=4.,guard=8/2048):
    # U repeats continuously. V stays in the guarded strip even on tiny parts.
    normal=(Vector(points[1])-Vector(points[0])).cross(Vector(points[2])-Vector(points[0]))
    axes=sorted(range(3),key=lambda k:abs(normal[k]))[:2]
    if 2 in axes:axes=[next(k for k in axes if k!=2),2]
    a,b=axes;lo=min(p[b] for p in points);hi=max(p[b] for p in points)
    length=max(hi-lo,.00001);span=1/count-2*guard
    return [(p[a]/coverage,strip/count+guard+(p[b]-lo)/length*span) for p in points]


def classify(role,color,surface):
    if role=='Roof':return 2,4
    if role=='Mineral':return (1 if color==(.32,.305,.265) else 3 if max(color)-min(color)<.09 else 0),4
    if surface in ('canvas','curtain'):return 4,8
    if surface=='blind':return 7,8
    if surface in ('frieze','leaf'):return 6,8
    if role=='Finish':
        if max(abs(a-b) for a,b in zip(color,(.38,.34,.23)))<.001:return 3,8
        if max(abs(a-b) for a,b in zip(color,(.13,.19,.15)))<.001:return 0,8
        if min(color)>.35:return 5,8
        if max(color)-min(color)<.07 and max(color)>.20:return 2,8
        if color[0]>color[2]*1.55 and max(color)<.4:return 0,8
        return 1,8
    return 0,1


def clip_height(poly,z,above,axis=2):
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        aa=a[axis]>=z-1e-8 if above else a[axis]<=z+1e-8
        bb=b[axis]>=z-1e-8 if above else b[axis]<=z+1e-8
        if aa:out.append(a)
        if aa!=bb:
            t=(z-a[axis])/(b[axis]-a[axis]);out.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(3)))
    clean=[]
    for v in out:
        if not clean or math.dist(v,clean[-1])>1e-7:clean.append(v)
    if len(clean)>1 and math.dist(clean[0],clean[-1])<1e-7:clean.pop()
    return clean


def masonry_faces(points,variant,painted=False,tile_height=BRICK_TILE_H,coverage=MASONRY_COVERAGE,ground_grid=True,upper_grid=False,vertical_cuts=()):
    lo=min(p[2] for p in points);hi=max(p[2] for p in points)
    normal=(Vector(points[1])-Vector(points[0])).cross(Vector(points[2])-Vector(points[0]))
    axis=0 if abs(normal[1])>abs(normal[0]) else 1
    if hi-lo<1e-5 or abs(normal.z)>.9999*normal.length:
        # Horizontal bearing/return charts: deliberately tiled within region.
        return [(points,strip_uv(points,variant,4,coverage))]
    out=[]
    for k in range(math.floor(lo/tile_height),math.floor((hi-1e-7)/tile_height)+1):
        poly=clip_height(clip_height(points,k*tile_height,True),(k+1)*tile_height,False)
        if len(poly)<3:continue
        pieces=[poly]
        if ground_grid and (k==0 or upper_grid) and max(p[axis] for p in poly)-min(p[axis] for p in poly)>.65:
            pieces=[];a=min(p[axis] for p in poly);b=max(p[axis] for p in poly)
            for j in range(math.floor(a/.65),math.floor((b-1e-7)/.65)+1):
                chunk=clip_height(clip_height(poly,j*.65,True,axis),(j+1)*.65,False,axis)
                if len(chunk)>=3:pieces.append(chunk)
        for cut in vertical_cuts:
            divided=[]
            for piece in pieces:
                if min(p[axis] for p in piece)+1e-7<cut<max(p[axis] for p in piece)-1e-7:
                    divided.extend([clip_height(piece,cut,True,axis),clip_height(piece,cut,False,axis)])
                else:divided.append(piece)
            pieces=[q for q in divided if len(q)>=3]
        for poly in pieces:
            uv=[(p[axis]/coverage,variant/4+GUARD+(p[2]/tile_height-k)*(.25-2*GUARD)) for p in poly]
            out.append((poly,uv))
    return out
