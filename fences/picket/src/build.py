"""Original white cedar spaced-picket kit, clean-start deterministic Blender."""
import argparse,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parents[1]/'src'),str(HERE.parents[2])]
from kit import model as G,materials as M
from modular import Builder
from dimensions import *
from finishes import white_wood

class Picket(Builder):
    def wood(self,parent,name,center,size,seed,tip=False,axis=(0,0,1),nails=()):
        center=Vector(center);length=size[2] if tip else max(size)
        f=self.frame(parent,name,center-Vector(axis)*length/2,axis)
        w=size[0] if tip else min(size[:2])
        depth=size[1] if tip else (size[2] if abs(axis[0])>.5 else max(size[:2]))
        mat=white_wood(name+' paint',f,parent,w,length,seed,self.wear,nails,depth=depth)
        if tip:
            w,h=size[0],size[2]
            # Distinct French Gothic shoulder and pinched throat, original profile.
            half=[(w/2,0),(w/2,h-.155),(w*.32,h-.144),(w*.26,h-.127),(w*.29,h-.112),(w/2,h-.093),(w*.43,h-.064),(w*.18,h)]
            pts=[(-w/2,0)]+half+ [(-x,z) for x,z in reversed(half[1:])]
            ob=G.profile(name,pts,center.y-size[1]/2,center.y+size[1]/2,mat,axis='Y',radius=.00065 if self.high else 0,segments=2)
            for v in ob.data.vertices:v.co.x+=center.x;v.co.z+=center.z-h/2
            self.attach(ob,parent)
        else:ob=self.box(parent,name,center,size,mat,.0008)
        ob['construction_role']='picket' if tip else 'frame';return ob
    def post(self,parent,name,x,seed):
        self.wood(parent,name,(x,0,POST_TOP/2),(POST,POST,POST_TOP),seed)
        f=self.frame(parent,name+' cap',(x,0,POST_TOP));mat=white_wood(name+' cap paint',f,parent,.114,.045,seed+9,self.wear)
        loops=[]
        for radius,z in [(.057,POST_TOP),(.057,POST_TOP+.009),(.011,CAP_TOP)]:
            loops.append([(x+u,v,z) for u,v in [(-radius,-radius),(radius,-radius),(radius,radius),(-radius,radius)]])
        self.attach(G.loft(name+' pyramid cap',loops,mat),parent)
    def saddles(self,parent,clear,metal):
        for s in (-1,1):
            x=s*clear/2
            for j,z in enumerate(RAILS):
                name=f'{parent.name} saddle {s} {j}'
                self.box(parent,name+' web',(x-s*.0005,0,z),(.001,.0401,RAIL_H+.002),metal,.00015)
                self.box(parent,name+' seat',(x-s*.0105,0,z-RAIL_H/2-.0005),(.019,.0401,.001),metal,.00015)
                for sy in (-1,1):self.box(parent,name+' cheek '+str(sy),(x-s*.0105,sy*.01955,z),(.019,.001,RAIL_H),metal,.00015)
                if self.high:
                    for sy in (-1,1):self.high_fastener(parent,name+' screw',(x-s*.012,sy*.0201,z),(0,sy,0),metal)
    def section(self,name,seed):
        p=self.root(name,STAGING[name]);clear=PITCH-POST;count=13;gap=(clear-count*WIDTH)/(count+1)
        for i in range(count):
            x=-clear/2+gap+WIDTH/2+i*(WIDTH+gap)
            self.wood(p,f'{name} picket {i+1:02}',(x,-RAIL_T/2-THICK/2,GROUND+HEIGHT/2),(WIDTH,THICK,HEIGHT),seed*100+i,True,nails=tuple(z-GROUND for z in RAILS))
        for i,z in enumerate(RAILS):self.wood(p,f'{name} rail {i+1}',(0,0,z),(clear-.014,RAIL_T,RAIL_H),seed*10+i,axis=(1,0,0))
        self.saddles(p,clear,M.galvanized(name+' zinc',None,self.wear))
        self.socket(p,'L',(-PITCH/2,0,0),180);self.socket(p,'R',(PITCH/2,0,0))
        for s in (-1,1):
            for i,z in enumerate(RAILS):self.socket(p,f'rail_{s}_{i}',(s*clear/2,0,z),0 if s>0 else 180,'rail_face')
    def posts(self):
        for i,(name,dirs) in enumerate([('Picket_End',(0,)),('Picket_Line',(0,180)),('Picket_Corner',(180,90))]):
            p=self.root(name,STAGING[name]);self.post(p,name+' timber',0,800+i)
            for yaw in dirs:self.socket(p,'connect_'+str(yaw),(0,0,0),yaw)
    def gate(self):
        p=self.root('Picket_GateBay',STAGING['Picket_GateBay'])
        for s in (-1,1):self.post(p,'Picket gate '+('hinge' if s<0 else 'latch')+' post',s*GATE_PITCH/2,930+s)
        self.socket(p,'L',(-GATE_PITCH/2,0,0),180);self.socket(p,'R',(GATE_PITCH/2,0,0))
        leaf=self.pivot(p,'Picket_Gate',(HINGE_X,HINGE_Y,0),'Z',(-110,0))
        before=set(bpy.context.scene.objects)
        # Five full pickets keep the gate's open rhythm close to the section.
        for i in range(5):
            x=-LEAF/2+WIDTH/2+i*(LEAF-WIDTH)/4
            self.wood(p,f'Picket gate board {i+1}',(x,-RAIL_T/2-THICK/2,GROUND+HEIGHT/2),(WIDTH,THICK,HEIGHT),950+i,True,nails=tuple(z-GROUND for z in RAILS))
        stile=.0635
        for s in (-1,1):self.wood(p,'Picket gate stile '+str(s),(s*(LEAF/2-stile/2),0,sum(RAILS)/2),(stile,RAIL_T,RAILS[-1]-RAILS[0]+RAIL_H),970+s)
        for i,z in enumerate(RAILS):self.wood(p,'Picket gate rail '+str(i+1),(0,0,z),(LEAF-2*stile,RAIL_T,RAIL_H),980+i,axis=(1,0,0))
        x0=-LEAF/2+stile;x1=LEAF/2-stile;lo=RAILS[0]+RAIL_H/2;hi=RAILS[1]-RAIL_H/2;bw=.073
        f=self.frame(p,'Picket gate brace',(x0,0,lo),(x1-x0,0,hi-lo));length=math.hypot(x1-x0,hi-lo)
        mat=white_wood('Picket brace paint',f,p,bw,length,999,self.wear)
        self.attach(G.profile('Picket compression brace',[(x0,lo),(x0+bw,lo),(x1,hi),(x1-bw,hi)],-RAIL_T/2,RAIL_T/2,mat,axis='Y',radius=.0008 if self.high else 0,segments=2),p)
        self.reparent([o for o in set(bpy.context.scene.objects)-before if o.parent==p],leaf)
        n=M.Nodes('Picket hardware black');metal=n.finish((.018,.021,.019),.52,.28,0)
        self.strap_hardware(p,leaf,metal,LEAF,GATE_PITCH,POST,RAILS,HINGE_X,HINGE_Y,-RAIL_T/2-THICK,.72)
        self.socket(leaf,'free_edge',(LEAF/2-HINGE_X,-HINGE_Y,.72),kind='gate_edge')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--wear',type=float,default=.55);ap.add_argument('--quality',choices=['high','game'],default='high');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);b=Picket('WhitePicket',a.quality=='high',a.wear)
    b.section('Picket_A',13);b.section('Picket_B',29);b.posts();b.gate()
    bpy.context.scene['quality']=a.quality;bpy.context.scene['asset']='WhitePicket';bpy.context.scene.unit_settings.system='METRIC'
    bpy.context.view_layer.update();Path(a.out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
if __name__=='__main__':main()
