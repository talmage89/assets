"""Render context beyond the delivered parcel; school/campus stay independent."""
import math
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
from siteworks import place,clear_templates,ROOT


def context(p):
    rt=bpy.data.objects.new('Presentation neighborhood / excluded from campus',None);bpy.context.collection.objects.link(rt)
    rt.rotation_euler.z=math.radians(p['site_yaw'])
    from geometry import Assembly
    from siteworks import rectangle,ground_finish
    land=Assembly('Neighborhood_ground');land.root.parent=rt
    for rect in [(-700,-105,-700,700),(105,700,-700,700),(-105,105,-700,-92),(-105,105,92,700)]:
        m=land.mesh('Neighboring_lawn',solid=False);rectangle(m,rect,-.01,'Siding');ground_finish(m.finish(),'Siding')
    for row in p['streets']:
        horizontal=row['axis']=='X';at=row['at']
        for i in range(-37,38):
            v=i*6.096
            if abs(v)<110:continue
            place('build/context/ground.glb','Continuing_public_street',(v,at,.01165) if horizontal else (at,v,.01165),90 if horizontal else 0,'Road_Straight_A',rt)
    # Neighboring houses are the library's unchanged construction, placed as
    # repeated blocks outside the school grounds as in the skatepark pipeline.
    styles=['houses.glb','houses-ranch.glb','houses-cape.glb']
    def house(label,j,point,yaw):
        style=styles[(p['seed']+j*7+len(label))%3]
        place(Path('build/context')/style,label+str(j),point,yaw,parent=rt)
    for j in range(-5,6):
        house('Across_street_house_',j,(j*25,-123-(j%3)*1.6,-.03),180)
    for j in range(-3,4):
        house('Side_street_house_',j,(-133-(j%2)*2,j*28,-.03),90)
        house('East_neighbor_',j,(138+(j%2)*2,j*28,-.03),-90)
        if p['parcel']!='backing onto a city park':house('Rear_neighbor_',j,(j*29,117+(j%3)*1.6,-.03),0)
    street_rows=[('Y',-115)]
    if not any(row['axis']=='Y' for row in p['streets']):street_rows.append(('Y',115))
    if p['parcel']!='backing onto a city park':street_rows.append(('X',99))
    for axis,at in street_rows:
        for i in range(-32,33):
            v=i*6.096;horizontal=axis=='X'
            place('build/context/ground.glb','Neighborhood_cross_street',(v,at,.01165) if horizontal else (at,v,.01165),90 if horizontal else 0,'Road_Straight_A',rt)
            for sign in (-1,1):
                for half in (-1.524,1.524):
                    q=(v+half,at+sign*4.12,.01165) if horizontal else (at+sign*4.12,v+half,.01165)
                    place('build/context/ground.glb','Neighborhood_curb',q,90 if horizontal else 0,'Curb_Straight',rt)
                for half in (-2.286,-.762,.762,2.286):
                    q=(v+half,at+sign*6.1,.01165) if horizontal else (at+sign*6.1,v+half,.01165)
                    place('build/context/ground.glb','Neighborhood_sidewalk',q,90 if horizontal else 0,'Sidewalk_A',rt)
    for j in range(12):
        place(ROOT/'trees/export'/('RedMaple.glb' if j%3 else 'PinOak.glb'),'Neighborhood_tree_'+str(j),(-135+j*24,-111+(j%2)*6,0),j*69,parent=rt)
    for j,(x,y) in enumerate(p['trees'][5:]):place(ROOT/'trees/export'/('RedMaple.glb' if j%2 else 'PinOak.glb'),'Neighbor_boundary_tree_'+str(j),(-116 if x<0 else 116,y,0),j*71,parent=rt)
    for j in range(10):place(ROOT/'trees/export'/('RedMaple.glb' if j%2 else 'PinOak.glb'),'Distant_east_tree_'+str(j),(160,-120+j*27,0),j*51,parent=rt)
    if p['parcel']=='backing onto a city park':
        for j in range(16):place(ROOT/'trees/export'/('RedMaple.glb' if j%2 else 'PinOak.glb'),'Park_tree_'+str(j),(-115+j*15,111+(j%3)*12,0),j*47,parent=rt)
    poles=[place('build/context/utility.glb','Neighborhood_pole_'+str(j),(j*40,-101,0),90,'Tangent',rt) for j in range(-3,4)]
    from kit.model import tube
    wire=bpy.data.materials.new('Native conductor / presentation');wire.use_nodes=True;wire.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.009,.010,.008,1)
    bpy.context.view_layer.update();inverse=rt.matrix_world.inverted()
    for left,right in zip(poles,poles[1:]):
        def pins(root):return sorted([o for o in root.children_recursive if '__Socket_Primary_' in o.name],key=lambda o:o.name)
        for pa,pb in zip(pins(left),pins(right)):
            start=inverse@pa.matrix_world.translation;end=inverse@pb.matrix_world.translation
            pts=[tuple(start.lerp(end,t)-Vector((0,0,1.15*4*t*(1-t)))) for t in [i/24 for i in range(25)]]
            ob=tube('Neighborhood conductor on native pin sockets',pts,float(pa.get('diameter_m',.0101))/2,wire,4);ob.parent=rt
    # The library car source is used intact for presentation: no further
    # body LOD, reshaping or period conversion is performed for this round.
    path=Path('build/context/car.blend').resolve()
    with bpy.data.libraries.load(str(path),link=False) as (src,dst):dst.objects=list(src.objects)
    obs=[ob for ob in dst.objects if ob]
    for ob in obs:bpy.context.collection.objects.link(ob)
    roots=[o for o in obs if o.parent not in obs]
    ex,ey=p['entry'];base=roots[0] if len(roots)==1 else bpy.data.objects.new('Native car',None)
    if len(roots)>1:
        bpy.context.collection.objects.link(base)
        for ob in roots:ob.parent=base
    placements={'finger':[((-56,-28),127),((-49,-15),180)],'courtyard':[((52,-20),32),((62,-36),29)],'compact':[((-54,-54),168),((-49,-26),195)]}[p['type']]
    base.parent=rt;base.location=(*placements[0][0],.018);base.rotation_euler.z=math.radians(placements[0][1])
    # A second intact instance waits on the parent route; source material
    # colors remain the library's. Its manufacturing period is lead-owned.
    copies={o:o.copy() for o in [base,*base.children_recursive]}
    for ob,cp in copies.items():
        bpy.context.collection.objects.link(cp);cp.parent=copies.get(ob.parent,rt)
        cp.matrix_basis=ob.matrix_basis.copy()
    q,yaw=placements[1];copies[base].location=(*q,.018);copies[base].rotation_euler.z=math.radians(yaw)
    clear_templates();bpy.context.view_layer.update()
    def triangles(objects):
        count=0
        for ob in objects:
            if ob.type=='MESH':ob.data.calc_loop_triangles();count+=len(ob.data.loop_triangles)
        return count
    rt['placed_presentation_triangles']=triangles(rt.children_recursive)
    rt['two_native_cars_triangles']=triangles([base,*base.children_recursive,copies[base],*copies[base].children_recursive])
    return rt
