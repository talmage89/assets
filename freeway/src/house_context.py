"""Distance shells from the house family's exact scripted envelope and holes.

The delivered weather grids are too disconnected for aggressive generic mesh
collapse. Rebuild their original skins and openings from the delivered plan,
reuse canonical materials and use simple distance fixtures. Nothing in the
house family is modified. This is an explicit local context LOD.
"""
import sys,json,importlib.util
from pathlib import Path
import bpy,bmesh
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
from kit import model as G
from kit.tiling import world_uv

def extract(parts):
    palette={};samples={}
    for ob in parts:
        colors=ob.data.color_attributes.active_color
        for face in ob.data.polygons:
            mat=ob.data.materials[face.material_index];name=mat.name.split('.')[0];palette[name]=mat
            if colors and colors.domain=='POINT':samples.setdefault(name,[]).extend(tuple(colors.data[i].color) for i in face.vertices)
        bm=bmesh.new();bm.from_mesh(ob.data)
        drop=[f for f in bm.faces if ob.data.materials[f.material_index].name.startswith(('HouseSiding','RanchRoof','RanchBrick','CapeBrick'))]
        if drop:bmesh.ops.delete(bm,geom=drop,context='FACES');bm.to_mesh(ob.data)
        bm.free()
    tints={key:tuple(np.median(value,axis=0)) for key,value in samples.items()}
    return palette,tints

