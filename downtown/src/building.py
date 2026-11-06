"""Original load-bearing brick commercial shells, 1880–1930 with later work.

Geometry carries construction at this gate. Fine coursing, wear and ornament
are intentionally reserved for shared tile/trim normals in the next gate.
"""
import math
import random
import bpy
from mathutils import Vector
from geometry import Batch, frame, pivot, wall
import ornament as O

STONE=(.47,.42,.32);IRON=(.035,.048,.041);DARK=(.018,.022,.020);CREAM=(.57,.53,.41)


class Building:
    def __init__(self,p,mats,layout):
        self.p=p;self.mats=mats;self.layout=layout;self.root=pivot(p['id'],(0,0,0),static_root=True,building=True)
        self.root['plan']=__import__('json').dumps(p,sort_keys=True);self.batches=[];self.doors=[];self.openings=[]
        self.rng=random.Random(p['seed']);w,d=p['width'],p['depth'];c=p['chamfer']
        # Counterclockwise footprint: the corner entry replaces the outer angle.
        self.poly=[(-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)]
        if p['corner']=='left':self.poly=[(-w/2+c,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2),(-w/2,-d/2+c)]
        if p['corner']=='right':self.poly=[(-w/2,-d/2),(w/2-c,-d/2),(w/2,-d/2+c),(w/2,d/2),(-w/2,d/2)]
        self.p['footprint']=self.poly
        for side,x in (('Left',-w/2),('Right',w/2)):
            self.socket('Party'+side,(x,0,0),'party_wall_line')
        self.socket('FrontLine',(0,-d/2,0),'sidewalk_building_line')
        self.socket('RearAlley',(0,d/2,0),'alley')
    def socket(self,name,p,kind,**props):return pivot(self.p['id']+'__Socket_'+name,p,self.root,socket_kind=kind,**props)
    def batch(self,name,xf=None,parent=None):
        b=Batch(self.p['id']+'__'+name,parent or self.root,self.mats,xf);self.batches.append(b);return b
    def graphic(self,b,key,x,y,z,w,h):
        b.quad([(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],self.layout[key])
    def trimframe(self,b,x,y,z,w,h,color=CREAM,bar=.06,depth=.09):
        for xx in (x-w/2+bar/2,x+w/2-bar/2):b.box((xx,y,z),(bar,depth,h),'Finish',color)
        for zz in (z-h/2+bar/2,z+h/2-bar/2):b.box((x,y,zz),(w-2*bar,depth,bar),'Finish',color)
    def door(self,name,xf,x,y,z,w=1.0,h=2.38,color=IRON,glazed=True):
        origin=xf((x-w/2+.004,y,z));o=pivot(self.p['id']+'__'+name,origin,self.root,pivot_axis='Z',range_degrees=[0,100])
        # Local open-frame geometry is stored in hinge space, including handles.
        b=self.batch(name,lambda v:xf((v[0]+x-w/2,y+v[1],z+v[2]))-origin,parent=o)
        self.trimframe(b,w/2,0,h/2,w-.008,h,color,.075,.045)
        if glazed:
            b.box((w/2,.002,h*.56),(w-.16,.004,h*.68),'Glass')
            b.box((w/2,0,.23),(w-.15,.045,.37),'Finish',color)
            b.box((w/2,0,.64),(w-.15,.045,.065),'Finish',color)
        else:b.box((w/2,0,h/2),(w-.15,.042,h-.13),'Finish',color)
        b.tube([(w-.16,-.05,.94),(w-.16,-.08,.94),(w-.16,-.08,1.28),(w-.16,-.05,1.28)],.012,color=(.38,.34,.23))
        for zz in (.22,1.12,2.12):b.tube([(.004,0,zz),(.004,0,zz+.085)],.012,color=IRON)
        self.doors.append(o)
        self.socket(name+'Threshold',xf((x,y,z)),'threshold',nominal_leaf_width_m=w)
        return o
    def window(self,b,o,index=0,rear=False):
        x=(o['x0']+o['x1'])/2;w=o['x1']-o['x0'];lo,hi=o['z0'],o['z1'];h=hi-lo;y=.105 if self.p['style']=='italianate' and not rear else .19
        tint=CREAM if self.p['style']=='italianate' else (.18,.20,.17)
        if rear:tint=((.29,.28,.23),(.16,.19,.17),(.36,.34,.29))[(index+self.p['index'])%3]
        # Recessed box frame; two overlapping sash planes and a meeting rail.
        filled=index==0 and self.p['index']==4 and not rear
        if filled:
            rise=o.get('rise',0)
            poly=[(x-w/2,.065,lo),(x+w/2,.065,lo),(x+w/2,.065,hi)]+[(x+w/2-w*j/12,.065,hi+rise*4*j/12*(1-j/12)) for j in range(1,13)]
            b.prism(poly,(0,.28,0),'Masonry',tuple(c*.73 for c in self.p['brick']))
        else:
            self.trimframe(b,x,y,(lo+hi)/2,w-.08,h-.06,tint,.068,.12)
            for k in range(2):
                zh=lo+.07+(h-.14)*(k+.5)/2;yy=y+.018 if k==0 else y+.052
                self.trimframe(b,x,yy,zh,w-.19,(h-.14)/2+.025,tint,.041,.037)
                b.box((x,yy+.013,zh),(w-.28,.004,(h-.14)/2-.060),'Glass')
                if self.p['style']=='italianate' and index%3==0:b.box((x,yy-.013,zh),(.022,.026,(h-.14)/2-.065),'Finish',tint)
        O.sill(b,x,w,lo,STONE)
        rise=o.get('rise',0)
        if self.p['style']=='italianate' and not rear:
            O.hood(b,x,w,hi,rise,CREAM)
        elif rise:
            # Wedge voussoirs; the UV follows the arch's rowlock axis.
            n=13
            for j in range(n):
                aa=j/n+.006;bb=(j+1)/n-.006
                xa=o['x0']-.07+(w+.14)*aa;xb=o['x0']-.07+(w+.14)*bb
                za=hi+rise*4*aa*(1-aa);zb=hi+rise*4*bb*(1-bb)
                color=STONE if self.p['style']=='romanesque' else tuple(c*.78 for c in self.p['brick'])
                b.prism([(xa,-.07,za),(xb,-.07,zb),(xb,-.07,zb+.23),(xa,-.07,za+.23)],(0,.20,0),'Mineral' if self.p['style']=='romanesque' else 'Masonry',color)
        else:
            # Tooled ashlar lintel: chamfered bearing faces and drafted edge.
            b.prism([(x-w/2-.14,-.105,hi+.025),(x+w/2+.14,-.105,hi+.025),
                (x+w/2+.14,-.105,hi+.18),(x+w/2+.10,-.105,hi+.23),
                (x-w/2-.10,-.105,hi+.23),(x-w/2-.14,-.105,hi+.18)],(0,.29,0),'Mineral',STONE)
            if not rear:O.molding(b,x-w/2-.17,x+w/2+.17,hi+.225,.15,.065,'Mineral',STONE)
        if rise and not filled:
            b.prism([(o['x0']+.04,y+.04,hi),(o['x1']-.04,y+.04,hi)]+[(o['x1']-.04-(w-.08)*j/12,y+.04,hi+rise*4*(j/12)*(1-j/12)) for j in range(1,12)],(0,.004,0),'Glass')
        if filled:return
        if rear and (index+self.p['index'])%3==0:
            for zz in (lo+h/3,lo+2*h/3):b.box((x,y-.023,zz),(w-.16,.028,.025),'Finish',tint)
            b.box((x,y-.023,(lo+hi)/2),(.026,.028,h-.14),'Finish',tint)
        # Shallow room with individual blind/curtain depth, not painted glass.
        b.box((x,1.02,(lo+hi)/2),(w+.18,.035,h+.25),'Interior',(.028,.030,.025) if (index+self.p['index'])%3 else (.55,.32,.11))
        b.box((x,.65,lo-.05),(w,.80,.035),'Finish',(.14,.11,.07))
        if index%3==0:
            drop=h*(.28+.11*(index%4));b.box((x,.34,hi-drop/2),(w-.19,.025,drop),'Finish',(.40,.37,.28))
            for zz in range(max(1,int(drop/.095))):b.box((x,.316,hi-.03-zz*.095),(w-.2,.035,.018),'Finish',(.47,.43,.33))
        else:
            for s in (-1,1):
                for j in range(3):b.box((x+s*(w*.35+j*.025),.35+j%2*.03,(lo+hi)/2),(w*.12,.035,h-.12),'Finish',(.37,.31,.23) if index%2 else (.52,.48,.39))
        if index==1 and not rear:
            b.box((x,.04,lo+.19),(w*.78,.60,.38),'Finish',(.34,.34,.30))
            for j in range(8):b.box((x-w*.30+j*w*.085,-.267,lo+.20),(.012,.015,.25),'Finish',(.12,.13,.12))
            for s in (-1,1):b.beam((x+s*w*.29,.19,lo-.08),(x+s*w*.29,-.23,lo-.02),.022,color=IRON)
    def upper_openings(self,L,rear=False,spacing=None):
        p=self.p;out=[];n=max(2,round((L-.6)/1.95)) if not rear else max(2,round((L-.6)/2.6))
        if spacing:n=max(3,min(8,round(L/spacing)))
        for level in range(1,p['stories']):
            base=p['floor_first']+(level-1)*p['upper'];h=p.get('window_height',1.96) if not rear else 1.63
            for j in range(n):
                x=(j+.5)*L/n;w=min(1.02,L/n-.60)
                out.append(dict(x0=x-w/2,x1=x+w/2,z0=base+.65,z1=base+.65+h,rise=.22 if p['style'] in ('italianate','romanesque') and not rear else 0))
        return out
    def storefront(self,b,L,xf):
        p=self.p;stair=1.22 if p['stories']>1 else .22;s0=.36+stair;s1=L-.36;sw=s1-s0
        h=p['floor_first'];head=h-1.42;trans=h-1.05;col=IRON if p['storefront']=='iron' else (.26,.27,.24) if p['storefront']=='aluminum' else (.13,.19,.15)
        b.box((L/2,.14,h-.38),(L-.1,.47,.65),'Finish',col)
        self.graphic(b,p['tenant'],(s0+s1)/2,-.105,h-.38,sw-.15,.47)
        # Slender iron/wood piers transmit the girder load to masonry plinths.
        for x in (.17,s0-.07,L-.17):
            if p['storefront']=='iron':O.pilaster(b,x,.14,head,col)
            else:
                b.box((x,.14,head/2),(.19,.34,head),'Finish',col)
                b.box((x,.12,.21),(.30,.40,.42),'Mineral',STONE)
                b.box((x,.09,head-.10),(.32,.39,.20),'Finish',col)
        if p['storefront']!='aluminum':
            O.molding(b,.02,L-.02,h-.74,.34,.10,color=col)
            O.molding(b,.02,L-.02,h-.075,.28,.09,color=col)
        # Dedicated stair door, independent of retail tenancy.
        if p['stories']>1:
            self.door('StairDoor',xf,.36+stair/2-.06,.20,.018,stair-.34,2.38,col,False)
            self.trimframe(b,.36+stair/2,.18,2.70,stair-.06,.48,col,.045,.07)
            b.box((.36+stair/2,.23,2.7),(stair-.16,.004,.38),'Glass')
            b.box((.36+stair/2,.22,3.21),(stair,.24,.43),'Finish',col)
        # Angled show-window returns to an inset single entry.
        center=s0+sw*.48;dw=1.02;recess=1.04;mouth=dw+1.04
        left,right=center-mouth/2,center+mouth/2;doorL,doorR=center-dw/2,center+dw/2
        chains=[((s0,.07),(left,.07)),((left,.07),(doorL,recess)),((doorR,recess),(right,.07)),((right,.07),(s1,.07))]
        kick=.51 if p['storefront']!='aluminum' else .32
        for j,(a,c) in enumerate(chains):
            length=math.dist(a,c);local=frame((*a,0),(*c,0));f=lambda v:xf(local(v))
            bb=self.batch('Display'+str(j),f)
            bb.box((length/2,.015,kick/2),(length,.10,kick),'Finish',col)
            # Applied panel field and real retaining rails; transom crosses whole front.
            self.trimframe(bb,length/2,-.042,kick/2,length-.13,kick-.12,col,.025,.022)
            self.trimframe(bb,length/2,.015,(kick+head)/2,length,head-kick,col,.046,.095)
            bb.box((length/2,.038,(kick+head)/2),(length-.10,.004,head-kick-.10),'Glass')
            if p['storefront']=='wood' and length>1.4:bb.box((length/2,-.018,(kick+head)/2),(.045,.055,head-kick),'Finish',col)
        self.door('StoreDoor',xf,center,recess+.07,.018,dw-.12,2.48,col)
        b.box((center,recess,2.80),(dw,.06,.55),'Glass')
        self.trimframe(b,center,recess-.03,2.80,dw,.55,col,.045,.08)
        # Entry terrazzo slab and sill do not bridge the angled glazing outside.
        b.prism([(left,.07,.014),(right,.07,.014),(doorR,recess+.16,.014),(doorL,recess+.16,.014)],(0,0,-.06),'Mineral',(.36,.34,.28))
        b.box((center,recess,.006),(dw,.24,.012),'Mineral',(.42,.42,.38))
        # Transom: old prismatic band or later opaque cover, seeded per building.
        for j in range(max(3,round(sw/.55))):
            n=max(3,round(sw/.55));x=s0+(j+.5)*sw/n
            self.trimframe(b,x,.12,trans,sw/n,.62,col,.035,.10)
            b.box((x,.15,trans),(sw/n-.075,.005,.53),'Finish' if p['transom']=='covered' else 'Glass',col if p['transom']=='covered' else (.80,.88,.83))
            if p['transom']=='prism':
                # Coarse daylight-glass subdivisions; actual prisms belong in normal.
                for k in (-1,0,1):b.box((x+k*.10,.125,trans),(.008,.012,.50),'Finish',(.28,.34,.30))
        b.box((L/2,-.045,h-.02),(L+.10,.64,.13),'Finish',col)
        # Upper girder drip/cornice ledges are seated on the pier capitals.
        b.box((L/2,-.01,head+.035),(L,.38,.12),'Finish',col)
        self.shop_room(b,s0,s1,head,center)
        if p['awning']:self.awning(b,xf,s0,s1,h-1.05)
        if p['index']%2==1:
            x=L-.50;zz=h-.65
            b.beam((x,.13,zz+.35),(x,-1.18,zz+.35),.040,color=IRON)
            b.beam((x,.13,zz+.80),(x,-.94,zz+.35),.027,color=IRON)
            b.box((x,-.88,zz-.07),(.065,.69,.68),'Finish',IRON)
            for yy in (-1.12,-.64):b.beam((x,yy,zz+.27),(x,yy,zz+.36),.025,color=IRON)
            # Projecting sign face is in the YZ plane, same sheet and same quad.
            r=self.layout[p['tenant']]
            b.quad([(x-.036,-1.21,zz-.37),(x-.036,-.55,zz-.37),(x-.036,-.55,zz+.23),(x-.036,-1.21,zz+.23)],r)
            self.socket('BladeBracket',xf((x,.13,zz+.35)),'sign_bracket')
    def shop_room(self,b,a,c,head,entry):
        p=self.p;w=c-a;cx=(a+c)/2;dep=5.5
        b.box((cx,dep,head/2),(w,.08,head),'Finish',(.085,.080,.061))
        b.box((cx,2.7,-.03),(w,5.5,.06),'Mineral',(.20,.17,.12))
        b.box((cx,2.7,head+.10),(w,5.5,.06),'Finish',(.32,.29,.22))
        for side,x in (('left',a+.05),('right',c-.05)):
            if p['corner']!=side:b.box((x,2.8,head/2),(.10,5.5,head),'Finish',(.22,.20,.16))
        if p['tenant']!='vacant':
            for xx in (a+w*.25,a+w*.70):b.box((xx,2.6,head-.045),(.85,.20,.025),'Interior',(.75,.60,.32))
        if p['tenant']=='vacant':
            for s in (-1,1):
                x=entry+s*1.55;b.box((x,.09,1.18),(1.10,.005,1.45),'Finish',(.39,.31,.20))
            return
        if p['tenant']=='diner':
            b.box((c-.7,3.0,1.02),(1.0,3.6,.13),'Mineral',(.41,.34,.23))
            b.box((c-.7,3.0,.50),(.75,3.5,1.0),'Finish',(.18,.10,.06))
            for j in range(4):
                yy=1.6+j*.82;b.tube([(c-1.52,yy,0),(c-1.52,yy,.62)],.037,color=IRON)
                b.box((c-1.52,yy,.65),(.40,.4,.10),'Finish',(.24,.065,.035))
            for j in range(2):
                yy=3.0+j*1.6;b.box((a+1.05,yy,.76),(1.25,.70,.08),'Mineral',(.45,.40,.30))
                b.box((a+1.05,yy,.37),(.10,.10,.74),'Finish',IRON)
                for off in (-.66,.66):b.box((a+1.05,yy+off,.59),(1.20,.32,1.18),'Finish',(.25,.075,.035))
        elif p['tenant']=='barber':
            for j in range(3):
                xx=a+.70+j*(w-1.4)/3
                b.box((xx,2.40,.10),(.50,.50,.20),'Finish',IRON);b.tube([(xx,2.4,.18),(xx,2.4,.61)],.085,color=(.30,.30,.27))
                b.box((xx,2.4,.65),(.61,.61,.15),'Finish',(.15,.040,.025));b.box((xx,2.65,1.0),(.61,.12,.65),'Finish',(.15,.040,.025))
                b.box((xx,5.38,1.8),(.80,.02,1.25),'Glass')
        elif p['tenant'] in ('hardware','pharmacy','antiques'):
            for j in range(3):
                xx=a+.7+j*(w-1.4)/3
                for zz in (.25,.8,1.35,1.90):
                    b.box((xx,2.4,zz),(.78,.55,.035),'Finish',(.25,.18,.10))
                    for k in range(3):b.box((xx-.24+k*.24,2.4,zz+.14),(.15,.22,.25),'Finish',(.23+.06*k,.16+.025*j,.065))
                for off in (-.38,.38):b.box((xx+off,2.4,1.02),(.026,.45,2.04),'Finish',IRON)
        else:b.box((cx,2.9,.65),(w*.66,.80,1.3),'Finish',(.16,.12,.075))
    def awning(self,b,xf,a,c,z):
        span=c-a;panels=max(3,round(span/.92));cloth=(.11,.18,.13) if self.p['index']%2 else (.30,.12,.065)
        for i in range(panels):
            x0=a+span*i/panels;x1=a+span*(i+1)/panels;vs=[]
            for j in range(7):
                t=j/6
                for k in range(7):
                    u=k/6;x=x0+(x1-x0)*u;y=.06-1.65*t
                    zz=z-.48*t-.13*math.sin(math.pi*u)*math.sin(math.pi*t)-.035*math.sin(math.pi*t)
                    vs.append((x,y,zz))
            fs=[(j*7+k,j*7+k+1,(j+1)*7+k+1,(j+1)*7+k) for j in range(6) for k in range(6)]
            b.surface='canvas';b.geom(vs,fs,'Finish',cloth)
            # Weighted scalloped valance: hangs down, with the rolled hem in
            # its silhouette. Stitching and weave are baked into canvas strip.
            vs=[]
            for j in range(9):
                t=j/8;xx=x0+(x1-x0)*t;bottom=z-.72-.065*math.sin(math.pi*t)**2
                vs += [(xx,-1.595,z-.49),(xx,-1.61-.012*math.sin(t*math.tau),bottom)]
            b.geom(vs,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(8)],'Finish',cloth)
            b.surface=None
            # Actual ribs beneath cloth: each bay sags between these supports.
            b.beam((x0,.08,z-.012),(x0,-1.59,z-.492),.020,color=IRON)
        b.beam((c,.08,z-.012),(c,-1.59,z-.492),.020,color=IRON)
        for x in (a,c):b.beam((x,.12,z-.90),(x,-1.59,z-.48),.025,color=IRON)
        b.beam((a,-1.59,z-.49),(c,-1.59,z-.49),.025,color=IRON)
        self.socket('AwningLeft',xf((a,.12,z)),'awning_attachment');self.socket('AwningRight',xf((c,.12,z)),'awning_attachment')
    def cornice(self,b,L):
        p=self.p;top=p['height'];col=CREAM if p['cornice']=='metal' else p['brick']
        if p['cornice']=='metal':O.cornice(b,L,top,col,bool(p['corner']))
        else:
            # Each course steps outward by a fraction of a brick, with a
            # bed-joint shadow. Alternating brick headers form real corbels.
            for j in range(4):
                deep=.13+j*.052
                b.box((L/2,-deep/2+.035,top-.40+j*.087),(L,deep,.070),'Masonry',col)
            if p['cornice']=='corbel':
                n=round(L/.42)
                for j in range(n):
                    x=(j+.5)*L/n
                    for k in range(3):b.box((x,-.024-k*.027,top-.66+k*.083),(.20,.18+k*.054,.070),'Masonry',tuple(c*.90 for c in col))
        if p['cornice']!='metal':
            O.molding(b,-.025,L+.025,top-.04,.24,.10,'Mineral',STONE)
        if p['stories']>1:
            z=min(p['roof']+.20,top-.64)
            b.box((L/2,-.115,z),(1.43,.10,.26),'Mineral',STONE)
            self.graphic(b,'label'+str(4+p['index']%2),L/2,-.171,z,1.20,.20)
    def rear(self,xf,L):
        p=self.p;b=self.batch('RearConstruction',xf);ops=self.upper_openings(L,True)
        ops += [dict(x0=.60,x1=1.68,z0=.012,z1=2.25),dict(x0=L-2.3,x1=L-.65,z0=1.2,z1=2.5)]
        wall(b,L,p['height'],ops+[dict(x0=L-.51,x1=L-.25,z0=p['roof']-.02,z1=p['roof']+.12)],.34,tuple(c*.78 for c in p['brick']))
        for i,o in enumerate(ops[:-2]):self.window(b,o,i,True)
        self.door('ServiceDoor',xf,1.14,.36,.018,1.0,2.20,(.17,.18,.16),False)
        self.trimframe(b,L-1.475,.16,1.85,1.65,1.30,IRON,.07,.10)
        b.box((L-1.475,.20,1.85),(1.50,.004,1.15),'Glass')
        # Real scupper opening and downspout on standoff straps, not in midair.
        x=L-.38;rz=p['roof']
        b.prism([(x-.15,-.01,rz+.12),(x+.15,-.01,rz+.12),(x+.20,-.30,rz-.14),(x-.20,-.30,rz-.14)],(0,.015,0),'Finish',(.24,.25,.22))
        b.tube([(x,-.26,rz-.1),(x,-.28,rz-.4),(x,-.11,rz-.75),(x,-.11,.35),(x,-.26,.13)],.052,color=(.20,.23,.20))
        for z in (.65,3.0,5.8,8.5):
            if z<rz-.5:b.box((x,-.115,z),(.135,.16,.035),'Finish',IRON)
        # Supported electric meter, slack service loop and anchored conduit.
        b.tube([(2.10,-.08,.17),(2.10,-.08,2.15),(2.3,-.08,2.35),(2.4,-.08,2.40),(2.5,-.08,2.20),(2.6,-.08,2.18),(2.63,-.08,2.5)],.018,color=IRON)
        b.box((2.1,-.08,1.5),(.30,.18,.46),'Finish',(.28,.29,.25))
        b.tube([(2.10,-.20,1.54),(2.10,-.25,1.54)],.105,role='Glass',n=12)
        b.box((1.14,-.35,.055),(1.45,.80,.11),'Mineral',(.27,.26,.22))
        if p['fire_escape']:self.fire_escape(b,L)
        self.rear_variation(b,L)
    def rear_variation(self,b,L):
        p=self.p;i=p['index'];col=tuple(c*.78 for c in p['brick'])
        # Vary the alley skyline, not the accepted lot depth or main floor levels.
        if i%3!=1 and not p['fire_escape']:
            x0=.34 if i%2 else L*.54;x1=min(L-.28,x0+L*.39)
            dep=2.1+(i%3)*.65;h=2.60+(i%4)*.23
            # Open service passage / sash in a genuine hollow rear ell.
            for xx in (x0,x1):b.box((xx,-dep/2,h/2),(.18,dep,h),'Masonry',col)
            mid=(x0+x1)/2;opening=.95
            for xa,xc in ((x0,mid-opening/2),(mid+opening/2,x1)):
                b.box(((xa+xc)/2,-dep,h/2),(xc-xa,.18,h),'Masonry',col)
            b.box((mid,-dep,(h+2.1)/2),(opening,.18,h-2.1),'Masonry',col)
            self.trimframe(b,mid,-dep-.11,1.07,1.01,2.14,IRON,.06,.08)
            b.box((mid,-dep-.05,1.05),(.88,.04,2.0),'Finish',(.20,.21,.18))
            b.prism([(x0-.12,-dep-.15,h),(x1+.12,-dep-.15,h),
                     (x1+.12,.02,h+.25),(x0-.12,.02,h+.25)],(0,0,.055),'Roof')
            for xx in (x0-.08,x1+.08):b.beam((xx,-dep-.15,h),(xx,.05,h+.25),.06,.11,color=IRON)
        elif not p['fire_escape']:
            # Timber service porch, no obstruction in the escape stair lane.
            x=L-.95
            b.box((x,-.70,.20),(1.65,1.40,.12),'Finish',(.17,.13,.08))
            for xx in (x-.70,x+.70):
                b.box((xx,-1.25,1.50),(.085,.085,3.0),'Finish',(.18,.17,.12))
            b.prism([(x-.9,.02,3.12),(x+.9,.02,3.12),(x+.9,-1.55,2.98),(x-.9,-1.55,2.98)],(0,0,.045),'Roof')
            for k in range(2):b.box((x,-1.55-k*.25,.10-.05*k),(1.2,.25,.1),'Mineral',STONE)
        # Stair-stepped parapet follows a historic repaired rear wall.
        if i%2:
            for j in range(3):
                xa=j*L/3;xc=(j+1)*L/3;hh=.16*(1+(j+i)%3)
                b.box(((xa+xc)/2,.17,p['height']+hh/2),(xc-xa,.34,hh),'Masonry',col)
                b.box(((xa+xc)/2,.16,p['height']+hh+.035),(xc-xa+.02,.43,.07),'Mineral',STONE)
    def fire_escape(self,b,L):
        p=self.p;span=min(5.60,L-.55);cx=L/2;left=cx-span/2;right=cx+span/2;end=.95;col=(.035,.036,.030)
        levels=[p['floor_first']+i*p['upper']+.02 for i in range(p['stories']-1)]
        def guard(a,c,z):
            distance=math.dist(a,c);n=max(2,round(distance/.15))
            for i in range(n+1):
                t=i/n;x=a[0]+t*(c[0]-a[0]);y=a[1]+t*(c[1]-a[1]);b.box((x,y,z+.53),(.020,.020,1.06),'Finish',col)
            for zz in (.08,1.07):b.beam((*a,z+zz),(*c,z+zz),.035,color=col)
        for level,z in enumerate(levels):
            # Main walk along the rear plus two deeper end landings. The outer
            # stair lane stays OPEN above the flight, preserving headroom.
            rectangles=[(left,right,-1.30,-.10),(left,left+end,-2.45,-1.30),(right-end,right,-2.45,-1.30)]
            for xa,xc,ya,yc in rectangles:
                for yy in (ya,yc):b.box(((xa+xc)/2,yy,z-.065),(xc-xa,.065,.13),'Finish',col)
                for xx in (xa,xc):b.box((xx,(ya+yc)/2,z-.065),(.065,yc-ya,.13),'Finish',col)
                n=max(3,round((xc-xa)/.12))
                for j in range(n):b.box((xa+(j+.5)*(xc-xa)/n,(ya+yc)/2,z-.014),(.025,yc-ya-.05,.028),'Finish',col)
            for xx in (left+.35,right-.35):
                b.box((xx,-.018,z-.90),(.22,.04,1.6),'Finish',col)
                b.beam((xx,-.018,z-1.55),(xx,-2.39,z-.10),.090,.090,color=col)
            guard((left+end,-1.30),(right-end,-1.30),z)
            for xa,xc in ((left,left+end),(right-end,right)):
                guard((xa,-2.45),(xc,-2.45),z)
            for xx in (left,right):guard((xx,-2.45),(xx,-.10),z)
            # Stacked parallel flights end on the lower right landing. The rear
            # walk connects that landing back to the next flight on the left.
            # The first flight alone ends on grade, with real steel feet.
            low=levels[level-1] if level else .18;rise=z-low;steps=math.ceil(rise/.185)
            ax,bx=left+end,right-end;yy=-1.88
            for side in (-.44,.44):b.beam((ax,yy+side,z),(bx,yy+side,low),.070,.14,color=col)
            run=abs(bx-ax)
            for j in range(steps+1):
                t=j/steps;xx=ax+(bx-ax)*t;zz=z-rise*t
                b.box((xx,yy,zz),(run/steps+.025,.88,.035),'Finish',col)
                if j%3==0:
                    for side in (-.44,.44):b.beam((xx,yy+side,zz),(xx,yy+side,zz+1.02),.022,color=col)
            for side in (-.44,.44):
                b.beam((ax,yy+side,z+1.02),(bx,yy+side,low+1.02),.035,color=col)
                if level==0:
                    b.box((bx,yy+side,.0125),(.22,.24,.025),'Finish',col)
                    b.box((bx,yy+side,low/2),(.090,.090,low),'Finish',col)
    def bay_window(self,b,xf,o):
        x=(o['x0']+o['x1'])/2;lo=o['z0'];hi=o['z1'];col=CREAM
        poly=[(x-1.35,.0),(x-.86,-.70),(x+.86,-.70),(x+1.35,.0)]
        for z in (lo-.12,hi+.08):b.prism([(xx,yy,z) for xx,yy in poly],(0,0,.15),'Finish',col)
        for j,(a,c) in enumerate(zip(poly,poly[1:])):
            local=frame((*a,0),(*c,0));bb=self.batch('BaySash'+str(j),lambda v,local=local:xf(local(v)));L=math.dist(a,c)
            self.trimframe(bb,L/2,.02,(lo+hi)/2,L,hi-lo,col,.07,.11)
            bb.box((L/2,-.02,(lo+hi)/2),(L,.06,.055),'Finish',col)
            bb.box((L/2,.04,(lo+hi)/2),(L-.15,.004,hi-lo-.15),'Glass')
            bb.box((L/2,.55,(lo+hi)/2),(L,.03,hi-lo),'Finish',(.04,.038,.03))
        for xx in (x-.9,x+.9):b.beam((xx,.08,lo-.75),(xx,-.65,lo-.11),.16,.20,color=IRON)
        b.prism([(xx,yy,hi+.24+.14*(yy+.70)) for xx,yy in poly],(0,0,.045),'Roof')

    def roof(self):
        p=self.p;w,d=p['width'],p['depth'];b=self.batch('RoofAndServices');z=p['roof']
        # Falling membrane clipped to the real chamfer, with perimeter upstand.
        b.prism([(x,y,z-.03+.008*(-y+d/2)) for x,y in self.poly],(0,0,-.12),'Roof')
        for a,c in zip(self.poly,self.poly[1:]+self.poly[:1]):
            if abs(a[1]-d/2)<1e-6 and abs(c[1]-d/2)<1e-6:
                hole=-w/2+.38
                b.beam((*a,z+.14),(hole+.16,d/2,z+.14),.055,.28,role='Roof',color=(.12,.13,.12))
                b.beam((hole-.16,d/2,z+.14),(*c,z+.14),.055,.28,role='Roof',color=(.12,.13,.12))
            else:b.beam((*a,z+.14),(*c,z+.14),.055,.28,role='Roof',color=(.12,.13,.12))
        equipment=[(-w*.13,d*(.10+.035*(p['index']%4)))]
        if p['stories']==3 or p['index']%3==0:equipment.append((w*.22,-d*.12))
        for x,y in equipment:
            zz=z-.03+.008*(-y+d/2)
            b.box((x,y,zz+.16),(1.25,1.6,.32),'Finish',(.16,.18,.16))
            b.box((x,y,zz+.62),(1.10,1.40,.70),'Finish',(.32,.33,.29))
            for j in range(8):b.box((x-.48+j*.135,y-.708,zz+.62),(.021,.015,.50),'Finish',(.12,.14,.12))
            b.tube([(x-.06,y,zz+.981),(x-.06,y,zz+.99)],.38,color=IRON,n=16)
        for i in range(1+p['index']%2):
            xx=-w*.32+i*w*.62;yy=d*.34;zb=z-.03+.008*(-yy+d/2)
            b.box((xx,yy,zb+.62),(.65,.82,1.24),'Masonry',tuple(c*.65 for c in p['brick']))
            b.box((xx,yy,zb+1.28),(.76,.93,.10),'Mineral',STONE)
            b.box((xx,yy,zb+1.345),(.40,.53,.03),'Finish',DARK)
        zz=z-.03+.008*(d*.15+d/2);sx=-w*.20;sy=-d*.15
        # Hollow curb follows the falling roof at its foot and the inclined
        # glazing at its head; all four rails support the pane continuously.
        for xx in (sx-.70,sx+.60):
            b.prism([(xx,sy-1,zz-.012),(xx,sy+1,zz-.028),(xx,sy+1,zz+.54),(xx,sy-1,zz+.28)],(.10,0,0),'Finish',(.19,.21,.19))
        b.box((sx,sy-.95,zz+.134),(1.20,.10,.292),'Finish',(.19,.21,.19))
        b.box((sx,sy+.95,zz+.256),(1.20,.10,.568),'Finish',(.19,.21,.19))
        b.prism([(-w*.20-.65,-d*.15-1,zz+.28),(-w*.20+.65,-d*.15-1,zz+.28),(-w*.20+.65,-d*.15+1,zz+.54),(-w*.20-.65,-d*.15+1,zz+.54)],(0,0,.012),'Glass')
    def gallery(self):
        p=self.p;w,d=p['width'],p['depth'];b=self.batch('CastIronGallery');col=IRON;z=p['floor_first']-.085
        # Cast columns and a supported deck; component sizes are authored.
        for x in (-w/2+.38,0,w/2-.38):
            b.tube([(x,-d/2-2.55,0),(x,-d/2-2.55,z+.06)],.060,color=col,n=10)
            for zz in (.085,z-.22,z+.13):b.box((x,-d/2-2.55,zz),(.24,.24,.17),'Finish',col)
            b.tube([(x,-d/2-2.55,z+.18),(x,-d/2-2.55,z+2.68)],.043,color=col,n=8)
        b.box((0,-d/2-1.35,z),(w,2.70,.17),'Finish',(.18,.18,.14))
        for zz in (z+.12,z+1.06):b.beam((-w/2,-d/2-2.6,zz),(w/2,-d/2-2.6,zz),.04,color=col)
        for j in range(round(w/.14)):
            x=-w/2+(j+.5)*w/round(w/.14);b.box((x,-d/2-2.6,z+.57),(.018,.018,.91),'Finish',col)
        b.prism([(-w/2,-d/2+.05,z+2.94),(w/2,-d/2+.05,z+2.94),(w/2,-d/2-2.75,z+2.64),(-w/2,-d/2-2.75,z+2.64)],(0,0,.065),'Roof')
        for x in (-w/2+.35,0,w/2-.35):b.beam((x,-d/2+.08,z-.12),(x,-d/2-2.60,z-.12),.12,.15,color=col)
    def build(self):
        p=self.p;w,d=p['width'],p['depth'];verts=self.poly
        for i,(a,c) in enumerate(zip(verts,verts[1:]+verts[:1])):
            xf=frame((*a,0),(*c,0));L=math.dist(a,c);b=self.batch('Wall'+str(i),xf)
            front=abs(a[1]+d/2)<1e-6 and abs(c[1]+d/2)<1e-6
            rear=abs(a[1]-d/2)<1e-6 and abs(c[1]-d/2)<1e-6
            diagonal=abs(a[0]-c[0])>.1 and abs(a[1]-c[1])>.1
            exposed=(p['corner']=='left' and abs(a[0]+w/2)<1e-6 and abs(c[0]+w/2)<1e-6) or (p['corner']=='right' and abs(a[0]-w/2)<1e-6 and abs(c[0]-w/2)<1e-6)
            b.stone_ground=bool(p['corner'] and (front or diagonal or exposed))
            if rear:self.rear(xf,L);continue
            if front:
                ops=self.upper_openings(L)
                bay=None;access=None
                if p['gallery']:
                    access=min(ops,key=lambda o:abs((o['x0']+o['x1'])/2-L/2))
                    access.update(z0=p['floor_first']+.018,z1=p['floor_first']+2.43,rise=0)
                if p['bay_window']:
                    base=p['floor_first']+.45;cx=L*.50
                    ops=[o for o in ops if o['z0']>base+2.5 or abs((o['x0']+o['x1'])/2-cx)>1.55]
                    bay=dict(x0=cx-1.35,x1=cx+1.35,z0=base,z1=base+2.25);ops.append(bay)
                ops.append(dict(x0=.30,x1=L-.30,z0=0,z1=p['floor_first']-.72))
                wall(b,L,p['height'],ops,.44,p['brick']);self.storefront(b,L,xf)
                if p['corner']:
                    O.molding(b,0,L,p['floor_first']-.06,.26,.13,'Mineral',STONE)
                for j,o in enumerate(ops[:-1]):
                    if o is bay:self.bay_window(b,xf,o)
                    elif o is access:
                        self.door('GalleryDoor',xf,(o['x0']+o['x1'])/2,.47,o['z0'],o['x1']-o['x0']-.14,2.4,IRON)
                    else:self.window(b,o,j)
                self.cornice(b,L)
            elif diagonal:
                ops=[dict(x0=.22,x1=L-.22,z0=0,z1=2.85)]+self.upper_openings(L)
                wall(b,L,p['height'],ops,.44,p['brick'])
                self.door('CornerDoor',xf,L/2,.47,.018,L-.56,2.67,IRON)
                b.box((L/2,.80,-.03),(L-.44,1.60,.06),'Mineral',(.36,.34,.28))
                for j,o in enumerate(ops[1:]):self.window(b,o,j)
                for xx in (.11,L-.11):
                    b.box((xx,.13,1.42),(.21,.47,2.84),'Mineral',STONE)
                    O.molding(b,xx-.15,xx+.15,2.72,.31,.16,'Mineral',STONE)
                # Two broad nosings mark the recessed accessible landing, all
                # below the accepted level door threshold.
                for yy,zz in ((-.18,-.045),(-.32,-.095)):
                    b.box((L/2,yy,zz),(L+.12,.30,.09),'Mineral',STONE)
                O.molding(b,-.12,L+.12,2.86,.34,.20,'Mineral',STONE)
                self.graphic(b,'label0' if p['tenant']=='hotel' else 'label1',L/2,-.12,3.24,L-.28,.23)
                if p['cornice']=='metal':O.cornice(b,L,p['height'],CREAM,True)
                else:O.molding(b,-.10,L+.10,p['height']-.20,.40,.20,'Mineral',STONE)
            elif exposed:
                # First 40 ft of return are public facade, back is plainer.
                ops=self.upper_openings(L,True,4.2)
                first=abs(a[1]+d/2)<abs(c[1]+d/2)
                start=1.0 if first else L-10.0
                lower=[dict(x0=start+j*2.35,x1=start+j*2.35+1.70,z0=.55,z1=3.12) for j in range(4)]
                ops+=lower;wall(b,L,p['height'],ops,.34,p['brick'])
                for j,o in enumerate(ops):self.window(b,o,j,True)
                for zz in (p['floor_first']-.04,p['height']-.14):O.molding(b,0,L,zz,.28,.16,'Mineral',STONE)
                if p['corner']=='left':
                    # Keep painted lettering on uninterrupted rear masonry,
                    # clear of the first 40 ft of public-side display windows.
                    gx=min(L*.50,L-14.0);gz=2.70
                    assert not any(gx+3.45>o['x0'] and gx-3.45<o['x1'] and gz+.525>o['z0'] and gz-.525<o['z1']+o.get('rise',0) for o in ops)
                    self.graphic(b,'ghost',gx,-.012,gz,6.9,1.05)
                    # Demolished gable-roof neighbor flashing scar; not a new roof.
                    crest=min(4.35,p['floor_first']-.35)
                    for a,c in (((gx-3.85,-.02,.7),(gx-3.85,-.02,3.2)),((gx-3.85,-.02,3.2),(gx,-.02,crest)),((gx,-.02,crest),(gx+3.85,-.02,3.2)),((gx+3.85,-.02,3.2),(gx+3.85,-.02,.7))):
                        b.beam(a,c,.055,.018,role='Mineral',color=(.24,.22,.18))
            else:
                # Party faces have no windows; half-wall thickness remains inside lot.
                wall(b,L,p['height'],[],.22,tuple(c*.76 for c in p['brick']))
                b.box((L/2,.07,p['height']+.035),(L,.36,.09),'Mineral',STONE)
                side='right' if abs(a[0]-w/2)<1e-6 else 'left'
                neighbor=p.get('neighbor_'+side)
                if neighbor and p['height']-neighbor>1.7:
                    z=(p['height']+neighbor)/2
                    self.graphic(b,'ghost',L*.42,-.012,z,min(9.0,L*.60),1.12)
                    b.beam((.12,-.018,neighbor-.12),(L*.72,-.018,neighbor-.12),.055,.016,role='Mineral',color=(.24,.22,.18))
            self.openings.extend([dict(edge=i,**o) for o in locals().get('ops',[])])
        self.roof()
        if p['gallery']:self.gallery()
        # Tie plates at the actual first floor framing datum.
        b=self.batch('MasonryTiePlates',frame((*verts[0],0),(*verts[1],0)))
        for x in (.70,math.dist(verts[0],verts[1])-.70):
            z=p['floor_first']+.15
            pts=[(x+(.14 if j%2==0 else .055)*math.cos(math.pi/2+j*math.tau/10),-.03,z+(.14 if j%2==0 else .055)*math.sin(math.pi/2+j*math.tau/10)) for j in range(10)]
            b.prism(pts,(0,.030,0),'Finish',IRON)
        obs=[b.finish() for b in self.batches];obs=[o for o in obs if o]
        return self.root,obs,self.doors
