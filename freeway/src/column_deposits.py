"""Connected cap leakage on the actual 32-sided column surfaces.

The already-baked runoff chart contributes fine channels. The shaft's vertex
field supplies broad dampness and road splash; neither replaces the other.
"""
import math
from textures import rect

def add(batch):
 u0,v0,u1,v1=rect('runoff')
 bottom=.04;head=4.32;radius=.6006
 for column,y in enumerate((-7.,0.,7.)):
  # Two continuous half-cylinder charts, phased independently. The polygons
  # share the shaft's exact ring angles, so no planar sticker floats on it.
  for half in range(2):
   for j in range(16):
    a=(half*16+j)*math.tau/32;c=a+math.tau/32
    xa,ya=-radius*math.cos(a),y-radius*math.sin(a)
    xc,yc=-radius*math.cos(c),y-radius*math.sin(c)
    left=u0+j/16*(u1-u0);right=u0+(j+1)/16*(u1-u0)
    if (column+half)%2:left,right=u1-(left-u0),u1-(right-u0)
    pts=[(xa,ya,bottom),(xc,yc,bottom),(xc,yc,head),(xa,ya,head)]
    uv=[(left,v0),(right,v0),(right,v1),(left,v1)]
    normal_a=(-math.cos(a),-math.sin(a),0)
    normal_c=(-math.cos(c),-math.sin(c),0)
    batch.face(pts,'Maintenance',uv=uv,
               normals=[normal_a,normal_c,normal_c,normal_a],
               tint=(1,1,1,.88-.06*column+.04*half))
