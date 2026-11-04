"""S240 uses the C150 coating method at sedan-specific causal wear heights.

Factory factors and the runtime decoder are identical across the family.
Only original nodes/marking images are used; no photographic pixels enter here.
"""
import bpy
from kit import vehicle_materials as V
from kit.materials import Nodes
import pickup_spec as FAMILY
import sedan_spec as S


def paint(wear):
    mat=V.paint('Alder factory paint',FAMILY.COLORS['Atlantic'],0,
                (S.FRONT_AXLE,S.REAR_AXLE),refined=True,flakes=.65)
    n=Nodes.__new__(Nodes);n.mat=mat;n.nt=mat.node_tree
    p,x,y,z,nx,ny,nz=V.rest(n,'VehicleRest')
    # A deposited film follows grade and tire wakes. The large field is smooth;
    # small directional modulation follows rearward airflow, never isotropic noise.
    low=n.ramp(z,.57,.23)
    fans=[n.mul(low,.34)]
    for axle in [S.FRONT_AXLE,S.REAR_AXLE]:
        dy=n.math('SUBTRACT',y,axle+.24)
        aft=n.mul(n.ramp(dy,-.03,.16),n.ramp(dy,2.4,.50))
        ceiling=n.add(.64,n.mul(dy,-.10))
        rise=n.ramp(n.math('SUBTRACT',ceiling,z),0,.32)
        # Elongated streaks lean downward as the wake travels aft.
        flow=n.combine(n.mul(x,3),n.mul(dy,.7),n.add(n.mul(z,30),n.mul(dy,3)))
        streak=n.add(.90,n.mul(n.noise(flow,1,1),.10))
        fans.append(n.mul(aft,rise,streak,.78))
    film=n.mul(n.maximum(*fans),wear)
    # Cavity residue follows actual shut-line locations, never a panel-wide wash.
    gaps=n.maximum(*[n.band(y,v,.002,.007) for v in [S.DOOR_FRONT,S.DOOR_SPLIT,S.DOOR_REAR]])
    gaps=n.mul(gaps,n.ramp(z,1.02,.94),wear,.32)
    grime=gaps
    leading=n.mul(n.ramp(y,-2.10,-2.29),n.ramp(z,.68,.74),n.ramp(z,.86,.79))
    edges=n.mul(n.maximum(*[n.band(y,v-.004,.001,.003) for v in [S.DOOR_SPLIT,S.DOOR_REAR]]),n.ramp(z,.30,.46),n.ramp(z,1.0,.95))
    chips=n.mul(n.maximum(leading,edges),n.ramp(n.noise(p,780,2),.78,.86),wear)
    coverage=n.mul(n.math('SUBTRACT',1,n.mul(film,.28)),n.math('SUBTRACT',1,grime),n.math('SUBTRACT',1,chips))
    tint=n.nt.nodes['Paint tint'].outputs[0]
    dirt=n.mix(film,(0,0,0),(.009,.0075,.0055),True)
    dirt=n.mix(grime,dirt,(.008,.007,.006),True)
    dirt=n.mix(chips,dirt,(.105,.110,.113),True)
    base=n.vec('ADD',n.mix(coverage,(0,0,0),tint,True),dirt)
    def output(name,socket):n.feed(n.nt.nodes['OUT_'+name].inputs[0],socket)
    # Below one delivered texel, use the integrated clearcoat/flake response.
    # Point sampling 900–2800/m detail into a ~300 px/m atlas aliases to mottles.
    oldrough=.158
    output('height',0)
    for node in n.nt.nodes:
        if node.type=='BUMP':n.feed(node.inputs['Height'],0)
    arcs=n.math('SINE',n.mul(n.voronoi(p,8),3200))
    swirls=n.mul(n.ramp(arcs,.93,.99),n.ramp(n.noise(p,30,2),.57,.70),wear,.018)
    output('base',base);output('rough',n.add(oldrough,n.mul(film,.25),swirls))
    # Road deposits are dielectric; factory metallic remains an independent
    # uniform over the clean coverage, shared by all five colors.
    output('metal',n.mul(coverage,n.nt.nodes['Paint metallic'].outputs[0]))
    output('paint_coverage',coverage);output('paint_contamination',dirt);output('road_film',film);output('chips',chips)
    bs=n.nt.nodes['SURFACE'];n.feed(bs.inputs['Coat Weight'],n.add(.10,n.mul(coverage,.90)))
    n.feed(bs.inputs['Coat Roughness'],n.add(.385,n.mul(coverage,-.35)))
    return mat


