"""Stable attribute-coordinate finishes and dense original casting bake source."""
import argparse,sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import bpy
from mathutils import Vector
from kit import model as G
from kit.materials import Nodes
from build import allen_high
from spec import spec,height

PALETTE={}
def pos(n,name='FinishPosition'):
    return n.node('ShaderNodeAttribute',attribute_name=name).outputs['Vector']
def image(n,path,position,noncolor=False):
    q=n.node('ShaderNodeTexImage');q.image=bpy.data.images.load(str(path.resolve()),check_existing=True)
    if noncolor:q.image.colorspace_settings.name='Non-Color'
    q.extension='EXTEND';n.feed(q.inputs['Vector'],position);return q.outputs['Color'],q.outputs['Alpha']
def deckuv(n,p):
    x,y,z=n.split(p);return n.combine(n.add(n.mul(x,1/.22),.5),n.math('SUBTRACT',.5,n.mul(y,1/.822)),0)
def source_material(name,col,rough,metal,kind,s,art):
    n=Nodes(name);p=pos(n);x,y,z=n.split(p);rest=pos(n,'RestPosition');rx,ry,rz=n.split(rest);age={'new':0,'season':.58,'beat':1}[s.state]
    noise=n.noise(p,2600,2);heightfield=n.mul(n.math('SUBTRACT',noise,.5),.000009);base=col
    if kind in ('bottom','grip'):
        uv=deckuv(n,rest);base,_=image(n,art/f'{s.state}-{kind}.png',uv)
        rough,_=image(n,art/f'{s.state}-{kind}-rough.png',uv,True)
        h,_=image(n,art/f'{s.state}-{kind}-height.png',uv,True)
        heightfield=n.mul(n.math('SUBTRACT',h,.5),.004)
        if kind=='grip':
            foot,_=image(n,art/f'{s.state}-foot-contact.png',uv,True)
            coverage,_=image(n,art/f'{s.state}-grip-coverage.png',uv,True)
            substrate=base
            tooth=n.math('SUBTRACT',1,n.mul(foot,.78))
            # 0.35–0.7 mm aggregates survive the shipped texel footprint;
            # finer individual facets supply the glints in close views.
            cells=n.node('ShaderNodeTexVoronoi');n.feed(cells.inputs['Vector'],p);cells.inputs['Scale'].default_value=1450
            facets=n.split(cells.outputs['Color'])[0]
            grit=n.math('SUBTRACT',1,cells.outputs['Distance']);fine=n.voronoi(p,4500)
            heightfield=n.add(heightfield,n.mul(tooth,coverage,n.add(n.mul(grit,.00032),n.mul(fine,.000045))))
            graincolor=n.mix(facets,(.0045,.005,.0045),(.048,.050,.048),True)
            base=n.mix(n.mul(tooth,.62),base,graincolor,True)
            # Neutral-balanced used-grip calibration; facet sparkle is a
            # specular response, not a raised diffuse charcoal albedo.
            base=n.vec('MULTIPLY',base,(.38,.38,.38))
            base=n.mix(coverage,substrate,base,True)
            sparkle=n.ramp(facets,.78,.96)
            rough=n.mix(n.mul(sparkle,tooth,coverage),rough,.22)
            # A filed/score line just inside the actual curved rail.
            score=n.band(n.node('ShaderNodeAttribute',attribute_name='TrimDistance').outputs['Fac'],.0015,.00018,.00018)
            heightfield=n.math('SUBTRACT',heightfield,n.mul(score,.00022))
    elif kind=='maple':
        cross=name.endswith(('3','5'))
        grainpos=n.vec('MULTIPLY',p,(1.2,35,4) if cross else (35,1.2,4));grain=n.noise(grainpos,80,2)
        base=n.mix(grain,tuple(c*.79 for c in col),tuple(c*1.19 for c in col),True)
        rough=n.mix(noise,.43,.62);heightfield=n.mul(grain,.000035)
        end=n.ramp(n.math('ABSOLUTE',ry),.335,.405)
        grime=n.mul(age,end,n.noise(p,160,2));base=n.mix(grime,base,(.22,.125,.055),True)
    elif kind=='aluminum':
        base=n.mix(noise,(.40,.415,.405),(.435,.447,.435),True);rough=n.mix(noise,.55,.61)
        heightfield=n.mul(n.math('SUBTRACT',noise,.5),.000006)
        # A rail contacts the original DOWNWARD-facing axle housing, never
        # the casting's deck-facing top. Attribute normals stay in rest space.
        nz=n.split(pos(n,'RestNormal'))[2]
        hanger=n.node('ShaderNodeAttribute',attribute_name='HangerSurface').outputs['Fac']
        ground=n.mul(min(1,age*1.45),hanger,n.ramp(rz,s.axle_z+.001,s.axle_z-.004),n.ramp(nz,-.05,-.65))
        base=n.mix(ground,base,(.66,.68,.665),True);rough=n.mix(ground,rough,.23)
        score=n.noise(n.vec('MULTIPLY',rest,(.025,1,1)),2600,1)
        heightfield=n.add(heightfield,n.mul(ground,score,-.000018))
        # Mold parting witness at the axle's equator; thin ridge, no geometry.
        seam=n.band(rz,s.axle_z,.00015,.00010);heightfield=n.add(heightfield,n.mul(seam,.00008))
        uv=n.combine(n.add(n.mul(x,1/.045),.5),n.add(n.mul(z,1/.009),.5),0)
        ink,alpha=image(n,art/'truck-print.png',uv)
        mark=n.mul(alpha,n.band(x,0,.0225,.0001),n.band(z,0,.0045,.0001),n.ramp(y,.006,.008),n.math('SUBTRACT',1,ground))
        base=n.mix(mark,base,ink,True);metal=n.mix(mark,metal,0)
        grime=n.mul(age,n.band(rz,s.underside-.007,.007,.004),n.noise(p,250,2),.45)
        base=n.mix(grime,base,(.12,.105,.075),True)
        ao=n.node('ShaderNodeAmbientOcclusion',samples=8);ao.inputs['Distance'].default_value=.004
        cavity=n.mul(age,n.math('SUBTRACT',1,ao.outputs['AO']),.65)
        base=n.mix(cavity,base,(.12,.11,.09),True);rough=n.mix(cavity,rough,.72)
    elif kind=='wheel':
        radius=n.math('SQRT',n.add(n.mul(y,y),n.mul(z,z)))
        road=n.mul(n.band(x,0,.0133,.0025),n.ramp(radius,.020,.024))
        body={'new':(.73,.63,.405),'season':(.65,.48,.205),'beat':(.53,.36,.115)}[s.state]
        body=n.mix(noise,tuple(c*.94 for c in body),tuple(c*1.04 for c in body),True)
        stain=n.mul(min(1,age*1.9),road,n.mix(n.noise(p,650,2),.88,1))
        base=n.mix(stain,body,(.10,.060,.022),True);rough=n.mix(road,.43,.72)
        grease=n.mul(age,n.band(radius,.0129,.0015,.0015),n.ramp(x,.0125,.015),n.ramp(n.noise(p,850,2),.35,.68),.6)
        base=n.mix(grease,base,(.075,.051,.021),True)
        turn=n.math('ARCTAN2',y,z)
        lines=n.math('SINE',n.add(n.mul(radius,43000),n.mul(turn,2)))
        heightfield=n.add(n.mul(noise,.000012),n.mul(road,lines,.000009))
        uv=n.combine(n.add(n.mul(y,1/.060),.5),n.add(n.mul(z,1/.060),.5),0)
        ink,alpha=image(n,art/'wheel-print.png',uv)
        curb=n.mul(min(1,age*1.65),n.ramp(n.noise(p,1000,2),.29,.64))
        mask=n.mul(alpha,n.ramp(x,.0135,.0157),n.math('SUBTRACT',1,n.mul(curb,.98)))
        base=n.mix(mask,base,ink,True)
    elif kind=='steel':
        rough=n.mix(noise,.25,.36)
        # Axle screw pitch 24 TPI; the hidden smooth axle needs no game rings.
        helix=n.math('SINE',n.add(n.mul(n.math('ABSOLUTE',rx),math.tau/.001058),n.math('ARCTAN2',y,z)))
        ends=n.ramp(n.math('ABSOLUTE',rx),s.width/2-.011,s.width/2-.008)
        thread=n.node('ShaderNodeAttribute',attribute_name='ThreadSurface').outputs['Fac']
        radius=n.math('SQRT',n.add(n.mul(y,y),n.mul(z,z)))
        heightfield=n.add(heightfield,n.mul(thread,ends,n.ramp(radius,.0036,.00395),helix,.00018))
        base=n.mix(n.mul(age,noise,.22),col,(.19,.17,.115),True)
        nut=n.node('ShaderNodeAttribute',attribute_name='KingpinNut').outputs['Fac']
        grind=n.mul(age,nut,n.ramp(rz,.029,.022))
        base=n.mix(grind,base,(.63,.65,.63),True);rough=n.mix(grind,rough,.20)
        heightfield=n.add(heightfield,n.mul(grind,n.noise(n.vec('MULTIPLY',rest,(.06,1,1)),2400,1),-.000025))
    elif kind=='blacksteel':
        geo=n.node('ShaderNodeNewGeometry');rounded=n.node('ShaderNodeBevel',samples=4);rounded.inputs['Radius'].default_value=.00022
        edge=n.ramp(n.math('SUBTRACT',1,n.vec('DOT_PRODUCT',geo.outputs['Normal'],rounded.outputs['Normal'])),.005,.08)
        tool=n.mul(age,edge,n.ramp(n.noise(p,1400,2),.40,.67),.9)
        base=n.mix(tool,col,(.32,.34,.33),True);rough=n.mix(tool,rough,.28);metal=n.mix(tool,metal,1)
    elif kind=='shield':
        rough=n.mix(noise,.38,.48);base=n.mix(n.mul(age,noise,.6),col,(.025,.028,.021),True)
        radius=n.math('SQRT',n.add(n.mul(y,y),n.mul(z,z)))
        lip=n.maximum(n.band(radius,.0092,.00012,.00007),n.band(radius,.0072,.00008,.00008))
        heightfield=n.add(heightfield,n.mul(lip,.00004))
    mat=n.finish(base,rough,metal,heightfield,coat=.18 if kind in ('bottom','maple') else 0)
    if kind=='wheel':mat.node_tree.nodes['SURFACE'].inputs['Transmission Weight'].default_value=.06
    PALETTE[name]='deck' if kind in ('bottom','maple') else 'wheel' if kind=='wheel' else 'common'
    return mat

