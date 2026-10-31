"""Covey field finishes in explicit rest coordinates; no photographic inputs.

All distances are meters. Annual growth, pore vessels, 20-LPI cutter fields,
case oxide and contact-pressure wear are original procedural node networks.
The clean counterpart removes use only, retaining machining and checkering.
"""
import math
import bpy
from kit.materials import Nodes

SITES=('barrel_carry','muzzles','action_fade','lever_thumb','guard_fingers',
       'wrist_points','forend_points','stock_toe','forend_edges')

def sub(n,a,b):return n.math('SUBTRACT',a,b)
def ab(n,a):return n.math('ABSOLUTE',a)
def minimum(n,*vs):
    r=vs[0]
    for v in vs[1:]:r=n.math('MINIMUM',r,v)
    return r

def ramp(n,x,a,b):return n.ramp(n.math('DIVIDE',sub(n,x,a),sub(n,b,a)),0,1)
def interval(n,x,a,b,f=.001):return n.mul(ramp(n,x,a-f,a),ramp(n,x,b+f,b))
def oval(n,u,v,cu,cv,ru,rv):
    r=n.add(n.math('POWER',n.math('DIVIDE',sub(n,u,cu),ru),2),
            n.math('POWER',n.math('DIVIDE',sub(n,v,cv),rv),2))
    return n.ramp(r,1.3,.20)
def inputs(n):
    p=n.node('ShaderNodeAttribute',attribute_name='FinishPosition').outputs['Vector']
    normal=n.node('ShaderNodeAttribute',attribute_name='FinishNormal').outputs['Vector']
    return p,*n.split(p),*n.split(normal)
