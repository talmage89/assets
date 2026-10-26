"""Deterministic, measured privacy kit. Run from a factory-startup Blender."""
import argparse, math, random, sys
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from kit import model as G, materials as M
from dimensions import *
SET='WoodPrivacy'


def root(name,loc):
    ob=G.pivot(name,loc);ob['static_root']=True;ob['asset_set']=SET
    return ob


def socket(parent,name,loc,kind='post_center',yaw=0):
    ob=G.pivot(parent.name+'__'+name,(0,0,0));ob.parent=parent;ob.location=loc
    ob.rotation_euler.z=math.radians(yaw);ob['socket_kind']=kind
    return ob


def frame(parent,name,center,axis=(0,0,1)):
    ob=G.pivot('Source frame '+name,(0,0,0));ob.parent=parent;ob.location=center
    ob.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    return ob


def attach_local(ob,parent,part=None):
    # All authored coordinates are in a module's frame; attach applies transforms.
    bpy.context.view_layer.update();ob.matrix_world=parent.matrix_world@ob.matrix_world
    G.attach(ob,parent,asset_set=SET)
    bpy.context.view_layer.update()
    if part:ob['export_part']=part
    return ob


def timber(parent,name,center,size,seed,high,wear,axis=(0,0,1),nails=(),dog=False):
    length=size[2] if dog else max(size)
    # Keep each timber's meter coordinates when the baker consolidates geometry.
    center=Vector(center);direction=Vector(axis)
    start=center-direction*length/2
    f=frame(parent,name,start,axis)
    mat=M.weathered_wood(name+' pine',f,width=size[0] if dog else min(size[:2]),
                         length=length,seed=seed,wear=wear,nail_rows=nails,ground_frame=parent)
    if dog:
        w,h=size[0],size[2];e=.0185
        pts=[(-w/2,0),(w/2,0),(w/2,h-e),(w/2-e,h),(-w/2+e,h),(-w/2,h-e)]
        ob=G.profile(name,pts,center.y-THICK/2,center.y+THICK/2,mat,axis='Y',radius=.00065 if high else 0,segments=2)
        for v in ob.data.vertices:v.co.x+=center.x;v.co.z+=center.z-h/2
    else:ob=G.box(name,center,size,mat,.0011 if high else 0,2)
    attach_local(ob,parent)
    ob['timber']=True;ob['construction_role']='picket' if dog else 'frame'
    return ob


def brackets(parent,x,sign,high,metal):
    """Three folded saddles: rear web against post, two cheeks, bottom seat."""
    for j,z in enumerate(RAILS):
        # x is the post face. Positive sign points from the post into this bay.
        stem=f'{parent.name} saddle {sign:+} {j+1}'
        pieces=[('web',(x+sign*.0005,0,z),(.001,.0401,RAIL_H+.002)),
                ('seat',(x+sign*.0105,0,z-RAIL_H/2-.0005),(.019,.0401,.001))]
        for sy in (-1,1):pieces.append(('cheek',(x+sign*.0105,sy*.01955,z),(.019,.001,RAIL_H)))
        for suffix,center,size in pieces:
            attach_local(G.box(stem+' '+suffix,center,size,metal,.00015 if high else 0,1),parent)
        if high:
            for sy in (-1,1):
                for dz in (-.025,.025):
                    for ob in G.fastener(stem+' screw',(x+sign*.012,sy*.0201,z+dz),(0,sy,0),metal,.0028,True,kind='cross',washer=False):attach_local(ob,parent)


def section(name,seed,high,wear):
    p=root(name,STAGING[name]);rng=random.Random(seed)
    clear=PITCH-POST;count=17
    # 15 full-width interior pickets, two symmetrical rip-cut edge pickets.
    edge=(clear-15*WIDTH-(count-1)*GAP)/2
    cursor=-clear/2
    for i,w in enumerate([edge]+[WIDTH]*15+[edge]):
        x=cursor+w/2;cursor+=w+GAP
        dz=rng.uniform(-.0013,.0013) if i not in (0,16) else 0
        timber(p,f'{name} picket {i+1:02}',(x,-RAIL_T/2-THICK/2,GROUND+HEIGHT/2+dz),(w,THICK,HEIGHT),seed*100+i,high,wear,
               nails=tuple(z-GROUND-dz for z in RAILS),dog=True)
    for i,z in enumerate(RAILS):
        timber(p,f'{name} rail {i+1}',(0,0,z),(clear-.014,RAIL_T,RAIL_H),seed*10+i,high,wear,axis=(1,0,0))
    metal=M.galvanized(name+' zinc',None,wear)
    brackets(p,-clear/2,1,high,metal);brackets(p,clear/2,-1,high,metal)
    socket(p,'L',(-PITCH/2,0,0),yaw=180);socket(p,'R',(PITCH/2,0,0))
    for side in (-1,1):
        for i,z in enumerate(RAILS):socket(p,f'rail_{"L" if side<0 else "R"}_{i+1}',(side*clear/2,0,z),'rail_face')
    return p


