"""Walk-visible tenant identity with guarded sheet art and inexpensive forms."""
from geometry import *
from strip_graphics import quad


def dressing(m,p,parent,entry,ink,layout):
    w=m['width'];key=m['tenant'];dx=-w*.23
    # Installed vinyl and paper are on the outer glass surface, not a poster
    # apparently suspended in the room. Keep the door's clear hand area.
    quad('Door business hours',key,'window',.9144/2,-.032,1.30,.37,.29,entry,ink,layout)
    if key=='vacant':
        for i in range(3):
            x=-w/2+.74 if i==0 else -.28+i*1.39
            quad('Vacant taped kraft paper','Paper','sign',x,-.044,1.20,1.08,1.63,parent,ink,layout)
        quad('Vacant FOR LEASE',key,'poster',w*.20,-.049,1.54,1.15,.80,parent,ink,layout)
        return
    quad('Tenant glazing vinyl',key,'vinyl',w*.16,-.045,.74,1.61,.33,parent,ink,layout)
    quad('Tenant sale poster',key,'poster',(-w*.04 if key=='pizza' else w*.37),-.046,1.20,.68,.91,parent,ink,layout)
    # OPEN varies in placement instead of one identical black card per door.
    xx=-w*.40 if key in ('pizza','laundry','cleaner') else w*.08
    box('OPEN sign acrylic back',(xx,.035,1.69),(.71,.018,.34),'Black',parent,0)
    quad('Lit OPEN tubing','Open','sign',xx,-.046,1.69,.67,.32,parent,ink,layout)
    for sx in (-.24,.24):beam('OPEN hanging wire',(xx+sx,.035,1.84),(xx+sx,.035,2.17),.003,.003,'Metal',parent)
    if key in ('tax','nails','hair'):
        # A partial blind occupies one pane; slats stop above the display.
        xx=-w*.40
        box('Blind headrail',(xx,.08,2.18),(1.07,.05,.055),'White',parent,0)
        for i in range(12):box('Half drawn blind slat',(xx,.074,2.12-i*.035),(1.04,.033,.016),'White',parent,0)
        for sx in (-.36,.36):beam('Blind cord',(xx+sx,.06,2.15),(xx+sx,.06,1.71),.002,.002,'White',parent)
    if key=='pizza':
        box('Pizza menu backing',(w*.10,5.12,2.30),(2.9,.10,.76),'Black',parent,.008)
        quad('Pizza illuminated menu','PizzaMenu','sign',w*.10,5.061,2.30,2.82,.70,parent,ink,layout)
        x=w*.36;y=1.05
        box('Drinks cooler cabinet',(x,y,1.11),(.83,.68,1.90),'White',parent,.018)['floor_support']=True
        frame('Drinks cooler gasket',x,y-.348,1.19,.76,1.62,'Trim',parent,.028,.028)
        quad('Drinks cooler merchandise','Drinks','sign',x,y-.365,1.19,.68,1.51,parent,ink,layout)
        for j in range(8):
            xx=x-.25+(j%4)*.16;zz=.78+(j//4)*.45
            ob=box('Cooler drink package',(xx,y-.40,zz),(.10,.045,.27),'White',parent,0);ob['product_index']=j
        for zz in (.60,.99,1.38,1.77):box('Cooler shelf',(x,y-.37,zz),(.65,.018,.018),'Metal',parent,0)
        box('Cooler handle',(x-.29,y-.397,1.25),(.018,.026,.38),'Metal',parent,0)
        # Stacked folded cartons have a supported display beside the counter.
        for j in range(5):box('Takeout folded cartons',(w*.18-.7,3.8,1.24+j*.035),(.46,.41,.033),'White',parent,0)
    elif key in ('hair','nails'):
        for j in range(3):
            x=w*.29;y=2.7+j*1.35
            panel('Salon framed mirror',x,y,1.80,1.12,1.30,'Metal',parent,.012)
            frame('Salon mirror surround',x,y-.014,1.80,1.17,1.35,'Primary',parent,.028,.032)
        box('Salon window product shelf',(-w*.40,.85,.76),(.85,.38,1.20),'White',parent,0)['floor_support']=True
        for j in range(7):
            ob=box('Salon shelf product',(-w*.40-.33+j*.11,.77,1.45),(.075,.13,.22),'White',parent,0);ob['product_index']=j
        quad('Salon care products','Products','sign',-w*.40,.651,1.02,.80,.63,parent,ink,layout)
    elif key=='cleaner':
        # Front rack reads from the walk; each folded garment hangs from a
        # measured bar rather than floating in the window.
        x=w*.32;y=1.45
        for xx in (x-.58,x+.58):
            cylinder('Display rack upright',(xx,y,.16),(xx,y,1.83),.018,'Metal',parent,8)['floor_support']=True
        cylinder('Display garment rail',(x-.58,y,1.83),(x+.58,y,1.83),.018,'Metal',parent,8)
        for j in range(7):
            xx=x-.48+j*.16
            cylinder('Display garment hanger',(xx,y,1.62),(xx,y,1.83),.003,'Metal',parent,6)
            mesh('Display hanging pressed shirt',[(xx-.14,y-.03,.68),(xx+.14,y-.03,.68),(xx+.17,y-.03,1.45),(xx+.065,y-.03,1.59),(xx-.065,y-.03,1.59),(xx-.17,y-.03,1.45)],[(0,1,2,3,4,5)],'White' if j%3 else 'Primary',parent,False)
    elif key=='laundry':
        for side in (-1,1):
            for j in range(4):quad('Washer cycle control','WashControl','sign',side*(w/2-.78),1.4+j*1.23-.45,1.30,.61,.16,parent,ink,layout)
    elif key=='phone':
        box('Window accessory stand',(w*.34,.90,.72),(.76,.34,1.12),'White',parent,0)['floor_support']=True
        for j in range(6):
            ob=box('Phone accessory package',(w*.34-.27+j*.105,.76,1.35),(.085,.035,.17),'White',parent,0);ob['product_index']=j
        quad('Window accessory display','Products','sign',w*.34,.718,1.03,.69,.58,parent,ink,layout)
    elif key=='mattress':
        quad('Floor model offer',key,'poster',-w*.13,.31,1.18,.61,.84,parent,ink,layout)
