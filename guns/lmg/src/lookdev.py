"""Original manufactured finishes and eleven independently switchable use sites.

Coordinates are meter-valued rest attributes. Noise describes molding/tooling,
or fractures the margins of an already located rub; it cannot spread damage.
No photograph or reference-derived mask enters any material.
"""
import math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from kit.materials import Nodes
import finish_parameters as F
from wear_patterns import scratches
BASE=Path(__file__).resolve().parents[1]
SITES=F.SITES
def sub(n,a,b):return n.math('SUBTRACT',a,b)
def ab(n,a):return n.math('ABSOLUTE',a)
def div(n,a,b):return n.math('DIVIDE',a,b)
def mn(n,*xs):
    r=xs[0]
    for x in xs[1:]:r=n.math('MINIMUM',r,x)
    return r
def interval(n,x,a,b,f=.004):return n.mul(n.ramp(x,a-f,a),n.ramp(x,b+f,b))
def inp(n):
    p=n.node('ShaderNodeAttribute',attribute_name='FinishPosition').outputs['Vector']
    normal=n.node('ShaderNodeAttribute',attribute_name='FinishNormal').outputs['Vector']
    q=n.node('ShaderNodeAttribute',attribute_name='PartCoord').outputs['Vector']
    return p,*n.split(p),*n.split(normal),*n.split(q)
