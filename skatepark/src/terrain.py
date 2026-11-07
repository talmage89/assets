"""Connected poured terrain; the accepted section modules remain reusable.

Wing banks close exposed transition ends. Continuous decks and a raised street
plaza join the pours. At real junctions, buried faces are removed from placed
copies only; no source module section is changed.
"""
import math,json
import bpy,bmesh
from mathutils import Vector
import geometry as Q
from kit import model as G

def rectangle_skin(rt,name,rect,z,mat='Concrete'):
    x0,x1,y0,y1=rect
    return Q.mesh(name,[(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)],[(0,1,2,3)],rt,mat)

def subtract(rect,cuts):
    parts=[rect]
    for hx0,hx1,hy0,hy1 in cuts:
        result=[]
        for x0,x1,y0,y1 in parts:
            a,b=max(x0,hx0),min(x1,hx1);c,d=max(y0,hy0),min(y1,hy1)
            if a>=b or c>=d:result.append((x0,x1,y0,y1));continue
            result += [(x0,a,y0,y1),(b,x1,y0,y1),(a,b,y0,c),(a,b,d,y1)]
        parts=[r for r in result if r[1]-r[0]>1e-5 and r[3]-r[2]>1e-5]
    return parts

def world_rect(rect,item):
    x0,x1,y0,y1=rect;a=math.radians(item['yaw']);c,s=math.cos(a),math.sin(a);x,y,z=item['location']
    points=[(x+u*c-v*s,y+u*s+v*c) for u,v in ((x0,y0),(x1,y0),(x1,y1),(x0,y1))]
    return [min(p[0] for p in points),max(p[0] for p in points),min(p[1] for p in points),max(p[1] for p in points)]

def close_run(p,lib,run):
    items=sorted([p['placements'][i] for i in run['indices']],key=lambda m:m['location'][0]);source=lib[items[0]['piece']]
    w=source['footprint_m'][0];h=source['height_m'];deck=source['deck_m']
    rt=Q.root('Connected_'+run['name']);rt['construction']='continuous deck and 20 degree wing returns'
    if 'transition_radius_m' in source:
        r=source['transition_radius_m'];a=math.acos(1-h/r);L=source['profile_run_m']
        profile=[(-L/2+r*math.sin(a*j/40),r*(1-math.cos(a*j/40))) for j in range(41)]+[(L/2+deck,h)]
    else:
        a=math.radians(20);L=h/math.tan(a)+.18*math.tan(a/2)
        profile=[(-L/2+.18*math.sin(a*j/8),.18*(1-math.cos(a*j/8))) for j in range(9)]+[(L/2,h),(L/2+deck,h)]
    for s,item in ((-1,items[0]),(1,items[-1])):
        # Author in module frame, then place the complete terrain return.
        local=Q.root('Wing_'+run['name']+'_'+str(s));x=s*w/2;verts=[];faces=[]
        for y,z in profile:
            verts.extend([(x,y,z),(x+s*z/math.tan(math.radians(20)),y,0)])
        for j in range(len(profile)-1):
            a=2*j
            faces.append((a,a+3,a+2) if j==0 else (a,a+1,a+3,a+2))
        ob=Q.mesh('Monolithic side bank, tangent to the end section',verts,faces,local,smooth=False)
        # Recalculate from actual geometry; no smoothing across the deck arris.
        bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
        for f in bm.faces:
            if f.normal.z<0:f.normal_flip()
        bm.to_mesh(ob.data);bm.free()
        y,z=profile[-1];Q.mesh('Wing rear retaining closure',[(x,y,z),(x+s*z/math.tan(math.radians(20)),y,0),(x,y,0)],[(0,1,2) if s>0 else (2,1,0)],local)
        local.location=item['location'];local.rotation_euler.z=math.radians(item['yaw']);Q.join(local)
        # Parent while keeping the module's placement in the park frame.
        local.parent=rt
    if not run.get('shared_deck',True):return rt,None
    # Extend the level deck behind the entire contiguous row.
    first,last=items[0],items[-1];z=first['location'][2]+h
    xa=first['location'][0]-w/2;xb=last['location'][0]+w/2
    front=first['location'][1]+(profile[-1][0] if first['yaw']==0 else -profile[-1][0])
    back=(p['skating'][1]/2-.6096) if first['yaw']==0 else (-p['skating'][1]/2+.1524)
    y0,y1=sorted((front,back))
    if y1-y0>.001:
        rectangle_skin(rt,'Shared deck behind adjoining pours',(xa,xb,y0,y1),z)
        Q.mesh('Deck retaining rear wall',[(xa,back,z),(xb,back,z),(xb,back,-.15),(xa,back,-.15)],[(0,1,2,3) if back>front else (3,2,1,0)],rt)
        for x in (xa,xb):
            reverse=(back>front)!=(x==xa)
            Q.mesh('Deck end return',[(x,front,z),(x,back,z),(x,back,0),(x,front,0)],[(3,2,1,0) if reverse else (0,1,2,3)],rt)
        if run['name'].startswith('north'):guard(rt,xa,xb,back,lambda x:z)
    rt['deck_bounds_m']=[xa,xb,y0,y1];rt['deck_height_m']=z
    return rt,[xa,xb,y0,y1]

