"""Authored architectural profiles in meters; silhouettes, not copied catalog art.

Folded cornice shells, cast hollow brackets, washed stone, and cast storefront
supports. Fine tooling/fluting and sheet seam relief live in the shared trim.
"""
import math


def sweep(b,x0,x1,profile,z=0,role='Finish',color=None):
    # Profile ordered around a closed YZ section. End plates close the sweep.
    b.prism([(x0,y,z+zz) for y,zz in profile],(x1-x0,0,0),role,color)


def molding(b,x0,x1,z,projection=.22,height=.16,role='Finish',color=None):
    # Cyma reversa / bead / fillet, a formed sheet return into its backing.
    p=[(.025,0),(-projection*.40,0),(-projection*.44,height*.14),
       (-projection*.48,height*.22),(-projection*.70,height*.33),
       (-projection*.90,height*.48),(-projection,height*.72),
       (-projection,height),(.025,height)]
    sweep(b,x0,x1,p,z,role,color)


def sill(b,x,w,z,color):
    # 1:8 wash falls toward nose, with an undercut drip 25 mm behind it.
    p=[(.22,-.14),(-.16,-.14),(-.19,-.12),(-.19,-.075),
       (-.215,-.075),(-.215,-.12),(-.25,-.12),(-.25,-.025),(.22,.030)]
    sweep(b,x-w/2-.12,x+w/2+.12,p,z,'Mineral',color)
    molding(b,x-w/2-.04,x+w/2+.04,z-.20,.12,.06,'Mineral',color)


def hood(b,x,w,hi,rise,color):
    # Cast hood with shouldered ears, broken segmental pediment and keystone.
    a=x-w/2-.14;c=x+w/2+.14;spring=hi+.05
    for xx in (a+.05,c-.05):
        b.box((xx,-.075,hi-.035),(.13,.19,.32),'Finish',color)
        # Small side consoles carry the hood ends, hooked return silhouette.
        profile=[(.012,-.27),(-.10,-.27),(-.135,-.20),(-.11,-.13),(-.17,-.07),(-.23,-.03),(-.23,.05),(.012,.05)]
        sweep(b,xx-.06,xx+.06,profile,hi,'Finish',color)
    # Multi-step hood section swept over a shallow peaked/segmental head.
    section=[(.03,0),(-.085,0),(-.11,.025),(-.10,.055),(-.17,.08),(-.19,.115),(-.18,.145),(.03,.145)]
    n=10;vs=[]
    for j in range(n+1):
        t=j/n;xx=a+(c-a)*t;zz=spring+rise*4*t*(1-t)
        vs.extend((xx,y,zz+dz) for y,dz in section)
    k=len(section);fs=[]
    for j in range(n):
        for i in range(k):fs.append((j*k+i,j*k+(i+1)%k,(j+1)*k+(i+1)%k,(j+1)*k+i))
    fs += [tuple(reversed(range(k))),tuple(range(n*k,(n+1)*k))]
    b.geom(vs,fs,'Finish',color)
    # Raised fan tympanum and a projecting tapered key; no flat arched strip.
    b.prism([(a+.12,-.045,spring+.12),(c-.12,-.045,spring+.12),(x,-.045,spring+rise+.15)],(0,.05,0),'Finish',tuple(v*.90 for v in color))
    b.prism([(x-.075,-.215,spring+rise-.03),(x+.075,-.215,spring+rise-.03),
             (x+.12,-.215,spring+rise+.22),(x-.12,-.215,spring+rise+.22)],(0,.17,0),'Finish',color)


