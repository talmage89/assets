"""Original low-poly pole hardware, built as manufactured assemblies in metres.

Quick diagnostic materials only. Fine grain, threads, markings and corrosion
are reserved for the later single-family atlas, not extra geometry.
"""
import math,random
from pathlib import Path
import bpy
from mathutils import Vector
from kit import model as G
from plan import FT,IN
from span import sample

M={}


def palette():
    colors={'Wood':((.105,.081,.058),.9,0),'Endgrain':((.17,.13,.085),.9,0),
      'Steel':((.25,.28,.27),.56,.8),'Porcelain':((.11,.052,.025),.24,0),
      'Polymer':((.31,.33,.32),.72,0),'Paint':((.28,.32,.30),.73,0),
      'Cable':((.009,.012,.013),.7,0),'Aluminum':((.24,.26,.25),.48,.85),
      'Guard':((.55,.36,.028),.82,0),'Recess':((.021,.016,.011),.95,0),'Vine':((.045,.075,.019),.88,0)}
    for name,(color,rough,metal) in colors.items():
        m=bpy.data.materials.new('Utility_'+name);m.use_nodes=True
        p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
        p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
        m['checkpoint_material']=True;M[name]=m


class Assembly:
    def __init__(self,name):
        self.root=G.pivot(name,(0,0,0));self.root['static_root']=True;self.root['asset_set']='Utility'
        self.objects=[];self.sockets={}
    def add(self,ob,component):
        ob.parent=self.root;ob['component']=component;ob['asset_set']='Utility';self.objects.append(ob);return ob
    def box(self,name,p,size,mat='Steel',r=0,component='hardware'):
        return self.add(G.box(name,p,size,M[mat],r,1),component)
    def rod(self,name,a,b,r,mat='Steel',n=8,component='hardware'):
        if getattr(self,'bank_lod',False):n=max(4,round(n*.58))
        return self.add(G.cylinder(name,a,b,r,M[mat],n),component)
    def tube(self,name,pts,r,mat='Cable',n=6,component='leads'):
        if getattr(self,'bank_lod',False):n=4;pts=pts[::2]+([pts[-1]] if len(pts)%2==0 else [])
        return self.add(G.tube(name,pts,r,M[mat],n),component)
    def lathe(self,name,profile,xy=(0,0),mat='Porcelain',n=12,component='hardware'):
        if getattr(self,'bank_lod',False):n=max(6,round(n*.58))
        return self.add(G.lathe(name,profile,M[mat],n,center=xy),component)
    def socket(self,name,p,kind='conductor',diameter=None):
        ob=G.pivot(self.root.name+'__Socket_'+name,p);ob.parent=self.root;ob['socket_kind']=kind
        if diameter:ob['diameter_m']=diameter
        self.sockets[name]=ob;return ob
    def bolt(self,p,axis=(0,1,0),length=.36):
        p,axis=Vector(p),Vector(axis)
        self.rod('5/8 inch through bolt',p-axis*length/2,p+axis*length/2,.00794,n=6)
        for sign in (-1,1):
            a=p+axis*(length/2-.01)*sign
            self.rod('Square washer bearing',a,a+axis*.004*sign,.029,n=4)
            self.rod('Square nut',a+axis*.004*sign,a+axis*.017*sign,.0155,n=4)
    def finish(self):
        bpy.ops.object.select_all(action='DESELECT')
        for ob in self.objects:
            G.apply(ob);ob.select_set(True)
        if self.objects:
            bpy.context.view_layer.objects.active=self.objects[0];bpy.ops.object.join()
            ob=self.objects[0];ob.name=self.root.name+'__Mesh'
            # Origins and all transforms on the consolidated assembly are applied.
            bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
            self.objects=[ob]
        return self.root