def finish(n,base,rough,metal,h=0,spec=.56,wear=0):
    n.channel('specular_factor',spec);n.channel('micro_ao',1);n.channel('wear',wear)
    m=n.finish(base,rough,metal,h,bump=1)
    n.feed(m.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'],n.mul(spec,.5))
    return m
def text(n,u,v,name):
    tex=n.node('ShaderNodeTexImage',extension='CLIP',interpolation='Linear')
    tex.image=bpy.data.images.load(str(BASE/'build/markings'/(name+'.png')),check_existing=True)
    tex.image.colorspace_settings.name='Non-Color';n.feed(tex.inputs['Vector'],n.combine(u,v,0))
    return tex.outputs['Color']
def rub(n,p,d,along,start,end,width,fade=.008):
    # A connected core with multiscale irregular margins, fading at the ends.
    warped=n.add(d,n.mul(sub(n,n.noise(p,480,2),.5),width*.32))
    size=n.mul(width,n.add(.62,n.mul(n.noise(p,95,2),.95)))
    return n.mul(n.ramp(div(n,warped,size),1,.65),interval(n,along,start,end,fade))

def steel(name,part,key,wear,omit):
    n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n);ax=ab(n,x)
    active=lambda site:wear if omit not in (site,'all') else 0
    paint=key=='paint' or part.startswith(('FeedCover_Shell','FeedCover_PressedBead','FeedCover_SidePress','FeedCover_Flange','Receiver_Rivet','HeatShield','SideWell_DustCover','SideWell_FlapRib','SideWell_ThumbTab'))
    phosphate_color=F.BIPOD_PHOSPHATE if part.startswith('Bipod_') else F.PHOSPHATE
    bright=key=='steel' and not part.startswith('Bipod_Extension')
    base=F.PAINT if paint else (.16,.164,.155) if bright else phosphate_color
    rough=(.33 if part.startswith('FeedCover_') else F.PAINT_ROUGH) if paint else .48 if bright else F.PHOSPHATE_ROUGH
    metal=0 if paint else .95 if bright else F.PHOSPHATE_METAL;spec=F.PAINT_SPEC if paint else .85
    grain=n.ramp(n.noise(p,800,2),.34,.66);fine=n.noise(p,4300,2)
    rough=n.add(rough,n.mul(sub(n,grain,.5),.075))
    h=n.mul(sub(n,fine,.5),12e-6) if paint else n.add(n.mul(sub(n,grain,.5),12e-6),n.mul(sub(n,fine,.5),8e-6))
    if not paint and not bright:
        # Conversion-bath crystal/oxide variation, not deposited weather.
        crystal=n.ramp(n.noise(p,220,3),.34,.66)
        base=n.mix(crystal,tuple(c*.80 for c in phosphate_color),tuple(c*1.20 for c in phosphate_color),True)
        rough=n.add(rough,n.mul(sub(n,crystal,.5),.10))
    if part.startswith('Bipod_Extension'):
        base=(.25,.27,.29);rough=n.add(.27,n.mul(grain,.12));metal=.95
    # Phosphate's crystal skin, modest machining rings, never broad color noise.
    if part.startswith(('Barrel_Exterior','BarrelSeat','BarrelCollar','GasBlock','GasTube','GasRegulator','Regulator_Grip')):
        heat=n.maximum(n.band(y,.245,.025,.040),n.band(y,.531,.018,.032))
        heat=n.mul(heat,wear if omit!='all' else 0)
        base=n.mix(heat,base,(.007,.006,.0045),True)
        rough=n.mix(heat,rough,.66)
        if part=='Barrel_Exterior':
            oiled=n.mul(interval(n,y,.545,.663,.008),n.ramp(nz,-.2,.5),wear if omit!='all' else 0)
            rough=n.mix(oiled,rough,.32)
        rings=n.math('SINE',n.mul(y,math.tau/.00028));h=n.add(h,n.mul(rings,.8e-6))
    abrasion=0;sharp=1
    if part=='Receiver_Sheet':
        lower=rub(n,p,ab(n,sub(n,z,.054)),y,-.047,.226,.00125)
        front=rub(n,p,ab(n,sub(n,z,.065)),y,.148,.232,.00173)
        upper=rub(n,p,ab(n,sub(n,z,.120)),y,-.045,.224,.00107)
        end=rub(n,p,mn(n,ab(n,sub(n,y,-.05)),ab(n,sub(n,y,.233))),z,.058,.118,.00107)
        ridge=rub(n,p,ab(n,sub(n,z,.0915)),y,-.035,.214,.00043)
        abrasion=n.mul(n.maximum(lower,front,upper,end,ridge),n.ramp(ax,.0225,.024),active('receiver'))
        sharp=mn(n,ab(n,sub(n,z,.054)),ab(n,sub(n,z,.120)))
    elif part.startswith('Receiver_RearDoubler'):
        abrasion=n.mul(rub(n,p,ab(n,sub(n,y,-.050)),z,.059,.109,.00060),active('receiver'))
    elif part=='SideWell_Housing':
        abrasion=n.mul(rub(n,p,ab(n,sub(n,y,.132)),z,.067,.089,.00113),active('receiver'))
    elif part=='FeedCover_Shell':
        rear=rub(n,p,ab(n,sub(n,y,-.051)),x,-.028,.023,.0006,.009)
        side=rub(n,p,ab(n,sub(n,z,.1415)),y,-.035,.221,.00035,.008)
        side=n.mul(side,n.ramp(ax,.024,.028))
        lower=rub(n,p,ab(n,sub(n,z,.121)),y,-.032,.225,.00025,.010)
        abrasion=n.mul(n.maximum(rear,side,lower),n.ramp(n.noise(n.vec('MULTIPLY',p,(180,65,180)),1,2),.48,.64),active('cover'))
        scuff=n.mul(scratches(n,p,x,y,z,nz),active('cover_top'))
        abrasion=n.maximum(abrasion,scuff)
        sharp=mn(n,ab(n,sub(n,y,-.051)),ab(n,sub(n,z,.145)))
    elif part.startswith('FeedCover_PressedBead'):
        abrasion=n.mul(interval(n,y,-.020,.172,.014),n.ramp(nz,.75,.95),n.ramp(n.noise(p,240,2),.56,.68),active('cover'))
        sharp=ab(n,sub(n,z,.146))
    elif part.startswith('FeedCover_SidePress'):
        abrasion=n.mul(rub(n,p,ab(n,sub(n,z,.139)),y,-.018,.110,.00025),active('cover'))
    elif part.startswith('Receiver_Rivet'):
        radial=n.math('SQRT',n.add(n.mul(sub(n,v,.5),sub(n,v,.5)),n.mul(sub(n,w,.5),sub(n,w,.5))))
        crown=n.mul(n.ramp(ab(n,nx),.65,.9),n.ramp(n.noise(p,680,2),.425,.645))
        ring=n.mul(n.ramp(radial,.28,.44),n.ramp(ab(n,nx),.3,.7))
        abrasion=n.mul(n.maximum(crown,ring),active('rivets'))
        sharp=n.mul(sub(n,1,n.ramp(radial,.38,.48)),.001)
    elif part.startswith('Bipod_Foot'):
        # Ground and stones abrade the end lips and a few broad pressure lands.
        edge=n.maximum(n.ramp(u,.20,.03),n.ramp(u,.80,.97),n.ramp(w,.20,.03))
        broken=n.ramp(n.noise(n.vec('MULTIPLY',p,(280,100,210)),1,2),.36,.53)
        abrasion=n.mul(edge,broken,active('feet'));sharp=.0001
    core=n.mul(abrasion,n.ramp(sharp,.0007,.00015),n.ramp(n.noise(p,180,2),.47,.62),.8)
    base=n.mix(abrasion,base,(.075,.078,.078),True);rough=n.mix(abrasion,rough,.66)
    metal=n.mix(abrasion,metal,.12);spec=n.mix(abrasion,spec,.56)
    base=n.mix(core,base,(.50,.52,.53),True);rough=n.mix(core,rough,.35);metal=n.mix(core,metal,1)
    h=n.add(h,n.mul(abrasion,-.000016))
    carbon=0
    if part=='FlashHider':
        # Carbon at the lip and downstream of the five actual slots.
        carbon=n.mul(n.ramp(y,.687,.704),n.add(.70,n.mul(n.noise(p,310,2),.30)),active('flash'))
    elif part.startswith(('GasRegulator','Regulator_Grip')):
        carbon=n.mul(n.ramp(y,.5515,.5555),n.add(.75,n.mul(grain,.25)),active('regulator'))
    elif part in ('Receiver_Sheet','LinkPort_Rim','ChargingGuide'):
        around=n.mul(interval(n,y,.105,.217,.010),interval(n,z,.089,.119,.007),n.ramp(x,.021,.025))
        bottom=n.mul(interval(n,y,.124,.187,.008),n.ramp(z,.064,.053))
        carbon=n.mul(n.maximum(around,bottom),n.add(.70,n.mul(grain,.30)),active('ports'))
    base=n.mix(carbon,base,(.0022,.0020,.0017),True);rough=n.mix(carbon,rough,.93)
    metal=n.mix(carbon,metal,0);spec=n.mix(carbon,spec,.22)
    mark=0
    if part=='Receiver_Sheet':
        mark=n.mul(text(n,sub(n,1,div(n,n.add(y,.040),.120)),div(n,sub(n,z,.079),.015),'receiver'),n.ramp(n.mul(nx,-1),.85,.98))
    base=n.mix(mark,base,(.007,.0072,.0068),True);h=n.add(h,n.mul(mark,-.000065))
    if part.startswith(('Belt_Link','EjectedLink')) or part=='Link_Proof':
        base=n.mix(n.noise(p,650,3),(.09,.098,.102),(.165,.175,.18),True);metal=.85;rough=n.add(.61,n.mul(grain,.12))
        cuff=n.maximum(n.ramp(v,.08,.015),n.ramp(v,.92,.985))
        base=n.mix(n.mul(cuff,.5),base,(.090,.087,.076),True);rough=n.mix(cuff,rough,.46)
    return finish(n,base,rough,metal,h,spec,n.maximum(abrasion,carbon))

