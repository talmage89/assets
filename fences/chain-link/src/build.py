"""Galvanized residential chain-link with reusable alpha fabric and real fittings."""
import argparse,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1]/'src'),str(HERE.parents[2])]
from kit import model as G,materials as M
from kit.export import atlas_material
from modular import Builder
from dimensions import *
import mesh_tile

class Chain(Builder):
    def __init__(self,high,wear):
        super().__init__('ChainLink',high,wear);self.zinc=M.galvanized('Chain zinc',None,wear)
        folder=Path('build/fabric-source');mesh_tile.apply(folder)
        self.fabric_mat=atlas_material('ChainLink',folder.resolve(),.5,True)
        for node in self.fabric_mat.node_tree.nodes:
            if hasattr(node,'uv_map'):node.uv_map='BakeUV'
    def cyl(self,parent,name,start,end,radius,sides=12):
        return self.attach(G.cylinder(name,start,end,radius,self.zinc,max(sides*2,24) if self.high else sides),parent)
    def ring(self,parent,name,x,y,z,radius,height=.016,axis='Z',wall=.002,sides=12):
        c=(x,y) if axis=='Z' else ((x,z) if axis=='Y' else (y,z));center=z if axis=='Z' else y if axis=='Y' else x
        return self.attach(G.lathe(name,[(center-height/2,radius-wall),(center-height/2,radius),(center+height/2,radius),(center+height/2,radius-wall)],self.zinc,32 if self.high else sides,axis=axis,center=c,closed=True),parent)
    def post(self,parent,name,x,terminal=False):
        radius=(TERM_OD if terminal else LINE_OD)/2;top=TERM_TOP if terminal else LINE_TOP
        self.cyl(parent,name,(x,0,0),(x,0,top),radius,16)
        # Hollow cast cap with lip and low dome, supported directly on the tube.
        prof=[(top-.018,radius-.001),(top-.018,radius+.0015),(top+.004,radius+.0015),(top+.022,radius*.65),(top+.033,0),(top+.029,0),(top+.016,radius*.58),(top,radius-.001)]
        self.attach(G.lathe(name+' cap',prof,self.zinc,32 if self.high else 12,center=(x,0),closed=True),parent)
        if not terminal:
            # Eye's bore clears the continuous top rail; neck bears on the post cap.
            self.ring(parent,name+' rail eye',x,0,RAIL_Z,.0235,.016,'X',.004,12)
            self.box(parent,name+' eye neck',(x,0,1.223),(.020,.025,.026),self.zinc,.001)
    def band(self,parent,name,x,z,direction):
        self.ring(parent,name+' wrap',x,0,z,TERM_OD/2+.0015,.016,'Z',.0015,12)
        rad=math.radians(direction);v=Vector((math.cos(rad),math.sin(rad),0))
        front=Vector((math.sin(rad),-math.cos(rad),0))
        if direction==180:front=-front
        for label,offset in [(.0305,.03086875),(.0375,.03713125)]:
            center=Vector((x,0,z))+v*.029+front*offset
            ob=G.box(name+' ear '+str(label),center,(.046,.0015,.016),self.zinc,.0003 if self.high else 0,2);ob.rotation_euler.z=rad;self.attach(ob,parent)
        center=Vector((x,0,z))+v*.007+front*.034
        ob=G.box(name+' return',center,(.0015,.0085,.016),self.zinc,0);ob.rotation_euler.z=rad;self.attach(ob,parent)
        self.cyl(parent,name+' bolt',tuple(Vector((x,0,z))+v*.041+front*.027),tuple(Vector((x,0,z))+v*.041+front*.041),.003,6)
        if self.high:
            for ob in G.fastener(name+' carriage',tuple(Vector((x,0,z))+v*.041+front*.042),tuple(front),self.zinc,.0045,True,kind='hex',washer=True):self.attach(ob,parent)
    def terminal_fittings(self,parent,name,x,direction,stagger=0):
        # Rail end cup/collar carried by the terminal; pitch sockets stay at grade.
        rad=math.radians(direction);v=Vector((math.cos(rad),math.sin(rad),0))
        self.ring(parent,name+' brace band',x,0,RAIL_Z-.025-stagger,TERM_OD/2+.0015,.018,'Z',.0015,12)
        # Rail socket center just outside terminal side, rotated with direction.
        c=Vector((x,0,RAIL_Z))+v*(TERM_OD/2+.017)
        # A hollow cup is a lathed ring along X, then rotated about its center.
        cup=G.lathe(name+' rail end',[(0,.0215),(.025,.0215),(.025,.0188),(.002,.0188)],self.zinc,24 if self.high else 10,axis='X',center=(0,0),closed=True)
        cup.rotation_euler.z=rad;cup.location=(x+v.x*TERM_OD/2,v.y*TERM_OD/2,RAIL_Z);self.attach(cup,parent)
        # A stamped downward lug carries the hollow cup clear of its rail bore.
        lug_h=.018+stagger;center=Vector((x,0,RAIL_Z-.019-lug_h/2))+v*(TERM_OD/2-.004)
        lug=G.box(name+' rail lug',center,(.020,.004,lug_h),self.zinc,.0004 if self.high else 0,2);lug.rotation_euler.z=rad;self.attach(lug,parent)
        for i,z in enumerate((.20,.65,1.10)):self.band(parent,name+' tension '+str(i+1),x,z+stagger,direction)
        # Fittings include a flat tension bar, the section's fabric terminates here.
        front=Vector((math.sin(rad),-math.cos(rad),0))
        if direction==180:front=-front
        xx=x+v.x*.045+front.x*.034;yy=v.y*.045+front.y*.034
        bar=G.box(name+' tension bar',(xx,yy,GROUND+HEIGHT/2),(.015875,.0047625,HEIGHT-.012),self.zinc,0);bar.rotation_euler.z=rad;self.attach(bar,parent);bar['construction_role']='tension_bar'
    def wire_tie(self,parent,name,x,z,horizontal=True):
        if horizontal:
            points=[(x-.012,-.032,z-.026),(x-.012,-.026,z+.004),(x-.008,-.010,z+.019),(x+.008,.010,z+.019),(x+.012,.018,z),(x+.012,-.005,z-.018),(x+.010,-.034,z-.027)]
        else:
            points=[(x-.012,-.035,z-.013),(x-.025,-.008,z-.008),(x-.015,.019,z),(x+.014,.019,z+.008),(x+.025,-.010,z+.014),(x+.013,-.035,z+.015)]
        return self.attach(G.tube(name,points,.00145,self.zinc,8 if self.high else 4),parent)
    def fabric(self,parent,name,x0,x1,z0=GROUND,z1=GROUND+HEIGHT):
        verts=[];faces=[];uvs=[]
        def quad(xa,xb,za,zb,ua,ub,va,vb):
            i=len(verts);verts.extend([(xa,FABRIC_Y,za),(xb,FABRIC_Y,za),(xb,FABRIC_Y,zb),(xa,FABRIC_Y,zb)])
            faces.append((i,i+1,i+2,i+3));uvs.extend([(ua,va),(ub,va),(ub,vb),(ua,vb)])
        def breaks(lo,hi,offset=0):return [lo]+[offset+i*TILE for i in range(math.floor((lo-offset)/TILE)+1,math.ceil((hi-offset)/TILE)) if lo+1e-7<offset+i*TILE<hi-1e-7]+[hi]
        xx=breaks(x0,x1)
        for za,zb,flipped in [(z0,z0+EDGE,False),(z1-EDGE,z1,True)]:
            for xa,xb in zip(xx,xx[1:]):
                base=math.floor((xa+1e-7)/TILE)*TILE;u0,v0,u1,v1=EDGE_RECT
                quad(xa,xb,za,zb,u0+(xa-base)/TILE*(u1-u0),u0+(xb-base)/TILE*(u1-u0),v1 if flipped else v0,v0 if flipped else v1)
        zz=breaks(z0+EDGE,z1-EDGE,z0)
        for za,zb in zip(zz,zz[1:]):
            basez=z0+math.floor((za-z0+1e-7)/TILE)*TILE
            for xa,xb in zip(xx,xx[1:]):
                basex=math.floor((xa+1e-7)/TILE)*TILE;u0,v0,u1,v1=FIELD_RECT
                quad(xa,xb,za,zb,u0+(xa-basex)/TILE*(u1-u0),u0+(xb-basex)/TILE*(u1-u0),v0+(za-basez)/TILE*(v1-v0),v0+(zb-basez)/TILE*(v1-v0))
        ob=G.mesh(name,verts,faces,self.fabric_mat);self.attach(ob,parent);ob['allow_boundary']=True;ob['export_part']=name
        uv=ob.data.uv_layers.new(name='BakeUV')
        for i,p in enumerate(uvs):uv.data[i].uv=p
        ob['construction_role']='alpha_fabric';return ob
    def section(self,name,left_terminal=False,right_terminal=False):
        p=self.root(name,STAGING[name]);self.socket(p,'L',(-PITCH/2,0,0),180);self.socket(p,'R',(PITCH/2,0,0))
        xl=-PITCH/2+(TERM_OD/2+.003 if left_terminal else 0);xr=PITCH/2-(TERM_OD/2+.003 if right_terminal else 0)
        self.cyl(p,name+' top rail',(xl,0,RAIL_Z),(xr,0,RAIL_Z),RAIL_OD/2,12)
        self.cyl(p,name+' bottom tension wire',(-PITCH/2+(.0529375 if left_terminal else 0),FABRIC_Y,.095),(PITCH/2-(.0529375 if right_terminal else 0),FABRIC_Y,.095),.002,6)
        # Each section's six top ties carry the stand-off between rail and fabric.
        for i in range(6):self.wire_tie(p,name+' top tie '+str(i),-PITCH/2+.254+i*.508,RAIL_Z)
        self.fabric(p,name+'_Fabric',-PITCH/2+(.045 if left_terminal else 0),PITCH/2-(.045 if right_terminal else 0))
        self.socket(p,'rail_L',(-PITCH/2,0,RAIL_Z),180,'rail_axis');self.socket(p,'rail_R',(PITCH/2,0,RAIL_Z),0,'rail_axis')
    def posts(self):
        p=self.root('Chain_Line',STAGING['Chain_Line']);self.post(p,'Chain line post',0)
        for d in (0,180):self.socket(p,'connect_'+str(d),(0,0,0),d)
        for i,z in enumerate((.25,.55,.85,1.15)):self.wire_tie(p,'Chain line tie '+str(i),0,z,False)
        for name,dirs in [('Chain_Terminal',(0,)),('Chain_Terminal_End',(180,)),('Chain_Corner',(180,90))]:
            p=self.root(name,STAGING[name]);self.post(p,name+' post',0,True)
            for d in dirs:self.terminal_fittings(p,name+' '+str(d),0,d,.024 if name=='Chain_Corner' and d==90 else 0);self.socket(p,'connect_'+str(d),(0,0,0),d)
    def gate_frame(self,parent):
        w=LEAF-RAIL_OD;h=HEIGHT-RAIL_OD;zc=GROUND+HEIGHT/2;radius=.057
        path=G.rounded_rectangle(w,h,radius,8 if self.high else 3);vs=[];sides=24 if self.high else 10
        for i,(x,z) in enumerate(path):
            prev=Vector(path[i-1]);nxt=Vector(path[(i+1)%len(path)]);t=(nxt-prev).normalized();u=Vector((t.y,0,-t.x))
            for k in range(sides):vs.append(Vector((x,0,z+zc))+RAIL_OD/2*(u*math.cos(k*math.tau/sides)+Vector((0,1,0))*math.sin(k*math.tau/sides)))
        faces=[]
        for j in range(len(path)):
            for i in range(sides):faces.append((j*sides+i,j*sides+(i+1)%sides,((j+1)%len(path))*sides+(i+1)%sides,((j+1)%len(path))*sides+i))
        return self.attach(G.smooth(G.mesh('Chain gate welded frame',vs,faces,self.zinc),42),parent)
    def gate(self):
        p=self.root('Chain_GateBay',STAGING['Chain_GateBay']);self.socket(p,'L',(-GATE_PITCH/2,0,0),180);self.socket(p,'R',(GATE_PITCH/2,0,0))
        for s in (-1,1):
            self.post(p,'Chain gate '+('hinge' if s<0 else 'latch')+' post',s*GATE_PITCH/2,True)
            self.terminal_fittings(p,'Chain gate outside '+str(s),s*GATE_PITCH/2,180 if s<0 else 0)
        leaf=self.pivot(p,'Chain_Gate',(HINGE_X,HINGE_Y,0),'Z',(-110,0));before=set(bpy.context.scene.objects)
        self.gate_frame(p)
        # Straight bars and ties keep fabric off the rounded corner returns.
        for s in (-1,1):
            self.box(p,'Chain gate tension bar '+str(s),(s*(LEAF/2-.041),FABRIC_Y,GROUND+HEIGHT/2),(.015875,.0047625,HEIGHT-.0842),self.zinc,0)
            for i,z in enumerate((.20,.65,1.10)):
                self.wire_tie(p,f'Chain gate tie {s} {i}',s*(LEAF/2-RAIL_OD/2),z,False)
        self.fabric(p,'Chain_Gate_Fabric',-LEAF/2+.041,LEAF/2-.041,GROUND+.0381,GROUND+HEIGHT-.0381)
        self.reparent([o for o in set(bpy.context.scene.objects)-before if o.parent==p],leaf)
        for i,z in enumerate((.25,1.06)):
            self.ring(p,f'Chain hinge {i} post clamp',-GATE_PITCH/2,0,z-.027,TERM_OD/2+.002,.022,'Z',.002,12)
            self.box(p,f'Chain hinge {i} fixed arm',(-GATE_PITCH/2+.023,-.035,z-.027),(.060,.018,.010),self.zinc,.001)
            self.cyl(p,f'Chain hinge {i} pin',(HINGE_X,HINGE_Y,z-.040),(HINGE_X,HINGE_Y,z+.028),.004,8)
            sleeve=self.ring(p,f'Chain hinge {i} sleeve',HINGE_X,HINGE_Y,z,.008,.036,'Z',.0035,10);self.reparent([sleeve],leaf)
            collar=self.ring(p,f'Chain hinge {i} frame clamp',-LEAF/2+RAIL_OD/2,0,z,RAIL_OD/2+.002,.022,'Z',.002,10);self.reparent([collar],leaf)
            cx=-LEAF/2+RAIL_OD/2
            outline=[(HINGE_X+.0065,HINGE_Y-.005),(HINGE_X+.016,HINGE_Y-.005),(cx+.010,-.010),(cx+.010,.010),(cx-.008,.010),(cx-.008,-.002),(HINGE_X+.011,HINGE_Y+.005),(HINGE_X+.0065,HINGE_Y+.005)]
            neck=self.attach(G.profile(f'Chain hinge {i} moving arm',outline,z-.011,z+.011,self.zinc,axis='Z',radius=.0004 if self.high else 0,segments=2),p);self.reparent([neck],leaf)
        # Fork latch: two open jaws straddle the terminal, connected before it.
        before=set(bpy.context.scene.objects)
        self.box(p,'Chain latch fixed neck',(LEAF/2-.005,0,LATCH_Z),(.022,.018,.016),self.zinc,0)
        self.cyl(p,'Chain latch pin',(LATCH_X,-.052,LATCH_Z),(LATCH_X,.052,LATCH_Z),.004,8)
        self.reparent([o for o in set(bpy.context.scene.objects)-before if o.parent==p],leaf)
        latch=self.pivot(p,'Chain_ForkLatch',(LATCH_X,0,LATCH_Z),'Y',(-95,0));self.reparent([latch],leaf)
        before=set(bpy.context.scene.objects)
        for sy in (-1,1):
            self.ring(p,'Chain fork sleeve '+str(sy),LATCH_X,sy*.044,LATCH_Z,.0065,.006,'Y',.0022,10)
            pts=[(LATCH_X+.0055,LATCH_Z-.009),(GATE_PITCH/2+.043,LATCH_Z-.009),(GATE_PITCH/2+.049,LATCH_Z),(GATE_PITCH/2+.043,LATCH_Z+.009),(LATCH_X+.0055,LATCH_Z+.009)]
            self.attach(G.profile('Chain fork jaw '+str(sy),pts,sy*.044-.0015,sy*.044+.0015,self.zinc,axis='Y',radius=.0005 if self.high else 0,segments=2),p)
        self.box(p,'Chain fork bridge',(LATCH_X+.018,0,LATCH_Z),(.016,.088,.012),self.zinc,0)
        self.reparent([o for o in set(bpy.context.scene.objects)-before if o.parent==p],latch)
        self.socket(leaf,'free_edge',(LEAF/2-HINGE_X,-HINGE_Y,LATCH_Z),kind='gate_edge')
        # This prefab contains three reusable modules: two terminal posts and a
        # separate moving gate. Each has its own budget and isolated bake root.
        for s,label in [(-1,'Hinge'),(1,'Latch')]:
            postroot=self.root('Chain_GatePost_'+label,(0,0,0));postroot.parent=p;postroot.location=(s*GATE_PITCH/2,0,0)
            bpy.context.view_layer.update()
            members=[]
            for ob in list(p.children):
                if ob==postroot or ob.type!='MESH':continue
                if ('outside '+str(s)) in ob.name or ('gate '+('hinge' if s<0 else 'latch')+' post') in ob.name or (s<0 and ob.name.startswith('Chain hinge') and ('post clamp' in ob.name or 'fixed arm' in ob.name or ' pin' in ob.name)):
                    members.append(ob)
            self.reparent(members,postroot)
            self.socket(postroot,'outside',(0,0,0),180 if s<0 else 0)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--wear',type=float,default=.35);ap.add_argument('--quality',choices=['high','game'],default='high');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);b=Chain(a.quality=='high',a.wear)
    b.section('Chain_Start',True,False);b.section('Chain_EndSection',False,True);b.section('Chain_Section');b.section('Chain_BetweenTerminals',True,True);b.posts();b.gate()
    bpy.context.scene['quality']=a.quality;bpy.context.scene['asset']='ChainLink';bpy.context.scene.unit_settings.system='METRIC'
    bpy.context.view_layer.update();Path(a.out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
if __name__=='__main__':main()
