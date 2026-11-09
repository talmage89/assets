"""Period Type III bridge using main's shared freeway construction factories.

The smaller section is from FDOT 20130. Local +X is bridge station.
"""
import math
import bpy
import geometry as G
from plan import FT
import freeway_bridge as shared


class Batch(G.Batch):
    def geom(self,vs,fs,role='concrete',*args,**kwargs):
        return super().geom(vs,fs,'bridge_concrete' if role=='concrete' else role,*args,**kwargs)

# FDOT 20130: bottom-to-top 7 / 7.5 / 19 / 4.5 / 7 in zones.
# 45 in total, 16 in top, 22 in bottom, 7 in web; .75in foot chamfers.
SECTION=[(-.26035,0),(.26035,0),(.2794,.01905),(.2794,.1778),
         (.0889,.3683),(.0889,.8509),(.2032,.9652),(.2032,1.143),
         (-.2032,1.143),(-.2032,.9652),(-.0889,.8509),(-.0889,.3683),
         (-.2794,.1778),(-.2794,.01905)]


def girder(name,length=18.0086,parent=None):
    return shared.girder(name,length,SECTION,parent)


def pier(name,width=11.8872,kind='columns',height=2.11,parent=None,flow_angle=0):
    if kind=='columns':return shared.columns(name,width,height,parent)
    rt=G.root(name,parent=parent,module='Pier_'+kind)
    b=Batch(name+'__Substructure',rt)
    # Datum is waterline. Buried footings stop below exposed bed.
    if kind=='wall':
        # Skew the submerged stem with local flow, leaving the bearing cap
        # transverse to the bridge. Angle is radians about local +Z.
        def flow_point(x,y,z):
            c,s=math.cos(flow_angle),math.sin(flow_angle)
            return (c*x-s*y,s*x+c*y,z)
        w=.65;length=width*.83
        sec=[(w,-length/2+.65),(w,length/2-.65)]
        sec += [(w*math.cos(t),length/2-.65+w*math.sin(t)) for t in [i*math.pi/8 for i in range(1,9)]]
        sec += [(-w,-length/2+.65)]
        sec += [(w*math.cos(t),-length/2+.65+w*math.sin(t)) for t in [math.pi+i*math.pi/8 for i in range(1,9)]]
        b.loft([[flow_point(x,y,z) for x,y in sec] for z in (-1.4,-.15,.1,1.25,height-.8)])
        b.loft([[flow_point(x,y,z) for x,y in ((-1.125,-(length+1)/2),(1.125,-(length+1)/2),(1.125,(length+1)/2),(-1.125,(length+1)/2))] for z in (-1.725,-1.375)])
    # Chamfered cap section, extruded in the transverse direction.
    sec=[(-.86,height-.70),(-.76,height-.80),(.76,height-.80),(.86,height-.70),(.86,height-.08),(.78,height),(-.78,height),(-.86,height-.08)]
    b.loft([[(x,y,z) for x,z in sec] for y in (-width/2+.3,width/2-.3)])
    b.finish();return rt


def abutment(name,width=11.8872,parent=None,seat=2.687,top=4.13):
    rt=G.root(name,parent=parent,module='Abutment',seat_z_m=seat)
    b=Batch(name+'__Retaining',rt)
    # Bridge is to local -X; wingwalls contain the approach embankment.
    b.box((.40,0,(seat-.80)/2),(.80,width,seat))
    # The seat projects toward the span under the bearing plinths. The old
    # stem-only box ended behind their centers, leaving pads unsupported.
    b.box((.125,0,seat-.20),(1.85,width,.40))
    b.box((.82,0,(seat+top)/2),(.40,width,top-seat))
    b.box((.30,0,-.40),(1.8,width+.6,.35))
    for s in (-1,1):
        rings=[]
        for x,wing_top in ((.8,top),(3.2,top+.32),(6.3,top+.32)):
            center=s*(width/2+math.tan(math.radians(30))*(x-.8))
            rings.append([(x,center+offset,z) for offset,z in ((-.17,-.4),(.17,-.4),(.17,wing_top),(-.17,wing_top))])
        b.loft(rings)
        b.beam((.8,s*width/2,-.50),(6.3,s*(width/2+math.tan(math.radians(30))*5.5),-.50),.8,.35,'concrete')
    b.finish();return rt


