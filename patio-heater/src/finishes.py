"""Original manufacturing and cause-driven masks; no reference image inputs."""
import math
from kit.materials import Nodes,common,surface

def _rest(n,c,door=False):
    """Assembly-local shader coordinates reconstructed into the closed rest frame."""
    x,y,z=n.split(c['position'])
    if door:x=n.add(x,-.189);y=n.add(y,-.115);z=n.add(z,.435)
    p=n.combine(x,y,z)
    radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(y,y)))
    return p,x,y,z,radius

def _oxide(n,p):
    # Millimeter-scale variation inside already located corrosion, never a
    # whole-object noise wash. Dark oxide edges and orange porous bloom.
    return n.mix(n.ramp(n.noise(p,210,3),.30,.73),(.085,.026,.008),(.28,.105,.024),True)

def _radial_track(n,x,y,angle,width):
    a=math.radians(angle)
    along=n.add(n.mul(x,math.cos(a)),n.mul(y,math.sin(a)))
    cross=n.add(n.mul(x,-math.sin(a)),n.mul(y,math.cos(a)))
    return n.mul(n.band(cross,0,width,width*.6),n.ramp(along,0,.04))

def paint(wear,door=False):
    n=Nodes('Patio-season powder coat'+(' door' if door else ''))
    c=common(n);p,x,y,z,r=_rest(n,c,door);age=min(2,wear/.35)
    nz=n.split(c['normal'])[2]
    up=n.ramp(nz,.22,.86)
    # UV exposure follows the up-facing shoulder and base pan; vertical sides
    # see only a small diffuse-sky component. Broad manufacturing-scale breakup
    # varies the fade without turning every face into mottled grime.
    sky=n.maximum(up,n.mul(n.ramp(z,.14,.78),.15))
    chalk=n.mul(age,.68,sky,n.add(.80,n.mul(n.noise(p,18,2),.28)))
    base=n.mix(chalk,(.041,.052,.049),(.145,.165,.145),True)
    # The outer base lip is dragged; rear wheel neighborhoods are tipped against
    # paving. Long tangential scrapes expose primer and steel in 3--15 mm marks.
    lip=n.mul(n.band(r,.224,.005,.010),n.band(z,.016,.013,.010))
    wheel=n.maximum(*[n.ellipse(p,(a,.194),(.070,.080),axes=(0,1)) for a in (-.173,.173)])
    wheel=n.mul(wheel,n.ramp(z,.115,.035))
    scratch=n.ramp(n.noise(n.vec('MULTIPLY',p,(38,38,430)),1,2),.47,.65)
    intermittent=n.ramp(n.noise(p,52,3),.37,.67)
    dragged=n.mul(n.maximum(lip,wheel),scratch,intermittent,age)
    # Moisture held in the folded bottom edge breaks paint along the door hem.
    hem=n.mul(n.band(z,.098,.005,.012),n.ramp(n.noise(p,88,3),.40,.66)) if door else 0
    # Fingers and a rotating latch abrade a small region around its real bezel.
    dx=n.math('SUBTRACT',x,.1593);dz=n.math('SUBTRACT',z,.435)
    latchdist=n.math('SQRT',n.add(n.mul(dx,dx),n.mul(dz,dz)))
    face=n.band(y,-.134,.020,.018)
    touch=n.mul(n.ramp(latchdist,.049,.016),face) if door else 0
    latcharc=n.mul(n.band(latchdist,.021,.004,.005),face) if door else 0
    latchchips=n.mul(latcharc,n.ramp(n.noise(n.vec('MULTIPLY',p,(110,180,240)),1,2),.46,.66),age,.82)
    edgechips=n.mul(c['edge'],n.ramp(n.noise(p,95,2),.48,.67),age,.30)
    chips=n.maximum(dragged,n.mul(hem,age,.85),latchchips,edgechips)
    primer=n.ramp(chips,.05,.40)
    base=n.mix(primer,base,(.12,.12,.094),True)
    base=n.mix(n.ramp(chips,.25,.72),base,(.25,.27,.255),True)
    # Rust stays at exposed chips, real floor drains and the wet door hem.
    # Drain runoff follows the slope from the three bores at -135/-90/-45 deg.
    drain=n.maximum(*[_radial_track(n,x,y,a,.004) for a in (-135,-90,-45)])
    drain=n.mul(drain,n.ramp(r,.178,.206),n.ramp(z,.066,.008),
        n.ramp(n.noise(n.vec('MULTIPLY',p,(80,80,110)),1,3),.29,.63))
    hem_bloom=n.mul(n.band(z,.104,.007,.018),n.ramp(n.noise(p,45,3),.44,.68)) if door else 0
    rusty_chips=n.mul(chips,n.ramp(n.noise(p,66,3),.41,.68),.72)
    rust=n.maximum(rusty_chips,n.mul(drain,age,.72),n.mul(hem_bloom,age,.70))
    base=n.mix(rust,base,_oxide(n,p),True)
    # Short gravity runs below the door's wet hem, and radial runoff from the
    # three pole-flange screws onto the painted shoulder.
    flange=n.maximum(*[_radial_track(n,x,y,a,.004) for a in (30,150,270)])
    flange=n.mul(flange,n.ramp(r,.047,.060),n.ramp(r,.14,.085),n.band(z,.811,.013,.014),age,.58)
    base=n.mix(flange,base,_oxide(n,p),True)
    dust=n.mul(n.ramp(z,.20,.035),age,.18,n.ramp(n.noise(p,38,2),.25,.65))
    base=n.mix(dust,base,(.095,.080,.050),True)
    # Handling rub is slightly polished; chalk, deposits and oxide are rough.
    rough=n.add(.49,n.mul(chalk,.21),n.mul(rust,.23),n.mul(dust,.14))
    rough=n.mix(n.mul(touch,age,.38),rough,.35)
    metal=n.mul(n.ramp(chips,.25,.72),n.math('SUBTRACT',1,rust),.85)
    micro=n.mul(n.math('SUBTRACT',n.noise(p,1600,2),.5),13e-6)
    height=n.add(micro,n.mul(chips,-45e-6),n.mul(rust,35e-6))
    for name,mask in [('chalk',chalk),('drag_scuff',dragged),('latch_wear',latchchips),('rust',rust),('drain_runoff',drain)]:n.channel(name,mask)
    return n.finish(base,rough,metal,height)