def polymer(name,part,key,wear,omit):
    n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
    rubber=key=='rubber'
    family='handguard' if part.startswith('Handguard') else 'stock' if part.startswith('Stock') else 'grip' if part.startswith(('PistolGrip','Grip_')) else 'box' if part.startswith('Box') else 'handle'
    color,rgh,spec=F.POLYMER[family]
    grain_scale,skin,rough_variation=F.POLYMER_GRAIN[family]
    if rubber:grain_scale,skin,rough_variation=1000,12e-6,.12
    fine=n.noise(p,4300,2);mold=n.ramp(n.noise(p,grain_scale,2),.34,.66)
    base=(.006,.0063,.006) if rubber else color
    rough=n.add(.78 if rubber else rgh,n.mul(sub(n,mold,.5),rough_variation))
    touch=0;site=''
    if part=='CarryHandle_Grip':
        site='handle';touch=n.mul(interval(n,y,.164,.240,.009),n.ramp(nz,.64,.92))
    elif part=='Buttpad' or part=='Stock_Sculpt':
        site='butt'
        touch=n.mul(n.ramp(y,-.311,-.323),n.maximum(n.ramp(z,.095,.105),n.ramp(z,-.015,-.023)))
    elif part=='Box_Shell' or part.startswith(('Box_MoldRib','Box_EndRib','Box_ClipBacking')):
        site='box'
        bottom=n.ramp(z,-.105,-.140)
        corners=n.mul(n.ramp(ab(n,x),.047,.055),n.maximum(n.ramp(y,.132,.125),n.ramp(y,.201,.205)))
        # Sparse cross-direction drag scuffs inside bottom impact corners.
        edge=n.ramp(n.add(n.mul(n.noise(n.vec('MULTIPLY',p,(420,190,120)),1,2),.72),n.mul(mold,.28)),.43,.59)
        touch=n.mul(bottom,corners,edge)
    strength=wear if omit not in ('all',site) else 0;touch=n.mul(touch,strength)
    rough=n.mix(touch,rough,.18 if site=='handle' else .39 if site=='butt' else .79)
    rubbed=(.020,.021,.021) if site=='butt' else (.043,.044,.041) if site=='box' else (.005,.0055,.006)
    base=n.mix(touch,base,rubbed,True)
    polished=min(2e-6,skin*.5)
    h=n.mul(sub(n,mold,.5),n.mix(touch,skin,polished))
    h=n.add(h,n.mul(sub(n,fine,.5),1e-6))
    if part in ('Handguard_Sculpt','PistolGrip_Sculpt'):
        held=n.mul(interval(n,y,.270,.425,.020),n.ramp(ab(n,nx),.5,.95)) if part=='Handguard_Sculpt' else interval(n,z,-.060,.018,.012)
        held=n.mul(held,wear if omit!='all' else 0,n.ramp(n.noise(p,85,2),.30,.75))
        rough=n.mix(held,rough,.55 if part=='Handguard_Sculpt' else .34)
        base=n.mix(n.mul(held,.35),base,(.0055,.0063,.007) if part=='Handguard_Sculpt' else (.030,.032,.034),True)
    # The two mold halves leave a fine parting line around the center plane.
    seam=n.mul(n.band(x,0,.00018,.00012),n.ramp(ab(n,nx),.5,.05))
    h=n.add(h,n.mul(seam,.000055))
    return finish(n,base,rough,0,h,spec,touch)