def pin(a,x,y,z,polymer=False):
    a.rod('Forged insulator pin',(x,y,z-.19),(x,y,z-.025),.0127,n=8)
    if polymer:
        profile=[(z-.23,.016)]
        for k in range(5):
            zz=z-.2+k*.037
            profile.extend([(zz,.022),(zz+.006,.054),(zz+.012,.022)])
        profile.extend([(z-.015,.029),(z,.024)])
        a.lathe('Polymer line post sheds',profile,(x,y),'Polymer',10)
    else:
        # ANSI 55-3: 4.75-inch maximum shed, 3.75-inch high glazed porcelain.
        profile=[(z-.09525,.030),(z-.090,.055),(z-.080,.060325),(z-.071,.058),
                 (z-.061,.027),(z-.045,.042),(z-.031,.041),(z-.023,.028),
                 (z-.012,.038),(z-.004,.037),(z,.025)]
        a.lathe('ANSI 55-3 porcelain pin',profile,(x,y),n=12)
    # Tie wire in the neck; conductor bears in the upper saddle.
    pts=[(x+.035*math.cos(t),y+.035*math.sin(t),z-.021) for t in [i*math.tau/12 for i in range(13)]]
    a.tube('Neck tie',pts,.0016,'Aluminum',4)


def crossarm(a,s,z=None):
    z=s['primary']-.38 if z is None else z
    width=s['arm_ft']*FT
    a.box('Solid sawn crossarm',(0,.205,z),(width,.09525,.12065),'Wood',.003,'crossarm')
    a.box('Steel gain bearing',(0,.133,z),(.11,.055,.15),'Steel',.002,'crossarm')
    a.bolt((0,.08,z),length=.45)
    # Flat 1/4 x 1-1/4 inch braces, not cylindrical wire.
    for sign in (-1,1):
        p=Vector((sign*.78,.208,z-.055));q=Vector((sign*.035,.15,z-.69))
        ob=a.box('Flat crossarm brace',(p+q)/2,(.03175,.00635,(p-q).length),'Steel',0,'crossarm')
        ob.rotation_euler=(p-q).to_track_quat('Z','Y').to_euler()
        a.bolt((sign*.78,.205,z-.025),length=.15)
    a.bolt((0,0,z-.69),length=.34)
    return z


def strain(a,p,direction,component='deadend'):
    p=Vector(p);v=Vector(direction).normalized()
    a.rod('Deadend forged eye',p-v*.10,p,.017,n=8,component=component)
    for j in range(3):
        c=p+v*(.045+j*.055)
        a.rod('Deadend porcelain disk',c-v*.013,c+v*.013,.056,'Porcelain',12,component)
    end=p+v*.23
    a.rod('Strain clamp',p+v*.18,end,.013,'Aluminum',6,component)
    return tuple(end)


