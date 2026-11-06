"""Original outdoor finishes; rest attributes survive joins and projection isolation.

Noise describes manufacture or breaks causal masks; it never becomes a dirt wash.
Colors are linear reflectances, independent of presentation exposure.
"""
import bpy
from kit.materials import Nodes,drip_mask
CACHE={}
COLORS={'Anodized':(.045,.059,.055),'Paint':(.018,.038,.029),'Black':(.009,.012,.011),'Zinc':(.34,.37,.36),'Aluminum':(.29,.31,.30),'Blue':(.009,.045,.16),'Red':(.30,.019,.014),'Cream':(.52,.46,.31),'Paper':(.61,.58,.46),'Rubber':(.006,.008,.007),'Inside':(.008,.011,.009),'Concrete':(.29,.30,.275),'White':(.72,.73,.68),'Orange':(.46,.16,.023),'Rust':(.16,.055,.017),'Flag':(.36,.014,.009),'Lamp':(.78,.74,.62)}

def material(finish,module):
    key=(finish,module)
    if key in CACHE:return CACHE[key]
    n=Nodes('Furniture_'+module+'_'+finish);a=n.node('ShaderNodeAttribute');a.attribute_name='FurnitureRest';pos=a.outputs['Vector'];x,y,z=n.split(pos)
    q=n.node('ShaderNodeAttribute');q.attribute_name='PartRest';local=q.outputs['Vector']
    amin=n.node('ShaderNodeAttribute');amin.attribute_name='PartMin';amax=n.node('ShaderNodeAttribute');amax.attribute_name='PartMax'
    distances=[n.math('MINIMUM',a,b) for a,b in zip(n.split(n.vec('SUBTRACT',local,amin.outputs['Vector'])),n.split(n.vec('SUBTRACT',amax.outputs['Vector'],local)))];d0,d1,d2=distances
    second=n.math('SUBTRACT',n.add(d0,d1,d2),n.add(n.math('MINIMUM',n.math('MINIMUM',d0,d1),d2),n.math('MAXIMUM',n.math('MAXIMUM',d0,d1),d2)))
    line_edge=n.ramp(second,.010,.002)
    geo=n.node('ShaderNodeNewGeometry');nx,ny,nz=n.split(geo.outputs['Normal'])
    micro=n.noise(pos,740,2);breakup=n.noise(pos,42,3);fine=n.noise(pos,170,2)
    # Rounded-edge abrasion is supported by the high source's actual bevels.
    bevel=n.node('ShaderNodeBevel',samples=4);bevel.inputs['Radius'].default_value=.002
    edge=n.ramp(n.math('SUBTRACT',1,n.vec('DOT_PRODUCT',bevel.outputs[0],geo.outputs['Normal'])),.004,.11)
    ao=n.node('ShaderNodeAmbientOcclusion',samples=8);ao.inputs['Distance'].default_value=.016
    cavity=n.math('SUBTRACT',1,ao.outputs['AO'])
    up=n.ramp(nz,.25,.9);low=n.mul(n.ramp(z,.30,.04),n.ramp(breakup,.25,.70))
    c=COLORS[finish];metal=1 if finish in ('Aluminum','Zinc','Anodized') else 0;rough=.56
    if finish=='Zinc':
        # Zinc crystal grains alter reflectance slightly, never resemble rust.
        v=n.node('ShaderNodeTexVoronoi',feature='F1');n.feed(v.inputs['Vector'],pos);v.inputs['Scale'].default_value=155
        base=n.mix(n.ramp(v.outputs['Distance'],.20,.75),tuple(i*.75 for i in c),c,True);rough=n.add(.40,n.mul(micro,.15));height=n.mul(micro,.000018)
        oxide=n.mul(low,.42);base=n.mix(oxide,base,(.26,.28,.25),True);rough=n.mix(oxide,rough,.78);metal=n.mix(oxide,metal,.28)
    else:
        exposed=n.mul(up,n.ramp(breakup,.18,.80),.18)
        base=n.mix(exposed,c,tuple(min(1,i*1.28+.009) for i in c),True)
        rough=n.add(.43,n.mul(micro,.13),n.mul(exposed,.45));height=n.mul(micro,.000025 if metal else .00004)
    if finish=='Paint':rough=n.add(.65,n.mul(micro,.12))
    painted=finish in ('Paint','Black','Blue','Red','Cream')
    if painted:
        # Boots/carts hit feet and lower folds; rain remains below seams.
        chips=n.mul(n.maximum(edge,n.ramp(line_edge,.25,.80)),n.ramp(fine,.43,.63),n.maximum(n.ramp(low,.12,.42),.65))
        rust=n.mul(chips,n.ramp(breakup,.32,.64))
        base=n.mix(chips,base,(.18,.19,.18),True);base=n.mix(rust,base,(.17,.064,.022),True)
        rough=n.mix(chips,rough,.73);metal=n.mul(chips,n.math('SUBTRACT',1,rust))
        base=n.mix(n.mul(low,.65),base,tuple(i*.52 for i in c),True)
        # Sparse drip tracks from actual upper folds, coin cases and roof rails.
        sources=[(-.17,1.0,.016,.24),(.16,.98,.018,.32)]
        if 'Shelter' in module:sources=[(-1.8,2.43,.018,.38),(-.60,2.23,.014,.36),(.60,2.23,.017,.35),(1.8,2.43,.018,.40)]
        if 'Collection' in module:sources=[(-.34,.925,.012,.25),(.34,.925,.013,.30),(0,.95,.016,.20)]
        cdict=dict(position=pos,x=x,z=z,normal=geo.outputs['Normal']);drips=drip_mask(n,cdict,sources)
        base=n.mix(n.mul(drips,.72,n.ramp(fine,.25,.65)),base,tuple(i*.38 for i in c),True)
        rough=n.add(rough,n.mul(drips,.11))
        # Polished hand contact keeps the paint's own color.
        touch=n.mul(n.ellipse(pos,(.15,.64),(.07,.15)),n.ramp(ny,-.2,-.8)) if 'News' in module else n.mul(n.maximum(n.ellipse(pos,(0,.64),(.10,.08)),n.ellipse(pos,(-.91,.64),(.08,.08)),n.ellipse(pos,(.91,.64),(.08,.08))),n.ramp(ny,-.2,-.8)) if 'Bench' in module else 0
        base=n.mix(n.mul(touch,.28),base,tuple(i*.38 for i in c),True);rough=n.mix(touch,rough,.28)
    if finish in ('Aluminum','Anodized'):
        oxide=n.mul(n.maximum(cavity,n.mul(line_edge,.5)),n.ramp(breakup,.28,.64))
        base=n.mix(n.mul(oxide,.6),base,tuple(v*.42 for v in c),True)
        metal=n.mix(oxide,metal,.30)
        base=n.mix(n.mul(cavity,.36),base,(.065,.071,.065),True);rough=n.add(.55 if finish=='Aluminum' else .37,n.mul(micro,.15),n.mul(cavity,.16));height=n.mul(micro,.000018)
    if finish in ('Concrete','Inside','Rubber','Paper'):
        metal=0;rough=.82;height=n.mul(micro,.00007 if finish=='Concrete' else .000012)
    n.channel('edge',edge);n.channel('cavity',cavity)
    CACHE[key]=n.finish(base,rough,metal,height);return CACHE[key]

def attributes(rt):
    bpy.context.view_layer.update()
    for ob in rt.children_recursive:
        if ob.type!='MESH' or not ob.get('finish'):continue
        to_root=rt.matrix_world.inverted()@ob.matrix_world
        lo=[min(v.co[k] for v in ob.data.vertices) for k in range(3)];hi=[max(v.co[k] for v in ob.data.vertices) for k in range(3)]
        for name,value in [('PartMin',lo),('PartMax',hi)]:
            a=ob.data.attributes.get(name) or ob.data.attributes.new(name,'FLOAT_VECTOR','POINT')
            for row in a.data:row.vector=value
        for name,transform in [('FurnitureRest',to_root),('PartRest',None)]:
            a=ob.data.attributes.get(name) or ob.data.attributes.new(name,'FLOAT_VECTOR','POINT')
            for row,v in zip(a.data,ob.data.vertices):row.vector=transform@v.co if transform else v.co
        if ob.get('bake_surface'):
            ob.data.materials.clear();ob.data.materials.append(material(ob['finish'],rt.name));ob['asset_set']='StreetFurniture'
            for p in ob.data.polygons:p.material_index=0
