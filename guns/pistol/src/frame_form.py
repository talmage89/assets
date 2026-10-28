"""PD C9 compound polymer mold: rounded masses fused into a sculpted source.

All stations and reliefs are authored visual parameters in millimeters. This
is a game prop's outer form, without functional firearm internals. The middle
grip sections are inherited from the accepted pilot.
"""
import math
from mathutils import Vector
from kit import model as M

# Changing rounded sections give the flank a convex field, rather than a
# planar side bounded by an edge bevel. The front underside rises to the nose.
UPPER=[(-40.0,8.5,35.2,38.6),(-38.3,11.9,31.8,39.0),
 (-34,13.0,26.3,39.0),(-28,13.8,22.0,39.0),(-19,14.3,18.2,39.0),
 (-8,14.5,17.2,39.0),(5,14.4,18.2,39.0),(20,14.0,21.0,39.0),
 (34,13.8,23.5,39.0),(49,13.8,23.5,39.0),(55,13.6,23.5,39.0),
 (62,13.3,21.0,39.0),(70,13.0,16.4,39.0),(82,12.9,15.1,39.0),
 (100,12.8,16.5,39.0),(118,12.5,18.6,39.0),(128,11.9,21.0,39.0),
 (132,10.0,24.0,37.8)]

def molding_stations(rows,substeps=6):
 """Bounded C1 station flow for this mold's widths, depths and palm web.

 Harmonic slopes preserve the authored extrema while removing the straight
 spans and abrupt tangent changes of the initial seed lofts.
 """
 def slope(i,k):
  if i==0 or i==len(rows)-1:return 0.0
  a=(rows[i][k]-rows[i-1][k])/(rows[i][0]-rows[i-1][0])
  b=(rows[i+1][k]-rows[i][k])/(rows[i+1][0]-rows[i][0])
  return 0.0 if a*b<=0 else 2*a*b/(a+b)
 result=[]
 for i in range(len(rows)-1):
  left,right=rows[i:i+2];h=right[0]-left[0]
  for j in range(substeps):
   t=j/substeps;row=[left[0]+h*t]
   for k in range(1,len(left)):
    v=(2*t**3-3*t*t+1)*left[k]+(t**3-2*t*t+t)*h*slope(i,k)+(-2*t**3+3*t*t)*right[k]+(t**3-t*t)*h*slope(i+1,k)
    row.append(min(max(left[k],right[k]),max(min(left[k],right[k]),v)))
   result.append(row)
 return [*result,rows[-1]]

def upper_loop(y,hw,low,high,n=64):
 # An authored rounded half-section: a narrow seating land, full shoulder,
 # bowed flank and deep lower sweep. There is no planar flank segment.
 land=min(hw-.4,12.7)
 upper=M.bezier((land,high),(hw+.3,high),(hw+1.0,high-3),
                (hw+.85,high-(high-low)*.43),12)
 lower=M.bezier(upper[-1],(hw+.7,low+4),(hw-1.5,low),(hw-5,low),12)
 half=[(0,high),(land-1,high),*upper,*lower[1:],(0,low)]
 return [(x,y,z) for x,z in half]+[(-x,y,z) for x,z in reversed(half[1:-1])]

def guard_bar(material):
 path=[]
 for controls,n in [(((16,5),(20,-2),(21,-5.6),(31,-5.6)),16),
                    (((31,-5.6),(39,-5.6),(50,-5.6),(57,-5.6)),16),
                    (((57,-5.6),(61,-5.6),(62,-3.8),(62,0)),12),
                    (((62,0),(62,8),(62,15),(62,19)),14),
                    (((62,19),(62,25),(65,26),(73,27)),16)]:
  samples=M.bezier(*controls,n)
  path.extend(samples if not path else samples[1:])
 loops=[]
 for i,(y,z) in enumerate(path):
  a=Vector(path[max(0,i-1)]);b=Vector(path[min(len(path)-1,i+1)])
  tangent=(b-a).normalized();normal=Vector((-tangent.y,tangent.x))
  loops.append([(7.0*math.cos(t),y+3.4*math.sin(t)*normal.x,
                 z+3.4*math.sin(t)*normal.y) for t in [math.tau*j/32 for j in range(32)]])
 return M.loft('Rounded guard bar seed',loops,material)

