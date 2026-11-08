"""Clipped garden-style crossed blades and clumped unmown lot margins."""
import math,random


def add(parent,plan,lib):
    from ground_edges import edges
    from terrain import sward_height
    from kit.botany import Cards
    from mathutils import Vector
    import bpy
    cards=Cards();old=plan['kind']=='old';paths=[]
    # The accepted garden copies this same original Ground alpha field.
    from textures import RECTS
    u0,v0,u1,v1=RECTS['Plain'];pad=3/2048
    for row in plan['lots']:
        p=row['home'];r=random.Random(p['occupant_seed']+8603);L,W=p['length'],p['width'];angle=math.radians(row['yaw']);cs,sn=math.cos(angle),math.sin(angle)
        def world(u,v):
            x=row['origin'][0]+cs*u-sn*v;y=row['origin'][1]+sn*u+cs*v
            return Vector((x,y,sward_height(x,y)-.003))
        def tuft(u,v,height=None):
            center=world(u,v);width=r.uniform(.003,.008);height=height or r.uniform(.018,.041);az=r.uniform(0,math.tau)
            for k in range(1):
                a=az;axis=Vector((math.cos(a),math.sin(a),0));bend=Vector((-axis.y,axis.x,0));grid=[]
                for t in (0,.5,1):
                    point=center+Vector((0,0,height*t))+bend*(r.uniform(.003,.016)*t*t)
                    grid.append([point+axis*(s*width*(1-.78*t)/2) for s in (-1,1)])
                cards.add_grid(grid,(u0+pad,v0+pad,u1-pad,v1-pad),(.02,.1,r.random(),0))
        # Mown street-end lawn; absent on pads and compacted approaches.
        for j in range(1700):
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
    from surfaces import palette
    material=palette()['Metal'].copy();material.name='ManufacturedPBR_Grass';material['tiling_vertex_tint']=True
    material.use_backface_culling=False
    ns,ls=material.node_tree.nodes,material.node_tree.links
    bs=next(n for n in ns if n.type=='BSDF_PRINCIPLED')
    # The shared grass cell has the garden's neutral normal, roughness and
    # linear albedo gains. It does not read unrelated Ground trim normals.
    image=next(n for n in ns if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
    # Each narrow blade has its own bent, tapered silhouette; no alpha tuft
    # shape repeats. Plain atlas paint supplies a neutral rough substrate.
    bs.inputs['Roughness'].default_value=.94
    ob=cards.mesh('Clumped clipped summer lawn blades',material);ob.parent=parent;ob['component']='summer_weeds'
    ob.data.uv_layers.active.name='UVMap'
    wind=ob.data.color_attributes.get('Wind')
    if wind:ob.data.color_attributes.remove(wind)
    tint=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');ob.data.color_attributes.active_color=tint
    ob.data.color_attributes.active_color_index=ob.data.color_attributes.find('Tint')
    ob.data.color_attributes.render_color_index=ob.data.color_attributes.find('Tint')
    for row,vertex in zip(tint.data,ob.data.vertices):
        x,y=vertex.co[:2];dry=max(0,(.5+.25*math.sin(x*.19+y*.12+plan['seed'])+.25*math.sin(x*.37-y*.24)-.76)/.24)
        gain=.84+.30*(.5+.5*math.sin(x*31.7+y*43.1))
        row.color=(.260*.56*(1+dry*.42)*gain/.89,.314*.76*(1-dry*.38)*gain/.89,.054*.80*(1-dry*.22)*gain/.89,1)
    ob['cause']='individually varied 18–41mm clipped blades matching the July base hue; taller shaded skirt margins'
    return ob