def dirty_lower_glass(mat,wear):
    """A faint broken residue at the lower edge; clear main viewing area."""
    n=Nodes.__new__(Nodes);n.mat=mat;n.nt=mat.node_tree
    coord=n.node('ShaderNodeTexCoord');p=coord.outputs['Generated'];_,_,z=n.split(p)
    dust=n.mul(n.ramp(z,.10,.018),n.add(.35,n.mul(n.noise(n.vec('MULTIPLY',p,(2,4,.3)),24,2),.65)),wear,.18)
    base=n.nt.nodes['OUT_base'].inputs[0].links[0].from_socket
    rough=n.nt.nodes['OUT_rough'].inputs[0].links[0].from_socket
    n.feed(n.nt.nodes['OUT_base'].inputs[0],n.mix(dust,base,(.045,.040,.030),True))
    n.feed(n.nt.nodes['OUT_rough'].inputs[0],n.add(rough,n.mul(dust,.35)))
    return mat


def build(wear):
    from finishes import build as family_finishes
    m=family_finishes(0)
    # Reuse the family's responses with sedan axle locations for causal splash.
    for key,color,kind in [('rubber',(.009,.010,.011),'rubber'),('plastic',(.011,.013,.014),'plastic'),('bumper',(.016,.019,.021),'plastic'),('frame',(.008,.009,.010),'plastic')]:
        name=m[key].name;bpy.data.materials.remove(m[key])
        m[key]=V.manufactured(name,color,kind,wear*.8,(S.FRONT_AXLE,S.REAR_AXLE),refined=True)
    bpy.data.materials.remove(m['body'])
    m['body']=paint(wear)
    m['wheel']=V.manufactured('S240 cast alloy',(.23,.24,.25),'alloy',wear,
        brake_centers=[(sign*track/2,y,S.HUB_HEIGHT) for sign in [-1,1]
                       for track,y in [(S.FRONT_TRACK,S.FRONT_AXLE),(S.REAR_TRACK,S.REAR_AXLE)]],refined=True)
    m['glass']=V.glazing('S240 windshield',(.48,.54,.55))
    m['side_glass']=V.glazing('S240 front door glass',(.30,.38,.39),axes=(1,2))
    m['privacy']=V.glazing('S240 rear door glass',(.11,.15,.16),True,axes=(1,2))
    m['rear_glass']=V.glazing('S240 backlight',(.14,.19,.20),True)
    for key in ['glass','side_glass','privacy','rear_glass']:dirty_lower_glass(m[key],wear)
    m['rear_cover']=V.lamp('S240 red lamp cover',(.55,.010,.006),0,1)
    m['rear_cover'].node_tree.nodes['OUT_rough'].inputs[0].links[0].from_socket.default_value=.045
    from pathlib import Path
    directory=Path(__file__).resolve().parents[1]/'build/sedan/markings'
    image=bpy.data.images.load(str(directory/'model.png'),check_existing=True)
    n=Nodes('S240 original model');tex=n.node('ShaderNodeTexImage');tex.image=image
    m['model']=n.finish(tex.outputs['Color'],.25,.8)
    image=bpy.data.images.load(str(directory/'dealer.png'),check_existing=True)
    n=Nodes('S240 dealer insert');tex=n.node('ShaderNodeTexImage');tex.image=image
    uv=n.node('ShaderNodeTexCoord');n.feed(tex.inputs['Vector'],uv.outputs['UV'])
    x,y,z=n.split(uv.outputs['UV'])
    edge=n.maximum(n.ramp(x,.045,.025),n.ramp(x,.955,.975),n.ramp(y,.11,.08),n.ramp(y,.85,.90))
    m['dealer']=n.finish(tex.outputs['Color'],n.mix(edge,.36,.21),n.mul(edge,.35),n.mul(edge,.0012))
    # Recessed diamond relief behind the vertical cascade vanes, gloss black.
    n=Nodes('S240 grille lattice');tc=n.node('ShaderNodeTexCoord');u,v,_=n.split(tc.outputs['UV'])
    lines=[]
    for diagonal in [n.add(n.mul(u,44),n.mul(v,6)),n.add(n.mul(u,44),n.mul(v,-6))]:
        wave=n.math('PINGPONG',diagonal,1);lines.append(n.ramp(wave,.84,.96))
    bars=n.maximum(*lines)
    m['grille']=n.finish(n.mix(bars,(.003,.004,.004),(.014,.018,.018),True),n.mix(bars,.35,.14),n.mul(bars,.35),n.mul(bars,.00018))
    m['grille_bar']=V.manufactured('S240 gloss black grille',(.012,.015,.016),'chrome',0,refined=True)
    n=Nodes.__new__(Nodes);n.mat=m['grille_bar'];n.nt=n.mat.node_tree;n.feed(n.nt.nodes['OUT_rough'].inputs[0],.14)
    for side in ['L','R']:
        image=bpy.data.images.load(str(directory/'tire_relief.png'),check_existing=True)
        image.colorspace_settings.name='Non-Color'
        m['tire_'+side]=touring_tire('S240 lettered tire '+side,image,-1 if side=='L' else 1,wear)
    return m


