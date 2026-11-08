"""Fictional county/date plate; legend uses the original shared bank-card tile."""
import geometry as G


def add(p,parent):
    b=G.Batch('DateAndNamePlaques',parent,'bridge')
    x=-p.length/2+1.4;y=-p.deck_width/2+.44;z=p.deck_z+.50
    b.box((x,y,z),(1.28,.018,.28),'steel')
    top=1 if p.year==1974 else 1-60/512;bottom=top-56/512
    b.geom([(x-.64,y-.010,z-.14),(x+.64,y-.010,z-.14),(x+.64,y-.010,z+.14),(x-.64,y-.010,z+.14)],[(0,1,2,3)],'plants',uv=[(0,bottom),(.5,bottom),(.5,top),(0,top)])
    b.finish()