def parapet(name,length=6.096,parent=None):
    return shared.parapet(name,length,parent)


def deck(name,length=6.096,width=11.8872,parent=None,scuppers=(0,)):
    rt=G.root(name,parent=parent,module='DeckPanel')
    b=Batch(name+'__Slab',rt)
    lane=3.3528;edge=-.06-.02*lane
    section=[(-width/2,-.32),(width/2,-.32),(width/2,edge),(lane,edge),(0,-.06),(-lane,edge),(-width/2,edge)]
    b.loft([[(x,y,z) for y,z in section] for x in (-length/2,length/2)])
    # Asphalt crowned at 2%; walks are integral raised curbs.
    for s in (-1,1):
        vs=[(x,y,.00-.02*abs(y)) for x,y in ((-length/2,0),(length/2,0),(length/2,s*lane),(-length/2,s*lane))]
        b.geom(vs,[(0,1,2,3)],'asphalt')
        cuts=sorted([-length/2,length/2]+[x+off for x in scuppers for off in (-.18,.18)])
        for a,c in zip(cuts,cuts[1:]):
            if any(abs((a+c)/2-x)<.18 for x in scuppers):continue
            b.box(((a+c)/2,s*(lane+.1524/2),(edge+.085344)/2),(c-a,.1524,.085344-edge))
        walkwidth=width/2-lane-.1524
        b.box((0,s*(lane+.1524+walkwidth/2),(edge+.085344)/2),(length,walkwidth,.085344-edge))
        b.box((0,s*(width/2-.23),-.327),(length,.018,.018),'rubber')
    ob=b.finish()
    for x in scuppers:
        for side in (-1,1):
            cutter=G.model.box('Scupper opening cutter',(x,side*(lane+.0762),-.2),(.36,.22,1),G.M['bridge_concrete'],0)
            G.model.boolean(ob,cutter)
    mod=ob.modifiers.new('Final drain triangles','TRIANGULATE');G.model.apply(ob)
    return rt


def guardrail(name,length=7.62,parent=None):
    return shared.guardrail(name,length,parent)


