"""Split delivery through the family's shared PBR and RGBA8 weather pipeline."""
import argparse
import json
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import tiling
from cape_deliver import bake_weather,aged_orm,discard_loose,weld_uv_slivers
from cape_masonry import dielectric
from lookdev import materials
from ranch_uv import resolve,partitions
from deliver import externalize
from glb_budget import compact,read

ROOT=Path('build/split/delivery')


def write_changed(path,payload):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists() or path.read_bytes()!=payload:path.write_bytes(payload)


def freeze_folded_surface(ob):
    """Retain the source tessellation of folded thin eave returns exactly."""
    me=ob.data;me.calc_loop_triangles();tris=list(me.loop_triangles)
    mesh=bpy.data.meshes.new(me.name+'_Frozen');mesh.from_pydata([v.co for v in me.vertices],[],[t.vertices for t in tris]);mesh.update()
    for mat in me.materials:mesh.materials.append(mat)
    color=mesh.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for i,c in enumerate(me.color_attributes['Tint'].data):color.data[i].color=c.color
    # At the pre-bake call these coordinate/mask fields still feed the
    # procedural source. Vertex indices are unchanged by this tessellation.
    for a in me.attributes:
        if a.domain!='POINT' or not a.name.startswith(('Cape','Split')):continue
        prop={'FLOAT':'value','FLOAT_VECTOR':'vector','INT':'value','BOOLEAN':'value'}.get(a.data_type)
        if prop is None:continue
        dst=mesh.attributes.new(name=a.name,type=a.data_type,domain='POINT')
        for old,new in zip(a.data,dst.data):setattr(new,prop,getattr(old,prop))
    uv=mesh.uv_layers.new(name='UVMap');normals=[]
    for p,t in zip(mesh.polygons,tris):
        p.material_index=t.material_index;p.use_smooth=True
        for new_li,old_li in zip(p.loop_indices,t.loops):uv.data[new_li].uv=me.uv_layers.active.data[old_li].uv;normals.append(me.corner_normals[old_li].vector[:])
    mesh.normals_split_custom_set(normals);ob.data=mesh


def condition_roof_colors(objects,material):
    """Use COLOR_0's full range without changing the physical roof color.

    Dark roof factors waste most of RGBA8's precision. Move a common scalar
    into the standard glTF material factor and scale only its vertex colors
    inversely. Split material corners so neighboring trim cannot change.
    """
    import math
    largest=max(c for ob in objects for p in ob.data.polygons if ob.data.materials[p.material_index]==material for i in p.vertices for c in ob.data.color_attributes['Tint'].data[i].color[:3])
    factor=max(1/255,math.ceil(largest*255)/255);assert factor<=1,(largest,factor)
    for ob in objects:
        me=ob.data
        if not any(me.materials[p.material_index]==material for p in me.polygons):continue
        verts=[];faces=[];colors=[];uvs=[];normals=[];slots=[]
        for p in me.polygons:
            start=len(verts);roof=me.materials[p.material_index]==material
            for li in p.loop_indices:
                vi=me.loops[li].vertex_index;verts.append(me.vertices[vi].co[:]);c=me.color_attributes['Tint'].data[vi].color
                colors.append((*(q/factor if roof else q for q in c[:3]),1));uvs.append(me.uv_layers.active.data[li].uv[:]);normals.append(me.corner_normals[li].vector[:])
            faces.append(tuple(range(start,len(verts))));slots.append(p.material_index)
        mesh=bpy.data.meshes.new(me.name+'_ColorPrecision');mesh.from_pydata(verts,[],faces);mesh.update()
        for m in me.materials:mesh.materials.append(m)
        attr=mesh.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');uv=mesh.uv_layers.new(name='UVMap')
        for i,c in enumerate(colors):attr.data[i].color=c
        for li in range(len(mesh.loops)):uv.data[li].uv=uvs[li]
        for p,slot in zip(mesh.polygons,slots):p.material_index=slot;p.use_smooth=True
        mesh.normals_split_custom_set(normals);ob.data=mesh
    nt=material.node_tree;p=nt.nodes.get('Principled BSDF');base=p.inputs['Base Color'].links[0].from_socket
    mix=nt.nodes.new('ShaderNodeMix');mix.data_type='RGBA';mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[7].default_value=(factor,factor,factor,1)
    nt.links.new(base,mix.inputs[6]);nt.links.new(mix.outputs[2],p.inputs['Base Color'])
    return dict(material_factor=factor,vertex_scale=1/factor,physical_color_unchanged=True,physical_quantization_bound=factor*.5/255)


