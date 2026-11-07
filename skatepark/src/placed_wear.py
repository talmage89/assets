"""Placement-owned contact wear; four shared smears, never reusable-sector stamps.

All paths are in the feature's construction frame. Existing ride-line axes
choose approaches; bowl entries and pocket carves choose circumferential paths.
Every vertex is projected onto the actual game triangles before consolidation.
"""
import json,math,random
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import geometry as Q
from textures import RECTS


def substrate(roots,frame):
    vertices=[];faces=[]
    for rt in roots:
        for ob in rt.children_recursive:
            if ob.type!='MESH' or ob.get('surface_mark') or ob.get('fallen_litter'):continue
            n=len(vertices);T=frame.matrix_world.inverted()@ob.matrix_world
            vertices.extend(T@v.co for v in ob.data.vertices)
            ob.data.calc_loop_triangles()
            faces.extend(tuple(n+i for i in t.vertices) for t in ob.data.loop_triangles
                         if ob.data.materials[t.material_index].name.startswith(('Skate_Concrete','Skate_Trim_Steel')))
    return BVHTree.FromPolygons(vertices,faces,all_triangles=True)


def stroke(rt,tree,points,width,variant,opacity,cause,key='Scrape'):
    """Metric strip, soft baked edges; no new material or image allocation."""
    from finishes import ribbon
    rows=[];normals=[]
    for i,p in enumerate(points):
        p=Vector(p);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        hit,n,_,distance=tree.find_nearest(p)
        assert distance<.08,(rt.name,cause,distance)
        across=t.cross(n).normalized()
        row=[]
        for sign in (-1,1):
            q,normal,_,d=tree.find_nearest(hit+across*(sign*width/2))
            row.append(q+normal*.0012);normals.append(normal)
        rows.append(row)
    ob=ribbon(rt,cause,rows,width,key,normals=normals)
    if key=='Scrape':
        u0,v0,u1,v1=RECTS[key];pad=8/2048;cell=(u1-u0)/4
        for i,row in enumerate(ob.data.uv_layers.active.data):
            v=ob.data.loops[i].vertex_index
            row.uv=(u0+variant*cell+pad+(v%2)*(cell-2*pad),v0+pad+(v//2)/(len(points)-1)*(v1-v0-2*pad))
    for row in ob.data.color_attributes['Tint'].data:row.color=(1,1,1,opacity)
    length=sum((Vector(b)-Vector(a)).length for a,b in zip(points,points[1:]))
    data=json.loads(rt.get('placed_wear_json','[]'))
    data.append(dict(cause=cause,width_m=width,length_m=length,variant=variant,opacity=opacity,
                     triangles=sum(len(f.vertices)-2 for f in ob.data.polygons),
                     start_local_m=list(points[0]),end_local_m=list(points[-1])))
    rt['placed_wear_json']=json.dumps(data)
    return ob


def feature_contacts(rt,p,age,rng):
    if not any(k in rt for k in ('profile_run_m','bank_angle_degrees')) and not rt.name.startswith(('Ledge_18in','ManualPad','Prefab_GrindBox')):return
    import bpy
    bpy.context.view_layer.update();tree=substrate([rt],rt)
    if 'profile_run_m' in rt:
        r=rt['transition_radius_m'];L=rt['profile_run_m'];a=math.acos(1-rt['height_m']/r);w=rt['footprint_m'][0]
        for lane in range(2 if age<.5 else 3):
            x=(lane-(.5 if age<.5 else 1))*w*.25+rng.uniform(-.13,.13)*w
            # A short slide at the lip and a longer landing mark at the toe.
            for zone in ('lip','toe'):
                start=a-rng.uniform(.38,.85)/r if zone=='lip' else rng.uniform(.05,.25)/r
                length=rng.uniform(.35,.85) if zone=='lip' else rng.uniform(.7,1.3)
                end=min(a-.015/r,start+length/r)
                bend=rng.uniform(-.12,.12)
                for wheel in (-1,1):
                    points=[]
                    for j in range(25):
                        t=j/24;theta=start+(end-start)*t
                        points.append(Vector((x+wheel*.072+bend*math.sin(t*math.pi),-L/2+r*math.sin(theta),r*(1-math.cos(theta)))))
                    stroke(rt,tree,points,rng.uniform(.022,.034),rng.randrange(4),.45+age*.35,'Wheel slide on '+zone+' of placed ride line')
    elif rt.name.startswith(('Bank','PlazaBank')):
        h=rt['height_m'];angle=math.radians(rt['bank_angle_degrees']);run=h/math.tan(angle)+.18*math.tan(angle/2);w=rt['footprint_m'][0]
        for k in range(2):
            x=w*((k-.5)*.45+rng.uniform(-.08,.08));lo=-run/2+.25;hi=lo+rng.uniform(.5,1.0)
            for wheel in (-1,1):
                points=[Vector((x+wheel*.072+.025*math.sin(j*.15),lo+(hi-lo)*j/20,h-(run/2-(lo+(hi-lo)*j/20))*math.tan(angle))) for j in range(21)]
                stroke(rt,tree,points,.028,rng.randrange(4),.45+age*.3,'Wheel landing below bank approach')
    if rt.name.startswith(('Ledge_18in','ManualPad','Prefab_GrindBox')):
        w,length=rt['footprint_m'];h=rt['height_m']
        for side in (-1,1):
            # Trucks/boards scrape the first few centimeters below the armor,
            # along travel. No wheel arcs can be applied to the retaining face.
            for k in range(2 if age<.5 else 4):
                y=rng.uniform(-length*.42,length*.24);span=rng.uniform(.18,.45)
                pts=[Vector((side*w/2,y+span*j/12,h-.018-.008*math.sin(j*.12))) for j in range(13)]
                stroke(rt,tree,pts,.022,rng.randrange(4),.65,'Truck scrape just below ledge top edge')


def bowl_contacts(roots,p):
    if not p['bowl']:return
    import bpy,bowl
    sectors=sorted([r for r in roots if 'Bowl_Sector' in r.name],key=lambda r:r.name)
    bpy.context.view_layer.update();tree=substrate(sectors,sectors[0]);rng=random.Random(p['seed']+2701)
    bowl.SHAPE=p['bowl']['shape'];age=p['age']
    # Different visits to the entry, shallow pocket, waist and deep pocket.
    # Global paths cross sector boundaries; several sectors have no mark.
    for i in range(11 if p['year']==2011 else 18):
        t=rng.uniform(0,math.tau);u=rng.uniform(.10,.24) if i%3 else rng.uniform(.68,.86)
        sweep=rng.uniform(.065,.17)*rng.choice((-1,1));rise=rng.uniform(-.035,.08)
        owner=sectors[min(15,int(t/math.tau*16))]
        for wheel in (-1,1):
            pts=[]
            for j in range(33):
                f=j/32;tt=t+sweep*f;uu=u+rise*f+wheel*.018
                pts.append(bowl.station(tt,uu))
            stroke(owner,tree,pts,rng.uniform(.024,.037),rng.randrange(4),.54+age*.30,'Pocket carve from park bowl ride line')
    # Burnished toe carves are longer and translucent, never a warm wall fade.
    for i in range(5 if p['year']==2011 else 8):
        t=rng.uniform(0,math.tau);owner=sectors[min(15,int(t/math.tau*16))]
        pts=[bowl.station(t+.32*j/48,.065+.025*math.sin(j*.05+i)) for j in range(49)]
        stroke(owner,tree,pts,.16,rng.randrange(4),.30+age*.20,'Burnished low transition carve',key='Burnish')
    return sectors


def report(roots):
    rows=[dict(placement=rt.name,marks=json.loads(rt['placed_wear_json'])) for rt in roots if 'placed_wear_json' in rt]
    return dict(placements=rows,triangles=sum(m['triangles'] for r in rows for m in r['marks']),
                strokes=sum(len(r['marks']) for r in rows),new_texture_bytes=0,new_texture_memory_MiB=0,
                material='Existing Skate_Trim_Burnish BLEND; joined into each placement before export')
