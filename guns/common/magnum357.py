"""Original exterior .357 visual ammunition, independent of a specific gun.

Millimeter geometry, +Y toward bullet, base at Y=0. C.I.P. exterior envelope:
32.77 case length, 40.39 maximum overall, 11.18 rim, 9.63 body diameter.
No chamber, pressure, loading or functional internal design is provided.
The caller supplies materials and registration. Marking relief waits for bake.
"""
from kit import model as M
from mathutils import Matrix,Vector
CASE_LENGTH=32.77
OVERALL_LENGTH=40.2
RIM_DIAMETER=11.12
HEADSTAMP='PD 357 / 26'
def build(name,base,materials,*,fired=False,segments=24):
 x,y,z=base;parts=[]
 def lathe(suffix,profile,mat,n=segments,closed=False):
  ob=M.lathe(name+'_'+suffix,[(y+h,r) for h,r in profile],materials[mat],n,axis='Y',center=(x,z),closed=closed)
  parts.append(ob);return ob
 # Turned rim and case walls. Fired case has a real annular open mouth.
 profile=[(.0,1.8),(.0,5.56),(1.40,5.56),(1.40,4.78),(32.77,4.76)]
 if fired:profile += [(32.77,4.45),(2.0,4.45),(2.,1.8)]
 else:profile += [(32.77,0),(.25,0),(.25,1.8)]
 lathe('Case',profile,'brass',n=max(24,segments),closed=True)
 primer=[(.08,0),(-.03,.45),(-.03,1.7),(.25,1.7),(.25,0)] if fired else [(.02,0),(.02,1.7),(.25,1.7),(.25,0)]
 lathe('Primer',primer,'primer',n=12)
 if not fired:
  # Original jacketed soft-point: broad ogive, short exposed lead nose.
  lathe('Jacket',[(32.4,4.50),(34.5,4.5),(37.3,3.6),(39.1,2.35)],'copper')
  lathe('Lead',[(38.85,2.32),(40.2,1.55)],'lead',n=segments)
 return parts
