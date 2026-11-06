"""Fictional lettering quads select the single family atlas."""
from kit import model as G


def label(name,text,position,w,h,surface=None):
    from construction import M
    x,y,z=position
    if name=='Number tag':
        from atlas import point
        import re
        digits=re.search(r'\d{4}',text).group(0)
        glyphs='RV0123456789';vs=[];faces=[];coords=[]
        # Six glyph quads share one atlas/material and retain each pole's ID.
        # Their physical letter aspect is authored here, independent of the
        # atlas rectangle's otherwise anisotropic pixel allocation.
        placements=[('R',x-.012,z+h*.39),('V',x+.012,z+h*.39)]
        placements += [(char,x,z+h*(.17-i*.20)) for i,char in enumerate(digits)]
        for char,xx,zz in placements:
            cw=w*.36;ch=h*.16;k=len(vs)
            vs += [(xx-cw/2,y,zz-ch/2),(xx+cw/2,y,zz-ch/2),(xx+cw/2,y,zz+ch/2),(xx-cw/2,y,zz+ch/2)]
            faces.append((k,k+1,k+2,k+3));index=glyphs.index(char)
            coords.extend(point('Tag',(index+u)/len(glyphs),v) for u,v in ((0,0),(1,0),(1,1),(0,1)))
        ob=G.mesh(name,vs,faces,M['Polymer']);uv=ob.data.uv_layers.new(name='UVMap')
        for poly in ob.data.polygons:
            for li in poly.loop_indices:uv.data[li].uv=coords[ob.data.loops[li].vertex_index]
        ob['atlas_role']='Tag';ob['authored_tag_uv']=True;return ob
    if surface:
        import math
        cx,cy,radius,sides=surface;r=radius(z)
        xs=sorted({-w/2,0,w/2,*[round(r*math.cos(t*math.tau/sides),9) for t in range(sides)
            if math.sin(t*math.tau/sides)<0 and abs(r*math.cos(t*math.tau/sides))<w/2]})
        vs=[]
        for zz in (z-h/2,z+h/2):
            rr=radius(zz);ring=[(rr*math.cos(k*math.tau/sides),rr*math.sin(k*math.tau/sides)) for k in range(sides)]
            for xx in xs:
                hits=[]
                for a,b in zip(ring,ring[1:]+ring[:1]):
                    if min(a[0],b[0])-1e-9<=xx<=max(a[0],b[0])+1e-9 and abs(b[0]-a[0])>1e-9:
                        hits.append(a[1]+(b[1]-a[1])*(xx-a[0])/(b[0]-a[0]))
                vs.append((cx+xx,cy+min(hits)-.0004,zz))
        n=len(xs);faces=[(i,i+1,n+i+1,n+i) for i in range(n-1)]
    else:
        vs=[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)];faces=[(0,1,2,3)]
    ob=G.mesh(name,vs,faces,M['Polymer'])
    ob['atlas_role']='Brand' if name=='Birth brand' else 'Rating'
    return ob
