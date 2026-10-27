"""Shared fair side skins, rolled cab crown and formed front/bumper sections.

All independent panels evaluate the same original section fields across their
4.5 mm reveals. Arches are trimmed boundaries of those fields, not additions.
"""
import math
import bpy
from mathutils import Vector
from kit import model as G
from kit.vehicle import samples
import pickup_spec as S
from forms import (fair,section,side_x,belt_z,arch_floor,arch_point,
                   shoulder_z,hood,hood_z,nose_y,roof,roof_height,roof_width,
                   windshield,backlight,lamp_surface)


def rounded_polygon(points,distances,steps):
    """Tangent quadratic corner cuts, distances in physical meters in YZ."""
    out=[]
    for i,(p,d) in enumerate(zip(points,distances)):
        a=points[i-1];c=points[(i+1)%len(points)]
        la=math.dist(a,p);lc=math.dist(c,p);d=min(d,la*.40,lc*.40)
        q=tuple(p[k]+(a[k]-p[k])*d/la for k in range(2))
        r=tuple(p[k]+(c[k]-p[k])*d/lc for k in range(2))
        out.extend(tuple((1-t)**2*q[k]+2*t*(1-t)*p[k]+t*t*r[k] for k in range(2)) for t in samples(steps))
    return out


def build(b):
    gap=S.PANEL_GAP
    hood_p=G.pivot('Hood',(0,S.HOOD_REAR,1.408),'X',(-62,0));hood_p.parent=b.root
    hx=[0,.20,.40,.402,.410,.418,.48,.512,.520,.528,.602,.610,.618,.75,.90]
    hu=sorted(set([.5+x/1.8 for x in hx]+[.5-x/1.8 for x in hx]))
    b.skin('Hood outer',hood,32,18,b.m['body'],(0,0,1),hood_p,'hood',us=hu,vs=samples(12 if b.high else 4))
    b.skin('Roof crown',roof,44,44,b.m['body'],(0,0,1),category='cab',return_depth=.006,
           us=sorted(set(samples(24)+[.015,.025,.04,.07,.93,.96,.975,.985] if b.high else [0,.02,.04,.07,.12,.25,.5,.75,.88,.93,.96,.98,1])),
           vs=sorted(set(samples(36)+[.01,.025,.045,.07,.10,.4719101123595506,.88,.94,.98] if b.high else [0,.025,.07,.15,.3,.4719101123595506,.65,.80,.9,.97,1])))
    b.skin('Windshield',windshield,24,10,b.m['glass'],(0,-1,1),category='glass',gauge=.0048,return_depth=0)
    b.skin('Rear glass',backlight,24,10,b.m['glass'],(0,1,0),category='glass',gauge=.0048,return_depth=0)
    if b.detail:bpy.data.objects['Rear glass'].data.materials[0]=b.m['rear_glass']

    def side_panel(name,ya,yb,cap,sign,parent,category,axle=None):
        # One continuous skin from the trimmed arch to the belt. The draw field
        # extends 205 mm into the panel, so all its rows share correct tangents.
        ys=[ya+(yb-ya)*t for t in samples(4 if axle is not None else 4)]
        if axle is not None:
            ys += [arch_point(t,axle)[0] for t in samples(48 if b.high else 20)]
            ys += [axle+d for d in [-.75,-.68,-.60,.60,.68,.75]]
        us=sorted(set([0,1]+[(y-ya)/(yb-ya) for y in ys if ya<y<yb]))
        # Split at a fixed height, keeping both lower styling and the shoulder
        # independent of the change in arch-boundary parameter spacing.
        split=lambda y:shoulder_z(y)-.065
        def lower(u,v):
            y=ya+(yb-ya)*u;low=arch_floor(y,axle) if axle is not None else S.ROCKER+.013
            hi=split(y)
            target=v if v<=1.10 else 1.10+(hi-1.10)*(v-1.10)/.167
            d=target-low;k=.008
            lift=0 if d<=-k else (d if d>=k else (d+k)**2/(4*k))
            z=low+.97*lift+.03*(hi-low)*(target-.530)/(hi-.530)
            return sign*side_x(y,z),y,z
        b.skin(name,lower,24,22,b.m['body'],(sign,0,0),parent,category,us=us,
               vs=[.530,.620,.720,.780,.88,1.02,1.10,1.267] if not b.high else [.530,.620,.680,.720,.750,.780,.840,.900,.950,1.00,1.04,1.08,1.10,1.267],return_depth=.012)
        def upper(u,v):
            y=ya+(yb-ya)*u;h=shoulder_z(y)
            z=h+v if v<=.022 else h+.022+(cap(y)-h-.022)*(v-.022)/.078
            return sign*side_x(y,z),y,z
        # Fixed physical section stations, rather than an interpolation that
        # changes station order or clamps the hood cap around its leading edge.
        vs=[-.065,-.040,-.025,-.018,-.012,-.006,0,.006,.012,.016,.022,.06,.10] if b.high else [-.065,-.012,0,.012,.022,.10]
        b.skin(name+' shoulder',upper,24,20,b.m['body'],(sign,0,0),parent,category,us=samples(12 if b.high else (2 if category=='bed' else 4)),vs=vs,return_depth=.008)

    for side,sign in [('L',-1),('R',1)]:
        fend_end=S.DOOR_FRONT-gap/2
        side_panel('Front fender_'+side,-2.495,fend_end,lambda y:hood_z(.984,y),sign,b.root,'fenders',S.FRONT_AXLE)
        # The headlamp wraps beyond the front face into a genuinely open seat.
        def front_lower(u,v):
            y=-2.625+.125*u;z=S.ROCKER+(.883-S.ROCKER)*v
            return sign*side_x(y,z),y,z
        b.skin('Front fender lamp seat_'+side,front_lower,6,6,b.m['body'],(sign,0,0),category='fenders')
        def fender_top(u,v):
            x=.9045+(.984-.9045)*u;fy=nose_y(x,hood_z(x,S.HOOD_FRONT))
            y=fy+(S.HOOD_REAR-fy)*v
            return sign*x,y,hood_z(x,y)
        b.skin('Fender shoulder_'+side,fender_top,8,34,b.m['body'],(0,0,1),category='fenders',return_depth=.008)
        for end,ya,yb in [('F',S.DOOR_FRONT+gap/2,S.DOOR_SPLIT-gap/2),('R',S.DOOR_SPLIT+gap/2,S.DOOR_REAR)]:
            pivot=G.pivot('Door_'+end+side,(sign*.944,ya,1.04),'Z',((-72,0) if sign==1 else (0,72)))
            pivot.parent=b.root;pivot['checkpoint_only']=True
            side_panel('Door skin_'+end+side,ya,yb,belt_z,sign,pivot,'doors')
            if end=='F':
                outer=[(ya,belt_z(ya)),(yb,belt_z(yb)),(yb,1.882),(-.560,1.884),(-.775,1.820)]
                inner=[(ya+.066,belt_z(ya)+.045),(yb-.039,belt_z(yb)+.039),(yb-.039,1.844),(-.548,1.848),(-.746,1.785)]
                radii=[.035,.025,.035,.080,.090]
            else:
                outer=[(ya,S.BELT),(yb,S.BELT),(.878,1.835),(.760,1.879),(ya,1.882)]
                inner=[(ya+.039,S.BELT+.039),(yb-.049,S.BELT+.043),(.832,1.803),(.736,1.840),(ya+.039,1.844)]
                radii=[.025,.085,.100,.075,.025]
            def adjust(poly):
                return [(y,z+min(0,roof_height(roof_width(y),y)-1.882)*fair((z-1.70)/.10)) if y>-.65 else (y,z) for y,z in poly]
            outer=adjust(outer);inner=adjust(inner)
            paths=[rounded_polygon(poly,radii,8 if b.high else 5) for poly in (outer,inner)]
            dense=[[],[]]
            for i in range(len(paths[0])):
                count=max(1,math.ceil(max(math.dist(path[i],path[(i+1)%len(path)]) for path in paths)/.16))
                for path,result in zip(paths,dense):
                    p,q=path[i],path[(i+1)%len(path)]
                    result.extend(tuple(p[k]+(q[k]-p[k])*j/count for k in range(2)) for j in range(count))
            def loop(poly,inset=0):
                return [(sign*(side_x(y,z)-inset),y,z) for y,z in poly]
            outer0=loop(dense[0]);inside=loop(dense[1])
            sash=G.loft('Door sash_'+end+side,[loop(dense[0],.009),outer0,inside,loop(dense[1],.009)],b.m['body'],caps=False)
            sol=sash.modifiers.new('Sash gauge','SOLIDIFY');sol.thickness=.0009;sol.offset=-1
            G.smooth(sash,35);b.add(sash,pivot,'doors')
            # Restore the exposed sash's normal from the same side section as
            # the door below it; unequal corner loops must not dent reflections.
            n=len(outer0);custom=[(0,0,0)]*len(sash.data.loops)
            for face in sash.data.polygons:face.use_smooth=False
            for face in sash.data.polygons[n:2*n]:
                face.use_smooth=True
                for li in face.loop_indices:
                    p=sash.matrix_world@sash.data.vertices[sash.data.loops[li].vertex_index].co
                    e=1e-5;dy=(side_x(p.y+e,p.z)-side_x(p.y-e,p.z))/(2*e)
                    dz=(side_x(p.y,p.z+e)-side_x(p.y,p.z-e))/(2*e)
                    custom[li]=Vector((sign,-dy,-dz)).normalized()
            sash.data.normals_split_custom_set(custom)
            # Glass is planar in its own tumblehome plane. A convex perimeter
            # does not acquire a fan highlight when solidified.
            perimeter=loop(dense[1],.006)
            tilt=.018 if end=='R' else 0
            perimeter=[(sign*(.963-.26*(z-S.BELT)-.006-tilt*(y-ya)/(yb-ya)),y,z) for _,y,z in perimeter]
            cy=sum(q[1] for q in perimeter)/len(perimeter);cz=sum(q[2] for q in perimeter)/len(perimeter)
            verts=[(sign*(.963-.26*(cz-S.BELT)-.006-tilt*(cy-ya)/(yb-ya)),cy,cz)]+perimeter;n=len(perimeter)
            gl=G.mesh('Side glass_'+end+side,verts,[(0,i+1,(i+1)%n+1) for i in range(n)],b.m['glass'])
            sol=gl.modifiers.new('Glass thickness','SOLIDIFY');sol.thickness=.0048;sol.offset=-1
            b.add(gl,pivot,'glass')
            if b.detail:
                gl.data.materials[0]=b.m['side_glass' if end=='F' else 'privacy']
                sash.data.materials.append(b.m['plastic'])
                for face in sash.data.polygons:
                    center=sash.matrix_world@face.center
                    if (2*len(outer0)<=face.index<3*len(outer0)) or (abs(center.y-S.DOOR_SPLIT)<.055 and center.z>S.BELT+.02):face.material_index=1
        rear_outline=rounded_polygon(outer,radii,8 if b.high else 5)
        def pillar_a(u,v):
            xt,yt,zt=roof((1+.935+.065*u)/2,0)
            xb,yb,zb=windshield(1,0)
            xb+=(side_x(S.DOOR_FRONT,belt_z(S.DOOR_FRONT))-xb)*u
            yb+=(S.DOOR_FRONT-yb)*u;zb+=(belt_z(S.DOOR_FRONT)-zb)*u
            return sign*(xb+(xt-xb)*v),yb+(yt-yb)*v,zb+(zt-zb)*v
        b.skin('A pillar_'+side,pillar_a,6,30,b.m['body'],(sign,-1,0),category='cab',return_depth=.009)
        def pillar_c(u,v):
            z=S.ROCKER+(1.841-S.ROCKER)*v;t=fair((z-S.BELT)/.430)
            intersections=[]
            if z>S.BELT:
                for p,q in zip(rear_outline,rear_outline[1:]+rear_outline[:1]):
                    if (p[1]-z)*(q[1]-z)<=0 and abs(q[1]-p[1])>1e-8:
                        intersections.append(p[0]+(q[0]-p[0])*(z-p[1])/(q[1]-p[1]))
            front=max(intersections)+gap if intersections else .9265
            rear=1.025-.115*t;y=front+(rear-front)*u
            return sign*side_x(y,z),y,z
        b.skin('Cab rear corner_'+side,pillar_c,7,30,b.m['body'],(sign,0,0),category='cab')
        def roof_rail(u,v):
            y=-.720+1.620*v;edge=roof_height(roof_width(y),y)
            z=edge-.025*(1-u)
            return sign*(side_x(y,z)-.004*(1-fair(u))),y,z
        b.skin('Cab roof rail_'+side,roof_rail,3,36,b.m['body'],(sign,0,0),category='cab',return_depth=.006)
        def rocker(u,v):
            y=S.DOOR_FRONT+(S.DOOR_REAR-S.DOOR_FRONT)*u
            return sign*(.932+(side_x(y,.578)-.002-.932)*v),y,.538+.0355*v
        b.skin('Rocker return_'+side,rocker,24,3,b.m['body'],(sign,0,0),category='cab')
        if not b.detail:
            # Retained coarse mirror block from the earlier gate; detail is deferred.
            stem=G.box('Mirror support_'+side,(sign*1.036,-1.16,1.415),(.230,.125,.065),b.m['rubber'],.015,3)
            b.add(stem,b.root,'mirrors')
            mirror=G.box('Mirror envelope_'+side,(sign*1.13936,-1.19,1.505),(.180,.230,.180),b.m['bumper'],.024,4)
            b.add(mirror,b.root,'mirrors');mirror['bounds_exclude']=True;stem['bounds_exclude']=True
        side_panel('Bed outer_'+side,S.BED_OUTER_FRONT,2.844,lambda y:S.BED_TOP,sign,b.root,'bed',S.REAR_AXLE)
        def rail(u,v):
            y=S.BED_OUTER_FRONT+(2.844-S.BED_OUTER_FRONT)*v
            return sign*(.832+(.963-.832)*u),y,S.BED_TOP+.003
        b.skin('Bed rail_'+side,rail,6,32,b.m['body'],(0,0,1),category='bed',gauge=.0012,return_depth=.016)
        b.skin('Bed inner_'+side,lambda u,v:(sign*.832,S.BED_FRONT+S.BED_LENGTH*u,S.BED_FLOOR+(S.BED_TOP-S.BED_FLOOR)*v),18,5,b.m['bed'],(-sign,0,0),category='bed',return_depth=0)
        tub=G.box('Bed wheelhouse_'+side,(sign*.744,S.REAR_AXLE,1.015),(.203,.99,.22),b.m['bed'],.065,4 if b.high else 2);b.add(tub,b.root,'bed')
        b.skin('Bed rear corner_'+side,lambda u,v:(sign*(.863+(.982-.863)*u),2.847,.841+(S.BED_TOP-.841)*v),6,12,b.m['body'],(0,1,0),category='bed')
        lamp=G.box('Taillamp envelope_'+side,(sign*.922,2.850,1.182),(.122,.034,.395),b.m['glass'],.012,3);b.add(lamp,b.root,'lamp_forms')
        for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            def liner(u,v,axle=axle):
                y,z=arch_point(u,axle)
                return sign*(.650+.325*v),y,z+.014
            b.skin('Wheelwell_'+end+side,liner,48,3,b.m['rubber'],(0,0,-1),category='liners',gauge=.002,return_depth=0)
            outline=[arch_point(t,axle) for t in samples(40 if b.high else 28)]
            backing=G.profile('Wheelwell inboard_'+end+side,outline,sign*.649-.001,sign*.649+.001,b.m['rubber'],axis='X');b.add(backing,b.root,'liners')
            def lip(u,v,axle=axle):
                y,z=arch_point(u,axle)
                return sign*(side_x(y,z)-.018*v),y,z
            b.skin('Arch return_'+end+side,lip,48,2,b.m['body'],(sign,0,-1),category='fenders' if end=='F' else 'bed',us=samples(48 if b.high else 20),return_depth=0)
    b.skin('Cab rear lower',lambda u,v:((2*u-1)*.932,1.025,S.ROCKER+(1.458-S.ROCKER)*v),18,7,b.m['body'],(0,1,0),category='cab')
    def rear_header(u,v):
        a=backlight(u,1);c=roof(u,1)
        return tuple(p+(q-p)*v for p,q in zip(a,c))
    b.skin('Rear upper',rear_header,28,8,b.m['body'],(0,1,1),category='cab')
    # Cowl closes the real hood/windscreen transition without a raised glass box.
    b.skin('Cowl',lambda u,v:tuple(p+(q-p)*v for p,q in zip(hood(u,1),windshield(u,0))),24,4,b.m['body'],(0,0,1),category='cab')
    b.skin('Cab floor',lambda u,v:((2*u-1)*.92,S.DOOR_FRONT+(1.025-S.DOOR_FRONT)*v,.680),18,10,b.m['rubber'],(0,0,1),category='cab',return_depth=0)
    b.skin('Pickup bed floor',lambda u,v:((2*u-1)*.832,S.BED_FRONT+S.BED_LENGTH*v,S.BED_FLOOR),18,20,b.m['bed'],(0,0,1),category='bed')
    b.skin('Pickup box front',lambda u,v:((2*u-1)*.832,S.BED_FRONT,S.BED_FLOOR+(S.BED_TOP-S.BED_FLOOR)*v),18,6,b.m['bed'],(0,1,0),category='bed')
    gate=G.pivot('Tailgate',(0,2.824,S.BED_FLOOR),'X',(-90,0));gate.parent=b.root
    def gate_skin(u,v):
        x=(2*u-1)*.858;z=.841+(S.BED_TOP-.841)*v
        # Broad shallow stamp and upper shoulder, deliberately unbranded.
        y=2.847-.012*(1-(x/.858)**2)*(1-(2*v-1)**2)+.006*fair((z-1.34)/.07)
        return x,y,z
    b.skin('Tailgate outer',gate_skin,24,18,b.m['body'],(0,1,0),gate,'tailgate')
    b.skin('Tailgate inner',lambda u,v:((2*u-1)*.852,S.BED_REAR,S.BED_FLOOR+(S.BED_TOP-S.BED_FLOOR)*v),18,7,b.m['bed'],(0,-1,0),gate,'tailgate')
    b.skin('Tailgate top lip',lambda u,v:((2*u-1)*.858,S.BED_REAR+(2.853-S.BED_REAR)*v,S.BED_TOP+.003),24,3,b.m['body'],(0,0,1),gate,'tailgate',gauge=.0012,return_depth=.015)
    # Original tall grille on the shared 5.7-degree front face. Its upper edge
    # follows the hood shut line and its lamellae are recessed for real shadow.
    def front_patch(name,x0,x1,zlo,zhi,mat):
        def fn(u,v):
            x=x0+(x1-x0)*u;hi=hood_z(x,nose_y(x))-gap if zhi is None else zhi
            z=zlo+(hi-zlo)*v
            return x,nose_y(x,z),z
        us=sorted(set(samples(30 if b.high else 12)+[(x-x0)/(x1-x0) for sign in [-1,1] for d in [.760,.80,.84,.88,.91,.94,.96,.975] if x0<(x:=sign*d)<x1]))
        b.skin(name,fn,20,8,mat,(0,-1,0),category='nose',return_depth=.014,us=us,even_offset=False)
    front_patch('Nose brow',-.984,.984,1.208,None,b.m['body'])
    front_patch('Lower fascia',-.984,.984,.785,.847,b.m['body'])
    for sign in [-1,1]:
        lo,hi=sorted([sign*.690,sign*.984]);front_patch('Headlamp lower seat_'+str(sign),lo,hi,.847,.9245,b.m['body'])
        lo,hi=sorted([sign*.648,sign*.680]);front_patch('Nose lamp bridge_'+str(sign),lo,hi,.9245,1.208,b.m['body'])
        def corner_upper(u,v,sign=sign):
            a=.70+.30*u;x,y,z=lamp_surface(a,1)
            top=hood_z(x,y)-.0045;z=1.2075+(top-1.2075)*v
            x,y,z=lamp_surface(a,(z-.929)/.274)
            return sign*x,y,z
        b.skin('Upper lamp wrap surround_'+side,corner_upper,20,4,b.m['body'],(sign,-1,0),category='nose',return_depth=.006,even_offset=False)
        def corner_lower(u,v,sign=sign):
            a=.70+.30*u;lo=.847+.036*u;z=lo+(.9245-lo)*v
            x,y,z=lamp_surface(a,(z-.929)/.274)
            return sign*x,y,z
        b.skin('Lower lamp wrap surround_'+side,corner_lower,20,4,b.m['body'],(sign,-1,0),category='nose',return_depth=.006,even_offset=False)
        def lamp(u,v,s=sign):
            x,y,z=lamp_surface(u,v)
            return s*x,y,z
        b.skin('Headlamp envelope_'+str(sign),lamp,32,8,b.m['lens'],(sign,-1,0),category='lamp_forms',gauge=.0026,return_depth=0,
               us=sorted(set(samples(26 if b.high else 12)+[.70,.80,.9])))
    # A tall, hood-following surround forms one brow with the lamp corners.
    # Its lower inner wall reaches the grille 80 mm behind the shut-line face.
    outline=[(-.635,.809),(.635,.809),(.676,.858),(.676,1.205)]
    outline += [(x,hood_z(x,nose_y(x))-.0045) for x in [.64,.52,.41,0,-.41,-.52,-.64]]
    outline += [(-.676,1.205),(-.676,.858)]
    perimeter=rounded_polygon(outline,[.009]*len(outline),3 if b.high else 2)
    loops=[]
    for inset,offset in [(0,0),(.008,-.003),(.025,-.003),(.028,.080)]:
        loops.append([(x*(1-inset/.69),nose_y(x,z)+offset,1.035+(z-1.035)*(1-inset/.24)) for x,z in perimeter])
    grille=G.loft('Grille form surround',loops,b.m['body'],caps=False)
    sol=grille.modifiers.new('Surround gauge','SOLIDIFY');sol.thickness=.002
    b.add(grille,b.root,'nose')
    backing=G.profile('Grille envelope',[(x*.94,1.035+(z-1.035)*.85) for x,z in perimeter],-2.744,-2.731,b.m['rubber'],axis='Y')
    b.add(backing,b.root,'nose')
    # Swept formed bumper sections: upper return, beam crown, lower kick. The
    # tiny mid-beam crest retains the established envelope; corners tuck back.
    for end,sgn in [('F',-1),('R',1)]:
        zs=[.565,.590,.632,.707,.770,.792] if sgn<0 else [.590,.615,.665,.770,.812,.832]
        def bumper(u,z,sgn=sgn):
            x=(2*u-1)*.984;a=abs(x)
            wrap=(.225-math.sqrt(max(0,.225**2-max(0,a-.760)**2))) if sgn<0 else .095*fair((a-.735)/.249)
            depth=section(z,[(zs[0],.040),(zs[1],.009),(zs[2],0),(zs[3],.006),(zs[4],.032),(zs[5],.050)],.006)
            # Broad raised end cheeks and shallow center recess change planes.
            recess=.021*(1-fair((a-.43)/.20))
            return x,sgn*(S.LENGTH/2-wrap-depth-recess),z
        us=sorted(set(samples(34 if b.high else 24)+[.09,.12,.18,.28,.72,.82,.88,.91]))
        # Keep a small physical crest at x=.66, beyond the central recess.
        if sgn<0:
            for label,lo,hi in [('left',0,.205),('right',.795,1)]:
                b.skin('Front bumper '+label,lambda u,z,lo=lo,hi=hi:bumper(lo+(hi-lo)*u,z),16,8,b.m['bumper'],(0,-1,0),category='bumpers',gauge=.0025,return_depth=.040,vs=zs)
            for label,zs0 in [('lower',[.565,.590,.615]),('upper',[.745,.770,.792])]:
                b.skin('Front bumper '+label,lambda u,z:bumper(.205+.590*u,z),14,4,b.m['bumper'],(0,-1,0),category='bumpers',gauge=.0025,return_depth=.040,vs=zs0)
            b.skin('Bumper intake envelope',lambda u,v:((2*u-1)*.650,-2.850,.607+.148*v),12,3,b.m['rubber'],(0,-1,0),category='bumpers',gauge=.003,return_depth=0)
        else:
            if not b.detail:
                b.skin('Bumper_'+end,bumper,32,8,b.m['bumper'],(0,sgn,0),category='bumpers',gauge=.0025,return_depth=.045,us=us,vs=zs)
            else:
                for label,lo,hi in [('left',0,.407),('right',.593,1)]:
                    b.skin('Rear bumper '+label,lambda u,z,lo=lo,hi=hi:bumper(lo+(hi-lo)*u,z),18,6,b.m['chrome'],(0,1,0),category='bumpers',gauge=.0025,return_depth=.045,vs=zs)
                for label,z0,z1 in [('lower',.590,.615),('upper',.805,.832)]:
                    b.skin('Rear bumper '+label,lambda u,v,z0=z0,z1=z1:bumper(.407+.186*u,z0+(z1-z0)*v),8,2,b.m['chrome'],(0,1,0),category='bumpers',gauge=.0025,return_depth=.045)
        def shelf(u,v,sgn=sgn):
            x,y,z=bumper(u,zs[-1])
            return x,y-sgn*.075*v,z
        b.skin('Bumper upper return_'+end,shelf,28,3,b.m['bumper'],(0,0,1),category='bumpers',gauge=.0025,return_depth=0)
    def valance(u,v):
        x=(2*u-1)*(.950-.040*v);wrap=.205*fair((abs(x)-.735)/.249)
        return x,-2.895+wrap+.030*v,.565-.110*v
    b.skin('Lower valance',valance,34,5,b.m['rubber'],(0,-1,0),category='bumpers',gauge=.003,return_depth=.030)
