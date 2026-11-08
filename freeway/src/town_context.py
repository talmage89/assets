"""Narrow residential parcels, original native envelopes, yards and canopy.

55 ft is the central frontage; 50/55/60 ft lots share 106.9 ft depth between
public sidewalks and rear alleys. Streets/ROW use the accepted civil placement.
The two native tree meshes and four house meshes are linked instances.
"""
import json,math,random
from pathlib import Path
import bpy
from mathutils import Vector
import geom as Q
ROOT=Path(__file__).resolve().parents[2]
FT=.3048
STYLES={'Ranch14':'HearthfieldRanch-14','Cape':'HearthfieldCape-31','Cape33':'HearthfieldCape-33','Cape36':'HearthfieldCape-36'}

def town(p):
 from freeway_site import load,clone,delete
 rt=Q.root('TownContext',module_kind='context');rng=random.Random(p.seed+713)
 z=7. if p.kind=='diamond' else 0.
 b=Q.Batch('Neighborhood streets driveways alleys and parcels',rt)
 rows=[];lawns=[];driveways=[];trees=[]
 reserves=[(129,177,10,60),(-177,-129,-61,-11),(-242,-130,11,77),(-287,-121,77,91),
           (211,277,27,75),(293,359,-73,-25),(-358,-292,-73,-25),(-440,-374,25,73)] if p.kind=='diamond' else []
 if p.kind=='diamond':driveways.extend([(122,1,31.3424,3.6576),(-122,-1,-32.3424,3.6576)])
 def xy(u,s):
  c=p.center(s);n,_=p.frame(s);return (c[0]+n[0]*u,c[1]+n[1]*u)
 def point(u,s,h=0):return (*xy(u,s),z+h)
 def strip(u0,u1,s0,s1,role,h=0,tint=(1,1,1,1)):
  b.surface([point(u0,s0,h),point(u1,s0,h),point(u1,s1,h),point(u0,s1,h)],role,tint=tint)
 def fence(u0,u1,s0,s1,height=1.22):
  a=Vector(point(u0,s0));c=Vector(point(u1,s1));length=(c-a).length
  steps=max(1,math.ceil(length/3.048))
  for j in range(steps+1):
   v=a.lerp(c,j/steps);b.tube([v,v+Vector((0,0,height+.06))],.024,'Steel',4)
  b.face([a+Vector((0,0,.05)),c+Vector((0,0,.05)),c+Vector((0,0,height)),a+Vector((0,0,height))],'Fence',uv=[(0,0),(length/.3048,0),(length/.3048,height/.3048),(0,height/.3048)])
  b.beam(a+Vector((0,0,height)),c+Vector((0,0,height)),.026,'Steel')
 templates={n:load('build/context/'+n+'.glb') for n in STYLES}
 metadata={n:json.loads((ROOT/'houses/export'/(f+'.json')).read_text()) for n,f in STYLES.items()}
 # The native sockets are in their house frame, not guessed at the lot center.
 def local_point(u,s,yaw,q):
  ang=math.radians(yaw);x,y,h=q
  factor=1-u/p.radius if p.radius else 1
  return (u+x*math.cos(ang)-y*math.sin(ang),s+(x*math.sin(ang)+y*math.cos(ang))/factor,h)
 streets=[122+82*j for j in range(7)] if p.kind=='diamond' else [86+82*j for j in range(3)]
 cross=list(range(-640,641,128)) if p.kind=='diamond' else list(range(-512,513,128))
 extent=700 if p.kind=='diamond' else 545
 for side in (-1,1):
  for ri,street in enumerate(streets):
   for bank in (-1,1):
    if ri==0 and bank<0 and p.kind=='diamond':continue
    for block,(s0,s1) in enumerate(zip(cross,cross[1:])):
     # Commercial frontage and apartment parcels replace complete residential
     # blocks, rather than placing buildings over one another.
     widths=[60*FT,50*FT,55*FT,55*FT,55*FT,50*FT,50*FT]
     factor=1-side*(street+bank*6.524)/p.radius if p.radius else 1
     if p.radius:
      # Offset curves have different physical station lengths. Compensate
      # lot count so these remain 50–60 ft frontages on both curve sides.
      count=round((128-2*6.524)*factor/(55*FT))
      widths=[(128-2*6.524)/count]*count
     rng.shuffle(widths);margin=(128-2*6.524-sum(widths))/2
     start=s0+6.524+margin
     for frontage in widths:
      ss=start+frontage/2;start+=frontage
      if p.kind=='diamond' and abs(ss)<22:continue
      front=side*(street+bank*6.524);back=side*(street+bank*(41-1.9));pu0,pu1=sorted((front,back))
      if any(pu0<r and pu1>l and ss-frontage/2<k and ss+frontage/2>f for l,r,f,k in reserves):continue
      physical_frontage=frontage*factor
      style='Ranch14' if physical_frontage>18 else ('Cape' if physical_frontage>16 and rng.random()<.70 else rng.choice(('Cape33','Cape36')))
      meta=metadata[style];lo,hi=meta['bounds'];yaw=90 if -side*bank>0 else -90
      setback=rng.uniform(6.5,8.7)
      uu=side*(street+bank*(6.524+setback-lo[1]))
      house_factor=1-uu/p.radius if p.radius else 1
      station=ss-(lo[0]+hi[0])/2*math.sin(math.radians(yaw))/house_factor+rng.uniform(-.18,.18)
      ob=clone(templates[style],f'House_{len([r for r in rows if r["kind"]=="house"]):04d}',point(uu,station),yaw,rt)
      ob.rotation_euler.z-=station/p.radius if p.radius else 0
      parcel_front=side*(street+bank*6.524);parcel_back=side*(street+bank*(41-1.9))
      u0,u1=sorted((parcel_front,parcel_back));ss0,ss1=ss-frontage/2,ss+frontage/2
      lawns.append((u0,u1,ss0,ss1))
      rows.append(dict(kind='house',name=ob.name,style=style,point=point(uu,station),yaw=yaw,frontage_m=physical_frontage,depth_m=41-1.9-6.524,parcel_us=[u0,u1],parcel_stations=[ss0,ss1]))
      sockets=meta['sockets'];drive=sockets.get('GarageApron',sockets.get('Driveway'))
      if drive:
       du,ds,dh=local_point(uu,station,yaw,drive);half=1.524 if style!='Ranch14' else 1.95
       road_u=side*street+side*bank*3.66
       # Real drive drops the sidewalk and curb along its full aperture.
       b.surface([point(road_u,ds-half,.027),point(du,ds-half,dh+.008),point(du,ds+half,dh+.008),point(road_u,ds+half,.027)],'Concrete',tint=(.83,.82,.77,1))
       driveways.append((side*street,side*bank,ds,half))
      walk=sockets.get('Walk')
      if walk:
       wu,ws,wh=local_point(uu,station,yaw,walk);strip(parcel_front,wu,ws-.46,ws+.46,'Concrete',.033,(.9,.89,.85,1))
      # Enclosed rear yards leave the alley and front setback open.
      if rng.random()<.82:
       fence(parcel_back,parcel_back,ss0,ss1)
       end=uu-side*bank*2.0
       fence(parcel_back,end,ss1,ss1)
      # Yard trees have trunks outside the native house/garage envelope and
      # drive. Mature crowns may overhang a roof, as in the aerial photograph.
      def occupied(u,s):
       lu,ls,_=local_point(uu,station,yaw,((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0))
       return abs(u-lu)<(hi[1]-lo[1])/2+1.0 and abs(s-ls)<(hi[0]-lo[0])/2+1.0
      candidates=[]
      for j in range(0 if p.kind=='soundwall' and ri==0 and bank<0 else 12):
       u=rng.uniform(u0+1.7,u1-1.7);s=rng.uniform(ss0+1.2,ss1-1.2)
       if occupied(u,s):continue
       if drive and abs(s-ds)<2.5:continue
       if all(math.hypot(u-a,s-c)>4.8 for a,c in candidates):candidates.append((u,s))
       if len(candidates)>=2+(rng.random()<.22):break
      if p.kind=='soundwall' and ri==0 and bank<0 and rng.random()<.72:
       # Front gardens sit beyond these roofs from the freeway. A dense rear
       # tree belt here hid every house and the utility conductors.
       candidates=[(side*(street-6.524-rng.uniform(1.8,4.5)),ss+rng.uniform(-3,3))]
      for u,s in candidates:trees.append((u,s,rng.uniform(.82,1.22),'yard'))
      if rng.random()<.55:
       trees.append((side*(street+bank*4.48),ss+rng.uniform(-2,2),rng.uniform(.78,1.12),'street'))
   if ri<len(streets)-1:
    # Public service alleys occupy the back-to-back lot boundary.
    for a,c in zip(cross,cross[1:]):
     lo,hi=sorted((side*(street+41-1.8),side*(street+41+1.8)));spans=[(a+4,c-4)]
     for l,r,f,k in reserves:
      if hi<=l or lo>=r:continue
      spans=[v for start,end in spans for v in ((start,min(end,f)),(max(start,k),end)) if v[1]>v[0]]
     for start,end in spans:strip(lo,hi,start,end,'Asphalt',.022,(.73,.71,.65,1))
 # Public street skin, six-inch curb, planting strip and five-foot sidewalk.
 def street(u):
  breaks={-extent,extent}
  for s in cross:breaks.update((max(-extent,s-6.524),min(extent,s+6.524)))
  for du,bank,ds,half in driveways:
   if abs(du-u)<.1:breaks.update((ds-half,ds+half))
  for s in range(-extent,extent,12):breaks.add(s)
  values=sorted(breaks)
  for a,c in zip(values,values[1:]):
   if p.kind=='diamond' and abs(u+204)<.01 and 10.668<(a+c)/2<84:continue
   strip(u-3.66,u+3.66,a,c,'Asphalt',.025)
   if min(abs((a+c)/2-s) for s in cross)<6.524:continue
   for side in (-1,1):
    if any(abs(du-u)<.1 and bank==side and abs((a+c)/2-ds)<half+.001 for du,bank,ds,half in driveways):continue
    strip(u+side*3.66,u+side*3.8124,a,c,'Concrete',.16)
    strip(u+side*5,u+side*6.524,a,c,'Concrete',.16)
 for side in (-1,1):
  for u in streets:street(side*u)
  for s in cross:
   if p.kind=='diamond' and abs(s)<1:continue
   end=111 if p.kind=='diamond' else 42
   strip(side*end,side*(streets[-1]+45),s-3.66,s+3.66,'Asphalt',.026)
   strip(side*end,side*(end+7.32),s-7,s+7,'Asphalt',.027)
   for h in (-1,1):strip(side*end,side*(streets[-1]+45),s+h*4.8,s+h*6.324,'Concrete',.16)
 for lib in templates.values():delete(lib)
 if p.kind=='diamond':
  for a,c in [(-2200,-420),(420,2200)]:
   b.surface([(a,-8.382,7.18236),(c,-8.382,7.18236),(c,8.382,7.18236),(a,8.382,7.18236)],'Asphalt')
   for y in (-9.5,9.5):b.surface([(a,y-.76,7.18),(c,y-.76,7.18),(c,y+.76,7.18),(a,y+.76,7.18)],'Concrete')
  strip(-286,-122,80.34,87.66,'Asphalt',.025)
  for yy in (78.8,89.2):strip(-286,-122,yy-.762,yy+.762,'Concrete',.16)
  for file,name,pos,yaw in [('Gas','TerminalGas',(153,35,7),0),('Strip','TerminalStrip',(-186,44,7),0),('Gas','WestGas',(-153,-36,7),180)]:
   src=load('build/context/'+file+'.glb');clone(src,name,pos,yaw,rt);delete(src);rows.append(dict(kind=file,point=pos,yaw=yaw))
   native=ROOT/'commercial/export'/('CommercialGas-101.json' if file=='Gas' else 'CommercialStrip-201.json')
   meta=json.loads(native.read_text());angle=math.radians(yaw)
   for drive in meta['driveways']:
    if drive['edge']!='south':continue
    dx,dy=drive['center'];cx=pos[0]+dx*math.cos(angle)-dy*math.sin(angle);cy=pos[1]+dx*math.sin(angle)+dy*math.cos(angle)
    half=drive['width']/2;sign=1 if cy>0 else -1;near=sign*10.668;far=cy+sign*4
    b.surface([(cx-half,near,7.18236),(cx+half,near,7.18236),(cx+half,far,7.028),(cx-half,far,7.028)],'Asphalt')
    for xx in (cx-half,cx+half):b.surface([(xx,near,7.18236),(xx,far,7.028),(xx+sign*.3,far,7),(xx+sign*.3,near,7)],'Earth')
  # Apartment infill and paved lots replace reserved arterial-frontage blocks.
  apartment=load('build/context/Apartment.glb')
  for j,(u,s) in enumerate(((244,51),(326,-49),(-325,-49),(-407,49))):
   clone(apartment,f'Garden_apartment_{j}',point(u,s),0 if s>0 else 180,rt);rows.append(dict(kind='apartment',point=point(u,s)))
   strip(u-33,u+33,s-24,s+24,'Asphalt',.018,(.83,.82,.78,1))
   for k in range(16):
    x=u-29+k*3.6576
    strip(x,x+.1,s-21,s-16,'White',.025,(.78,.78,.71,1))
   for xx in (u-28,u+29):trees.append((xx,s+17,rng.uniform(.85,1.12),'apartment'))
  delete(apartment)
 # A broken, multi-depth tree canopy follows private yards, street planting
 # strips and the unbuilt ROW edge rather than one repeated row.
 for side in (-1,1):
  for s in range(-620 if p.kind=='diamond' else -490,621 if p.kind=='diamond' else 491,19 if p.kind=='diamond' else 31):
   if p.kind=='diamond' and abs(s)<90:continue
   if p.kind=='soundwall' and rng.random()<.40:continue
   trees.append((side*((109 if p.kind=='diamond' else 43)+rng.uniform(0,5)),s+rng.uniform(-5,5),rng.uniform(.68,1.12) if p.kind=='diamond' else rng.uniform(.55,.95),'ROW'))
 native=[load('build/context/TreeOak.glb'),load('build/context/TreeMaple.glb')]
 for j,(u,s,scale,kind) in enumerate(trees):
  pt=point(u,s);ob=clone(native[rng.randrange(2)],f'{kind}_tree_{j:04d}',pt,rng.uniform(0,360),rt);ob.scale=(scale,)*3
  rows.append(dict(kind='tree',cause=kind,point=pt,scale=scale))
 for lib in native:delete(lib)
 # School's broad color stations: dry root zones and shaded lawn. The grain
 # and blade normal are the shared Ground lawn; no photo pixels are used.
 from landscape import lawn_tint
 for u0,u1,s0,s1 in lawns:
  for i in range(3):
   for j in range(3):
    a=u0+(u1-u0)*i/3;c=u0+(u1-u0)*(i+1)/3;d=s0+(s1-s0)*j/3;e=s0+(s1-s0)*(j+1)/3
    start=len(b.colors);b.surface([point(a,d,.004),point(c,d,.004),point(c,e,.004),point(a,e,.004)],'Lawn')
    for k in range(start,len(b.colors)):
     x,y,_=b.v[k];b.colors[k]=lawn_tint(x,y,kind='yard',seed=p.seed)
 utility=load('build/context/Utility.glb');bpy.context.view_layer.update()
 pins={o.name.split('__Socket_')[-1].split('.')[0]:utility.matrix_world.inverted()@o.matrix_world.translation for o in utility.children_recursive if '__Socket_' in o.name}
 for side in (-1,1):
  poles=[]
  for j,s in enumerate(range(-640,641,42)):
   pt=point(side*(130 if p.kind=='diamond' else 48),s);clone(utility,f'JointUse_{side}_{j}',pt,0,rt);poles.append(pt)
  for a,c in zip(poles,poles[1:]):
   for key,r in [('Primary_A',.00505),('Primary_B',.00505),('Primary_C',.00505),('Neutral',.004),('Telephone',.0185)]:
    pin=pins.get(key)
    if pin is None:continue
    pts=[(a[0]+pin.x+(c[0]-a[0])*t,a[1]+pin.y+(c[1]-a[1])*t,z+pin.z-.65*4*t*(1-t)) for t in [k/12 for k in range(13)]]
    b.tube(pts,r,'DarkSteel',4)
 delete(utility)
 light=load('build/context/StreetLight.glb')
 for side in (-1,1):
  for j,s in enumerate(range(-560,561,96)):clone(light,f'Street_light_{side}_{j}',point(side*(118 if p.kind=='diamond' else 72),s),90 if side>0 else -90,rt)
 delete(light);b.finish()
 from landscape import verges
 verges(p,rt)
 rt['placements_json']=json.dumps(rows);return rt
