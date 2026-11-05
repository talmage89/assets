"""Original open diamond lattice, recessed beds and molded corner blanks."""
import math
import bpy
from mathutils import Vector
from kit import model as G
from detail_helpers import box
from hatch_check import mesh_tree


def face_y(x,z):
    # A designed smooth bow independent of the coarse well's triangulation.
    return -2.164+.185*(x/.90)**2+.018*((z-.585)/.25)**2


def lattice(b,name,zcenter,width,height,columns,rows,bar,depth):
    vertices=[];faces=[]
    dx=width/columns;dz=height/rows
    for j in range(rows):
        for k in range(columns):
            x=-width/2+(k+.5)*dx;z=zcenter-height/2+(j+.5)*dz
            start=len(vertices)
            # Diamond rims share outer edges; their opaque black webs are
            # behind the bright beveled front, with actual open holes.
            for d,inset in [(0,-bar*.5),(0,bar),(depth,bar),(depth,-bar*.5)]:
                for xx,zz in [(x-dx/2+inset,z),(x,z-dz/2+inset),(x+dx/2-inset,z),(x,z+dz/2-inset)]:
                    vertices.append((xx,face_y(xx,zz)+.026+d,zz))
            for ring in ([0,1,2,3] if b.high else [0,1,3]):
                a=ring*4;c=((ring+1)%4)*4
                for i in range(4):faces.append(tuple(start+q for q in [a+i,a+(i+1)%4,c+(i+1)%4,c+i]))
    ob=G.mesh(name,vertices,faces,b.m['grille_bar']);G.smooth(ob,45);b.add(ob,category='trim')
    ob['open_cell_lattice']=True
    if not b.high:
        ob['allow_boundary']=True;ob['boundary_reason']='Back of molded web hidden against the recessed bed; front and both relief walls retained'


def build(b):
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith(('H120 grille swept vane','Low wide grille opening blade','Lower intake opening blade')):bpy.data.objects.remove(ob,do_unlink=True)
    for name,z,w,h in [('Low wide grille opening',.585,1.20,.210),('Lower intake opening',.300,1.20,.105)]:
        ob=bpy.data.objects[name];old=ob.data
        # Closed bowed backing is a dark cavity, with no invented relief bump.
        nu=12 if b.high else 6;ps=[]
        for d in [0,.003]:
            for zz in [z-h/2,z+h/2]:
                for i in range(nu+1):
                    x=-w/2+w*i/nu;ps.append((x,face_y(x,zz)+.070+d,zz))
        stride=nu+1;offset=2*stride;faces=[]
        for i in range(nu):
            faces.extend([(i,i+1,stride+i+1,stride+i),(offset+i,offset+stride+i,offset+stride+i+1,offset+i+1),
                          (i,offset+i,offset+i+1,i+1),(stride+i+1,offset+stride+i+1,offset+stride+i,stride+i)])
        faces.extend([(0,stride,offset+stride,offset),(nu,offset+nu,offset+stride+nu,stride+nu)])
        temp=G.mesh('H120 recessed cavity',ps,faces,b.m['grille']);G.smooth(temp,80)
        temp.data.transform(ob.matrix_world.inverted());ob.data=temp.data;bpy.data.objects.remove(temp,do_unlink=True)
        if old.users==0:bpy.data.meshes.remove(old)
        for prop in ['outer_skin_faces','lens_outer_faces']: 
            if prop in ob:del ob[prop]
    lattice(b,'H120 upper diamond grille',.585,1.17,.182,14,2,.0035,.012)
    lattice(b,'H120 lower diamond intake',.300,1.15,.078,20,1,.0025,.010)
    for side,sign in [('L',-1),('R',1)]:
        # Closed molded pocket insert, seated in the existing return. A
        # shallow horizontal blank is a real face, not an unbounded black hole.
        x=sign*.758;z=.427
        tree=mesh_tree([bpy.data.objects['Corner pocket '+side+' opening']])
        hit=tree.ray_cast(Vector((x,-3,z)),Vector((0,1,0)),3)[0]
        if hit is None:hit=tree.find_nearest(Vector((x,-2,z)))[0]
        x,z=hit.x,hit.z;y=hit.y-.007
        ob=box(b,'H120 fog pocket molded blank '+side,(x,y,z),(.078,.012,.065),b.m['bumper'],'trim',radius=.008)
        for j in [-1,1]:
            box(b,'H120 fog blank reveal '+side+str(j),(x,y-.007,z+j*.013),(.058,.003,.003),b.m['grille_bar'],'trim',radius=.001)