def touring_tire(name,image,sign,wear):
    """Native passenger-tire dimensions; type is molded rubber, never white ink."""
    n=Nodes(name);tc=n.node('ShaderNodeTexCoord');p=tc.outputs['Object'];x,y,z=n.split(p)
    ax=n.math('ABSOLUTE',x);r=n.math('SQRT',n.add(n.mul(y,y),n.mul(z,z)))
    angle=n.math('ARCTAN2',z,y)
    tread=n.mul(n.ramp(ax,.105,.080),n.ramp(r,.306,.324))
    phase=n.add(n.mul(angle,52/6.283185307179586),n.mul(x,18))
    blocks=n.mul(n.ramp(n.math('FRACT',phase),.10,.18),n.ramp(n.math('FRACT',phase),.94,.86))
    lanes=n.ramp(n.math('ABSOLUTE',n.math('SUBTRACT',n.math('FRACT',n.mul(x,28)),.5)),.45,.34)
    tex=n.node('ShaderNodeTexImage');tex.image=image;tex.extension='CLIP';tex.interpolation='Linear'
    n.feed(tex.inputs['Vector'],n.combine(n.add(.5,n.mul(y,sign/.81)),n.add(.5,n.mul(z,1/.81)),0))
    side=n.mul(n.ramp(ax,.090,.114),n.ramp(r,.238,.254),n.ramp(r,.315,.302))
    type_relief=n.mul(tex.outputs['Color'],side)
    height=n.add(n.mul(tread,blocks,lanes,.0018),n.mul(type_relief,.00065))
    dust=n.mul(side,n.ramp(r,.247,.278),wear,.20)
    base=n.mix(dust,(.0050,.0055,.0060),(.035,.030,.023),True)
    base=n.vec('ADD',base,n.mix(type_relief,(0,0,0),(.0018,.0017,.0015),True))
    mat=n.finish(base,.77,0,height);mat.diffuse_color=(.010,.011,.012,1)
    return mat
