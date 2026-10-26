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

def wood(wear,root,horizontal=False):
    from mathutils import Vector
    frame=bpy.data.objects.new('Arm pine grain' if horizontal else 'Post pine grain',None)
    bpy.context.collection.objects.link(frame);frame.parent=root
    if horizontal:
        frame.location=(0,-.40,(D.ARM_TOP+D.ARM_BOTTOM)/2)
        frame.rotation_mode='QUATERNION';frame.rotation_quaternion=Vector((0,0,1)).rotation_difference(Vector((0,1,0)))
    mat=M.weathered_wood('Silvered rough-sawn pine arm' if horizontal else 'Silvered rough-sawn pine post',frame,
        width=.0889,length=.47 if horizontal else D.ARM_TOP,seed=83 if horizontal else 71,
        wear=min(1,wear*1.9),ground_frame=root)
    # Match the darker silvered pine in the installed reference. Preserve the
    # kit's grain/check/splash masks and its explicit bake-channel interface.
    nt=mat.node_tree;out=nt.nodes['OUT_base'];original=out.inputs[0].links[0].from_socket
    grade=nt.nodes.new('ShaderNodeMixRGB');grade.name='Weathered pine tone';grade.blend_type='MULTIPLY'
    grade.inputs[0].default_value=1
    age=min(1,wear/.45);grade.inputs[2].default_value=(1-.40*age,1-.36*age,1-.32*age,1)
    nt.links.new(original,grade.inputs[1]);nt.links.new(grade.outputs[0],out.inputs[0])
    if not horizontal:
        # The post's grade contact stays wet and receives road splash. Reuse
        # the kit's grade/noise mask, at a scale that survives a full hero.
        load=nt.nodes.new('ShaderNodeMath');load.operation='MULTIPLY';load.use_clamp=True
        nt.links.new(nt.nodes['OUT_splash'].outputs[0],load.inputs[0]);load.inputs[1].default_value=2.4
        dirt=nt.nodes.new('ShaderNodeMixRGB');dirt.name='Wet road-splashed post base'
        nt.links.new(load.outputs[0],dirt.inputs[0]);nt.links.new(grade.outputs[0],dirt.inputs[1])
        dirt.inputs[2].default_value=(.022,.025,.017,1);nt.links.new(dirt.outputs[0],out.inputs[0])
    return mat

def enamel(wear,red=False,floor=False,rest_z=0):
    n=M.Nodes('Red signal enamel' if red else 'Black galvanized powder coat');c=M.common(n);p=c['position'];x,y,z=n.split(p)
    z=n.add(z,rest_z)  # Door geometry is rebased to its hinge; recover rest height.
    noise=n.noise(p,380,3);edge=c['edge'];cavity=c['cavity']
    # Door folds/catch and the exposed lower shell edges rub in daily operation.
    fold=n.maximum(edge,n.band(z,D.BOTTOM+.002,.002,.003))
    chipped=n.mul(wear*1.15,fold,n.ramp(n.noise(p,210,3),.50,.68))
    base=(.40,.008,.004) if red else (.004,.005,.004)
    chalk=n.mul(wear*.65,n.maximum(c['up'],.18))
    base=n.mix(chalk,base,(.30,.028,.015) if red else (.022,.024,.021),True)
    col=n.mix(chipped,base,(.24,.26,.25),True)
    rust=n.mul(chipped,n.ramp(n.noise(p,115,3),.54,.69),.65)
    col=n.mix(rust,col,(.16,.055,.016),True)
    drip=n.mul(wear,cavity,.18,n.ramp(n.noise(n.vec('MULTIPLY',p,(3,3,.15)),150,2),.32,.65))
    col=n.mix(drip,col,(.042,.031,.018),True)
    damp=0 if red else n.mul(wear*.65,n.ramp(z,D.BOTTOM+.045,D.BOTTOM+.002),n.ramp(n.noise(n.vec('MULTIPLY',p,(35,35,3)),3,3),.40,.70))
    col=n.mix(damp,col,(.012,.011,.007),True)
    h=n.mul(n.math('SUBTRACT',noise,.5),7e-6)
    if floor:
        # Raised pressed dimples: 19 mm pitch, ~3 mm crown, reduced to normal detail.
        wave=n.mul(n.math('COSINE',n.mul(x,math.tau/.019)),n.math('COSINE',n.mul(y,math.tau/.019)))
        h=n.add(h,n.mul(n.ramp(wave,.55,.95),.0031))
    return n.finish(col,n.mix(chipped,.42 if red else .36,.78),n.mul(chipped,.72),h)