def finish(n,base,rough,metal,height=0,ao=1,sites=None,spec=.45):
    for site in SITES:n.channel(site,(sites or {}).get(site,0))
    n.channel('micro_ao',ao)
    n.channel('specular_factor',n.mul(spec,2))
    mat=n.finish(base,rough,metal,height,bump=1)
    n.feed(mat.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'],spec)
    return mat

def steel(name,role,wear):
    n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n);ax=ab(n,x);sites={}
    fine=n.noise(p,7000,2)
    polish=n.noise(n.combine(n.mul(x,2100),n.mul(y,15),n.mul(z,2100)),1,2)
    base=(.029,.031,.034);rough=n.add(.285,n.mul(sub(n,polish,.5),.075));metal=1
    h=n.mul(sub(n,fine,.5),.8e-6)
    broken=n.add(.67,n.mul(n.noise(n.combine(n.mul(x,250),n.mul(y,240),n.mul(z,270)),1,3),.48))
    if role=='case':
        # Irregular quench-oxide flow, domain warped at two physical scales.
        # Color is fixed to the metal; it is not an environment/iridescence map.
        warp=n.noise(p,75,3)
        warped=n.vec('ADD',p,n.vec('MULTIPLY',n.combine(warp,n.noise(p,96,2),n.noise(p,57,3)),(.013,.013,.013)))
        flow=n.noise(warped,180,3)
        blue=(.10,.13,.16);straw=(.18,.16,.12);brown=(.14,.10,.075)
        oxide=n.mix(n.ramp(flow,.29,.48),brown,straw,True)
        oxide=n.mix(n.ramp(flow,.48,.66),oxide,blue,True)
        # Flats handled during carrying and wiping lose color first. Fence
        # hollows/recesses and the front of the bar retain denser case colors.
        flats=n.mul(n.ramp(ab(n,nx),.75,.97),interval(n,y,.071,.155,.012))
        lower=n.mul(n.ramp(nz,-.20,-.88),interval(n,y,.076,.163,.012),.80)
        crest=n.mul(n.ramp(z,.044,.055),n.ramp(ab(n,nx),.7,.15),.30)
        pressure=n.maximum(n.mul(flats,.68),lower,crest)
        edge=n.maximum(n.mul(n.band(ax,.0257,.00045,.0011),n.ramp(z,.015,.007)),
                       n.mul(n.ramp(y,.176,.181),n.ramp(ab(n,nx),.3,.9)))
        fade=n.ramp(n.mul(n.maximum(pressure,edge),broken,wear['action_fade']),.48,.82)
        sites['action_fade']=fade
        base=n.mix(fade,oxide,(.26,.27,.28),True)
        rough=n.mix(fade,n.add(.30,n.mul(sub(n,polish,.5),.08)),.39)
        # Fine oxide freckles survive in the colored surface, while wiping
        # pressure smooths the faded flats. No uncaused dirt blanket.
        speck=n.mul(n.ramp(n.noise(p,2200,2),.46,.70),sub(n,1,n.mul(fade,.8)))
        base=n.mix(n.mul(speck,.24),base,(.020,.022,.024),True)
        rough=n.add(rough,n.mul(speck,.055))
        h=n.add(h,n.mul(speck,-2e-6))
        # The standing face is polished working steel; it was never a color
        # case sample. Its real planar face remains readable when open.
        face=n.mul(n.ramp(ny,.75,.99),n.band(y,.115,.00018,.00020))
        base=n.mix(face,base,(.24,.25,.26),True);rough=n.mix(face,rough,.31)
    elif role=='barrel':
        base=(.0397,.0427,.0430)
        rough=n.add(.24,n.mul(sub(n,polish,.5),.06))
        # Years of slightly shifted carrying positions beyond the splinter
        # merge into one long, thin field on the outside flanks; no cuff.
        center=n.add(.255,n.mul(nz,.025),n.mul(nx,.010))
        footprints=n.maximum(oval(n,y,z,sub(n,center,.055),.039,.075,.0081),oval(n,y,z,center,.039,.075,.0081),oval(n,y,z,n.add(center,.055),.039,.075,.0081))
        carry=n.mul(footprints,n.ramp(ab(n,nx),.12,.80),
                    n.ramp(nz,.86,.40),broken,wear['barrel_carry'])
        carry=n.ramp(carry,.23,.79)
        muzzle=n.mul(n.ramp(y,.7667,.7738),n.add(.65,n.mul(n.ramp(ab(n,nx),.20,.85),.35)),broken,wear['muzzles'])
        muzzle=n.ramp(muzzle,.16,.76)
        sites.update(barrel_carry=carry,muzzles=muzzle)
        rub=n.maximum(carry,muzzle)
        # Hand rubbing thins the oxide; it does not expose fresh white steel.
        base=n.mix(carry,base,(.155,.16,.165),True)
        base=n.mix(muzzle,base,(.24,.26,.28),True);rough=n.mix(rub,rough,.36)
        bore=n.mul(n.ramp(ny,.90,.2),n.ramp(y,.771,.7754),n.ramp(nz,.1,-.4),.15)
        rough=n.add(rough,bore)
    elif role=='lever':
        base=(.020,.022,.024)
        # Fine-filed upper thumb land retains satin blue between contact rubs;
        # the protected stem keeps its polished reflection.
        rough=n.mix(n.mul(n.ramp(nz,.50,.95),interval(n,y,.0,.065,.006)),.31,.75)
        touch=n.mul(interval(n,y,.020,.042,.004),n.ramp(nz,-.20,.40),n.ramp(x,-.006,-.003),broken,wear['lever_thumb'])
        rub=n.ramp(touch,.17,.70);sites['lever_thumb']=rub
        base=n.mix(rub,base,(.56,.59,.62),True);rough=n.mix(rub,rough,.19)
        # Small original thumb-file cuts, cut normal only, not triangles.
        cuts=n.ramp(n.math('PINGPONG',n.add(n.mul(x,.80),n.mul(y,.60)),.000635),.00016,.00006)
        h=n.add(h,n.mul(cuts,interval(n,y,.023,.043,.002),n.ramp(nz,.55,.95),-.000045,sub(n,1,n.mul(rub,.8))))
    elif role=='guard':
        base=(.016,.018,.020);rough=n.mix(n.ramp(ab(n,nx),.55,.92),.17,.34)
        # Polished inner bow, satin filed narrow edges; oxide thinning is
        # progressive, with bright steel confined to pressure maxima.
        # Follow the real formed band's changing width and its continuous
        # inner bow: rear normal +Y, floor +Z, front normal -Y. The former
        # rear interval tested a front-facing normal and missed both curves.
        rear=n.mul(interval(n,y,.008,.040,.012),n.ramp(ny,.15,.85),n.ramp(z,-.007,-.015))
        floor=n.mul(interval(n,y,.016,.101,.012),n.ramp(nz,-.20,.65),n.ramp(z,-.017,-.027))
        front=n.mul(interval(n,y,.079,.106,.010),n.ramp(ny,-.15,-.85),n.ramp(z,.001,-.008))
        pressure=n.maximum(n.mul(rear,1.5),floor,n.mul(front,1.3))
        half_width=n.mul(.0062,n.add(.64,n.mul(n.ramp(y,.013,.038),.36)))
        contact_edge=sub(n,half_width,.0019)
        rub=n.ramp(n.mul(pressure,n.band(x,contact_edge,.0013,.0028),n.ramp(ab(n,nx),.95,.45),broken,wear['guard_fingers']),.17,.76)
        rub=n.math('POWER',rub,3)
        sites['guard_fingers']=rub
        base=n.mix(rub,base,(.56,.59,.62),True);rough=n.mix(rub,rough,.14)
    elif role=='trigger':
        base=(.027,.0275,.030);rough=n.add(.32,n.mul(sub(n,polish,.5),.07))
        # Intact blued blade flats and polished contact edges.
        edge=n.ramp(ab(n,nx),.98,.70)
        base=n.mix(edge,base,(.034,.032,.032),True);rough=n.mix(edge,rough,.50)
    elif role=='safety':
        base=(.2635,.255,.22);rough=.24
        a=n.math('PINGPONG',n.add(x,y),.00056)
        b=n.math('PINGPONG',sub(n,x,y),.00056)
        shape=n.math('DIVIDE',n.math('MINIMUM',a,b),.00056)
        field=n.ramp(nz,.5,.95);cavity=n.mul(n.ramp(shape,.42,.10),field)
        h=n.add(h,n.mul(sub(n,shape,1),field,.00018))
        base=n.mix(n.mul(cavity,.94),base,(.008,.009,.010),True)
        rough=n.mix(cavity,rough,.45)
    elif role=='rib':
        rough=.49
        # Fine longitudinal matting; no change to the accepted rib surface.
        h=n.add(h,n.mul(n.math('SINE',n.mul(x,math.tau/.00036)),n.ramp(nz,.70,.97),5e-6))
    elif role=='bright':base=(.28,.29,.30);rough=n.add(.30,n.mul(sub(n,polish,.5),.07))
    elif role=='dark':rough=.42
    return finish(n,base,rough,metal,h,sites=sites)

