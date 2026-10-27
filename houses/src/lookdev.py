"""Source-only shared PBR, metric charts and stock-glTF vertex weather.

No bake, imported art, custom runtime shader or hidden overlay texture. The
weather lives in one POINT Tint channel, interpolated over exterior surfaces.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
import bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import tiling
from textures import SETS


def materials(folder):
    mats={name:tiling.material('House'+name,folder,tint=True) for name in SETS}
    glass=tiling.material('HouseTrim',folder,tint=True);glass.name='HouseGlass'
    p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1
    p.inputs['IOR'].default_value=1.5
    # The selected clear/screen strips have metallic=0 in the shared ORM.
    # Keep this link: disconnecting it makes Blender write a second ORM image.
    glass.use_backface_culling=False
    mats['Glass']=glass
    return mats


def subdivide(ob,meta):
    if ob.get('component') not in ('wall','roof','foundation','fireplace','rear_landing','porch_steps'):return
    bm=bmesh.new();bm.from_mesh(ob.data)
    if ob.get('component')=='porch_steps':
        y0=meta['porch']['y0']
        for nose in (y0-.6269,y0-.3221,y0-.03):
            for off in (.035,.09):
                bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,nose+off,0),plane_no=(0,1,0))
    if ob.get('component') in ('wall','foundation'):
        # Add samples where splash and drips act, rather than tessellating every
        # manufactured trim bevel. Coordinates here are the static world frame.
        if ob.get('component')=='foundation':levels=(.10,.22)
        else:
            block=next(b for b in meta['blocks'] if b['name']==ob.get('block'))
            bottom=.99 if meta['spec']['cladding'][block['name']][ob.get('face')]=='veneer' else max(.02,block['floor']-.205)
            levels=tuple(bottom+d for d in (.0,.12,.28,.42))
        for z in levels:
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,z),plane_no=(0,0,1))
        if ob.get('component')=='wall':
            axis=0 if ob.get('face') in ('front','back') else 1
            # Project overhanging gutter corners onto their supporting wall.
            # Raw eave ends lie 305 mm beyond it and miss a narrow streak.
            coords=sorted(set(round(max(block['x0' if axis==0 else 'y0']+.07,min(point[axis],block['x1' if axis==0 else 'y1']-.07))+off,5) for d in meta['drains'] if d['block']==ob.get('block') for point in [d['centerline'][3],*d['gutter']] for off in (-.14,.0,.14)))
            top=next(b['eave'] for b in meta['blocks'] if b['name']==ob.get('block'))
            for z in (top-.38,):
                bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,z),plane_no=(0,0,1))
            for c in coords:
                p=[0,0,0];p[axis]=c;n=[0,0,0];n[axis]=1
                bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=p,plane_no=n)
    for _ in range(6):
        bm.normal_update()
        component=ob.get('component')
        face=ob.get('face',ob.name.split('_')[1] if '_' in ob.name else '')
        outward={'front':Vector((0,-1,0)),'back':Vector((0,1,0)),'left':Vector((-1,0,0)),'right':Vector((1,0,0))}.get(face)
        def exposed(f):
            if component=='roof':return f.normal.z>.4
            if component in ('wall','foundation') and outward:return f.normal.dot(outward)>.5
            return f.normal.z>-.5
        edges=[e for e in bm.edges if e.calc_length()>1.05 and any(f.calc_area()>.22 and exposed(f) for f in e.link_faces)]
        if not edges:break
        bmesh.ops.subdivide_edges(bm,edges=edges,cuts=1,use_grid_fill=True)
    bmesh.ops.triangulate(bm,faces=bm.faces[:])
    # Partial edge subdivision can leave collinear triangulation slivers.
    # Dissolve their zero-area edges into neighbors, retaining the surface.
    bmesh.ops.dissolve_degenerate(bm,edges=bm.edges[:],dist=1e-7)
    bmesh.ops.triangulate(bm,faces=bm.faces[:]);bm.to_mesh(ob.data);bm.free();ob.data.update()


def weather(p,n,role,component,meta,block_name=None,face=None):
    """Localized water, soil, shade and exposure, carried by stock COLOR_0."""
    x,y,z=p;m,g=meta['blocks'];north=min(1,max(0,n.y)*2.2)
    block=next((b for b in (m,g) if b['name']==block_name),min((m,g),key=lambda b:abs(y-b['y0'])+max(0,b['x0']-x,x-b['x1'])))
    ripple=(math.sin(x*8.7+y*3.9)+.5*math.sin(x*23.1-y*11.8))/1.5
    amount=0;green=0
    if role in ('Siding','Veneer','Concrete') and component not in ('foyer','porch_steps'):
        bottom=max(.02,block['floor']-.205)
        if role=='Siding' and meta['spec']['cladding'][block['name']].get(face)=='veneer':bottom=.99
        if role=='Concrete':bottom=0
        # Two to three first exposed courses. Soil is browner, not a gray wash.
        reach=bottom+.245+.065*ripple+.025*math.sin(x*3+y*7)
        amount+=.55*max(0,min(1,(reach+.075-z)/.20))
        if role=='Siding':
            green+=north*.20*math.exp(-((z-(block['eave']-.25))/.42)**2)*(.70+.30*math.sin(x*5.1)**2)
        for d in meta['drains']:
            if d['block']!=block['name']:continue
            # Overflow at both gutter corners, tapering down the supporting wall.
            for px,py,pz in d['gutter']:
                px=max(block['x0']+.07,min(px,block['x1']-.07))
                py=max(block['y0']+.07,min(py,block['y1']-.07))
                horizontal=abs(x-px) if abs(n.y)>abs(n.x) else abs(y-py)
                perpendicular=abs(y-py) if abs(n.y)>abs(n.x) else abs(x-px)
                below=pz-.12-z
                if perpendicular<.52 and 0<below<1.0:
                    amount+=.65*math.exp(-(horizontal/(.13+.04*below))**2)*math.exp(-below/.50)
            px,py,pz=d['centerline'][3]
            horizontal=abs(x-px) if abs(n.y)>abs(n.x) else abs(y-py)
            perpendicular=abs(y-py) if abs(n.y)>abs(n.x) else abs(x-px)
            if perpendicular<.4:
                amount+=.30*math.exp(-(horizontal/.15)**2)*(.7+.3*math.sin(z*6+x*4)**2)
                amount+=.48*math.exp(-(horizontal/.31)**2)*math.exp(-(z/.32)**2)
    if role=='Shingles' and component=='roof':
        ridge=block['eave']+block['pitch']*min(block['x1']-block['x0'],block['y1']-block['y0'])/2
        stripes=(.5+.5*math.sin(x*4.8+.23*math.sin(y*2)))**6
        below_ridge=math.exp(-((z-(ridge-.38))/1.0)**2)
        green=north*.42*(.30+.70*stripes)*(.30+.70*below_ridge)
    if component=='garage_door':
        # Entire bottom panel, strongest at rubber seal and recessed panel edges.
        amount+=.62*max(0,min(1,(.70-z)/.52))*(.82+.18*math.sin(x*8.7)**2)
    if component=='porch_steps' and n.z>0.5:
        y0=meta['porch']['y0']
        for nose in (y0-.6269,y0-.3221,y0-.03):
            amount+=.50*math.exp(-((y-(nose+.055))/.065)**2)*(.70+.30*math.sin(x*5.2)**2)
    if component=='drainage':amount+=.10*(.5+.5*math.sin(x*13+y*9)**2)
    amount=min(.72,amount);green=min(.40,green)
    tint=Vector((1-amount*.55-green*.52,1-amount*.65-green*.38,1-amount*.78-green*.58))
    return tint,amount,green


def prepare(source,out,folder=Path('textures/source')):
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
    meta=json.loads(source.with_suffix('.json').read_text());mats=materials(folder)
    stats=dict(vertices_weathered=0,north_algae_vertices=0,exterior_added_triangles=0)
    densities={name:[] for name in mats};triangles=0
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':continue
        me=ob.data;me.calc_loop_triangles();before=len(me.loop_triangles);subdivide(ob,meta);me=ob.data
        oldnames=[m.name.replace('House_','') for m in me.materials]
        for i,role in enumerate(oldnames):me.materials[i]=mats[role]
        attr=me.color_attributes['Tint'];uv=me.uv_layers.active
        world=[ob.matrix_world@v.co for v in me.vertices]
        component=ob.get('component','number');role_by_vertex={};normal_by_vertex={};scores={}
        for poly in me.polygons:
            role=oldnames[poly.material_index];n=(ob.matrix_world.to_3x3()@poly.normal).normalized()
            for vi in poly.vertices:
                role_by_vertex[vi]=role
                outward={'front':Vector((0,-1,0)),'back':Vector((0,1,0)),'left':Vector((-1,0,0)),'right':Vector((1,0,0))}.get(ob.get('face'))
                score=n.dot(outward) if outward else (n.z if component in ('roof','porch_steps') else poly.area)
                if score>scores.get(vi,-1e20):normal_by_vertex[vi]=n;scores[vi]=score
            axis=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=axis]
            strip=0
            if role in ('Trim','Glass'):
                if component=='drainage' or component in ('roof_vent','valley','flashing'):strip=5
                elif component=='eave_rake_soffit' and n.z<-.6:strip=2
                elif component=='rear_landing' and meta['spec']['rear_landing']=='deck':strip=3
                elif role=='Glass':
                    # The lower sash has effective insect-screen coverage.
                    opening=next((o for o in meta['openings'] if ob.name.startswith(o['id'])),None)
                    center=sum(world[i].z for i in poly.vertices)/len(poly.vertices)
                    strip=7 if opening and center<opening['z']+opening['h']/2 else 6
                elif component=='window':
                    c=attr.data[poly.vertices[0]].color
                    shutter=meta['spec']['colors']['shutter']
                    if max(abs(c[k]-shutter[k]*.78) for k in range(3))<.002:strip=1
                    elif int(ob.name.split('_')[2])%4==1 and max(c[:3])<.5 and min(c[:3])>.23:strip=4
            points=[world[i] for i in poly.vertices]
            if role=='Trim' and strip not in (1,4):
                # Long stock extrusions run along U; avoid stretching one atlas
                # strip over the full six-meter height of a corner post.
                axes.sort(key=lambda k:max(p[k] for p in points)-min(p[k] for p in points),reverse=True)
            lo=min(p[axes[1]] for p in points);hi=max(p[axes[1]] for p in points)
            for li in poly.loop_indices:
                p=world[me.loops[li].vertex_index]
                if role in ('Trim','Glass'):
                    # U repeats every 4 m; V is contained within its atlas strip.
                    # Each face stays in its finish region, including long posts.
                    span=max(.5,(hi-lo)/.92)
                    u=p[axes[0]]/4
                    if strip==5:
                        # Painted gutters occupy the dielectric part; flashing
                        # and vent metal select the metallic end of the strip.
                        u=.78+(.20*(p[axes[0]]%4)/4) if component in ('roof_vent','valley','flashing') else .03+.68*(p[axes[0]]%4)/4
                    uv.data[li].uv=(u,(strip+.04+(p[axes[1]]-lo)/span)/8)
                    assert strip/8<=uv.data[li].uv.y<=(strip+1)/8, (ob.name,strip,uv.data[li].uv.y)
                elif role=='Shingles' and abs(n.z)>.30:
                    # Along-ridge U; V is true slope distance, rather than XY squash.
                    if abs(n.y)>=abs(n.x):coord=(p.x,p.y/max(.2,abs(n.z)))
                    else:coord=(p.y,p.x/max(.2,abs(n.z)))
                    uv.data[li].uv=tuple(v/SETS[role][1] for v in coord)
                else:
                    uv.data[li].uv=(p[axes[0]]/SETS[role][1],p[axes[1]]/SETS[role][1])
        for v in me.vertices:
            role=role_by_vertex[v.index];p=world[v.index];n=normal_by_vertex[v.index]
            c=Vector(attr.data[v.index].color[:3])
            if role in ('Veneer','Glass'):c=Vector((1,1,1))
            if role=='Shingles':
                c=Vector(dict(warm_charcoal=(1.0,.84,.63),weathered_wood=(1.0,.81,.60),dark_brown=(.86,.70,.53))[meta['spec']['shingle_color']])
            if role=='Concrete':c=Vector((.8,.8,.8))
            factor,amount,green=weather(p,n,role,component,meta,ob.get('block'),ob.get('face'))
            if component=='front_door':
                # Sun fading is concentrated on the broad exposed face.
                fade=.34+.10*math.sin(p.z*1.8)**2
                # Fade toward a lighter, less saturated version of this paint.
                gray=sum(c)/3
                c=c.lerp(c*.55+Vector((gray+.10,gray+.085,gray+.065))*.45,fade)
            if component=='porch_steps' and n.z>.5:
                # Polished, lighter concrete at the tread's exposed leading edge.
                y0=meta['porch']['y0']
                wear=max(max(0,1-abs(p.y-(nose+.025))/.06) for nose in (y0-.6269,y0-.3221,y0-.03))
                factor*=1+.08*wear*(.65+.35*math.cos(p.x*2.1)**2)
            attr.data[v.index].color=(*(c[k]*factor[k] for k in range(3)),1)
            stats['vertices_weathered']+=amount>.04;stats['north_algae_vertices']+=green>.025
        me.color_attributes.active_color=attr;me.calc_loop_triangles()
        stats['exterior_added_triangles']+=len(me.loop_triangles)-before;triangles+=len(me.loop_triangles)
        # Area-based observed UV density, grouped by shared material.
        for t in me.loop_triangles:
            p=[world[i] for i in t.vertices];a=(p[1]-p[0]).cross(p[2]-p[0]).length/2
            u=[uv.data[i].uv for i in t.loops];ua=abs((u[1]-u[0]).cross(u[2]-u[0]))/2
            role=oldnames[t.material_index]
            if a>1e-7 and ua>1e-12:densities[role].append((math.sqrt(ua/a)*SETS.get(role,SETS['Trim'])[0],a))
    import numpy as np
    def percentiles(rows):
        rows=sorted(rows);v=np.array([r[0] for r in rows]);w=np.cumsum([r[1] for r in rows]);w/=w[-1]
        return dict(zip(('p10','median','p90'),map(float,np.interp([.1,.5,.9],w,v))))
    assert 30000<=triangles<=80000,triangles
    meta.update(stage='source look-development checkpoint; before Cycles bake',triangles=triangles,
        material_sets=5,materials=6,weather=stats,source_geometry_sha256=meta['geometry_sha256'],
        density_px_m={k:percentiles(v) for k,v in densities.items() if v},density_method='triangle UV/world area, physical area weighted percentiles',
        original_form_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    out.parent.mkdir(parents=True,exist_ok=True);out.with_suffix('.json').write_text(json.dumps(meta,indent=2))
    bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()));print('LOOKDEV',triangles,stats,meta['density_px_m'])
    return meta


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=Path('build/house.blend'))
    p.add_argument('--out',type=Path,default=Path('build/lookdev.blend'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);prepare(a.source,a.out)