def bracket(b,x,z,color,width=.085):
    # Low cage with a changing section: broad rolled volute face, narrow neck.
    profile=[(.015,-.69),(-.11,-.69),(-.17,-.66),(-.19,-.61),
             (-.18,-.56),(-.145,-.52),(-.12,-.47),(-.15,-.41),
             (-.25,-.36),(-.37,-.31),(-.46,-.25),(-.49,-.18),
             (-.47,-.11),(-.43,-.085),(-.37,-.10),(-.35,-.14),
             (-.37,-.18),(-.40,-.18),(-.41,-.15),(-.39,-.13),
             (-.34,-.10),(-.30,-.075),(.015,-.075)]
    sweep(b,x-width/2,x+width/2,profile,z,'Finish',color)
    # Front rib, rounded lower boss. Side small curls are baked into strip 5.
    b.tube([(x,-.17,z-.60),(x,-.19,z-.60)],.048,color=color,n=8)


def cornice(b,L,top,color,heavy=False):
    scale=1.16 if heavy else 1.0
    molding(b,0,L,top-.78,.20,.10,color=color)
    sweep(b,0,L,[(.035,-.69),(-.055,-.69),(-.055,-.22),(.035,-.22)],top,color=color)
    molding(b,-.045,L+.045,top-.26,.46*scale,.18,color=color)
    # Rolled crown, overhanging drip and the 1.2 mm folded top weathering cover.
    sweep(b,-.065,L+.065,[(.06,-.08),(-.53*scale,-.08),(-.61*scale,-.045),
        (-.61*scale,.025),(-.57*scale,.045),(-.53*scale,.015),(.06,.015)],top,color=color)
    n=max(3,round(L/1.32));step=L/n
    for j in range(n+1):
        xx=.19+(L-.38)*j/n
        # Paired scrolls, separated sufficiently to throw individual shadows.
        for off in (-.085,.085):bracket(b,xx+off,top,color)
    for j in range(n):
        cx=(j+.5)*step
        b.surface='frieze'
        b.box((cx,-.068,top-.49),(step-.43,.028,.22),'Finish',tuple(v*.88 for v in color))
        b.surface=None
        # Frieze field raised border, not a solid box face.
        for dz in (-.12,.12):b.box((cx,-.09,top-.49+dz),(step-.39,.035,.025),'Finish',color)
        for dx in (-(step-.40)/2,(step-.40)/2):b.box((cx+dx,-.09,top-.49),(.025,.035,.23),'Finish',color)
    for j in range(round(L/.17)):
        xx=(j+.5)*L/round(L/.17)
        b.box((xx,-.29,top-.235),(.065,.16,.092),'Finish',color)
    for j in range(round(L/.42)):
        xx=(j+.5)*L/round(L/.42)
        b.box((xx,-.365,top-.14),(.075,.27,.065),'Finish',color)


def pilaster(b,x,y,head,col):
    # Cast pilaster supported by a square base, with stepped collar and capital.
    for zz,ww,dd,hh in ((.07,.28,.36,.14),(.19,.23,.31,.10),(.31,.205,.28,.14),
                         (head-.36,.225,.34,.09),(head-.25,.29,.39,.12),
                         (head-.13,.34,.42,.11)):
        b.box((x,y,zz),(ww,dd,hh),'Finish',col)
    # Slight shaft entasis with chamfered corners rather than a rectangular pier.
    rings=[(.38,.091),(head*.40,.098),(head-.42,.086)];vs=[]
    for zz,r in rings:
        for j in range(8):
            t=math.tau*(j+.5)/8;vs.append((x+r*math.cos(t),y+.005+.135*math.sin(t),zz))
    fs=[(k*8+j,k*8+(j+1)%8,(k+1)*8+(j+1)%8,(k+1)*8+j) for k in range(2) for j in range(8)]
    fs += [tuple(reversed(range(8))),tuple(range(16,24))];b.surface='cast_shaft';b.geom(vs,fs,'Finish',col);b.surface=None
    # Bolted capitals and base flange, heads 16 mm wide, no gratuitous spheres.
    for zz in (.13,head-.20):
        for dx in (-.095,.095):b.tube([(x+dx,y-.205,zz),(x+dx,y-.219,zz)],.010,color=col,n=6)
