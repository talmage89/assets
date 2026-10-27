"""Original vehicle manufacturing shaders; meter-valued rest-space wear.

All shaders expose the kit bake channels. Coordinates may come from a stored
vector attribute, so road film stays on moving panels during source posing.
No image is downloaded. Optional lettering is an original generated relief.
"""
import math
import bpy
from kit.materials import Nodes


def rest(n,attribute):
    a=n.node('ShaderNodeAttribute',attribute_name=attribute)
    p=a.outputs['Vector'];x,y,z=n.split(p)
    geo=n.node('ShaderNodeNewGeometry');nx,ny,nz=n.split(geo.outputs['Normal'])
    return p,x,y,z,nx,ny,nz


def road_mask(n,p,y,z,axles,wear):
    """Broken splash fans aft of tires, gravity sediment low on the body."""
    breakup=n.noise(n.vec('MULTIPLY',p,(5,1,8)),9,3)
    sediment=n.mul(n.ramp(z,.86,.53),n.ramp(breakup,.30,.72),1.35)
    fans=[]
    for axle in axles:
        dy=n.math('SUBTRACT',y,axle)
        aft=n.mul(n.ramp(dy,.04,.19),n.ramp(dy,.85,.40))
        ceiling=n.add(.63,n.mul(n.ramp(dy,.8,.08),.25),n.mul(breakup,.08))
        height=n.ramp(z,ceiling,.46) if not hasattr(ceiling,'is_output') else n.ramp(n.math('SUBTRACT',ceiling,z),0,.25)
        fans.append(n.mul(aft,height,n.ramp(breakup,.36,.71),1.15))
    return n.math('MULTIPLY',n.maximum(sediment,*fans),wear,clamp=True)


def daily_road_mask(n,p,y,z,axles,wear):
    """Dilute road film: tire-driven fans, with only a trace on the sill."""
    grain=n.add(.72,n.mul(n.noise(p,150,2),.28))
    terms=[n.mul(n.ramp(z,.675,.565),.08)]
    for axle in axles:
        d=n.math('SUBTRACT',y,axle+.27)
        aft=n.mul(n.ramp(d,0,.15),n.ramp(d,1.08,.24))
        # A swept, widening envelope. Noise changes deposit density, never
        # displaces its surface or draws a repeating water-caustic ridge.
        ceiling=n.add(.76,n.mul(d,-.075))
        fall=n.ramp(n.math('SUBTRACT',ceiling,z),0,.18)
        terms.append(n.mul(aft,fall,.40))
    return n.mul(n.maximum(*terms),grain,wear)


def paint(name,color,wear=.65,axles=(),attribute='VehicleRest',front=None,rear=None,refined=False,rail_height=None):
    n=Nodes(name);p,x,y,z,nx,ny,nz=rest(n,attribute)
    tint=n.node('ShaderNodeRGB',name='Paint tint');tint.outputs[0].default_value=(*color,1)
    film=(daily_road_mask if refined else road_mask)(n,p,y,z,axles,wear)
    wake=0 if rear is None else n.mul(n.ramp(y,rear-.22,rear-.04),n.ramp(z,1.24,.84),n.ramp(n.noise(n.vec('MULTIPLY',p,(4,2,.5)),24,3),.28,.70),wear,.65)
    film=n.maximum(film,0 if refined else wake)
    if refined and rear is not None and rail_height is not None:
        rail=n.mul(n.ramp(y,rear-.12,rear-.01),n.band(z,rail_height,.015),wear,.22)
        film=n.maximum(film,rail)
    # Contamination sits above the original hue. A neutral wear atlas can be
    # multiplied by any factory tint; no five-copy texture set is needed.
    faded=n.mul(n.ramp(nz,.3,.95),wear,.003 if refined else .018)
    contamination=n.mix(faded,(0,0,0),(.32,.34,.34),True)
    contamination=n.mix(film,contamination,(.047,.040,.031) if refined else (.075,.065,.051),True)
    front_mask=0 if front is None else n.mul(n.ramp(y,front+.33,front+.03),n.ramp(z,1.11,1.25),n.maximum(n.ramp(ny,-.15,-.8),n.mul(n.ramp(nz,.4,.9),.8) if refined else 0))
    chips=n.mul(front_mask,wear,n.ramp(n.noise(p,670,2),.78,.88))
    contamination=n.mix(chips,contamination,(.10,.11,.115),True)
    coverage=n.mul(n.math('SUBTRACT',1,faded),n.math('SUBTRACT',1,film),n.math('SUBTRACT',1,chips))
    base=n.vec('ADD',n.mix(coverage,(0,0,0),tint.outputs[0],True),contamination)
    peel=n.noise(p,2800,2);height=n.mul(n.math('SUBTRACT',peel,.5),1.6e-6)
    rough=n.add(.15 if refined else .24,n.mul(n.noise(p,900,2),.012 if refined else .035),n.mul(film,.22))
    if refined:
        # Sparse wash swirls modulate only highlight roughness, never albedo.
        arcs=n.math('SINE',n.mul(n.voronoi(n.vec('MULTIPLY',p,(1,1,1)),8),3200))
        swirls=n.mul(n.ramp(arcs,.92,.99),n.ramp(n.noise(p,30,2),.57,.70),wear,.018)
        rough=n.add(rough,swirls)
    mat=n.finish(base,rough,.12,height,coat=1)
    bs=mat.node_tree.nodes['SURFACE'];n.feed(bs.inputs['Coat Weight'],n.math('SUBTRACT',1,n.mul(n.maximum(film,chips),.90)))
    n.feed(bs.inputs['Coat Roughness'],n.add(.035 if refined else .11,n.mul(film,.35)))
    n.channel('road_film',film);n.channel('chips',chips)
    n.channel('paint_coverage',coverage);n.channel('paint_contamination',contamination)
    mat.diffuse_color=(*color,1);mat['vehicle_paint']=True;return mat