def ammo(name,part,key):
    n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
    q=n.node('ShaderNodeAttribute',attribute_name='AmmoPosition').outputs['Vector'];a,b,c=n.split(q)
    tool=n.noise(n.vec('MULTIPLY',q,(3000,32,3000)),1,2)
    rough=n.add(.28,n.mul(tool,.24));metal=1
    draw=n.noise(n.vec('MULTIPLY',q,(7200,180,7200)),1,2)
    press=n.noise(n.vec('MULTIPLY',q,(800,100,800)),1,2)
    if key=='copper':
        base=n.mix(press,(.425,.147,.050),(.49,.178,.066),True)
        green=n.ramp(n.add(b,n.mul(sub(n,press,.5),.00032)),.0511,.0515);base=n.mix(green,base,(.010,.105,.029),True)
        metal=n.mix(green,1,0);rough=n.mix(green,n.add(.25,n.mul(draw,.25)),.58)
        return finish(n,base,rough,metal,n.mul(sub(n,draw,.5),5e-6),.56)
    base=n.mix(tool,(.37,.23,.062),(.50,.325,.105),True)
    base=n.mix(n.mul(n.ramp(press,.35,.68),.23),base,(.225,.153,.058),True)
    anneal=n.mul(n.ramp(n.add(b,n.mul(sub(n,press,.5),.0030)),.030,.035),n.add(.70,n.mul(press,.30)));base=n.mix(anneal,base,(.195,.151,.087),True);rough=n.mix(anneal,rough,.53)
    head=n.ramp(ny,-.60,-.96);r=n.math('SQRT',n.add(n.mul(a,a),n.mul(c,c)))
    stamp=n.mul(text(n,n.add(.5,div(n,a,.0096)),n.add(.5,div(n,c,.0096)),'headstamp'),head)
    primer=n.mul(head,n.ramp(r,.0019,.0016));seal=n.mul(head,n.band(r,.00184,.00008,.00004))
    base=n.mix(primer,base,(.23,.24,.22),True);base=n.mix(seal,base,(.065,.012,.009),True)
    if part in ('Case_Proof','EjectedCase_Case'):
        soot=n.ramp(b,.037,.043);base=n.mix(soot,base,(.018,.015,.008),True);rough=n.mix(soot,rough,.78)
    h=n.add(n.mul(sub(n,draw,.5),4e-6),n.mul(stamp,-.000045),n.mul(seal,-.000025))
    return finish(n,base,rough,metal,h,.56)

