"""Checkpoint surfaces reuse the car family's manufacturing and optical shaders."""
import bpy
from kit import vehicle_materials as V
from kit.materials import Nodes
import spec as S

def build(wear):
    axles=(S.FRONT_AXLE,S.REAR_AXLE)
    m={'yellow':V.paint('Bus yellow',(.79,.405,.009),wear,axles,front=-5.94,rear=6.006,metallic=0,flakes=0)}
    for key,c,kind in [('black',(.008,.009,.009),'rubber'),('frame',(.013,.014,.013),'steel'),
        ('aluminum',(.35,.37,.36),'alloy'),('wheel',(.29,.31,.30),'steel'),
        ('vinyl',(.043,.064,.050),'plastic'),('floor',(.015,.016,.015),'rubber'),
        ('ceiling',(.42,.43,.385),'plastic'),('dash',(.025,.029,.026),'plastic'),
        ('white',(.70,.72,.65),'plastic'),('red',(.40,.007,.005),'plastic')]:
        m[key]=V.manufactured('Bus '+key,c,kind,wear,axles,refined=True)
    m['glass']=V.glazing('Bus glass',(.81,.86,.80),axes=(1,2))
    m['windshield']=V.glazing('Bus windshield',(.86,.89,.84))
    m['lens']=V.glazing('Bus optical cover',(.96,.98,.97))
    m['reflector']=V.manufactured('Bus optical reflector',(.55,.57,.56),'chrome',0,refined=True)
    n=Nodes('Bus tape');a=n.node('ShaderNodeAttribute',attribute_name='VehicleRest');p=a.outputs['Vector'];_,y,z=n.split(p)
    phase=n.math('FRACT',n.math('DIVIDE',n.add(y,2.835),.470));black=n.math('GREATER_THAN',phase,.75)
    base=n.mix(black,(.64,.65,.59),(.009,.010,.009),True)
    edge=n.mul(n.ramp(z,1.024,1.011),wear,.10)
    m['tape']=n.finish(n.mix(edge,base,(.13,.12,.09),True),.55,0)
    m['mirror']=V.manufactured('Bus mirror',(.69,.72,.72),'chrome',0,refined=True)
    m['mirror'].node_tree.nodes['SURFACE'].inputs['Roughness'].default_value=.045
    m['tire']=V.tire('Bus tire',None,1,wear)
    # Reuse the car's radial tread field at a truck's physical envelope.
    nt=m['tire'].node_tree;tc=next(n for n in nt.nodes if n.type=='TEX_COORD')
    mul=nt.nodes.new('ShaderNodeVectorMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=(.275/S.TIRE_WIDTH,.40135/S.HUB,.40135/S.HUB)
    links=list(tc.outputs['Object'].links);nt.links.new(tc.outputs['Object'],mul.inputs[0])
    for link in links:nt.links.new(mul.outputs[0],link.to_socket)
    for key,col,power in [('amber',(.65,.13,.003),10),('warning_red',(.5,.004,.002),14),
                          ('headlight',(.85,.79,.60),5),('dome',(.72,.65,.45),2),('strobe',(.85,.90,1),20)]:
        m[key]=V.lamp('Bus '+key,col,power)
    # Rivet relief is a physical seam/rail pattern in meters, baked into the atlas.
    # It is not scattered noise and adds no delivery vertices.
    mat=m['yellow'];n=Nodes.__new__(Nodes);n.mat=mat;n.nt=mat.node_tree
    a=n.node('ShaderNodeAttribute',attribute_name='VehicleRest');p=a.outputs['Vector'];x,y,z=n.split(p)
    side=n.ramp(n.math('ABSOLUTE',x),1.18,1.208)
    sy=n.math('PINGPONG',n.add(y,-S.ROW_START+S.ROW_PITCH/2),S.ROW_PITCH/2)
    # PINGPONG repeats at the full bay pitch. Z rows are at a 75mm fastener pitch.
    sz=n.math('PINGPONG',z,.0375)
    radial=n.add(n.mul(sy,sy),n.mul(sz,sz))
    rivet=n.mul(side,n.ramp(z,1.79,1.77),n.ramp(z,.765,.800),n.ramp(radial,.006**2,.003**2))
    roof=n.ramp(z,2.68,2.75);ry=n.math('PINGPONG',n.add(y,3.38),.632)
    lap=n.mul(roof,n.ramp(ry,.005,.0015))
    rx=n.math('PINGPONG',x,.05);roof_rivets=n.mul(roof,n.ramp(n.add(n.mul(ry,ry),n.mul(rx,rx)),.006**2,.003**2))
    h=n.nt.nodes['OUT_height'];old=h.inputs[0].links[0].from_socket;n.feed(h.inputs[0],n.add(old,n.mul(rivet,.0012),n.mul(lap,.0007),n.mul(roof_rivets,.0012)))
    # Two real fastener rows on each pressed black rail. The spatial gate
    # excludes black seals, brackets and underbody fittings sharing this shader.
    rail=Nodes.__new__(Nodes);rail.mat=m['black'];rail.nt=rail.mat.node_tree
    rp=rail.node('ShaderNodeAttribute',attribute_name='VehicleRest').outputs['Vector'];xx,yy,zz=rail.split(rp)
    rows=[];dy=rail.math('PINGPONG',yy,.075)
    for center in [.795,1.222,1.624,1.778]:
        for dz in [-.032,.032]:
            zdist=rail.math('SUBTRACT',zz,center+dz)
            rows.append(rail.ramp(rail.add(rail.mul(dy,dy),rail.mul(zdist,zdist)),.006**2,.003**2))
    gate=rail.mul(rail.ramp(rail.math('ABSOLUTE',xx),1.219,1.226),rail.ramp(rail.math('ABSOLUTE',xx),1.253,1.250))
    h=rail.nt.nodes['OUT_height'];old=h.inputs[0].links[0].from_socket
    rail.feed(h.inputs[0],rail.add(old,rail.mul(gate,rail.maximum(*rows),.0010)))
    # Sparse skirt corrosion belongs to the wet lower sheet edge; preliminary only.
    rust=n.mul(side,n.ramp(z,.870,.770),n.ramp(n.noise(n.vec('MULTIPLY',p,(1,2,5)),47,2),.61,.77),wear)
    base=n.nt.nodes['OUT_base'];old=base.inputs[0].links[0].from_socket;n.feed(base.inputs[0],n.mix(rust,old,(.13,.048,.012),True))
    return m

def printed(name,image):
    n=Nodes('Bus print '+name);tex=n.node('ShaderNodeTexImage');tex.image=image
    return n.finish(tex.outputs['Color'],.48,0)
