"""Finite caused weather fields over the library's baked limestone charts.

Alpha and color are ordinary glTF vertex data. No new image set, photographic
projection, shader noise, or repeated circular stain stamp is introduced.
"""
import math,random
import bpy,bmesh
from mathutils import Vector


def patch(a,name,origin,u,v,width,height,color,mask,nx=10,ny=7):
    m=a.mesh(name,kind='CausedWeather',authored_winding=True,allow_boundary=True)
    vs=[Vector(origin)+Vector(u)*(width*i/nx)+Vector(v)*(height*j/ny) for j in range(ny+1) for i in range(nx+1)]
    fs=[]
    for j in range(ny):
        for i in range(nx):
            k=j*(nx+1)+i;fs.append((k,k+1,k+nx+2,k+nx+1))
    m.geom(vs,fs,'Concrete',color);ob=m.finish();me=ob.data
    ma=bpy.data.materials.get('CivicWeather')
    if not ma:
        ma=a.materials[3].copy();ma.name='CivicWeather';ma.use_backface_culling=False
        vc=next(n for n in ma.node_tree.nodes if n.type=='VERTEX_COLOR')
        ma.node_tree.links.new(vc.outputs['Alpha'],ma.node_tree.nodes.get('Principled BSDF').inputs['Alpha'])
        ma.surface_render_method='DITHERED'
    me.materials.clear();me.materials.append(ma)
    for face in me.polygons:face.material_index=0
    uv=me.uv_layers.active;attr=me.color_attributes['Tint']
    for loop in me.loops:
        index=loop.vertex_index;i=index%(nx+1);j=index//(nx+1)
        attr.data[loop.index].color=(*color,max(0,min(.88,mask(i/nx,j/ny))))
        uv.data[loop.index].uv=(width*i/nx/4,.009+.23*j/ny)
    ob['cause']=name;return ob


def walls(a,p):
    rng=random.Random(p['seed']+81);w,d=p['width'],p['depth'];floor=p['floor']
    top=6 if p['program']=='station' else floor+p['stories']*p['story_pitch']
    faces=[('front',(-w/2,-d/2-.003,0),(1,0,0),w),
        ('rear',(w/2,d/2+.003,0),(-1,0,0),w),('east',(w/2+.003,-d/2,0),(0,1,0),d),
        ('west',(-w/2-.003,-d/2,0),(0,1,0),d)]
    if p['program']=='station':
        faces=[('rear',(-w/2+p['bayblock'],d/2+.003,0),(-1,0,0),p['bayblock']),
            ('west',(-w/2-.003,-d/2,0),(0,1,0),d)]
        if p['office']:faces += [('front',(-w/2+p['bayblock'],-d/2-.003,0),(1,0,0),p['office']),
            ('east',(w/2+.003,-d/2,0),(0,1,0),12.192)]
    for face,origin,u,length in faces:
        phase=rng.uniform(0,6);vertical=(0,0,1)
        # Splash occurs below 0.45m; the irregular edge does not make a band.
        patch(a,'RainSplash_'+face,origin,u,vertical,length,.55,(.075,.063,.038),
            lambda s,t:.55*max(0,1-t/(.45+.35*math.sin(s*19+phase)**2))*(.45+.55*math.sin(s*31+phase)**2),nx=round(length/.45),ny=5)
        if face!='front' or p['program']!='station':
            o=Vector(origin)+Vector((0,0,top-1.35))
            leaks=[(rng.uniform(.025,.975),rng.uniform(.008,.027),rng.uniform(.24,.52),rng.uniform(.25,.65)) for _ in range(rng.randint(6,10))]
            def runoff(s,t,leaks=leaks):
                return .055*t**4+sum(strength*math.exp(-((s-center)/width)**2)*max(0,(t-end)/(1-end))**.55 for center,width,strength,end in leaks)
            patch(a,'CorniceShelterAndWash_'+face,o,u,vertical,length,1.35,(.050,.049,.036),
                runoff,nx=round(length/.35),ny=8)
        # Damp masonry discharges salts in distinct low patches near drains.
        for j in range(2 if face=='front' else 1):
            start=length*(.18+.53*j)+rng.uniform(-.5,.5);ww=rng.uniform(1.25,2.1)
            origin2=Vector(origin)+Vector(u)*start+Vector((0,0,floor+.04))
            # Salts creep out along irregular mortar/capillary fronts, rather
            # than making a pale round spot or a repeated row of stamps.
            patch(a,'SaltBloom_'+face+str(j),origin2,u,vertical,ww,.65,(.62,.60,.49),
                lambda s,t,ph=phase:.42*math.sin(s*math.pi)**.65*max(0,1-abs(t-(.26+.09*math.sin(s*19+ph)))/(.09+.07*math.sin(s*31+ph)**2)),nx=16,ny=9)
    # Sill-edge water tracks, placed from the actual exported sash geometry.
    for ob in list(a.objects):
        if ob.get('module_kind') not in ('TallSash','AluminumWindow'):continue
        angle=math.radians(ob['weather_yaw_degrees']);axis=Vector((math.cos(angle),math.sin(angle),0));normal=Vector((math.sin(angle),-math.cos(angle),0))
        for side in (-1,1):
            if rng.random()<.18:continue
            length=rng.uniform(.55,1.10);width=rng.uniform(.22,.41);strength=rng.uniform(.34,.52)
            center=Vector(ob['weather_origin_m']);center.z-=length+.15
            o=center+axis*(side*(ob['weather_width_m']/2+width/2+.015)-width/2)+normal*.003
            patch(a,'SillRunoff_'+ob.name+str(side),o,axis,(0,0,1),width,length,(.083,.078,.050),
                lambda s,t,st=strength:st*math.sin(s*math.pi)**2*t**.55,nx=4,ny=9)
    repairs(a,p)
    if p['program']=='station' and p['office']:
        # An open scupper discharges down the exposed block wall behind the
        # crew wing. The stain starts below its actual spout, not on a grid.
        xx=-w/2+p['bayblock'];yy=5.3
        m=a.mesh('BlockWallScupper',kind='Scupper',trim_strip=2)
        m.box((xx+.16,yy,5.88),(.35,.32,.12),'Trim',(.22,.23,.20));m.finish()
        patch(a,'BlockScupperRunoff',(xx+.004,yy-.6,2.4),(0,1,0),(0,0,1),1.2,3.37,(.058,.067,.044),
            lambda s,t:.45*math.exp(-((s-.5)/(.095+.16*(1-t)))**2)*t**.35,nx=8,ny=16)
    guard_openings(a)


