"""Original bent galvanized mailbox, returned door, real pivots and half-lap timber."""
import sys,math
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as G,materials as M
from kit.prop import Build,arguments
import dimensions as D

def arch(r,bottom,spring,n):
    return [(-r,bottom),(-r,spring)]+[(r*math.cos(math.pi-i*math.pi/n),spring+r*math.sin(math.pi-i*math.pi/n)) for i in range(1,n+1)]+[(r,bottom)]

def wood(wear,horizontal=False):
    n=M.Nodes('Weathered end-grain cedar' if horizontal else 'Weathered vertical cedar');c=M.common(n);p=c['position'];x,y,z=n.split(p)
    grain=n.noise(n.vec('MULTIPLY',p,(1,1,.025) if not horizontal else (1,.025,1)),95,4)
    ridges=n.math('POWER',n.ramp(grain,.28,.68),3)
    exposure=n.ramp(z,.1,.4) if not horizontal else .75
    col=n.mix(grain,(.19,.105,.046),(.40,.29,.17),True)
    col=n.mix(n.mul(wear,.55,exposure),col,(.26,.25,.22),True)
    damp=n.mul(wear,n.ramp(z,.17,.015),n.ramp(n.noise(p,38,3),.2,.75))
    col=n.mix(damp,col,(.045,.038,.022),True)
    # Fine longitudinal checking comes from the wood fibers, broken by grain.
    cracks=n.mul(n.ramp(grain,.68,.78),wear)
    fiber=n.noise(n.vec('MULTIPLY',p,(1,.008,1) if horizontal else (1,1,.008)),380,3)
    col=n.mix(n.mul(wear,n.ramp(fiber,.57,.74),.4),col,(.09,.073,.048),True)
    nx,ny,nz=n.split(c['normal']);end=n.ramp(n.math('ABSOLUTE',ny if horizontal else nz),.7,.95)
    xx=n.add(x,-.012);vv=n.add(z,-1.0025) if horizontal else n.add(y,-.018)
    radius=n.math('SQRT',n.add(n.mul(xx,xx),n.mul(vv,vv)))
    rings=n.math('SINE',n.add(n.mul(radius,1300),n.mul(n.noise(p,47,3),15),n.mul(grain,.7)))
    endcol=n.mix(n.ramp(rings,-.5,.6),(.23,.19,.14),(.28,.24,.18),True)
    col=n.mix(end,col,endcol,True)
    return n.finish(col,.86,0,n.add(n.mul(ridges,.00018),n.mul(cracks,-.00035),n.mul(fiber,.0001)))

def enamel(wear,red=False,floor=False):
    n=M.Nodes('Red signal enamel' if red else 'Black galvanized powder coat');c=M.common(n);p=c['position'];x,y,z=n.split(p)
    noise=n.noise(p,380,3);edge=c['edge'];cavity=c['cavity']
    chipped=n.mul(wear,n.maximum(n.mul(edge,.65),n.mul(n.ramp(z,.025,0),.4)),n.ramp(noise,.64,.78))
    base=(.40,.008,.004) if red else (.004,.005,.004)
    col=n.mix(chipped,base,(.24,.26,.25),True)
    rust=n.mul(chipped,n.ramp(n.noise(p,115,3),.54,.69),.65)
    col=n.mix(rust,col,(.16,.055,.016),True)
    drip=n.mul(wear,cavity,.18,n.ramp(n.noise(n.vec('MULTIPLY',p,(3,3,.15)),150,2),.32,.65))
    col=n.mix(drip,col,(.042,.031,.018),True)
    h=n.mul(n.math('SUBTRACT',noise,.5),7e-6)
    if floor:
        # Raised pressed dimples: 19 mm pitch, ~3 mm crown, reduced to normal detail.
        wave=n.mul(n.math('COSINE',n.mul(x,math.tau/.019)),n.math('COSINE',n.mul(y,math.tau/.019)))
        h=n.add(h,n.mul(n.ramp(wave,.55,.95),.0031))
    return n.finish(col,n.mix(chipped,.32 if red else .23,.72),n.mul(chipped,.72),h)

