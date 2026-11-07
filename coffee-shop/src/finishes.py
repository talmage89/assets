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
            # Selected bottom leg faces reveal steel through the coating.
            uv=ob.data.uv_layers.active;a,b,c,d=G.LAYOUT['steel']
            for face in ob.data.polygons:
                z=sum(ob.data.vertices[i].co.z for i in face.vertices)/len(face.vertices)
                if .022<z<.070 and abs(face.normal.z)<.7 and face.index%7==0:
                    for li in face.loop_indices:uv.data[li].uv=((a+c)/2,(b+d)/2)

def flat_mark(batch,x,y,z,w,d,key,angle=0):
    a=math.radians(angle);verts=[]
    for xx,yy in ((-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)):
        verts.append((x+xx*math.cos(a)-yy*math.sin(a),y+xx*math.sin(a)+yy*math.cos(a),z))
    batch.print(verts,key)

def placed(p,front):
    seed=p['seed'];rng=random.Random(seed+295);z=p['grade'];kind=p['kind'];age={'downtown':.30,'strip':.85,'pad':1.0}[kind]
    marks=G.root('PlacedUseHistory',parent=front,part='site_wear');b=G.Batch('Placed coffee rings and customer spills',marks)
    for t in p['tables']:
        for j in range(2):
            flat_mark(b,t['x']+rng.uniform(-.24,.24),t['y']+rng.uniform(-.21,.21),z+(.763 if t['accessible'] else .743),.083,.082,'ring',rng.uniform(0,360))
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
    # Queue darkening is spatially confined in the room; ends at the counter.
    qb=G.Batch('Customer queue floor wear',marks)
    for j in range(5):
        flat_mark(qb,p['counter_x']-.85+(.0 if kind!='strip' else .22*j),p['counter_y']-1.00-j*.34,z+.0185,.54,.47,'spill',j*31)
    qb.finish()
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
        # Sill's wear is on the horizontal customer contact surface.
        flat_mark(b,5.71,2.8,.991,.36,1.30,'scuff');b.finish()
    return marks
