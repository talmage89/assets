"""Garden-specific summer turf, cultivated cuts and trafficked granular courts.

Reuse the library's original baked lawn normals/ORM and blade field; a local
July albedo variant never writes into the accepted Ground delivery. All wear
stations follow traffic, bed trimming or drought at tree/plot edges.
"""
import math,random
from pathlib import Path
import numpy as np
from PIL import Image


def drought(x,y):
    # Exposed southern path shoulder and the sunny outer tree/plot margin.
    return .72*math.exp(-((x+.1)**2+(y+5)**2)/3.5)+.48*math.exp(-((x+11)**2+(y-5)**2)/10)


def summer_tint(x,y,extra_dry=0):
    stripe=.92+.065*math.tanh(math.sin((x+.23)*math.pi/1.22)*4)
    dry=min(.9,drought(x,y)+extra_dry)
    trample=.30*math.exp(-((x-.18-.12*math.sin(y*.55))/.29)**4)
    varied=.94+.035*math.sin(x*2.3+y*.77)+.025*math.sin(y*3.1-x*.9)
    return (min(1,stripe*varied*(1+dry*.18)),stripe*varied*(1-dry*.55-trample*.24),stripe*varied*(1-dry*.35-trample*.35),1)


def verge(p,parent):
    """Mown, curb-dry street frontage in the full-site photo comparisons."""
    import geometry as Q
    from kit import tiling
    W,D=p['size'];edge=W/2+3;front=-D/2;back=front-2.838;gap=p['main_width']/2
    vertices=[];faces=[]
    for left,right in ((-edge,-gap),(gap,edge)):
        nx=math.ceil(right-left);ny=math.ceil(front-back)
        base=len(vertices)
        vertices.extend([(left+(right-left)*i/nx,back+(front-back)*j/ny,-.0397) for j in range(ny+1) for i in range(nx+1)])
        faces.extend([(base+j*(nx+1)+i,base+j*(nx+1)+i+1,base+(j+1)*(nx+1)+i+1,base+(j+1)*(nx+1)+i) for j in range(ny) for i in range(nx)])
    ob=Q.mesh('Summer street turf verge',vertices,faces,parent,'Lawn',upward=True);tiling.world_uv(ob,3.048)
    tint=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for row,v in zip(tint.data,ob.data.vertices):
        x,y=v.co[:2];dry=.40*math.exp(-((x-p.get('sign_x',3.4))**2+(y-front+1.45)**2)/2.0)
        color=summer_tint(x,y,dry);fade=min(1,max(0,(edge-abs(x))/.8))
        row.color=tuple(1+(c-1)*fade for c in color[:3])+(1,)
    ob['cause']='unirrigated roadside verge; mowing follows the garden and dry grass follows the curb/sign frontage'
    return ob