def manufactured(name,color,kind='plastic',wear=.65,axles=(),attribute='VehicleRest',brake_centers=(),refined=False,cargo_bounds=None):
    n=Nodes(name);p,x,y,z,nx,ny,nz=rest(n,attribute)
    metal=1 if kind in ['chrome','alloy','steel'] else 0
    rough={'chrome':.17,'alloy':.27,'steel':.46,'rubber':.78,'fabric':.88,'plastic':.54,'liner':.87}.get(kind,.55)
    film=(daily_road_mask if refined else road_mask)(n,p,y,z,axles,wear)
    if refined and kind in ['alloy','chrome','steel']:film=0
    fine=n.noise(p,4000 if kind!='fabric' else 2400,2)
    base=n.mix(n.mul(n.ramp(nz,.35,.95),wear,.15),color,tuple(min(.065,v*1.5) for v in color),True) if kind in ['plastic','rubber'] else color
    base=n.mix(film,base,(.049,.042,.032),True)
    if brake_centers:
        dust=[]
        for cx,cy,cz in brake_centers:
            r=n.math('SQRT',n.add(n.mul(n.math('SUBTRACT',y,cy),n.math('SUBTRACT',y,cy)),n.mul(n.math('SUBTRACT',z,cz),n.math('SUBTRACT',z,cz))))
            d=n.math('ABSOLUTE',n.math('SUBTRACT',x,cx))
            dust.append(n.mul(n.ramp(r,.060,.110),n.ramp(r,.245,.205),n.ramp(d,.17,.02)))
        mask=n.mul(n.maximum(*dust),wear,.16 if refined else .42,n.add(.70,n.mul(n.noise(p,190,2),.3)))
        base=n.mix(mask,base,(.027,.022,.018),True);metal=n.mix(mask,metal,0)
    h=n.mul(n.math('SUBTRACT',fine,.5),18e-6 if kind in ['plastic','fabric','liner'] else .8e-6)
    if refined and kind=='liner' and cargo_bounds is not None:
        half_width,front,rear,floor=cargo_bounds
        corners=n.mul(n.ramp(z,floor+.075,floor),n.maximum(n.ramp(n.math('ABSOLUTE',x),half_width-.15,half_width),n.ramp(y,front+.15,front),n.ramp(y,rear-.20,rear)),wear,.25)
        base=n.mix(corners,base,(.066,.057,.043),True)
    if kind=='liner':
        # Bed scuffs follow dragged cargo, not a uniform surface overlay.
        stretch=n.vec('MULTIPLY',p,(450,1,90));lines=n.ramp(n.noise(stretch,2,2),.63,.75)
        contact=n.mul(n.ramp(z,1.0,.90),n.ramp(n.noise(p,17,2),.48,.65),lines,wear)
        base=n.mix(contact,base,(.055,.057,.056),True);h=n.add(h,n.mul(contact,-.00025))
    if refined and kind=='chrome':
        # Sparse dried droplet rims vary roughness, not chrome's metal color.
        cells=n.voronoi(p,190);spots=n.mul(n.band(cells,.32,.024,.018),n.ramp(n.noise(p,42,2),.57,.69),wear)
        rough=n.add(.105,n.mul(spots,.18))
    if refined and kind=='alloy':rough=.30;h=0
    mat=n.finish(base,n.add(rough,n.mul(film,.18)),metal,h)
    mat.diffuse_color=(*color,1);return mat


