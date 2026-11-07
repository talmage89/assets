"""Assemble three distinct cafes and a reusable stock library; export first."""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import bpy
from mathutils import Vector,Matrix
from kit import tiling
from plan import generate,PROOFS
from graphics import generate as graphics
import geometry as G
import pieces as P
from package import externalize,bundle


def import_piece(path,parent=None,prefix=None,select=None):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()));obs=list(set(bpy.context.scene.objects)-before)
    roots=[o for o in obs if o.parent not in obs]
    if select:
        selected=next(o for o in obs if o.name==select)
        keep=set(G.descendants(selected))
        selected.parent=None;selected.location=(0,0,0)
        for o in obs:
            if o not in keep:bpy.data.objects.remove(o,do_unlink=True)
        obs=list(keep);roots=[selected]
    for o in roots:o.parent=parent
    if prefix:
        for o in obs:o.name=prefix+o.name
    return roots,obs


def library():
    bpy.ops.wm.read_factory_settings(use_empty=True);G.palette();lib=G.root('CoffeeShopPieces',library=True)
    defs={}
    for key,fn in [('BistroChair',P.chair),('BistroTable',P.table),('UmbrellaTable',lambda name,parent:P.table(name,parent=parent,umbrella=True)),('AccessibleTable',lambda name,parent:P.table(name,True,parent)),('Counter',P.counter),('EspressoMachine',P.espresso),('Grinder',P.grinder),('Brewer',P.brewer),('PastryCase',P.pastry),('SoftChair',P.armchair),('AFrame',P.aframe),('Planter',P.planter)]:
        defs[key]=fn(key,parent=lib)
        from finishes import stock
        stock(defs[key],key)
    for i,state in enumerate(('Open','Closed')):
        roots,obs=import_piece(REPO/'patio-set/export/PatioSet.glb',lib,select='Umbrella_'+state)
        r=roots[0];r.name='Umbrella_'+state;r['piece']='Umbrella_'+state;defs[r.name]=r
    for key in ('BikeRack','Litter','Recycling'):
        roots,obs=import_piece(REPO/f'street-furniture/export/{key}.gltf',lib)
        r=G.root('Stock_'+key,parent=lib,piece=key)
        for o in roots:o.parent=r
        defs[key]=r
    # Single roots remain at zero in stock files; the library is spaced for inspection.
    rows=[]
    for i,(key,r) in enumerate(defs.items()):
        r.location=(0,0,0);bpy.context.view_layer.update();out=Path('build/pieces')/(key+'.glb');out.parent.mkdir(parents=True,exist_ok=True)
        tiling.export(out,G.descendants(r));meta=externalize(out,Path('export/pieces')/(key+'.gltf'))
        tris=sum(len(o.data.polygons) for o in G.descendants(r) if o.type=='MESH')
        # Imported kit pieces are already triangles; our batch finalizes each face.
        tris=sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in G.descendants(r) if o.type=='MESH')
        limit=4000 if 'Umbrella' in key else 3000
        if tris>limit and key not in ('Litter','Recycling'):raise ValueError((key,tris,limit))
        rows.append(dict(piece=key,triangles=tris,limit=limit,reused=key in ('Umbrella_Open','Umbrella_Closed','BikeRack','Litter','Recycling'),**meta))
        r.location=((i%5)*2.15,(i//5)*3.25,0)
    tiling.export('build/pieces/library.glb');externalize('build/pieces/library.glb','export/CoffeeShopPieces.gltf')
    Path('build/pieces/manifest.json').write_text(json.dumps(rows,indent=2)+'\n')


def add_piece(key,name,pos,parent,yaw=0):
    # Import once per stock mesh, then clone its hierarchy with linked mesh data.
    cache=add_piece.cache
    if key not in cache:
        roots,obs=import_piece(Path('export/pieces')/(key+'.gltf'))
        if len(roots)!=1:raise ValueError((key,[o.name for o in roots]))
        r=roots[0];r.name='Template_'+key;cache[key]=r
    return G.clone(cache[key],name,pos,parent,yaw)
add_piece.cache={}


def fixtures(p,front):
    grade=p['grade'];r=G.root('Room',parent=front,part='visible_room');b=G.Batch('Room__ShellAndDressing',r);w=p['width'];dep=p['room_depth'];ceiling=3.04 if p['kind']!='downtown' else 3.16
    nx=math.ceil((w-.5)/.45);ny=math.ceil(dep/.45)
    vs=[(-(w-.5)/2+(w-.5)*i/nx,dep*j/ny,grade+.016) for j in range(ny+1) for i in range(nx+1)]
    b.geom(vs,[(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i) for j in range(ny) for i in range(nx)],'floor')
    b.box((0,dep/2,grade+ceiling),(w-.5,dep,.055),'cream')
    b.box((0,dep,grade+ceiling/2),(w-.48,.085,ceiling),'wall')
    for s in (-1,1):
        if s>0 and p['kind']=='pad':
            for ya,yb in ((0,1.885),(3.715,dep)):b.box((s*(w/2-.29),(ya+yb)/2,grade+ceiling/2),(.035,yb-ya,ceiling),'cream')
            for za,zb in ((grade,.9652),(2.0652,grade+ceiling)):b.box((s*(w/2-.29),2.8,(za+zb)/2),(.035,1.83,zb-za),'cream')
        else:b.box((s*(w/2-.29),dep/2,grade+ceiling/2),(.035,dep,ceiling),'cream')
    # Tables and the soft seating corner occupy different sides in each room.
    seats=([(-2.12,2.5),(-2.12,4.6)] if p['kind']=='downtown' else [(2.2,2.0),(4.25,4.2),(1.7,5.7)] if p['kind']=='strip' else [(-3.15,2.4),(-2.8,5.2)])
    for i,(x,y) in enumerate(seats):
        add_piece('BistroTable',f'Room_Table_{i+1}',(x,y,grade),r)
        for j,sgn in enumerate((-1,1)):add_piece('BistroChair',f'Room_Chair_{i+1}_{j}',(x+sgn*.57,y,grade),r,90 if sgn<0 else -90)
    softx=-1.9 if p['kind']=='downtown' else 4.7 if p['kind']=='strip' else -3.6;softy=dep-1.15
    add_piece('SoftChair','Room_LoungeA',(softx,softy,grade),r,0)
    if p['kind']!='downtown':add_piece('SoftChair','Room_LoungeB',(softx+(-1.1 if softx>0 else 1.1),softy,grade),r,18)
    b.rounded((softx,softy-.80,grade+.34),(.72,.48,.04),.018,'wood')
    for x in (-.27,.27):b.box((softx+x,softy-.80,grade+.16),(.045,.35,.32),'wood')
    # Community notices and abstract art are original sheet regions.
    b.box((softx,dep-.05,grade+1.81),(1.42,.055,.94),'wood');b.panel(softx,dep-.081,grade+1.81,1.33,.85,'community')
    artx=-w*.32 if p['kind']=='strip' else w*.34;b.box((artx,dep-.05,grade+1.9),(.80,.06,1.06),'wood');b.panel(artx,dep-.082,grade+1.9,.71,.97,'art')
    # Condiment bar with return, urns, lids, napkins and small waste aperture.
    cx=-w/2+.84 if p['kind']!='strip' else w/2-.84;cy=1.12
    b.box((cx,cy,grade+.46),(1.05,.45,.92),'wood');b.rounded((cx,cy,grade+.94),(1.13,.53,.04),.009,'cream')
    for dx in (-.30,0):
        b.lathe([(grade+.96,.045),(grade+1.15,.045),(grade+1.20,.024),(grade+1.22,.024)],'steel',12,center=(cx+dx,cy))
    b.box((cx+.27,cy,grade+1.015),(.18,.18,.105),'black');b.box((cx+.27,cy-.02,grade+1.072),(.13,.12,.008),'white')
    for j in range(3):b.cylinder((cx+.42,cy+.11,grade+.976+j*.008),.038,.008,'white',12)
    # Pendants have cord, canopy, formed shade and actual bulb. Light sockets
    # survive export; presentation adds the necessary area lights at those nodes.
    pendants=[(p['counter_x']-.95,2.60),(p['counter_x']+.50,2.60),(softx,softy-.25)]
    for i,(x,y) in enumerate(pendants):
        z=grade+2.35;b.cylinder((x,y,grade+ceiling-.04),.065,.028,'black',12)
        b.tube([(x,y,z+.12),(x,y,grade+ceiling-.04)],.003,'black',6)
        b.lathe([(z-.045,.19),(z,.18),(z+.10,.10),(z+.12,.025)],'copper',20,center=(x,y))
        b.cylinder((x,y,z-.035),.12,.012,'white',16);G.socket(f'Room_Pendant_{i}',(x,y,z-.06),r,'light',power_w=90)
    shell=b.finish()
    from finishes import room_floor_age
    room_floor_age(shell,p)
    counter=add_piece('Counter','Room_Counter',(p['counter_x'],p['counter_y'],grade),r,p['counter_yaw'])
    # Scale the straight joinery along its own long axis, then apply geometry.
    if abs(p['counter_length']-3.65)>1e-6:
        for o in counter.children_recursive:
            if o.type=='MESH':o.data=o.data.copy();o.data.transform(Matrix.Diagonal((p['counter_length']/3.65,1,1,1)))
    # Back bar and customer counter leave a real .96m barista aisle. The
    # machine's operating face looks into that aisle, not into a wall.
    back=G.Batch('Room__BackBar',counter);back.box((0,1.65,.49),(3.3,.58,.98),'wood');back.rounded((0,1.65,1.025),(3.39,.66,.055),.012,'cream');back.finish()
    work=G.root('Room_Worktop',(0,1.65,1.054),counter)
    add_piece('EspressoMachine','Room_Espresso',(.24,.09,0),work)
    add_piece('Grinder','Room_Grinder_1',(-.36,.12,0),work);add_piece('Grinder','Room_Grinder_2',(-.66,.12,0),work)
    add_piece('Brewer','Room_Brewer',(1.28,.0,0),work)
    frontwork=G.root('Room_CustomerTop',(0,0,1.054),counter)
    bb=G.Batch('Room__CounterSmallware',frontwork);bb.rounded((-.99,-.02,.07),(.29,.21,.14),.012,'black')
    bb.panel(-.99,-.132,.16,.26,.15,'screen');bb.cylinder((-1.30,-.14,.095),.060,.19,'glass',16);bb.panel(-1.30,-.202,.09,.09,.09,'chalk')
    # Stainless pitchers, cup stacks and supported syrup bottles.
    for j in range(3):
        x=.73+j*.10;bb.lathe([(.0,.029),(.10,.037),(.12,.037)],'steel',12,center=(x,.16))
    for j in range(3):
        for k in range(3):bb.lathe([(.005+k*.016,.026),(.05+k*.016,.032)],'white',10,center=(-.12+j*.08,.22))
    bb.finish()
    casepos=(p['counter_x']-p['counter_length']/2-.59,p['counter_y'],grade) if p['kind']!='strip' else (-2.57,1.63,grade)
    add_piece('PastryCase','Room_PastryCase',casepos,r)
    # Menu group is immediately behind the working counter, not on a remote back wall.
    yaw=math.radians(p['counter_yaw']);menu=G.root('Room_MenuFrame',(p['counter_x']-math.sin(yaw)*2.06,p['counter_y']+math.cos(yaw)*2.06,grade),r);menu.rotation_euler.z=yaw
    mb=G.Batch('Room__Menus',menu)
    for i in range(3):
        x=(i-1)*1.10;mb.box((x,.0,2.18),(1.08,.055,.80),'wood');mb.panel(x,-.029,2.18,1.025,.745,'menu'+str(i))
    # Mounting rails transfer the boards to a low service partition.
    mb.box((0,.10,1.55),(3.38,.10,3.04),'wall');mb.finish()
    G.socket('Room_OrderQueue',(p['counter_x']-.9,p['counter_y']-.95,grade),r,'queue')
    return r


def exterior(p,front):
    r=G.root('StorefrontFitout',parent=front,part='storefront');b=G.Batch('Storefront__AwningSignHardware',r);w=p['width'];kind=p['kind'];pal=p['palette'];grade=p['grade']
    # New fabric awning fits the host's original carrier; ribs are wall-braced.
    aw=G.root('Awning',parent=r);ab=G.Batch('Awning__SewnPanels',aw)
    left=-w/2+1.65 if kind=='downtown' else -w/2+.42;right=w/2-.40;top=3.52 if kind=='downtown' else 2.98
    dep=1.42 if kind!='strip' else 1.12;drop=.38;n=max(3,round((right-left)/.88))
    for j in range(n):
        a=left+(right-left)*j/n;c=left+(right-left)*(j+1)/n;vs=[]
        for row in range(6):
            t=row/5
            for col in range(7):
                u=col/6;vs.append((a+(c-a)*u,-dep*t-.018*math.sin(math.pi*u)*t,top-drop*t-.095*math.sin(math.pi*u)*math.sin(math.pi*t)-.012*math.sin(3*math.pi*u)*t*t*(1-t)))
        aa,bb,cc,dd=G.LAYOUT[pal]
        faces=[];uvs=[]
        for row in range(5):
            for col in range(6):
                indices=(row*7+col,row*7+col+1,(row+1)*7+col+1,(row+1)*7+col)
                coords=[(aa+(cc-aa)*k/6,bb+(dd-bb)*v/5) for k,v in ((col,row),(col+1,row),(col+1,row+1),(col,row+1))]
                faces.append(indices);uvs.append(coords)
        ab.geom(vs,faces,pal,smooth=True,uv_faces=uvs)
        for k in range(8):
            u=k/8;v=(k+1)/8;x0=a+(c-a)*u;x1=a+(c-a)*v
            def curtain(t,bottom=False):
                return (a+(c-a)*t,-dep-.018*math.sin(math.pi*t)-(.022*math.sin(t*math.tau+j*.7) if bottom else 0),top-drop-(.20+.038*math.sin(math.pi*t)**2 if bottom else 0))
            ab.geom([curtain(u),curtain(v),curtain(v,True),curtain(u,True)],[(0,1,2,3)],pal,smooth=True)
        ab.beam((a,.045,top-.025),(a,-dep+.030,top-drop-.024),.020,role='black')
    ab.beam((right,.045,top-.025),(right,-dep+.030,top-drop-.024),.020,role='black');ab.beam((left,-dep+.030,top-drop-.024),(right,-dep+.030,top-drop-.024),.025,role='black')
    for x in (left,right):
        ab.box((x,.025,top-.34),(.12,.045,.62),'black');ab.beam((x,.025,top-.65),(x,-dep+.030,top-drop-.04),.025,role='black')
    cloth=ab.finish();cloth['awning_cloth']=True;cloth['fabric_panel_span_m']=(right-left)/n;cloth['sag_m']=.095
    signz=4.20 if kind=='strip' else 4.18 if kind=='downtown' else 3.36;signw=min(5.4,w-2);sy=-.40 if kind=='downtown' else -.105
    b.box((.3,sy,signz),(signw,.16,.65),pal);b.panel(.3,sy-.083,signz,signw-.04,.60,p['name'])
    # Two goosenecks fastened to the real carrier.
    for x in (-1.25,1.85):
        b.box((x,-.025,signz+.49),(.11,.03,.17),'black');b.tube([(x,-.04,signz+.49),(x,-.32,signz+.65),(x,-.60,signz+.52),(x,-.64,signz+.37)],.013,'black',8)
        b.lathe([(signz+.30,.10),(signz+.34,.11),(signz+.40,.045)],'black',16,center=(x,-.64));G.socket('Sign_Light_'+str(x),(x,-.64,signz+.29),r,'light',power_w=45)
    if kind=='downtown':
        x=w/2-.32;b.box((x,-.62,3.38),(.075,.74,.60),pal)
        b.beam((x,.04,3.85),(x,-1.01,3.85),.032);b.beam((x,.04,4.15),(x,-.85,3.85),.025)
        for yy in (-.90,-.37):b.tube([(x,yy,3.85),(x,yy,3.69)],.008,'steel',6)
        a,bv,c,d=G.LAYOUT[p['name']]
        b.geom([(x-.040,-.98,3.11),(x-.040,-.26,3.11),(x-.040,-.26,3.65),(x-.040,-.98,3.65)],[(0,1,2,3)],p['name'],[(a,bv),(c,bv),(c,d),(a,d)])
    # In-window menu holders occupy a small area; main equipment sightline stays clear.
    wx=-w/2+2.14 if kind=='downtown' else w/2-1.40
    b.box((wx,.15,grade+1.22),(.59,.030,.64),'wood');b.panel(wx,.132,grade+1.22,.54,.59,'menu0')
    b.panel(wx,.125,grade+1.82,.57,.27,'hours')
    # Applied vinyl, on the actual front pane, with open coverage around ink.
    vx=2.85 if kind=='downtown' else .55 if kind=='strip' else 3.5
    # Omit the redundant promotional vinyl. It cast a second readable word
    # onto the room behind it. Hours and menu holders remain single prints.
    b.finish()
    # Door-mounted panic bar and hydraulic closer follow actual host pivots.
    for door in [o for o in front.children_recursive if o.get('pivot_axis') and ('StoreDoor' in o.name or 'Entry' in o.name)]:
        db=G.Batch(door.name+'__PanicAndCloser',door)
        db.box((.46,.064,1.04),(.63,.040,.045),'steel')
        db.box((.46,-.026,.19),(.73,.008,.24),'steel')
        if kind!='downtown':db.panel(.46,-.0305,.19,.64,.17,'scuff')
        for x in (.17,.75):db.box((x,.037,1.04),(.055,.08,.08),'black')
        h=2.48 if kind=='downtown' else 2.03;db.box((.19,.036,h-.10),(.25,.07,.065),'steel');db.beam((.19,.073,h-.075),(.40,.16,h-.04),.014,role='steel');db.beam((.40,.16,h-.04),(.08,.12,h+.005),.014,role='steel');db.finish()
    return r


def outside(p,front):
    r=G.root('OutdoorSeating',parent=front,part='outdoor');z=p['grade'];kind=p['kind'];b=G.Batch('Outdoor__Boundary',r)
    for j,(x0,y0,x1,y1) in enumerate(p['rail']):
        length=math.hypot(x1-x0,y1-y0);n=math.ceil(length/1.8);h=p['barrier_height']
        for i in range(n+1):
            t=i/n;x=x0+(x1-x0)*t;y=y0+(y1-y0)*t;b.box((x,y,z+h/2),(.032,.032,h),'black');b.box((x,y,z+.01),(.10,.10,.02),'black')
        for zz in (.13,h):b.beam((x0,y0,z+zz),(x1,y1,z+zz),.025,.025)
        # Low fence is cane detectable; no rope-only trip line.
        for i in range(1,math.ceil(length/.15)):
            t=i/math.ceil(length/.15);b.box((x0+(x1-x0)*t,y0+(y1-y0)*t,z+(h+.13)/2),(.012,.012,h-.13))
    b.finish()
    for i,t in enumerate(p['tables']):
        umbrella=next((u for u in p['umbrellas'] if abs(u['x']-t['x'])<.05 and abs(u['y']-t['y'])<.05),None)
        tab=add_piece('AccessibleTable' if t['accessible'] else 'UmbrellaTable' if umbrella else 'BistroTable',t['id'],(t['x'],t['y'],z),r,t['rotation'])
        G.socket(t['id']+'__Placement',(t['x'],t['y'],z),r,'furniture_placement',clear_radius_m=t['occupied_radius'])
        # Accessible bay has only one opposing chair; keep the approach open.
        angles=[0] if t['accessible'] else [0,180]
        for j,a in enumerate(angles):
            a+=t['rotation'];rad=math.radians(a);x=t['x']+.58*math.cos(rad);y=t['y']+.58*math.sin(rad)
            ch=add_piece('BistroChair',f'{t["id"]}_Chair_{j+1}',(x,y,z),r,a-90)
            ch['placeable']=True
        settings=P.setting(t['id']+'_Setting',t['setting'],t['placement_seed'],tab);settings.location=(0,-.12,.762 if t['accessible'] else .742)
    for i,u in enumerate(p['umbrellas']):
        # Stock 38.1mm pole passes through a 52mm guide in the new four-leg
        # table. Its original weighted base remains on grade underneath.
        table=next(t for t in p['tables'] if abs(t['x']-u['x'])<.05 and abs(t['y']-u['y'])<.05)
        pos=(table['x'],table['y'],z)
        add_piece('Umbrella_'+u['state'].title(),'Outdoor_Umbrella_'+str(i+1),pos,r)
    # A-frame and pots stay in the furnishing zone, outside the through route.
    af=(-1.80,-4.50) if kind=='downtown' else (-4.35,-4.0) if kind=='strip' else (3.7,-3.0)
    add_piece('AFrame','Outdoor_AFrame',(*af,z),r,12 if kind!='pad' else -10)
    pots=([(-4.05,-4.78),(p['seating_zone'][1]-.31,-4.75)] if kind=='downtown' else [(-2.35,-5.37),(p['seating_zone'][1]-.33,-5.37)] if kind=='strip' else [(7.60,8.0),(9.95,.35),(1.35,-4.05)])
    for i,(x,y) in enumerate(pots):add_piece('Planter','Outdoor_Planter_'+str(i),(x,y,z),r)
    # Public fixtures are outside the cafe frontage to avoid choking the path.
    xx=p['width']/2+1.0 if kind!='pad' else 8.65;yy=-4.0 if kind!='pad' else -3.20
    for i,key in enumerate(('Litter','Recycling')):add_piece(key,'Outdoor_'+key,(xx+i*.85,yy,z),r)
    add_piece('BikeRack','Outdoor_BikeRack',(-p['width']/2-1.0,-3.75,z),r,90)
    return r


def paving(p,front):
    r=G.root('SiteWalk',parent=front,part='site');b=G.Batch('Site__PoursAndCurbs',r);z=p['grade'];w=p['width'];kind=p['kind']
    xmin=-w/2-2.3;xmax=w/2+2.8 if kind!='pad' else 11.2;dep=p['walk']
    # Individual pours and their real 3mm joints. No unscaled slab underneath.
    for i in range(math.ceil((xmax-xmin)/1.524)):
        a=xmin+i*1.524;c=min(xmax,a+1.524)
        for j in range(math.ceil(dep/1.524)):
            y=-dep+j*1.524;d=min(1.524,-y)
            x0=a+.0015;x1=c-.0015;y0=y+.0015;y1=y+d-.0015
            # Local wear needs samples on the exposed top only. The side
            # gauges remain single faces; no hidden bottom is exported.
            vs=[(x0+(x1-x0)*u/4,y0+(y1-y0)*v/4,z) for v in range(5) for u in range(5)]
            b.geom(vs,[(v*5+u,v*5+u+1,(v+1)*5+u+1,(v+1)*5+u) for v in range(4) for u in range(4)],'cream')
            ring=[(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)]
            b.geom(ring+[(xx,yy,z-.13) for xx,yy,zz in ring],[(k,(k+1)%4,(k+1)%4+4,k+4) for k in range(4)],'cream')
    if kind=='pad':
        b.box((8.2,4.25,z-.07),(5.8,8.50,.14),'cream')
    b.box(((xmin+xmax)/2,-dep-.075,z-.0762),(xmax-xmin,.15,.1524),'cream')
    walk=b.finish()
    # Reuse Ground's actual concrete atlas with world-projected UVs.
    con=tiling.material('Concrete',REPO/'ground/textures/ship',tint=True);walk.data.materials.clear();walk.data.materials.append(con)
    bpy.context.view_layer.update();tiling.world_uv(walk,3.048)
    from finishes import paving_age
    paving_age(walk,p)
    return r


def build(seed,kind):
    bpy.ops.wm.read_factory_settings(use_empty=True);add_piece.cache={};G.palette();p=generate(seed,kind)
    shop=G.root('CoffeeShop_'+str(seed),static_root=True,kind=kind,seed=seed)
    front=G.root('FrontFrame',(0,-p['depth']/2,0),shop,frame='front-center, ground',grade=p['grade'])
    roots,obs=import_piece(Path('build/hosts')/(kind+'.glb'),front,prefix='Host_')
    host_tri=sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in obs if o.type=='MESH')
    for o in obs:
        if o.type=='MESH':o['part']='host'
    fixtures(p,front);exterior(p,front);outside(p,front);paving(p,front)
    from finishes import placed
    placed(p,front)
    # Remove source templates; every instance retains its shared mesh data.
    for template in list(add_piece.cache.values()):
        for o in reversed(G.descendants(template)):bpy.data.objects.remove(o,do_unlink=True)
    bpy.context.view_layer.update();sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['stage']=p['stage']
    folder=Path('build/shops');folder.mkdir(parents=True,exist_ok=True);src=folder/(str(seed)+'.blend')
    bpy.ops.wm.save_as_mainfile(filepath=str(src.resolve()),compress=True)
    tiling.export(src.with_suffix('.glb'));meta=externalize(src.with_suffix('.glb'),Path('export')/f'CoffeeShop-{seed}.gltf')
    counts={}
    for ob in sc.objects:
        if ob.type!='MESH':continue
        par=ob
        while par.parent and par.parent!=front:par=par.parent
        key=par.name;counts[key]=counts.get(key,0)+sum(len(f.vertices)-2 for f in ob.data.polygons)
    p.update(host_triangles=host_tri,counts=counts,room_triangles=counts.get('Room',0),triangles=sum(counts.values()),**meta)
    p['bundle_sha256']=bundle(Path('export')/f'CoffeeShop-{seed}.gltf')
    p['sockets']={o.name:dict(position=list(o.matrix_world.translation),kind=o['socket_kind']) for o in sc.objects if o.get('socket_kind')}
    p['pivots']={o.name:dict(position=list(o.matrix_world.translation),axis=o['pivot_axis'],range=list(o['range_degrees'])) for o in sc.objects if o.get('pivot_axis')}
    if p['triangles']>=200000 or p['room_triangles']>=60000:raise ValueError(('Budget',p['triangles'],p['room_triangles']))
    src.with_suffix('.json').write_text(json.dumps(p,indent=2)+'\n');print('COFFEE',kind,seed,p['triangles'],p['room_triangles'],flush=True);return p


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=Path('build/coffee.blend'));a.add_argument('--seed',type=int);a.add_argument('--kind',choices=['downtown','strip','pad']);a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    graphics();library();rows=[build(seed,kind) for seed,kind in ([(a.seed,a.kind)] if a.seed is not None else PROOFS)]
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()),compress=True);a.out.with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n')