def maps(repo,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for channel in ('BaseColor','Normal','ORM'):
        source=Path(repo)/f'ground/textures/ship/T_Lawn_{channel}.png'
        target=out/f'T_GardenLawn_{channel}.png'
        if channel=='BaseColor':
            rgb=np.asarray(Image.open(source).convert('RGB'),dtype=float)/255
            linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
            linear*=np.array([2.25,2.55,1.65])
            rgb=np.where(linear<=.0031308,linear*12.92,1.055*linear**(1/2.4)-.055)
            Image.fromarray(np.uint8(np.clip(rgb,0,1)*255+.5)).save(target)
        else:target.write_bytes(source.read_bytes())


def material(repo):
    from kit import tiling
    return tiling.material('GardenLawn','textures/ship',tint=True)


def turf(p,ground):
    import bpy
    import geometry as Q
    from kit import tiling
    # Same authored 3.048 m scale of the shared Ground tile; the previous
    # metre repeat minified blades into an even average at eye height.
    for ob in ground.children:
        if ob.type!='MESH':continue
        # Ground base has vertical sides; XY projection is valid only on
        # horizontal turf, otherwise the side charts collapse to a line.
        uv=ob.data.uv_layers.active
        for face in ob.data.polygons:
            if ob.data.materials[face.material_index]!=Q.M['Lawn'] or abs(face.normal.z)<.99:continue
            for li in face.loop_indices:
                point=ob.matrix_basis@ob.data.vertices[ob.data.loops[li].vertex_index].co
                uv.data[li].uv=(point.x/3.048,point.y/3.048)
        tint=ob.data.color_attributes.get('Tint') or ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        for row,vert in zip(tint.data,ob.data.vertices):
            x,y=(ob.matrix_basis@vert.co)[:2]
            row.color=summer_tint(x,y)
    # Clipped, narrow tufts above the cut turf, concentrated along bed edges
    # and the worn path shoulders. Clipped blades, never long reeds.
    from kit.botany import Cards
    from mathutils import Vector
    from atlas import grass_rect
    import plants
    rng=random.Random(p['seed']+9701);grass=Cards()
    def tuft(x,y,az,triangles,source=None):
        r=source or rng
        if any(a['surface']=='Gravel' and abs(x-a['center'][0])<a['size'][0]/2+.035 and abs(y-a['center'][1])<a['size'][1]/2+.035 for a in p['paths']):return
        width=r.uniform(.16,.23);height=r.uniform(.028,.052)
        for plane in range(2):
            angle=az+plane*1.15;axis=Vector((math.cos(angle),math.sin(angle),0));out=Vector((-axis.y,axis.x,0))
            rows=3 if triangles==8 or plane==0 else 2;grid=[]
            for j in range(rows):
                t=j/(rows-1);base=Vector((x,y,-.003))+out*(.012*t*t)+Vector((0,0,height*t))
                grid.append([base+axis*(sign*width/2) for sign in (-1,1)])
            grass.add_grid(grid,grass_rect(r.randrange(4)),(.02,.1,r.random(),.7))
    for bed in p['plots']:
        x,y=bed['center'];w,d=bed['width'],bed['depth']
        for side in (-1,1):
            for j in range(round(d/.11)):tuft(x+side*(w/2+rng.uniform(.025,.11)),y-d/2+(j+.5)*.11,math.pi/2,8)
            for j in range(round(w/.11)):tuft(x-w/2+(j+.5)*.11,y+side*(d/2+rng.uniform(.025,.11)),0,6)
    if p['archetype']=='park':
        # Break the planar surface along the visible traffic shoulders. The
        # centre remains worn; independent RNG preserves existing clover.
        shoulder=random.Random(p['seed']+643)
        for j in range(40):
            y=shoulder.uniform(-p['size'][1]/2+2,-1)
            x=.18+.12*math.sin(y*.55)+(-1 if j%2 else 1)*shoulder.uniform(.35,.70)
            tuft(x,y,shoulder.uniform(0,math.tau),8,shoulder)
    if grass.vertices:
        ob=grass.mesh('Rooted native fine turf tufts',plants.LEAF);ob.parent=ground;ob.data.uv_layers.active.name='UVMap'
        tint=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        for row,vertex in zip(tint.data,ob.data.vertices):
            x,y=vertex.co[:2];dry=drought(x,y)
            row.color=(1,1-dry*.55,1-dry*.35,1)
        ob['cause']='25–45 mm clipped edge sward; crossed original Ground alpha tufts, existing family atlas'
    # Clover leaves grow as low triples in the unmown margins, with a few
    # flowering weeds; same plant atlas/material allocation as vegetables.
    from atlas import rect
    from kit.botany import Cards
    import plants
    from mathutils import Vector
    cards=Cards();stems=[];stem_faces=[]
    for j in range(180):
        x=rng.uniform(-p['size'][0]/2+.2,p['size'][0]/2-.2);y=rng.uniform(-p['size'][1]/2+.2,p['size'][1]/2-.2)
        if abs(x-.18-.12*math.sin(y*.55))<.32:continue
        if any(abs(x-b['center'][0])<b['width']/2+.08 and abs(y-b['center'][1])<b['depth']/2+.08 for b in p['plots']):continue
        if any(a['surface']!='Lawn' and abs(x-a['center'][0])<a['size'][0]/2+.08 and abs(y-a['center'][1])<a['size'][1]/2+.08 for a in p['paths']):continue
        base_index=len(stems);stems.extend([(x-.0007,y,0),(x+.0007,y,0),(x+.0007,y,.016),(x-.0007,y,.016)]);stem_faces.append((base_index,base_index+1,base_index+2,base_index+3))
        for k in range(3):
            a=k*math.tau/3+j;v=Vector((math.cos(a),math.sin(a),0));side=Vector((-v.y,v.x,0));base=Vector((x,y,.016))
            grid=[[base+v*(t*.045)+side*(u*.018)+Vector((0,0,.008*math.sin(t*math.pi))) for u in (-1,1)] for t in (0,.5,1)]
            cards.add_grid(grid,rect('bean'),(.02,.1,rng.random(),0))
    if stems:Q.mesh('Rooted fine clover petioles',stems,stem_faces,ground,'Stem')
    ob=cards.mesh('Clover in turf margins',plants.LEAF);ob.parent=ground
    ob.data.uv_layers.active.name='UVMap'
    tint=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for row in tint.data:row.color=(.88,.95,.72,1)


def gravel_edges(p,rt):
    import geometry as Q
    rng=random.Random(p['seed']+477);routes=[a for a in p['paths'] if a['surface']=='Gravel']
    def inside(x,y):return any(abs(x-a['center'][0])<a['size'][0]/2-1e-5 and abs(y-a['center'][1])<a['size'][1]/2-1e-5 for a in routes)
    # Trace union's exposed perimeter, not each overlapping route rectangle.
    xs=sorted({a['center'][0]+s*a['size'][0]/2 for a in routes for s in (-1,1)})
    ys=sorted({a['center'][1]+s*a['size'][1]/2 for a in routes for s in (-1,1)})
    for x0,x1 in zip(xs,xs[1:]):
      for y0,y1 in zip(ys,ys[1:]):
        if not inside((x0+x1)/2,(y0+y1)/2):continue
        corners=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
        for j,(dx,dy) in enumerate(((0,-1),(1,0),(0,1),(-1,0))):
            a,b=corners[j],corners[(j+1)%4];mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
            if inside(mx+dx*.01,my+dy*.01):continue
            # 3 mm steel strip retains fines; driven stakes below its top.
            Q.box('Granular path steel edging',(mx,my,-.017),((x1-x0)+.003 if dx==0 else .003,(y1-y0)+.003 if dy==0 else .003,.066),rt,'Steel')
            length=math.dist(a,b)
            for k in range(round(length*8)):
                t=rng.random();offset=rng.uniform(.008,.095);x=a[0]+(b[0]-a[0])*t+dx*offset;y=a[1]+(b[1]-a[1])*t+dy*offset;z=.014*(1-offset/.10)
                r=rng.uniform(.004,.012)
                Q.mesh('Loose angular shoulder aggregate',[(x-r,y-r,z),(x+r,y-r*.7,z),(x+r*.5,y+r,z),(x-r*.7,y+r*.6,z),(x,y,z+r*.55)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],rt,'Gravel',upward=True)
    # Foot/tire compression marks: darker fine-grain swatch, low contrast,
    # in a staggered traffic line along the main route rather than black rails.
    from surfaces import rect
    a,b,c,d=rect('Gravel')
    def compressed_uv(ob):
        uv=ob.data.uv_layers.active;points=[v.co for v in ob.data.vertices]
        lo=[min(v[i] for v in points) for i in (0,1)];span=[max(v[i] for v in points)-lo[i] for i in (0,1)]
        for face in ob.data.polygons:
            for li in face.loop_indices:
                v=ob.data.vertices[ob.data.loops[li].vertex_index].co
                u=(v.x-lo[0])/span[0];t=(v.y-lo[1])/span[1]
                # Source-cell positions compensate for the reserved UV guards.
                uv.data[li].uv=(a+(c-a)*((.948+.030*u-.012)/.976),b+(d-b)*((.027+.018*t-.012)/.976))
    for j in range(70):
        y=-p['size'][1]/2+.18+j*.255;x=(-.18 if j%2 else .18)+.08*math.sin(y*.8)
        ob=Q.mesh('Traffic compressed sole print',[(x-.034,y-.105,.0144),(x+.034,y-.105,.0144),(x+.042,y-.04,.0144),(x+.038,y+.075,.0144),(x+.018,y+.10,.0144),(x-.025,y+.09,.0144),(x-.040,y+.03,.0144)],[(0,1,2,3,4,5,6)],rt,'Gravel',upward=True)
        compressed_uv(ob)
    # Paired wheel passages follow the route from the gate, fade into grain
    # through interruptions and bending, and remain flush at the true grade.
    for side in (-1,1):
        for j in range(55):
            y=-p['size'][1]/2+.12+j*.32
            if j%7 in (0,1):continue
            x=side*.31+.04*math.sin(y*.9)
            ob=Q.mesh('Granular court wheel compression',[(x-.015,y,.0143),(x+.015,y,.0143),(x+.014,y+.24,.0143),(x-.014,y+.24,.0143)],[(0,1,2,3)],rt,'Gravel',upward=True)
            compressed_uv(ob)
