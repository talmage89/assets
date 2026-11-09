"""Postwar glazing, garden wings and later brick additions."""
import math
import geometry as G
from hardware import doors


def glazed_end(parent,p,y,back=False):
    rt=G.root('Glazed rear gable' if back else 'Glazed entry gable',(0,y,0),parent,module_kind='GlazedGable')
    if back:rt.rotation_euler.z=math.pi
    w=p['width'];peak=p['ridge'];e=p['eave'];m=G.Mesh('Gable glazing mullions and plinth',rt)
    # Full gable glazing is subdivided by structural timber and steel sash.
    def top(x):return peak-abs(x)/(w/2)*(peak-e)-.25
    cells=12;dx=w/cells
    for i in range(cells):
        a=-w/2+i*dx+.04;b=a+dx-.08
        z0=.72 if abs((a+b)/2)>1.2 else 2.43
        m.geom([(a,-.02,z0),(b,-.02,z0),(b,-.02,top(b)),(a,-.02,top(a))],[(0,1,2,3)],'stained',uv=[[(.50+(a/w+.5)*.49,.02),( .50+(b/w+.5)*.49,.02),(.50+(b/w+.5)*.49,.48),(.50+(a/w+.5)*.49,.48)]])
        m.beam((a,-.10,z0),(a,-.10,top(a)),.065,.10,'iron')
        m.box(((a+b)/2,0,.36),(b-a,.25,.72),'brick')
    for z in (2.43,4.7,7.0,9.3,11.6,13.9):
        hw=w/2 if z<e else (peak-z)/(peak-e)*w/2
        if hw>.2:m.box((0,-.10,z),(2*hw,.12,.07),'iron')
    m.finish();doors('Modern front doors' if not back else 'Modern rear exit',rt,(0,-.13,.1524),modern=True)
    return rt


def additions(parent,p):
    from buildings import wing
    w=p['width'];l=p['length']
    if p['style']=='aframe':
        if 'hall' in p['wings']:wing(parent,'Fellowship hall',(w/2+10.5,l/2+3.5,0),(21.0,12.2,4.25))
        if 'education' in p['wings']:wing(parent,'Education wing',(w/2+21.8,2.0,0),(8.53,24.4,3.5))
        m=G.Mesh('Covered courtyard connection',parent,module_kind='Canopy')
        y=-l/2+5.0
        m.box((w/2+9.5,y,3.20),(19.0,3.66,.27),'stone',(.75,.79,.77))
        for x in (w/2+1,w/2+9.6,w/2+17.8):
            for yy in (y-1.52,y+1.52):
                m.box((x,yy,1.52),(.15,.15,3.04),'iron');m.box((x,yy,.10),(.50,.50,.20),'concrete')
        m.finish()
        m=G.Mesh('Garden memorial bench',parent,module_kind='Bench')
        for x in (w/2+5,w/2+10):
            for yy in (2.0,2.4):m.box((x,yy,.25),(.24,.20,.50),'stone')
        m.box((w/2+7.5,2.2,.54),(5.5,.60,.12),'stone');m.finish()
    elif 'hall' in p['wings']:
        wing(parent,'1958 parish hall',(w/2+5.0,l/2-4,0),(10.0,14.63,4.12),False)
        m=G.Mesh('Hall connecting hyphen',parent,module_kind='Hyphen');m.box((w/2+1.0,l/2-10.5,1.55),(2.0,2.5,3.1),'brick');m.box((w/2+1.0,l/2-10.5,3.17),(2.3,2.8,.14),'asphalt');m.finish()
    if 'transepts' in p['wings']:
        for s in (-1,1):wing(parent,'Transept '+str(s),(s*(w/2+3),l/2-6,0),(6,8.53,6.5),False)
