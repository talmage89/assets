"""Bellford H-54: measured original dry-barrel hydrant; no external asset input.

FH-84 provides overall anchors. All profiles, ribs, cap geometry and chains
are authored equations; reference drawings are never parsed by this script.
"""
import argparse,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import model as G,materials as M


class Hydrant:
    def __init__(self,high,wear):
        self.high=high;self.n=96 if high else 24
        self.root=G.pivot('FireHydrant',(0,0,0));self.root['static_root']=True
        drips=[dict(x=x,z=.638,width=.004,length=.11,direction=(0,-1,0)) for x in (-.09,.07)]
        bands=[(.056,.002),(.087,.001),(.626,.002),(.651,.002)]
        rings=[((0,-.154,.4572),(0,-1,0),.080,.003),
               ((0,-.183,.4572),(0,-1,0),.064,.003)]
        for sign in (-1,1):rings.append(((sign*.153,0,.4572),(sign,0,0),.053,.002))
        self.red=M.painted_cast('Weathered municipal red enamel',(.23,.006,.004),wear,bands,drips,.32,wear_rings=rings)
        self.cream=M.painted_cast('Chalked warm white bonnet enamel',(.69,.67,.57),wear,
                                    [(.653,.002),(.675,.002),(.777,.002)],drips,.49)
        self.black=M.surface('Bituminous ground stub','paint',wear,color=(.011,.014,.012),dust=.5,grime=.3,roughness=.73)
        self.seal=M.surface('Dark cap and bonnet reveals','rubber',wear,color=(.009,.008,.006),roughness=.85)
        self.steel=M.surface('Dull zinc chain and hardware','stainless',wear,color=(.25,.27,.25),roughness=.60,dust=.2,grime=.3)
        self.nut=M.surface('Wrench polished bronze','brass',wear,color=(.24,.17,.075),roughness=.62,grime=.5)

    def add(self,ob):return G.attach(ob,self.root,'Hydrant')

    def lathe(self,name,profile,mat,n=None,ribs=0,amplitude=0):
        if not self.high:
            if name=='Traffic lower flange':profile=[(.041275,.100),(.041275,.165),(.055,.171),(.058,.100)]
            if name=='Traffic upper flange':profile=[(.060,0),(.060,.164),(.066,.171),(.080,.171),(.089,.115),(.100,.104),(.100,0)]
            if name=='Cast upper barrel':profile=[p for p in profile if p[0] not in (.13,.235,.250)]
            if name=='Cast bonnet':profile=[p for p in profile if p[0] not in (.675,.722,.764)]
            if name in ('Breakaway joint shadow','Bonnet gasket reveal','Bonnet thrust collar'):n=16
        ob=G.lathe(name,profile,mat,n or self.n)
        if ribs:
            for v in ob.data.vertices:
                x,y,z=v.co;rad=math.hypot(x,y)
                if rad<.03:continue
                if 'bonnet' in name:
                    envelope=max(0,math.sin(math.pi*min(1,max(0,(z-.675)/.098))))**.65
                else:envelope=max(0,math.sin(math.pi*min(1,max(0,(z-.10)/.14))))**.6
                delta=amplitude*max(0,math.cos(math.atan2(y,x)*ribs))**6*envelope
                v.co.x*=1+delta/rad;v.co.y*=1+delta/rad
            ob.data.update()
        return ob

    def pent(self,name,axis,base,height,af,mat):
        r=af/(2*math.cos(math.pi/5));n=5
        # Edge chamfers remain explicit in low mesh, with flat wrench flats.
        ob=G.lathe(name,[(0,0),(0,r*.90),(.0015,r),(height-.002,r),
                         (height,r*.88),(height,0)],mat,n)
        for p in ob.data.polygons:p.use_smooth=False
        ob.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();ob.location=base
        return self.add(ob)

    def bolt(self,name,x,y,z,mat):
        h=.011;r=.010
        profile=[(0,0),(0,r*.9),(.001,r),(h-.002,r),(h,r*.85),(h,0)] if self.high else [(0,0),(0,r),(h,r),(h,0)]
        ob=G.lathe(name,profile,mat,6)
        ob.location=(x,y,z)
        for p in ob.data.polygons:p.use_smooth=False
        self.add(ob)
        if self.high:
            self.add(G.lathe(name+' washer',[(z-.001,.006),(z-.001,.012),(z+.001,.012),(z+.001,.006)],mat,24,center=(x,y),closed=True))

    def body(self):
        self.add(self.lathe('Bitumen lower barrel at grade',[(0,0),(0,.100),(.057,.100),(.057,0)],self.black))
        # Two real flange halves and a thin shadow reveal. Below-grade shoe is omitted.
        self.add(self.lathe('Traffic lower flange',[(.041275,.100),(.041275,.163),(.047,.171),(.055,.171),(.058,.162),(.058,.100)],self.red))
        self.add(self.lathe('Breakaway joint shadow',[(.058,0),(.058,.163),(.060,.163),(.060,0)],self.seal))
        self.add(self.lathe('Traffic upper flange',[(.060,0),(.060,.164),(.066,.171),(.080,.171),(.087,.158),(.089,.115),(.100,.104),(.100,0)],self.red))
        prof=[(.087,.103),(.100,.103),(.13,.102),(.18,.102),(.235,.102),(.240,.110),(.250,.112),(.270,.112),(.279,.101),(.32,.100),(.42,.100),(.52,.101),(.608,.102),(.620,.108),(.626,.138),(.638,.139)]
        body=self.lathe('Cast upper barrel',prof,self.red,ribs=6,amplitude=.0075)
        # Union the three cast nozzle necks into the barrel: no hidden backing faces.
        for label,axis,big in [('Pumper',(0,-1,0),True),('Hose left',(-1,0,0),False),('Hose right',(1,0,0),False)]:
            r=.073 if big else .049
            neck=G.lathe(label+' cast throat',[(.065,0),(.065,r*.78),(.101,r*1.12),(.124,r),(.139,r),(.139,0)],self.red,self.n)
            neck.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();neck.location=(0,0,.4572)
            G.boolean(body,neck,'UNION')
        # Exact unions can leave almost coincident intersection vertices. Weld
        # only sub-micron numerical residue, then remove degenerate edges/faces.
        bm=bmesh.new();bm.from_mesh(body.data)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
        bmesh.ops.triangulate(bm,faces=list(bm.faces))
        bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        bm.to_mesh(body.data);bm.free()
        G.smooth(body,48);self.add(body)
        # Eight galvanized, then overpainted flange bolts on each flange.
        for z,rad,mat,prefix in [(.080,.143,self.red,'Traffic flange'),(.638,.119,self.cream,'Bonnet')]:
            for i in range(8):
                t=(i+.5)*math.tau/8
                self.bolt(prefix+f' bolt {i+1}',rad*math.cos(t),rad*math.sin(t),z,mat)
        self.add(self.lathe('Bonnet gasket reveal',[(.638,0),(.638,.135),(.640,.135),(.640,0)],self.seal))
        self.add(self.lathe('Cast bonnet',[(.640,0),(.640,.138),(.644,.145),(.650,.145),(.657,.137),(.661,.112),
                        (.675,.103),(.697,.101),(.722,.094),(.745,.081),(.764,.059),(.776,.039),(.780,.036),(.780,0)],self.cream,ribs=8,amplitude=.0035))
        self.add(self.lathe('Bonnet thrust collar',[(.778,0),(.778,.036),(.785,.036),(.789,.030),(.789,0)],self.cream))
        self.pent('Pentagonal operating nut',(0,0,1),(0,0,.7838),.029,.0381,self.nut)
        # Real filler screw, sitting on the front bonnet slope.
        self.add(G.cylinder('Bonnet oil filler screw',(0,-.091,.714),(0,-.095,.718),.006,self.nut,8))

    def caps(self):
        for label,axis,big in [('Pumper',(0,-1,0),True),('Hose left',(-1,0,0),False),('Hose right',(1,0,0),False)]:
            r=.080 if big else .053
            end=.224 if big else .207772
            # Painted cast cap overlaps the replaceable bronze nozzle; only the reveal reads.
            for name,prof,mat in [
                (label+' cap seam',[(.137,0),(.137,r*.95),(.141,r*.95),(.141,0)],self.seal),
                (label+' cap',[(.141,0),(.141,r*.94),(.145,r),(.155,r),(.159,r*.97),(.173,r*.96),
                             (.181,r*.84),(.188,r*.61),(.190,r*.43),(.190,0)],self.red),
            ]:
                if not self.high and name.endswith(' cap'):
                    prof=[(.141,0),(.141,r),(.158,r),(.180,r*.86),(.190,r*.43),(.190,0)]
                segments=12 if not self.high and name.endswith('seam') else self.n
                ob=G.lathe(name,prof,mat,segments);ob.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();ob.location=(0,0,.4572);self.add(ob)
            self.pent(label+' cap wrench nut',axis,Vector((0,0,.4572))+Vector(axis)*.187,end-.187,.033 if not big else .0381,self.red)
            # Raised cast cap perimeter bead in source, transferred to normal map.
            if self.high:
                ob=G.lathe(label+' cap raised face ring',[(.183,r*.69),(.185,r*.71),(.188,r*.69),(.185,r*.67)],self.red,64,closed=True)
                ob.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();ob.location=(0,0,.4572);self.add(ob)

    def chain(self,name,points):
        # Uniform arc stations; alternated planes make actual interlinked steel loops.
        pts=list(map(Vector,points));lengths=[0]
        for a,b in zip(pts,pts[1:]):lengths.append(lengths[-1]+(b-a).length)
        count=round(lengths[-1]/.020)
        def sample(distance):
            for i in range(len(pts)-1):
                if distance<=lengths[i+1]:return pts[i].lerp(pts[i+1],(distance-lengths[i])/(lengths[i+1]-lengths[i]))
            return pts[-1]
        for i in range(count+1):
            distance=lengths[-1]*i/count;center=sample(distance)
            tangent=(sample(min(lengths[-1],distance+.004))-sample(max(0,distance-.004))).normalized()
            u=tangent.cross(Vector((0,1,.1))).normalized();v=tangent.cross(u).normalized()
            transverse=u if i%2==0 else v
            steps=16 if self.high else 6;sides=8 if self.high else 4
            path=[center+tangent*(.0125*math.cos(j*math.tau/steps))+transverse*(.0055*math.sin(j*math.tau/steps)) for j in range(steps)]
            # Ring loft with analytical frame: avoid seam cap or double vertices.
            loops=[]
            normal=tangent.cross(transverse).normalized()
            for j,p in enumerate(path):
                along=(path[(j+1)%steps]-path[j-1]).normalized();out=along.cross(normal)
                loops.append([p+.00165*(out*math.cos(k*math.tau/sides)+normal*math.sin(k*math.tau/sides)) for k in range(sides)])
            self.add(G.smooth(G.ring_loft(name+f' link {i:02}',loops,self.steel)))

    def chains(self):
        for sign in (-1,1):
            self.chain('Chain hose '+str(sign),G.bezier((sign*.185,-.010,.423),(sign*.192,-.075,.228),(sign*.05,-.145,.247),(sign*.008,-.139,.302),24))
        self.chain('Chain pumper',G.bezier((.012,-.197,.421),(.030,-.209,.349),(-.008,-.146,.296),(0,-.150,.310),20))
        loops=[]
        for i in range(8):
            t=i*math.tau/8
            loops.append([(.010*math.cos(t)+.00165*math.cos(k*math.tau/4)*math.cos(t),
                           -.139+.00165*math.sin(k*math.tau/4),
                           .302+.010*math.sin(t)+.00165*math.cos(k*math.tau/4)*math.sin(t)) for k in range(4)])
        self.add(G.smooth(G.ring_loft('Chain common joining ring',loops,self.steel)))
        # Cap lugs and a common chain anchor hook, no movable parts in this prop.
        for x,y in [(-.185,0),(.185,0),(.012,-.197)]:
            self.add(G.tube('Cap chain forged eye',[(x-.005,y,.431),(x-.006,y-.002,.414),(x+.006,y-.002,.414),(x+.005,y,.431)],.0024,self.red,8 if self.high else 4))

    def casting(self):
        if not self.high:return
        font=bpy.data.fonts.load('/usr/share/fonts/TTF/DejaVuSans-Bold.ttf')
        for text,z,size in [('BELLFORD',.545,.036),('5 1/4',.503,.032),('WATER WORKS',.405,.025),('H-54',.365,.028),('2021',.312,.025)]:
            cu=bpy.data.curves.new('Original foundry type','FONT');cu.body=text;cu.font=font;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.00065;cu.resolution_u=3
            ob=bpy.data.objects.new('Raised casting '+text,cu);bpy.context.collection.objects.link(ob)
            bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.convert(target='MESH');ob.select_set(False)
            for v in ob.data.vertices:
                x,y,d=v.co;radius=.1015 if z>.5 else .1003;angle=-x/radius;r=radius+d
                v.co=(r*math.sin(angle),r*math.cos(angle),z+y)
            bm=bmesh.new();bm.from_mesh(ob.data)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
            bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
            bm.to_mesh(ob.data);bm.free()
            ob.data.materials.append(self.red);self.add(ob)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--quality',choices=['high','game'],default='high');p.add_argument('--wear',type=float,default=.55)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not 0<=a.wear<=2:raise ValueError('wear must be in [0,2]')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    b=Hydrant(a.quality=='high',a.wear);b.body();b.caps();b.chains();b.casting()
    sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
    sc['asset']='FireHydrant';sc['quality']=a.quality;sc['wear']=a.wear;sc['seed']=54;sc['stage']='lookdev'
    bpy.context.view_layer.update();Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    count=0
    for ob in sc.objects:
        if ob.type=='MESH':ob.data.calc_loop_triangles();count+=len(ob.data.loop_triangles)
    print('BUILD_COUNTS',json.dumps({'Hydrant':count}),flush=True)

if __name__=='__main__':main()