def wood(a,s):
    rng=random.Random(s['seed']);n=20;h=s['height'];ground_c=s['circumference_6ft_in']*IN
    # The ANSI reference station is 6 ft from butt, .5 ft below grade on 45s.
    zr=(6-s['embed_ft'])*FT;r0=ground_c/(2*n*math.sin(math.pi/n));rt=21*IN/(2*n*math.sin(math.pi/n))
    radius=lambda z:r0+(rt-r0)*(z-zr)/(h-zr)
    loops=[]
    for z in [-.12,0,.2,.6,1.2,2,3,4,5,6,7,8,h]:
        if z>h:continue
        loops.append([(radius(z)*math.cos(i*math.tau/n),radius(z)*math.sin(i*math.tau/n),z) for i in range(n)])
    a.add(G.smooth(G.loft('Treated class 4 southern pine shaft',loops,M['Wood'])), 'wood')
    # Bare cut-end is a real cap face, not a second full disk.
    pole=a.objects[-1];pole.data.materials.append(M['Endgrain'])
    pole.data.polygons[-1].material_index=1
    for j in range(12):
        t=rng.uniform(0,math.tau);z=rng.uniform(.08,h-.6);ln=rng.uniform(.22,1.1);w=rng.uniform(.0015,.004)
        vs=[]
        for zz,ww in [(z,0),(z+.14*ln,w),(z+.75*ln,w*.65),(min(h-.01,z+ln),0)]:
            r=radius(zz)+.00025
            vs.extend([(r*math.cos(t+sg*ww/r),r*math.sin(t+sg*ww/r),zz) for sg in ((0,) if ww==0 else (-1,1))])
        a.add(G.mesh('Drying check',vs,[(0,1,2),(1,3,4,2),(3,5,4)],M['Recess']),'checks')
    # Quarter-round wood ground-wire molding protects #6 copper to 8 ft.
    a.rod('Continuous copper ground',(.02,-radius(0)-.012,-.1),(.02,-radius(h-.45)-.012,h-.45),.00206,'Aluminum',6,'grounding')
    p=Vector((.02,-radius(-.1)-.010,-.1));q=Vector((.02,-radius(2.5)-.010,2.5))
    mold=a.box('Ground wire protective molding',(p+q)/2,(.038,.026,(q-p).length),'Wood',.009,'grounding')
    mold.rotation_euler=(q-p).to_track_quat('Z','Y').to_euler()
    for z in (.25,.9,1.7,2.45):a.rod('Molding nail',(.02,-radius(z)-.038,z),(.02,-radius(z)-.044,z),.0022,n=6,component='grounding')
    # Old staple population stays small; scars and brand will bake later.
    for j in range(7):
        z=.8+j*.19;x=rng.uniform(-.05,.05);y=-math.sqrt(radius(z)**2-x*x)-.002
        a.tube('Old fence/sign staple',[(x-.008,y,z-.01),(x-.008,y-.006,z),(x+.008,y-.006,z),(x+.008,y,z-.01)],.0012,'Steel',4,'staples')
    a.box('Utility number tag',(0,-radius(1.8)-.004,1.8),(.065,.003,.22),'Polymer',0,'markings')
    # Simple printed original fictional numbers and brand, deferred final relief.
    from markings import label
    a.add(label('Number tag',f'RV\n{s["seed"]:04d}',(0,-radius(1.8)-.006,1.8),.055,.19),'markings')
    a.add(label('Birth brand',f'RILL TIMBER\nSP  CCA  1992\n4 / {s["length_ft"]}',(0,-radius(1.05)-.002,1.05),.12,.15),'markings')
    if s['seed']%3==0 and s['kind'] in ('riser','transformer'):
        for j in range(2):
            pts=[]
            for k in range(9):
                z=.02+k*.075;t=j*1.4+k*.16;r=radius(z)+.005
                pts.append((r*math.cos(t),r*math.sin(t),z))
            a.tube('Sparse ground-rooted vine',pts,.0015,'Vine',4,'vine')
            for k in (2,4,6,8):
                p=Vector(pts[k]);out=Vector((p.x,p.y,.2)).normalized();across=out.cross(Vector((0,0,1))).normalized()
                v=[p,p+out*.045+across*.015,p+out*.065,p+out*.045-across*.015]
                a.add(G.mesh('Small vine leaf',v,[(0,1,2,3)],M['Vine']),'vine')
    a.root['pole_spec']=__import__('json').dumps(s)


def communication(a,s):
    z=s['communication'];x=-.24
    a.bolt((-.02,0,z),axis=(1,0,0),length=.39)
    a.rod('Messenger suspension shoe',(-.17,0,z),(-.28,0,z),.016,n=8)
    a.socket('CommStrand',(x,0,z),diameter=.00635)
    a.socket('LashedFiber',(x-.014,0,z-.038),diameter=.020)
    a.socket('Telephone',(x,0,z-.36),diameter=.028)
    a.box('Splice hanger',(x,0,z-.17),(.025,.38,.035),'Steel')
    a.rod('Sealed inline splice case',(x-.025,-.34,z-.21),(x-.025,.34,z-.21),.072,'Cable',12,'communications')
    for yy in (-.24,.24):a.rod('Case circumferential clamp',(x-.025,yy-.012,z-.21),(x-.025,yy+.012,z-.21),.077,'Steel',12,'communications')
    for sign in (-1,1):
        pts=G.bezier((x-.014,sign*.45,z-.038),(x-.18,sign*.85,z-.5),(x-.20,sign*.35,z-.84),(x-.025,sign*.25,z-.21),18)
        a.tube('Fiber slack loop',pts,.010,'Cable',6,'communications')
    a.socket('CommDrop',(x,-.05,z-.39),diameter=.006)


