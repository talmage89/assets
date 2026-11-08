"""Ground's turf/trim images with irregular edges and seed-owned use marks."""
import math,random
import bpy
from kit.tiling import world_uv


def mesh(parent,name,vs,fs,mat,coverage=3.048):
    # Open ground skins have authored upward winding. A volume-oriented
    # normal recalculation can reverse isolated cards according to position.
    data=bpy.data.meshes.new(name);data.from_pydata(vs,[],fs);data.materials.append(mat);data.update()
    ob=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(ob)
    ob.parent=parent;ob['top_surface']=True;world_uv(ob,coverage)
    for layer in {n.layer_name or 'Color' for n in mat.node_tree.nodes if n.type=='VERTEX_COLOR'}:
        col=ob.data.color_attributes.new(name=layer,type='FLOAT_COLOR',domain='POINT');ob.data.color_attributes.active_color=col
        for row in col.data:row.color=(1,1,1,1)
    ob['reused_surface']='ground';return ob


def turf(parent,plan,mat):
    W,D=plan['size'];nx=math.ceil(W/1.25);ny=math.ceil(D/1.25);vs=[];fs=[]
    for j in range(ny+1):
        for i in range(nx+1):
            x,y=-W/2+i*W/nx,-D/2+j*D/ny
            z=-.008-.018*(.5+.5*math.sin(x*.61+math.sin(y*.29)))*(.5+.5*math.sin(y*.83+x*.3))
            vs.append((x,y,z))
    for j in range(ny):
        for i in range(nx):k=j*(nx+1)+i;fs.append((k,k+1,k+nx+2,k+nx+1))
    ob=mesh(parent,'Summer turf / worn routes and shaded edges',vs,fs,mat)
    col=ob.data.color_attributes.active_color;old=plan['kind']=='old'
    for index,(x,y,z) in enumerate(vs):
        # Solar moisture differences at the parcel scale, with no noise wash.
        dry=.5+.25*math.sin(x*.19+y*.12+plan['seed'])+.25*math.sin(x*.37-y*.24)
        wear=0.;shade=0.
        for lot in plan['lots']:
            px,py,_=lot['origin'];h=lot['home'];yaw=lot['yaw']
            u=(x-px)*(1 if yaw==0 else -1);v=(y-py)*(1 if yaw==0 else -1)
            # Shortcut between the parking end and the stair toe; narrow soil
            # cores widen where people turn, rather than a rectangular band.
            walk_y=-h['width']/2-3.0
            if -h['length']*.20<u<h['length']/2+1.5:
                wear=max(wear,math.exp(-((v-walk_y)/(.22+.08*math.sin(u*1.7)))**4)*(.55 if old else .32))
            edge=min(abs(v-h['width']/2),abs(v+h['width']/2))
            if abs(u)<h['length']/2:shade=max(shade,math.exp(-(edge/.70)**2)*(.4+.3*math.sin(u*.7)**2))
            if lot['home']['occupant_seed']%3==0 and abs(u-h['length']/2)<5:
                dry=max(dry,.68+.18*math.sin(v*1.9+u*.6))
        c=(.98,.97-.31*dry,.79-.41*dry)
        soil=(.65,.49,.26);c=tuple(c[k]*(1-wear)+soil[k]*wear for k in range(3))
        c=tuple(c[k]*(1-shade*.22) for k in range(3));col.data[index].color=(*c,1)
    return ob


def decal(parent,name,center,size,mat,rect,yaw=0,seed=0,z=.020):
    x,y=center;w,h=size;r=math.radians(yaw);cs,sn=math.cos(r),math.sin(r)
    points=[(x+cs*u-sn*v,y+sn*u+cs*v,z) for u,v in ((-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2))]
    ob=mesh(parent,name,points,[(0,1,2,3)],mat);uv=ob.data.uv_layers.active
    u0,v0,u1,v1=rect;pad=3/2048
    for li,(u,v) in enumerate(((u0+pad,v0+pad),(u1-pad,v0+pad),(u1-pad,v1-pad),(u0+pad,v1-pad))):uv.data[li].uv=(u,v)
    ob['placement_seed']=seed;return ob


