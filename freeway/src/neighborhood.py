"""Seeded town blocks and afternoon actors, in separate exported packages.

Read-only native library deliveries supply all buildings, foliage and bodies.
House envelopes use the existing explicit distance adapter. No civil alignment
is changed by these placements. Colors decode the native original paint data.
"""
import math,random,json
from pathlib import Path
import bpy
from mathutils import Vector
import geom as Q
from plan import ramp_points


def town(p):
    from freeway_site import load,clone,delete
    rt=Q.root('TownContext',module_kind='context');rng=random.Random(p.seed+713)
    z=7.0 if p.kind=='diamond' else 0.;b=Q.Batch('Neighborhood grid and parcels',rt);rows=[]
    def xy(u,s):
        c=p.center(s);n,_=p.frame(s);return (c[0]+n[0]*u,c[1]+n[1]*u)
    def point(u,s,h=0):return (*xy(u,s),z+h)
    def strip(u0,u1,s0,s1,role,h=0,tint=(1,1,1,1)):
        b.surface([point(u0,s0,h),point(u1,s0,h),point(u1,s1,h),point(u0,s1,h)],role,tint=tint)
    def street(u,s0,s1):
        # Segmented curves preserve this town's grid offset from the right of way.
        n=max(1,math.ceil((s1-s0)/12));stations=[s0+(s1-s0)*i/n for i in range(n+1)]
        for a,c in zip(stations,stations[1:]):
            strip(u-3.66,u+3.66,a,c,'Asphalt',.025)
            for side in (-1,1):
                strip(u+side*3.66,u+side*3.8124,a,c,'Concrete',.16)
                strip(u+side*5.0,u+side*6.524,a,c,'Concrete',.16)
    if p.kind=='diamond':
        # Continue the town's arterial beyond the civil excerpt and its camera.
        for a,c in [(-2200,-420),(420,2200)]:
            b.surface([(a,-8.382,7.18236),(c,-8.382,7.18236),(c,8.382,7.18236),(a,8.382,7.18236)],'Asphalt')
            for y in (-9.50,9.50):b.surface([(a,y-.76,7.18),(c,y-.76,7.18),(c,y+.76,7.18),(a,y+.76,7.18)],'Concrete')
    cross=range(-640,641,128) if p.kind=='diamond' else range(-448,449,112)
    streets=[122,204,286] if p.kind=='diamond' else [70,146,222]
    extent=700 if p.kind=='diamond' else 530
    for side in (-1,1):
        for u in streets:street(side*u,-extent,extent)
        for s in cross:
            if abs(s)<1 and p.kind=='diamond':continue
            # Local cross streets stop at the ROW fence, with a paved hammerhead.
            end=111 if p.kind=='diamond' else 42
            strip(side*end,side*1200,s-3.66,s+3.66,'Asphalt',.026)
            strip(side*end,side*(end+7.32),s-7.0,s+7.0,'Asphalt',.027)
            for h in (-1,1):strip(side*end,side*1200,s+h*4.8,s+h*6.324,'Concrete',.16)
    houses=[load('build/context/Ranch.glb'),load('build/context/Cape.glb')]
    house_stations=range(-608,609,32) if p.kind=='diamond' else range(-480,481,32)
    offsets=[146,180,228,262,310] if p.kind=='diamond' else [44,94,122,170,198,246]
    idx=0
    for side in (-1,1):
        for row,u in enumerate(offsets):
            # More rows around the diamond; staggered roofs/backyards at Cedar Hollow.
            for s in house_stations:
                if min(abs(s-c) for c in cross)<14:continue
                if p.kind=='diamond' and abs(s)<90:continue
                if row>2 and abs(s)>380:continue
                s+=rng.uniform(-2,2);uu=side*(u+rng.uniform(-1.2,1.2))
                # First Cedar Hollow row faces away from the sound wall.
                street_u=min(streets,key=lambda a:abs(a-u));facing=side*(1 if street_u>u else -1)
                pos=point(uu,s);yaw=90 if facing>0 else -90
                h=clone(houses[(idx+p.seed)%2],f'House_{idx:03d}',pos,yaw,rt)
                h.rotation_euler.z-=s/p.radius if p.radius else 0
                rows.append(dict(kind='house',point=pos,yaw=yaw))
                a,c=sorted((uu+facing*7,side*street_u-facing*3.66))
                strip(a,c,s-1.524,s+1.524,'Concrete',.032)
                # Back-yard property divisions stop short of the public sidewalk.
                backyard=uu-facing*10.5
                for ss in (s-14.8,s+14.8):
                    pa=point(backyard,ss);pb=point(uu+facing*4,ss)
                    for lift in (.45,.95,1.45):b.beam((pa[0],pa[1],z+lift),(pb[0],pb[1],z+lift),.07,'Wood',.14)
                    for pt in (pa,pb):b.beam(pt,(pt[0],pt[1],z+1.5),.09,'Wood')
                idx+=1
    for lib in houses:delete(lib)
    if p.kind=='diamond':
        for file,name,pos,yaw in [('Gas','TerminalGas',(135,35,7),0),('Strip','TerminalStrip',(-186,44,7),0),('Gas','WestGas',(-136,-36,7),180)]:
            src=load('build/context/'+file+'.glb');clone(src,name,pos,yaw,rt);delete(src);rows.append(dict(kind=file,point=pos,yaw=yaw))
        # Actual driveway links from original parcel mouths into the arterial.
        for xa,xb,ya,yb in [(142.5,149.8,10.668,16),(-142.5,-135.2,-16,-10.668),(-231,-223,10.668,16),(-149,-141,10.668,16)]:
            b.surface([(xa,ya,z+.028),(xb,ya,z+.028),(xb,yb,z+.028),(xa,yb,z+.028)],'Asphalt')
    trees=[load('build/context/TreeOak.glb'),load('build/context/TreeMaple.glb')]
    for side in (-1,1):
        for j,s in enumerate(range(-600 if p.kind=='diamond' else -480,601 if p.kind=='diamond' else 481,34 if p.kind=='diamond' else 32)):
            if p.kind=='diamond' and abs(s)<90:continue
            u=side*((113 if p.kind=='diamond' else 37)+rng.uniform(0,8 if p.kind=='diamond' else 2));pt=point(u,s+(0 if p.kind=='diamond' else 16)+rng.uniform(-2,2))
            ob=clone(trees[j%2],f'ROW_tree_{side}_{j}',pt,rng.uniform(0,360),rt)
            # Native species at different actual ages; uniform size preserves form.
            scale=rng.uniform(.60,1.05);ob.scale=(scale,)*3
            rows.append(dict(kind='tree',point=pt,scale=scale))
        for j,s in enumerate(range(-510,511,76)):
            u=side*rng.choice([171,252,326] if p.kind=='diamond' else [110,182,262]);pt=point(u,s)
            ob=clone(trees[(j+1)%2],f'Garden_tree_{side}_{j}',pt,rng.uniform(0,360),rt);scale=rng.uniform(.65,1.05);ob.scale=(scale,)*3
    for lib in trees:delete(lib)
    utility=load('build/context/Utility.glb');bpy.context.view_layer.update()
    pins={o.name.split('__Socket_')[-1].split('.')[0]:utility.matrix_world.inverted()@o.matrix_world.translation for o in utility.children_recursive if '__Socket_' in o.name}
    for side in (-1,1):
        poles=[]
        for j,s in enumerate(range(-640,641,42)):
            pt=point(side*(130 if p.kind=='diamond' else 78),s);clone(utility,f'JointUse_{side}_{j}',pt,0,rt);poles.append(pt)
        for a,c in zip(poles,poles[1:]):
            for key,r in [('Primary_A',.00505),('Primary_B',.00505),('Primary_C',.00505),('Neutral',.004),('CommPhone',.0185)]:
                pin=pins.get(key)
                if pin is None:continue
                pts=[(a[0]+pin.x+(c[0]-a[0])*t,a[1]+pin.y+(c[1]-a[1])*t,z+pin.z-.65*4*t*(1-t)) for t in [k/12 for k in range(13)]]
                b.tube(pts,r,'DarkSteel',4)
    delete(utility)
    light=load('build/context/StreetLight.glb')
    for side in (-1,1):
        for j,s in enumerate(range(-560,561,96)):
            clone(light,f'Street_light_{side}_{j}',point(side*(118 if p.kind=='diamond' else 66),s),90 if side>0 else -90,rt)
    delete(light);b.finish();rt['placements_json']=json.dumps(rows);return rt