def hardware(wear):
    """Plated fastener corrosion collects in tool recesses and head edges."""
    n=Nodes('Outdoor plated fasteners / crevice oxide');c=common(n);p=c['position'];age=min(2,wear/.35)
    crevice=n.maximum(c['cavity'],n.mul(c['edge'],.55))
    rust=n.mul(age,crevice,n.ramp(n.noise(p,310,2),.38,.67),.72)
    base=n.mix(rust,(.38,.40,.40),_oxide(n,p),True)
    return n.finish(base,n.mix(rust,.38,.83),n.mix(rust,1,.05),n.mul(rust,18e-6))

def latch_handle(wear):
    """Finger-burnished ABS with pale edge scratches, in the door rest frame."""
    n=Nodes('Latch handle / touched and abraded ABS');c=common(n);p=c['position'];age=min(2,wear/.35)
    cuts=n.mul(age,c['edge'],n.ramp(n.noise(n.vec('MULTIPLY',p,(150,120,450)),1,2),.38,.63))
    base=n.mix(cuts,(.008,.011,.009),(.15,.16,.14),True)
    return n.finish(base,n.mix(min(1,age*.65),.60,.33),0,n.mul(cuts,-18e-6))

def thermal(name,wear,role):
    n=Nodes(name);c=common(n);p=c['position'];x,y,z=n.split(p)
    radial=n.math('SQRT',n.add(n.mul(x,x),n.mul(y,y)))
    if role=='hood':
        # Hot exhaust rises above emitter, spreads radially on the underside.
        downward=n.ramp(n.split(c['normal'])[2],-.15,-.9)
        hot=n.mul(downward,n.ramp(radial,.36,.07),min(1,wear*2.8))
    else:hot=n.mul(n.band(z,2.011,.065,.055),min(1,wear*2.8))
    base=n.mix(n.ramp(hot,.03,.22),(.43,.46,.47),(.34,.235,.105),True)
    base=n.mix(n.band(hot,.42,.10,.14),base,(.18,.115,.115),True)
    base=n.mix(n.ramp(hot,.45,.82),base,(.105,.17,.245),True)
    grain=n.noise(n.vec('MULTIPLY',p,(40,40,1800)),1,2)
    rough=n.add(.32,n.mul(hot,.18),n.mul(grain,.08));metal=1;height=n.mul(grain,1.2e-6)
    if role=='hood':
        age=min(2,wear/.35);up=n.ramp(n.split(c['normal'])[2],.20,.82)
        # Wind-borne dust settles on upward faces and behind the crown/lap seams.
        seam=n.maximum(*[_radial_track(n,x,y,a,.005) for a in (-30,90,210)])
        seam=n.mul(seam,n.ramp(radial,.151,.173))
        sheltered=n.maximum(n.band(radial,.160,.009,.012),n.mul(seam,.65))
        dust=n.mul(up,age,n.add(.17,n.mul(sheltered,.32)),n.add(.55,n.mul(n.noise(p,24,3),.55)))
        base=n.mix(dust,base,(.16,.145,.105),True)
        # Evaporated rain deposits: broken mineral rings 4--12 mm across,
        # interrupted by radial runoff and restricted to rain-facing aluminum.
        xy=n.combine(x,y,0);distance=n.voronoi(xy,95)
        ringcenter=n.add(.24,n.mul(n.noise(xy,23,2),.17))
        ring=n.band(distance,ringcenter,.038,.045)
        sparse=n.mul(n.ramp(n.noise(xy,18,2),.53,.69),
            n.ramp(n.noise(xy,210,2),.32,.58))
        spots=n.mul(up,ring,sparse,age,.50)
        base=n.mix(spots,base,(.46,.43,.34),True)
        rough=n.add(rough,n.mul(dust,.38),n.mul(spots,.32))
        metal=n.mix(n.maximum(dust,n.mul(spots,.65)),1,.12)
        height=n.add(height,n.mul(dust,8e-6),n.mul(spots,7e-6))
        n.channel('settled_dust',dust);n.channel('rain_minerals',spots)
    return n.finish(base,rough,metal,height)