def veneer_charts(ob,seed):
    """Resolve stone, coping and factory brick into guarded ordinary UV0."""
    from split_atlas import rect
    import numpy as np
    from mathutils.geometry import tessellate_polygon
    me=ob.data;me.calc_loop_triangles();uv=me.uv_layers.active
    old_normals=[n.vector.copy() for n in me.corner_normals]
    verts=[];faces=[];coords=[];colors=[];normals=[];slots=[]
    for tri in me.loop_triangles:
        ids=list(tri.vertices);lis=list(tri.loops);name=me.materials[tri.material_index].name.split('.')[0];veneer=name in ('SplitStone','SplitBrick');stone=name=='SplitStone'
        coping=stone and ob.get('component') in ('opening_masonry','veneer_cap')
        tc=[np.array(uv.data[i].uv,dtype='float64') for i in lis]
        d=tc[1]-tc[0];e=tc[2]-tc[0]
        if coping and abs(d[0]*e[1]-d[1]*e[0])<1e-14:
            # The source samples a constant coping-row center. Give the
            # physical cross section a nondegenerate chart within that face.
            pts=[ob.matrix_world@me.vertices[i].co for i in ids]
            axis=max(range(3),key=lambda k:abs(tri.normal[k]));axes=[k for k in range(3) if k!=axis]
            axes.sort(key=lambda k:max(p[k] for p in pts)-min(p[k] for p in pts),reverse=True)
            tc=[np.array((p[axes[0]]/.6096,.2+(p[axes[1]]%1.3716)/1.3716*.6)) for p in pts]
        poly=[(tc[i],np.eye(3)[i]) for i in range(3)]
        pieces=[(0,0,poly)] if not veneer else [(0,row,p) for row,p in partitions(poly,1,1)]
        region=rect('coping' if coping else 'stone' if stone else str(seed)) if veneer else None
        for col,row,poly in pieces:
            start=len(verts)
            for t,w in poly:
                verts.append(sum((me.vertices[ids[k]].co*w[k] for k in range(3)),Vector()))
                coords.append((t[0],region[1]+(t[1]-row)*(region[3]-region[1])) if veneer else t)
                colors.append(tuple(sum(me.color_attributes['Tint'].data[ids[k]].color[c]*w[k] for k in range(3)) for c in range(4)))
                normals.append(sum((old_normals[lis[k]]*w[k] for k in range(3)),Vector()).normalized())
            for k in range(1,len(poly)-1):faces.append((start,start+k,start+k+1));slots.append(tri.material_index)
    mesh=bpy.data.meshes.new(me.name+'_StoneCharts');mesh.from_pydata(verts,[],faces);mesh.update()
    for mat in me.materials:mesh.materials.append(mat)
    layer=mesh.uv_layers.new(name='UVMap');color=mesh.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for i,c in enumerate(colors):color.data[i].color=c
    for p,slot in zip(mesh.polygons,slots):
        p.material_index=slot;p.use_smooth=True
        for li in p.loop_indices:layer.data[li].uv=coords[mesh.loops[li].vertex_index]
    mesh.normals_split_custom_set([normals[l.vertex_index] for l in mesh.loops]);ob.data=mesh


