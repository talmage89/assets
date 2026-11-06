"""Park interfaces, missing site fixtures and local library instances."""
import math,json
from pathlib import Path
import bpy
from mathutils import Vector
from geometry import *
from kit.fonts import find_font

def load(family):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path('build/context',family+'.glb').resolve()))
    added=set(bpy.context.scene.objects)-before
    return {o.name.split('.')[0]:o for o in added if o.parent not in added}

def remove(library):
    obs={o for r in library.values() for o in [r,*r.children_recursive]}
    for o in obs:bpy.data.objects.remove(o,do_unlink=True)

def rules_print(rt,town):
    """Three original signs in one temporary 1K sheet, not 8k glyph triangles.

    This sheet is folded into the planned trim atlas during look-dev.
    """
    from PIL import Image,ImageDraw,ImageFont
    path=Path('build/T_Skatepark_FormRules.png')
    towns=('ALDER GLEN','CEDAR JUNCTION','MILL CREEK')
    if bpy.data.materials.get('Skate_Form_Rules') is None:
        im=Image.new('RGB',(1024,1024),(44,66,61));draw=ImageDraw.Draw(im)
        for i,label in enumerate(towns):
            x=(i%2)*512;y=(i//2)*512;cx=x+192
            for text,yy,size,bold in [(label,30,26,True),('PARKS & RECREATION',70,17,False),('SKATE PARK',119,31,True),('OPEN DAWN TO DUSK',200,19,False),('HELMETS REQUIRED',237,19,True),('SHARE THE LINES',274,19,False),('NO GLASS / NO BIKES',311,18,False),('EST. '+str((2011,2004,1999)[i]),430,19,False)]:
                font=ImageFont.truetype(find_font('DejaVu Sans','Bold' if bold else 'Book'),size);draw.text((cx,y+yy),text,font=font,fill=(211,211,206),anchor='mm')
            draw.rectangle((x+16,y+16,x+368,y+490),outline=(211,211,206),width=2)
        im.save(path)
    mat=bpy.data.materials.get('Skate_Form_Rules')
    if mat is None:
        mat=material('Skate_Form_Rules',(.65,.65,.64),.7);node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(path.resolve()),check_existing=True);mat.node_tree.links.new(node.outputs['Color'],mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
    i=towns.index(town);u=(i%2)*.5;v=1-(i//2)*.5
    o=G.plane_uv('Rules original print',[(-.371,-.0476,1.153),(.371,-.0476,1.153),(.371,-.0476,2.147),(-.371,-.0476,2.147)],mat);o.parent=rt
    uv=o.data.uv_layers.active
    for f in o.data.polygons:
        for li in f.loop_indices:
            p=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(u+(p.x+.371)/.742*.375,v-.5+(p.z-1.153)/.994*.5)
    return o

def fountain():
    rt=root('DrinkingFountain','site');x,y=0,0
    cyl('Cast pedestal',(0,0,.01),(0,0,.78),.105,rt,'Paint',16)
    cyl('Pedestal flange',(0,0,.001),(0,0,.016),.17,rt,'Paint',20)
    # Two heights on a common pedestal; shallow bowls with real rolled rims.
    for s,z in ((-1,.865),(1,1.015)):
        cx=s*.27
        beam('Cantilever fountain arm',(0,0,z-.09),(cx,0,z-.09),.075,rt,'Paint')
        prof=[(z-.06,.04),(z-.035,.12),(z-.012,.175),(z,.18),(z+.005,.172),(z-.008,.16),(z-.030,.06)]
        own(G.lathe('Stainless drinking basin',prof,M['Zinc'],32,center=(cx,0),closed=True),rt)
        cyl('Bubbler mounting',(cx,-.095,z),(cx,-.095,z+.04),.02,rt,'Zinc',12)
        cyl('Drain',(cx,0,z-.03),(cx,0,z-.028),.017,rt,'Black',12)
        box('Push control',(cx,-.174,z-.012),(.055,.012,.027),rt,'Steel',.004)
    return rt

def shade():
    rt=root('ShadePavilion','site');w,d=6.096,4.8768
    for x in (-w/2+.20,w/2-.20):
        for y in (-d/2+.20,d/2-.20):
            box('Anchored pavilion column',(x,y,1.35),(.14,.14,2.70),rt,'Paint',.006)
            box('Column base shoe',(x,y,.02),(.25,.25,.04),rt,'Steel',.003)
            for sx in (-1,1):cyl('Pavilion slab anchor',(x+sx*.09,y,.04),(x+sx*.09,y,.06),.01,rt,'Zinc',6)
    for y in (-d/2+.2,d/2-.2):beam('Longitudinal eave beam',(-w/2,y,2.7),(w/2,y,2.7),.14,rt,'Paint')
    for x in (-w/2,-w/4,0,w/4,w/2):
        beam('Roof rafter',(x,-d/2-.25,2.70),(x,0,3.55),.10,rt,'Paint')
        beam('Roof rafter',(x,0,3.55),(x,d/2+.25,2.70),.10,rt,'Paint')
    for s in (-1,1):
        v=[(-w/2-.3,0,3.57),(w/2+.3,0,3.57),(w/2+.3,s*(d/2+.30),2.72),(-w/2-.3,s*(d/2+.30),2.72)]
        o=mesh('Standing seam metal shade roof',v,[(0,1,2,3)],rt,'Paint');m=o.modifiers.new('Closed roof sheet','SOLIDIFY');m.thickness=.0012;G.apply(o)
        for j in range(15):
            x=-w/2-.3+j*(w+.6)/14;beam('Raised roof seam',(x,0,3.58),(x,s*(d/2+.30),2.73),.022,rt,'Paint',.012)
    return rt

def bleacher():
    rt=root('ThreeRowBleacher','site');w=4.8768
    for j in range(3):
        y=j*.61;z=.43+j*.22
        box('Extruded aluminum seat',(0,y,z),(w,.25,.04),rt,'Zinc',.008)
        box('Aluminum footboard',(0,y-.24,z-.22),(w,.29,.035),rt,'Zinc',.003)
        for x in (-w*.4,0,w*.4):
            beam('Bolted bleacher leg',(x,y,.025),(x,y,z-.02),.05,rt,'Zinc')
    for x in (-w*.4,0,w*.4):beam('Bleacher diagonal brace',(x,-.3,.025),(x,1.35,.9),.04,rt,'Zinc')
    return rt

def site(p):
    W,D=p['skating'];SW,SD=p['site'];roots=[]
    rt=root('SitePaving','site');roots.append(rt)
    # Site turf excludes skating and parking footprints; bowl does not have a
    # hidden green plane running through it.
    for x0,x1,y0,y1 in [(-SW/2,-W/2-1,-SD/2,SD/2),(W/2+1,SW/2,-SD/2,SD/2),(-W/2-1,W/2+1,D/2+1,SD/2)]:
        box('Park lawn',((x0+x1)/2,(y0+y1)/2,-.04),(x1-x0,y1-y0,.06),rt,'Lawn',0)
    # Front parking lot, perpendicular stalls and a separate entry walkway.
    py=-D/2-8.5344
    box('Asphalt parking',(0,py,-.06),(W+12.192,12.192,.10),rt,'Asphalt',0)
    box('Level public walk',(0,-D/2-2.4384,-.05),(W+12.192,2.4384,.10),rt,'Concrete',.003)
    box('Street to gate walk',(0,-D/2-8.5344,-.025),(2.4384,14.6304,.05),rt,'Concrete',.002)
    for s in (-1,1):
        for i in range(5):
            x=s*(3.9624+i*2.7432)
            box('Parking stall stripe',(x,py-.65,.001),(.10,5.4864,.002),rt,'White',0)
            box('Precast wheel stop',(x-1.37,py+1.75,.075),(1.524,.15,.15),rt,'Concrete',.025)
    f=load('furniture')
    for i,loc in enumerate(p['benches']):roots.append(instance(f['Bench'],'Bench_'+str(i),loc,90 if i<2 else 180))
    for i,s in enumerate((-1,1)):roots.append(instance(f['Litter'],'Litter_'+str(i),(s*4,-D/2-2.2,0)))
    roots.append(instance(f['BikeRack'],'BikeRack',(3,-D/2-2.4,0)));remove(f)
    ft=fountain();ft.location=(-3,-D/2-2.1,0);roots.append(ft)
    if p['shade']:
        ft=shade();ft.location=(W/2+5.4864,6.096,0);roots.append(ft)
    if p['bleachers']:
        ft=bleacher();ft.location=(W/2+4,1.0,0);ft.rotation_euler.z=-math.pi/2;roots.append(ft)
    # Actual library chain sections, posts and working gate, on native 10ft pitch.
    f=load('chain');fence=root('PerimeterFence','site');roots.append(fence)
    nx=math.ceil((W+2.4384)/3.048);ny=math.ceil((D+2.4384)/3.048)
    fx=nx*3.048/2;fy=ny*3.048/2
    entry_opening=6.096 if nx%2==0 else 3.048
    for y,yaw in ((-fy,0),(fy,0)):
        for i in range(nx):
            x=(i-(nx-1)/2)*3.048
            if y<0 and abs(x)<1.6:continue
            instance(f['Chain_Section'],'Chain section',(x,y,0),yaw,fence)
        for i in range(nx+1):
            x=(i-nx/2)*3.048
            if y<0 and abs(x)<entry_opening/2-.001:continue
            instance(f['Chain_Line'],'Chain post',(x,y,0),yaw,fence)
    # Two trimmed side runs fit the chosen park pad exactly at native pitch.
    for x in (-fx,fx):
        N=ny
        for i in range(N):instance(f['Chain_Section'],'Chain side',(x,(i-(N-1)/2)*3.048,0),90,fence)
        for i in range(1,N):instance(f['Chain_Line'],'Chain side post',(x,(i-N/2)*3.048,0),90,fence)
    gate=instance(f['Chain_GateBay'],'ParkGate',(0,-fy,0),0,fence)
    for s in (-1,1):
        # Low infill to the wider 10ft entry bay around the native pedestrian gate.
        # Horizontal library bays straddle the origin: a 6.096m opening was
        # reserved by the two omitted bays. Infill meets gate-post centers.
        gate_pitch=1.069975;length=(entry_opening-gate_pitch)/2
        ob=instance(f['Chain_Section'],'Gate infill',(s*(gate_pitch/2+length/2),-fy,0),0,fence);ob.scale.x=length/3.048
    remove(f)
    sign=root('RulesSign','site');sign.location=(1.20,-D/2-2.0,0);roots.append(sign)
    cyl('Rules post',(0,0,0),(0,0,2.2),.03016,sign,'Zinc',12)
    box('Municipal sign back',(0,-.045,1.65),(.762,.003,1.016),sign,'Paint',.016)
    rules_print(sign,p['town'])
    for z in (1.30,2.0):cyl('Rules sign fixing',(0,-.047,z),(0,-.052,z),.004,sign,'Zinc',6)
    f=load('tree')
    for i,loc in enumerate(p['trees']):roots.append(instance(next(iter(f.values())),'ParkMaple_'+str(i),loc,(i*71+p['seed'])%360))
    remove(f)
    f=load('light')
    for i,loc in enumerate(((-W/2-3,-D/2+3,0),(W/2+3,D/2-3,0))):roots.append(instance(next(iter(f.values())),'ParkLight_'+str(i),loc,i*180))
    remove(f)
    return roots
