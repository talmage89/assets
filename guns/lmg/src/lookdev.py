"""Original manufactured finishes and nine independently switchable use sites.

Coordinates are meter-valued rest attributes. Noise describes molding/tooling,
or fractures the margins of an already located rub; it cannot spread damage.
No photograph or reference-derived mask enters any material.
"""
import math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from kit.materials import Nodes
BASE=Path(__file__).resolve().parents[1]
SITES=('receiver','cover','handle','flash','regulator','ports','feet','box','butt')
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
    bright=key=='steel' and not part.startswith('Bipod_Extension')
    base=(.0015,.00154,.0015) if paint else (.16,.164,.155) if bright else (.044,.045,.042)
    rough=.42 if paint else .48 if bright else .67
    metal=0 if paint else .95 if bright else .45;spec=.161 if paint else .56
    grain=n.noise(p,1250,2);fine=n.noise(p,4300,2)
    rough=n.add(rough,n.mul(sub(n,grain,.5),.075))
    h=n.mul(sub(n,fine,.5),5e-6 if paint else 9e-6)
    # Phosphate's crystal skin, modest machining rings, never broad color noise.
    if part=='Barrel_Exterior':
        heat=n.maximum(n.band(y,.245,.025,.040),n.band(y,.531,.018,.032))
        heat=n.mul(heat,wear if omit!='all' else 0)
        base=n.mix(heat,base,(.021,.020,.017),True)
        rough=n.mix(heat,rough,.74)
        rings=n.math('SINE',n.mul(y,math.tau/.00028));h=n.add(h,n.mul(rings,.8e-6))
    abrasion=0;sharp=1
    if part=='Receiver_Sheet':
        lower=rub(n,p,ab(n,sub(n,z,.054)),y,-.047,.028,.0030)
        front=rub(n,p,ab(n,sub(n,z,.065)),y,.188,.232,.0038)
        upper=rub(n,p,ab(n,sub(n,z,.120)),y,-.045,.030,.0027)
        abrasion=n.mul(n.maximum(lower,front,upper),n.ramp(ax,.0225,.024),active('receiver'))
        sharp=mn(n,ab(n,sub(n,z,.054)),ab(n,sub(n,z,.120)))
    elif part.startswith('Receiver_RearDoubler'):
        abrasion=n.mul(rub(n,p,ab(n,sub(n,y,-.050)),z,.059,.109,.0011),active('receiver'))
    elif part=='SideWell_Housing':
        abrasion=n.mul(rub(n,p,ab(n,sub(n,y,.132)),z,.067,.089,.0021),active('receiver'))
    elif part=='FeedCover_Shell':
        rear=rub(n,p,ab(n,sub(n,y,-.051)),x,-.028,.023,.0032,.009)
        side=rub(n,p,ab(n,sub(n,z,.1415)),y,-.035,.035,.0027,.015)
        side=n.mul(side,n.ramp(ax,.024,.028))
        abrasion=n.mul(n.maximum(rear,side),active('cover'))
        sharp=mn(n,ab(n,sub(n,y,-.051)),ab(n,sub(n,z,.145)))
    elif part.startswith('FeedCover_PressedBead'):
        abrasion=n.mul(interval(n,y,-.020,.080,.022),n.ramp(nz,.35,.85),active('cover'))
        sharp=ab(n,sub(n,z,.146))
    elif part.startswith('FeedCover_SidePress'):
        abrasion=n.mul(rub(n,p,ab(n,sub(n,z,.139)),y,-.018,.035,.0013),active('cover'))
    elif part.startswith('Bipod_Foot'):
        # Ground and stones abrade the end lips and a few broad pressure lands.
        edge=n.maximum(n.ramp(u,.18,.03),n.ramp(u,.82,.97),n.ramp(w,.18,.03))
        broken=n.ramp(n.noise(n.vec('MULTIPLY',p,(280,100,210)),1,2),.36,.53)
        abrasion=n.mul(edge,broken,active('feet'));sharp=.0001
    core=n.mul(abrasion,n.ramp(sharp,.00016,.000025),n.ramp(n.noise(p,180,2),.63,.78),.6)
    base=n.mix(abrasion,base,(.062,.061,.057),True);rough=n.mix(abrasion,rough,.88)
    metal=n.mix(abrasion,metal,.08);spec=n.mix(abrasion,spec,.56)
    base=n.mix(core,base,(.235,.229,.209),True);rough=n.mix(core,rough,.49);metal=n.mix(core,metal,1)
    h=n.add(h,n.mul(abrasion,-.000016))
    carbon=0
    if part=='FlashHider':
        # Carbon at the lip and downstream of the five actual slots.
        carbon=n.mul(n.ramp(y,.681,.704),n.add(.70,n.mul(n.noise(p,310,2),.30)),active('flash'))
    elif part.startswith(('GasRegulator','Regulator_Grip')):
        carbon=n.mul(n.ramp(y,.540,.552),n.add(.75,n.mul(grain,.25)),active('regulator'))
    elif part in ('Receiver_Sheet','LinkPort_Rim','ChargingGuide'):
        around=n.mul(interval(n,y,.105,.217,.010),interval(n,z,.089,.119,.007),n.ramp(x,.021,.025))
        bottom=n.mul(interval(n,y,.124,.187,.008),n.ramp(z,.064,.053))
        carbon=n.mul(n.maximum(around,bottom),n.add(.70,n.mul(grain,.30)),active('ports'))
    base=n.mix(carbon,base,(.00065,.00060,.00050),True);rough=n.mix(carbon,rough,.93)
    metal=n.mix(carbon,metal,0);spec=n.mix(carbon,spec,.22)
    mark=0
    if part=='Receiver_Sheet':
        mark=n.mul(text(n,sub(n,1,div(n,n.add(y,.040),.120)),div(n,sub(n,z,.079),.015),'receiver'),n.ramp(n.mul(nx,-1),.85,.98))
    base=n.mix(mark,base,(.007,.0072,.0068),True);h=n.add(h,n.mul(mark,-.000065))
    if part.startswith(('Belt_Link','EjectedLink')) or part=='Link_Proof':
        base=n.mix(grain,(.023,.024,.023),(.042,.043,.040),True);metal=.65;rough=n.add(.53,n.mul(grain,.10))
        cuff=n.maximum(n.ramp(v,.08,.015),n.ramp(v,.92,.985))
        base=n.mix(n.mul(cuff,.5),base,(.090,.087,.076),True);rough=n.mix(cuff,rough,.46)
    return finish(n,base,rough,metal,h,spec,n.maximum(abrasion,carbon))

