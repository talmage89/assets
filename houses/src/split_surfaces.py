"""Cape-calibrated finishes plus split-specific moisture and vehicle sites.

Fine manufacture remains in the existing family tiles. All extra weather is
source procedural detail; it has not been baked into a delivery texture.
"""
from kit.materials import Nodes
from cape_surfaces import layer as cape_layer,attr

# Body-only changes preserve the Cape brick's neutral mortar. Palette controls
# are linear RGB factors, never pixel colors sampled from a photograph.
BRICK_BODY={51:(1.06,.68,.245),53:(.67,.59,.36),54:(1.00,1.0,.93),55:(2.30,2.35,1.06),56:(1.55,1.95,1.05)}


def layer(mat,role,meta):
    cape_layer(mat,role,meta,roof_shade=True,lap_exposure_m=.2032 if meta['spec']['siding']=='aluminum' else None)
    n=Nodes.__new__(Nodes);n.mat=mat;n.nt=mat.node_tree;p=n.nt.nodes.get('Principled BSDF')
    if role=='Glass':
        for link in list(p.inputs['Normal'].links):n.nt.links.remove(link)
        return
    def value(key):
        socket=p.inputs[key];return socket.links[0].from_socket if socket.is_linked else socket.default_value
    base=value('Base Color');rough=value('Roughness');normal=value('Normal')
    previous_height=n.nt.nodes.get('OUT_height')
    previous_height=previous_height.outputs[0] if previous_height else 0
    for node in list(n.nt.nodes):
        if node.name in ('OUT_base','OUT_rough','OUT_height'):node.name='Cape_'+node.name
    def minimum(a,b):return n.math('MINIMUM',a,b)
    x,y,z=n.split(attr(n,'SplitRest'));bottom,eave,old=n.split(attr(n,'CapeContext'))
    nx,ny,nz=n.split(n.node('ShaderNodeNewGeometry').outputs['True Normal'])
    north=n.ramp(ny,-.15,.55);sun=n.maximum(n.ramp(ny,.15,-.75),n.mul(n.ramp(nx,.2,-.8),.55))
    rest=attr(n,'SplitRest');broad=n.noise(rest,4.5,3);grain=n.noise(n.vec('MULTIPLY',rest,(18,18,.28)),32,2)
    breakup=n.ramp(broad,.32,.68);wet=0;overflow=0
    # Continuous meter-scale runoff beneath actual sills and gutter endpoints.
    for opening in meta['openings']:
        if opening['kind']!='window':continue
        block=next(b for b in meta['blocks'] if b['name']==opening['block'])
        face=opening['face'];front_back=face in ('front','back')
        plane=block['y0'] if face=='front' else block['y1'] if face=='back' else block['x0'] if face=='left' else block['x1']
        on=n.ramp(n.math('ABSOLUTE',n.add(y if front_back else x,-plane)),.25,.045)
        below=n.mul(n.ramp(z,opening['z']+.01,opening['z']-.06),n.ramp(z,opening['z']-1.4,opening['z']-.24))
        origin=block['x0' if front_back else 'y0'];u=x if front_back else y
        for sign in (-1,1):
            center=origin+opening['u']+sign*opening['w']*.45
            trail=n.ramp(n.math('ABSOLUTE',n.add(u,-center)),.14,.018)
            wet=n.maximum(wet,n.mul(on,below,trail))
    for drain in meta['drains']:
        q=drain['centerline'][3]
        xy=n.combine(x,y,0);near=n.ramp(n.vec('DISTANCE',xy,(q[0],q[1],0)),.42,.025)
        wet=n.maximum(wet,n.mul(near,n.ramp(z,q[2]+.06,q[2]-.10)))
        for q in drain['gutter']:
            below=n.math('SUBTRACT',q[2],z)
            trail=n.mul(n.ramp(n.vec('DISTANCE',xy,(q[0],q[1],0)),.42,.025),n.ramp(below,-.05,.08),n.ramp(below,1.1,.12))
            overflow=n.maximum(overflow,trail)
    height=0
    if role in ('Siding','Concrete','Trim','Veneer'):
        # Splash from the raised landing has a real contact surface. Tall
        # cladding above masonry must not receive a fictitious grade dirt band.
        main=meta['blocks'][0];xy=n.combine(x,y,0)
        landing=n.ramp(n.vec('DISTANCE',xy,(meta['door_x'],main['y0'],0)),1.05,.20)
        splash=n.mul(landing,n.ramp(n.add(z,-meta['levels']['living']),.34,.02),n.ramp(n.add(z,-meta['levels']['living']),-.08,.025),breakup,.35)
        base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(splash,-.40)),n.add(1,n.mul(splash,-.47)),n.add(1,n.mul(splash,-.55))))
    if role=='Veneer':
        uv=n.node('ShaderNodeTexCoord').outputs['UV'];u,v,_=n.split(uv)
        if meta['spec']['veneer']=='brick':
            # Analytic joint locator is the original modular Cape bond.
            zz=n.mul(v,.2032/3*8);row=n.math('FLOOR',n.math('DIVIDE',zz,.2032/3))
            parity=n.mul(n.math('FRACT',n.math('DIVIDE',row,2)),2)
            uu=n.add(n.mul(u,.6096),n.mul(parity,.1016))
            # Shader MODULO truncates negative U; FRACT gives the periodic
            # positive cell coordinate on both sides of the asset origin.
            xx=n.mul(n.math('FRACT',n.math('DIVIDE',uu,.2032)),.2032)
            yy=n.mul(n.math('FRACT',n.math('DIVIDE',zz,.2032/3)),.2032/3)
            edge=minimum(minimum(xx,n.add(.2032,n.mul(xx,-1))),minimum(yy,n.add(.2032/3,n.mul(yy,-1))))
            body=n.ramp(edge,.003,.008)
            factors=BRICK_BODY.get(meta['seed'],BRICK_BODY[51])
            altered=n.vec('MULTIPLY',base,factors)
            if (meta['seed']-51)%6==3:
                fired=n.node('ShaderNodeTexWhiteNoise');n.feed(fired.inputs['Vector'],n.combine(n.math('FLOOR',n.math('DIVIDE',uu,.2032)),row,0));unit=fired.outputs['Value']
                tone=n.mix(n.ramp(unit,0,.55),(.08,.095,.065),(.65,.74,.46),color=True)
                tone=n.mix(n.ramp(unit,.55,1),tone,(1.50,1.70,1.00),color=True)
                altered=n.vec('MULTIPLY',base,tone)
            base=n.mix(body,base,altered,color=True)
        # Rain-darkened bodies and broken, chalky salt fronts remain localized.
        low=n.ramp(n.add(z,-meta['spec']['site_grade_m']),.38,.035)
        moisture=n.mul(n.maximum(n.mul(low,.68),wet),n.add(.38,n.mul(breakup,.62)))
        base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(moisture,-.40)),n.add(1,n.mul(moisture,-.37)),n.add(1,n.mul(moisture,-.33))))
        salts=n.mul(n.maximum(n.mul(low,.25),n.mul(wet,.75)),n.band(broad,.57,.045,.018),.22)
        base=n.mix(salts,base,(.52,.51,.47),color=True)
        mildew=n.mul(n.maximum(north,n.mul(n.ramp(nx,0,.8),.6)),low,breakup,.38)
        base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(mildew,-.55)),n.add(1,n.mul(mildew,-.40)),n.add(1,n.mul(mildew,-.51))))
        height=n.mul(salts,.0003);rough=n.add(rough,n.mul(moisture,.04))
    if role=='Siding' and meta['spec']['siding']=='battens':
        base=n.vec('MULTIPLY',base,n.mix(grain,(.95,.95,.94),(1.04,1.04,1.025),color=True))
        rough=n.add(.67,n.mul(breakup,.13));height=n.mul(grain,.00009)
        peel=n.mul(old,wet,n.ramp(grain,.59,.73),.65)
        base=n.mix(peel,base,(.205,.216,.211),color=True)
        height=n.add(height,n.mul(peel,-.0006))
    if role=='Siding' and meta['spec']['siding']=='wood':
        along=n.mix(n.ramp(n.math('ABSOLUTE',ny),.2,.7),y,x)
        row=n.math('FLOOR',n.math('DIVIDE',z,.1016));board=n.math('FLOOR',n.math('DIVIDE',along,2.44))
        coats=n.noise(n.combine(board,row,meta['seed']),1,0)
        variation=n.add(.55,n.mul(coats,.90))
        base=n.vec('MULTIPLY',base,n.combine(variation,variation,variation))
    if role=='Trim':
        garage=attr(n,'SplitGarage','Fac');paint=attr(n,'SplitPaint','Fac')
        rough=n.mix(attr(n,'SplitVinyl','Fac'),rough,.40)
        # The lowest section catches road film; fresh replacement doors retain
        # their higher paint value, while old sunny steel loses gloss/chroma.
        garage_opening=next((o for o in meta['openings'] if o['kind']=='garage'),None)
        if garage_opening:
            low=n.ramp(n.add(z,-garage_opening['z']),.48,.025)
            soil=n.mul(garage,low,n.add(.48,n.mul(breakup,.50)))
            base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(soil,-.52)),n.add(1,n.mul(soil,-.49)),n.add(1,n.mul(soil,-.46))))
            fade=n.mul(garage,sun,.22 if meta['spec']['roof_age']=='tired' else .07)
            base=n.mix(fade,base,n.vec('ADD',n.vec('MULTIPLY',base,(.80,.80,.80)),(.09,.09,.085)),color=True)
            rough=n.mix(garage,rough,n.add(.52,n.mul(soil,.25)))
            if meta['spec']['garage']['condition']=='bottom_section':
                replaced=n.ramp(n.add(z,-garage_opening['z']),garage_opening['h']/4+.004,garage_opening['h']/4-.004)
                coat=n.mix(replaced,.86,1.40)
                base=n.vec('MULTIPLY',base,n.mix(garage,(1,1,1),n.combine(coat,coat,coat),color=True))
        runs=n.mul(overflow,paint,.47,breakup)
        base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(runs,-.65)),n.add(1,n.mul(runs,-.61)),n.add(1,n.mul(runs,-.56))))
    if role=='Concrete':
        drive=attr(n,'SplitDrive','Fac');retaining=attr(n,'SplitRetaining','Fac');d=meta['driveway']
        off=n.add(x,-d['x']);distance=n.math('ABSOLUTE',off)
        tracks=n.ramp(n.math('ABSOLUTE',n.add(distance,-.76)),.21,.06)
        parking=n.ramp(n.math('ABSOLUTE',n.add(y,-d['back']+3.0)),3.8,.65)
        edge=n.ramp(distance,d['width']/2-.38,d['width']/2-.05)
        # Engine/drivetrain drips join into irregular lobes at the parked bay,
        # with separate short tire contact paths rather than two black stripes.
        engine=n.mul(n.ramp(n.math('ABSOLUTE',n.add(off,-.14)),.55,.12),n.ramp(n.math('ABSOLUTE',n.add(y,-d['back']+3.4)),1.15,.25),n.ramp(broad,.36,.65))
        marks=n.mul(drive,n.maximum(n.mul(tracks,parking,.31),n.maximum(n.mul(engine,.78),n.mul(edge,.30))))
        base=n.vec('MULTIPLY',base,n.combine(n.add(1,n.mul(marks,-.79)),n.add(1,n.mul(marks,-.77)),n.add(1,n.mul(marks,-.73))))
        # Hairline cracks grow from authored control joints, with spalled lips.
        yy=n.add(y,-d['front']);phase=n.math('MODULO',yy,2.4)
        joint=n.ramp(minimum(phase,n.add(2.4,n.mul(phase,-1))),.012,.003)
        branch=n.math('ABSOLUTE',n.add(off,n.mul(n.noise(n.combine(0,y,0),3,2),.18),-.09))
        crack=n.mul(n.ramp(branch,.012,.0025),n.ramp(minimum(phase,n.add(2.4,n.mul(phase,-1))),.50,.05))
        cut=n.mul(drive,n.maximum(joint,crack));base=n.mix(n.mul(cut,.74),base,(.035,.033,.028),color=True)
        height=n.add(height,n.mul(cut,-.0022))
        base_stain=n.mul(retaining,n.ramp(n.add(z,-d['back_z']),.42,.03),breakup,.45)
        base=n.vec('MULTIPLY',base,n.add(1,n.mul(base_stain,-.64)))
    n.feed(p.inputs['Base Color'],n.channel('base',base));n.feed(p.inputs['Roughness'],n.channel('rough',rough))
    bump=n.node('ShaderNodeBump');bump.inputs['Strength'].default_value=.65;bump.inputs['Distance'].default_value=1
    n.feed(bump.inputs['Height'],n.channel('split_height',height))
    n.channel('height',n.add(previous_height,height))
    if hasattr(normal,'is_output'):n.feed(bump.inputs['Normal'],normal)
    n.feed(p.inputs['Normal'],bump.outputs[0])