def sample_wear(objects,meta):
    """Add planar sampling only where a meter-scale causal field needs it."""
    import numpy as np
    rows={}
    for ob in objects:
        component=ob.get('component');cuts=[]
        if component=='driveway':
            d=meta['driveway']
            step=.85 if meta['seed']==56 else .60
            cuts.extend((0,float(q)) for q in np.arange(d['x']-d['width']/2+.25,d['x']+d['width']/2,step))
            cuts.extend((1,float(q)) for q in np.arange(d['front']+.25,d['back'],step))
            if meta['seed']!=56:
                # Narrow source control-joint cracks need actual samples on
                # both lips; a coarse color grid would average them away.
                for q in np.arange(d['front']+2.4,d['back'],2.4):
                    cuts.extend((1,float(q+offset)) for offset in (-.012,0,.012))
        elif component=='garage_panel':
            d=next(o for o in meta['openings'] if o['kind']=='garage')
            cuts.extend((2,d['z']+q) for q in (.08,.30))
        elif component=='eave_rake_soffit' and meta['seed']==51:
            world=[ob.matrix_world@v.co for v in ob.data.vertices]
            lo=[min(p[k] for p in world) for k in range(3)];hi=[max(p[k] for p in world) for k in range(3)]
            axis=max((0,1),key=lambda k:hi[k]-lo[k])
            for drain in meta['drains']:
                for q in drain['gutter']:
                    if all(lo[k]-.5<=q[k]<=hi[k]+.5 for k in range(3)):
                        cuts.extend((axis,q[axis]+offset) for offset in (-.20,-.06,.06,.20) if lo[axis]<q[axis]+offset<hi[axis])
        if not cuts:continue
        me=ob.data;me.calc_loop_triangles();before=len(me.loop_triangles)
        stored=me.attributes.new(name='_WearNormals',type='FLOAT_VECTOR',domain='CORNER')
        stored.data.foreach_set('vector',np.array([n.vector[:] for n in me.corner_normals],dtype='float32').ravel())
        bm=bmesh.new();bm.from_mesh(me)
        # Freeze the source's actual tessellation before cutting. Some folded
        # miter returns are nonplanar ngons; retriangulating those after a cut
        # would silently change their surface by millimeters.
        bmesh.ops.triangulate(bm,faces=list(bm.faces))
        inv=ob.matrix_world.inverted()
        for axis,q in sorted(set(cuts)):
            point=Vector((0,0,0));point[axis]=q;normal=Vector((0,0,0));normal[axis]=1
            bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],dist=1e-7,plane_co=inv@point,plane_no=ob.matrix_world.to_3x3().transposed()@normal,clear_inner=False,clear_outer=False)
        bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
        me.normals_split_custom_set([v.vector.normalized() for v in me.attributes['_WearNormals'].data]);me.attributes.remove(me.attributes['_WearNormals'])
        me.color_attributes.active_color=me.color_attributes['Tint'];me.calc_loop_triangles()
        rows[ob.name]=dict(before=before,after=len(me.loop_triangles),cuts=len(cuts))
    return rows