def polymer(name,part,key,wear,omit):
    n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
    fine=n.noise(p,1100,2);mold=n.noise(p,430,2)
    rubber=key=='rubber';base=(.004,.0042,.0039) if rubber else (.011,.012,.011)
    rough=n.add(.81 if rubber else .73,n.mul(sub(n,mold,.5),.07))
    touch=0;site=''
    if part=='CarryHandle_Grip':
        site='handle';touch=n.mul(interval(n,y,.164,.240,.009),n.ramp(nz,-.5,.4))
    elif part=='Buttpad' or part=='Stock_Sculpt':
        site='butt'
        touch=n.mul(n.ramp(y,-.302,-.327),n.maximum(n.ramp(z,.075,.100),n.ramp(z,.004,-.018),n.mul(n.ramp(ab(n,x),.015,.020),.7)))
    elif part=='Box_Shell' or part.startswith(('Box_MoldRib','Box_EndRib','Box_ClipBacking')):
        site='box'
        bottom=n.ramp(z,-.088,-.114)
        corners=n.mul(n.ramp(ab(n,x),.036,.055),n.maximum(n.ramp(y,.145,.128),n.ramp(y,.187,.203)))
        # Sparse cross-direction drag scuffs inside bottom impact corners.
        edge=n.ramp(n.add(n.mul(n.noise(n.vec('MULTIPLY',p,(420,190,120)),1,2),.72),n.mul(mold,.28)),.41,.57)
        touch=n.mul(bottom,corners,edge)
    strength=wear if omit not in ('all',site) else 0;touch=n.mul(touch,strength)
    rough=n.mix(touch,rough,.36 if site=='handle' else .49 if site=='butt' else .87)
    rubbed=(.016,.017,.015) if site=='butt' else (.032,.033,.030) if site=='box' else (.008,.0085,.008)
    base=n.mix(touch,base,rubbed,True)
    h=n.mul(sub(n,mold,.5),n.mix(touch,240e-6 if not rubber else 160e-6,16e-6))
    h=n.add(h,n.mul(sub(n,fine,.5),18e-6))
    if part in ('Handguard_Sculpt','PistolGrip_Sculpt'):
        held=n.mul(interval(n,y,.270,.425,.020),n.ramp(ab(n,nx),.5,.95)) if part=='Handguard_Sculpt' else interval(n,z,-.060,.018,.012)
        held=n.mul(held,wear if omit!='all' else 0,n.ramp(n.noise(p,85,2),.30,.75))
        rough=n.mix(held,rough,.50)
        base=n.mix(n.mul(held,.65),base,(.008,.0085,.008),True)
    # The two mold halves leave a fine parting line around the center plane.
    seam=n.mul(n.band(x,0,.00018,.00012),n.ramp(ab(n,nx),.5,.05))
    h=n.add(h,n.mul(seam,.000055))
    return finish(n,base,rough,0,h,.60,touch)

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
