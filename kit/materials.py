"""Meter-scale manufacturing finishes, with physically located weather layers.

Finish -> heat -> handling -> abrasion/chips -> rust -> grease -> gravity dust.
Noise only breaks up those masks or describes manufacturing microstructure.
Every source exposes OUT_base/rough/metal/height (height is in meters) and
inspection masks OUT_edge/cavity/grease/dust. All masks are original nodes.
"""
import math
import bpy


class Nodes:
    def __init__(self,name):
        self.mat=bpy.data.materials.new(name)
        self.mat.use_nodes=True
        self.nt=self.mat.node_tree
        self.nt.nodes.clear()
    def node(self,kind,**properties):
        node=self.nt.nodes.new(kind)
        for key,value in properties.items():setattr(node,key,value)
        return node
    def feed(self,destination,source):
        if hasattr(source,'is_output'):self.nt.links.new(source,destination)
        else:destination.default_value=source
    def math(self,operation,a,b=0,clamp=False):
        node=self.node('ShaderNodeMath',operation=operation,use_clamp=clamp)
        self.feed(node.inputs[0],a);self.feed(node.inputs[1],b)
        return node.outputs[0]
    def mul(self,*values):
        result=values[0]
        for value in values[1:]:result=self.math('MULTIPLY',result,value)
        return result
    def add(self,*values):
        result=values[0]
        for value in values[1:]:result=self.math('ADD',result,value)
        return result
    def maximum(self,*values):
        result=values[0]
        for value in values[1:]:result=self.math('MAXIMUM',result,value)
        return result
    def mix(self,factor,a,b,color=False):
        node=self.node('ShaderNodeMix',data_type='RGBA' if color else 'FLOAT',clamp_factor=True)
        self.feed(node.inputs[0],factor)
        self.feed(node.inputs[6 if color else 2],(*a,1) if color and not hasattr(a,'is_output') else a)
        self.feed(node.inputs[7 if color else 3],(*b,1) if color and not hasattr(b,'is_output') else b)
        return node.outputs[2 if color else 0]
    def vec(self,operation,a,b):
        node=self.node('ShaderNodeVectorMath',operation=operation)
        self.feed(node.inputs[0],a);self.feed(node.inputs[1],b)
        return node.outputs['Value'] if operation in ('DOT_PRODUCT','DISTANCE') else node.outputs[0]
    def noise(self,position,scale,detail=3,roughness=.58):
        node=self.node('ShaderNodeTexNoise')
        self.feed(node.inputs['Vector'],position)
        node.inputs['Scale'].default_value=scale
        node.inputs['Detail'].default_value=detail
        node.inputs['Roughness'].default_value=roughness
        return node.outputs['Fac']
    def voronoi(self,position,scale,feature='F1'):
        node=self.node('ShaderNodeTexVoronoi',feature=feature)
        self.feed(node.inputs['Vector'],position);node.inputs['Scale'].default_value=scale
        return node.outputs['Distance']
    def split(self,position):
        node=self.node('ShaderNodeSeparateXYZ');self.feed(node.inputs[0],position)
        return tuple(node.outputs)
    def combine(self,x,y,z):
        node=self.node('ShaderNodeCombineXYZ')
        for target,value in zip(node.inputs,(x,y,z)):self.feed(target,value)
        return node.outputs[0]
    def ramp(self,value,start,end,lo=0,hi=1):
        node=self.node('ShaderNodeMapRange',interpolation_type='SMOOTHSTEP',clamp=True)
        self.feed(node.inputs['Value'],value)
        for key,val in [('From Min',start),('From Max',end),('To Min',lo),('To Max',hi)]:
            node.inputs[key].default_value=val
        return node.outputs['Result']
    def band(self,value,center,width,softness=.003):
        distance=self.math('ABSOLUTE',self.math('SUBTRACT',value,center))
        return self.ramp(distance,width+softness,width)
    def ellipse(self,position,center,radii,axes=(0,2)):
        components=self.split(position)
        a=self.math('DIVIDE',self.math('SUBTRACT',components[axes[0]],center[0]),radii[0])
        b=self.math('DIVIDE',self.math('SUBTRACT',components[axes[1]],center[1]),radii[1])
        distance=self.add(self.mul(a,a),self.mul(b,b))
        return self.ramp(distance,1,.45)
    def channel(self,name,value):
        if not hasattr(value,'is_output'):
            node=self.node('ShaderNodeRGB' if isinstance(value,tuple) else 'ShaderNodeValue')
            node.outputs[0].default_value=(*value,1) if isinstance(value,tuple) else value
            value=node.outputs[0]
        node=self.node('NodeReroute',name='OUT_'+name,label='OUT_'+name)
        self.feed(node.inputs[0],value)
        return node.outputs[0]
    def finish(self,base,rough,metal,height=0,bump=1.0,coat=0,anisotropy=0):
        bsdf=self.node('ShaderNodeBsdfPrincipled',name='SURFACE')
        for name,value,key in [('base',base,'Base Color'),('rough',rough,'Roughness'),('metal',metal,'Metallic')]:
            self.feed(bsdf.inputs[key],self.channel(name,value))
        normal=self.node('ShaderNodeBump')
        normal.inputs['Distance'].default_value=bump
        normal.inputs['Strength'].default_value=.65
        self.feed(normal.inputs['Height'],self.channel('height',height))
        self.feed(bsdf.inputs['Normal'],normal.outputs[0])
        bsdf.inputs['Specular IOR Level'].default_value=.33 if coat==0 and anisotropy==0 else .5
        bsdf.inputs['Coat Weight'].default_value=coat
        bsdf.inputs['Coat Roughness'].default_value=.22
        bsdf.inputs['Anisotropic'].default_value=anisotropy
        if anisotropy:
            tangent=self.node('ShaderNodeVectorTransform',vector_type='VECTOR',convert_from='OBJECT',convert_to='WORLD')
            tangent.inputs[0].default_value=(1,0,0)
            self.feed(bsdf.inputs['Tangent'],tangent.outputs[0])
        output=self.node('ShaderNodeOutputMaterial',name='OUT')
        self.feed(output.inputs['Surface'],bsdf.outputs[0])
        return self.mat


