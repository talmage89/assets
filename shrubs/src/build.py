"""Rebuild the boxwood source look-dev checkpoint from a clean Blender scene."""
import argparse,sys,random,math,json
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Euler
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G,botany,foliage
from settings import *
from growth import generate,CENTER


def wood_material(images):
    mat=bpy.data.materials.new('Shrub stems and soil');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links
    bs=n.get('Principled BSDF');bs.inputs['Specular IOR Level'].default_value=.22
    for channel in ('BaseColor','Normal','ORM'):
        tex=n.new('ShaderNodeTexImage');tex.image=images[channel]
        if channel=='BaseColor':l.new(tex.outputs['Color'],bs.inputs['Base Color'])
        elif channel=='Normal':
            nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.55;l.new(tex.outputs[0],nm.inputs['Color']);l.new(nm.outputs[0],bs.inputs['Normal'])
        else:
            sep=n.new('ShaderNodeSeparateColor');l.new(tex.outputs[0],sep.inputs[0]);l.new(sep.outputs['Green'],bs.inputs['Roughness'])
    return mat


def assign_uv(ob):
    uv=ob.data.uv_layers.new(name='BakeUV');u0,v0,u1,v1=WOOD_RECT
    for poly in ob.data.polygons:
        for li in poly.loop_indices:
            p=ob.data.vertices[ob.data.loops[li].vertex_index].co
            uv.data[li].uv=(u0+(u1-u0)*((math.atan2(p.y,p.x)/math.tau)%1),v0+(v1-v0)*min(.99,max(.01,p.z/.9)))


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--quality',default='game');p.add_argument('--wear',type=float,default=.35);p.add_argument('--seed',type=int,default=SEED);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['quality']=a.quality;sc['stage']='BOXWOOD SOURCE LOOKDEV / checkpoint'
    root=G.pivot('Boxwood',(0,0,0));root['static_root']=True
    images={c:bpy.data.images.load(str((a.out.parent.parent/'textures/ship'/f'T_Shrubs_{c}.png').resolve())) for c in ('BaseColor','Normal','ORM')}
    for c in ('Normal','ORM'):images[c].colorspace_settings.name='Non-Color'
    leaf=foliage.material(images['BaseColor'],images['Normal'],images['ORM'],name='Boxwood glossy thin leaves',roughness=.50,specular=.40,transmission=.18,normal_strength=.90,back_multiplier=(1.42,1.24,1.48,1),back_saturation=.68,edge_fade=(.10,.26))
    bark=wood_material(images);rng=random.Random(a.seed+7);stems,sites=generate(a.seed);wood=[]
    for i,s in enumerate(stems):
        ob=botany.sweep(f'Wood_{i:02}',s['points'],s['radii'],bark,sides=s['sides'],phase=s['phase'])
        part=ob.data.attributes.new(name='GrowthPart',type='INT',domain='FACE')
        for value in part.data:value.value=i if i>=7 else 0
        wood.append(ob)
    # The coarse rooted core only is fused. Fine short ends remain low-sided
    # sweeps; the skin hides their embedded attachment caps, never floating ends.
    core=botany.fuse_stems(wood[:7],name='Rooted woody core',voxel_size=.003,triangle_target=350,connected_only=True)
    # Retain all seven rooted leaders: their feet now overlap as real stock.
    bm=bmesh.new();bm.from_mesh(core.data)
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,.002),plane_no=(0,0,1),clear_inner=True)
    bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
    for v in bm.verts:v.co.z-=.002
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    # At this centimeter scale the recalc heuristic can choose the inner
    # orientation after the grade cap. Measure signed volume, then orient out.
    if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
    assert all(e.is_manifold for e in bm.edges) and bm.calc_volume(signed=True)>0
    bm.to_mesh(core.data);bm.free();core.data.update()
    part=core.data.attributes.get('GrowthPart') or core.data.attributes.new(name='GrowthPart',type='INT',domain='FACE')
    for value in part.data:value.value=0
    wood=[core]+wood[7:]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in wood:ob.select_set(True)
    bpy.context.view_layer.objects.active=core;bpy.ops.object.join();core.name='Boxwood wood'
    assign_uv(core)
    part=core.data.attributes['GrowthPart'];owners={v:part.data[f.index].value for f in core.data.polygons for v in f.vertices}
    wind=[]
    for v in core.data.vertices:
        owner=owners[v.index]
        family=owner if owner>=7 else min(range(7),key=lambda i:min((v.co-p).length for p in stems[i]['points']))
        wind.append((min(1,max(0,v.co.z/.9))*.38,.5 if owner>=7 else .25,stems[family]['phase'],0))
    botany.wind_attribute(core,wind)
    # A small irregular on-grade soil/root plug, not a decorative circular base.
    n=17;verts=[(0,0,.008)];ring=[]
    for i in range(n):
        az=i*math.tau/n;r=rng.uniform(.105,.145);ring.append((r*math.cos(az),r*math.sin(az),0))
    verts+=ring
    soil=G.mesh('Small soil at stems',verts,[(0,1+i,1+(i+1)%n) for i in range(n)],bark);soil['allow_boundary']=True
    uv=soil.data.uv_layers.new(name='BakeUV')
    for loop in soil.data.loops:
        co=soil.data.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(.12+co.x*.5,.525+co.y*.11)
    botany.wind_attribute(soil,[(0,0,.27,0)]*len(soil.data.vertices))

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
        for nn in normals:
            if nn.dot(d)<0:nn=-nn
            wind=(min(1,c.z/.9),1,s['phase'],rng.uniform(.6,.95))
            # Align each new-growth card's actual V axis with the shoot.
            seed=Vector((0,0,1)) if abs(nn.z)<.95 else Vector((1,0,0))
            bu=nn.cross(seed).normalized();bv=nn.cross(bu).normalized()
            roll=math.atan2(-d.dot(bu),d.dot(bv)) if new else rng.random()*math.tau
            cards.add(c,nn,roll,size,LEAF_RECTS[tile],CENTER,wind,.72,clump_center=CENTER+d*.18,clump_blend=.24)
            card_info.append(dict(tile=tile,branch=site['branch'],new=new,old=old))
    leaves=cards.mesh('Boxwood leaf cards',leaf)
    for ob in (core,leaves,soil):ob.parent=root;ob['asset_set']='Boxwood';ob['export_part']=ob.name
    bpy.context.view_layer.update()
    graph=dict(seed=a.seed,stems=[dict(points=[list(p) for p in s['points']],radii=s['radii'],level=s['level'],parent=s['parent']) for s in stems],cards=card_info,centers=cards.centers,widths=cards.widths,new_shoot_extensions_m=[s['extension'] for s in sites if s['new']])
    (a.out.parent/'growth.json').write_text(json.dumps(graph,indent=2))
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
    for ob in (core,leaves,soil):ob.data.calc_loop_triangles()
    print('BOXWOOD',json.dumps({o.name:len(o.data.loop_triangles) for o in (core,leaves,soil)}))

if __name__=='__main__':main()