def transformer(a,s,index=0):
    # Conventional 50 kVA envelope: Meta Power Solutions' published 20-inch
    # tank diameter / 42-inch overall height; original details and nameplate.
    x=(index-1)*.65 if s.get('bank',1)>1 else 0
    y=-.48 if s.get('bank',1)==1 else -.52
    bottom=s['neutral']+.23;top=bottom+.8128
    bank=s.get('bank',1)>1;a.bank_lod=bank
    for z in (bottom+.12,top-.10):
        a.box('Transformer pole hanger',(x,-.19,z),(.15,.10,.10),'Steel',.003,'transformer')
        a.box('Formed tank lug',(x,-.285,z),(.14,.13,.06),'Steel',.003,'transformer')
        a.bolt((x,-.04,z),length=.44)
    a.lathe('Rolled steel transformer tank',[(bottom,.229),(bottom+.018,.254),(top-.02,.254),(top,.25)],(x,y),'Paint',24,'transformer')
    a.lathe('Pressed lid and rolled clamp',[(top-.017,.258),(top+.007,.263),(top+.018,.246),(top+.025,.21)],(x,y),'Paint',24,'transformer')
    # Two rolled lifting eyes, a pressure-relief plug and a low drain boss.
    for sign in (-1,1):
        a.tube('Tank lifting eye',[(x+sign*.20,y-.035,top-.13),(x+sign*.29,y-.035,top-.08),(x+sign*.29,y+.035,top-.08),(x+sign*.20,y+.035,top-.13)],.011,'Steel',6,'transformer')
    a.rod('Pressure relief',(x+.24,y,top-.13),(x+.29,y,top-.13),.018,'Cable',8,'transformer')
    a.rod('Tank drain',(x,y-.24,bottom+.08),(x,y-.28,bottom+.08),.018,'Steel',8,'transformer')
    # One high-voltage bushing for grounded-wye; grounded tank return.
    bz=top+.254
    a.lathe('High voltage bushing',[(top,.032),(top+.04,.030),(top+.05,.055),(top+.065,.025),
       (top+.09,.050),(top+.105,.023),(top+.13,.044),(top+.145,.022),(bz,.016)],(x,y),'Porcelain',12,'transformer')
    for j in range(3):
        xx=x+(j-1)*.12;zz=top-.23
        a.rod('Low voltage porcelain bushing',(xx,y-.225,zz),(xx,y-.31,zz),.029,'Porcelain',10,'transformer')
        a.rod('LV spade terminal',(xx,y-.30,zz),(xx,y-.35,zz),.012,'Aluminum',6,'transformer')
        rack_offset=(index-1)*.65 if bank else 0
        a.tube('Secondary lead to service rack',G.bezier((xx,y-.35,zz),(xx,y-.65,zz-.28),(.30+rack_offset+j*.04,-.55,s['neutral']-.22),(.28+rack_offset,-.18,s['neutral']+(j-1)*.055),12),.008,'Cable',6,'transformer')
    # Cutout and arrester each stand on a real standoff on the side of pole.
    cx=x+.42;cy=-.14;cz=top+.32
    if bank:
        a.rod('Bank hardware hanger upright',(x,-.19,top-.11),(x,-.19,top+.25),.017,'Steel',6,'transformer')
    else:
        a.box('Cutout pole bearing pad',(0,-.12,cz-.12),(.11,.085,.13),'Steel',0,'transformer')
        a.bolt((0,0,cz-.12),length=.4)
    a.box('Cutout bracket',(x+.20,cy,cz-.12),(.56,.045,.048),'Steel',0,'transformer')
    a.rod('Cutout porcelain support',(cx,cy,cz-.25),(cx,cy,cz+.16),.035,'Porcelain',12,'transformer')
    for k in range(5):a.rod('Cutout rain shed',(cx,cy,cz-.19+k*.066),(cx,cy,cz-.177+k*.066),.061,'Porcelain',10,'transformer')
    a.rod('Dropout fuse tube',(cx,cy-.16,cz-.21),(cx,cy-.19,cz+.18),.015,'Cable',8,'transformer')
    for dz in (-.21,.18):a.rod('Cutout contact jaw',(cx,cy,cz+dz),(cx,cy-.19,cz+dz),.012,'Steel',6,'transformer')
    ax=x-.36
    a.box('Arrester standoff',(x-.17,cy,top+.16),(.46,.04,.04),'Steel',0,'transformer')
    if not bank:
        a.box('Arrester pole bearing pad',(0,-.12,top+.16),(.11,.085,.10),'Steel',0,'transformer')
    a.rod('MOV arrester continuous core',(ax,cy,top+.12),(ax,cy,top+.34),.016,'Polymer',8,'transformer')
    for k in range(5):
        z=top+.12+k*.042
        a.lathe('MOV arrester polymer shed',[(z,.016),(z+.006,.039),(z+.012,.016)],(ax,cy),'Polymer',10,'transformer')
    high=a.sockets['Primary_'+(('B','A','C')[index] if bank else 'A')].location
    a.tube('Primary jumper to fuse',G.bezier(high,(high.x,-.22,high.z-.12),(cx,cy-.1,cz+.36),(cx,cy-.18,cz+.18),14),.0041,'Aluminum',6,'transformer')
    a.tube('Fuse to HV bushing',G.bezier((cx,cy-.18,cz-.21),(cx,-.6,cz-.4),(x,y-.2,bz+.12),(x,y,bz),14),.0041,'Cable',6,'transformer')
    a.tube('Bushing arrester connection',G.bezier((x,y,bz),(x-.2,y,bz+.1),(ax,cy,top+.5),(ax,cy,top+.32),10),.003,'Aluminum',6,'transformer')
    a.tube('Tank bonding lead',[(ax,cy,top+.12),(ax,-.22,bottom+.12),(.02,-.14,bottom)],.00206,'Aluminum',6,'transformer')
    from markings import label
    a.add(label('Transformer rating','RILL ELECTRIC\n50 kVA',(x,y-.256,bottom+.36),.18,.15),'transformer')
    a.bank_lod=False