def assign(wear,omit=''):
    records={}
    for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
        part=ob.name
        shift=Vector((dict(Cartridge_Proof=.4,Case_Proof=.5,Link_Proof=.6).get(part,0),0,0))
        vertices=[ob.matrix_world@v.co-shift for v in ob.data.vertices]
        lo=Vector([min(v[k] for v in vertices) for k in range(3)]);hi=Vector([max(v[k] for v in vertices) for k in range(3)])
        center=Vector((0,.145,.124)) if part.startswith('Belt_') else Vector((.055,.150,.090)) if part.startswith('EjectedCase') else Vector((0,0,0))
        normal=ob.matrix_world.to_3x3().inverted().transposed()
        for attr,values,domain in [('FinishPosition',vertices,'POINT'),('FinishNormal',[(normal@r.vector).normalized() for r in ob.data.corner_normals],'CORNER'),('PartCoord',[Vector([(v[k]-lo[k])/max(hi[k]-lo[k],1e-8) for k in range(3)]) for v in vertices],'POINT'),('AmmoPosition',[v-center for v in vertices],'POINT')]:
            old=ob.data.attributes.get(attr)
            if old:ob.data.attributes.remove(old)
            field=ob.data.attributes.new(attr,'FLOAT_VECTOR',domain);field.data.foreach_set('vector',[a for v in values for a in v])
        roles=[]
        for i,old in enumerate(list(ob.data.materials)):
            key=old.name.removeprefix('Inspection_').split('.')[0];name='H56_'+part+'_'+str(i)
            if key in ('polymer','rubber'):mat=polymer(name,part,key,wear,omit)
            elif key in ('brass','copper'):mat=ammo(name,part,key)
            else:mat=steel(name,part,key,wear,omit)
            ob.data.materials[i]=mat;roles.append(key)
        records[part]=roles
    return dict(wear=wear,omitted_site=omit,parts=records)