def guard(rt,x0,x1,y,height):
    """42in welded municipal deck guard; the real square sections carry it."""
    top=1.0668;y-=.10
    for j in range(math.ceil((x1-x0)/1.8288)+1):
        x=x0+.10+(x1-x0-.20)*j/math.ceil((x1-x0)/1.8288);z=height(x)
        Q.beam('Anchored square deck guard post',(x,y,z),(x,y,z+top),.0508,rt,'Paint')
        Q.profile('Guard base flange seated on graded deck',[(x-.065,height(x-.065)),(x+.065,height(x+.065)),(x+.065,height(x+.065)+.012),(x-.065,height(x-.065)+.012)],y-.065,y+.065,rt,'Zinc',axis='Y')
    for h in (.10,top):Q.beam('Continuous welded guard rail',(x0,y,height(x0)+h),(x1,y,height(x1)+h),.0381,rt,'Paint')
    count=math.ceil((x1-x0)/.115)
    for j in range(1,count):
        x=x0+(x1-x0)*j/count;z=height(x)
        Q.beam('19mm guard picket',(x,y,z+.10),(x,y,z+top),.01905,rt,'Paint')

def north_connection(p,rows):
    """A continuous sloping deck joins both transition runs behind the park."""
    west,east=sorted([r for r in rows if r.name.startswith('Connected_north')],key=lambda r:r['deck_bounds_m'][0])
    x0=west['deck_bounds_m'][1];x1=east['deck_bounds_m'][0]
    y0=max(west['deck_bounds_m'][2],east['deck_bounds_m'][2]);y1=min(west['deck_bounds_m'][3],east['deck_bounds_m'][3])
    z0=west['deck_height_m'];z1=east['deck_height_m'];rt=Q.root('NorthDeckConnection');span=x1-x0
    def top(x):return z0+(z1-z0)*(x-x0)/span
    def bottom(x):
        # The neighboring wing banks already own the wall below this line.
        a=z0-max(0,x-x0)*math.tan(math.radians(20))
        b=z1-max(0,x1-x)*math.tan(math.radians(20))
        return max(0,a if x-x0<1.2192/math.tan(math.radians(20)) else 0,b if x1-x<1.2192/math.tan(math.radians(20)) else 0)
    xs=sorted(set([x0,x1,x0+1.2192/math.tan(math.radians(20)),x1-1.2192/math.tan(math.radians(20))]+[x0+span*j/12 for j in range(13)]))
    for a,b in zip(xs,xs[1:]):
        Q.mesh('Graded deck connects the transition runs',[(a,y0,top(a)),(b,y0,top(b)),(b,y1,top(b)),(a,y1,top(a))],[(0,1,2,3)],rt)
        verts=[(a,y0,bottom(a)),(b,y0,bottom(b)),(b,y0,top(b)),(a,y0,top(a))]
        if abs(top(a)-bottom(a))<1e-6:face=(0,1,2)
        elif abs(top(b)-bottom(b))<1e-6:face=(0,1,3)
        else:face=(0,1,2,3)
        Q.mesh('Exposed formed retaining wall between wing returns',verts,[face],rt)
        Q.mesh('Continuous north retaining back',[(a,y1,-.15),(b,y1,-.15),(b,y1,top(b)),(a,y1,top(a))],[(3,2,1,0)],rt)
    guard(rt,x0,x1,y1,top);rt['deck_slope']=abs(z1-z0)/span
    return rt,[x0,x1,y0,y1]

def guard_contacts(roots):
    """Probe actual plate underside vertices against actual deck triangles."""
    from mathutils.bvhtree import BVHTree
    bpy.context.view_layer.update();decks=[];plates=[]
    for root in roots:
        for ob in root.children_recursive:
            if ob.type!='MESH':continue
            if ob.name.startswith(('Shared deck behind','Graded deck connects')):decks.append(ob)
            elif ob.name.startswith('Guard base flange seated'):plates.append(ob)
    if not plates:return None
    vertices=[];faces=[]
    for ob in decks:
        n=len(vertices);vertices += [ob.matrix_world@v.co for v in ob.data.vertices]
        ob.data.calc_loop_triangles();faces += [tuple(n+i for i in t.vertices) for t in ob.data.loop_triangles]
    tree=BVHTree.FromPolygons(vertices,faces,all_triangles=True);errors=[]
    for ob in plates:
        for face in ob.data.polygons:
            if face.normal.z>-.9:continue
            for index in face.vertices:
                point=ob.matrix_world@ob.data.vertices[index].co
                hit=tree.ray_cast(point+Vector((0,0,.03)),Vector((0,0,-1)),.1)[0]
                assert hit is not None,('Unsupported deck guard flange',ob.name,list(point))
                errors.append(abs(hit.z-point.z))
    assert errors and max(errors)<2e-5,errors
    return dict(plates=len(plates),actual_underside_samples=len(errors),maximum_contact_error_m=max(errors),scope='Source triangle-surface contacts; serialization is verified separately by GLB re-import')