def pole(name,s):
    a=Assembly(name);wood(a,s);h=s['height'];primary=s['primary'];neutral=s['neutral']
    end=s['kind'] in ('deadend','riser');direction=(0,1 if s['kind']=='deadend' else -1,0)
    if s['framing']=='crossarm':
        armz=crossarm(a,s)
        a.socket('CrossarmMount',(0,0,armz),'crossarm_mount')
        coords=[(-s['arm_ft']*FT*.40,.205,armz+.24),(0,-.10,primary),(s['arm_ft']*FT*.40,.205,armz+.24)] if s['phases']==3 else [(0,-.1,primary)]
    else:
        coords=[(-.51,0,primary-.82),(0,-.10,primary),(.51,0,primary-1.64)] if s['phases']==3 else [(0,-.10,primary)]
        for x,y,z in coords:
            a.box('Armless steel pole bracket',(x/2,0,z-.20),(max(.12,abs(x)),.055,.065),'Steel',.002)
            a.bolt((0,0,z-.20),length=.34)
    for j,p in enumerate(coords):
        # Give A the top center position in both framing styles.
        phase=('B','A','C')[j] if len(coords)==3 else 'A'
        if end:
            # Deadend eyes bear directly on the arm / pole, not in the air
            # at the tangent pin's elevated conductor height.
            if abs(p[0])>.2:p=(p[0],p[1],armz if s['framing']=='crossarm' else p[2]-.20)
            else:p=(p[0],direction[1]*.15,p[2])
            p=strain(a,p,direction)
        else:pin(a,*p,polymer=s['framing']=='armless' and s['phases']==3)
        a.socket('Primary_'+phase,p,diameter=.0101)
    a.box('Secondary clevis pole bracket',(.16,-.02,neutral),(.17,.06,.065),'Steel',.002)
    a.box('Secondary vertical rack',(.25,0,neutral),(.035,.04,.22),'Steel',0)
    # Two insulated hots and a bare neutral terminate at a porcelain service rack.
    for j,zz in enumerate((neutral-.06,neutral,neutral+.06)):
        a.rod('Secondary spool',(.25,0,zz-.023),(.25,0,zz+.023),.025,'Porcelain',10)
    a.socket('Neutral',(.275,0,neutral),diameter=.008)
    a.rod('Service messenger strain clamp',(.28,-.02,neutral),(.28,-.18,neutral),.009,'Aluminum',6)
    a.socket('Service',(.28,-.18,neutral),diameter=.022)
    a.bolt((0,0,h-.17),axis=(1,0,0),length=.25)
    if s['comm']:communication(a,s)
    if s['kind']=='transformer':
        a.socket('TransformerMount',(0,0,neutral+.23),'transformer_mount')
        if s.get('bank',1)>1:
            for zz in (neutral+.35,neutral+.23+.7128):
                a.box('Three-can bank steel support rail',(0,-.19,zz),(1.6,.09,.09),'Steel',.002,'bank_rack')
                a.bolt((0,0,zz),length=.45)
            for sign in (-1,1):a.rod('Bank rail knee brace',(sign*.62,-.18,neutral+.35),(0,-.1,neutral-.20),.02,'Steel',8,'bank_rack')
            # Three independent 120/240 V secondary circuits; the primary
            # phases are distinct. Never join out-of-phase secondary hots.
            a.box('Independent secondary rack rail',(.25,-.02,neutral),(1.58,.06,.065),'Steel',0,'bank_rack')
            for off,phase in ((-.65,'B'),(.65,'C')):
                a.box('Outer bank secondary vertical rack',(.25+off,0,neutral),(.035,.04,.22),'Steel',0,'bank_rack')
                a.rod('Outer bank rack support',(.25+off,-.02,neutral),(off,-.18,neutral+.35),.015,'Steel',6,'bank_rack')
                for dz in (-.06,0,.06):a.rod('Outer bank secondary spool',(.25+off,0,neutral+dz-.023),(.25+off,0,neutral+dz+.023),.025,'Porcelain',8,'bank_rack')
                a.rod('Outer bank messenger clamp',(.28+off,-.02,neutral),(.28+off,-.18,neutral),.009,'Aluminum',6,'bank_rack')
                a.socket('Service_'+phase,(.28+off,-.18,neutral),'service_triplex',.022)
            a.socket('Service_A',(.28,-.18,neutral),'service_triplex',.022)
            a.root['bank_secondary']='three independent 120/240V circuits, not paralleled; central A circuit supplies this street'
        for i in range(s.get('bank',1)):transformer(a,s,i)
    if s['kind']=='riser':
        # Two straps per lower length; long-radius sweep enters underground.
        a.tube('Rigid primary riser conduit',G.bezier((0,.8,-.12),(0,.23,-.12),(0,.23,.3),(0,.23,.8),10)+[(0,.23,neutral+.62)],.0445,'Steel',10,'riser')
        for z in (.45,2,3.6,5.2,6.8):
            a.box('Conduit saddle standoff',(0,.17,z),(.13,.12,.035),'Steel',0,'riser')
        a.box('Riser U guard',(0,.30,1.1),(.13,.04,2.2),'Guard',.012,'riser')
        keys=['Primary_A'] if s['phases']==1 else ['Primary_B','Primary_A','Primary_C']
        a.box('Riser pothead support bar',(0,.23,neutral+.67),(.94,.055,.04),'Steel',0,'riser')
        for j,key in enumerate(keys):
            x=(j-(len(keys)-1)/2)*.38
            a.tube('Conduit breakout to sealed pothead',G.bezier((0,.23,neutral+.62),(x,.23,neutral+.53),(x,.23,neutral+.60),(x,.23,neutral+.70),6),.014,'Cable',6,'riser')
            profile=[(neutral+.67,.024)]
            for k in range(3):
                zz=neutral+.70+k*.055;profile.extend([(zz,.021),(zz+.01,.0475),(zz+.02,.020)])
            profile.append((neutral+.89,.014))
            a.lathe('Sealed primary cable termination',profile,(x,.23),'Polymer',6 if len(keys)==3 else 8,'riser')
            a.tube('Riser insulated phase lead',G.bezier((x,.23,neutral+.89),(x,.45,neutral+1.2),(a.sockets[key].location.x,.4,a.sockets[key].location.z-.10),a.sockets[key].location,10),.010,'Cable',6,'riser')
            a.socket('Riser_'+key,(x,.23,neutral+.89),'riser_terminal',.020)
        a.socket('RiserUnderground',(0,.8,-.12),'underground')
    a.socket('LightBracket',(.16,0,neutral+.08),'street_light').rotation_euler.z=math.pi/2
    if s.get('light'):
        z=neutral+.08
        a.box('Wood pole light mounting plate',(.16,0,z),(.04,.14,.36),'Steel',0,'light_bracket')
        for zz in (z-.13,z+.13):a.bolt((0,0,zz),axis=(1,0,0),length=.38)
        pts=G.bezier((.18,0,z-.10),(.9,0,z+.4),(1.65,0,z+.46),(2.0,0,z+.46),10)
        a.tube('Six foot luminaire bracket',pts,.03015,'Steel',8,'light_bracket')
        a.rod('Arm triangulating support',(.18,0,z-.6),(1.1,0,z+.27),.014,'Steel',8,'light_bracket')
        a.socket('LightHead',(2.0,0,z+.46),'street_light_head').rotation_euler.z=math.pi/2
    a.socket('GuyUpper',(0,.04,h-.76),'guy')
    a.root['kind']=s['kind'];a.finish();return a