def polygon(n,u,v,points):
    ds=[]
    for (a,b),(c,d) in zip(points,points[1:]+points[:1]):
        ds.append(n.math('DIVIDE',sub(n,n.mul(c-a,sub(n,v,b)),n.mul(d-b,sub(n,u,a))),math.hypot(c-a,d-b)))
    return minimum(n,*ds)

def wood(name,role,wear):
    n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n);sites={}
    if role=='stock':
        axis=n.add(n.mul(y,.105),n.mul(n.maximum(n.add(y,.080),0),.27))
        zz=sub(n,z,axis);rx=n.add(x,.041);rz=n.add(n.mul(zz,.8),.040)
        arch=n.mul(n.math('MINIMUM',n.add(y,.075),0),n.math('MINIMUM',n.add(y,.075),0),.16)
    else:zz=sub(n,z,.026);rx=n.add(x,.034);rz=n.add(n.mul(zz,.82),.024);arch=n.mul(sub(n,y,.265),sub(n,y,.265),.27)
    radius=n.math('SQRT',n.add(n.mul(rx,rx),n.mul(rz,rz)))
    figure=n.add(n.mul(n.math('SINE',n.add(n.mul(zz,105),n.mul(y,12))),.00030),
                 n.mul(n.math('SINE',n.add(n.mul(x,155),n.mul(y,22))),.00018))
    phase=n.mul(n.add(radius,arch,figure),math.tau/.0039)
    phase=n.add(phase,n.mul(n.math('SINE',n.mul(radius,420)),.75),n.mul(n.math('SINE',n.mul(radius,1140)),.35))
    year=n.math('FRACT',n.mul(phase,1/math.tau));late=n.ramp(year,.88,.99)
    tone=n.add(.42,n.mul(n.ramp(year,.1,.63),.20),n.mul(n.ramp(year,.65,.96),-.20))
    low,high=((.025,.008,.0035),(.30,.110,.052)) if role=='stock' else ((.01152,.004032,.002268),(.1064,.03136,.01764))
    base=n.mix(tone,low,high,True)
    base=n.mix(n.mul(late,.16),base,(.010,.0035,.0017),True)
    # Original 60–190 µm vessel apertures and soft longitudinal fibers.
    # Closed Voronoi boundaries read as leather on transverse wood.
    cells=n.node('ShaderNodeTexVoronoi',feature='F1',distance='EUCLIDEAN')
    n.feed(cells.inputs['Vector'],n.combine(n.mul(x,3200),n.mul(y,200),n.mul(zz,3300)));cells.inputs['Scale'].default_value=1
    col=n.node('ShaderNodeSeparateColor',mode='RGB');n.feed(col.inputs[0],cells.outputs['Color'])
    pores=n.mul(n.ramp(cells.outputs['Distance'],.30,.10),n.ramp(col.outputs[0],.40,.70))
    fiber=n.ramp(n.noise(n.combine(n.mul(x,1400),n.mul(y,40),n.mul(zz,1700)),1,2),.590 if role=='stock' else .52,.36 if role=='stock' else .32)
    base=n.mix(n.mul(fiber,.70 if role=='stock' else .65),base,(.017,.005,.0023),True)
    base=n.mix(n.mul(pores,.70),base,(.006,.0024,.0012),True)
    h=n.add(n.mul(late,-8e-6),n.mul(fiber,-6e-6),n.mul(pores,-28e-6))
    rough=n.add(.29 if role=='stock' else .40,n.mul(pores,.10),n.mul(late,.025));ao=n.mix(pores,1,.87)
    if role=='stock':
        # Paired original pointed panels; cutter directions have unit length,
        # so perpendicular pitch is exactly 25.4 / 20 = 1.27 mm on the side.
        dist=polygon(n,y,z,[(-.088,-.006),(-.069,-.018),(-.012,-.016),(.023,.003),(.011,.021),(-.043,.017)])
        facing=n.mul(n.ramp(ab(n,nx),.50,.88),n.ramp(ab(n,x),.010,.014))
        u,v=y,z;point_site='wrist_points'
        pressure=n.mul(oval(n,y,z,-.027,.000,.055,.019),wear[point_site])
    else:
        check=n.node('ShaderNodeAttribute',attribute_name='CheckPosition').outputs['Vector']
        u,v,_=n.split(check)
        dist=polygon(n,u,v,[(.198,-.035),(.214,-.045),(.312,-.038),(.333,0),(.312,.038),(.214,.045)])
        facing=n.ramp(nz,.50,.05);point_site='forend_points'
        pressure=n.mul(oval(n,u,ab(n,v),.250,.033,.062,.010),interval(n,u,.207,.320,.003),wear[point_site])
    inside=n.mul(n.ramp(dist,.0016,.0022),facing)
    cut_u=n.add(n.mul(u,.32),n.mul(v,math.sqrt(1-.32**2)));cut_v=sub(n,n.mul(u,.32),n.mul(v,math.sqrt(1-.32**2)))
    a=n.math('PINGPONG',cut_u,.000635)
    b=n.math('PINGPONG',cut_v,.000635)
    # Unit cutter normals give 20 LPI and an approximately 3:1 diamond.
    # Contact spans the entire grip. Individual cutter points flatten at
    # different rates as grain hardness varies; never polish a solid stripe.
    hardness=n.node('ShaderNodeTexWhiteNoise',noise_dimensions='3D')
    n.feed(hardness.inputs['Vector'],n.combine(n.math('FLOOR',n.math('DIVIDE',cut_u,.00127)),
           n.math('FLOOR',n.math('DIVIDE',cut_v,.00127)),n.add(17.3,n.mul(n.math('LESS_THAN',x,0),31.1)) if role=='stock' else 17.3))
    selected=n.ramp(sub(n,n.mul(pressure,.40 if role=='stock' else .50),hardness.outputs['Value']),-.04,.04)
    pressure=n.mul(n.ramp(pressure,.15,.65),selected)
    # Distance to either cutter: pointed diamond tops become flat under the
    # hands, with their grooves and the unhandled perimeter left intact.
    peak=n.math('MINIMUM',a,b);shape=n.math('DIVIDE',peak,.000635)
    cap=n.mix(pressure,1,.50)
    profile=n.math('MINIMUM',shape,cap)
    height=n.mul(sub(n,profile,1),.00030,inside)
    grooves=n.ramp(shape,.30,.08)
    border=n.mul(n.maximum(n.band(dist,.00050,.00017,.00018),n.band(dist,.00125,.00012,.00014)),facing)
    h=n.add(h,height,n.mul(border,-.00022))
    relief=n.maximum(n.mul(grooves,inside),border)
    base=n.mix(n.mul(relief,.78 if role=='stock' else .92),base,(.010,.0038,.0018),True)
    ao=n.mix(relief,ao,.70);rough=n.mix(inside,rough,.50 if role=='stock' else .65)
    rough=n.mix(n.mul(grooves,inside),rough,.78)
    # Cut end-grain absorbs more of the oil stain than the planed lands.
    # This construction response also exists on the unused counterpart.
    base=n.mix(n.mul(inside,.54 if role=='stock' else .53),base,(.010,.0038,.0018),True)
    worn=n.mul(pressure,inside,n.ramp(shape,.50,.72));sites[point_site]=worn
    base=n.mix(n.mul(worn,.80),base,(.20,.100,.044),True);rough=n.mix(worn,rough,.27 if role=='stock' else .36)
    # Oil finish settles in cut grooves even before use. Preserve it in the
    # clean counterpart; only flattened point tops change in the wear proof.
    oil=inside
    base=n.mix(n.mul(oil,grooves,.15),base,(.006,.0022,.0011),True)
    # Deliberately irregular bowls, concentrated at toe/heel and wood edges.
    # There is no overall noise wash and no change to silhouette geometry.
    if role=='stock':
        site='stock_toe';dents=[(-.292,-.106,.0121,.0051),
          (-.276,-.097,.005,.0018),(-.294,-.011,.003,.0015)]
    else:
        site='forend_edges';dents=[(.286,.0310,.0022,.0013),(.346,.0310,.0010,.0005),(.193,.0305,.0010,.0005)]
    all_dents=0
    for cy,cz,wy,wz in dents:
        u0=n.add(n.math('DIVIDE',sub(n,y,cy),wy),n.mul(n.math('DIVIDE',sub(n,z,cz),wz),.31))
        v0=n.math('DIVIDE',sub(n,z,cz),wz)
        u0=n.add(u0,n.mul(sub(n,n.noise(p,1450,2),.5),.36))
        r=n.add(n.math('POWER',ab(n,u0),1.5),n.math('POWER',ab(n,v0),1.4))
        dent=n.mul(n.math('MAXIMUM',sub(n,1,r),0),n.ramp(ab(n,nx),.10,.75),wear[site])
        # A short torn lip on one impact quadrant, interrupted by fibers.
        # A full bright upper arc reads as a stamped crescent.
        fracture=n.ramp(n.noise(n.combine(n.mul(y,2800),n.mul(z,5100),n.mul(x,350)),1,2),.42,.63)
        lip=n.mul(n.band(r,.90,.06,.09),n.ramp(v0,.12,.60),n.ramp(u0,-.05,.35),fracture,n.ramp(ab(n,nx),.10,.75),wear[site])
        all_dents=n.maximum(all_dents,dent,lip)
        h=n.add(h,n.mul(dent,dent,-.00018),n.mul(lip,.000020))
        base=n.mix(n.mul(dent,.75),base,(.011,.0048,.0025),True)
        base=n.mix(n.mul(lip,.65),base,(.25,.14,.068),True);rough=n.mix(n.maximum(dent,lip),rough,.63)
    sites[site]=all_dents
    # Exposed cut wood is porous; cavities lose reflected visibility. Oil on
    # the flat lands and flattened tips retains its soft Fresnel sheen.
    # This is effective reflection visibility, not a different wood albedo.
    spec=n.mix(inside,.49 if role=='stock' else .45,.16)
    spec=n.mix(n.mul(relief,.94),spec,.012)
    spec=n.mix(pores,spec,.10)
    spec=n.mix(worn,spec,.33)
    return finish(n,base,rough,0,h,ao,sites,spec)

