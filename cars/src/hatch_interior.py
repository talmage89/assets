"""Five-place low sedan cabin, built with the family's formed-section method."""
import math
import bpy,bmesh
from mathutils import Vector
from kit import model as G
from detail_helpers import box,tube,loop,print_quad
from hatch_check import mesh_tree,plane_cut
import hatch_spec as S


def build(b):
    def cushion(name,x,y,w,d,z0,z1,mat):
        rings=[[(x+u,y+v,z) for u,v in G.rounded_rectangle(w*s,d*s,min(.045,w*.13),2 if not b.high else 4)]
               for z,s in [(z0,.91),((z0+z1)/2,1),(z1,.94)]]
        return b.add(G.smooth(G.loft(name,rings,mat)),category='interior')
    for side,x in [('L',-.43),('R',.43)]:
        for dx in [-.16,.16]:box(b,'H120 seat rail '+side+str(dx),(x+dx,-.25,.285),(.025,.49,.035),b.m['frame'],'interior',radius=0)
        cushion('H120 front cushion '+side,x,-.23,.49,.52,.325,.455,b.m['cloth'])
        rings=[]
        for z,y,w,d in [(.43,.015,.46,.14),(.64,.09,.49,.15),(.90,.20,.44,.13),(1.015,.25,.37,.105)]:
            rings.append([(x+u,y+v,z) for u,v in G.rounded_rectangle(w,d,.035,2 if not b.high else 4)])
        b.add(G.smooth(G.loft('H120 front backrest '+side,rings,b.m['cloth'])),category='interior')
        for sign in [-1,1]:
            tube(b,'H120 headrest stalk '+side+str(sign),[(x+sign*.068,.25,.98),(x+sign*.068,.29,1.09)],.005,b.m['chrome'],'interior',sides=6)
            tube(b,'H120 bolster piping '+side+str(sign),[(x+sign*.16,-.055,.49),(x+sign*.17,.02,.67),(x+sign*.145,.14,.93)],.0014,b.m['seat_side'],'interior',sides=4)
        cushion('H120 front headrest '+side,x,.29,.25,.12,1.055,1.205,b.m['cloth'])
        box(b,'H120 seat buckle '+side,(x+(.255 if x<0 else -.255),.0,.43),(.025,.038,.045),b.m['plastic'],'interior',radius=.004)
    cushion('H120 rear bench',0,.94,1.32,.47,.382,.465,b.m['cloth'])
    rings=[[(u,y+v,z) for u,v in G.rounded_rectangle(w,.12,.035,2 if not b.high else 4)]
           for z,y,w in [(.44,1.17,1.22),(.72,1.24,1.26),(1.01,1.33,1.22)]]
    b.add(G.smooth(G.loft('H120 rear backrest',rings,b.m['cloth'])),category='interior')
    for i,x in enumerate([-.45,0,.45]):
        for dx in [-.05,.05]:tube(b,'H120 rear headrest stalk '+str(i)+str(dx),[(x+dx,1.32,.97),(x+dx,1.34,1.07)],.0045,b.m['chrome'],'interior',sides=6)
        cushion('H120 rear headrest '+str(i),x,1.345,.225,.10,1.045,1.18,b.m['cloth'])
    # A sloping upper crash pad, driver hood, console and five-seat package.
    profile=[(-1.025,.47),(-1.025,.86),(-.94,.91),(-.69,.86),(-.56,.74),(-.63,.49)]
    dash=G.profile('H120 dashboard shell',profile,-.77,.77,b.m['interior'],axis='X',radius=.012,segments=2 if b.high else 1)
    for v in dash.data.vertices:
        if v.co.z<.73:v.co.x*=.50/.77
    b.add(dash,category='interior')
    box(b,'H120 center stack',(0,-.573,.705),(.30,.05,.28),b.m['seat_side'],'interior',radius=.016)
    print_quad(b,'H120 center screen',[(.127,-.542,.72),(-.127,-.542,.72),(-.127,-.542,.82),(.127,-.542,.82)],b.m['display'],'interior')
    box(b,'H120 instrument hood',(.43,-.67,.88),(.35,.18,.105),b.m['plastic'],'interior',radius=.022)
    print_quad(b,'H120 instrument panel',[(.58,-.574,.84),(.28,-.574,.84),(.28,-.574,.895),(.58,-.574,.895)],b.m['display'],'interior')
    for x in [-.65,-.20,.20,.65]:
        box(b,'H120 vent '+str(x),(x,-.605,.83),(.095,.025,.042),b.m['plastic'],'interior',radius=.006)
        for z in [.821,.835]:box(b,'H120 vent vane '+str(x)+str(z),(x,-.590,z),(.080,.005,.003),b.m['interior_light'],'interior',radius=0)
    box(b,'H120 console',(0,-.09,.365),(.235,.80,.24),b.m['interior'],'interior',radius=.025)
    box(b,'H120 armrest',(0,.14,.525),(.25,.30,.060),b.m['seat_side'],'interior',radius=.020)
    for y in [-.10,-.24]:
        loop(b,'H120 cup rim '+str(y),(0,y,.489),(1,0,0),(0,1,0),(.043,.043),.004,b.m['plastic'],'interior',segments=12,sides=4)
        box(b,'H120 cup floor '+str(y),(0,y,.47),(.080,.080,.012),b.m['plastic'],'interior',radius=.016)
    tube(b,'H120 shifter',[(.065,-.40,.48),(.065,-.37,.58)],.010,b.m['chrome'],'interior',sides=6)
    box(b,'H120 shift knob',(.065,-.37,.59),(.04,.055,.046),b.m['seat_side'],'interior',radius=.013)
    c=Vector((.43,-.43,.855));a=Vector((1,0,0));up=Vector((0,-.43,.903)).normalized();normal=a.cross(up)
    loop(b,'H120 steering rim',c,a,up,(.172,.172),.014,b.m['rubber'],'interior',segments=24 if not b.high else 40,sides=6 if not b.high else 10)
    tube(b,'H120 steering column',[tuple(c+normal*.02),(.43,-.75,.62)],.026,b.m['plastic'],'interior',sides=8)
    box(b,'H120 steering airbag',c,(.14,.065,.12),b.m['seat_side'],'interior',radius=.022)
    for angle in [0,math.pi,1.5*math.pi]:
        tube(b,'H120 wheel spoke '+str(angle),[tuple(c+a*(.06*math.cos(angle))+up*(.06*math.sin(angle))),tuple(c+a*(.15*math.cos(angle))+up*(.15*math.sin(angle)))],.016,b.m['interior_light'],'interior',sides=4)
    for side,sign in [('L',-1),('R',1)]:
        for end,ya,yb in [('F',S.DOOR_FRONT,S.DOOR_SPLIT),('R',S.DOOR_SPLIT,S.DOOR_REAR)]:
            parent=bpy.data.objects['Door_'+end+side];y=(ya+yb)/2;w=yb-ya-.12
            door=bpy.data.objects['Door '+end+'_'+side];skin=mesh_tree([door]);vertices=[]
            margin=.235 if end=='F' else .065
            ys=[ya+margin+(yb-ya-margin-.065)*j/5 for j in range(6)]
            if end=='R':ys=sorted(set(ys+[.9,1.0,1.1,1.18]))
            rocker=bpy.data.objects['Rocker_'+side]
            for yy in ys:
                cut=plane_cut([door],yy);sill=plane_cut([rocker],yy)
                bottom=max(min(p[1] for segment in cut for p in segment)+.035,.31)
                if end=='R' and abs(yy-S.REAR_AXLE)<S.ARCH_RADIUS+.014:
                    bottom=max(bottom,S.HUB_HEIGHT+math.sqrt((S.ARCH_RADIUS+.014)**2-(yy-S.REAR_AXLE)**2)+.035)
                for k in range(3):
                    zz=bottom+(.975-bottom)*k/2
                    hit=skin.ray_cast(Vector((sign*2,yy,zz)),Vector((-sign,0,0)),4)[0]
                    if hit is None:raise ValueError(('Door card misses its supported skin',end,side,yy,zz))
                    vertices.append((sign*(abs(hit.x)-.060),yy,zz))
            faces=[(j*3+k,(j+1)*3+k,(j+1)*3+k+1,j*3+k+1) for j in range(len(ys)-1) for k in range(2)]
            card=G.mesh('H120 door card '+end+side,vertices,faces,b.m['interior'])
            if card.data.polygons[0].normal.x*sign>0:
                for face in card.data.polygons:face.flip()
            sol=card.modifiers.new('Door card wall','SOLIDIFY');sol.thickness=.025;sol.offset=-1;sol.use_even_offset=False
            b.add(card,parent,'interior')
            box(b,'H120 door armrest '+end+side,(sign*.770,y+(.22 if end=='F' else 0),.725),(.07,w*.50,.055),b.m['seat_side'],'interior',parent,.016)
            box(b,'H120 inner latch '+end+side,(sign*.765,y-.18,.82),(.025,.090,.025),b.m['chrome'],'interior',parent,.005)
            box(b,'H120 door pocket '+end+side,(sign*.760,y+(.18 if end=='F' else -.14),.53),(.055,.45,.060),b.m['plastic'],'interior',parent,.012)
    cargo(b)
    # The headliner follows the held roof as a compound section, not a flat lid.
    roof=bpy.data.objects['Roof'];copy=roof.copy();copy.data=roof.data.copy();bpy.context.collection.objects.link(copy)
    copy.name='H120 headliner';copy.data.materials.clear();copy.data.materials.append(b.m['headliner'])
    for v in copy.data.vertices:v.co.z-=.022
    bm=bmesh.new();bm.from_mesh(copy.data)
    remove=[f for f in bm.faces if f.normal.z<.3]
    bmesh.ops.delete(bm,geom=remove,context='FACES');bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(copy.data);bm.free()
    if copy.data.has_custom_normals:copy.data.normals_split_custom_set([(0,0,0)]*len(copy.data.loops))
    sol=copy.modifiers.new('Lining shell gauge','SOLIDIFY');sol.thickness=.002;sol.use_even_offset=False;G.apply(copy)
    if not b.high:
        modifier=copy.modifiers.new('Hidden headliner allocation','DECIMATE');modifier.ratio=.10;G.apply(copy)
    b.add(copy,category='interior')
    for x in [-.43,.43]:box(b,'H120 stowed visor '+str(x),(x,-.29,1.327),(.33,.14,.018),b.m['headliner'],'interior',radius=.008)
    tube(b,'H120 cabin mirror mount',[(0,-.45,1.22),(0,-.40,1.18)],.012,b.m['plastic'],'interior',sides=6)
    box(b,'H120 cabin mirror',(0,-.39,1.17),(.21,.035,.065),b.m['plastic'],'interior',radius=.012)
    box(b,'H120 cabin mirror pane',(0,-.37,1.17),(.19,.003,.049),b.m['mirror'],'interior',radius=.008)


def cargo(b):
    """Trimmed load well, wheelhouse trim and removable parcel cover."""
    box(b,'H120 cargo floor',(0,1.61,.494),(1.05,.82,.026),b.m['cloth'],'cargo',radius=.008)
    for sign in [-1,1]:
        box(b,'H120 cargo wheelhouse trim '+str(sign),(sign*.572,1.62,.625),(.11,.68,.28),b.m['interior'],'cargo',radius=.030)
    box(b,'H120 load sill',(0,2.016,.584),(1.04,.052,.045),b.m['plastic'],'cargo',radius=.008)
    if b.high:box(b,'H120 parcel cover',(0,1.60,.971),(1.11,.63,.018),b.m['cloth'],'cargo',radius=.010)
    else:
        outline=[(u,1.60+v) for u,v in G.rounded_rectangle(1.11,.63,.018,1)]
        b.add(G.profile('H120 parcel cover',outline,.962,.980,b.m['cloth'],axis='Z'),category='cargo')
    for sign in []:
        tube(b,'H120 parcel cover tether '+str(sign),[(sign*.50,1.88,.978),(sign*.50,1.91,1.10)],.0015,b.m['rubber'],'cargo',sides=4)