def factory_variants(template):
    """Decode the car family's baked coverage into ordinary PBR color images.

    This local derivative changes factory paint only; the native body, bake and
    deliveries stay immutable. Distant variants are 1024; original blue is shared.
    """
    import numpy as np
    from kit.image_io import write_png,linear_to_srgb
    from PIL import Image
    paints={m for ob in template.children_recursive if ob.type=='MESH' for m in ob.data.materials if m and m.get('paint_decode')}
    result={};folder=Path('textures/context');folder.mkdir(parents=True,exist_ok=True)
    for name in ('Porcelain','Carbon','Aluminum','Graphite','Atlantic'):
        replacements={}
        for mat in paints:
            m=mat.copy();colors=json.loads(mat['paint_colors']);color=colors[name];ref=mat['paint_reference_color']
            texture=next(n for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
            if name!='Atlantic':
                key=mat.name.split('.')[0].replace(' ','')+'_'+name;path=folder/(key+'.png')
                if not path.exists():
                    # bpy pixels are linear scene values, exactly as the native decode.
                    a=np.empty(len(texture.image.pixels),np.float32);texture.image.pixels.foreach_get(a);a=a.reshape(texture.image.size[1],texture.image.size[0],4)
                    rgb=np.clip(a[:,:,:3]+a[:,:,3,None]*(np.asarray(color)-np.asarray(ref)),0,1)
                    # Linear-light reduction, then sRGB encoding.
                    out=np.stack([np.asarray(Image.fromarray(rgb[:,:,i]).resize((1024,1024),Image.Resampling.LANCZOS)) for i in range(3)],axis=2)
                    write_png(path,linear_to_srgb(np.clip(out[::-1],0,1)),bits=8)
                texture.image=bpy.data.images.load(str(path.resolve()),check_existing=True)
            bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
            # Preserve native flakes/deposits in ORM; factor the factory metallic.
            m['factory_color']=name;m['native_paint_source']=mat.name
            for prop in ('paint_decode','paint_reference_color','paint_colors','paint_metallic'):
                if prop in m:del m[prop];replacements[mat]=m
        result[name]=replacements
    return result


def traffic(p):
    from freeway_site import load,clone,delete,along
    rt=Q.root('Traffic',module_kind='traffic');rng=random.Random(p.seed*37);placements=[]
    bodies=[load('build/context/'+n+'.glb') for n in ('Hatch','SUV','Crossover')];full=[load('build/context/'+n+'.glb') for n in ('HeroHatch','HeroSUV','HeroCrossover')];hero=full[0]
    variants=[factory_variants(t) for t in [*bodies,*full]];mesh_variants={}
    def colorize(ob,kind,color):
        replacements=variants[kind][color]
        for mesh in ob.children_recursive:
            if mesh.type!='MESH' or not any(m in replacements for m in mesh.data.materials):continue
            key=(mesh.data.as_pointer(),color,kind)
            if key not in mesh_variants:
                data=mesh.data.copy()
                for i,m in enumerate(data.materials):
                    if m in replacements:data.materials[i]=replacements[m]
                mesh_variants[key]=data
            mesh.data=mesh_variants[key]
    def actor(pos,yaw,where,speed=0,roll=0,nearest=False):
        heading=math.radians(yaw);forward=(math.sin(heading),-math.cos(heading));lateral=(math.cos(heading),math.sin(heading))
        for old in placements[:]:
            dx=pos[0]-old['location'][0];dy=pos[1]-old['location'][1]
            same_lane=abs(dx*lateral[0]+dy*lateral[1])<2.3 and abs(dx*forward[0]+dy*forward[1])<6.6 and abs(pos[2]-old['location'][2])<.7
            if not same_lane:continue
            if where in ('terminal_queue','arterial_queue') and 'queue' not in old['role']:
                delete(bpy.data.objects[old['name']]);placements.remove(old)
            else:return None
        i=len(placements);kind=3 if nearest else rng.randrange(3)
        if not nearest and where in ('mainline','bridge','arterial_queue') and abs(pos[1])<120 and abs(pos[0])<110:kind+=3
        color=rng.choices(['Porcelain','Carbon','Graphite','Aluminum','Atlantic'],[34,22,24,10,10])[0]
        ob=clone(full[kind-3] if kind>=3 else bodies[kind],f'Car_{i:03d}',pos,yaw,rt);ob.rotation_euler.y=roll;colorize(ob,kind,color)
        ob['speed_mps']=speed;ob['traffic_role']=where
        placements.append(dict(name=ob.name,body=('Hatch','SUV','Crossover','HeroHatch','HeroSUV','HeroCrossover')[kind],color=color,location=list(pos),yaw=yaw,speed_mps=speed,role=where))
        return ob
    # Afternoon flow: 1.7–3.1 seconds at 25–29m/s, with independent lane phases.
    for side in (-1,1):
        for lane in range(2):
            s=-p.length/2+rng.uniform(10,65)
            while s<p.length/2-10:
                speed=rng.uniform(25,29);pos=p.xyz(s,p.lane(side,lane));yaw=-math.degrees(s/p.radius if p.radius else 0)+(180 if side>0 else 0)
                actor(pos,yaw,'mainline',speed,math.atan(side*p.bank if p.bank else -.02));s+=speed*rng.uniform(1.7,3.1)
    # Retain the exact accepted near-car anchor for before/after scale.
    side,lane,s=(1,0,-26) if p.kind=='diamond' else (1,1,-22)
    pos=p.xyz(s,p.lane(side,lane))
    # Remove a potential flow placement within 10m of the retained actor.
    for row in placements[:]:
        if math.dist(row['location'],pos)<10:
            delete(bpy.data.objects[row['name']]);placements.remove(row)
    actor(pos,180-math.degrees(s/p.radius if p.radius else 0),'mainline',27,math.atan(side*p.bank if p.bank else -.02),True)
    if p.kind=='diamond':
        for side in (-1,1):
            for entry in (False,True):
                pts=list(map(Vector,ramp_points(p,side,entry,192)))
                # Stop queues belong to the off-ramp, entrance ramps remain flowing.
                indices=[18,48,81,118,152] if entry else [14,51,91,133,181,186,191]
                for j in indices:
                    v=pts[j];d=pts[j+1]-pts[j-1];yaw=math.degrees(math.atan2(d.x,-d.y))
                    # Forward is native -Y. Crossfall reverses with travel direction.
                    actor(v,yaw,'entrance' if entry else ('terminal_queue' if j>=178 else 'exit'),13 if entry else (0 if j>=178 else 18),-.02)
        for side in (-1,1):
            for lane,y in enumerate((side*3.3528,side*6.7056)):
                for x in range(-350,351,39 if lane else 57):
                    # Signal reservation is kept clear; queuing occurs upstream.
                    if abs(abs(x)-78)<20:continue
                    z=7.35-.02*abs(y);actor((x+rng.uniform(-4,4),y,z),90 if side<0 else -90,'arterial',12,side*.02)
            for tx in (-78,78):
                for j in range(3):
                    x=tx+side*(23+j*6.3);y=side*6.7056;actor((x,y,7.35-.02*abs(y)),90 if side<0 else -90,'arterial_queue',0,side*.02)
        for x,y in ((-19,3.3528),(9,-6.7056),(17,6.7056)):
            side=1 if y>0 else -1;actor((x,y,7.35-.02*abs(y)),90 if side<0 else -90,'bridge',12,side*.02)
        for x,y,yaw in [(126,24,0),(139,23,180),(-207,27,0),(-190,27,0),(-162,27,0)]:actor((x,y,7.05),yaw,'commercial_parked')
    else:
        for side in (-1,1):
            for j,s in enumerate(range(-430,431,76)):
                c=p.center(s);u=side*70;actor((c[0]+u,c[1],.04),180 if side>0 else 0,'neighborhood',8)
    for lib in [*bodies,*full]:delete(lib)
    rt['placements_json']=json.dumps(placements);return rt
