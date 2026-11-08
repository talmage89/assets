"""Stock PBR binding, V-band UV clipping and placement-owned concrete tint.

UV repetition is intentional manufacture, not overlapping unique lightmaps.
Only structural faces are split at atlas band limits; no mesh is subdivided
to make an image-space stain. Alpha marks reuse this same PBR triple.
"""
import hashlib,json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from kit import tiling

LAYOUT={}


def palette():
    global LAYOUT
    LAYOUT=json.loads(Path('build/lookdev/atlas-layout.json').read_text())
    opaque=tiling.material('ParkingGarage',Path('textures/lookdev/ship'),tint=True);opaque.name='Garage concrete and steel / baked'
    next(n for n in opaque.node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.35
    alpha=opaque.copy();alpha.name='Garage causal deposits / shared coverage';bs=alpha.node_tree.nodes.get('Principled BSDF')
    tex=next(n for n in alpha.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.name.endswith('BaseColor.png'))
    alpha.node_tree.links.new(tex.outputs['Alpha'],bs.inputs['Alpha']);alpha.surface_render_method='DITHERED';alpha.use_backface_culling=False
    vc=next(n for n in alpha.node_tree.nodes if n.type=='VERTEX_COLOR');mul=alpha.node_tree.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY'
    alpha.node_tree.links.new(tex.outputs['Alpha'],mul.inputs[0]);alpha.node_tree.links.new(vc.outputs['Alpha'],mul.inputs[1]);alpha.node_tree.links.new(mul.outputs[0],bs.inputs['Alpha'])
    light=opaque.copy();light.name='Garage practical lenses / shared atlas';bs=light.node_tree.nodes.get('Principled BSDF')
    tex=next(n for n in light.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.name.endswith('BaseColor.png'))
    light.node_tree.links.new(tex.outputs['Color'],bs.inputs['Emission Color']);bs.inputs['Emission Strength'].default_value=3
    return opaque,alpha,light


def clip(poly,axis,value,above):
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        ia=(a[axis]>=value-1e-8) if above else (a[axis]<=value+1e-8);ib=(b[axis]>=value-1e-8) if above else (b[axis]<=value+1e-8)
        if ia:out.append(a)
        if ia!=ib:
            t=(value-a[axis])/(b[axis]-a[axis]);out.append(a.lerp(b,t))
    return out


def concrete_tint(q,normal,ob,p,salt,role):
    variation=.77+.11*salt;warm=.98+.035*math.sin(salt*71)
    factor=1.0
    if role=='Deck' and normal.z>.7:factor*=.78 # maintained, traffic-darkened sealer; pale soffits retain cement tone
    if role=='Concrete' and p['system']=='pt':factor*=.85
    if ob.name.startswith('Tower_'):
        panel=math.floor((q.z+.002)/p['floor_to_floor']);variation*=1+.025*math.sin(panel*2.31+salt*73)
    if normal.z>.7 and q.z>(p['levels']-1)*p['floor_to_floor']-.3:
        factor*=1.035 # broad sun exposure; lane wear uses projected coverage
    return (variation*factor,variation*factor*warm,variation*factor*(.95+.035*salt),1)


def bind(root,p,mats):
    opaque,alpha,light=mats;count=0
    for ob in list(root.children_recursive):
        if ob.type!='MESH':continue
        old=ob.data
        if not any(m and m.name.startswith('Garage form ') for m in old.materials):continue
        vs=[];fs=[];uvs=[];colors=[];indices=[];materials=[]
        def slot(mat):
            if mat not in materials:materials.append(mat)
            return materials.index(mat)
        salt=int(hashlib.sha256(ob.name.encode()).hexdigest()[:8],16)/0xffffffff
        olduv=old.uv_layers.active
        for f in old.polygons:
            mat=old.materials[f.material_index];role=mat.name.removeprefix('Garage form ').split('.')[0]
            poly=[old.vertices[i].co.copy() for i in f.vertices]
            if not mat.name.startswith('Garage form ') or role=='glass':
                index=slot(mat);cuv=[tuple(olduv.data[li].uv) for li in f.loop_indices]
                start=len(vs);vs.extend(poly);fs.append(tuple(range(start,len(vs))));uvs.append(cuv);colors.append([(1,1,1,1)]*len(poly));indices.append(index);continue
            role='Light' if role=='fluorescent' else role
            # The cast traffic finish occupies its own roughness band. Bare
            # soffits share cement manufacture, with cast/precast tint, so a
            # second material/draw is not required on each structural tile.
            if role=='Deck' and f.normal.z<.7:role='Concrete'
            cell='precast' if role=='Concrete' else 'cast' if role=='Deck' else 'steel' if role=='Steel' else role
            chart=LAYOUT[cell];a,b,c,d=chart['rect'];axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2]
            # U repeats across the whole width of each strip. Put the long
            # direction there so thin tee soffits do not pay for V-band cuts.
            axes.sort(key=lambda k:max(v[k] for v in poly)-min(v[k] for v in poly),reverse=True);uaxis,vaxis=axes
            pieces=[(poly,0)];coverage=chart['coverage']
            if coverage:
                cw,ch=coverage;lo=min(v[vaxis] for v in poly);hi=max(v[vaxis] for v in poly)
                # Large core panels trade some transverse texel density for
                # zero silhouette-neutral subdivisions; the tower stays in
                # its 8k budget. Small faces retain the physical density.
                if ob.name.startswith('Tower'):ch=max(ch,hi-lo)
                coverage=(cw,ch)
                pieces=[]
                # Small fabricated faces fit one chart at physical density.
                # Translate their phase instead of cutting a narrow stair,
                # jamb or flange just because it straddles a world grid line.
                if hi-lo<=ch+1e-7:
                    pieces=[(poly,lo-max(0,ch-(hi-lo))*salt)]
                else:
                    for band in range(math.floor((lo+1e-7)/ch),math.floor((hi-1e-7)/ch)+1):
                        part=clip(clip(poly,vaxis,band*ch,True),vaxis,(band+1)*ch,False)
                        if len(part)>=3:pieces.append((part,band*ch))
            for part,phase in pieces:
                start=len(vs);vs.extend(part);fs.append(tuple(range(start,len(vs))));indices.append(slot(light if role=='Light' else opaque));puv=[];tints=[]
                u0,u1=min(v[uaxis] for v in part),max(v[uaxis] for v in part);v0,v1=min(v[vaxis] for v in part),max(v[vaxis] for v in part)
                for v in part:
                    if coverage:
                        cw,ch=coverage;puv.append((v[uaxis]/cw+salt,b+(v[vaxis]-phase)/ch*(d-b)))
                    else:puv.append((a+(.15+.7*(v[uaxis]-u0)/max(1e-9,u1-u0))*(c-a),b+(.15+.7*(v[vaxis]-v0)/max(1e-9,v1-v0))*(d-b)))
                    q=ob.matrix_world@v;normal=(ob.matrix_world.to_3x3()@f.normal).normalized()
                    tints.append(concrete_tint(q,normal,ob,p,salt,role) if role in ('Concrete','Deck') else (1,1,1,1))
                uvs.append(puv);colors.append(tints)
        me=bpy.data.meshes.new(old.name+' baked UV bands');me.from_pydata(vs,[],fs);me.update()
        for m in materials:me.materials.append(m)
        uv=me.uv_layers.new(name='UVMap');tint=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=tint
        for f,index,cuv,rgba in zip(me.polygons,indices,uvs,colors):
            f.material_index=index
            for li,xy,col in zip(f.loop_indices,cuv,rgba):uv.data[li].uv=xy;tint.data[li].color=col
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces))
        # Float32 clipping at a grid vertex can leave nanometre-wide slivers.
        # Remove these numerical faces, rather than exporting collapsed UVs.
        uv_layer=bm.loops.layers.uv.active
        def sliver(f):
            a,b,c=[loop[uv_layer].uv for loop in f.loops]
            return f.calc_area()<1e-7 or abs((b-a).cross(c-a))<1e-10
        bmesh.ops.delete(bm,geom=[f for f in bm.faces if sliver(f)],context='FACES')
        bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
        bm.to_mesh(me);bm.free();me.update();ob.data=me;count+=1
    return count


def source_finish():
    """Same exported geometry/camera, original manufacture before bake/filter."""
    for mat in bpy.data.materials:
        if not mat.use_nodes or not mat.name.startswith('Garage '):continue
        for node in mat.node_tree.nodes:
            if node.type!='TEX_IMAGE' or not node.image or 'T_ParkingGarage_' not in node.image.name:continue
            name=node.image.name.split('.')[0]+'.png'
            if 'Normal' in name:continue
            path=Path('build/lookdev/atlas-source')/name
            if path.exists():
                node.image=bpy.data.images.load(str(path.resolve()),check_existing=True)
                node.image.colorspace_settings.name='Non-Color' if '_ORM' in name else 'sRGB'
        normal=next((n for n in mat.node_tree.nodes if n.type=='NORMAL_MAP'),None)
        if normal is None:continue
        n=mat.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(Path('build/lookdev/atlas-source/T_ParkingGarage_Height.png').resolve()),check_existing=True);n.image.colorspace_settings.name='Non-Color'
        bump=mat.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.008;bump.inputs['Strength'].default_value=.35
        mat.node_tree.links.new(n.outputs['Color'],bump.inputs['Height'])
        bs=mat.node_tree.nodes.get('Principled BSDF');mat.node_tree.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