def perforated(wear):
    n=Nodes('Oxidized perforated emitter / hot copper');c=common(n);x,y,z=n.split(c['position'])
    angle=n.math('ARCTAN2',y,x)
    # 144 holes around each of 48 staggered rows. These submillimeter recesses
    # bake into the atlas; silhouette has a rolled seam and separate guard rods.
    row=n.math('FLOOR',n.math('DIVIDE',n.math('SUBTRACT',z,1.91),.0044))
    stagger=n.mul(n.math('MODULO',row,2),.5)
    u=n.math('PINGPONG',n.add(n.mul(angle,144/math.tau),stagger),.5)
    v=n.math('PINGPONG',n.math('DIVIDE',z,.0044),.5)
    hole=n.ramp(n.add(n.mul(u,u),n.mul(v,v)),.085,.040)
    face=n.ramp(n.math('ABSOLUTE',n.split(c['normal'])[2]),.5,.1)
    hole=n.mul(hole,face)
    hot=n.band(z,2.015,.065,.04)
    base=n.mix(n.mul(hot,wear),(.24,.255,.245),(.20,.12,.045),True)
    edgeheat=n.mul(n.band(z,2.09,.012,.025),min(1,wear*2.5))
    base=n.mix(edgeheat,base,(.115,.15,.20),True)
    base=n.mix(hole,base,(.012,.006,.003),True)
    mat=n.finish(base,n.mix(hole,.58,.86),n.mix(hole,1,0),n.mul(hole,-.00030))
    bs=mat.node_tree.nodes['SURFACE'];n.feed(bs.inputs['Emission Color'],base);bs.inputs['Emission Strength'].default_value=0
    return mat
