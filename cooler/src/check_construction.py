"""Independent physical capacity, support, drain and staged lid-clearance proof."""
import sys,json,argparse,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import bpy
from mathutils import Vector
from kit.assembly import distance
from kit.motion import surface,sweep
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
errors=[];measured={}
def named(s):return next(o for o in bpy.context.scene.objects if o.name.startswith(s))
def points(o):return surface(o)['points']
body=named('Insulated hollow');pts=points(body)
def hull(vs):
 vs=sorted(set((round(v.x,7),round(v.y,7)) for v in vs))
 cross=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 halves=[]
 for sequence in (vs,list(reversed(vs))):
  h=[]
  for v in sequence:
   while len(h)>1 and cross(h[-2],h[-1],v)<=0:h.pop()
   h.append(v)
  halves.append(h[:-1])
 return halves[0]+halves[1]
def area(poly):return abs(sum(x*y2-x2*y for (x,y),(x2,y2) in zip(poly,poly[1:]+poly[:1])))/2
sections=[];outlines=[]
for level,bx,by in [(.065,.256,.131),(.075,.261,.136),(.349,.276,.151),(.360,.278,.153)]:
 ring=hull([v for v in pts if abs(v.z-level)<1e-5 and abs(v.x)<bx and abs(v.y)<by]);assert len(ring)>8;outlines.append(ring)
 z=sum(v.z for v in pts if abs(v.z-level)<1e-5)/len([v for v in pts if abs(v.z-level)<1e-5]);sections.append(dict(z_m=z,area_m2=area(ring),vertices=len(ring)))
volume=0.0
for j,(aa,bb) in enumerate(zip(sections,sections[1:])):
 assert len(outlines[j])==len(outlines[j+1])
 mid=[((u[0]+v[0])/2,(u[1]+v[1])/2) for u,v in zip(outlines[j],outlines[j+1])]
 volume+=(bb['z_m']-aa['z_m'])*(aa['area_m2']+4*area(mid)+bb['area_m2'])/6

qt=volume/.000946352946;measured['cavity']=dict(section_measurements=sections,volume_m3=volume,US_quarts=qt,method='Mesh-vertex convex sections; prismoidal integration of measured polygon sections; small drain volume omitted')
if not 45<=qt<=50:errors.append('Actual cavity capacity outside 45–50 US qt')
feet=[o for o in bpy.context.scene.objects if o.name.startswith('Rubber foot')];minima=[min(v.z for v in points(o)) for o in feet];measured['foot_min_z_m']=minima
if len(feet)!=4 or max(abs(z) for z in minima)>1e-5:errors.append('Feet not on ground')
# A horizontal ray from just behind the recessed handle measures the remaining wall.
tree=surface(body)['tree'];hit=tree.ray_cast(Vector((.3009,0,.283)),Vector((-1,0,0)),.10)
wall=(.301-hit[0].x) if hit[0] else 0;measured['grip_remaining_wall_m']=wall
if wall<.025:errors.append('Grip cuts too far into insulated wall')
# Bore centerline passes through the complete body wall without a surface hit.
drain=tree.ray_cast(Vector((.24,.10,.079)),Vector((1,0,0)),.12);measured['drain_centerline_body_hit']=list(drain[0]) if drain[0] else None
if drain[0] is not None:errors.append('Drain does not connect to cavity')
contacts=[]
for aa,bb,limit in [('Continuous freezer gasket','Insulated hollow',.0001),('Continuous freezer gasket','Insulated stepped',.0001),('Body hinge bridge -1','Insulated hollow',.0001),('Lid hinge bridge -1','Insulated stepped',.0001),('Body bearing -1','Body hinge bridge -1',.0001),('Lid bearing -1','Lid hinge bridge -1',.0001),('Rubber foot -1 -1','Molded base runner',.002)]:
 d,method=distance(named(aa),named(bb));contacts.append(dict(parts=[aa,bb],distance_m=d,method=method,limit_m=limit))
 if d>limit:errors.append('Unsupported '+aa)
for foot in feet:
 fp=points(foot);center=sum(fp,Vector())/len(fp)
 runners=[o for o in bpy.context.scene.objects if o.name.startswith('Molded base runner')]
 runner=min(runners,key=lambda ob:(sum(points(ob),Vector())/len(points(ob))-center).length_squared)
 d,method=distance(foot,runner);contacts.append(dict(parts=[foot.name,runner.name],distance_m=d,method=method,limit_m=.0001))
 if d>.0001:errors.append('Unsupported '+foot.name)
ground=[v for foot in feet for v in points(foot) if abs(v.z)<1e-5]
center=Vector(((min(v.x for v in ground)+max(v.x for v in ground))/2,(min(v.y for v in ground)+max(v.y for v in ground))/2,0))
origin_error=(center-bpy.data.objects['Cooler'].matrix_world.translation).length
measured['footprint_origin_error_m']=origin_error
if origin_error>1e-5:errors.append('Origin is not centered on ground footprint')
measured['contacts']=contacts
# Retraction of the flexible cam is measured separately by kit.motion. The lid
# sweep then uses the actually released latch transforms, as required to open it.
for s in ('L','R'):bpy.data.objects['Latch_'+s].rotation_euler.x=math.radians(-90)
bpy.context.view_layer.update()
opening=sweep({'MOTIONS':[dict(node='Lid',axis='X',range=[0,-108],step=3,tolerance_m=.0005)]})
if not opening['passed']:errors.append('Released lid opening interferes')
measured['released_lid_sweep']=opening
r=dict(passed=not errors,source=a.source,scope='Independent evaluated construction surfaces; GLB preservation checked separately',measurements=measured,errors=errors)
Path(a.out).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));assert r['passed'],'Construction failures'