def postmesh(parent,name,x,seed,high,wear):
    # Low bevel-top profile sheds water and preserves actual dressed section.
    f=frame(parent,name,(x,0,0));mat=M.weathered_wood(name+' pine',f,POST,POST_TOP,seed,wear,ground_frame=parent)
    r=POST/2;c=.005
    loops=[[(x+u,v,z) for u,v in [(-r,-r),(r,-r),(r,r),(-r,r)]] for z in (0,POST_TOP-c)]
    loops.append([(x+u,v,POST_TOP) for u,v in [(-r+c,-r+c),(r-c,-r+c),(r-c,r-c),(-r+c,r-c)]])
    ob=G.loft(name,loops,mat);G.bevel(ob,.00065 if high else 0,2)
    attach_local(ob,parent);ob['construction_role']='post';return ob


def posts(high,wear):
    for i,(name,dirs) in enumerate([('Post_End',(0,)),('Post_Line',(0,180)),('Post_Corner',(180,90))]):
        p=root(name,STAGING[name]);postmesh(p,name+' timber',0,700+i,high,wear)
        for angle in dirs:
            rad=math.radians(angle)
            socket(p,'connect_'+str(angle),(0,0,0),yaw=angle)
            for j,z in enumerate(RAILS):socket(p,f'face_{angle}_{j+1}',(POST/2*math.cos(rad),POST/2*math.sin(rad),z),'rail_face',angle)