def guard_openings(a):
    """Weather belongs on wall surfaces; it cannot bridge a glazing/door hole.

    Expand the real opening bounds by more than the weather grid cell. Every
    corner of a triangle over an opening then has zero coverage, including
    triangles straddling its edge. This is coverage, not a collision solid.
    """
    holes=[]
    for ob in a.objects:
        if 'weather_origin_m' not in ob:continue
        angle=math.radians(ob['weather_yaw_degrees']);cs,sn=math.cos(angle),math.sin(angle)
        holes.append((Vector(ob['weather_origin_m']),Vector((cs,sn,0)),Vector((sn,-cs,0)),ob['weather_width_m']/2+.50,ob['weather_height_m']))
    for ob in list(a.objects):
        if ob.get('module_kind')!='CausedWeather' or not any(s in ob.name for s in ('RainSplash','CorniceShelter','SaltBloom','SillRunoff')):continue
        zero=set()
        for vertex in ob.data.vertices:
            for origin,axis,normal,half,height in holes:
                delta=vertex.co-origin
                if abs(delta.dot(normal))<.02 and abs(delta.dot(axis))<half and -.20<delta.z<height+.20:
                    zero.add(vertex.index);break
        tint=ob.data.color_attributes['Tint']
        for loop in ob.data.loops:
            if loop.vertex_index in zero:tint.data[loop.index].color[3]=0
        # No invisible sheet faces across openings, or empty-mask geometry.
        bm=bmesh.new();bm.from_mesh(ob.data);layer=bm.loops.layers.float_color['Tint']
        discard=[face for face in bm.faces if all(loop[layer][3]<.000001 for loop in face.loops)]
        bmesh.ops.delete(bm,geom=discard,context='FACES');bm.to_mesh(ob.data);bm.free();ob.data.update()
        if not ob.data.polygons:
            a.objects.remove(ob);bpy.data.objects.remove(ob,do_unlink=True)


def repairs(a,p):
    """Wrong-color repointing follows bed/perpend joints, in bounded repairs."""
    rng=random.Random(p['seed']+218);m=a.mesh('RepointedRepairs',kind='RepointedMasonry',trim_strip=5,authored_winding=True)
    front=-p['depth']/2-.004;course=1.2192/18;brick=.2032
    repairs=[(-p['width']*.40,p['floor']+.10,1.3,6),(p['width']*.34,p['floor']+1.65,1.0,6),(-p['width']*.22,p['floor']+.10,1.9,6)]
    if p['program']=='station':repairs=[(-p['width']*.38,4.75,1.3,6),(-p['width']*.14,5.12,1.6,5)]
    for cx,cz,wide,rows in repairs:
        for j in range(rows):
            z=p['floor']+round((cz-p['floor'])/course+j)*course;left=cx-wide/2+rng.uniform(-.10,.14);right=cx+wide/2-rng.uniform(0,.23)
            m.geom([(left,front,z-.003),(right,front,z-.003),(right,front,z+.003),(left,front,z+.003)],[(0,1,2,3)],'Trim',(.32,.30,.242))
            for k in range(math.ceil((right-left)/brick)):
                x=(math.floor(left/brick)+k+(j%2)*.5)*brick
                if not left<x<right:continue
                m.geom([(x-.003,front,z),(x+.003,front,z),(x+.003,front,z+course-.007),(x-.003,front,z+course-.007)],[(0,1,2,3)],'Trim',(.32,.30,.242))
    m.finish()


def rust(a,p,name,length=.48):
    x,y,z=p
    patch(a,name,(x-.15,y-.06,z),(1,0,0),(0,1,0),.30,length,(.24,.058,.012),
        lambda s,t:.56*math.exp(-((s-.5)/(.10+.18*t))**2)*(1-t)**.8,nx=3,ny=4)
