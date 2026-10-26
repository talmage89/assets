"""Opaque painted cedar: edge/cut wear, nail seats and grade-driven mildew."""
from kit.materials import Nodes

def white_wood(name,frame,ground,width,length,seed,wear,nails=(),depth=None):
    n=Nodes(name);tc=n.node('ShaderNodeTexCoord');tc.object=frame;p=tc.outputs['Object'];x,y,z=n.split(p)
    gh=n.node('ShaderNodeTexCoord');gh.object=ground;h=n.split(gh.outputs['Object'])[2]
    fiber=n.noise(n.combine(n.add(n.mul(x,750),seed*7.3),n.mul(y,750),n.mul(z,5)),1,3)
    ridges=n.noise(n.combine(n.add(n.mul(x,175),seed*2.1),n.mul(y,175),n.mul(z,3.7)),1,3)
    chips=n.noise(n.combine(n.add(n.mul(x,410),seed*.9),n.mul(y,410),n.mul(z,145)),1,2)
    # A surface sits at one section limit everywhere: an edge needs proximity
    # to both cross-section limits. This keeps a rail's broad face intact.
    depth=width if depth is None else depth
    geometry=n.node('ShaderNodeNewGeometry')
    up=n.ramp(n.split(geometry.outputs['Normal'])[2],.5,.95)
    side_edge=n.mul(n.ramp(n.math('ABSOLUTE',x),width/2-.006,width/2-.001),n.ramp(n.math('ABSOLUTE',y),depth/2-.006,depth/2-.001))
    edge=n.maximum(side_edge,n.ramp(z,.025,0),n.ramp(z,length-.035,length))
    # Rain enters cut ends, while sun breaks down the top paint film along fibers.
    end=n.maximum(n.ramp(z,.08,0),n.ramp(z,length-.12,length))
    peel=n.ramp(n.noise(n.combine(n.add(n.mul(x,55),seed*.9),n.mul(y,55),n.mul(z,10)),1,3),.43,.57)
    broken=n.mul(n.maximum(edge,n.mul(end,.95),n.mul(up,.35)),peel,wear*2.5)
    damp=n.mul(n.ramp(h,.33,.045),n.ramp(n.noise(n.combine(n.mul(x,35),n.mul(y,35),n.mul(h,14)),1,3),.18,.61),wear*2.5)
    base=n.mix(n.add(n.mul(fiber,.075),n.mul(ridges,.09)),(.72,.715,.68),(.50,.51,.48),True)
    base=n.mix(n.mul(up,wear*.28),base,(.78,.77,.72),True)
    base=n.mix(broken,base,(.10,.075,.043),True)
    ground_normal=n.node('ShaderNodeVectorTransform',vector_type='NORMAL',convert_from='WORLD',convert_to='OBJECT');n.feed(ground_normal.inputs[0],geometry.outputs['Normal'])
    # Rear/shaded face dries slowly. Height stays in the grade frame on rails too.
    shaded=n.ramp(n.split(ground_normal.outputs[0])[1],-.4,.8)
    damp=n.mul(damp,n.add(.65,n.mul(shaded,.55)))
    base=n.mix(damp,base,(.045,.073,.033),True)
    splash=n.mul(n.ramp(h,.18,.045),wear*1.5,n.ramp(n.noise(n.combine(n.mul(x,62),n.mul(y,62),n.mul(h,24)),1,3),.26,.65))
    base=n.mix(splash,base,(.10,.076,.043),True)
    heads=0;stains=0
    for row in nails:
        for xx in (-width*.23,width*.23):
            heads=n.maximum(heads,n.ellipse(p,(xx,row),(.0025,.0025)))
            stains=n.maximum(stains,n.mul(n.band(x,xx,.00065,.001),n.band(z,row-.013,.011,.007)))
    base=n.mix(n.mul(stains,wear*.18),base,(.12,.09,.055),True)
    base=n.mix(heads,base,(.15,.16,.15),True)
    height=n.add(n.mul(fiber,.00009),n.mul(ridges,.00035),n.mul(broken,-.00015),n.mul(heads,-.00012))
    n.channel('paint_wear',broken);n.channel('mildew',damp)
    return n.finish(base,n.add(.64,n.mul(fiber,.12),n.mul(damp,.10)),n.mul(heads,.65),height)
