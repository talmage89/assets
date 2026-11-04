"""Fit concealed construction to the accepted outer envelope.

Changes are measured again by the full solid sweeps, rather than exempting
panels, tires or glass from collisions. All coordinates below are metres.
"""
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def fit(b):
    door_trees={}
    for code in ['FL','FR','RL','RR']:
        skin=bpy.data.objects['Door '+code[0]+'_'+code[1]]
        door_trees[code]=BVHTree.FromPolygons([skin.matrix_world@v.co for v in skin.data.vertices],[tuple(f.vertices) for f in skin.data.polygons])
    for ob in list(bpy.context.scene.objects):
        if ob.type != 'MESH':
            continue
        inv = ob.matrix_world.inverted()
        if ob.get('part_category')=='interior' and ob.parent.name.startswith('Door_'):
            code=ob.parent.name[-2:];sign=-1 if code[-1]=='L' else 1;tree=door_trees[code]
            reference=max(abs((ob.matrix_world@v.co).x) for v in ob.data.vertices)
            inset=.022 if 'carrier' in ob.name else .035 if 'Door card' in ob.name else .055
            for vertex in ob.data.vertices:
                p=ob.matrix_world@vertex.co
                hit=tree.ray_cast(Vector((sign*2,p.y,p.z)),Vector((-sign,0,0)),3)[0]
                if hit is None:hit=tree.find_nearest(p)[0]
                p.x -= sign*max(0,reference-(abs(hit.x)-inset));vertex.co=inv@p
            ob['interior_skin_fit']='Conformed behind actual outer-door rays with preserved section depth'

        if ob.name.startswith('Wheelwell'):
            front = '_F' in ob.name
            for vertex in ob.data.vertices:
                p = ob.matrix_world @ vertex.co
                sign = -1 if p.x < 0 else 1
                if 'inboard' in ob.name:
                    p.x = sign * ((.47 if front else .56) + (abs(p.x)-.56))
                else:
                    p.x = sign * ((.73 if front else .75) if abs(p.x) > .7 else (.47 if front else .56))
                vertex.co = inv @ p
        if ob.name in ['Arch cladding_FL fender','Arch cladding_FR fender','Arch flange_FL fender','Arch flange_FR fender']:
            sign=-1 if '_FL' in ob.name else 1
            skin=bpy.data.objects['Front fender_'+('L' if sign<0 else 'R')]
            tree=BVHTree.FromPolygons([skin.matrix_world@v.co for v in skin.data.vertices],[tuple(f.vertices) for f in skin.data.polygons])
            for vertex in ob.data.vertices:
                p=ob.matrix_world@vertex.co
                if abs(p.y+.96525)<1e-5:
                    hit=tree.ray_cast(Vector((sign*2,p.y,p.z)),Vector((-sign,0,0)),3)[0]
                    if hit is None:hit=tree.find_nearest(p)[0]
                    stand=abs(p.x)-abs(hit.x);factor=max(0,min(1,(.014-stand)/.012))
                    p.y-=.006*factor;vertex.co=inv@p
            ob['joint_return_chamfer_m']=.006
        if ob.name.startswith('Taillamp') and 'optical cassette' in ob.name:
            gate = ' gate ' in ob.name
            sign = -1 if '-1' in ob.name else 1
            for vertex in ob.data.vertices:
                p = ob.matrix_world @ vertex.co
                p.x = sign * (min(abs(p.x), .7405) if gate else max(abs(p.x), .7495))
                vertex.co = inv @ p
        if ob.name.startswith('Arch hem_'):
            # The steel hem follows the closure segment that carries its cladding.
            from suv_joints import split_y
            code=ob.name.split('_')[-1];side=code[-1];end=code[0]
            front=bpy.data.objects['Door_F'+side];rear=bpy.data.objects['Door_R'+side]
            sections=[('fender',None,-.97525,b.root),('door',-.95775,None,front)] if end=='F' else [('door',None,1.25775,rear),('quarter',1.26225,None,b.root)]
            split_y(b,ob.name,sections)
            continue
        if ob.name.startswith('Quarter side glazing'):
            for vertex in ob.data.vertices:
                p=ob.matrix_world@vertex.co;p.x += -.004 if p.x>0 else .004;vertex.co=inv@p
        if ob.name.startswith('Washer nozzle'):
            world = ob.matrix_world.copy()
            ob.parent = bpy.data.objects['Hood']
            ob.matrix_world = world
    bpy.context.view_layer.update()