def assemble(p,parent):
    rt=G.root('Bridge',parent=parent,bridge_plan=p.data());n=5
    # Keep the deck overhang at 0.95m to the outer girder centerline;
    # spreading five girders across the roadway avoids a 1.9m cantilever.
    outer=p.deck_width/2-.95
    ys=[-outer+i*2*outer/(n-1) for i in range(n)]
    soffit=p.deck_z-.32;bottom=soffit-1.143;seat=bottom-.30
    for i in range(p.spans):
        a=-p.length/2+i*p.span;c=a+p.span
        for j,y in enumerate(ys):
            ob=girder(f'Girder_{i}_{j}',p.span-.28,rt);ob.location=((a+c)/2,y,bottom)
        d=Batch(f'Span_{i}__DiaphragmsHaunches',rt)
        for x in (a+.48,(a+c)/2,c-.48):
            for ya,yb in zip(ys,ys[1:]):d.box((x,(ya+yb)/2,bottom+.69),(.22,yb-ya-.178,.75))
        for y in ys:d.box(((a+c)/2,y,soffit+.02),(p.span-.28,.41,.04))
        d.finish()
        for k in range(3):
            panel_len=(p.span-.04)/3;center=a+.02+(k+.5)*panel_len
            openings=[xx-center for xx in (a+p.span*.28,a+p.span*.73) if abs(xx-center)<panel_len/2-.18]
            panel=deck(f'Deck_{i}_{k}',panel_len,p.deck_width,rt,openings)
            panel.location=(center,0,p.deck_z)
        for side in (-1,1):
            for j in range(3):
                ob=parapet(f'Parapet_{i}_{side}_{j}',p.span/3-.016,rt)
                ob.location=(a+(j+.5)*p.span/3,side*(p.deck_width/2-.3048),p.deck_z+.085344)
        # Each 8m scupper drains through a real gutter gap into a downpipe.
        drain=Batch(f'Span_{i}__DrainConduit',rt)
        for side in (-1,1):
            for x in (a+p.span*.28,a+p.span*.73):
                y=side*(3.3528+.0762)
                # Open cast trough directly below the actual curb notch.
                for dx in (-.18,.18):drain.box((x+dx,y,p.deck_z-.15),(.008,.22,.18),'steel')
                for dy in (-.11,.11):drain.box((x,y+dy,p.deck_z-.15),(.36,.008,.18),'steel')
                drain.tube([(x,y,p.deck_z-.24),(x,y,p.deck_z-.67),(x,side*(p.deck_width/2+.12),p.deck_z-.74),(x,side*(p.deck_width/2+.12),p.deck_z-1.28)],.055,'steel',8,thickness=.004)
            y=side*(p.deck_width*.31)
            drain.tube([(a+.15,y,soffit-.23),(c-.15,y,soffit-.23)],.048,'steel',8)
            for x in (a+2,a+7,c-2):
                drain.tube([(x,y-.12,soffit),(x,y-.12,soffit-.30),(x,y+.12,soffit-.30),(x,y+.12,soffit)],.008,'steel',6)
        drain.finish()
    for i in range(p.spans+1):
        x=-p.length/2+i*p.span
        if i in (0,p.spans):
            ob=abutment('Abutment_'+str(i),p.deck_width,rt,seat,soffit)
            ob.location.x=x;ob.rotation_euler.z=math.pi if i==0 else 0
        else:
            tx,ty=p.tangent(0)
            ob=pier('Pier_'+str(i),p.deck_width,p.pier,seat,rt,flow_angle=math.atan2(-tx,ty));ob.location.x=x
        b=Batch('BearingStation_'+str(i),rt)
        for y in ys:
            offsets=(.40,-.40) if 0<i<p.spans else ((.40,) if i==0 else (-.40,))
            for dx in offsets:
                shared.bearing(b,x+dx,y,seat)
        b.box((x,0,p.deck_z-.04),(.035,6.72,.04),'rubber')
        for dx in (-.033,.033):b.box((x+dx,0,p.deck_z-.039),(.025,6.72,.008),'steel')
        b.finish()
    for s in (-1,1):
        b=Batch('ApproachSlab_'+str(s),rt)
        b.box((s*(p.length/2+2),0,p.deck_z-.18),(4,p.deck_width,.28));b.finish()
        for side in (-1,1):
            ob=guardrail(f'ApproachRail_{s}_{side}',parent=rt)
            ob.location=(s*(p.length/2+4),side*(p.deck_width/2-.20),p.deck_z-.02*3.3528-.008)
            ob.scale.x=s
            ob.scale.y=side
    # Preserve the native rail profile and top datum. Only the buried post
    # tips follow actual triangulated soil, which differs from an analytic
    # bank formula near a retaining-wall transition.
    from channel import surface_z
    bpy.context.view_layer.update()
    for root in [o for o in rt.children if o.name.startswith('ApproachRail_')]:
        for ob in G.descendants(root):
            if ob.type!='MESH':continue
            low=min(v.co.z for v in ob.data.vertices);inv=ob.matrix_world.inverted()
            tips=ob.data.attributes.new('_GROUND_TIP',type='FLOAT',domain='POINT')
            for v,tag in zip(ob.data.vertices,tips.data):
                if abs(v.co.z-low)>1e-5:continue
                world=ob.matrix_world@v.co;world.z=surface_z(p,world.x,world.y)-.005
                v.co=inv@world;tag.value=1
            ob.data.update()
    if p.kind=='downtown':
        plinths=Batch('ParapetLightPedestals',rt)
        for side in (-1,1):
            for x in (-17,17):
                plinths.box((x,side*(p.deck_width/2-.3048),p.deck_z+.492672),(.65,.6096,.814656))
        plinths.finish()
    for y in (-1.6764,1.6764):
        pts=[(-120+i*4,y,p.deck_z-.02*abs(y)+.008) for i in range(61)]
        if y>0:pts.reverse()
        G.path('Lane_'+str(y),pts,rt,'drive',speed_m_s=11.176)
    for y in (-4.2672,4.2672):G.path('Sidewalk_'+str(y),[(x,y,p.deck_z+.085344) for x in (-120,120)],rt,'walk')
    return rt
