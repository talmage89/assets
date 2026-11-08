"""Era-specific construction cues; inferred from the cited park photographs."""
import math


def exterior(a,p):
    L,W,F,E=p['length'],p['width'],p['floor'],p['eave']
    m=a.mesh('EraDetails',component='era_details')
    if p['era']=='1972':
        # Factory two-tone waist, formed cap and seam cover. Openings start
        # above this band, so it never paints across glass or a door leaf.
        for sy in (-1,1):
            door=-L*.035 if sy<0 else L*.26
            dw=.9144 if p['double'] else .813
            for x0,x1 in ((-L/2,door-dw/2-.07),(door+dw/2+.07,L/2)):
                m.box(((x0+x1)/2,sy*(W/2+.009),F+.37),(x1-x0,.018,.68),'Siding',p['accent'])
                m.box(((x0+x1)/2,sy*(W/2+.021),F+.73),(x1-x0,.028,.035),'Trim')
        for sx in (-1,1):
            m.box((sx*(L/2+.012),0,F+.37),(.024,W,.68),'Siding',p['accent'])
            m.box((sx*(L/2+.024),0,F+.73),(.025,W,.035),'Trim')
    # Porch lights have a wall back, downward hood and opaque warm diffuser.
    for sy,u in ((-1,-L*.035),(1,L*.26)):
        y=sy*(W/2+.065);x=u+.65
        m.box((x,y,F+1.76),(.13,.075,.23),'Trim',(.055,.058,.049),r=.012)
        m.box((x,y+sy*.055,F+1.72),(.10,.055,.12),'Trim',(.61,.55,.37),r=.008)
        m.box((x,y+sy*.040,F+1.87),(.19,.16,.055),'Trim',(.045,.049,.041))
    if p['era']=='1996':
        # Gabled shallow entry canopy; actual posts bear on the deck, not air.
        x=-L*.035;front=-W/2-1.85;back=-W/2+.12
        for sx in (-1,1):
            xx=x+sx*1.28
            m.box((xx,front,F+1.10),(.0889,.0889,2.20),'Trim')
            m.beam((xx,front,F+1.75),(xx-sx*.28,front,F+2.20),.055,.055,'Trim',r=0)
        for sy in (front,back):
            m.box((x,sy,F+2.18),(2.70,.09,.14),'Trim')
        for sx in (-1,1):
            m.prism([(x,back,F+2.60),(x+sx*1.45,back,F+2.26),
                     (x+sx*1.45,front-.18,F+2.26),(x,front-.18,F+2.60)],
                    (0,0,-1),.075,'Shingles')
            m.beam((x,front-.18,F+2.59),(x+sx*1.45,front-.18,F+2.25),.055,.10,'Trim',r=0)
    m.finish()


def window(a,p,face,h,xf):
    u,w,z,ht=h['u'],h['w'],h['z'],h['h']
    m=a.mesh('WindowDetails_'+face,component='window_detail')
    # Outside storm frame stands 65mm proud of siding, with a deep sill.
    for uu in (u-w/2+.014,u+w/2-.014):
        m.box((uu,.065,z+ht/2),(.028,.035,ht+.024),'Trim',(.43,.45,.43),xf=xf)
    for zz in (z-.008,z+ht+.008):
        m.box((u,.065,zz),(w+.04,.035,.028),'Trim',(.43,.45,.43),xf=xf)
    m.box((u,.09,z-.035),(w+.13,.18,.035),'Trim',xf=xf)
    if p['era']=='1972':
        # Folded aluminum hood, hems and side cheeks. Supported at the wall.
        yy=.62;top=z+ht+.18
        m.prism([xf((u-w/2-.12,0,top)),xf((u+w/2+.12,0,top)),
                 xf((u+w/2+.12,yy,top-.19)),xf((u-w/2-.12,yy,top-.19))],(0,0,-1),.012,'Trim',p['accent'])
        for uu in (u-w/2-.12,u+w/2+.12):
            m.prism([xf((uu,0,top)),xf((uu,yy,top-.19)),xf((uu,0,top-.40))],(0,0,-1),.012,'Trim',p['accent'])
        for j in range(5):
            d=(j+.5)*yy/5;m.box((u,d,top-.19*d/yy+.006),(w+.25,.018,.016),'Trim',xf=xf)
    elif p['era']=='1996':
        for sx in (-1,1):
            xx=u+sx*(w/2+.19)
            m.box((xx,.045,z+ht/2),(.25,.035,ht+.08),'Trim',p['accent'],xf=xf)
            for j in range(9):m.box((xx,.070,z+.08+j*(ht-.10)/9),(.21,.014,.035),'Trim',p['accent'],xf=xf)
    m.finish()


def steps(a,p):
    # Every inspection home includes both landings; the site instances them
    # as part of the home. Their pivots and deck sockets stay independent.
    from addons import deck
    from geometry import place
    L,W=p['length'],p['width']
    d=deck(a.root.name+'_Deck',p['deck_width'],height=p['floor']-.025,seed=p['seed'])
    place(d.root,(-L*.035,-W/2-1.11,0),parent=a.root)
    b=deck(a.root.name+'_BackSteps',1.22,1.0,p['floor']-.025,p['seed']+1)
    place(b.root,(L*.26,W/2+.55,0),180,parent=a.root)