def glazing(name,tint=(.96,.98,.98),privacy=False,axes=(0,2)):
    n=Nodes(name);tc=n.node('ShaderNodeTexCoord');v=n.split(tc.outputs['Generated']);u,w=v[axes[0]],v[axes[1]]
    edge=n.maximum(n.ramp(u,.033,.018),n.ramp(u,.967,.982),n.ramp(w,.055,.025),n.ramp(w,.963,.984))
    # Sparse printed dots soften the inner frit edge. Generated coordinates
    # are local to the glass; source photos never enter these nodes.
    dots=n.mul(n.ramp(n.math('SINE',n.mul(u,1500)),.8,.96),n.ramp(n.math('SINE',n.mul(w,900)),.8,.96))
    border=n.maximum(edge,n.mul(n.ramp(edge,0,.1),dots))
    base=n.mix(border,tint,(.003,.004,.004),True)
    # Frit is printed behind the smooth outer laminate; it changes color and
    # transmission, not the outside glass roughness.
    mat=n.finish(base,.025,0)
    bs=mat.node_tree.nodes['SURFACE'];n.feed(bs.inputs['Transmission Weight'],n.math('SUBTRACT',1,border));bs.inputs['IOR'].default_value=1.52;bs.inputs['Specular IOR Level'].default_value=.5
    mat.diffuse_color=(*tint,1);mat['vehicle_glass']=True;mat['privacy_tint']=bool(privacy)
    return mat


def tire(name,lettering=None,sign=1,wear=.65):
    n=Nodes(name);tc=n.node('ShaderNodeTexCoord');p=tc.outputs['Object'];x,y,z=n.split(p)
    ax=n.math('ABSOLUTE',x);r=n.math('SQRT',n.add(n.mul(y,y),n.mul(z,z)))
    angle=n.math('ARCTAN2',z,y)
    phase=n.add(n.mul(angle,52/math.tau),n.mul(x,21))
    blocks=n.ramp(n.math('FRACT',phase),.09,.16)
    blocks=n.mul(blocks,n.ramp(n.math('FRACT',phase),.94,.85))
    lanes=n.ramp(n.math('ABSOLUTE',n.math('SUBTRACT',n.math('FRACT',n.mul(x,25)),.5)),.44,.34)
    tread=n.mul(n.ramp(ax,.118,.096),n.ramp(r,.348,.385))
    height=n.mul(tread,blocks,lanes,.0025)
    sipe=n.mul(tread,n.ramp(n.math('SINE',n.add(n.mul(angle,208),n.mul(x,150))),.90,.99),-.00032)
    height=n.add(height,sipe,n.mul(n.noise(p,2500,2),12e-6))
    if lettering:
        tex=n.node('ShaderNodeTexImage');tex.image=lettering;tex.extension='CLIP';tex.interpolation='Linear'
        n.feed(tex.inputs['Vector'],n.combine(n.add(.5,n.mul(y,sign/0.86)),n.add(.5,n.mul(z,1/.86)),0))
        side=n.mul(n.ramp(ax,.105,.125),n.ramp(r,.245,.260),n.ramp(r,.363,.344))
        height=n.add(height,n.mul(tex.outputs['Color'],side,.00065))
    dust=n.mul(n.ramp(r,.248,.280),n.ramp(r,.400,.370),n.ramp(ax,.102,.126),wear,.70,n.add(.65,n.mul(n.noise(p,140,2),.35)))
    base=n.mix(dust,(.009,.010,.011),(.110,.102,.088),True)
    mat=n.finish(base,.77,0,height);mat.diffuse_color=(.018,.019,.02,1);return mat


def lamp(name,color=(1,1,1),strength=8,transmission=0):
    n=Nodes(name);m=n.finish(color,.12,0,coat=.3);bs=m.node_tree.nodes['SURFACE']
    bs.inputs['Transmission Weight'].default_value=transmission;bs.inputs['IOR'].default_value=1.49
    bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=0
    m['lamp_lit_strength']=strength;m.diffuse_color=(*color,1);return m


def brake_rotor(name):
    """Turned steel friction surface; object origin on its X-axis wheel hub."""
    n=Nodes(name);tc=n.node('ShaderNodeTexCoord');x,y,z=n.split(tc.outputs['Object'])
    radius=n.math('SQRT',n.add(n.mul(y,y),n.mul(z,z)))
    turn=n.math('SINE',n.mul(radius,math.tau/.00032))
    rough=n.add(.32,n.mul(turn,.025))
    return n.finish((.29,.30,.31),rough,1,n.mul(turn,.35e-6))