def main():
    a=arguments();b=Build('Mailbox',a.quality,a.wear);count=64 if b.high else 20
    black=enamel(a.wear);red=enamel(a.wear,True);timber=wood(a.wear);armmat=wood(a.wear,True);zinc=b.metal();r=D.WIDTH/2
    door=G.pivot('Door',(0,D.DOOR_Y,D.DOOR_Z),'X',(0,105));door.parent=b.root
    flag=G.pivot('Flag',D.FLAG,'X',(0,90));flag.parent=b.root
    # Hollow U-section, open front; each plate has real steel gauge.
    outer=arch(r,D.BOTTOM,D.SPRING,count);inner=arch(r-D.GAUGE,D.BOTTOM,D.SPRING,count)
    b.add(G.smooth(G.profile('Bent galvanized shell',outer+list(reversed(inner)),-D.LENGTH/2,D.LENGTH/2,black,axis='Y')))
    b.add(G.profile('Seamed rear panel',arch(r-D.GAUGE,D.BOTTOM,D.SPRING,count),D.LENGTH/2-D.GAUGE,D.LENGTH/2,black,axis='Y'))
    b.add(G.box('Pressed metal floor',(0,0,D.FLOOR-D.GAUGE/2),(D.WIDTH-2*D.GAUGE,D.LENGTH-D.GAUGE,D.GAUGE),enamel(a.wear,floor=True),0))
    # Thin returned door wraps the shell with 1.2 mm radial running clearance.
    outline=arch(r+.002,D.FLOOR-.004,D.SPRING,count)
    face=G.profile('Door stamped face',outline,D.DOOR_Y-.0008,D.DOOR_Y,black,axis='Y')
    if b.high:
        mark=M.print_material('Original 1847 address',Path('build/markings/address.png').resolve(),base=black)
        face.data.materials.append(mark);uv=face.data.uv_layers.new(name='PrintUV')
        for polygon in face.data.polygons:
            polygon.material_index=1 if polygon.normal.y<-.9 else 0
            for i in polygon.loop_indices:
                v=face.data.vertices[face.data.loops[i].vertex_index].co
                uv.data[i].uv=((v.x+r+.002)/(2*(r+.002)),(v.z-(D.FLOOR-.004))/(D.SPRING+r+.002-(D.FLOOR-.004)))
    b.add(face,door)
    rim_inner=arch(r+.0012,D.FLOOR-.004,D.SPRING,count)
    b.add(G.smooth(G.profile('Door returned edge',outline+list(reversed(rim_inner)),D.DOOR_Y,-D.LENGTH/2+.012,black,axis='Y')),door)
    # Hinge is two coaxial end-pin joints, not intersecting solid cylinders.
    for sign in [-1,1]:
        x=sign*(r+.001)
        b.add(G.cylinder('Fixed hinge pin', (x-sign*.004,D.DOOR_Y,D.DOOR_Z),(x+sign*.005,D.DOOR_Y,D.DOOR_Z),.0022,zinc,12))
        tab=G.lathe('Door hinge ear',[(x-.0004,.0024),(x-.0004,.005),(x+.0004,.005),(x+.0004,.0024)],black,32 if b.high else 12,axis='X',center=(D.DOOR_Y,D.DOOR_Z),closed=True)
        b.add(tab,door)
        b.add(G.box('Fixed hinge bracket',(sign*(r+.0056),-D.LENGTH/2+.002,D.DOOR_Z),(.0008,.016,.010),black,0))
        b.add(G.box('Fixed hinge anchor',(sign*(r+.0026),-D.LENGTH/2+.010,D.DOOR_Z-.001),(.0068,.006,.004),black,0))
    # Pull strap and roof catch, with real separation except the latch contact.
    ztop=D.SPRING+r+.002
    for name,center,size in [
      ('Door pull stem',(0,D.DOOR_Y-.004,ztop-.018),(.014,.006,.036)),
      ('Door pull curl',(0,D.DOOR_Y-.012,ztop-.002),(.018,.022,.006))]:
        b.add(G.box(name,center,size,black,.001 if b.high else 0,2),door)
    catch=[(-.207,ztop-.0024),(-.219,ztop-.0024),(-.225,ztop+.003),(-.259,ztop+.003),(-.259,ztop+.001),(-.260,ztop+.001),(-.260,ztop+.004),(-.225,ztop+.004),(-.219,ztop-.0014),(-.207,ztop-.0014)]
    b.add(G.profile('Roof spring catch',catch,-.007,.007,zinc,axis='X',radius=.0002 if b.high else 0))
    # A flat stamped flag, parallel to the side; raised +90 about X.
    pts=[(-.009,-.008),(.14,-.008),(.14,-.035),(.205,-.035),(.205,.035),(.14,.035),(.14,.008),(-.009,.008)]
    ob=G.profile('Flag red stamped blade',[(u+D.FLAG[1],v+D.FLAG[2]) for u,v in pts],D.FLAG[0]-.0005,D.FLAG[0]+.0005,red,axis='X',radius=.0004 if b.high else 0)
    b.add(ob,flag)
    b.add(G.cylinder('Flag nylon stand-off',(r-.0001,D.FLAG[1],D.FLAG[2]),(D.FLAG[0]-.0005,D.FLAG[1],D.FLAG[2]),.007,zinc,16))
    b.add(G.cylinder('Flag pivot cap',(D.FLAG[0]+.0005,D.FLAG[1],D.FLAG[2]),(D.FLAG[0]+.003,D.FLAG[1],D.FLAG[2]),.005,zinc,12),flag)
    # Half-lap: post's left half supports the arm's right half at the joint.
    w=.04445;y0=.15555;y1=.24445
    post=[(-w,0),(w,0),(w,D.ARM_BOTTOM),(0,D.ARM_BOTTOM),(0,D.ARM_TOP),(-w,D.ARM_TOP)]
    b.add(G.profile('Wood notched 4x4 post',post,y0,y1,timber,axis='Y',radius=.0006 if b.high else 0))
    arm=[(-w,-.20),(w,-.20),(w,.27),(-w,.27),(-w,y1),(0,y1),(0,y0),(-w,y0)]
    b.add(G.profile('Wood half-lap arm',arm,D.ARM_BOTTOM,D.ARM_TOP,armmat,axis='Z',radius=.0006 if b.high else 0))
    b.add(G.box('Wood mounting board',(0,0,D.ARM_TOP+.01905/2),(.145,.45,.01905),armmat,.0005 if b.high else 0))
    b.bolt('Timber joint bolt',(.045,.20,(D.ARM_BOTTOM+D.ARM_TOP)/2),(1,0,0),zinc,.005)
    # Mounting screws enter the board through the lower side skirts.
    for side in [-1,1]:
        for yy in [-.14,.14]:
            b.bolt('Mounting side screw',(side*(r+.001),yy,D.FLOOR-.010),(side,0,0),zinc,.0028)
    # Ground origin is the center of the post's actual footprint.
    for child in b.root.children:
        if child.type=='MESH':
            for vertex in child.data.vertices:vertex.co.y-=.20
        else:child.location.y-=.20
    b.save(a.out,a.quality)
if __name__=='__main__':main()