def ammo(name,role,fired):
    n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n);fine=n.noise(p,6500,2)
    h=n.mul(sub(n,fine,.5),1.5e-6);rough=n.add(.30,n.mul(fine,.065))
    if role in ('brass','primer'):
        base=(.49,.285,.078) if role=='brass' else (.37,.34,.25);metal=1
        patch=n.noise(p,600,2);tarnish=n.mul(n.ramp(patch,.48,.76),.21)
        base=n.mix(tarnish,base,(.17,.086,.024),True)
        radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(z,z)))
        h=n.add(h,n.mul(n.math('SINE',n.mul(radius,math.tau/.00015)),1e-6))
        if role=='brass':
            from pathlib import Path
            im=n.node('ShaderNodeTexImage',interpolation='Linear',extension='CLIP')
            im.image=bpy.data.images.load(str(Path(__file__).resolve().parents[1]/'build/markings/headstamp.png'),check_existing=True)
            im.image.colorspace_settings.name='Non-Color'
            n.feed(im.inputs['Vector'],n.combine(n.add(n.mul(x,1/.0224),.5),n.add(n.mul(z,1/.0224),.5),0))
            stamp=n.mul(im.outputs['Color'],n.ramp(ny,-.5,-.95))
            h=n.add(h,n.mul(stamp,-.00008));base=n.mix(n.mul(stamp,.75),base,(.045,.023,.008),True)
    else:
        base=(.255,.009,.006);metal=0;rough=n.add(.46,n.mul(fine,.04))
        angle=n.math('ARCTAN2',z,x);ribs=n.math('SINE',n.mul(angle,160))
        h=n.add(h,n.mul(ribs,n.ramp(ab(n,ny),.40,.10),.000009))
        soot=n.mul(n.ramp(y,.061,.069),n.add(.94,n.mul(n.noise(p,600,2),.06))) if fired else 0
        if role=='mouth':soot=n.maximum(soot,.92)
        base=n.mix(soot,base,(.008,.003,.0018),True);rough=n.mix(soot,rough,.82)
    return finish(n,base,rough,metal,h)