FINISHES={
 'powder':((.015,.017,.015),0,.63,18e-6,0),
 'paint':((.62,.64,.61),0,.57,24e-6,0),
 'enamel':((.007,.009,.010),0,.23,2.0e-6,.15),
 'stainless':((.48,.51,.53),1,.40,.6e-6,0),
 'cast_iron':((.003,.0035,.0035),0,.64,14e-6,.04),
 'cast_aluminum':((.19,.20,.19),1,.69,18e-6,0),
 'plastic':((.004,.005,.004),0,.60,3e-6,0),
 'rubber':((.010,.011,.010),0,.88,12e-6,0),
 'chrome':((.62,.65,.66),1,.22,.2e-6,0),
 'brass':((.49,.30,.09),1,.36,2e-6,0),
 'soot':((.011,.012,.013),0,.84,25e-6,0),
}


def common(n):
    """Stable rest-frame positions/normals, contact cavities and edge proximity."""
    tc=n.node('ShaderNodeTexCoord');position=tc.outputs['Object']
    geometry=n.node('ShaderNodeNewGeometry')
    rest=n.node('ShaderNodeVectorTransform',vector_type='NORMAL',convert_from='WORLD',convert_to='OBJECT')
    n.feed(rest.inputs[0],geometry.outputs['Normal'])
    normal=rest.outputs[0]
    x,y,z=n.split(position);nx,ny,nz=n.split(normal)
    ao=n.node('ShaderNodeAmbientOcclusion',samples=8,only_local=False,inside=False)
    ao.inputs['Distance'].default_value=.009
    cavity=n.math('SUBTRACT',1,ao.outputs['AO'])
    rounded=n.node('ShaderNodeBevel',samples=4)
    rounded.inputs['Radius'].default_value=.0014
    edge=n.math('SUBTRACT',1,n.vec('DOT_PRODUCT',rounded.outputs['Normal'],geometry.outputs['Normal']))
    edge=n.ramp(edge,.002,.08)
    upward=n.ramp(nz,.35,.95)
    n.channel('edge',edge);n.channel('cavity',cavity)
    return dict(position=position,normal=normal,x=x,y=y,z=z,up=upward,edge=edge,cavity=cavity)