def worn_walk(parent,p,x0,x1,y,mat):
    """Compacted soil on the actual stair-to-parking route, with worn margins."""
    rng=random.Random(p['occupant_seed']+248);n=math.ceil((x1-x0)/.9);vs=[];fs=[]
    for j in range(n+1):
        x=x0+(x1-x0)*j/n;center=y+rng.uniform(-.055,.055)
        width=.23+rng.uniform(0,.10)+.12*math.exp(-((x-x0)/.8)**2)
        vs.extend([(x,center-width,.002),(x,center+width,.002)])
        if j:k=(j-1)*2;fs.append((k,k+2,k+3,k+1))
    ob=mesh(parent,'Compacted stair to parking footpath',vs,fs,mat,1.524)
    for c in ob.data.color_attributes.active_color.data:
        variation=rng.uniform(.94,1.04);c.color=(.75*variation,.61*variation,.37*variation,1)
    return ob


def pavement(a,p,lib,library_material):
    # Reuse the canonical alpha ravel/crack/oil manufacture. Unique placement,
    # rotation and extents prevent the row from repeating the same history.
    trim=library_material(lib,'GroundTrim');seed=p['occupant_seed'];r=random.Random(seed+148)
    L,W=p['length'],p['width']
    if p.get('corner_apron'):
        for j in range(16):
            # Native fissures are millimeters wide after atlas mapping;
            # the wider strip retains their ragged sides in the park shot.
            decal(a.root,'Corner apron settlement crack',(-L*.46+j*L*.061,-W/2-2.0+r.uniform(-1.1,1.1)),(.45,2.5+r.random()),trim,(.5,0,.625,.25),r.uniform(-65,65),seed,z=.003)
        for j in range(8):
            decal(a.root,'Corner apron repair',(-L*.40+j*L*.11,-W/2-1.8+r.uniform(-1,1)),(.6+r.random(),.35+r.random()),trim,(.25,.25,.5,.5),r.uniform(-70,70),seed,z=.002)
        decal(a.root,'Corner parked engine oil',(-L*.31,-7.2),(1.2,1.5),trim,(.5,.5,.75,.75),33,seed,z=.004)
        for j in range(4):
            decal(a.root,'Gravel at aged hardstanding edge',(-L*.35+j*5.7,-8.23),(.20,6.096),trim,(0,.5,.5,.75),90,seed,z=.003)
    if seed%3==0:
        for j in range(3):decal(a.root,'Loose gravel on dirt apron',(L/2+.9+j*1.8,-1.075),(1.8,2.95),trim,(0,.5,.5,.75),180*(j%2),seed,z=.019)
    if p['era']!='1996' or seed%4==0:
        decal(a.root,'Trampled stair toe',(-L*.035-p['deck_width']/2+.475,-W/2-3.56),(1.2,.76),trim,(.5,.25,1,.5),r.uniform(-14,14),seed,z=.006)
    if seed%4!=1:decal(a.root,'Engine sump stain',(L/2+2.5,-1.1),(.60+r.random()*.6,.8+r.random()*.9),trim,(.5,.5,.75,.75),r.uniform(-180,180),seed)
    if seed%3!=1:
        for j in range(2 if p['era']!='1996' else 1):
            decal(a.root,'Pad settlement crack',(L/2+1.1+j*1.8,-1.1+r.uniform(-.6,.6)),(.16,1.6+r.random()),trim,(.5,0,.625,.25),r.uniform(-60,60),seed)


def road_edge(parent,p,mat,tint=(1,1,1)):
    # A continuous irregular 15–75mm fringe, not regularly spaced teeth.
    # Centerline width remains the accepted 20/24 ft.
    w=p['street_width'];vs=[];fs=[];r=random.Random(p['seed']+512)
    for x in (-p['loop_x'],p['loop_x']):
        for side in (-1,1):
            n=math.ceil(p['span']/.8);stations=[-p['span']/2]+[-p['span']/2+j*p['span']/n+r.uniform(-.22,.22) for j in range(1,n)]+[p['span']/2]
            depth=r.uniform(.015,.075)
            for y,ynext in zip(stations,stations[1:]):
                nextdepth=r.uniform(.015,.075);k=len(vs)
                vs.extend([(x+side*(w/2-.015),y,.016),(x+side*(w/2+depth),y,.007),
                           (x+side*(w/2+nextdepth),ynext,.007),(x+side*(w/2-.015),ynext,.016)])
                fs.append((k,k+1,k+2,k+3) if side>0 else (k+3,k+2,k+1,k));depth=nextdepth
    ob=mesh(parent,'Broken curbless asphalt edges',vs,fs,mat,6.096)
    for v in ob.data.color_attributes.active_color.data:v.color=(*tint,1)
    return ob