def gate(high,wear):
    p=root('Gate_Bay',STAGING['Gate_Bay']);metal=M.galvanized('Gate hardware zinc',None,wear)
    for s in (-1,1):postmesh(p,'Gate '+('hinge' if s<0 else 'latch')+' post',s*GATE_PITCH/2,802+s,high,wear)
    socket(p,'L',(-GATE_PITCH/2,0,0),yaw=180);socket(p,'R',(GATE_PITCH/2,0,0))
    leaf=G.pivot('Gate',tuple(Vector(STAGING['Gate_Bay'])+Vector((HINGE_X,HINGE_Y,0))),'Z',(-110,0))
    leaf.parent=p;leaf.location=(HINGE_X,HINGE_Y,0)
    # Author gate wood in bay coordinates, then rebase to the true hinge axis.
    def reparent_since(before,new_parent):
        for ob in set(bpy.context.scene.objects)-before:
            if ob.parent==p:
                world=ob.matrix_world.copy();ob.parent=new_parent;ob.matrix_world=world
    before=set(bpy.context.scene.objects)
    n=7;w=(LEAF-(n-1)*GAP)/n
    for i in range(n):
        timber(p,f'Gate picket {i+1}',(-LEAF/2+w/2+i*(w+GAP),-RAIL_T/2-THICK/2,GROUND+HEIGHT/2),(w,THICK,HEIGHT),850+i,high,wear,
               nails=tuple(z-GROUND for z in RAILS),dog=True)
    stile_w=.0635
    for s in (-1,1):timber(p,f'Gate stile {s}',(s*(LEAF/2-stile_w/2),0,(RAILS[0]+RAILS[-1])/2),(stile_w,RAIL_T,RAILS[-1]-RAILS[0]+RAIL_H),882+s,high,wear)
    for i,z in enumerate(RAILS):timber(p,f'Gate rail {i+1}',(0,0,z),(LEAF-2*stile_w,RAIL_T,RAIL_H),890+i,high,wear,axis=(1,0,0))
    # Two bearing-cut compression braces, lower hinge to upper latch.
    for i,(za,zb) in enumerate(zip(RAILS[:-1],RAILS[1:])):
        x0=-LEAF/2+stile_w;x1=LEAF/2-stile_w
        lo=za+RAIL_H/2;hi=zb-RAIL_H/2
        # Angled ends bear on rail edges; coplanar with gate rails, not floating on rear.
        bw=.073
        pts=[(x0,lo),(x0+bw,lo),(x1,hi),(x1-bw,hi)]
        center=Vector(((x0+x1)/2,0,(lo+hi)/2));length=Vector((x1-x0,0,hi-lo)).length
        f=frame(p,'Gate brace '+str(i),center-Vector((x1-x0,0,hi-lo)).normalized()*length/2,(x1-x0,0,hi-lo))
        mat=M.weathered_wood('Gate brace '+str(i)+' pine',f,bw,length,920+i,wear,ground_frame=p)
        ob=G.profile('Gate compression brace '+str(i+1),pts,-RAIL_T/2,RAIL_T/2,mat,axis='Y',radius=.0007 if high else 0,segments=2);attach_local(ob,p)
    bpy.context.view_layer.update();reparent_since(before,leaf)
    # Two actual hollow sleeve/pin hinges with bent strap necks.
    for i,z in enumerate((RAILS[0],RAILS[-1])):
        base=f'Gate hinge {i+1}'
        attach_local(G.box(base+' fixed leaf',(-GATE_PITCH/2,-POST/2-.0015,z),(.074,.003,.061),metal,.0003 if high else 0,2),p)
        attach_local(G.cylinder(base+' fixed pin',(HINGE_X,HINGE_Y,z-.041),(HINGE_X,HINGE_Y,z+.041),.0035,metal,16 if high else 8),p)
        # Fixed barrel carried on a neck from the stationary plate.
        for dz in (-.032,.032):
            attach_local(G.box(base+' fixed neck',(HINGE_X-.019,-.049,z+dz),(.044,.010,.013),metal,0),p)
        pts=[(HINGE_X+.0046,HINGE_Y-.006),(HINGE_X+.016,HINGE_Y-.006),(-LEAF/2+.043,-.038425),
             (-LEAF/2+.245,-.038425),(-LEAF/2+.260,-.031),( -LEAF/2+.245,-.034925),
             (-LEAF/2+.036,-.034925),(HINGE_X+.012,HINGE_Y+.006),(HINGE_X+.0046,HINGE_Y+.006)]
        before=set(bpy.context.scene.objects)
        attach_local(G.profile(base+' moving strap',pts,z-.018,z+.018,metal,axis='Z',radius=.0003 if high else 0,segments=2),p)
        sleeve=G.lathe(base+' moving sleeve',[(z-.024,.0039),(z-.024,.0065),(z+.024,.0065),(z+.024,.0039)],metal,24 if high else 8,center=(HINGE_X,HINGE_Y),closed=True)
        attach_local(sleeve,p)
        bpy.context.view_layer.update();reparent_since(before,leaf)
        if high:
            for xx in (-GATE_PITCH/2,-LEAF/2+.065,-LEAF/2+.185):
                before=set(bpy.context.scene.objects)
                for ob in G.fastener(base+' mounting screw',(xx,-.039 if xx>-OPENING/2 else -.048,z),(0,-1,0),metal,.004,True,kind='cross',washer=False):attach_local(ob,p)
                if xx>-OPENING/2:
                    bpy.context.view_layer.update();reparent_since(before,leaf)
    # Gravity latch lifts at the gate edge, clear of the stationary receiving tab.
    before=set(bpy.context.scene.objects)
    attach_local(G.cylinder('Gate latch pivot stand-off',(.375,-.039,1.12),(.375,-.048,1.12),.0055,metal,16 if high else 8),p)
    attach_local(G.box('Gate latch backing',(.375,-.037,1.12),(.055,.004,.090),metal,.001 if high else 0,2),p)
    bpy.context.view_layer.update();reparent_since(before,leaf)
    latch=G.pivot('Latch',tuple(Vector(STAGING['Gate_Bay'])+Vector((.375,-.051,1.12))),'Y',(-65,0))
    bpy.context.view_layer.update()
    world=latch.matrix_world.copy();latch.parent=leaf;latch.matrix_world=world
    bar=G.profile('Latch lifting bar',[(0,-.012),(.097,-.012),(.108,-.003),(.108,.012),(0,.012)],-.003,.003,metal,axis='Y',radius=.0005 if high else 0,segments=2)
    bar.location=(.375,-.051,1.12)
    attach_local(bar,p)
    world=bar.matrix_world.copy();bar.parent=latch;bar.matrix_world=world
    for ob in G.fastener('Latch pivot',(.375,-.054,1.12),(0,-1,0),metal,.0045,high,kind='hex',washer=high):
        attach_local(ob,p);world=ob.matrix_world.copy();ob.parent=leaf;ob.matrix_world=world
    attach_local(G.box('Latch strike backing',(GATE_PITCH/2,-POST/2-.0015,1.12),(.060,.003,.075),metal,.0005 if high else 0,2),p)
    # Keeper is open above, catching the lowered bar's front edge.
    attach_local(G.box('Latch strike seat',(.477,-.047,1.105),(.028,.017,.004),metal,0),p)
    attach_local(G.box('Latch strike retaining tab',(.477,-.057,1.115),(.028,.003,.024),metal,0),p)
    socket(leaf,'free_edge',((LEAF/2)-HINGE_X,-HINGE_Y,1.12),'gate_edge')
    return p


def main():
    a=argparse.ArgumentParser();a.add_argument('--out',required=True);a.add_argument('--wear',type=float,default=.65);a.add_argument('--quality',default='high',choices=['high','game']);args=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    high=args.quality=='high'
    section('Section_A',41,high,args.wear);section('Section_B',97,high,args.wear);posts(high,args.wear);gate(high,args.wear)
    sc=bpy.context.scene;sc['quality']=args.quality;sc['asset']='WoodPrivacy';sc.unit_settings.system='METRIC'
    bpy.context.view_layer.update();Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(args.out).resolve()))
    print('BUILT',args.quality,len(sc.objects),'objects')

if __name__=='__main__':main()