def drip_mask(n,c,sources):
    """Gravity tracks below authored (x,z,width,length) spill sources in object meters."""
    terms=[]
    for source in sources:
        if isinstance(source,dict):
            x,z,width,length=(source[k] for k in ('x','z','width','length'))
            face=n.ramp(n.vec('DOT_PRODUCT',c['normal'],source.get('direction',(0,-1,0))),.1,.8)
        else:
            x,z,width,length=source;face=1
        fall=n.mul(n.ramp(c['z'],z+.001,z-.004),n.ramp(c['z'],z-length,z-length*.55))
        meander=n.mul(n.math('SUBTRACT',n.noise(n.vec('MULTIPLY',c['position'],(1,1,.10)),55,2),.5),width*.8)
        distance=n.math('ABSOLUTE',n.math('SUBTRACT',c['x'],n.add(x,meander)))
        streak=n.ramp(distance,width,width*.20)
        terms.append(n.mul(fall,streak,face))
    return n.maximum(0,*terms)


def handling_mask(n,c,zones):
    return n.maximum(0,*[n.ellipse(c['position'],zone['center'],zone['radii'],zone.get('axes',(0,2))) for zone in zones])


def fingerprint(n,c,zones):
    """Sub-millimeter curved fingerprint ridges, restricted to measured touch zones."""
    terms=[]
    for zone in zones:
        a,b=zone.get('axes',(0,2));v=n.split(c['position'])
        x=n.math('SUBTRACT',v[a],zone['center'][0]);y=n.math('SUBTRACT',v[b],zone['center'][1])
        radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(y,y)))
        curve=n.add(radius,n.mul(n.math('SINE',n.mul(y,120)),.0015))
        ridges=n.ramp(n.math('SINE',n.mul(curve,math.tau/.00048)),.2,.8)
        envelope=n.ellipse(c['position'],zone['center'],(min(.012,zone['radii'][0]),min(.018,zone['radii'][1])),(a,b))
        terms.append(n.mul(envelope,ridges))
    return n.maximum(0,*terms)


def abrasion_mask(n,c,wear,exposure):
    """Sparse long scrapes, restricted to exposed edges/handling surfaces."""
    stretched=n.vec('MULTIPLY',c['position'],(12,1600,320))
    lines=n.ramp(n.noise(stretched,1,2),.64,.73)
    gate=n.ramp(n.noise(c['position'],45,4),.56,.71)
    return n.mul(lines,gate,exposure,wear)


