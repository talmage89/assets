"""Existing library manufacture maps; placement-owned causal vertex tint."""
import importlib.util,math
from pathlib import Path
import bpy
from mathutils import Vector
from kit import tiling
import geometry as G

spec=importlib.util.spec_from_file_location('_church_downtown_uv',G.ROOT/'downtown/src/surfaces.py')
D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
ROLES={}


def paint_material():
    if 'paint' in G.MATS:return
    ma=tiling.material('GroundTrim',G.ROOT/'ground/textures/ship',alpha=True)
    ma.name='Church_Ground_markings';ma.use_backface_culling=False;G.MATS['paint']=ma


def palette():
    # Initialize Blender's complete importer/exporter AO group before tiling.
    from io_scene_gltf2.blender.com.material_helpers import create_settings_group
    if not bpy.data.node_groups.get('glTF Material Output'):create_settings_group('glTF Material Output')
    specs={'brick':('DowntownMasonry','downtown/textures/ship'),
           'siding':('HouseSiding','houses/textures/ship'),
           'stone':('DowntownMineralRoof','downtown/textures/ship'),
           'iron':('DowntownFinish','downtown/textures/ship'),
           'shingle':('RanchRoof','houses/textures/ranch-ship'),
           'concrete':('Concrete','ground/textures/ship'),
           'asphalt':('Asphalt','ground/textures/ship'),
           'lawn':('Lawn','ground/textures/ship'),
           'timber':('ChurchCraft','church/textures/ship'),
           'slate':('ChurchCraft','church/textures/ship'),
           'bronze':('ChurchCraft','church/textures/ship')}
    for role,(name,folder) in specs.items():
        ma=tiling.material(name,G.ROOT/folder,tint=True);ma.name='Church_'+role
        G.MATS[role]=ma
    for role,color,rough,metal in [('glass',(.91,.93,.86),.10,0),('black',(.006,.008,.009),.85,0)]:
        ma=bpy.data.materials.new('Church_'+role);ma.use_nodes=True;ma['tiling_vertex_tint']=False
        p=ma.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
        if role=='glass':p.inputs['Transmission Weight'].default_value=.94;p.inputs['IOR'].default_value=1.49
        ma.use_backface_culling=False;G.MATS[role]=ma
    for role,file,emit in [('stained','T_ChurchGlass_BaseColor.png',.0),('letters','T_ChurchLetters_BaseColor.png',0)]:
        ma=tiling.material('ChurchGlass',G.ROOT/'church/textures/ship') if role=='stained' else bpy.data.materials.new('Church_'+role)
        ma.name='Church_'+role;ma.use_nodes=True;ma['tiling_vertex_tint']=False
        ns,ls=ma.node_tree.nodes,ma.node_tree.links;p=ns.get('Principled BSDF')
        tx=ns.new('ShaderNodeTexImage');tx.image=bpy.data.images.load(str((G.ROOT/'church/textures/ship'/file).resolve()),check_existing=True)
        ls.new(tx.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.35 if role=='stained' else .65
        if role=='stained':ls.new(tx.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=emit
        else:
            ls.new(tx.outputs['Alpha'],p.inputs['Alpha']);ma.surface_render_method='DITHERED';ma.use_backface_culling=False
        ma.use_backface_culling=False;G.MATS[role]=ma


def charts(points,role):
    if role=='brick':return D.masonry_faces(points,0,upper_grid=True)
    normal=(Vector(points[1])-Vector(points[0])).cross(Vector(points[2])-Vector(points[0]))
    axis=max(range(3),key=lambda k:abs(normal[k]));axes=[(1,2),(0,2),(0,1)][axis]
    if role in ('stone','iron'):
        return [(points,D.strip_uv(points,0 if role=='stone' else 1,4 if role=='stone' else 8,coverage=2))]
    if role in ('timber','slate','bronze'):
        idx={'timber':0,'slate':1,'bronze':2}[role];a,b=axes;lo=min(p[b] for p in points);hi=max(p[b] for p in points)
        if role=='slate' and hi-lo>1e-6:
            # 406mm slate width / 196mm visible gauge. Split at atlas tile
            # boundaries instead of stretching fourteen courses over a roof.
            nz=abs(normal.normalized().z);height=2.7432*(max(.1,1-nz*nz)**.5 if b==2 else 1)
            out=[]
            for k in range(math.floor(lo/height),math.floor((hi-1e-7)/height)+1):
                poly=D.clip_height(D.clip_height(points,k*height,True,b),(k+1)*height,False,b)
                if len(poly)<3:continue
                out.append((poly,[(p[a]/4.8768,1/3+.008+(p[b]/height-k)*(1/3-.016)) for p in poly]))
            return out
        return [(points,[(p[a]/2,idx/3+.008+(p[b]-lo)/max(hi-lo,1e-7)*(.333- .016)) for p in points])]
    cov={'concrete':3.048,'asphalt':6.096,'lawn':6.096,'shingle':4.8768,'siding':1.2192}.get(role,1)
    return [(points,[(p[axes[0]]/cov,p[axes[1]]/cov) for p in points])]


def tint(p,role,col,props):
    x,y,z=p;f=1.
    if role=='iron':col=tuple(v*.037 for v in col)
    if role=='stone':col=tuple(v*.38 for v in col)
    if role=='timber' and props.get('door'):col=tuple(v*.15 for v in col)
    if role=='brick':
        floor=props.get('floor',.6096);zz=max(0,z-floor)
        reach=.55+.14*math.sin(x*4.9+y*3.2)+.06*math.sin(x*19+y*11)
        damp=.36*max(0,1-zz/reach)
        # Sill-end leaks, flashing runoff and base moisture follow construction.
        tracks=sum(math.exp(-((x-s)/.13)**2) for s in props.get('drips',[]))
        runoff=min(.20,tracks*.19*math.exp(-max(0,props.get('drip_z',6)-z)/2))
        f-=damp+runoff
        patch=props.get('patch',False)
        if patch:col=tuple(a*b for a,b in zip(col,(1.12,1.04,.91)))
    if role=='asphalt':col=tuple(v*.62 for v in col)
    if role=='lawn':
        # Broad coherent mowing/exposure changes, with the existing fine turf.
        f=.70+.05*math.sin(x*.75+y*.06)+.035*math.sin(y*1.4)
    return tuple(max(0,min(1.8,c*f)) for c in col)
