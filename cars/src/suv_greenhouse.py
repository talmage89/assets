"""Original six-light greenhouse apertures projected onto the fair parent."""
import bpy,math
from mathutils import Vector
from kit import model as G

def build(b,tree,surface):
 from suv_body import form_blank
 from suv_apertures import regularize_blank,outline,cut_mesh,surface_uv
 # y positions and z endpoints are authored construction controls, not pixels.
 windows=[('Front',(-.940,1.185),(-.215,1.605),(.092,1.622),(.092,1.174)),
          ('Rear',(.205,1.177),(.205,1.621),(1.005,1.603),(1.005,1.213)),
          ('Quarter',(1.105,1.220),(1.105,1.593),(1.463,1.539),(1.651,1.288))]
 for side,sgn in [('L',-1),('R',1)]:
  for name,bl,tl,tr,br in windows:
   rows=[];nu=12
   for j in range(5):
    v=j/4;row=[]
    for i in range(nu+1):
     u=i/nu
     y=(bl[0]*(1-u)+br[0]*u)*(1-v)+(tl[0]*(1-u)+tr[0]*u)*v
     z=(bl[1]*(1-u)+br[1]*u)*(1-v)+(tl[1]*(1-u)+tr[1]*u)*v
     # Circular-corner inset in the pane's own chart, 16 mm corner radius.
     if i in [0,nu]:z+=(.014 if j==0 else -.014 if j==4 else 0)
     x=.880-.34*max(0,z-1.16)
     row.append((sgn*x,y,z))
    rows.append(row)
   ob=form_blank(name+' side glazing_'+side,rows,b.m['glass'],tree,name=='Front')
   ob['glazing_gauge_m']=.0048
   regularize_blank(ob,surface,name=='Front')
   cutters=[q for q in outline(ob,surface)]
   for panel in list(bpy.context.scene.objects):
    if panel.type!='MESH' or panel.get('part_category') not in ['pillars','body','doors']:continue
    center=panel.matrix_world.translation
    # Chart outlines identify the side unambiguously; opposite side untouched.
    cut_mesh(panel,cutters,surface)
   for vertex in ob.data.vertices:
    _,n=surface_uv(vertex.co,surface);vertex.co-=n*.006
   b.add(ob,bpy.data.objects.get('Door_'+('F' if name=='Front' else 'R')+side) if name!='Quarter' else None,category='glass')

 # Roof-hinged backlight: 1160 mm top / 1490 mm base guides before projection.
 rows=[];nu=18
 for j in range(7):
  v=j/6;half=.745*(1-v)+.580*v;y=2.12*(1-v)+1.92*v;z=1.295*(1-v)+1.590*v
  row=[]
  for i in range(nu+1):
   u=i/nu;x=(2*u-1)*half;zz=z-.012*(x/half)**2
   row.append((x,y,zz))
  rows.append(row)
 blank=form_blank('Backlight',rows,b.m['glass'],tree,False);blank['glazing_gauge_m']=.0048;regularize_blank(blank,surface,False)
 from suv_apertures import carve
 b.add(blank,bpy.data.objects['Liftgate'],category='glass')
 carve(False,[blank],surface,recess=.006)
