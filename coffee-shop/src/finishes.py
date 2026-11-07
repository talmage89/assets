"""Placed causal age on shared charts; no per-seed texture allocations.

High frequency manufacture is in the baked atlas. Macro age uses glTF COLOR_0
and bounded alpha marks, each placed by its physical cause after assembly.
"""
import json,math,random
import bpy
import geometry as G

def tint(ob,fn):
    ob.data=ob.data.copy();me=ob.data
    attr=me.color_attributes.get('Tint') or me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=attr
    for face in me.polygons:
        for li in face.loop_indices:
            p=me.vertices[me.loops[li].vertex_index].co
            old=attr.data[li].color;rgb=fn(p,face)
            attr.data[li].color=(*(min(1,max(0,c)) for c in rgb),1)

def stock(root,key):
    for ob in root.children_recursive:
        if ob.type!='MESH' or not ob.name.startswith(key):continue
        if key=='BistroChair':
            # Drag abrasion occurs on the lower leg surfaces. Preserve every
            # accepted vertex and triangle; sample only the actual foot zone.
            def f(p,face):
                a=.18*math.exp(-((p.z-.045)/.037)**2);return (1-a,1-a*.8,1-a*.6)
            tint(ob,f)
            # Remap existing leg faces; texture V follows actual local height.
            # This leaves the accepted 2,156 triangles entirely unchanged.
            uv=ob.data.uv_layers.active;a,b,c,d=G.LAYOUT['leg_wear'];roles=json.loads(ob['cafe_roles']);semantic=ob.data.attributes['CafeRole']
            for face in ob.data.polygons:
                ps=[ob.data.vertices[i].co for i in face.vertices];lo=min(p.z for p in ps);hi=max(p.z for p in ps)
                if roles[semantic.data[face.index].value]=='black' and lo<.030 and hi>.15 and abs(face.normal.z)<.8:
                    old=G.LAYOUT['black']
                    for li in face.loop_indices:
                        q=ob.data.vertices[ob.data.loops[li].vertex_index].co;u=(uv.data[li].uv.x-old[0])/(old[2]-old[0]);uv.data[li].uv=(a+u*(c-a),b+(q.z-lo)/(hi-lo)*(d-b))

def flat_mark(batch,x,y,z,w,d,key,angle=0):
    a=math.radians(angle);verts=[]
    for xx,yy in ((-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)):
        verts.append((x+xx*math.cos(a)-yy*math.sin(a),y+xx*math.sin(a)+yy*math.cos(a),z))
    batch.print(verts,key)

def paving_age(ob,p):
    rng=random.Random(p['seed']+817);sites=[]
    for t in p['tables']:
        for j in range(3):sites.append((t['x']+rng.uniform(-.52,.52),t['y']+rng.uniform(-.44,.44),rng.uniform(.34,.56),rng.uniform(.28,.46),rng.uniform(.24,.40)))
    sites.extend((p['entry'][0]+rng.uniform(-.32,.32),-.35-j*.30,.28,.43,.13) for j in range(4))
    attr=ob.data.color_attributes['Tint'];age={'downtown':.9,'strip':1.0,'pad':.85}[p['kind']]
    for face in ob.data.polygons:
        for li in face.loop_indices:
            q=ob.data.vertices[ob.data.loops[li].vertex_index].co
            stain=sum(s*math.exp(-(((q.x-x)/w)**2+((q.y-y)/d)**2)**1.3) for x,y,w,d,s in sites)
            stain=min(.50,stain*age)*(.85+.15*math.sin(q.x*27+q.y*18)**2)
            edge=.09*math.exp(-abs(q.y)/.13) if p['kind']=='downtown' else 0
            shade=1-stain-edge;attr.data[li].color=(shade,shade*(1-.018*stain),shade*(1-.05*stain),1)


