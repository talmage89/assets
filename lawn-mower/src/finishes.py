"""Original cause-driven grass, oil, fuel, handling and textile finishes."""
import math
from pathlib import Path
import bpy
from kit.materials import Nodes,common,surface

def finish(role,wear=.35):
    n=Nodes('Meadow / '+role);c=common(n);p=c['position'];x,y,z=n.split(p);age=wear/.35
    micro=n.noise(p,1700,2);broken=n.ramp(n.noise(p,170,3),.38,.65)
    rad=n.math('SQRT',n.add(n.mul(x,x),n.mul(y,y)))
    grass=oil=chips=fuel=cake=inner=weave=folds=seam=0
    if role=='deck':
        base=(.34,.092,.023);rough=.40;metal=0
        lip=n.ramp(z,.127,.060)
        underside=n.ramp(n.split(c['normal'])[2],-.1,-.8)
        # Accumulation follows the wet cutting chamber and lower rolled edge.
        grass=n.mul(age,n.maximum(lip,n.mul(underside,.84)),n.add(.20,n.mul(broken,.68)))
        scuff=n.mul(n.ramp(rad,.237,.282),n.band(z,.083,.030,.025),broken,age)
        boot=n.mul(n.ellipse(p,(.0,.255),(.15,.060),axes=(0,1)),n.ramp(z,.125,.16),broken,age)
        chips=n.maximum(n.mul(scuff,.60),n.mul(boot,.7),n.mul(c['edge'],broken,age,.28))
        base=n.mix(n.mul(c['up'],age,.14),base,(.40,.15,.052),True)
        base=n.mix(chips,base,(.23,.225,.18),True)
        base=n.mix(n.mul(chips,n.ramp(n.noise(p,250),.48,.73),.7),base,(.15,.050,.012),True)
        oil=n.mul(n.ramp(rad,.175,.115),n.band(z,.18,.025,.025),age,.85)
    elif role=='engine':
        base=(.17,.175,.16);rough=.57;metal=.85
        oil=n.mul(n.ramp(z,.31,.20),age,n.add(.62,n.mul(n.noise(n.vec('MULTIPLY',p,(2,2,.22)),60),.30)))
    elif role=='bag':
        base=(.010,.016,.012);metal=0;rough=.96
        # Fading follows the open-sky exposed side shoulders; abrasion follows
        # the loaded lower seam and back corners that scrape garage floors.
        fade=n.mul(age,n.maximum(c['up'],.28),.48)
        base=n.mix(fade,base,(.063,.071,.047),True)
        ground=n.ramp(z,.285,.125)
        drag=n.mul(age,ground,n.ramp(n.noise(n.vec('MULTIPLY',p,(1,4,12)),65),.34,.66))
        base=n.mix(drag,base,(.12,.115,.060),True)
        grass=n.mul(ground,age,.45,n.add(.35,n.mul(broken,.5)))
        side=n.ramp(n.math('ABSOLUTE',n.split(c['normal'])[0]),.25,.75)
        warp=n.math('SINE',n.mul(n.mix(side,x,y),math.tau/.0028))
        weft=n.math('SINE',n.mul(z,math.tau/.0028))
        weave=n.mul(warp,weft,115e-6)
        roof=n.add(.310,n.mul(n.ramp(y,.375,.460),.087),n.mul(n.ramp(y,.460,.640),.121),n.mul(n.ramp(y,.640,.790),.105),n.mul(n.ramp(y,.790,.855),.007))
        welt=n.band(z,n.add(roof,-.009),.002,.002)
        stitch=n.ramp(n.math('SINE',n.mul(y,math.tau/.005)),.1,.5)
        vertical=n.maximum(n.band(y,.387,.002,.003),n.band(y,.840,.002,.003))
        seam=n.mul(n.maximum(welt,vertical),n.add(.6,n.mul(stitch,.4)),.00045)
        # Tension gathers radiate from corner attachments, fading toward the
        # middle of each unsupported fabric panel.
        fromtop=n.math('SUBTRACT',roof,z)
        corner=n.maximum(n.band(y,.43,.035,.065),n.band(y,.80,.035,.065))
        foldwave=n.math('SINE',n.add(n.mul(y,110),n.mul(fromtop,43)))
        folds=n.mul(side,corner,n.ramp(fromtop,.008,.045),n.ramp(fromtop,.26,.08),foldwave,.0013)
    elif role=='bag_top':
        base=(.014,.020,.016);metal=0;rough=.62
        base=n.mix(n.mul(age,c['up'],.22),base,(.064,.072,.049),True)
        chips=n.mul(age,c['edge'],broken,.35)
        base=n.mix(chips,base,(.14,.15,.10),True)
    elif role=='grip':
        base=(.009,.014,.012);rough=.68;metal=0
        hands=n.maximum(n.ellipse(p,(-.14,.526),(.075,.030),axes=(0,1)),n.ellipse(p,(.14,.526),(.075,.030),axes=(0,1)))
        base=n.mix(n.mul(hands,age,.4),base,(.025,.030,.022),True);rough=n.mix(n.mul(hands,age,.7),rough,.33)
    elif role=='tire':
        base=(.012,.015,.012);rough=.84;metal=0
        # Coordinates are wheel-pivot local, so residue rotates with the tread.
        radius=n.math('SQRT',n.add(n.mul(y,y),n.mul(z,z)))
        outer=n.ramp(radius,.062,.082)
        grass=n.mul(age,outer,n.ramp(n.noise(n.vec('MULTIPLY',p,(1,1.7,1)),200),.42,.65),.78)
        base=n.mix(n.mul(c['edge'],broken,age,.4),base,(.09,.095,.073),True)
    elif role=='hub':
        base=(.30,.32,.29);rough=.54;metal=0
        grass=n.mul(age,c['cavity'],broken,.7)
        base=n.mix(n.mul(age,c['edge'],broken,.5),base,(.12,.135,.11),True)
    elif role in ('shroud','recoil'):
        base=(.012,.018,.017);rough=.47;metal=0
        fuel=n.mul(n.ellipse(p,(-.077,.095),(.055,.050),axes=(0,1)),n.ramp(z,.36,.4),age,.56)
        base=n.mix(n.mul(age,c['up'],.10),base,(.065,.072,.058),True)
    else:
        base=(.015,.020,.018);rough=.51;metal=0
        chips=n.mul(age,c['edge'],broken,.34)
        base=n.mix(chips,base,(.15,.16,.13),True)
    if role=='recoil':
        dy=n.add(y,.052);rr=n.math('SQRT',n.add(n.mul(x,x),n.mul(dy,dy)))
        angle=n.math('ARCTAN2',dy,x)
        slots=n.mul(n.ramp(rr,.040,.046),n.ramp(rr,.094,.085),n.ramp(n.math('SINE',n.add(n.mul(angle,20),n.mul(rr,70))),.35,.65))
        base=n.mix(slots,base,(.001,.0015,.001),True)
        rough=n.mix(slots,rough,.82)
    # Original generated ink is projected analytically in authored meters.
    # Texture coordinates never depend on a reference photo or imported image.
    if role in ('deck','bag_top','shroud'):
        tex=n.node('ShaderNodeTexImage',extension='CLIP')
        tex.image=bpy.data.images.load(str(Path('build/markings',('warning' if role=='deck' else 'bag' if role=='bag_top' else 'badge')+'.png').resolve()),check_existing=True)
        if role=='deck':
            uv=n.combine(n.add(n.mul(x,1/.130),.5),n.mul(n.add(y,.260),1/.048),0)
            zone=n.mul(n.ramp(z,.140,.148),c['up'])
        elif role=='bag_top':
            uv=n.combine(n.add(n.mul(x,1/.275),.5),n.mul(n.add(y,-.655),1/.113),0)
            zone=n.ramp(n.split(c['normal'])[2],.35,.65)
        else:
            uv=n.combine(n.add(n.mul(x,1/.117),.5),n.mul(n.add(z,-.359),1/.040),0)
            zone=n.mul(n.ramp(y,-.162,-.172),n.ramp(n.split(c['normal'])[1],-.35,-.8))
        n.feed(tex.inputs['Vector'],uv)
        base=n.mix(n.mul(tex.outputs['Alpha'],zone),base,tex.outputs['Color'],True)
    # The inside is exposed steel beneath a thick retained clipping cake.
    # Radial throw loads the outer chamber; the rear throat and side discharge
    # retain the heaviest moist deposits. Paint is not the revealed substrate.
    if role=='deck':
        nx,ny,nz=n.split(c['normal'])
        inward=n.ramp(n.add(n.mul(x,nx),n.mul(y,ny)),-.045,-.18)
        inner=n.maximum(n.ramp(nz,-.15,-.75),n.mul(inward,n.ramp(z,.165,.13)))
        throw=n.ramp(rad,.11,.245)
        discharge=n.maximum(n.ellipse(p,(.26,-.015),(.095,.15),axes=(0,1)),n.ellipse(p,(0,.25),(.20,.11),axes=(0,1)))
        load=n.maximum(throw,discharge)
        flakes=n.ramp(n.noise(n.vec('MULTIPLY',p,(1.2,1.8,3)),45,3),.28,.46)
        cake=n.mul(inner,min(1,age),n.add(.60,n.mul(load,.39)),flakes)
        rust=n.ramp(n.noise(p,180,3),.38,.70)
        exposed=n.mix(rust,(.075,.083,.069),(.17,.070,.023),True)
        base=n.mix(inner,base,exposed,True)
        matting=n.noise(n.vec('MULTIPLY',p,(2,8,1)),130,3)
        olive=n.mix(matting,(.030,.045,.008),(.14,.125,.042),True)
        base=n.mix(cake,base,olive,True)
        # Avoid the exterior lip layer diluting the interior's packed fibers.
        grass=n.mul(grass,n.math('SUBTRACT',1,inner))
        rough=n.mix(inner,rough,.78);rough=n.mix(cake,rough,.98)
        metal=n.mix(inner,metal,n.mul(n.math('SUBTRACT',1,cake),.45))
    grasscol=n.mix(n.noise(p,380,2),(.026,.036,.007),(.11,.095,.024),True)
    base=n.mix(grass,base,grasscol,True)
    base=n.mix(oil,base,(.011,.009,.005),True)
    base=n.mix(fuel,base,(.055,.037,.012),True)
    rough=n.mix(grass,rough,.97);rough=n.mix(oil,rough,.30);rough=n.mix(fuel,rough,.35)
    metal=n.mix(n.maximum(grass,oil,fuel),metal,0)
    height=n.add(n.mul(micro,12e-6),n.mul(grass,180e-6),n.mul(chips,-45e-6),weave,seam,folds,n.mul(cake,n.add(.0011,n.mul(n.noise(n.vec('MULTIPLY',p,(2,8,1)),170),.0011))),n.mul(slots,-.0012) if role=='recoil' else 0,n.mul(n.band(rad,.155,.0018,.002),.0007) if role=='deck' else 0)
    for key,val in [('grass',grass),('oil',oil),('fuel',fuel),('scuff',chips),('interior_cake',cake),('inside',inner)]:n.channel(key,val)
    return n.finish(base,rough,metal,height)