def guy(name,start,anchor):
    a=Assembly(name);p,q=Vector(start),Vector(anchor);v=(q-p).normalized();egg=p.lerp(q,.38)
    a.rod('7 strand guy upper',p,egg-v*.09,.00476,'Steel',6,'guy')
    a.rod('Guy strain egg',egg-v*.09,egg+v*.09,.035,'Porcelain',10,'guy')
    a.rod('7 strand guy lower',egg+v*.09,q,.00476,'Steel',6,'guy')
    end=q-v*min(2.44,(q-p).length*.3)
    a.rod('Faded 8 foot yellow guy guard',q,end,.026,'Guard',10,'guard')
    a.rod('5/8 inch anchor eye rod',q-v*.18,q+v*.3,.00794,'Steel',8,'anchor')
    a.rod('Anchor forged eye',q-v*.22,q-v*.15,.025,'Steel',8,'anchor')
    for t in (.10,.23):
        c=q-v*(2.44+t)
        a.rod('Guy preform grip',c-v*.06,c+v*.06,.009,'Steel',6,'guy')
    a.socket('Pole',p,'guy');a.socket('Anchor',q,'ground_anchor');a.finish();return a


def conductor(name,start,end,sag,diameter,mat='Aluminum',tolerance=.008):
    pts,report=sample(start,end,sag,tolerance)
    ob=G.tube(name,pts,diameter/2,M[mat],4,caps=False)
    ob['asset_set']='Utility';ob['span']=True;ob['diameter_m']=diameter;ob['sag_m']=sag
    report.update(name=name,start=list(start),end=list(end),diameter_m=diameter,points=pts,
                  triangles=8*(len(pts)-1),material=mat,tolerance_m=tolerance)
    return ob,report