def plate(name):
    n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n)
    cuts=n.maximum(n.ramp(n.math('PINGPONG',n.add(x,z),.00068),.00018,.00005),
                   n.ramp(n.math('PINGPONG',sub(n,x,z),.00068),.00018,.00005))
    return finish(n,(.009,.008,.007),.64,0,n.mul(cuts,n.ramp(ny,-.4,-.9),-.00011))

def assign(amount=1,disabled=()):
    from parameters import HEADS
    wear={s:0 if s in disabled else amount for s in SITES};records={}
    parts=sorted([o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')],key=lambda o:o.name)
    for owner,ob in enumerate(parts,1):
        isammo=ob.name.startswith(('Live','Hull','Insert'))
        origin=tuple(v*.001 for v in HEADS[ob['bone']]) if isammo else (0,0,0)
        for name,domain,data in [('FinishPosition','POINT',[(v.co.x-origin[0],v.co.y-origin[1],v.co.z-origin[2]) for v in ob.data.vertices]),
                                 ('FinishNormal','CORNER',[row.vector[:] for row in ob.data.corner_normals])]:
            old=ob.data.attributes.get(name)
            if old:ob.data.attributes.remove(old)
            attr=ob.data.attributes.new(name,'FLOAT_VECTOR',domain);attr.data.foreach_set('vector',[a for row in data for a in row])
        if ob.name=='Forend_Walnut':
            attr=ob.data.attributes.new('CheckPosition','FLOAT_VECTOR','POINT');values=[]
            # Developed lower section, around its 1.6-mm bottom corners and
            # up the sides; continuous across the bottom, not a projected grid.
            for vertex in ob.data.vertices:
                x,y,z=vertex.co;ym=y*1000
                stations=[(181.5,17.2,12),(211,17.2,12.6),(242,16.4,14.8),(279,15.35,17.3),(314,14.3,19.6),(340,13.53,21.43),(355,11.5,32.3)]
                a,b=next(((a,b) for a,b in zip(stations,stations[1:]) if a[0]<=ym<=b[0]),(stations[0],stations[1]) if ym<181.5 else (stations[-2],stations[-1]))
                t=(ym-a[0])/(b[0]-a[0]);w=(a[1]+t*(b[1]-a[1]))*.001;bottom=(a[2]+t*(b[2]-a[2]))*.001;r=.0016
                if abs(x)<w-r:s=x
                elif z<bottom+r:
                    angle=math.atan2(max(0,abs(x)-(w-r)),max(0,bottom+r-z));s=math.copysign(w-r+r*angle,x)
                else:s=math.copysign(w-r+r*math.pi/2+z-bottom-r,x)
                values.extend((y,s,0))
            attr.data.foreach_set('vector',values)
        roles=[]
        for i,old in enumerate(list(ob.data.materials)):
            key=old.name.removeprefix('CP_').split('.')[0];name='Covey_'+ob.name+'_'+str(i)
            if isammo:role=key;mat=ammo(name,key,ob.name.startswith('Hull'))
            elif key=='wood':role='stock' if ob.name=='Stock_Walnut' else 'forend';mat=wood(name,role,wear)
            elif key=='plate':role='butt';mat=plate(name)
            elif key=='brass':
                role='bead';n=Nodes(name);mat=finish(n,(.62,.50,.26),.31,1)
            else:
                if ob.name in ('Action_Body','Trigger_Plate','Top_Strap','Hinge_Pin'):role='case'
                elif ob.name.startswith('Barrel_') and ob.name in ('Barrel_R','Barrel_L'):role='barrel'
                elif ob.name=='Top_Lever':role='lever'
                elif ob.name in ('Trigger_Guard','Guard_RearTang'):role='guard'
                elif ob.name in ('Front_Trigger','Rear_Trigger'):role='trigger'
                elif ob.name=='Tang_Safety':role='safety'
                elif ob.name=='Solid_TopRib':role='rib'
                elif key=='steel':role='bright'
                else:role='dark'
                mat=steel(name,role,wear)
            # Independent selected-to-active identity witness. bake_form.py
            # saves it separately and strips it from the delivered color map.
            node=mat.node_tree.nodes.new('ShaderNodeValue');node.name='OUT_owner'
            node.outputs[0].default_value=owner/255
            ob.data.materials[i]=mat;roles.append(role)
        records[ob.name]=roles
    bpy.context.scene['finish_wear']=amount
    return records