def build(p,lib):
    if p['type']!='poured':return [],[]
    roots=[];cuts=[]
    for run in p['transition_runs']:
        rt,cut=close_run(p,lib,run);roots.append(rt)
        if cut:cuts.append(cut)
    rt,cut=north_connection(p,roots);roots.append(rt);cuts.append(cut)
    plaza=p['plaza'];x0,x1,y0,y1=plaza['bounds'];h=plaza['height']
    rt=Q.root('UpperStreetPlaza');roots.append(rt);cuts.append([x0,x1,y0,y1])
    topcuts=list(cuts[:-1])
    for item in p['placements']:
        source=lib[item['piece']]
        if item['location'][2]>=h-.0001 or item['piece'].startswith(('Stairs','PlazaBank')):
            topcuts += [world_rect(c,item) for c in json.loads(source.get('ground_cut_json','[]'))]
    for xa in [x0+i*3.048 for i in range(math.ceil((x1-x0)/3.048))]:
        for ya in [y0+i*3.048 for i in range(math.ceil((y1-y0)/3.048))]:
            for rect in subtract((xa+.0015,min(xa+3.048,x1)-.0015,ya+.0015,min(ya+3.048,y1)-.0015),topcuts):
                rectangle_skin(rt,'Upper plaza saw-cut troweled pour',rect,h)
    frontcuts=[]
    for item in p['placements']:
        if item['piece'].startswith(('Stairs','PlazaBank')):
            rects=json.loads(lib[item['piece']]['ground_cut_json'])
            frontcuts.append((item['location'][0]+min(r[0] for r in rects),item['location'][0]+max(r[1] for r in rects)))
    intervals=[(x0,x1)]
    for a,b in frontcuts:
        intervals=[q for c,d in intervals for q in ((c,min(d,a)),(max(c,b),d)) if q[1]-q[0]>.0001]
    for a,b in intervals:
        Q.mesh('Street terrace formed front wall',[(a,y0,0),(b,y0,0),(b,y0,h),(a,y0,h)],[(0,1,2,3)],rt)
        Q.box('Sealed rounded terrace nosing',((a+b)/2,y0,h-.025),(b-a,.08,.05),rt,r=.008)
    # Retaining edge and planted spectator pocket are at the outside of the run.
    for xa in (x0,x1):Q.mesh('Plaza perimeter retaining wall',[(xa,y0,0),(xa,y1,0),(xa,y1,h),(xa,y0,h)],[(3,2,1,0) if xa==x0 else (0,1,2,3)],rt)
    Q.mesh('Plaza rear retaining wall',[(x0,y1,0),(x1,y1,0),(x1,y1,h),(x0,y1,h)],[(3,2,1,0)],rt)
    planter=Q.root('SpectatorPlanter');roots.append(planter)
    mirror=-1 if p['layout_mirror'] else 1
    cx=mirror*(p['skating'][0]/2-.70);cy=y0+4.8768
    for side in (-1,1):
        Q.box('Cast planter long wall',(cx+side*.265,cy,(h+.45)/2),(.12,6.096,h+.45),planter,r=.008)
        Q.box('Cast planter end return',(cx,cy+side*2.988,(h+.45)/2),(.41,.12,h+.45),planter,r=.008)
    Q.box('Soil recessed below the actual planter rim',(cx,cy,h+.324),(.41,5.856,.012),planter,'Leaf' if 'Walk' in Q.M else 'Joint',0)
    # Two stepped seat terraces at the outside of the bowl deck.
    seats=Q.root('BowlSpectatorSteps');roots.append(seats)
    for j in range(2):
        Q.box('Cast spectator terrace',(mirror*(-p['skating'][0]/2+.60+j*.48),-.8,.15*(2-j)),(.48,5.4864,.30*(2-j)),seats,r=.006)
    return roots,cuts


def bury_seams(rt,item,p):
    """Delete internal end caps from placed copies at a continuous pour seam."""
    for run in p.get('transition_runs',[]):
        items=sorted([p['placements'][i] for i in run['indices']],key=lambda m:m['location'][0])
        if item not in items:continue
        index=items.index(item);w=rt['footprint_m'][0]
        for ob in rt.children_recursive:
            if ob.type!='MESH':continue
            ob.data=ob.data.copy();bm=bmesh.new();bm.from_mesh(ob.data)
            dead=[f for f in bm.faces if 'Concrete' in ob.data.materials[f.material_index].name and (all(abs(v.co.x+w/2)<1e-5 for v in f.verts) or all(abs(v.co.x-w/2)<1e-5 for v in f.verts))]
            bmesh.ops.delete(bm,geom=dead,context='FACES');bm.to_mesh(ob.data);bm.free()