def room_floor_age(ob,p):
    roles=json.loads(ob['cafe_roles']);semantic=ob.data.attributes['CafeRole'];colors=ob.data.color_attributes['Tint'];a=math.radians(p['counter_yaw']);co=math.cos(a);sn=math.sin(a);age={'downtown':.35,'strip':1.,'pad':.85}[p['kind']]
    for face in ob.data.polygons:
        if roles[semantic.data[face.index].value]!='floor':continue
        for li in face.loop_indices:
            q=ob.data.vertices[ob.data.loops[li].vertex_index].co;dx=(q.x-p['counter_x'])*co+(q.y-p['counter_y'])*sn;dy=-(q.x-p['counter_x'])*sn+(q.y-p['counter_y'])*co
            tracked=math.exp(-((dx+.55+.10*math.sin(dy*2))/.50)**2-((dy+1.35)/1.05)**4)
            handoff=.5*math.exp(-((dx-.45)/.65)**2-((dy+.72)/.32)**2)
            loss=.26*age*min(1,tracked+handoff)*(.85+.15*math.sin(q.x*17+q.y*21)**2)
            colors.data[li].color=(1-loss,1-loss*.98,1-loss*.93,1)


def table_mark(batch,front,t,x,y,w,d,key,angle):
    """Clip wear onto actual cast/steel top faces; never bridge lattice holes."""
    from check import clip
    from mathutils import Vector
    root=next(o for o in front.children_recursive if o.name==t['id']);inv=front.matrix_world.inverted();a=math.radians(angle);co=math.cos(a);sn=math.sin(a);rect=G.LAYOUT[key]
    for ob in root.children_recursive:
        if ob.type!='MESH':continue
        xf=inv@ob.matrix_world
        for face in ob.data.polygons:
            if (xf.to_3x3()@face.normal).z<.8:continue
            q=[xf@ob.data.vertices[i].co for i in face.vertices]
            if min(p.z for p in q)<(.754 if t['accessible'] else .725)+front.get('grade',0):continue
            poly=[((p.x-x)*co+(p.y-y)*sn,-(p.x-x)*sn+(p.y-y)*co,p.z) for p in q]
            for axis,value,above in ((0,-w/2,True),(0,w/2,False),(1,-d/2,True),(1,d/2,False)):
                if len(poly)<3:break
                poly=clip(poly,axis,value,above)
            if len(poly)<3:continue
            vs=[(x+u*co-v*sn,y+u*sn+v*co,z+.00035) for u,v,z in poly];uv=[(rect[0]+(u/w+.5)*(rect[2]-rect[0]),rect[1]+(v/d+.5)*(rect[3]-rect[1])) for u,v,z in poly]
            batch.geom(vs,[tuple(range(len(vs)))],key,uv)


