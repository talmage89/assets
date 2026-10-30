"""Original inert cartridge/case/link display meshes for a 5.56×45 game prop.

Exterior silhouette approximations only. Solid decorative bases, no primer
pocket, chamber, projectile interior, loading data or functioning link design.
The caller supplies materials, registration and millimeter-to-meter conversion.
"""
import math

def cartridge(lathe,name,position,bone,*,fired=False,sides=24):
 x,y,z=position
 case=[(0,0),(0,4.6),(.6,4.8),(1.2,4.8),(1.7,4.25),(2.6,4.25),
       (3,4.7),(31.5,4.35),(35.5,3.25),(44.5,3.05)]
 case += [(44.5,2.6),(42.5,2.6),(42.5,0)] if fired else [(44.5,0)]
 result=[lathe(name+'_Case',[(y+h,r) for h,r in case],'brass',bone,center=(x,z),nseg=sides)]
 if not fired:
  tip=[(43.5,0),(43.5,2.9),(47,2.9),(51.5,2.4),(55,1.4),(57,.25),(57,0)]
  result.append(lathe(name+'_Jacket',[(y+h,r) for h,r in tip],'copper',bone,center=(x,z),nseg=sides))
 return result

def link(mesh,material,name='DisplayLink',spacing=12.8):
 """Decorative open cuffs/bridge. Spacing is a rig parameter, not a specification."""
 vs=[];fs=[]
 # Alternating axial bands suggest interleaving. All surfaces have finite thickness.
 for cx,lo,hi in [(0,8,12),(0,23,27),(-spacing,15,20)]:
  start=len(vs);n=10
  for y,r in [(lo,5.05),(lo,5.8),(hi,5.8),(hi,5.05)]:
   for j in range(n+1):
    t=math.radians(145)+math.radians(250)*j/n
    vs.append((cx+r*math.cos(t),y,r*math.sin(t)))
  m=n+1
  for a,b in ((0,1),(1,2),(2,3),(3,0)):
   for j in range(n):fs.append(tuple(start+v for v in (a*m+j,a*m+j+1,b*m+j+1,b*m+j)))
  fs.extend([(start,start+m,start+2*m,start+3*m),
             (start+n,start+3*m+n,start+2*m+n,start+m+n)])
 # Diagonal formed webs join the actual cuff ends. The earlier horizontal
 # strips sat above the open arcs and visibly floated in the standalone view.
 # Ends enter their supporting axial bands; finite width/thickness overlaps
 # the cuff skin. This remains an inert visual proxy, not a working link.
 radius=5.425;z=radius*math.sin(math.radians(145))
 main_x=radius*math.cos(math.radians(145))
 other_x=-spacing+radius*math.cos(math.radians(395))
 for ya,yb in ((11.8,15.2),(23.2,19.8)):
  dx,dy=other_x-main_x,yb-ya;length=math.hypot(dx,dy)
  ux,uy=dy/length*.38,-dx/length*.38
  k=len(vs)
  vs += [(x+sign*ux,y+sign*uy,z+height) for height in (-.38,.38)
         for x,y,sign in ((main_x,ya,-1),(other_x,yb,-1),(other_x,yb,1),(main_x,ya,1))]
  fs += [tuple(k+i for i in f) for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]]
 return mesh(name,vs,fs,material)
