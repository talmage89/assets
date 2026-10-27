"""Rebuild the boxwood source look-dev checkpoint from a clean Blender scene."""
import argparse,sys,random,math,json
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Euler
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G,botany,foliage
from settings import *
from growth import generate,CENTER,BASAL_COUNT
from materials import foliage_material


def wood_material(images):
    mat=bpy.data.materials.new('Shrubs stems');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links
    bs=n.get('Principled BSDF');bs.name='SURFACE';n.get('Material Output').name='OUT';bs.inputs['Specular IOR Level'].default_value=.22
    for channel in ('BaseColor','Normal','ORM'):
        tex=n.new('ShaderNodeTexImage');tex.image=images[channel]
        if channel=='BaseColor':
            l.new(tex.outputs['Color'],bs.inputs['Base Color'])
            out=n.new('ShaderNodeMixRGB');out.name='OUT_base';out.inputs[0].default_value=0;l.new(tex.outputs['Color'],out.inputs[1])
        elif channel=='Normal':
            nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.55;l.new(tex.outputs[0],nm.inputs['Color']);l.new(nm.outputs[0],bs.inputs['Normal'])
        else:
            sep=n.new('ShaderNodeSeparateColor');l.new(tex.outputs[0],sep.inputs[0]);l.new(sep.outputs['Green'],bs.inputs['Roughness'])
            out=n.new('ShaderNodeMath');out.name='OUT_rough';out.operation='MULTIPLY';out.inputs[1].default_value=1;l.new(sep.outputs['Green'],out.inputs[0])
            out=n.new('ShaderNodeValue');out.name='OUT_metal';out.outputs[0].default_value=0
    return mat


def assign_uv(ob):
    uv=ob.data.uv_layers.new(name='BakeUV');u0,v0,u1,v1=WOOD_RECT
    for poly in ob.data.polygons:
        for li in poly.loop_indices:
            p=ob.data.vertices[ob.data.loops[li].vertex_index].co
            uv.data[li].uv=(u0+(u1-u0)*((math.atan2(p.y,p.x)/math.tau)%1),v0+(v1-v0)*min(.99,max(.01,p.z/.9)))


