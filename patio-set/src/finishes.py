"""Original exposed/shaded outdoor finishes, authored physical rest frames."""
import math
from kit import materials as M


def powder(wear):
    n=M.Nodes('Terrace bronze / top chalk / boot scuffs / mineral spots');c=M.common(n);p=c['position']
    fine=n.noise(p,1900,2)
    exposure=n.mul(c['up'],wear,n.add(.65,n.mul(n.noise(p,9,3),.35)))
    base=n.mix(n.mul(exposure,2.1),(.029,.022,.016),(.245,.215,.155),True)
    low=n.ramp(c['z'],.09,.017)
    scratches=n.ramp(n.noise(n.vec('MULTIPLY',p,(25,8,980)),1,2),.46,.68)
    scuff=n.mul(low,wear*3.1,scratches,n.maximum(c['edge'],.4))
    base=n.mix(scuff,base,(.26,.27,.25),True)
    corners=n.mul(c['cavity'],wear*1.8,n.ramp(n.noise(p,95,3),.25,.65))
    splash=n.mul(n.ramp(c['z'],.075,.012),wear,n.ramp(n.noise(p,80,3),.40,.65))
    dirt=n.maximum(corners,splash)
    base=n.mix(dirt,base,(.085,.060,.026),True)
    v=n.node('ShaderNodeTexVoronoi');n.feed(v.inputs['Vector'],p);v.inputs['Scale'].default_value=26
    rings=n.band(v.outputs['Distance'],.30,.016,.025)
    spots=n.mul(rings,c['up'],wear*1.5,n.ramp(n.noise(p,35,2),.30,.67))
    base=n.mix(spots,base,(.38,.34,.23),True)
    rough=n.add(.48,n.mul(exposure,.42),n.mul(dirt,.2),n.mul(spots,.20))
    return n.finish(base,rough,n.mul(scuff,.8),n.add(n.mul(n.math('SUBTRACT',fine,.5),15e-6),n.mul(dirt,25e-6)))


def fabric(name,wear,sling=False,closed=False,binding=False):
    n=M.Nodes(name);c=M.common(n);p=c['position'];x,y,z=c['x'],c['y'],c['z']
    pitch=.0034 if sling else .0016
    u=n.mul(x,math.tau/pitch);v=n.mul(n.add(y,z),math.tau/pitch)
    warp=n.math('POWER',n.math('ABSOLUTE',n.math('SINE',u)),2.2)
    weft=n.math('POWER',n.math('ABSOLUTE',n.math('SINE',v)),2.2)
    thread=n.mix(.5,warp,weft)
    base=n.mix(n.mul(thread,.65),(.035,.095,.047),(.13,.205,.095),True)
    angle=n.math('ARCTAN2',y,x)
    if sling:
        seam=n.maximum(n.band(n.math('ABSOLUTE',x),.264,.006,.004),n.band(z,.94,.008,.004))
    else:seam=n.ramp(n.math('ABSOLUTE',n.math('SINE',n.mul(angle,4))),.040,.012)
    # Exposure accumulated through thin cloth: both sling faces age, upward faces most.
    sun=n.ramp(n.vec('DOT_PRODUCT',c['normal'],(0,-.62,.785)),.05,.85)
    exposure=n.add(.42,n.mul(n.maximum(c['up'],n.mul(sun,.50)),.58)) if sling else n.add(.18,n.mul(n.maximum(c['up'],n.mul(sun,.42)),.82))
    if closed:
        ridge=n.ramp(n.math('SINE',n.add(n.mul(angle,8),n.mul(n.math('SUBTRACT',z,1.13),1.05))),-.35,.75)
        exposure=ridge
        protected_tie=n.band(z,1.675,.025,.015)
        exposure=n.mul(exposure,n.math('SUBTRACT',1,n.mul(protected_tie,.85)))
    protected=n.maximum(n.mul(seam,.75),n.mul(c['cavity'],.8))
    fade=n.mul(wear*1.35,exposure,n.math('SUBTRACT',1,protected),n.add(.78,n.mul(n.noise(p,8,2),.22)))
    if binding:fade=n.mul(fade,.5)
    base=n.mix(fade,base,(.13,.205,.113),True)
    base=n.mix(n.mul(seam,.25),base,(.025,.065,.028),True)
    dirt=n.mul(wear*1.4,c['cavity'],n.ramp(n.noise(p,110,3),.30,.65))
    base=n.mix(dirt,base,(.055,.045,.015),True)
    height=n.add(n.mul(thread,180e-6 if sling else 50e-6),n.mul(seam,.00022))
    if binding:
        # Paired 4 mm stitches, laid along the binding/pocket in source geometry.
        stitch=n.ramp(n.math('SINE',n.mul(n.add(n.math('SQRT',n.add(n.mul(x,x),n.mul(y,y))),z),math.tau/.004)),.4,.7)
        height=n.add(height,n.mul(stitch,.00020))
        base=n.mix(n.mul(stitch,.12),base,(.35,.37,.23),True)
    return n.finish(base,n.add(.78,n.mul(fade,.12),n.mul(dirt,.08)),0,height)
