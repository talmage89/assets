"""Explicit reusable atlas tiles, separate from unique non-overlapping islands.

A tiled mesh keeps authored UVs inside a declared rectangle. Repetition is
intentional only there; the rest of the atlas retains ordinary overlap checks.
"""
import fnmatch,math

def tiled_spec(name,config):
    for pattern,spec in config.get('TILED_MESHES',{}).items():
        if fnmatch.fnmatchcase(name,pattern):return spec
    return None

def tile_report(objects,config,size=2048,layer='BakeUV'):
    rows=[];errors=[]
    for ob in objects:
        spec=tiled_spec(ob.name,config)
        if spec is None:continue
        u0,v0,u1,v1=spec['rect'];uv=ob.data.uv_layers.get(layer) or ob.data.uv_layers.active
        if uv is None:errors.append(ob.name+': missing tile UVs');continue
        densities=[];outside=0;invalid=0;ob.data.calc_loop_triangles()
        for tri in ob.data.loop_triangles:
            coords=[uv.data[i].uv for i in tri.loops]
            outside+=any(p.x<u0-1e-6 or p.x>u1+1e-6 or p.y<v0-1e-6 or p.y>v1+1e-6 for p in coords)
            area=abs((coords[1]-coords[0]).cross(coords[2]-coords[0]))*.5
            points=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
            physical=(points[1]-points[0]).cross(points[2]-points[0]).length*.5
            if area<1e-14 or physical<1e-12:invalid+=1
            else:densities.append(math.sqrt(area/physical)*size)
        if outside or invalid or not densities:errors.append(ob.name+': invalid tile triangles')
        if densities and not (spec.get('density_min',0)<=min(densities) and max(densities)<=spec.get('density_max',1e8)):errors.append(ob.name+': tile texel density outside declared band')
        rows.append(dict(object=ob.name,triangles=len(ob.data.loop_triangles),rectangle=spec['rect'],outside=outside,degenerate=invalid,density_min=min(densities,default=0),density_max=max(densities,default=0),overlap_policy='authored reuse within this tile only'))
    return dict(passed=not errors,errors=errors,meshes=rows)
