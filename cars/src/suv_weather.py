"""SUV-specific causal wear layered over the family's neutral-factor method."""
import math,bpy
from mathutils import Vector
from mathutils.kdtree import KDTree
from kit.materials import Nodes
from kit import vehicle_materials as V
import suv_spec as S


def graph(mat):
    n=Nodes.__new__(Nodes);n.mat=mat;n.nt=mat.node_tree
    return n


def previous(n,name):
    node=n.nt.nodes['OUT_'+name]
    return node.inputs[0].links[0].from_socket


def replace(n,name,value,socket=None):
    destinations=[n.nt.nodes['OUT_'+name].inputs[0]]
    if socket:destinations.append(n.nt.nodes['SURFACE'].inputs[socket])
    for destination in destinations:
        supplied=value
        if not hasattr(value,'is_output'):
            for link in list(destination.links):n.nt.links.remove(link)
            if isinstance(value,tuple) and len(value)==3 and destination.type=='RGBA':supplied=(*value,1)
        n.feed(destination,supplied)


def paint(mat,wear):
    n=graph(mat);p,x,y,z,nx,ny,nz=V.rest(n,'VehicleRest')
    originals={k:previous(n,k) for k in ['base','rough','height','paint_coverage','paint_contamination']}
    # Extra SUV road load remains in tire wakes, not a noisy full-body wash.
    film=V.daily_road_mask(n,p,y,z,(S.FRONT_AXLE,S.REAR_AXLE),wear*.75)
    distance=n.node('ShaderNodeAttribute',attribute_name='WearEdgeDistance').outputs['Fac']
    gaps=n.mul(n.ramp(distance,.008,.0015),wear,.42)
    edges=n.maximum(*[n.band(y,seam,.003,.002) for seam in [S.DOOR_FRONT,S.DOOR_SPLIT,S.DOOR_REAR]])
    door=n.mul(edges,n.ramp(n.math('ABSOLUTE',x),.78,.87),n.ramp(z,1.25,1.13),n.ramp(z,.30,.40))
    hood=n.mul(n.ramp(y,-1.99,-2.17),n.ramp(z,.86,.94),n.maximum(n.ramp(ny,-.1,-.75),n.mul(n.ramp(nz,.3,.9),.7)))
    chip=n.mul(n.maximum(door,hood),wear,n.ramp(n.noise(p,740,2),.77,.87))
    deposit=n.maximum(film,gaps)
    base=n.mix(deposit,originals['base'],(.055,.047,.036),True)
    base=n.mix(chip,base,(.16,.17,.17),True)
    contamination=n.mix(deposit,originals['paint_contamination'],(.055,.047,.036),True)
    contamination=n.mix(chip,contamination,(.16,.17,.17),True)
    coverage=n.mul(originals['paint_coverage'],n.math('SUBTRACT',1,deposit),n.math('SUBTRACT',1,chip))
    replace(n,'base',base,'Base Color');replace(n,'paint_coverage',coverage);replace(n,'paint_contamination',contamination)
    rough=n.add(originals['rough'],n.mul(deposit,.15),n.mul(chip,.22));replace(n,'rough',rough,'Roughness')
    replace(n,'height',n.add(originals['height'],n.mul(chip,-.00009)))
    bs=n.nt.nodes['SURFACE'];old=bs.inputs['Coat Weight'].links[0].from_socket
    n.feed(bs.inputs['Coat Weight'],n.mul(old,n.math('SUBTRACT',1,n.mul(n.maximum(deposit,chip),.8))))
    old=bs.inputs['Coat Roughness'].links[0].from_socket
    swirls=n.mul(n.ramp(n.math('SINE',n.mul(n.voronoi(p,8),3200)),.92,.99),n.ramp(n.noise(p,30,2),.57,.70),wear,.013)
    n.feed(bs.inputs['Coat Roughness'],n.add(old,n.mul(deposit,.18),swirls))
    n.channel('suv_road_film',film);n.channel('gap_grime',gaps);n.channel('suv_chips',chip)


def glass(mat,wear):
    n=graph(mat);tc=n.node('ShaderNodeTexCoord');x,y,z=n.split(tc.outputs['Generated'])
    # Sediment is confined to the bottom edge, partly on the printed frit.
    dirt=n.mul(n.ramp(z,.075,.015),n.ramp(n.noise(tc.outputs['Generated'],220,2),.3,.7),wear,.10)
    replace(n,'base',n.mix(dirt,previous(n,'base'),(.045,.036,.024),True),'Base Color')
    replace(n,'rough',n.add(previous(n,'rough'),n.mul(dirt,.08)),'Roughness')
    bs=n.nt.nodes['SURFACE'];old=bs.inputs['Transmission Weight'].links[0].from_socket
    n.feed(bs.inputs['Transmission Weight'],n.mul(old,n.math('SUBTRACT',1,n.mul(dirt,.2))))
    n.channel('lower_edge_sediment',dirt)


