"""Independent affine height-plane check, including mirrored/sheared UVs."""
import sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from suv_height_normal import derive


for mirrored in [False,True]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    me=bpy.data.meshes.new('Sheared plane');ps=[(0,0,0),(2,.4,0),(2.3,1.4,0),(.3,1,0)]
    me.from_pydata(ps,[],[(0,1,2),(0,2,3)]);me.update();ob=bpy.data.objects.new('Plane',me);bpy.context.collection.objects.link(ob)
    ob.rotation_euler=(.23,-.31,.47);bpy.context.view_layer.update()
    uv=me.uv_layers.new(name='BakeUV');coords=[(.1,.1),(.9,.1),(.9,.9),(.1,.9)]
    for li in range(len(me.loops)):
        u,v=coords[me.loops[li].vertex_index];uv.data[li].uv=(1-u if mirrored else u,v)
    size=128;y,x=np.mgrid[:size,:size];u=((1-x/size) if mirrored else x/size)-.1;v=1-y/size-.1;u/=.8;v/=.8
    height=.2*(2*u+.3*v)-.3*(.4*u+v)
    encoded,report=derive(ob,height.astype(np.float32),padding=2)
    tangent=Vector((-2,-.4,0) if mirrored else (2,.4,0)).normalized();bitangent=Vector((0,0,1)).cross(tangent)*(-1 if mirrored else 1)
    expected=Vector((-.2*.65,.3*.65,1)).normalized();sample=encoded[30:90,30:90].reshape(-1,3)*2-1
    world=np.array([tuple(tangent*n[0]+bitangent*n[1]+Vector((0,0,1))*n[2]) for n in sample])
    error=float(np.max(np.linalg.norm(world-np.array(tuple(expected)),axis=1)))
    assert error<1e-4,(mirrored,error)
    print('X220_HEIGHT_NORMAL_AFFINE',mirrored,error)
    valid=np.ones(height.shape,bool);valid[48:56,48:56]=False
    missing=height.astype(np.float32).copy();missing[~valid]=-.005
    encoded,_=derive(ob,missing,padding=2,sample_valid=valid)
    selected=valid[30:90,30:90];sample=(encoded[30:90,30:90]*2-1)[selected]
    world=np.array([tuple(tangent*n[0]+bitangent*n[1]+Vector((0,0,1))*n[2]) for n in sample])
    error=float(np.max(np.linalg.norm(world-np.array(tuple(expected)),axis=1)))
    assert error<1e-4,(mirrored,'Uncovered samples created a false slope',error)
    print('X220_HEIGHT_NORMAL_MISSING_SAMPLES',mirrored,error)
