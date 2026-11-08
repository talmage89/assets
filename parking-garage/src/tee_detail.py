"""PCI Fig17-inspired 12ft / 30in tee, dapped to existing 24in end seats.

The 1997 manual §6.2.1.2 describes dapped ends to reduce framing depth.
End reinforcement/strand design is outside this visual construction model.
"""
from geometry import Mesh
from plan import TEE,SPAN,FLOOR,deck_z,end_fade
import bpy,bmesh
from mathutils import Vector


def deepen(root,p):
    count=0
    for rr in list(root.children):
        if rr.get('module_kind')!='DoubleTee':continue
        for ob in list(rr.children):
            if ob.type=='MESH':bpy.data.objects.remove(ob,do_unlink=True)
        source(rr)
        x,cy,z=rr.location;lev=round(z/FLOOR);ramp=rr.name.startswith('Ramp_')
        for ob in rr.children:
            if ob.type!='MESH':continue
            for v in ob.data.vertices:
                q=v.co.copy();vy=q.y;zz=q.z+deck_z(p,lev,x+q.x,cy+q.y,ramp)-lev*FLOOR
                if q.z<=-.049 and ((not ramp and q.y>0) or (ramp and q.y<0)):
                    vy-=.43*abs(q.y)/(SPAN/2-.22)
                if abs(q.z+.6846)<1e-5:zz-=.0004+.01*(SPAN/2-abs(q.y))*end_fade(p,x+q.x)
                v.co=(q.x,vy,zz)
            bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
        count+=1
    for rr in root.children:
        if rr.get('module_kind')!='Fixture':continue
        rr.location.z-=.1524
        for ob in rr.children:
            if ob.type!='MESH':continue
            ob.data=ob.data.copy()
            for v in ob.data.vertices:
                if v.co.z>.30:v.co.z+=.1524
    return count


def source(r):
    b=Mesh(r.name+'__DoubleTee__Mesh',r);x=(TEE-.020)/2;s=TEE/4;fl=.1016
    def section(depth):
        top=-.05-fl;h=-.05-depth;t=.098425;bt=.060325;c=.0762
        return [(-x,-.05),(x,-.05),(x,top),(s+t+c,top),(s+t,top-c),(s+bt,h),(s-bt,h),(s-t,top-c),(s-t-c,top),
                (-s+t+c,top),(-s+t,top-c),(-s+bt,h),(-s-bt,h),(-s-t,top-c),(-s-t-c,top),(-x,top)]
    ys=[-SPAN/2+.22,-SPAN/2+.70,-SPAN/2+.72,0,SPAN/2-.72,SPAN/2-.70,SPAN/2-.22]
    sec=[section(.6096 if i in (0,1,5,6) else .762) for i in range(len(ys))];n=len(sec[0])
    vs=[(xx,y,z) for y,ss in zip(ys,sec) for xx,z in ss]
    fs=[tuple(reversed(range(n))),tuple(range((len(ys)-1)*n,len(ys)*n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(ys)-1) for i in range(n)]
    b.geom(vs,fs)
    def skin(section,mat):
        n=len(section);ys=[-SPAN/2+.03,0,SPAN/2-.03];vs=[(xx,yy,zz) for yy in ys for xx,zz in section]
        fs=[tuple(reversed(range(n))),tuple(range(2*n,3*n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(2) for i in range(n)]
        b.geom(vs,fs,mat)
    skin([(-x,0),(x,0),(x,-.05),(-x,-.05)],'Deck')
    skin([(TEE/2-.011,-.010),(TEE/2+.011,-.010),(TEE/2+.011,.002),(TEE/2-.011,.002)],'Seal')
    for sy in (-1,1):
        for sx in (-1,1):b.box((sx*s,sy*(SPAN/2-.34),-.6721),(.24,.22,.025),'Seal')
    for y in (-6.1,0,6.1):b.box((x-.075,y,-.048),(.12,.10,.008),'Steel')
    return b.finish()