def assign(s,art):
    mapping={}
    for m in list(bpy.data.materials):
        name=m.name
        if 'bottom' in name:kind='bottom'
        elif 'grip' in name:kind='grip'
        elif 'Maple' in name:kind='maple'
        elif 'cast aluminum' in name:kind='aluminum'
        elif 'zinc steel' in name:kind='steel'
        elif 'bearing shield' in name:kind='shield'
        elif 'black hardware' in name:kind='blacksteel'
        elif 'wheel /' in name:kind='wheel'
        else:kind='simple'
        b=m.node_tree.nodes.get('Principled BSDF') if m.use_nodes else None
        if not b:continue
        # Preserve the independent manufacturing source names for per-face
        # delivery assignment; all coordinate systems are stable attributes.
        mapping[m]=source_material('Finish '+name,tuple(b.inputs['Base Color'].default_value[:3]),b.inputs['Roughness'].default_value,b.inputs['Metallic'].default_value,kind,s,art)
    for o in bpy.context.scene.objects:
        if o.type=='MESH':
            for slot in o.material_slots:
                if slot.material in mapping:slot.material=mapping[slot.material]

def attributes(o,s):
    world=o.matrix_world
    # Cache before writing custom data: interleaving vertex-normal reads and
    # attribute writes repeatedly invalidates Blender's evaluated normal cache.
    normal_matrix=world.to_3x3().inverted().transposed()
    normals=[tuple((normal_matrix@v.normal).normalized()) for v in o.data.vertices]
    normal=o.data.attributes.new('RestNormal','FLOAT_VECTOR','POINT')
    normal.data.foreach_set('vector',[c for v in normals for c in v])
    for key,enabled in (('HangerSurface',o.get('part')=='hangers'),('KingpinNut','kingpin locknut' in o.name)):
        attr=o.data.attributes.new(key,'FLOAT','POINT')
        for row in attr.data:row.value=float(enabled)
    thread=o.data.attributes.new('ThreadSurface','FLOAT','POINT')
    for row in thread.data:row.value=1 if o.get('part')=='axles' else 0
    if o.get('part')=='deck':
        from mathutils.geometry import intersect_point_line
        adjacent={}
        for face in o.data.polygons:
            for edge in face.edge_keys:adjacent.setdefault(tuple(sorted(edge)),set()).add(face.material_index)
        border=[(Vector((o.data.vertices[a].co.x,o.data.vertices[a].co.y)),Vector((o.data.vertices[b].co.x,o.data.vertices[b].co.y))) for (a,b),mats in adjacent.items() if 1 in mats and 8 in mats]
        trim=o.data.attributes.new('TrimDistance','FLOAT','POINT')
        for v,row in zip(o.data.vertices,trim.data):
            p=Vector((v.co.x,v.co.y));minimum=1e9
            for a,b in border:
                q,f=intersect_point_line(p,a,b);q=a.lerp(b,max(0,min(1,f)));minimum=min(minimum,(p-q).length)
            row.value=minimum
    wr=o.parent
    while wr and not wr.name.startswith('Wheel_'):wr=wr.parent
    side=-1 if wr and wr.name.endswith('L') else 1
    for name in ('RestPosition','FinishPosition'):
        a=o.data.attributes.get(name) or o.data.attributes.new(name,'FLOAT_VECTOR','POINT')
        for v,row in zip(o.data.vertices,a.data):
            p=world@v.co
            if name=='FinishPosition' and wr:
                p=wr.matrix_world.inverted()@p;p.x*=side;p.y*=side
            elif name=='FinishPosition' and o.get('part') in ('hangers','baseplates'):
                sign=-1 if o.name.startswith('Front') else 1
                p=Vector((-sign*p.x,sign*(p.y-sign*s.axle_y),p.z-s.axle_z))
            elif name=='FinishPosition' and o.get('part')=='axles':
                sign=-1 if o.name.startswith('Front') else 1
                p=Vector((p.x,p.y-sign*s.axle_y,p.z-s.axle_z))
            row.vector=p

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--art',default='build/art');p.add_argument('--palette',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));root=bpy.data.objects['Skateboard'];s=spec(int(root['seed']),root['age_state'])
    root['checkpoint']='Procedural dense look-dev / bake source'
    games=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='Skateboard']
    for o in games:
        if o.get('dense_source'):
            dense=bpy.data.objects[o['dense_source']];dense.hide_set(False);dense.hide_render=False
            G.attach(dense,o.parent,asset_set='Skateboard');dense['part']=o['part'];dense.name=o.name+' high';dense['source_only']=False
            bpy.data.objects.remove(o,do_unlink=True)
        elif o.get('part')=='axles':
            label='Front' if 'Front' in o.name else 'Rear';ay=(-1 if label=='Front' else 1)*s.axle_y
            hi=G.cylinder(o.name+' high',(-s.width/2,ay,s.axle_z),(s.width/2,ay,s.axle_z),.004,o.data.materials[0],64);G.attach(hi,o.parent,asset_set='Skateboard');hi['part']='axles';bpy.data.objects.remove(o,do_unlink=True)
        elif o.name.startswith('Flush Allen bolt head'):
            points=[o.matrix_world@v.co for v in o.data.vertices];cx=(min(p.x for p in points)+max(p.x for p in points))/2;cy=(min(p.y for p in points)+max(p.y for p in points))/2
            hi=allen_high(o.name+' high',cx,cy,height(s,cx,cy)+s.thickness,o.data.materials[0]);G.attach(hi,o.parent,asset_set='Skateboard');hi['part']=o['part'];bpy.data.objects.remove(o,do_unlink=True)
        elif o.get('part') in ('truck_hardware','axle_nuts','mount_hardware'):
            # Small manufactured chamfers transfer to the normal bake only.
            G.bevel(o,.00013,2);G.apply(o)
    bpy.context.view_layer.update()
    for o in bpy.context.scene.objects:
        if o.type=='MESH' and o.get('asset_set'):
            fallback=o.data.materials[2] if o.get('part')=='deck' else next(m for m in o.data.materials if m)
            for i,m in enumerate(o.data.materials):
                if m is None:o.data.materials[i]=fallback
    assign(s,Path(a.art))
    for o in bpy.context.scene.objects:
        if o.type=='MESH' and o.get('asset_set'):attributes(o,s);o.hide_render=False;o.hide_set(False)
    from mathutils import Matrix
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH' and o.get('asset_set'):
            key=o.name[:-5] if o.name.endswith(' high') else o.name
            frame=G.pivot('Projection / '+key,(0,0,0));frame.parent=o.parent;frame.matrix_basis=Matrix.Identity(4);G.attach(o,frame,asset_set='Skateboard')
    import json
    Path(a.palette).write_text(json.dumps(PALETTE,indent=2))
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
if __name__=='__main__':main()