def surface(name,kind,wear=.35,grime=0,dust=0,heat=0,color=None,zones=None,
            deposits=None,rust=False,heat_height=None,roughness=None,cook_zones=None,chip_height=None,heat_zones=None,wheel_radius=None):
    """Build layered PBR with authored wear locations rather than uniform dirt noise.

    zones: handling ellipses in object meters; deposits: gravity drip sources.
    rust=True targets the tank foot ring, equator weld and collar creases.
    heat_height=(center,width) places thermal exposure; otherwise curvature/cavities
    decide where heat residue accumulates. A material can be shared across parts
    with the same pivot/rest frame. `wear=0` suppresses all use-related layers.
    """
    if kind not in FINISHES:raise ValueError(kind)
    col,metal,rough,micro,coat=FINISHES[kind]
    col=color or col;rough=rough if roughness is None else roughness
    n=Nodes(name);c=common(n);p=c['position']
    fine=n.noise(p,1700 if kind in ('paint','powder') else 3200 if kind=='enamel' else 2200,2)
    # Microstructure is the sole whole-surface noise layer: manufactured orange peel/casting.
    height=n.mul(n.math('SUBTRACT',fine,.5),micro)
    base=col;spec=.33 if coat==0 and kind!='stainless' else .5
    zones=zones or []
    touch=handling_mask(n,c,zones)
    prints=fingerprint(n,c,zones)
    rough=n.add(rough,n.mul(n.math('SUBTRACT',fine,.5),.035))
    if kind=='stainless':
        grain=n.noise(n.vec('MULTIPLY',p,(5,1700,1700)),1,2)
        height=n.mul(n.math('SUBTRACT',grain,.5),micro*5)
        rough=n.add(rough,n.mul(n.math('SUBTRACT',grain,.5),.22))
    if kind=='enamel':
        # Subtle finish waviness and orange peel, not large distorted reflections.
        height=n.add(height,n.mul(n.math('SUBTRACT',n.noise(p,95,2),.5),1.5e-6))
    if kind=='cast_iron':
        # Porcelain coated black iron stays black even where food oils/heat accumulate.
        top=n.mul(c['up'],n.ramp(c['z'],.873,.885))
        rough=n.mix(n.mul(top,wear*.35),rough,.34)
        height=n.add(height,n.mul(n.voronoi(p,2600),6e-6))
        contact=n.mul(top,handling_mask(n,c,cook_zones or []))
        cooked=n.mul(contact,wear*2.1,n.ramp(n.noise(p,60,3),.25,.75))
        oil=n.mul(contact,wear,n.ramp(n.noise(p,180,3),.52,.68))
        base=n.mix(cooked,base,(.0014,.0013,.0011),True)
        rough=n.mix(cooked,rough,.58)
        rough=n.mix(oil,rough,.36)
        height=n.add(height,n.mul(cooked,80e-6))
        spec=n.mix(cooked,spec,.22)
    if kind=='powder' and cook_zones:
        contact=n.mul(c['up'],handling_mask(n,c,cook_zones))
        char=n.mul(contact,wear*2.3,n.ramp(n.noise(p,150,4),.38,.62))
        base=n.mix(char,base,(.0015,.0017,.0015),True)
        rough=n.mix(char,rough,.40);spec=n.mix(char,spec,.18)
        height=n.add(height,n.mul(char,20e-6))
    if kind=='rubber' and wheel_radius:
        radius=n.math('SQRT',n.add(n.mul(c['x'],c['x']),n.mul(c['z'],c['z'])))
        shoulder=n.ramp(radius,*wheel_radius)
        scuffs=n.mul(shoulder,wear,n.ramp(n.noise(p,140,4),.45,.65))
        base=n.mix(scuffs,base,(.028,.026,.021),True)
        rough=n.mix(scuffs,rough,.94)
        # Mold split line on each sidewall and rim of the tread.
        seam=n.band(n.math('ABSOLUTE',c['y']),.015,.0003,.0003)
        height=n.add(height,n.mul(seam,12e-6))
    # Thermal exposure is located near vents/cookbox, with patch breakup inside its mask.
    hot=n.band(c['z'],*heat_height) if heat_height else n.maximum(c['edge'],n.mul(c['cavity'],.7))
    if heat_zones:hot=n.mul(hot,handling_mask(n,c,heat_zones))
    hot=n.mul(hot,heat,wear,n.ramp(n.noise(p,110 if kind=='powder' else 36,3),.35,.7))
    heat_color=(.029,.030,.027) if kind in ('cast_iron','soot','enamel') else (.20,.145,.078)
    base=n.mix(n.mul(hot,.35),base,heat_color,True)
    rough=n.mix(hot,rough,.38 if kind=='enamel' else .74)
    # Fingerprints are principally roughness/oil, not bright stamped pictures.
    print_mask=n.mul(prints,wear*.95)
    rough=n.mix(print_mask,rough,.20)
    base=n.mix(n.mul(touch,wear*.035),base,tuple(v*.75 for v in col),True)
    exposure=n.maximum(n.mul(c['edge'],.9),n.mul(touch,.6))
    scratches=abrasion_mask(n,c,wear,exposure)
    rough=n.mix(scratches,rough,.72)
    height=n.add(height,n.mul(scratches,-5e-6))
    # Sparse chips: their placement follows edge proximity, handling and low exposed edges.
    low=n.ramp(c['z'],*chip_height) if chip_height else 0
    chips=n.mul(c['edge'],n.maximum(low,n.mul(touch,.75)),wear*1.8,
                n.ramp(n.noise(p,260,4),.59,.74))
    if kind in ('paint','powder'):
        base=n.mix(chips,base,(.15,.16,.15),True)
        metal=n.mix(chips,metal,.9)
        rough=n.mix(chips,rough,.62)
        height=n.add(height,n.mul(chips,-35e-6))
    if rust:
        foot=n.ramp(c['z'],.065,.019)
        weld=n.band(c['z'],.192,.0018,.004)
        collar=n.mul(n.ramp(c['z'],.38,.424),c['edge'])
        origin=n.maximum(n.mul(foot,n.maximum(c['edge'],c['cavity'],.18)),
                         n.mul(weld,.65),n.mul(collar,.4))
        breakup=n.noise(p,130,5)
        bloom=n.mul(origin,wear*.7,n.ramp(breakup,.43,.59))
        rust_patch=n.mul(origin,wear*2.8,n.ramp(breakup,.56,.67))
        base=n.mix(bloom,base,(.19,.105,.045),True)
        rust_col=n.mix(n.noise(p,680,3),(.11,.037,.009),(.30,.12,.025),True)
        base=n.mix(rust_patch,base,rust_col,True)
        rough=n.mix(rust_patch,rough,.88);metal=n.mix(rust_patch,metal,0)
        height=n.add(height,n.mul(rust_patch,22e-6))
    # Grease anchors to cavities, creases, contact points and explicit downward tracks.
    drips=drip_mask(n,c,deposits or [])
    cavity_grime=n.mul(c['cavity'],n.ramp(n.noise(p,120,4),.28,.65))
    grease=n.mul(n.maximum(drips,cavity_grime),grime,wear)
    if kind=='cast_iron':grease=n.mul(grease,.7)
    if kind=='soot':
        # Carbon flakes: a low-frequency thermal mask plus actual crack boundaries.
        carbon=n.maximum(n.mul(c['cavity'],.8),n.mul(c['up'],.18),touch)
        flakes=n.ramp(n.voronoi(n.vec('MULTIPLY',p,(1,1,.55)),210,'DISTANCE_TO_EDGE'),.008,.045)
        flake_mask=n.mul(carbon,wear,n.ramp(n.noise(p,25,4),.35,.7))
        base=n.mix(flake_mask,base,(.003,.004,.005),True)
        base=n.mix(n.mul(flake_mask,n.math('SUBTRACT',1,flakes),.45),base,(.035,.036,.034),True)
        height=n.add(height,n.mul(flake_mask,flakes,90e-6))
    grease_color=(.003,.004,.004) if kind in ('soot','cast_iron') else (.012,.008,.003)
    base=n.mix(grease,base,grease_color,True)
    rough=n.mix(grease,rough,.22);metal=n.mix(grease,metal,0)
    height=n.add(height,n.mul(grease,8e-6))
    # Gravity settling: up-facing surfaces plus creases. Whole-object dust is impossible.
    dust_mask=n.mul(n.maximum(n.mul(c['up'],.52),n.mul(c['cavity'],.6)),
                    dust,wear,n.ramp(n.noise(p,170,3),.23,.72))
    base=n.mix(dust_mask,base,(.13,.115,.085),True)
    rough=n.mix(dust_mask,rough,.91);metal=n.mix(dust_mask,metal,0)
    n.channel('grease',grease);n.channel('dust',dust_mask)
    n.channel('chips',chips);n.channel('handling',touch)
    material=n.finish(base,rough,metal,height,coat=coat,anisotropy=.32 if kind=='stainless' else 0)
    n.feed(material.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'],spec)
    material.diffuse_color=(*col,1);material['finish']=kind;material['wear']=wear
    return material


def painted_cast(name,color,wear=.35,rim_bands=(),deposits=(),roughness=.48):
    """Outdoor enamel over sand-cast iron, in an assembly's meter rest frame.

    rim_bands are (height, half-width) wear-prone ledges, not arbitrary patches.
    deposits are the ordinary gravity-track dictionaries. Sun chalking follows
    exposure, splash follows ground height, and chips/rust follow edges/ledges.
    """
    n=Nodes(name);c=common(n);p=c['position']
    grain=n.noise(p,1050,3)
    casting=n.noise(p,390,3)
    height=n.add(n.mul(n.math('SUBTRACT',grain,.5),26e-6),
                 n.mul(n.math('SUBTRACT',casting,.5),45e-6))
    ledges=n.maximum(0,*[n.band(c['z'],z,w,.002) for z,w in rim_bands])
    exposed=n.maximum(c['edge'],n.mul(ledges,.65))
    breakup=n.ramp(n.noise(p,245,4),.57,.71)
    chips=n.mul(wear,exposed,breakup,2.0)
    chalk=n.mul(wear,.30,n.maximum(c['up'],.16),n.ramp(n.noise(p,13,3),.20,.75))
    pale=tuple(v*.73+.13 for v in color)
    base=n.mix(chalk,color,pale,True)
    base=n.mix(chips,base,(.033,.027,.018),True)
    rust=n.mul(chips,n.ramp(n.noise(p,570,3),.32,.64))
    rust_color=n.mix(n.noise(p,850,2),(.065,.021,.006),(.22,.071,.015),True)
    base=n.mix(rust,base,rust_color,True)
    trails=drip_mask(n,c,deposits)
    soil=n.mul(wear,n.maximum(n.mul(c['cavity'],.38),n.mul(trails,.22),
               n.mul(n.ramp(c['z'],.19,.025),.35)),n.ramp(n.noise(p,95,3),.22,.76))
    base=n.mix(soil,base,(.075,.053,.028),True)
    rough=n.add(roughness,n.mul(chalk,.35),n.mul(n.math('SUBTRACT',grain,.5),.055))
    rough=n.mix(chips,rough,.78);rough=n.mix(soil,rough,.85)
    height=n.add(height,n.mul(chips,-.00013),n.mul(rust,.00008))
    n.channel('chips',chips);n.channel('dust',soil)
    mat=n.finish(base,rough,n.mul(chips,n.math('SUBTRACT',1,rust),.45),height)
    mat.diffuse_color=(*color,1);mat['wear']=wear;mat['finish']='painted sand casting'
    return mat


def print_material(name,path,base=None,ink=(.012,.014,.012),rough=.55):
    """Original generated RGBA graphics over a procedural substrate; routable channels."""
    n=Nodes(name);texture=n.node('ShaderNodeTexImage')
    texture.image=bpy.data.images.load(str(path),check_existing=True)
    uv=n.node('ShaderNodeUVMap',uv_map='PrintUV');n.feed(texture.inputs['Vector'],uv.outputs[0])
    if base:
        group=bpy.data.node_groups.new(name+'_substrate','ShaderNodeTree')
        for key in ('base','rough','metal','height'):
            group.interface.new_socket(name=key,in_out='OUTPUT',socket_type='NodeSocketColor' if key=='base' else 'NodeSocketFloat')
        mapping={}
        properties=('operation','data_type','blend_type','clamp_factor','use_clamp','noise_dimensions',
                    'feature','distance','samples','only_local','inside','vector_type',
                    'convert_from','convert_to','attribute_name','attribute_type','object')
        for old in base.node_tree.nodes:
            if old.name in ('OUT','SURFACE') or old.bl_idname=='ShaderNodeBump':continue
            new=group.nodes.new(old.bl_idname);new.name=old.name
            for prop in properties:
                if hasattr(old,prop):setattr(new,prop,getattr(old,prop))
            for destination,source in zip(new.inputs,old.inputs):
                if hasattr(source,'default_value'):
                    try:destination.default_value=source.default_value
                    except (TypeError,ValueError):pass
            for destination,source in zip(new.outputs,old.outputs):
                if hasattr(source,'default_value'):
                    try:destination.default_value=source.default_value
                    except (TypeError,ValueError):pass
            mapping[old]=new
        for link in base.node_tree.links:
            if link.from_node in mapping and link.to_node in mapping:
                group.links.new(mapping[link.from_node].outputs[list(link.from_node.outputs).index(link.from_socket)],
                                mapping[link.to_node].inputs[list(link.to_node.inputs).index(link.to_socket)])
        output=group.nodes.new('NodeGroupOutput')
        for key in ('base','rough','metal','height'):group.links.new(group.nodes['OUT_'+key].outputs[0],output.inputs[key])
        substrate=n.node('ShaderNodeGroup');substrate.node_tree=group
        base_color=n.mix(texture.outputs['Alpha'],substrate.outputs['base'],texture.outputs['Color'],True)
        shader=base.node_tree.nodes['SURFACE']
        result=n.finish(base_color,n.mix(texture.outputs['Alpha'],substrate.outputs['rough'],rough),
                        n.mix(texture.outputs['Alpha'],substrate.outputs['metal'],0),substrate.outputs['height'],
                        coat=shader.inputs['Coat Weight'].default_value,
                        anisotropy=shader.inputs['Anisotropic'].default_value)
        result.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'].default_value=shader.inputs['Specular IOR Level'].default_value
        return result
    return n.finish(texture.outputs['Color'],rough,0)


def combustion(name,wear,role,burner_x=(-.205,0,.205)):
    """Carbon from hot lanes, gravity oil tracks and drain pooling, in meters.

    role: hood (hinge-local frame), bowl or channel (asset frame). The caller
    supplies physical burner positions. Noise only breaks those exposure masks.
    """
    n=Nodes(name);c=common(n);p=c['position'];z=c['z']
    lane=n.maximum(0,*[n.band(c['x'],x,.020,.035) for x in burner_x])
    breakup=n.ramp(n.noise(n.vec('MULTIPLY',p,(1,1,.55)),55,4),.20,.75)
    manufacture=n.noise(p,1800,3)
    if role=='hood':
        spread=n.add(.060,n.mul(n.ramp(z,0,.22),.075))
        plumes=n.maximum(0,*[n.ramp(n.math('DIVIDE',n.math('ABSOLUTE',n.math('SUBTRACT',c['x'],x)),spread),1.3,.45) for x in burner_x])
        thermal_height=n.ramp(z,-.01,.09)
        exposure=n.maximum(n.mul(plumes,.9,thermal_height),n.mul(thermal_height,.30),n.mul(c['cavity'],.85))
        carbon=n.mul(exposure,wear*2.7,breakup)
        base=n.mix(carbon,(.025,.026,.024),(.0015,.0018,.002),True)
        rough=n.mix(carbon,.70,.94)
        oil=n.mul(n.band(z,.015,.014,.018),wear,breakup)
    elif role=='bowl':
        under=n.mul(lane,n.ramp(z,.80,.73))
        drain=n.mul(n.ellipse(p,(0,-.024),(.12,.15),(0,1)),n.ramp(z,.76,.70))
        exposure=n.maximum(n.mul(c['cavity'],.85),n.mul(c['up'],.42),under,drain)
        carbon=n.mul(exposure,wear*2.5,breakup)
        base=n.mix(carbon,(.021,.023,.020),(.0012,.0014,.0012),True)
        rough=n.mix(carbon,.73,.93)
        tracks=drip_mask(n,c,[dict(x=x,z=.887,width=w,length=.19,direction=(0,-1,0)) for x,w in [(-.19,.009),(.07,.006),(.24,.004)]])
        oil=n.mul(n.maximum(drain,tracks,n.mul(c['cavity'],.55)),wear*1.8,breakup)
    elif role=='channel':
        apex=n.band(z,.841,.0015,.006)
        exposure=n.maximum(n.mul(apex,.8),n.mul(lane,.95))
        carbon=n.mul(exposure,wear*2.6,breakup)
        tint=n.mul(exposure,wear,n.ramp(n.noise(p,90,3),.25,.70))
        base=n.mix(tint,(.045,.048,.043),(.11,.068,.025),True)
        base=n.mix(carbon,base,(.0015,.0017,.0015),True)
        rough=n.mix(carbon,.58,.89)
        # Tracks descend the V faces from the apex, varying by channel X.
        warp=n.mul(n.math('SUBTRACT',n.noise(n.vec('MULTIPLY',p,(1,.1,.4)),35,3),.5),.012)
        across=n.add(c['y'],warp)
        streak=n.maximum(0,*[n.band(across,y,.0025,.003) for y in (-.125,-.045,.062,.157)])
        oil=n.mul(streak,n.ramp(z,.808,.819),wear*1.8,n.ramp(n.noise(p,220,3),.2,.7))
    else:raise ValueError(role)
    cracks=n.ramp(n.voronoi(p,95,'DISTANCE_TO_EDGE'),.006,.035)
    height=n.add(n.mul(n.math('SUBTRACT',manufacture,.5),22e-6),n.mul(carbon,cracks,190e-6))
    base=n.mix(oil,base,(.012,.006,.002),True);rough=n.mix(oil,rough,.25)
    height=n.add(height,n.mul(oil,35e-6))
    n.channel('carbon',carbon);n.channel('grease',oil)
    metal=n.mix(n.maximum(carbon,oil),.55 if role=='channel' else 0,0)
    result=n.finish(base,rough,metal,height)
    result.diffuse_color=(.015,.017,.015,1);result['wear']=wear
    return result


def ported_burner(name,wear,burner_z=.770,port_z=.772,pitch=.0118,start=-.209):
    """Dull heat-tinted tube with soot blooms around actual repeated flame ports."""
    n=Nodes(name);c=common(n);p=c['position']
    phase=n.math('FRACT',n.math('DIVIDE',n.math('SUBTRACT',c['y'],start),pitch))
    dy=n.mul(n.math('MINIMUM',phase,n.math('SUBTRACT',1,phase)),pitch)
    dz=n.math('SUBTRACT',c['z'],port_z)
    d2=n.add(n.mul(dy,dy),n.mul(dz,dz))
    nx=n.split(c['normal'])[0]
    side=n.ramp(n.math('ABSOLUTE',nx),.55,.92)
    ports=n.mul(n.ramp(d2,.0018**2,.00075**2),side,n.ramp(c['y'],start-.003,start),n.ramp(c['y'],.218,.205))
    heat=n.mul(n.band(c['z'],burner_z+.003,.006,.004),wear*1.6,n.ramp(n.noise(p,65,3),.25,.7))
    base=n.mix(heat,(.18,.21,.22),(.13,.085,.035),True)
    soot=n.mul(ports,n.maximum(.70,wear*2))
    base=n.mix(soot,base,(.001,.0012,.0012),True)
    rough=n.mix(heat,.67,.77);rough=n.mix(soot,rough,.91)
    metal=n.mix(soot,.85,0)
    height=n.add(n.mul(n.math('SUBTRACT',n.noise(p,2300,2),.5),3e-6),n.mul(ports,-60e-6))
    n.channel('ports',ports);n.channel('heat',heat)
    result=n.finish(base,rough,metal,height);result.diffuse_color=(.08,.09,.09,1)
    return result