def main():
    a=arguments();b=Build('Mailbox',a.quality,a.wear);count=64 if b.high else 20
    black=enamel(a.wear);doorpaint=enamel(a.wear,rest_z=D.DOOR_Z);red=enamel(a.wear,True);timber=wood(a.wear,b.root);armmat=wood(a.wear,b.root,True);zinc=b.metal();r=D.WIDTH/2
    door=G.pivot('Door',(0,D.DOOR_Y,D.DOOR_Z),'X',(0,105));door.parent=b.root
    flag=G.pivot('Flag',D.FLAG,'X',(0,90));flag.parent=b.root
    # Hollow U-section, open front; each plate has real steel gauge.
    outer=arch(r,D.BOTTOM,D.SPRING,count);inner=arch(r-D.GAUGE,D.BOTTOM,D.SPRING,count)
    b.add(G.smooth(G.profile('Bent galvanized shell',outer+list(reversed(inner)),-D.LENGTH/2,D.LENGTH/2,black,axis='Y')))
    b.add(G.profile('Seamed rear panel',arch(r-D.GAUGE,D.BOTTOM,D.SPRING,count),D.LENGTH/2-D.GAUGE,D.LENGTH/2,black,axis='Y'))
    b.add(G.box('Pressed metal floor',(0,0,D.FLOOR-D.GAUGE/2),(D.WIDTH-2*D.GAUGE,D.LENGTH-D.GAUGE,D.GAUGE),enamel(a.wear,floor=True),0))
    # Thin returned door wraps the shell with 1.2 mm radial running clearance.
    outline=arch(r+.002,D.FLOOR-.004,D.SPRING,count)
    face=G.profile('Door stamped face',outline,D.DOOR_Y-.0008,D.DOOR_Y,doorpaint,axis='Y')
    if b.high:
        mark=M.print_material('Original 1847 address',Path('build/markings/address.png').resolve(),base=doorpaint)
        face.data.materials.append(mark);uv=face.data.uv_layers.new(name='PrintUV')
        for polygon in face.data.polygons:
            polygon.material_index=1 if polygon.normal.y<-.9 else 0
            for i in polygon.loop_indices:
                v=face.data.vertices[face.data.loops[i].vertex_index].co
                uv.data[i].uv=((v.x+r+.002)/(2*(r+.002)),(v.z-(D.FLOOR-.004))/(D.SPRING+r+.002-(D.FLOOR-.004)))
    b.add(face,door)
    rim_inner=arch(r+.0012,D.FLOOR-.004,D.SPRING,count)
    b.add(G.smooth(G.profile('Door returned edge',outline+list(reversed(rim_inner)),D.DOOR_Y,-D.LENGTH/2+.012,doorpaint,axis='Y')),door)
    # Hinge is two coaxial end-pin joints, not intersecting solid cylinders.
    for sign in [-1,1]:
        x=sign*(r+.001)
        b.add(G.cylinder('Fixed hinge pin', (x-sign*.004,D.DOOR_Y,D.DOOR_Z),(x+sign*.005,D.DOOR_Y,D.DOOR_Z),.0022,zinc,12))
        tab=G.lathe('Door hinge ear',[(x-.0004,.0024),(x-.0004,.005),(x+.0004,.005),(x+.0004,.0024)],doorpaint,32 if b.high else 12,axis='X',center=(D.DOOR_Y,D.DOOR_Z),closed=True)
        b.add(tab,door)
        b.add(G.box('Fixed hinge bracket',(sign*(r+.0056),-D.LENGTH/2+.002,D.DOOR_Z),(.0008,.016,.010),black,0))
        b.add(G.box('Fixed hinge anchor',(sign*(r+.0026),-D.LENGTH/2+.010,D.DOOR_Z-.001),(.0068,.006,.004),black,0))
    # Pull strap and roof catch, with real separation except the latch contact.
    ztop=D.SPRING+r+.002
    for name,center,size in [
      ('Door pull stem',(0,D.DOOR_Y-.004,ztop-.018),(.014,.006,.036)),
      ('Door pull curl',(0,D.DOOR_Y-.012,ztop-.002),(.018,.022,.006))]:
        b.add(G.box(name,center,size,doorpaint,.001 if b.high else 0,2),door)
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
        elif child.name not in ('Arm pine grain','Post pine grain'):child.location.y-=.20
    b.save(a.out,a.quality)
if __name__=='__main__':main()