def sculpt(grip,material,grip_center,magwell_loop,grip_loop):
 def tool_box(low,high):
  ob=M.box('Mold tool',(Vector(low)+Vector(high))/2,Vector(high)-Vector(low),material,radius=0)
  M.apply(ob);return ob
 def cut(tool,operation='DIFFERENCE'):
  tool.data.materials.clear();tool.data.materials.append(material)
  M.boolean(grip,tool,operation)
  grip.data.materials.clear();grip.data.materials.append(material)
  for f in grip.data.polygons:f.material_index=0
 cut(M.loft('Upper rounded mold seed',[upper_loop(*s) for s in molding_stations(UPPER)],material),'UNION')
 cut(guard_bar(material),'UNION')
 # A broad swept palm web bridges grip to tang. Its rear boundary hooks
 # back under the slide without the stacked lobes of separate local ellipsoids.
 web=[]
 for z,hw,rear,front in molding_stations([(0,13.0,-23.0,20.0),(8,14.0,-22.0,24.0),
                       (16,14.4,-23.5,30.0),(24,14.4,-29.0,35.0),
                       (32,13.5,-35.0,40.0),(37,10.0,-34.0,40.0)]):
  web.append(grip_loop(z,(rear+front)/2,hw,(front-rear)/2,n=64))
 cut(M.loft('Swept palm web seed',web,material),'UNION')
 surround=M.box('Rounded release surround seed',(-11.8,16.5,10),(4.8,13,16),material,radius=2.0,segments=8)
 M.apply(surround);cut(surround,'UNION')
 remesh=grip.modifiers.new('Rounded seeds / mold union','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.42;remesh.use_smooth_shade=True;M.apply(grip)
 relax=grip.modifiers.new('Broad web radii','SMOOTH');relax.factor=.65;relax.iterations=14;M.apply(grip)
 # Cavity walls describe only the visible prop and clear the accepted rig.
 cut(M.loft('Magazine cavity',[magwell_loop(z) for z in (-61,-49,20,45)],material))
 cut(M.loft('Flared cavity',[magwell_loop(-55,13.8,21),magwell_loop(-47,10.5,17.8)],material))
 cut(tool_box((-10.4,-36.8,34.4),(10.4,134,45)))
 cut(tool_box((-9.2,31,31),(9.2,73,47)))
 cut(tool_box((-8.3,18,26.5),(8.3,31,40.5)))
 opening=M.fillet_polygon([(22,-3),(58,-3),(58,24),(29,24)],3.5,segments=10)
 cut(M.profile('Guard aperture',opening,-20,20,material,axis='X'))
 # The swept round bar flows into the frontstrap as an open saddle. Do not
 # drill a finite-ended cylinder into this compound surface.
 cut(tool_box((-4.5,36,15),(4.5,55,35)))
 # Slim control seats follow the flank. A raised molded release surround is
 # retained around the rectangular opening rather than exposed as a bolt seat.
 pocket=M.fillet_polygon([(10.7,3.1),(22.3,3.1),(22.3,17.0),(10.7,17.0)],1.8,8)
 cut(M.profile('Release seat',pocket,-18,-11.8,material,axis='X'))
 cut(tool_box((-17,4,26.8),(-11.5,18,38.0)))
 # The bent stem swings inside the molding. Leave a real outer skin over
 # its travel cavity; only the raised thumb pad needs an external opening.
 stem=[(18,27),(46,28.5),(46,33.0),(18,36.2)]
 cut(M.profile('Internal stop-stem cavity',stem,-13.25,-11.5,material,axis='X'))
 cut(tool_box((-15,9,30),(-10.1,21,44)))
 for side in (-1,1):
  lo,hi=sorted((side*13.65,side*17))
  cut(tool_box((lo,44.0,27.8),(hi,51.7,33.6)))
 cut(tool_box((-10.8,4,29),(-9.9,28,39.2)),'UNION')
 # Accessory interface: reliefs cut into the continuous molding, with a
 # transverse underside slot. Rounded tools leave a molded root radius.
 rail_relief=M.fillet_polygon([(79,18.6),(121,22.1),(121,24.0),(79,20.5)],.55,6)
 for side in (-1,1):
  lo,hi=sorted((side*11.1,side*18))
  cut(M.profile('Molded rail side relief',rail_relief,lo,hi,material,axis='X'))
 slot=M.box('Transverse molded slot',(0,108.25,15.3),(36,5.5,9.0),material,radius=.65,segments=5)
 M.apply(slot);cut(slot)
 remesh=grip.modifiers.new('Sculpted finished mold','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.28;remesh.use_smooth_shade=True;M.apply(grip)
 relax=grip.modifiers.new('Molded cavity radii','SMOOTH');relax.factor=.65;relax.iterations=10;M.apply(grip)
 # Authored raised panel rims on the actual mold surface. Fine texture waits
 # for look-dev. Restrict displacement to exterior side normals/positions.
 grip.data.update()
 for v in grip.data.vertices:
  x,y,z=v.co
  if not (-48<z<4 and abs(x)>10.8):continue
  u=y-grip_center(z)+1.0
  qx=abs(u)-12.0;qz=abs(z+23)-19.0
  distance=math.hypot(max(qx,0),max(qz,0))+min(max(qx,qz),0)-2.8
  height=.42*math.exp(-(distance/.65)**2)
  if distance<0:height+=.10*(1-math.exp(-(distance/1.0)**2))
  # Fade the edge around the curved front/back shoulders rather than forming
  # a separate sharp plate on either side of the accepted grip section.
  weight=min(1,max(0,(abs(x)-10.8)/2.6))
  v.co.x+=math.copysign(height*weight,x)
 grip.data.update();M.smooth(grip,70)
 return grip
