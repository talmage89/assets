"""Family construction helpers: grade origins, post-center sockets and hardware.

Shared by the two later fence types; the accepted privacy geometry is unchanged.
All dimensions are meters and all generated geometry is original.
"""
import math
import bpy
from mathutils import Vector
from kit import model as G

class Builder:
    def __init__(self,asset,high,wear):self.asset=asset;self.high=high;self.wear=wear
    def root(self,name,location):
        ob=G.pivot(name,location);ob['static_root']=True;ob['asset_set']=self.asset;return ob
    def socket(self,parent,name,location,yaw=0,kind='post_center'):
        ob=G.pivot(parent.name+'__'+name,(0,0,0));ob.parent=parent;ob.location=location
        ob.rotation_euler.z=math.radians(yaw);ob['socket_kind']=kind;return ob
    def frame(self,parent,name,start,axis=(0,0,1)):
        ob=G.pivot('Source frame '+name,(0,0,0));ob.parent=parent;ob.location=start
        ob.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();return ob
    def attach(self,ob,parent):
        bpy.context.view_layer.update();ob.matrix_world=parent.matrix_world@ob.matrix_world
        G.attach(ob,parent,asset_set=self.asset);bpy.context.view_layer.update();return ob
    def box(self,parent,name,center,size,mat,bevel=.0005):
        return self.attach(G.box(name,center,size,mat,bevel if self.high else 0,2),parent)
    def reparent(self,objects,parent):
        bpy.context.view_layer.update()
        for ob in objects:
            world=ob.matrix_world.copy();ob.parent=parent;ob.matrix_world=world
        bpy.context.view_layer.update()
    def pivot(self,parent,name,location,axis,limits):
        ob=G.pivot(name,(0,0,0),axis,limits);ob.parent=parent;ob.location=location
        bpy.context.view_layer.update();return ob
    def strap_hardware(self,parent,leaf,mat,width,pitch,post,rail_z,hinge_x,hinge_y,skin_y,latch_z):
        """Bent straps on hollow sleeves, fixed pins and a released gravity latch."""
        for i,z in enumerate(rail_z):
            stem=f'{leaf.name} hinge {i+1}'
            self.box(parent,stem+' backing',(-pitch/2,-post/2-.0015,z),(.074,.003,.061),mat)
            self.attach(G.cylinder(stem+' pin',(hinge_x,hinge_y,z-.041),(hinge_x,hinge_y,z+.041),.0035,mat,16 if self.high else 8),parent)
            for dz in (-.032,.032):self.box(parent,stem+' neck '+str(dz),(hinge_x-.019,-.049,z+dz),(.044,.010,.013),mat,0)
            pts=[(hinge_x+.0046,hinge_y-.006),(hinge_x+.016,hinge_y-.006),(-width/2+.043,skin_y-.0035),
                 (-width/2+.265,skin_y-.0035),(-width/2+.28,skin_y),(-width/2+.265,skin_y),
                 (-width/2+.036,skin_y),(hinge_x+.012,hinge_y+.006),(hinge_x+.0046,hinge_y+.006)]
            ob=self.attach(G.profile(stem+' strap',pts,z-.018,z+.018,mat,axis='Z',radius=.0003 if self.high else 0,segments=2),parent);self.reparent([ob],leaf)
            ob=self.attach(G.lathe(stem+' sleeve',[(z-.024,.0039),(z-.024,.0065),(z+.024,.0065),(z+.024,.0039)],mat,24 if self.high else 8,center=(hinge_x,hinge_y),closed=True),parent);self.reparent([ob],leaf)
            if self.high:
                for xx in (-pitch/2,-width/2+.065,-width/2+.24):
                    fast=self.high_fastener(parent,stem+' screw',(xx,(-post/2-.003 if xx< -width/2 else skin_y-.004),z),(0,-1,0),mat,.0035)
                    if xx>-width/2:self.reparent(fast,leaf)
        lx=width/2-.065;y=skin_y-.016
        backing=self.box(parent,leaf.name+' latch backing',(lx,skin_y-.002,latch_z),(.05,.004,.08),mat)
        pin=self.attach(G.cylinder(leaf.name+' latch pin',(lx,skin_y-.004,latch_z),(lx,y+.003,latch_z),.0045,mat,16 if self.high else 8),parent)
        self.reparent([backing,pin],leaf)
        latch=self.pivot(parent,leaf.name+'_Latch',(lx,y,latch_z),'Y',(-65,0));self.reparent([latch],leaf)
        bar=G.profile(leaf.name+' lifting latch',[(0,-.010),(.1,-.010),(.11,0),(.11,.010),(0,.010)],-.002,.002,mat,axis='Y',radius=.0004 if self.high else 0,segments=2)
        bar.location=(lx,y,latch_z);self.attach(bar,parent);self.reparent([bar],latch)
        self.box(parent,leaf.name+' strike backing',(pitch/2,-post/2-.0015,latch_z),(.060,.003,.075),mat)
        xx=width/2+.031
        self.box(parent,leaf.name+' strike seat',(xx,y+.006,latch_z-.012),(.028,.017,.004),mat,0)
        self.box(parent,leaf.name+' retaining tab',(xx,y-.004,latch_z-.002),(.028,.003,.024),mat,0)
        return latch
    def high_fastener(self,parent,name,center,axis,mat,radius=.003):
        obs=G.fastener(name,center,axis,mat,radius,True,kind='cross',washer=False)
        return [self.attach(ob,parent) for ob in obs]
