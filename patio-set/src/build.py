"""Larkspur Terrace: original procedural matching patio family, seed 73.

All geometry is authored analytically in meters. References never enter Blender.
The library contains one chair; studio instances prove the four-chair arrangement.
"""
import sys,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
import bpy,bmesh
from mathutils import Vector,Matrix
from kit import model as G,materials as M
from kit.prop import arguments
import finishes

class Family:
    def __init__(self,args):
        self.args=args;self.high=args.quality=='high';self.side=16 if self.high else 8
        self.paint=finishes.powder(args.wear)
        self.sling=finishes.fabric('Sage basket sling / paired yarn / protected hems',args.wear,True)
        self.cloth=finishes.fabric('Sage canopy acrylic / radial seams / exposed fade',args.wear)
        self.binding=finishes.fabric('Sewn sage binding / double stitch',args.wear,binding=True)
        self.folded=finishes.fabric('Furled sage / exposed ridges and protected creases',args.wear,closed=True)
        self.rubber=M.surface('Molded charcoal nylon feet', 'rubber',args.wear,color=(.018,.020,.015),roughness=.8)
        self.metal=M.surface('Satin stainless fasteners','stainless',args.wear,roughness=.48)
        self.root=None;self.aset=None
    def module(self,name,aset):
        self.root=G.pivot(name,(0,0,0));self.root['static_root']=True;self.root['asset_set']=aset;self.aset=aset
        return self.root
    def add(self,ob,parent=None):return G.attach(ob,parent or self.root,self.aset)
    def box(self,name,c,s,mat=None,r=.001):
        return self.add(G.box(name,c,s,mat or self.paint,r,3 if self.high else 1))
    def tube(self,name,points,r,mat=None,sides=None,parent=None):
        return self.add(G.tube(name,points,r,mat or self.paint,sides or self.side),parent)
    def bar(self,name,a,b,w,h=None,parent=None):
        # Closed extrusion; capped ends represent sealed welded/end-plugged stock.
        a,b=Vector(a),Vector(b);height=h or w
        section=G.rounded_rectangle(w,height,min(w,height)*.15,3 if self.high else 1)
        ob=G.profile(name,section,0,(b-a).length,self.paint,axis='Z')
        G.smooth(ob,35);ob.location=a;ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
        return self.add(ob,parent)
    def bolt(self,name,p,d,parent=None,r=.0034):
        for ob in G.fastener(name,p,d,self.metal,r,self.high,kind='socket',washer=self.high):self.add(ob,parent)
    def shell(self,name,vs,fs,mat,thick=.0014,parent=None):
        ob=G.mesh(name,vs,fs,mat)
        if sum(p.normal.z*p.area for p in ob.data.polygons)<0:
            bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
        G.smooth(ob,70)
        mod=ob.modifiers.new('Actual sewn material thickness','SOLIDIFY');mod.thickness=thick;mod.offset=-1;mod.use_even_offset=True
        return self.add(ob,parent)
    def sling_panel(self,name,contour,width,parent=None):
        steps=12 if self.high else 6;vs=[]
        for y,z in contour:
            for i in range(steps+1):
                u=-1+2*i/steps;x=width/2*u
                sag=.011*(1-u*u)*math.sin(math.pi*(y-contour[0][0])/(contour[-1][0]-contour[0][0]))
                vs.append((x,y,z-sag))
        fs=[(j*(steps+1)+i,j*(steps+1)+i+1,(j+1)*(steps+1)+i+1,(j+1)*(steps+1)+i) for j in range(len(contour)-1) for i in range(steps)]
        return self.shell(name,vs,fs,self.sling,parent=parent)

    def chair(self):
        root=self.module('Chair','Chair')
        for sign in (-1,1):
            x=sign*.309
            # Smooth bent tubular arm and front upright, rear leg welded at arm return.
            arm=[(x,-.334,.021),(x,-.310,.35),(x,-.302,.56),(x,-.292,.607),
                 (x,-.263,.637),(x,-.20,.645),(x,.10,.63),(x,.235,.613)]
            curved=[arm[0]]
            for k in range(1,len(arm)-1):
                a,b,c=map(Vector,(arm[k-1],arm[k],arm[k+1]));entry=b+(a-b)*.20;end=b+(c-b)*.20
                for j in range(5 if self.high else 3):
                    t=j/(4 if self.high else 2);curved.append(tuple((1-t)**2*entry+2*(1-t)*t*b+t*t*end))
            curved.append(arm[-1])
            self.tube(f'Chair arm and front leg {sign}',curved,.016)
            rear=[(x,.345,.021),(x,.30,.31),(x,.25,.48),(x,.235,.613)]
            self.tube(f'Chair rear leg {sign}',rear,.016)
            for y in (-.334,.345):
                self.box(f'Chair foot {sign} {y}',(x,y,.013),(.034,.035,.026),self.rubber,.003)
            rail=[(sign*.277,-.30,.445),(sign*.277,-.22,.442),(sign*.277,.055,.424),
                  (sign*.277,.13,.448),(sign*.277,.20,.60),(sign*.277,.295,.84),(sign*.277,.325,.945)]
            self.tube(f'Chair sling spline rail {sign}',rail,.0125)
            self.tube(f'Chair seat mounting boss {sign}',[(sign*.277,-.303,.43),(sign*.310,-.303,.43)],.010,sides=12 if self.high else 8)
            self.bolt(f'Chair seat fixing {sign}',(sign*.323,-.303,.430),(sign,0,0))
            self.bolt(f'Chair rear fixing {sign}',(sign*.322,.249,.48),(sign,0,0))
            if self.high:
                self.tube(f'Chair sewn pocket {sign}',[(sign*.263,y,z+.0007) for x,y,z in rail],.0018,self.sling,sides=6)
        for y,z in [(-.297,.431),(.108,.411),(.325,.943)]:
            self.tube('Chair welded cross member', [(-.277,y,z),(0,y,z+.004),(.277,y,z)],.011)
        self.tube('Chair lower rear spreader',[(-.309,.29,.285),(.309,.29,.285)],.011)
        self.sling_panel('Chair continuous tensioned sling',[(-.30,.445),(-.22,.443),(.055,.425),(.13,.450),(.20,.60),(.295,.841),(.325,.946)],.535)
        root.location=(-1.45,0,0)

    def table(self):
        root=self.module('Table','Table')
        w,d,h=1.524,.9652,.762
        for sign in (-1,1):
            self.box('Table long perimeter extrusion',(0,sign*(d/2-.025),h-.015),(w-.05,.05,.03),r=.003)
            self.box('Table short perimeter extrusion',(sign*(w/2-.025),0,h-.015),(.05,d,.03),r=.003)
        for i in range(-7,8):
            ob=G.box(f'Table drainage slat {i+8:02d}',(i*.094,0,h-.010),(.088,d-.1,.020),self.paint,.0013,3 if self.high else 1)
            if i==0:
                cutter=G.cylinder('Umbrella bore tool',(0,0,.72),(0,0,.79),.027,self.paint,48 if self.high else 24)
                G.boolean(ob,cutter)
            self.add(ob)
        # Molded insert bore leaves 6.95 mm radial clearance around the 38.1 mm shaft.
        ring=G.lathe('Table umbrella insert',[(h-.023,.026),(h-.023,.028),(h-.001,.028),(h+.0007,.030),(h+.001,.026)],self.rubber,48 if self.high else 24,closed=True)
        self.add(ring)
        for sx in (-1,1):
            for sy in (-1,1):
                top=(sx*.643,sy*.353,.723);bottom=(sx*.694,sy*.406,.018)
                self.bar(f'Table leg {sx} {sy}',bottom,top,.037)
                self.box(f'Table foot {sx} {sy}',(bottom[0],bottom[1],.013),(.041,.041,.026),self.rubber,.003)
                self.box(f'Table cast corner socket {sx} {sy}',top,(.065,.064,.043),r=.005)
                self.bolt(f'Table leg bolt {sx} {sy}',(top[0],top[1]-.033,.716),(0,-1,0),r=.004)
        for sy in (-1,1):
            self.bar('Table underside longitudinal bearer',(-.68,sy*.35,.714),(.68,sy*.35,.714),.026,.035)
        for sx in (-1,1):
            self.bar('Table lower end stretcher',(sx*.675,-.383,.27),(sx*.675,.383,.27),.024)
        # Two longitudinal braces carry a central guide without blocking the pole.
        for sy in (-1,1):self.bar('Table lower longitudinal tie',(-.675,sy*.07,.27),(.675,sy*.07,.27),.020)
        self.add(G.lathe('Table lower pole guide',[(.260,.038),(.260,.085),(.280,.085),(.280,.038)],self.paint,32 if self.high else 20,closed=True))

    def chaise(self):
        root=self.module('Chaise','Chaise');hinge=(0,.275,.365)
        for sx in (-1,1):
            x=sx*.342
            self.tube(f'Chaise long chassis {sx}',[(x,-1.035,.325),(x,-.95,.35),(x,.15,.35),(x,.25,.30),(x,.95,.285)],.016)
            for y in (-.79,.76):
                self.bar(f'Chaise splayed leg {sx} {y}',(sx*.342,y,.016),(sx*.342,y-.035,.326 if y<0 else .297),.028)
                self.box(f'Chaise foot {sx} {y}',(sx*.342,y,.013),(.032,.041,.026),self.rubber,.003)
            self.tube(f'Chaise seat spline {sx}',[(sx*.303,-1.039,.34),(sx*.303,-.95,.35),(sx*.303,.24,.35)],.012)
        for y,z in [(-1.035,.325),(-.79,.31),(.20,.327),(.85,.277)]:
            self.bar('Chaise chassis cross tie',(-.342,y,z),(.342,y,z),.022)
        self.sling_panel('Chaise fixed sling',[(-1.039,.341),(-.95,.351),(-.55,.345),(-.08,.349),(.24,.352)],.584)
        for sx in (-1,1):
            self.tube(f'Chaise fixed sewn spline pocket {sx}',[(sx*.291,-1.039,.342),(sx*.291,-.95,.352),(sx*.291,-.55,.346),(sx*.291,-.08,.350),(sx*.291,.24,.353)],.0023,self.sling,sides=6 if self.high else 5)
        back=G.pivot('Chaise_Backrest',hinge,'X',(0,65));back.parent=root
        # Geometry authored in world/rest coordinates, then rebased onto the hinge.
        for sx in (-1,1):
            self.tube(f'Chaise backrest rail {sx}',[(sx*.303,.285,.365),(sx*.303,.62,.365),(sx*.303,1.037,.365)],.012,parent=back)
            self.add(G.lathe(f'Chaise rotating hinge boss {sx}',[(sx*.308,.0065),(sx*.308,.027),(sx*.325,.027),(sx*.325,.0065)],self.paint,32 if self.high else 16,axis='X',center=(.275,.365),closed=True),back)
            # Fixed thick indexed cheek plates: holes and machined edge detail in high only.
            ob=G.lathe(f'Chaise fixed hinge quadrant {sx}',[(sx*.33-.003,.0065),(sx*.33-.003,.052),(sx*.33+.003,.052),(sx*.33+.003,.0065)],self.paint,48 if self.high else 24,axis='X',center=(.275,.365),closed=True)
            if self.high:
                for deg in (0,25,45,65):
                    a=math.radians(deg);y=.275+.039*math.cos(a);z=.365+.039*math.sin(a)
                    G.boolean(ob,G.cylinder('Index recess tool',(sx*.33-.010,y,z),(sx*.33+.010,y,z),.0023,self.metal,12))
            self.add(ob)
            self.box(f'Chaise hinge chassis bracket {sx}',(sx*.33,.275,.331),(.006,.026,.054),r=.001)
            lock=G.pivot('Chaise_Lock_'+('L' if sx<0 else 'R'),(sx*.341,.275,.365),'X',(0,360));lock.parent=root
            # Captive bolt through real clearance bores, joining wheel and hinge.
            self.add(G.cylinder(f'Chaise hinge lock shaft {sx}',(sx*.305,.275,.365),(sx*.345,.275,.365),.006,self.metal,16 if self.high else 8),lock)
            ob=G.lathe(f'Chaise hinge handwheel {sx}',[(sx*.333,0),(sx*.333,.023),(sx*.351,.026),(sx*.358,.023),(sx*.358,0)],self.rubber,32 if self.high else 24,axis='X',center=(.275,.365));self.add(ob,lock)
            self.bolt(f'Chaise hinge bolt {sx}',(sx*.359,.275,.365),(sx,0,0),lock,r=.004)
        self.tube('Chaise backrest crown',[(-.303,1.037,.365),(0,1.041,.371),(.303,1.037,.365)],.012,parent=back)
        self.tube('Chaise backrest lower crossbar',[(-.303,.30,.352),(.303,.30,.352)],.010,parent=back)
        self.sling_panel('Chaise hinged sling',[(.295,.367),(.55,.367),(.80,.369),(1.037,.367)],.584,parent=back)
        for sx in (-1,1):
            self.tube(f'Chaise back sewn spline pocket {sx}',[(sx*.291,.295,.368),(sx*.291,.55,.368),(sx*.291,.80,.370),(sx*.291,1.037,.368)],.0023,self.sling,sides=6 if self.high else 5,parent=back)
            for y in (-1.035,1.037):
                self.add(G.cylinder(f'Chaise spline end plug {sx} {y}',(sx*.303,y-.003,.34 if y<0 else .365),(sx*.303,y+.004,.34 if y<0 else .365),.013,self.rubber,12 if self.high else 8),root if y<0 else back)
        root.location=(1.75,.2,0)

    def umbrella_base(self,prefix):
        base=[(.010,.021),(.010,.241),(.018,.250),(.035,.247),(.045,.231),(.052,.060),(.072,.038),(.325,.028),(.330,.025),(.330,.0203),(.052,.0203)]
        self.add(G.lathe(prefix+' weighted cast base',base,self.paint,64 if self.high else 32,closed=True))
        self.add(G.lathe(prefix+' socket bottom stop',[(.017,0),(.017,.023),(.025,.023),(.025,0)],self.paint,32 if self.high else 16))
        self.add(G.lathe(prefix+' rubber ground ring',[(0,.210),(0,.238),(.012,.241),(.015,.210)],self.rubber,48 if self.high else 24,closed=True))
        self.add(G.lathe(prefix+' aluminum pole',[(.025,.01705),(.025,.01905),(2.49,.01905),(2.49,.01705)],self.paint,32 if self.high else 16,closed=True))
        self.add(G.lathe(prefix+' pole joint collar',[(.813,.019),(.813,.021),(.84,.021),(.84,.019)],self.paint,32 if self.high else 16,closed=True))
        self.bolt(prefix+' base securing screw',(.027,0,.25),(1,0,0),r=.004)
        self.box(prefix+' crank cast case',(0,-.005,.978),(.057,.062,.093),r=.013)
        crank=G.pivot(prefix+'_Crank',(0,-.043,.978),'Y',(0,360));crank.parent=self.root
        self.tube(prefix+' crank arm',[(0,-.044,.978),(.055,-.044,1.006)],.0075,sides=10 if self.high else 6,parent=crank)
        self.add(G.cylinder(prefix+' crank rotating grip',(.055,-.044,1.006),(.055,-.091,1.006),.011,self.rubber,16 if self.high else 8),crank)
        self.bolt(prefix+' crank fixing',(0,-.052,.978),(0,-1,0),crank)
        self.add(G.lathe(prefix+' finial',[(2.475,0),(2.475,.030),(2.500,.031),(2.54,.023),(2.565,0)],self.paint,32 if self.high else 16))
        return crank

    def cloth_triangles(self,ob):
        # Cycles and the game exporter must use the same diagonals on saddle quads.
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
        bm.to_mesh(ob.data);bm.free()
        return ob

    def canopy(self):
        # Equal high/game cloth tessellation keeps thin-sheet projections stable.
        n=4;rings=[.027,.20,.48,.72,1.0];R=1.3716;count=8*n
        def point(f,i):
            k=i//n;t=(i%n)/n;a=k*math.pi/4;b=(k+1)*math.pi/4
            scallop=math.sin(math.pi*t)**1.15
            rr=R*f-.035*scallop*f**3
            x=rr*((1-t)*math.cos(a)+t*math.cos(b));y=rr*((1-t)*math.sin(a)+t*math.sin(b))
            return x,y,2.48-.44*f**1.1-.075*scallop*f**1.6
        loops=[[point(f,i) for i in range(count)] for f in rings]
        vs=[p for loop in loops for p in loop]
        fs=[(j*count+i,j*count+(i+1)%count,(j+1)*count+(i+1)%count,(j+1)*count+i) for j in range(len(rings)-1) for i in range(count)]
        self.cloth_triangles(self.shell('Open eight-panel canopy',vs,fs,self.cloth,.0017))
        # The vent has its own downturned valance, separate from the gap below it.
        loops=[]
        for r,z in [(.024,2.513),(.11,2.498),(.27,2.465),(.27,2.442)]:
            loops.append([(r*math.cos(i*math.tau/count),r*math.sin(i*math.tau/count),z) for i in range(count)])
        ob=G.loft('Open floating wind vent',loops,self.cloth,caps=False)
        if sum(p.normal.z*p.area for p in ob.data.polygons)<0:
            bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
        sol=ob.modifiers.new('Vent sewn thickness','SOLIDIFY');sol.thickness=.0017
        self.cloth_triangles(self.add(G.smooth(ob,70)))
        for i in range(8):
            a=i*math.pi/4;c,s=math.cos(a),math.sin(a)
            rib=[(x,y,z-.014) for x,y,z in [point(f,i*n) for f in rings]]
            self.tube(f'Open rib {i}',rib,.006,self.paint,sides=12 if self.high else 6)
            self.tube(f'Open stretcher {i}',[(.030*c,.030*s,1.94),rib[2]],.0045,self.paint,sides=6 if self.high else 5)
            self.add(G.cylinder(f'Open sewn rib tip {i}',(1.357*c,1.357*s,2.018),(1.378*c,1.378*s,2.034),.008,self.binding,10 if self.high else 6))
            # A sewn tunnel wraps the rib underneath the canopy; its crown meets
            # the lower cloth skin and prevents the metal emerging at each bend.
            self.tube(f'Open underside rib pocket {i}',[(x,y,z-.012) for x,y,z in [point(f,i*n) for f in rings]],.011,self.binding,sides=8 if self.high else 4)
        if self.high:
            for name,ff in [('Open stitched hem',(.987,1)),('Open vent binding',None)]:
                if ff:
                    ob=G.loft(name,[[(x,y,z+.0006) for x,y,z in [point(f,i) for i in range(count)]] for f in ff],self.binding,caps=False)
                else:
                    ob=G.loft(name,[[(.271*math.cos(i*math.tau/count),.271*math.sin(i*math.tau/count),z) for i in range(count)] for z in (2.442,2.449)],self.binding,caps=False)
                if ff and sum(p.normal.z*p.area for p in ob.data.polygons)<0:
                    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
                ob['allow_boundary']=True;self.add(ob)
        for z,r in [(2.46,.042),(1.94,.045)]:
            self.add(G.lathe('Open rib hub',[(z-.023,.020),(z-.023,r),(z+.023,r),(z+.023,.020)],self.rubber,32 if self.high else 16,closed=True))

    def closed_canopy(self):
        count=48
        profile=[(1.13,.082),(1.17,.116),(1.36,.101),(1.65,.060),(1.72,.064),(1.99,.110),(2.25,.105),(2.40,.068),(2.48,.025)]
        loops=[]
        for j,(z,r) in enumerate(profile):
            ring=[]
            for i in range(count):
                a=i*math.tau/count;phase=(z-1.13)*1.05
                fold=1+.23*math.sin(8*a+phase)+.075*math.sin(16*a-phase*.7)
                rr=r*fold
                ring.append((rr*math.cos(a),rr*math.sin(a),z+.028*math.cos(8*a)*(1 if j==0 else .15)))
            loops.append(ring)
        ob=G.loft('Closed gathered eight-gore canopy',loops,self.folded,caps=False)
        sol=ob.modifiers.new('Furled sewn envelope thickness','SOLIDIFY');sol.thickness=.0018;self.cloth_triangles(self.add(G.smooth(ob,65)))
        # Bound scalloped lower hem and eight gathered pocket seams project to cloth.
        if self.high:
            ob=G.loft('Closed stitched gathered hem',[[(x*1.007,y*1.007,z+dz) for x,y,z in loops[0]] for dz in (0,.012)],self.binding,caps=False)
            ob['allow_boundary']=True;self.add(ob)
            for i in range(8):
                self.tube(f'Closed sewn pocket seam {i}',[(x*1.006,y*1.006,z) for x,y,z in [loop[i*6] for loop in loops]],.0011,self.binding,sides=5)
        # The top vent's own short valance remains visible over the gathered body.
        self.add(G.lathe('Closed vent valance',[(2.375,.077),(2.405,.073),(2.405,.071),(2.375,.075)],self.folded,24,closed=True))
        self.add(G.lathe('Closed woven tie band',[(1.655,.072),(1.655,.077),(1.692,.077),(1.692,.072)],self.sling,48 if self.high else 24,closed=True))
        self.box('Closed tie buckle',(0,-.080,1.673),(.028,.013,.027),self.rubber,.002)
        for sx in (-1,1):
            ob=G.sheet('Closed tie free tail',[(-.082,1.666),(-.099,1.59),(-.087,1.54)],.018,.0015,self.sling);ob.location.x=sx*.014;self.add(ob)
        for i in range(8):
            a=i*math.pi/4
            self.tube('Closed exposed rib tip',[(.079*math.cos(a),.079*math.sin(a),1.10),(.089*math.cos(a),.089*math.sin(a),1.19)],.0045,sides=6)
        self.add(G.lathe('Closed lowered runner',[(1.13,.020),(1.13,.039),(1.17,.039),(1.17,.020)],self.rubber,24 if self.high else 12,closed=True))

    def umbrella(self,closed=False):
        prefix='Closed' if closed else 'Open'
        root=self.module('Umbrella_'+prefix,'Umbrella_'+prefix)
        self.umbrella_base(prefix)
        if closed:self.closed_canopy();root.location=(-2.5,1,0)
        else:self.canopy()

    def save(self):
        sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
        sc['asset']='PatioSet';sc['quality']=self.args.quality;sc['wear']=self.args.wear;sc['seed']=73
        for name,dy in [('Chair',-.0055),('Chaise',.015)]:
            root=bpy.data.objects[name]
            for ob in root.children:
                if ob.type=='MESH':
                    for v in ob.data.vertices:v.co.y+=dy
                else:ob.location.y+=dy
        bpy.context.view_layer.update()
        Path(self.args.out).parent.mkdir(parents=True,exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(self.args.out).resolve()))
        counts={}
        for ob in sc.objects:
            if ob.type=='MESH':ob.data.calc_loop_triangles();counts[ob['asset_set']]=counts.get(ob['asset_set'],0)+len(ob.data.loop_triangles)
        print('FAMILY_TRIANGLES',json.dumps(counts),flush=True)

if __name__=='__main__':
    a=arguments();f=Family(a);f.table();f.chair();f.chaise();f.umbrella();f.umbrella(True);f.save()