def export_house(seed):
    folder=Path('export/textures');folder.mkdir(parents=True,exist_ok=True)
    for channel in ('BaseColor','Normal'):
        path=Path('textures/split-ship')/f'T_SplitStone_{channel}.png';dest=folder/path.name
        payload=path.read_bytes()
        if not dest.exists() or dest.read_bytes()!=payload:dest.write_bytes(payload)
    source=Path(f'build/split/house-{seed}.blend');bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
    meta=json.loads(source.with_suffix('.json').read_text());skin=meta['spec']['siding']
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]
    for ob in objects:
        if ob.get('component')=='eave_rake_soffit':freeze_folded_surface(ob)
    assignments={o.name:[m.name.split('.')[0] for m in o.data.materials] for o in objects}
    # Unit kiln color belongs to manufacture, never to sparse weather samples.
    if meta['spec']['veneer']=='brick':
        for ob in objects:
            for poly in ob.data.polygons:
                if ob.data.materials[poly.material_index].name.split('.')[0]=='SplitBrick':
                    for vi in poly.vertices:ob.data.color_attributes['Tint'].data[vi].color=(1,1,1,1)
        for mat in {m for ob in objects for m in ob.data.materials if m.name.split('.')[0]=='SplitBrick'}:
            channel=mat.node_tree.nodes.get('OUT_split_brick_factor');assert channel is not None,'Rebuild source after factor separation'
            white=mat.node_tree.nodes.new('ShaderNodeRGB');white.outputs[0].default_value=(1,1,1,1)
            for link in list(channel.outputs[0].links):mat.node_tree.links.new(white.outputs[0],link.to_socket)
    meta['wear_sampling']=sample_wear(objects,meta)
    meta['weather_bake']=bake_weather(objects,fine_mix=.12)
    meta['weather_bake']['retained_source_fine_granule_field']=.12
    # Restore the accepted small parking/overflow masks' street-scale contrast
    # after vertex averaging. Their positions still come from real causes.
    import math
    d=meta['driveway']
    for ob in objects:
        component=ob.get('component')
        if component not in ('driveway','eave_rake_soffit'):continue
        colors=ob.data.color_attributes['Tint']
        for v in ob.data.vertices:
            p=ob.matrix_world@v.co;factor=1.
            if component=='driveway':
                dx=p.x-d['x']-.14;dy=p.y-(d['back']-3.4)
                oil=max(0,1-abs(dx)/.65)*max(0,1-abs(dy)/1.15)
                tire=max(0,1-abs(abs(p.x-d['x'])-.76)/.36)*max(0,1-abs(p.y-(d['back']-3.0))/3.4)
                factor=1-.45*oil-.16*tire
            elif component=='eave_rake_soffit':
                for drain in meta['drains']:
                    q=Vector(drain['centerline'][0]);q.z+=.183;r=math.hypot(p.x-q.x,p.y-q.y)
                    if -.05<q.z-p.z<.50:factor=min(factor,1-.43*max(0,1-r/.48))
            c=colors.data[v.index];c.color=(*(q*factor for q in c.color[:3]),1)
    wood=bpy.data.objects.get('Aged_GrayWoodAtSillNoses')
    if wood:
        for c in wood.data.color_attributes['Tint'].data:c.color=(*(q*.65 for q in c.color[:3]),1)
    meta['wear_filter_transfer']=dict(engine_drips=.45,tire_film=.16,low_gutter_ends=.43,wet_wood=.65,scope='Bounded, cause-local compensation of vertex-filtered wear; no whole-surface overlay or geometry changes')
    if skin=='aluminum':
        for ob in objects:
            changed=set()
            for poly in ob.data.polygons:
                if ob.data.materials[poly.material_index].name.split('.')[0]!='HouseSiding':continue
                for vi in poly.vertices:
                    if vi in changed:continue
                    c=ob.data.color_attributes['Tint'].data[vi];c.color=(*(min(1,q*1.12) for q in c.color[:3]),1);changed.add(vi)
        meta['aluminum_filter_transfer']=1.12
    for ob in objects:
        if ob.get('component')!='roof':continue
        import numpy as np
        attr=ob.data.color_attributes['Tint'];a=np.array([q.color[:3] for q in attr.data]);y=a@np.array((.2126,.7152,.0722));pivot=float(np.median(y))
        target=np.maximum(pivot+2.0*(y-pivot),.001);factor=np.clip(target/np.maximum(y,1e-8),.75,1.30)*np.where(y>pivot,1.09,.98)*.945
        for q,f in zip(attr.data,factor):q.color=(*(min(1,c*f) for c in q.color[:3]),1)
    meta['roof_filter_transfer']=dict(contrast=2.0,pivot='per-plane median',factor_bounds=[.694575,1.339065],above_median_gain=1.09,below_median_gain=.98,gain=.945)
    original=materials(Path('textures/ship'));aged_orm(original['Trim'])
    if skin in ('wood','aluminum'):aged_orm(original['Siding'],constant=True)
    if skin in ('battens','grooved'):original['Siding']=original['Trim'].copy();original['Siding'].name='SplitPaintedBoards'
    else:next(n for n in original['Siding'].node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.15
    original['Shingles']=tiling.material('RanchRoof',Path('textures/ranch-ship'),tint=True)
    # The accepted source uses uniform .93 roughness. Retain that response
    # to within .005 after filtering; the canonical ORM remains the AO input.
    roof_p=original['Shingles'].node_tree.nodes.get('Principled BSDF')
    for key,value in (('Roughness',.925),('Metallic',0.)):
        for link in list(roof_p.inputs[key].links):original['Shingles'].node_tree.links.remove(link)
        roof_p.inputs[key].default_value=value
    original['Veneer']=dielectric('SplitStone',Path('textures/split-ship'),roughness=.91)
    if meta['spec']['veneer']=='stone':next(n for n in original['Veneer'].node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.85
    # Normal manufacture keeps its original independent density. The normal
    # texture's ordinary glTF transform reverses color-band V addressing.
    from split_atlas import rect
    nt=original['Veneer'].node_tree
    normal_image=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and n.image and '_Normal' in n.image.name)
    r=rect(str(seed)) if meta['spec']['veneer']=='brick' else None
    if r:
        normal_image.image=bpy.data.images.load(str(Path('textures/cape-ship/T_CapeBrick_Normal.png').resolve()),check_existing=True);normal_image.image.colorspace_settings.name='Non-Color'
    uv=nt.nodes.new('ShaderNodeTexCoord');mapping=nt.nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value=(1,1/(r[3]-r[1]) if r else 2,1)
    mapping.inputs['Location'].default_value=(0,-r[1]/(r[3]-r[1]) if r else 0,0)
    nt.links.new(uv.outputs['UV'],mapping.inputs['Vector']);nt.links.new(mapping.outputs[0],normal_image.inputs['Vector'])
    original['Concrete']=dielectric('CapeConcrete',Path('textures/cape-ship'))
    p=original['Glass'].node_tree.nodes.get('Principled BSDF');nt=original['Glass'].node_tree
    for link in list(p.inputs['Base Color'].links):nt.links.remove(link)
    p.inputs['Base Color'].default_value=(.96,.98,.96,1);p.inputs['IOR'].default_value=1.52
    rough=p.inputs['Roughness'].links[0].from_socket;mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=.010/(9/255)
    nt.links.new(rough,mul.inputs[0]);nt.links.new(mul.outputs[0],p.inputs['Roughness'])
    charts={};reductions={}
    from ranch_reduce import reduce
    for ob in objects:
        names=assignments[ob.name];used={names[p.material_index] for p in ob.data.polygons}
        if ob.get('component')=='eave_rake_soffit':freeze_folded_surface(ob)
        if ob.get('component')=='wall':
            component=ob.get('component')
            if component=='drainage':ob['component']='eave_rake_soffit'
            row=reduce(ob,meta,tolerance=.012,passes=22,include_front=True,wall_min_z=meta['spec']['site_grade_m']+.40)
            if row:reductions[ob.name+'_planar_weather']=row
            ob['component']=component
        if 'RanchRoof' in used:
            row=reduce(ob,meta,tolerance=.015) if ob.get('component')!='eave_rake_soffit' else None
            if row:reductions[ob.name]=row
            whole=ob.get('component')=='roof'
            if whole:
                bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.join_triangles(bm,faces=list(bm.faces),cmp_materials=True,cmp_uvs=True,angle_face_threshold=.001,angle_shape_threshold=2.8);bm.to_mesh(ob.data);bm.free();ob.data.update()
            ob.data.calc_loop_triangles();area=sum(t.area for t in ob.data.loop_triangles)
            charts[ob.name]=resolve(ob,meta['spec']['roof_age']=='newer',True,absolute_area_tolerance=5e-8 if area<1e-4 else 0,use_polygons=whole)
        if 'SplitStone' in used or 'SplitBrick' in used:vener=veneer_charts(ob,seed)
        if ob.get('component') in ('roof','ridge','wall'):
            row=reduce(ob,meta,tolerance=.025,passes=28,include_front=True,wall_min_z=meta['spec']['site_grade_m']+.40)
            if row:reductions[ob.name+'_after_charts']=row
        for i,name in enumerate(names):
            role={'RanchRoof':'Shingles','SplitBrick':'Veneer','SplitStone':'Veneer','SplitPaintedBoards':'Siding'}.get(name,name.removeprefix('House'))
            ob.data.materials[i]=original[role]
        for attribute in list(ob.data.attributes):
            if attribute.name.startswith(('Cape','Split')):ob.data.attributes.remove(attribute)
    meta['submicrometer_uv_welds']={ob.name:n for ob in objects if (n:=weld_uv_slivers(ob))}
    meta['removed_unreferenced_vertices']={ob.name:n for ob in objects if (n:=discard_loose(ob))}
    keep={m for ob in objects for m in ob.data.materials}
    for mat in list(bpy.data.materials):
        if mat not in keep:bpy.data.materials.remove(mat,do_unlink=True)
    for role,mat in original.items():
        if mat in keep:mat.name='SplitPaintedBoards' if role=='Siding' and skin in ('battens','grooved') else 'RanchRoof' if role=='Shingles' else 'SplitStone' if role=='Veneer' else 'CapeConcrete' if role=='Concrete' else 'House'+role
    meta['roof_color_precision']=condition_roof_colors(objects,original['Shingles'])
    total=0
    for ob in objects:ob.data.calc_loop_triangles();total+=len(ob.data.loop_triangles)
    meta.update(stage='Baked split-level delivery / external shared PBR maps',triangles=total,charts=charts,reduction=reductions)
    ROOT.mkdir(parents=True,exist_ok=True);game=ROOT/f'game-{seed}.blend';write_changed(game.with_suffix('.json'),json.dumps(meta,indent=2).encode());bpy.ops.wm.save_as_mainfile(filepath=str(game.resolve()))
    moving={o for o in bpy.context.scene.objects if o.name in ('FrontDoor','ServiceDoor') or o.get('motion_kind')=='sectional_track'}
    static=[o for o in objects if o.parent not in moving]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in static:ob.select_set(True)
    bpy.context.view_layer.objects.active=static[0];bpy.ops.object.join();static[0].name='House_Static'
    embedded=ROOT/f'house-{seed}.glb';tiling.export(embedded);compact(embedded)
    known=ROOT/'images';known.mkdir(exist_ok=True)
    for folder in ('textures/ship','textures/ranch-ship','textures/cape-ship','textures/split-ship'):
        for path in Path(folder).glob('T_*.png'):(known/path.name).write_bytes(path.read_bytes())
    out=Path(f'export/HearthfieldSplit-{seed}.gltf');staged=ROOT/'publish'/out.name
    sizes=externalize(embedded,staged,known,max_images=18,min_images=11)
    for suffix in ('.gltf','.bin'):write_changed(out.with_suffix(suffix),staged.with_suffix(suffix).read_bytes())
    write_changed(out.with_suffix('.json'),json.dumps(meta,indent=2).encode());doc,_=read(embedded)
    row=dict(seed=seed,triangles=total,materials=len(doc['materials']),meshes=len(doc['meshes']),**sizes)
    print('SPLIT_DELIVERED',row,flush=True);return row


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seeds',default='51,52,53,54,55,56');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    rows=[export_house(int(s)) for s in a.seeds.split(',')]
    (ROOT/'delivery.json').write_text(json.dumps(dict(rows=rows),indent=2))
