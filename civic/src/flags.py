"""Light-breeze cloth under gravity, original graphics using shared paint maps."""
import math
import bpy,bmesh
from geo import orient


def point(u,v):
    # The upper hoist is supported. Gravity gathers the fly inward and down;
    # diagonal stress folds originate at the two halyard clips.
    reach=1.615*u*(.76+.18*(1-v))
    depth=.19*math.sin(u*11-v*4)*math.sin(u*math.pi*.85)+.11*u
    drop=.85*v+.40*u**1.25+.055*math.sin(u*9+v*5)*u
    return (reach,depth,-drop)


def cloth(a,p,name,national=True):
    x,y,z=p;pivot=name+'_Flag';a.pivot(pivot,p,axis='Z',limits=(-180,180))
    m=a.mesh(name+'_Cloth',part=pivot,kind='Flag',trim_strip=4,authored_winding=True,allow_boundary=True)
    xs=sorted(set([i/26 for i in range(27)]+[.4]));ny=26;charts=[]
    white=(.72,.70,.62);red=(.36,.018,.027);blue=(.016,.035,.12)
    for j in range(ny):
        for u,uu in zip(xs,xs[1:]):
            v,vv=j/ny,(j+1)/ny
            color=blue if national and uu<=.400001 and j<14 else red if national and (j//2)%2==0 else white
            if not national:color=(.018,.10,.145) if j<18 else (.53,.35,.065)
            m.geom([point(u,v),point(uu,v),point(uu,vv),point(u,vv)],[(0,1,2,3)],'Trim',color)
            charts += [(u,v),(uu,v),(uu,vv),(u,vv)]
    if national:
        # Fifty five-point stars; no borrowed flag texture or decal sheet.
        for row in range(9):
            count=6 if row%2==0 else 5
            for col in range(count):
                u=.4*(col+(.5 if count==6 else 1))/6;v=(7/13)*(row+.5)/9
                points=[]
                for j in range(10):
                    t=-math.pi/2+j*math.pi/5;r=.014 if j%2==0 else .006
                    q=point(u+math.cos(t)*r/1.615,v+math.sin(t)*r/.85)
                    points.append((q[0],q[1]-.001,q[2]))
                    charts.append((u+math.cos(t)*r/1.615,v+math.sin(t)*r/.85))
                m.geom(points,[tuple(range(10))],'Trim',white)
    else:
        # Fictional Briar Glen: limestone diamond around a three-tier pine.
        for poly,color in [([(.25,.48),(.49,.15),(.73,.48),(.49,.81)],white),
            ([(.33,.62),(.49,.29),(.65,.62)],(.025,.12,.065)),
            ([(.37,.48),(.49,.21),(.61,.48)],(.025,.12,.065))]:
            pts=[point(u,v) for u,v in poly];m.geom([(xx,yy-.001,zz) for xx,yy,zz in pts],[tuple(range(len(pts)))],'Trim',color)
            charts += poly
    orient(m,p,0);ob=m.finish()
    for loop in ob.data.loops:
        u,v=charts[loop.vertex_index];ob.data.uv_layers.active.data[loop.index].uv=(u*1.615/4,.504+v*.117)
    # Cell colors remain CORNER data across the stripe/canton boundaries,
    # while coincident positions share a smooth cloth normal field.
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bm.to_mesh(ob.data);bm.free();ob.data.update()
    ma=bpy.data.materials.get('CivicFlagCloth')
    if not ma:
        ma=a.materials[4].copy();ma.name='CivicFlagCloth';ma.use_backface_culling=False
    ob.data.materials.clear();ob.data.materials.append(ma)
    for face in ob.data.polygons:face.material_index=0;face.use_smooth=True
    ob['flag_design']='United States, 50 stars / 13 stripes' if national else 'Fictional Briar Glen pine and limestone'


def pole(a,p,name,national=True):
    x,y,z=p;m=a.mesh(name,kind='Flagpole',trim_strip=2,weather=True)
    m.box((x,y,z+.06),(.48,.48,.12),'Concrete',(.32,.31,.27))
    m.tube([(x,y,z+.12),(x,y,z+9.1)],.044,'Trim',(.48,.49,.46),sides=16)
    m.tube([(x,y,z+9.05),(x,y,z+9.15)],.071,'Trim',(.34,.35,.32),sides=12)
    vs=[];n=12
    for zz in (-.065,-.045,0,.045,.065):
        radius=math.sqrt(.075**2-zz**2)
        vs.extend([(x+radius*math.cos(j*math.tau/n),y+radius*math.sin(j*math.tau/n),z+9.22+zz) for j in range(n)])
    fs=[tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))]
    fs += [(row*n+j,row*n+(j+1)%n,(row+1)*n+(j+1)%n,(row+1)*n+j) for row in range(4) for j in range(n)]
    m.geom(vs,fs,'Trim',(.52,.35,.11))
    # Two tensioned halyard falls and a cleat fixed to the shaft.
    for side in (-1,1):
        m.tube([(x+side*.053,y-.016,z+8.99),(x+side*.055,y-.014,z+1.34)],.0032,'Trim',(.38,.35,.27),sides=4)
    m.box((x,y-.052,z+1.32),(.045,.032,.12),'Trim',(.31,.32,.29))
    m.tube([(x-.10,y-.07,z+1.27),(x-.065,y-.09,z+1.32),(x+.065,y-.09,z+1.32),(x+.10,y-.07,z+1.37)],.009,'Trim',(.34,.35,.32),sides=6)
    for zz in (1.31,1.33,1.35):m.tube([(x-.055,y-.095,z+zz),(x+.06,y-.095,z+zz)],.0032,'Trim',(.38,.35,.27),sides=4)
    m.finish();cloth(a,(x+.055,y-.016,z+8.80),name,national)
