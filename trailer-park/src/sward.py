"""Clipped garden-style crossed blades and clumped unmown lot margins."""
import math,random


def add(parent,plan,lib):
    from ground_edges import edges,modules
    from terrain import sward_height
    from kit.botany import Cards
    from mathutils import Vector
    import bpy
    base,additions=modules();cards=Cards();old=plan['kind']=='old';paths=[]
    # The accepted garden copies this same original Ground alpha field.
    u0,v0,u1,v1=additions.RECTS['grass'];cw=(u1-u0)/4;ch=(v1-v0)/2;pad=2/2048
    for row in plan['lots']:
        p=row['home'];r=random.Random(p['occupant_seed']+8603);L,W=p['length'],p['width'];angle=math.radians(row['yaw']);cs,sn=math.cos(angle),math.sin(angle)
        def world(u,v):
            x=row['origin'][0]+cs*u-sn*v;y=row['origin'][1]+sn*u+cs*v
            return Vector((x,y,sward_height(x,y)-.003))
        def tuft(u,v,height=None):
            center=world(u,v);width=r.uniform(.14,.23);height=height or r.uniform(.024,.045);az=r.uniform(0,math.tau)
            for k in range(2):
                a=az+k*1.15;axis=Vector((math.cos(a),math.sin(a),0));bend=Vector((-axis.y,axis.x,0));grid=[]
                for t in (0,.5,1):
                    point=center+Vector((0,0,height*t))+bend*(.012*t*t)
                    grid.append([point+axis*(s*width/2) for s in (-1,1)])
                cell=r.randrange(2);band=r.randrange(2)
                cards.add_grid(grid,(u0+cell*cw+pad,v0+band*ch+pad,u0+(cell+1)*cw-pad,v0+(band+1)*ch-pad),(.02,.1,r.random(),0))
        # Mown street-end lawn; absent on pads and compacted approaches.
        for j in range(640):
            u=r.uniform(L/2+.15,L/2+5.35)
            if j%2:
                if old and row['number']==1:continue
                v=r.uniform(-plan['lot_frontage']/2-(1.4 if old else 1.15)+.15,-2.65)
                wy=-W/2-3.0;walk_end=L/2+1.2
                if abs(v-wy)<.46 and u<walk_end+.46:continue
                if abs(u-walk_end)<.46 and wy-.46<v<-2.55:continue
                if p['carport'] and u<L/2+.65 and -W/2-3.65<v<-W/2:continue
            else:v=r.uniform(.55,plan['lot_frontage']/2-1.6)
            clump=.5+.5*math.sin(u*4.1+v*2.7+p['seed'])*math.sin(v*3.7-u*.8)
            if r.random()>.40+.55*clump:continue
            if p['upkeep']!='kept' and abs(u-L/2-2.2)<1 and abs(v-1.2)<.6:continue
            tuft(u,v)
        if not (old and row['number']==1):
            for j in range(round(L*11)):
                u=r.uniform(-L/2+.1,L/2-.1);v=-W/2-r.uniform(3.57,3.95)
                if abs(u+L*.035)<p['deck_width']/2 and v>-W/2-3.8:continue
                tuft(u,v)
            # Mower cannot reach the wall; taller bunches stay rooted here.
            for j in range(round(L*6)):
                u=r.uniform(-L/2+.1,L/2-.1);v=-W/2-r.uniform(.03,.18)
                if abs(u+L*.035)<p['deck_width']/2+.1 or abs(u-(L/2-2.9))<3.45 and p['carport']:continue
                if r.random()<.45:tuft(u,v,r.uniform(.08,.18))
        for j in range(12):
            u=L/2+r.uniform(.1,5.3);v=r.choice((.48,plan['lot_frontage']/2-1.6));point=world(u,v)
            paths.append([point,point+Vector((.12,.05,0))])
    fringe=edges(parent,paths,plan['seed']+9713,lib);fringe['component']='summer_weeds'
    material=fringe.data.materials[0].copy();material.name='ManufacturedGrassBlades';material['tiling_vertex_tint']=True
    ns,ls=material.node_tree.nodes,material.node_tree.links
    bs=next(n for n in ns if n.type=='BSDF_PRINCIPLED');original=bs.inputs['Base Color'].links[0].from_socket
    # Garden's copied tufts use neutral normals and a very rough leaf field;
    # the Ground trim normal must not turn fine mown blades into hard lumps.
    for link in list(bs.inputs['Normal'].links):ls.remove(link)
    for link in list(bs.inputs['Roughness'].links):ls.remove(link)
    bs.inputs['Roughness'].default_value=.94
    tint_node=ns.new('ShaderNodeVertexColor');tint_node.layer_name='Tint'
    multiply=ns.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1
    ls.new(original,multiply.inputs[1]);ls.new(tint_node.outputs['Color'],multiply.inputs[2]);ls.new(multiply.outputs[0],bs.inputs['Base Color'])
    ob=cards.mesh('Clumped clipped summer lawn blades',material);ob.parent=parent;ob['component']='summer_weeds'
    ob.data.uv_layers.active.name='UVMap'
    wind=ob.data.color_attributes.get('Wind')
    if wind:ob.data.color_attributes.remove(wind)
    tint=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');ob.data.color_attributes.active_color=tint
    for row,vertex in zip(tint.data,ob.data.vertices):
        x,y=vertex.co[:2];dry=.5+.5*math.sin(x*.37-y*.24)
        row.color=(.96,1-dry*.32,.60-dry*.20,1)
    ob['cause']='garden July method; 27–52mm clipped blades, 80–180mm shaded skirt margins'
    return ob
