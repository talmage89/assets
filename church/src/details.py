"""Construction connections and visible community-use fixtures."""
import math,json
from pathlib import Path
import geometry as G
from hardware import doors


def side_exit(parent,p,point,yaw=90):
    rt=G.root('Accessible side exit',point,parent,module_kind='ExitBay');rt.rotation_euler.z=math.radians(yaw)
    w=p['bay'];h=p['eave'];t=p['wall'];gap=2.22;top=2.90
    m=G.Mesh('Side exit pierced masonry',rt,floor=p['floor'])
    for s in (-1,1):m.box((s*(w/2+gap/2)/2,0,h/2),(w/2-gap/2,t,h),'brick')
    m.box((0,0,(top+h)/2),(gap,t,h-top),'brick');m.finish()
    doors('Side panic doors',rt,(0,-t/2-.08,p['floor']))
    return rt


def fittings(parent,p):
    w=p['width'];l=p['length'];modern=p['style']=='aframe'
    m=G.Mesh('Bike rack and cornerstone',parent,module_kind='Fixtures')
    x=w/2+1.4;y=-l/2-3.2
    for j in range(3):
        xx=x+j*.8;m.tube([(xx,y,0),(xx,y,.65),(xx+.08,y,.80),(xx+.60,y,.80),(xx+.68,y,.65),(xx+.68,y,0)],.024,'iron',10)
    m.box((-w/2+.65,-l/2-.025,.48),(.75,.10,.30),'stone')
    m.finish()
    # The alphabet sheet also supplies the fictional cornerstone date.
    chars=json.loads(Path('build/letters.json').read_text());m=G.Mesh('Original cornerstone date',parent,sheet=True)
    for j,c in enumerate(str(p['date'])):m.panel(-w/2+.43+j*.12,-l/2-.082,.49,.11,.20,'letters',chars[c])
    m.finish()
    if modern:
        for i in range(p['bays']+1):
            m=G.Mesh('Bent steel shoes '+str(i),parent,module_kind='BentShoe');yy=-l/2+i*p['bay']
            for s in (-1,1):
                x=s*(p['ridge']-.70-.15)/math.tan(math.radians(p['pitch']))
                m.box((x,yy,.16),(.56,.91,.025),'iron')
                for off in (-.35,.35):
                    m.box((x,yy+off,.38),(.64,.018,.42),'iron')
                    for z in (.29,.46):m.tube([(x,yy+off-.025,z),(x,yy+off+.025,z)],.021,'bronze',8)
                for dx in (-.22,.22):
                    for dy in (-.36,.36):m.tube([(x+dx,yy+dy,.16),(x+dx,yy+dy,.21)],.018,'bronze',6)
            m.finish()
