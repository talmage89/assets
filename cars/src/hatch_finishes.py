"""H120 uses the C150 coating method at hatch-specific causal wear heights.

Factory factors and the runtime decoder are identical across the family.
Only original nodes/marking images are used; no photographic pixels enter here.
"""
import bpy
from kit import vehicle_materials as V
from kit.materials import Nodes
import pickup_spec as FAMILY
import hatch_spec as S


def paint(wear):
    mat=V.paint('Alder factory paint',FAMILY.COLORS['Atlantic'],0,
                (S.FRONT_AXLE,S.REAR_AXLE),refined=True,flakes=.65)
    n=Nodes.__new__(Nodes);n.mat=mat;n.nt=mat.node_tree
    p,x,y,z,nx,ny,nz=V.rest(n,'VehicleRest')
    streaks=n.noise(n.vec('MULTIPLY',p,(1,1,.55)),35,3)
    grain=n.add(.85,n.mul(n.noise(p,270,2),.15))
    ceiling=n.add(.29,n.mul(n.noise(p,7,2),.05))
    fans=[n.mul(n.ramp(n.math('SUBTRACT',ceiling,z),0,.22),.45)]
    for axle in [S.FRONT_AXLE,S.REAR_AXLE]:
        dy=n.math('SUBTRACT',y,axle+.25)
        aft=n.mul(n.ramp(dy,0,.12),n.ramp(dy,2.60,1.50))
        ceiling=n.add(n.add(.52,n.mul(n.noise(p,7,2),.020)),n.mul(dy,-.035))
        fans.append(n.mul(aft,n.ramp(n.math('SUBTRACT',ceiling,z),0,.23),.85))
    film=n.mul(n.maximum(*fans),grain,wear,.65)
    loading=n.mul(n.ramp(y,1.98,2.10),n.band(z,.615,.012,.040),n.ramp(n.math('ABSOLUTE',x),.62,.46),wear)
    abrasion=n.mul(loading,n.ramp(n.noise(n.vec('MULTIPLY',p,(.25,4,2)),420,2),.70,.81),.20)
    # Cavity residue follows actual shut-line locations, never a panel-wide wash.
    gaps=n.maximum(*[n.band(y,v,.002,.007) for v in [S.DOOR_FRONT,S.DOOR_SPLIT,S.DOOR_REAR]])
    gaps=n.mul(gaps,n.ramp(z,1.02,.94),wear,.32)
    grime=gaps
    leading=n.mul(n.ramp(y,-1.82,-2.04),n.ramp(z,.68,.74),n.ramp(z,.86,.79))
    edges=n.mul(n.maximum(*[n.band(y,v-.004,.001,.003) for v in [S.DOOR_SPLIT,S.DOOR_REAR]]),n.ramp(z,.30,.46),n.ramp(z,1.0,.95))
    chips=n.mul(n.maximum(leading,edges),n.ramp(n.noise(p,780,2),.78,.86),wear)
    coverage=n.mul(n.math('SUBTRACT',1,film),n.math('SUBTRACT',1,grime),n.math('SUBTRACT',1,chips))
    tint=n.nt.nodes['Paint tint'].outputs[0]
    dirt=n.mix(film,(0,0,0),(.095,.082,.064),True)
    dirt=n.mix(grime,dirt,(.008,.007,.006),True)
    dirt=n.mix(chips,dirt,(.105,.110,.113),True)
    base=n.vec('ADD',n.mix(coverage,(0,0,0),tint,True),dirt)
    def output(name,socket):n.feed(n.nt.nodes['OUT_'+name].inputs[0],socket)
    oldrough=n.nt.nodes['OUT_rough'].inputs[0].links[0].from_socket
    arcs=n.math('SINE',n.mul(n.voronoi(p,8),3200))
    swirls=n.mul(n.ramp(arcs,.93,.99),n.ramp(n.noise(p,30,2),.57,.70),wear,.018)
    output('base',base);output('rough',n.add(oldrough,n.mul(film,.25),swirls,abrasion))
    output('paint_coverage',coverage);output('paint_contamination',dirt);output('road_film',film);output('chips',chips)
    bs=n.nt.nodes['SURFACE'];n.feed(bs.inputs['Coat Weight'],n.add(.10,n.mul(coverage,.90)))
    n.feed(bs.inputs['Coat Roughness'],n.add(.035,n.mul(film,.35),swirls))
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
    # Reuse the family's responses with hatch axle locations for causal splash.
    for key,color,kind in [('rubber',(.009,.010,.011),'rubber'),('plastic',(.011,.013,.014),'plastic'),('bumper',(.016,.019,.021),'plastic'),('frame',(.008,.009,.010),'plastic')]:
        name=m[key].name;bpy.data.materials.remove(m[key])
        m[key]=V.manufactured(name,color,kind,wear*.8,(S.FRONT_AXLE,S.REAR_AXLE),refined=True)
    bpy.data.materials.remove(m['body'])
    m['body']=paint(wear)
    m['wheel']=V.manufactured('H120 cast alloy',(.23,.24,.25),'alloy',wear,
        brake_centers=[(sign*track/2,y,S.HUB_HEIGHT) for sign in [-1,1]
                       for track,y in [(S.FRONT_TRACK,S.FRONT_AXLE),(S.REAR_TRACK,S.REAR_AXLE)]],refined=True)
    m['glass']=V.glazing('H120 windshield',(.90,.93,.94))
    m['side_glass']=V.glazing('H120 front door glass',(.503,.573,.593),axes=(1,2))
    m['privacy']=V.glazing('H120 rear door glass',(.82,.86,.88),False,axes=(1,2))
    m['rear_glass']=V.glazing('H120 backlight',(.98,.99,.99),False)
    for key in ['glass','side_glass','privacy','rear_glass']:dirty_lower_glass(m[key],wear)
    m['rear_cover']=V.lamp('H120 red lamp cover',(.55,.010,.006),0,1)
    m['rear_cover'].node_tree.nodes['OUT_rough'].inputs[0].links[0].from_socket.default_value=.045
    from pathlib import Path
    directory=Path(__file__).resolve().parents[1]/'build/hatch-detail/markings'
    image=bpy.data.images.load(str(directory/'model.png'),check_existing=True)
    n=Nodes('H120 original model');tex=n.node('ShaderNodeTexImage');tex.image=image
    m['model']=n.finish(tex.outputs['Color'],.25,.8)
    image=bpy.data.images.load(str(directory/'dealer.png'),check_existing=True)
    n=Nodes('H120 dealer insert');tex=n.node('ShaderNodeTexImage');tex.image=image
    uv=n.node('ShaderNodeTexCoord');n.feed(tex.inputs['Vector'],uv.outputs['UV'])
    x,y,z=n.split(uv.outputs['UV'])
    edge=n.maximum(n.ramp(x,.045,.025),n.ramp(x,.955,.975),n.ramp(y,.11,.08),n.ramp(y,.85,.90))
    m['dealer']=n.finish(tex.outputs['Color'],n.mix(edge,.36,.21),n.mul(edge,.35),n.mul(edge,.0012))
    # The open webs are geometric. Their recessed radiator bed stays matte
    # and nearly black, rather than carrying a second, bumped lattice.
    n=Nodes('H120 intake cavity')
    m['grille']=n.finish((.0015,.0017,.0018),.94,0)
    m['grille_bar']=V.manufactured('H120 gloss black grille',(.012,.015,.016),'chrome',0,refined=True)
    n=Nodes.__new__(Nodes);n.mat=m['grille_bar'];n.nt=n.mat.node_tree;n.feed(n.nt.nodes['OUT_rough'].inputs[0],.14);n.feed(n.nt.nodes['OUT_metal'].inputs[0],0)
    for side in ['L','R']:
        # The family's original fictional lettering is the only relief image.
        image=bpy.data.images.load(str(directory/'tire_relief.png'),check_existing=True)
        image.colorspace_settings.name='Non-Color'
        # Rebuild with that image so no geometry is spent on type.
        if image:
            m['tire_'+side]=V.tire('H120 lettered tire '+side,None,-1 if side=='L' else 1,wear=wear)
            nt=m['tire_'+side].node_tree
            # The class photos show dark dusty rubber, rather than a pale tire
            # annulus. Preserve the radial cause and reduce its reflected value.
            n=Nodes.__new__(Nodes);n.mat=m['tire_'+side];n.nt=nt
            base=nt.nodes['OUT_base'].inputs[0].links[0].from_socket
            n.feed(nt.nodes['OUT_base'].inputs[0],n.vec('MULTIPLY',base,(.55,.55,.55)))
            tc=next(t for t in nt.nodes if t.type=='TEX_COORD')
            links=list(tc.outputs['Object'].links);scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='MULTIPLY'
            scale.inputs[1].default_value=(.275/.225,FAMILY.HUB_HEIGHT/S.HUB_HEIGHT,FAMILY.HUB_HEIGHT/S.HUB_HEIGHT)
            nt.links.new(tc.outputs['Object'],scale.inputs[0])
            for link in links:nt.links.new(scale.outputs[0],link.to_socket)
            # Passenger-sidewall lettering uses its measured 273 mm annulus;
            # the truck's global tread coordinates would bury it at the bead.
            local=n.node('ShaderNodeTexCoord');x,y,z=n.split(local.outputs['Object'])
            radius=n.math('SQRT',n.add(n.mul(y,y),n.mul(z,z)))
            embossed=n.node('ShaderNodeTexImage');embossed.image=image;embossed.extension='CLIP'
            sign=-1 if side=='L' else 1
            n.feed(embossed.inputs['Vector'],n.combine(n.add(.5,n.mul(y,sign*1.26)),n.add(.5,n.mul(z,1.26)),0))
            coverage=n.mul(n.ramp(n.math('ABSOLUTE',x),.093,.108),n.ramp(radius,.241,.248),n.ramp(radius,.307,.297))
            # Raised molded type catches a little pale road dust. This faint
            # deposit also survives minification when the relief is subtexel.
            glyph=n.mul(coverage,embossed.outputs['Color'])
            rubber=nt.nodes['OUT_base'].inputs[0].links[0].from_socket
            n.feed(nt.nodes['OUT_base'].inputs[0],n.vec('ADD',rubber,n.mix(n.mul(glyph,wear),(0,0,0),(.020,.018,.014),True)))
            old=nt.nodes['OUT_height'].inputs[0].links[0].from_socket
            n.feed(nt.nodes['OUT_height'].inputs[0],n.add(old,n.mul(glyph,.0005)))
    return m