def assemble_wood(wood,stems,name,height):
    # Numerous slender stems emerge independently from a below-grade crown.
    # Clip/cap every actual sweep at grade; no elevated fused trunk pedestal.
    for stem,ob in zip(stems,wood):
        bm=bmesh.new();bm.from_mesh(ob.data);bm.verts.ensure_lookup_table()
        sides=stem['sides'];last=len(bm.verts)//sides-1
        for edge in bm.edges:
            a,b=[v.index for v in edge.verts]
            edge.seam=(a%sides==b%sides==0) or (a//sides==b//sides and a//sides in (0,last))
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,.002),plane_no=(0,0,1),clear_inner=True)
        for edge in bm.edges:
            if edge.is_boundary:edge.seam=True
        bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
        for v in bm.verts:v.co.z-=.002
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
        bm.to_mesh(ob.data);bm.free();ob.data.update()
    core=wood[0]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in wood:ob.select_set(True)
    bpy.context.view_layer.objects.active=core;bpy.ops.object.join();core.name=name
    assign_uv(core)
    part=core.data.attributes['GrowthPart'];owners={v:part.data[f.index].value for f in core.data.polygons for v in f.vertices}
    wind=[]
    for v in core.data.vertices:
        owner=owners[v.index]
        family=owner
        wind.append((min(1,max(0,v.co.z/height))*.38,.5 if stems[owner]['parent']>=0 else .25,stems[family]['phase'],0))
    botany.wind_attribute(core,wind)
    return core


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--species',choices=['boxwood','hydrangea'],default='boxwood');p.add_argument('--quality',default='game');p.add_argument('--wear',type=float,default=.35);p.add_argument('--seed',type=int,default=SEED);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['quality']=a.quality;sc['stage']='BOXWOOD SOURCE LOOKDEV / checkpoint'
    root=G.pivot('Hydrangea' if a.species=='hydrangea' else 'Boxwood',(0,0,0));root['static_root']=True
    images={c:bpy.data.images.load(str((ROOT/'shrubs/textures/analytic'/f'T_Shrubs_{c}.png').resolve())) for c in ('BaseColor','Normal','ORM')}
    for c in ('Normal','ORM'):images[c].colorspace_settings.name='Non-Color'
    if a.species=='hydrangea':
        from hydrangea import generate as generate_hydrangea
        bark=wood_material(images);wood,leaves,graph=generate_hydrangea(images,bark)
        core=assemble_wood(wood,graph['stems'],'Hydrangea wood',1.2)
        for ob in (core,leaves):ob.parent=root;ob['asset_set']='Hydrangea';ob['export_part']=ob.name
        graph['species']='Hydrangea';graph['seed']=815
        (a.out.parent/'growth.json').write_text(json.dumps(graph,indent=2))
        bpy.context.view_layer.update();bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
        for ob in (core,leaves):ob.data.calc_loop_triangles()
        print('HYDRANGEA',json.dumps({o.name:len(o.data.loop_triangles) for o in (core,leaves)}));return
    leaf=foliage_material(images)
    bark=wood_material(images);rng=random.Random(a.seed+7);stems,sites=generate(a.seed);wood=[]
    for i,s in enumerate(stems):
        ob=botany.sweep(f'Wood_{i:02}',s['points'],s['radii'],bark,sides=s['sides'],phase=s['phase'])
        part=ob.data.attributes.new(name='GrowthPart',type='INT',domain='FACE')
        for value in part.data:value.value=i
        wood.append(ob)
    core=assemble_wood(wood,stems,'Boxwood wood',.9)
    cards=botany.Cards();card_info=[]
    for site in sites:
        c=site['center'];d=site['direction'];s=stems[site['branch']];new=site['new'];old=site['old']
        tile=6 if new else (7 if old else rng.randrange(6));size=CARD_SIZE*(rng.uniform(.97,1.025) if not new else 1)
        if new:
            # Plane's V axis follows the shoot. Two crossed cards maintain its
            # silhouette while avoiding view-facing billboards.
            axis=d;u=axis.cross(Vector((0,0,1)))
            if u.length<.01:u=Vector((1,0,0))
            u.normalize();normals=[u.cross(axis).normalized(),u]
        else:
            rot=Euler((rng.random()*math.tau,rng.random()*math.tau,rng.random()*math.tau)).to_matrix()
            normals=[rot@Vector((1,0,0)),rot@Vector((0,1,0)),rot@Vector((0,0,1))]
        for ni,nn in enumerate(normals):
            c=site['center']-d*.045 if ni==2 else site['center']
            if nn.dot(d)<0:nn=-nn
            wind=(min(1,c.z/.9),1,s['phase'],rng.uniform(.6,.95))
            # Align each new-growth card's actual V axis with the shoot.
            seed=Vector((0,0,1)) if abs(nn.z)<.95 else Vector((1,0,0))
            bu=nn.cross(seed).normalized();bv=nn.cross(bu).normalized()
            roll=math.atan2(-d.dot(bu),d.dot(bv)) if new else rng.random()*math.tau
            cards.add(c,nn,roll,size,LEAF_RECTS[tile],CENTER,wind,.45,clump_center=c-d*.026,clump_blend=.82)
            card_info.append(dict(tile=tile,branch=site['branch'],new=new,old=old))
    leaves=cards.mesh('Boxwood leaf cards',leaf)
    for ob in (core,leaves):ob.parent=root;ob['asset_set']='Boxwood';ob['export_part']=ob.name
    bpy.context.view_layer.update()
    graph=dict(seed=a.seed,stems=[dict(s,points=[list(p) for p in s['points']]) for s in stems],cards=card_info,centers=cards.centers,widths=cards.widths,new_shoot_extensions_m=[s['extension'] for s in sites if s['new']])
    (a.out.parent/'growth.json').write_text(json.dumps(graph,indent=2))
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
    for ob in (core,leaves):ob.data.calc_loop_triangles()
    print('BOXWOOD',json.dumps({o.name:len(o.data.loop_triangles) for o in (core,leaves)}))

if __name__=='__main__':main()
