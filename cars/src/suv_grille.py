"""Alder's open double-chevron grille and separate lower cooling comb.

Sixteen molded blades sit 42 mm ahead of the radiator bed. Two bowed carriers
connect them and support the badge stem. Eighteen straight matte lower fins
are distinct. The 636 game triangles replace 560 former ribs/webs plus 76
triangles of required support; this is real open geometry.
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
                # Continue normals through the shallow molded bend while the
                # 90-degree rectangular-section edges remain manufactured edges.
                G.smooth(ob,35)
            for v in [.30,.70]:
                rows=[]
                for j in range(6):
                    p=sample(.018+.964*j/5,v);p.y-=.028
                    rows.append([tuple(p+Vector((0,dy,dz))) for dy,dz in [(-.012,-.0045),(.012,-.0045),(.012,.0045),(-.012,.0045)]])
                ob=G.loft('Grille structural rail '+str(v),rows,b.m['gloss_black'])
                b.add(ob,category='trim')
            back=sample(.5,.70).y-.020;front=-2.255
            b.add(G.box('Grille badge stem',(0,(front+back)/2,.837),(.026,back-front,.044),b.m['gloss_black'],0),category='trim')
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