def alloy(mat,wear):
    """Machined faces over darker cast pockets, with radial brake deposits."""
    n=graph(mat);p,x,y,z,nx,ny,nz=V.rest(n,'VehicleRest')
    face=n.ramp(n.math('ABSOLUTE',nx),.38,.85);dust=[];turns=[]
    for axle in [S.FRONT_AXLE,S.REAR_AXLE]:
        r=n.math('SQRT',n.add(n.mul(n.math('SUBTRACT',y,axle),n.math('SUBTRACT',y,axle)),n.mul(n.math('SUBTRACT',z,S.HUB_HEIGHT),n.math('SUBTRACT',z,S.HUB_HEIGHT))))
        radial=n.mul(n.ramp(r,.065,.105),n.ramp(r,.225,.195))
        dust.append(n.mul(radial,n.band(y,axle,.23,.02)))
        turns.append(n.mul(n.band(y,axle,.23,.02),n.math('SINE',n.mul(r,math.tau/.0006))))
    deposit=n.mul(n.maximum(*dust),wear,n.mix(face,.55,.18),n.add(.75,n.mul(n.noise(p,190,2),.25)))
    base=n.mix(face,(.055,.064,.071),previous(n,'base'),True)
    replace(n,'base',n.mix(deposit,base,(.023,.019,.016),True),'Base Color')
    replace(n,'rough',n.add(n.mix(face,.38,.24),n.mul(deposit,.20),n.mul(n.maximum(*turns),face,.012)),'Roughness')
    replace(n,'height',n.mul(n.maximum(*turns),face,.4e-6))
    bs=n.nt.nodes['SURFACE'];bs.inputs['Coat Weight'].default_value=.35;bs.inputs['Coat Roughness'].default_value=.16
    n.channel('suv_brake_dust',deposit);n.channel('machined_face',face)


def edge_attributes():
    """Measure distance to actual exposed skin borders; no image inputs."""
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not any(m.get('vehicle_paint') for m in ob.data.materials):continue
        me=ob.data;role=me.attributes.get('skin_face_role');edges={}
        for face in me.polygons:
            if role and role.data[face.index].value!=0:continue
            for a,c in zip(face.vertices,tuple(face.vertices[1:])+tuple(face.vertices[:1])):
                e=tuple(sorted((a,c)));edges[e]=edges.get(e,0)+1
        samples=[]
        for (a,c),count in edges.items():
            if count!=1:continue
            a=ob.matrix_world@me.vertices[a].co;c=ob.matrix_world@me.vertices[c].co
            steps=max(1,math.ceil((c-a).length/.004))
            samples.extend(a.lerp(c,i/steps) for i in range(steps+1))
        attr=me.attributes.get('WearEdgeDistance') or me.attributes.new('WearEdgeDistance','FLOAT','POINT')
        if samples:
            tree=KDTree(len(samples))
            for i,p in enumerate(samples):tree.insert(p,i)
            tree.balance()
            for v,d in zip(me.vertices,attr.data):d.value=tree.find(ob.matrix_world@v.co)[2]
        else:
            for d in attr.data:d.value=.1


def cladding_fasteners(mat):
    """Original push-rivet head relief on the actual inner arch flanges."""
    from suv_exterior import tree_for
    n=graph(mat);p,x,y,z,nx,ny,nz=V.rest(n,'VehicleRest');heads=[];recess=[]
    for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
        for side,sign in [('L',-1),('R',1)]:
            obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Arch flange_'+end+side)]
            tree=tree_for(obs)
            for dy in [-.35,.35]:
                point=tree.find_nearest(Vector((sign*.86,axle+dy,.56)))[0]
                distance=n.vec('DISTANCE',p,tuple(point))
                heads.append(n.ramp(distance,.0046,.0037));recess.append(n.ramp(distance,.0018,.0011))
    head=n.maximum(*heads);cut=n.maximum(*recess)
    replace(n,'height',n.add(previous(n,'height'),n.mul(head,.00075),n.mul(cut,-.00035)))
    replace(n,'base',n.mix(head,previous(n,'base'),(.022,.024,.024),True),'Base Color')
    n.channel('push_rivet_relief',head)


def freeze_exposure_normals():
    """Keep exposure/chip masks attached while the canted doors open.

    Surface shading still uses the live mesh normals. Only the manufacturing
    graphs' geometric-normal queries use this rest-frame corner attribute.
    """
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        matrix=ob.matrix_world.to_3x3().inverted().transposed();me=ob.data
        attr=me.attributes.get('VehicleRestNormal') or me.attributes.new('VehicleRestNormal','FLOAT_VECTOR','CORNER')
        for d,norm in zip(attr.data,me.corner_normals):d.vector=(matrix@norm.vector).normalized()
    for mat in bpy.data.materials:
        if not mat.use_nodes:continue
        nt=mat.node_tree;destinations=[link.to_socket for node in nt.nodes if node.type=='NEW_GEOMETRY' for link in list(node.outputs['Normal'].links)]
        if not destinations:continue
        attr=nt.nodes.new('ShaderNodeAttribute');attr.attribute_name='VehicleRestNormal'
        normal=nt.nodes.new('ShaderNodeVectorMath');normal.operation='NORMALIZE';nt.links.new(attr.outputs['Vector'],normal.inputs[0])
        for destination in destinations:nt.links.new(normal.outputs[0],destination)