def placed(p,front):
    seed=p['seed'];rng=random.Random(seed+295);z=p['grade'];kind=p['kind'];age={'downtown':.30,'strip':.85,'pad':1.0}[kind]
    marks=G.root('PlacedUseHistory',parent=front,part='site_wear');b=G.Batch('Placed coffee rings and customer spills',marks)
    for t in p['tables']:
        for j in range(2):
            table_mark(b,front,t,t['x']+rng.uniform(-.24,.24),t['y']+rng.uniform(-.21,.21),.083,.082,'ring',rng.uniform(0,360))
        table_mark(b,front,t,t['x']-.15,t['y']-.18,.08,.035,'scuff',rng.uniform(-35,35))
        # Spills are below customers' seats and table rims, not a continuous
        # dirty band around the entire patio or every furniture footprint.
        flat_mark(b,t['x']+rng.uniform(-.6,.6),t['y']-.42,z+.0012,.20+.22*age,.14+.13*age,'spill',rng.uniform(0,360))
        for j in range(3 if kind!='downtown' else 1):
            x=t['x']+rng.uniform(-.9,.9);y=t['y']+rng.uniform(-.62,.62)
            # Flattened gum has an irregular angular edge, 12–23 mm across.
            rad=rng.uniform(.006,.012);n=7;vs=[(x+rad*rng.uniform(.6,1.1)*math.cos(k*math.tau/n),y+rad*rng.uniform(.6,1.1)*math.sin(k*math.tau/n),z+.0015) for k in range(n)]
            b.geom(vs,[tuple(range(n))],'rubber')
    # Sidewalk history stays on the old downtown slabs even with fresh paint.
    if kind=='downtown':
        for j in range(9):flat_mark(b,rng.uniform(-4.2,4.2),rng.uniform(-5.8,-.4),z+.001,.25,.12,'spill',rng.uniform(0,360))
    if kind!='downtown':
        entry=p['entry'][0]
        for j in range(7):flat_mark(b,entry+rng.uniform(-.3,.3),rng.uniform(-1.7,-.3),z+.001,.22,.09,'scuff',rng.uniform(-20,20))
    b.finish()
    # The customer queue is a continuous floor-owned field, not repeated dots.
    for ob in front.children_recursive:
        if ob.type!='MESH':continue
        if ob.get('awning_cloth'):
            # Remap just cloth, not welded supports. Top exposure lightens
            # old canvas; valance lower edge is where runoff deposits remain.
            roles=json.loads(ob.get('cafe_roles','[]'));att=ob.data.attributes.get('CafeRole')
            colors=ob.data.color_attributes.get('Tint')
            if colors:
                top=3.52 if kind=='downtown' else 2.98;dep=1.12 if kind=='strip' else 1.42
                for f in ob.data.polygons:
                    for li in f.loop_indices:
                        q=ob.data.vertices[ob.data.loops[li].vertex_index].co
                        fade=.13*age*(.6+.4*math.sin(q.x*.6+seed)) if q.z>top-.39 else 0
                        grime=.32*age*math.exp(-((q.z-(top-.60))/.10)**2)*(.65+.35*math.sin(q.x*21)**2)
                        colors.data[li].color=(1-grime,1-grime*.94,1-grime*.88,1)
                # Fabric upper chart: a sun-bleached edge rather than turning
                # the entire fixture the same pale tone.
                uv=ob.data.uv_layers.active
                for f in ob.data.polygons:
                    if att and roles[att.data[f.index].value]==p['palette'] and sum(ob.data.vertices[i].co.z for i in f.vertices)/len(f.vertices)>top-.39 and age>.7:
                        old=G.LAYOUT[p['palette']];new=G.LAYOUT[p['palette']+'_faded']
                        for li in f.loop_indices:
                            # Fading is encoded in its own existing swatch;
                            # keep hue, lift only the worn exposed yarn color.
                            colors.data[li].color=(1,.94,.88,1)
                            u,v=uv.data[li].uv;uv.data[li].uv=(new[0]+(u-old[0])/(old[2]-old[0])*(new[2]-new[0]),new[1]+(v-old[1])/(old[3]-old[1])*(new[3]-new[1]))
        if 'Outdoor__Boundary' in ob.name and kind=='strip':
            # Narrow pale hits where chair backs meet the rail, using the
            # existing material's steel cell on actual face surfaces.
            uv=ob.data.uv_layers.active
            if uv:
                a,bv,c,d=G.LAYOUT['steel']
                for f in ob.data.polygons:
                    q=f.center
                    if .80<q.z-z<1.04 and any(abs(q.x-t['x'])<.22 for t in p['tables']) and f.index%4==0:
                        for li in f.loop_indices:uv.data[li].uv=((a+c)/2,(bv+d)/2)
    if kind=='pad':
        # Sparse cracks and repaint patches on the exposed original stucco.
        b=G.Batch('Pad local stucco repairs',marks)
        for x,h in ((-4.40,1.65),(4.73,2.2)):
            b.panel(x,-.026,h,.43,.021,'crack');b.panel(x+.12,-.027,h-.26,.24,.018,'crack')
        for yy,zz,length in ((5.1,1.76,1.0),(6.4,1.79,.65),(7.75,.62,.8)):
            b.print([(5.488,yy,zz-.013),(5.488,yy+length,zz-.013),(5.488,yy+length,zz+.013),(5.488,yy,zz+.013)],'crack')
        # Sill's wear is on the horizontal customer contact surface.
        flat_mark(b,5.71,2.8,.98805,.36,1.30,'scuff');b.finish()
    return marks