def skins(root,metadata,palette,tints):
    sys.path.insert(0,str(ROOT/'houses/src'))
    spec=importlib.util.spec_from_file_location('freeway_native_house_builder',ROOT/'houses/src/build.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    houseplan=sys.modules['plan'];allowed=set(houseplan.Block.__dataclass_fields__)
    blocks=[houseplan.Block(**{k:v for k,v in row.items() if k in allowed}) for row in metadata['blocks']]
    class Adapter:
        plan={'blocks':blocks}
        def frame(self,block,face):
            o,t,n,length=houseplan.wall_frame(block,face)
            def xf(v):return Vector((o[0]+t[0]*v[0]+n[0]*v[1],o[1]+t[1]*v[0]+n[1]*v[1],v[2]))
            return xf,n,length
    out=[]
    def face(name,points,role,coverage,up=False):
        if len(points)<3:return
        points=list(map(Vector,points));normal=(points[1]-points[0]).cross(points[2]-points[0])
        if normal.length<1e-9:return
        if up and normal.z<0:points.reverse()
        expected=(points[1]-points[0]).cross(points[2]-points[0]).normalized()
        mat=palette[role];ob=G.mesh(name,points,[tuple(range(len(points)))],mat);ob.parent=root
        # The general closed-solid normal recalculator may reverse a lone
        # open skin. Restore its authored exterior before backface culling.
        if ob.data.polygons[0].normal.dot(expected)<0:
            bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
        ob['context_surface_kind']='roof' if up else 'wall';ob['context_expected_local_normal']=list(expected)
        n=ob.data.polygons[0].normal;axes=(0,1) if abs(n.z)>.5 else (0,2) if abs(n.y)>abs(n.x) else (1,2)
        world_uv(ob,coverage,axes=axes)
        tint=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        for value in tint.data:value.color=tints.get(role,(1,1,1,1))
        out.append(ob)
    for i,row in enumerate(metadata['roof_faces']):
        a,b,c=row['plane'];face('Native complete roof '+str(i),[(x,y,a*x+b*y+c) for x,y in row['polygon']],'RanchRoof',4.8768,True)
    for block in blocks:
        for side in ('front','back','left','right'):
            xf,n,length=Adapter().frame(block,side)
            for polygon,adjoining in mod.wall_sections(Adapter(),block,side):
                regions=[polygon]
                for hole in metadata['openings']:
                    if hole['block']!=block.name or hole['face']!=side:continue
                    constraints=[(1,0,-hole['u']+hole['w']/2),(-1,0,hole['u']+hole['w']/2),(0,1,-hole['z']),(0,-1,hole['z']+hole['h'])]
                    regions=[p for old in regions for p in houseplan.subtract(old,constraints)]
                veneer=metadata['spec']['cladding'].get(block.name,{}).get(side)=='veneer'
                brick=next((key for key in palette if key.startswith(('RanchBrick','CapeBrick'))),'HouseSiding')
                for poly in regions:
                    for role,region in ([(brick,houseplan.clip(poly,0,-1,.99)),('HouseSiding',houseplan.clip(poly,0,1,-.99))] if veneer else [('HouseSiding',poly)]):
                        if not region:continue
                        points=[xf((u,.012 if role=='HouseSiding' else .072,z)) for u,z in region]
                        # Match the original exterior-facing winding explicitly.
                        normal=(points[1]-points[0]).cross(points[2]-points[0])
                        if normal.dot(Vector((*n,0)))<0:points.reverse()
                        face('Native complete wall '+block.name+' '+side,points,role,2.4384)
    return out

def fixtures(root,metadata):
    """Distance window/door casings and real supports at native plan positions."""
    plan=sys.modules['plan'];allowed=set(plan.Block.__dataclass_fields__);out=[]
    blocks={row['name']:plan.Block(**{k:v for k,v in row.items() if k in allowed}) for row in metadata['blocks']}
    def mat(name,color,rough=.7):
        m=bpy.data.materials.new('Freeway context '+name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;return m
    trim=mat('painted casing',metadata['spec']['colors']['trim']);glass=mat('dark glazing',(.025,.038,.041),.22)
    shutter=mat('shutters',metadata['spec']['colors']['shutter']);door=mat('entry door',metadata['spec']['colors']['door']);concrete=mat('porch concrete',(.32,.32,.29),.9)
    def panel(name,xf,normal,uv,material,depth=.045):
        pts=[xf((u,depth,z)) for u,z in uv]
        if (pts[1]-pts[0]).cross(pts[2]-pts[0]).dot(Vector((*normal,0)))<0:pts.reverse()
        ob=G.mesh(name,pts,[tuple(range(len(pts)))],material);ob.parent=root;world_uv(ob,1.,axes=(0,2) if normal[1] else (1,2));out.append(ob)
    for block in blocks.values():
        height=max(.02,block.floor-.205)
        ob=G.box('Native foundation envelope',(block.cx,block.cy,height/2),(block.width,block.depth,height),concrete,0);ob.parent=root;world_uv(ob,2.4384);out.append(ob)
    for hole in metadata['openings']:
        block=blocks[hole['block']];o,t,n,length=plan.wall_frame(block,hole['face'])
        def xf(v):return Vector((o[0]+t[0]*v[0]+n[0]*v[1],o[1]+t[1]*v[0]+n[1]*v[1],v[2]))
        u0=hole['u']-hole['w']/2;u1=u0+hole['w'];z0=hole['z'];z1=z0+hole['h'];c=.07
        kind=hole['kind'];pane=glass if kind in ('window','slider') else door
        panel('Native plan '+kind,xf,n,[(u0,z0),(u1,z0),(u1,z1),(u0,z1)],pane,.075)
        for a,b,c0,c1 in [(u0-c,u0,z0-c,z1+c),(u1,u1+c,z0-c,z1+c),(u0,u1,z0-c,z0),(u0,u1,z1,z1+c)]:panel('Distance casing',xf,n,[(a,c0),(b,c0),(b,c1),(a,c1)],trim,.09)
        if kind=='window':
            z=z0+hole['h']*.52;panel('Window meeting rail',xf,n,[(u0,z-.018),(u1,z-.018),(u1,z+.018),(u0,z+.018)],trim,.092)
            if hole['w']>1.3:
                u=hole['u'];panel('Window mullion',xf,n,[(u-.02,z0),(u+.02,z0),(u+.02,z1),(u-.02,z1)],trim,.092)
            if hole.get('shutters'):
                for a,b in [(u0-.32,u0-.08),(u1+.08,u1+.32)]:panel('Native shutter envelope',xf,n,[(a,z0),(b,z0),(b,z1),(a,z1)],shutter,.075)
    porch=metadata.get('porch')
    if porch:
        p=plan.Block(**{k:v for k,v in porch.items() if k in allowed});floor=p.floor
        def box(name,point,size,material):
            ob=G.box(name,point,size,material,0);ob.parent=root;world_uv(ob,1.);out.append(ob)
        box('Native porch slab',(p.cx,p.cy,floor-.10),(p.width,p.depth,.20),concrete)
        for x in (p.x0+.12,p.x1-.12):box('Porch bearing post',(x,p.y0+.12,(floor+p.eave-.15)/2),(.12,.12,p.eave-.15-floor),trim)
        steps=max(1,round(floor/.1778))
        for j in range(steps):box('Porch step',(p.cx,p.y0-.28*(j+.5),floor*(steps-j)/steps/2),(min(p.width,1.4),.28,floor*(steps-j)/steps),concrete)
    # Horizontal eave fascia only; internal roof intersections stay roofing.
    for row in metadata['roof_faces']:
        a,b,c=row['plane'];pts=[Vector((x,y,a*x+b*y+c)) for x,y in row['polygon']]
        for p,q in zip(pts,pts[1:]+pts[:1]):
            if abs(p.z-q.z)>.002 or (p-q).length<.2:continue
            ob=G.cylinder('Horizontal eave trim',p-Vector((0,0,.07)),q-Vector((0,0,.07)),.07,trim,4);ob.parent=root;world_uv(ob,1.);out.append(ob)
    return out
