"""Geometric mean curvature on actual triangles, independent of shading normals.

Cotangent Laplace--Beltrami with mixed Voronoi areas, Meyer et al., section 3.5:
https://geometry.caltech.edu/pubs/DMSB_III.pdf . H=(k1+k2)/2; convex is positive.
Adapted from the original family diagnostic in 85d7450; no fit, smoothing or
parent substitution is applied to the game measurements.
Open exterior boundaries are gray, not a false curvature.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]


def mean_curvature(points,triangles):
    p=np.asarray(points,dtype=float);t=np.asarray(triangles,dtype=int)
    xyz=p[t];e1=xyz[:,1]-xyz[:,0];e2=xyz[:,2]-xyz[:,0]
    cross=np.cross(e1,e2);double=np.linalg.norm(cross,axis=1)
    good=double>1e-14;t=t[good];xyz=xyz[good];cross=cross[good];double=double[good]
    cot=[]
    for i in range(3):
        a=xyz[:,(i+1)%3]-xyz[:,i];b=xyz[:,(i+2)%3]-xyz[:,i]
        cot.append(np.einsum('ij,ij->i',a,b)/double)
    cot=np.asarray(cot).T;area=np.zeros(len(p));normal=np.zeros_like(p);lap=np.zeros_like(p)
    obtuse=np.any(cot<0,axis=1)
    for i in range(3):
        j,k=(i+1)%3,(i+2)%3
        a=np.sum((xyz[:,j]-xyz[:,i])**2,axis=1);b=np.sum((xyz[:,k]-xyz[:,i])**2,axis=1)
        mixed=(a*cot[:,k]+b*cot[:,j])/8
        mixed=np.where(obtuse,np.where(cot[:,i]<0,double/4,double/8),mixed)
        np.add.at(area,t[:,i],mixed);np.add.at(normal,t[:,i],cross)
        np.add.at(lap,t[:,i],cot[:,k,None]*(xyz[:,i]-xyz[:,j])+cot[:,j,None]*(xyz[:,i]-xyz[:,k]))
    normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-20)
    h=np.einsum('ij,ij->i',lap,normal)/np.maximum(4*area,1e-20)
    edges=np.sort(np.concatenate([t[:,[0,1]],t[:,[1,2]],t[:,[2,0]]]),axis=1)
    unique,count=np.unique(edges,axis=0,return_counts=True);border=set(unique[count!=2].ravel().tolist())
    valid=area>1e-12
    if border:valid[list(border)]=False
    return h,valid,area,normal


def selected_triangles(ob,parent=False):
    ob.data.calc_loop_triangles();result=[]
    normal_matrix=ob.matrix_world.to_3x3().inverted().transposed()
    all_faces=parent or ob.name.startswith(('Mirror housing','Liftgate spoiler'))
    for tri in ob.data.loop_triangles:
        f=ob.data.polygons[tri.polygon_index];c=ob.matrix_world@f.center
        if not all_faces:
            role=ob.data.attributes.get('sheet_role')
            if role is not None:
                if role.data[f.index].value!=0:continue
                result.append(tuple(tri.vertices));continue
            radial=c-Vector((0,max(-1.4,min(1.4,c.y)),.65))
            if (normal_matrix@f.normal).dot(radial)<=0:continue
        result.append(tuple(tri.vertices))
    return result


def color(h):
    # Nonlinear but explicitly calibrated scale gives shallow broad defects and
    # sharp design lines equal visibility; no per-part automatic normalization.
    stops=[(-20,(.10,.05,.45)),(-5,(.05,.28,.9)),(-1,(.12,.75,.85)),
           (0,(.48,.72,.45)),(1,(.90,.82,.16)),(5,(.98,.25,.035)),(20,(.5,.025,.02))]
    if h<=stops[0][0]:return (*stops[0][1],1)
    for (a,ca),(b,cb) in zip(stops,stops[1:]):
        if h<=b:
            w=(h-a)/(b-a);return (*(x+(y-x)*w for x,y in zip(ca,cb)),1)
    return (*stops[-1][1],1)


def material():
    m=bpy.data.materials.new('Measured geometric mean curvature');m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
    attr=n.new('ShaderNodeVertexColor');attr.layer_name='Geometric mean curvature';em=n.new('ShaderNodeEmission');l.new(attr.outputs['Color'],em.inputs['Color']);out=n.new('ShaderNodeOutputMaterial');l.new(em.outputs[0],out.inputs[0]);return m


def apply(obs,parent=False):
    mat=material();report={}
    for ob in obs:
        ps=[tuple(ob.matrix_world@v.co) for v in ob.data.vertices];ts=selected_triangles(ob,parent)
        if not ts:continue
        h,valid,areas,normals=mean_curvature(ps,ts)
        layer=ob.data.color_attributes.get('Geometric mean curvature') or ob.data.color_attributes.new(name='Geometric mean curvature',type='FLOAT_COLOR',domain='CORNER')
        outer={tuple(sorted(t)) for t in ts};ob.data.calc_loop_triangles()
        included={t.polygon_index for t in ob.data.loop_triangles if tuple(sorted(t.vertices)) in outer}
        for f in ob.data.polygons:
            for li in f.loop_indices:
                vi=ob.data.loops[li].vertex_index
                layer.data[li].color=color(h[vi]) if valid[vi] and f.index in included else (.17,.17,.17,1)
        ob.data.materials.clear();ob.data.materials.append(mat)
        for f in ob.data.polygons:f.material_index=0
        vals=h[valid];report[ob.name]=dict(vertices=len(ps),triangles=len(ts),valid_vertices=int(valid.sum()),
            H_m_inv_percentiles=np.percentile(vals,[0,1,5,50,95,99,100]).tolist() if len(vals) else [],
            points=ps,mean_curvature_m_inv=h.tolist(),valid=valid.tolist())
    return report


def self_test():
    # Analytic sphere and cylinder, with deliberately triangulated curved quads.
    tests={}
    for kind in ['sphere','cylinder','plane']:
        ps=[];ts=[];nu=128;nv=64
        for j in range(nv+1):
            for i in range(nu):
                u=math.tau*i/nu;v=(j/nv-.5)*1.8
                if kind=='sphere':ps.append((2*math.cos(v)*math.cos(u),2*math.cos(v)*math.sin(u),2*math.sin(v)))
                elif kind=='cylinder':ps.append((2*math.cos(u),2*math.sin(u),v))
                else:ps.append((i/nu,j/nv,0))
        for j in range(nv):
            for i in range(nu if kind!='plane' else nu-1):
                a=j*nu+i;b=j*nu+(i+1)%nu;c=b+nu;d=a+nu;ts.extend([(a,b,c),(a,c,d)])
        h,valid,*_=mean_curvature(ps,ts);expected={'sphere':.5,'cylinder':.25,'plane':0}[kind]
        error=float(np.max(np.abs(h[valid]-expected)));tests[kind]=dict(expected_m_inv=expected,maximum_error=error)
        assert error<.003,(kind,error)
    print('CURVATURE_ANALYTIC_TEST',json.dumps(tests));return tests


if __name__=='__main__':self_test()
