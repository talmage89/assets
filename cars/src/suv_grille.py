"""Alder's open double-chevron grille and separate lower cooling comb.

Sixteen molded blades sit 42 mm ahead of the radiator bed. Two concealed
cross-rails connect them and carry the existing badge. The lower opening uses
eighteen straight matte fins. The 560 game triangles replace the former ribs
and webs one for one; this is real open geometry, with no opacity trick.
"""
import bpy
from mathutils import Vector
from kit import model as G


def build(b):
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith(('Upper grille opening blade','Lower intake opening blade')):
            bpy.data.objects.remove(ob,do_unlink=True)
    # Match the measured mouth/bed bow, independently of nearby cut triangles.
    # The bed remains at the original 65 mm recess, visibly behind the blades.
    for name,upper in [('Upper grille opening',True),('Lower intake opening',False)]:
        bed=bpy.data.objects[name]
        raw=list(bed['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
        nu=bed['form_columns']
        def sample(u,v):
            xx=max(0,min(nu-1.000001,u*(nu-1)));zz=max(0,min(3.999999,v*4))
            i,j=int(xx),int(zz);a=xx-i;c=zz-j
            return ps[j*nu+i].lerp(ps[j*nu+i+1],a).lerp(ps[(j+1)*nu+i].lerp(ps[(j+1)*nu+i+1],a),c)
        if upper:
            for i in range(16):
                u=(i+.5)/16;sgn=-1 if u<.5 else 1;rows=[]
                for v in [.025,.50,.975]:
                    p=sample(u,v);p.x+=sgn*.019*(1-abs(2*v-1))
                    p.y-=.042
                    rows.append([tuple(p+Vector((dx,dy,0))) for dx,dy in [(-.008,-.004),(.008,-.004),(.008,.011),(-.008,.011)]])
                ob=G.loft('Alder chevron grille blade '+str(i),rows,b.m['dark_chrome'])
                b.add(ob,category='trim')
                # Flat manufactured blade faces, with an actual kink in plan;
                # never smooth a rectangular section into its neighboring face.
                for f in ob.data.polygons:f.use_smooth=False
            for v in [.30,.70]:
                a=sample(.018,v);c=sample(.982,v);p=(a+c)*.5;p.y-=.020
                ob=G.box('Grille structural rail '+str(v),p,((c-a).length,.012,.009),b.m['gloss_black'],0)
                b.add(ob,category='trim')
        else:
            for i in range(18):
                u=(i+.5)/18;a=sample(u,.035);c=sample(u,.965)
                # Louver face is deliberately different from the upper jewelry.
                rows=[]
                for p in [a,c]:
                    p.y-=.024
                    rows.append([tuple(p+Vector((dx,dy,0))) for dx,dy in [(-.004,-.003),(.004,-.003),(.004,.014),(-.004,.014)]])
                ob=G.loft('Lower cooling comb '+str(i),rows,b.m['gloss_black']);b.add(ob,category='trim')
                for f in ob.data.polygons:f.use_smooth=False
