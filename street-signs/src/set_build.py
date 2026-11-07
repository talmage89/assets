"""Additional sign library only. Shared sheet and daylight sheeting grades, real-gauge drilled blanks.

Both the inspection blend and separate glTF are rebuildable. Original STOP,
blades, atlases and delivery files are never opened for writing.
"""
import argparse,json,math,sys,hashlib
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
from kit import model as G
from set_catalog import SIGNS,ASSEMBLIES,INCH

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('build/set/Signs.blend'));a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    folder=Path(__file__).resolve().parents[1];work=folder/'build/set';layout=json.loads((work/'layout.json').read_text())
    im=bpy.data.images.load(str(work/'T_RoadSigns_Faces.png'))
    def finish(name,rough,metal):
        m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
        node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=im;m.node_tree.links.new(node.outputs['Color'],p.inputs['Base Color'])
        if not metal:
            factor=m.node_tree.nodes.new('ShaderNodeMath');factor.operation='MULTIPLY';factor.inputs[1].default_value=.5;m.node_tree.links.new(node.outputs['Alpha'],factor.inputs[0]);m.node_tree.links.new(factor.outputs[0],p.inputs['Specular IOR Level'])
        return m
    mat=finish('RoadSigns_GalvanizedAluminum',.52,1)
    engineering=finish('RoadSigns_EngineeringGrade',.39,0)
    prismatic=finish('RoadSigns_HighIntensityPrismatic',.27,0)
    roots=[];current=None;construction={}
    def own(o,chart='metal'):
        o.parent=current;o['asset_set']=current.name;o['solid']=True
        if o.type=='MESH':
            if o.modifiers:G.apply(o)
            uv=o.data.uv_layers.active or o.data.uv_layers.new(name='UVMap');uv.name='UVMap';r=layout[chart]
            for x in uv.data:x.uv=((r[0]+r[2])/2,(r[1]+r[3])/2)
        return o
    def box(n,c,s):return own(G.box(n,c,s,mat,0))
    def cyl(n,a,b,r,s=8):return own(G.cylinder(n,a,b,r,mat,s))
    def bolt(n,x,y,z):
        kind=current.get('post_type','band')
        rear=.0312 if kind=='round' else .0264 if kind=='square' else -.010 if kind in ('u2','u3') else y+.027
        cyl(n+' shank',(x,y-.008,z),(x,rear+.009,z),.003,6)
        cyl(n+' carriage head',(x,y-.0015,z),(x,y-.004,z),.0067,10)
        cyl(n+' rear nut',(x,rear,z),(x,rear+.007,z),.0055,6)
    def sticker(x,y,z,w=.095,h=.038):
        o=own(G.plane_uv('Agency inspection stencil / date',[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],mat))
        r=layout['backlabel'];uv=o.data.uv_layers.active
        for poly in o.data.polygons:
            for li in poly.loop_indices:
                v=o.data.vertices[o.data.loops[li].vertex_index].co
                uv.data[li].uv=(r[0]+(1-(v.x-x+w/2)/w)*(r[2]-r[0]),r[1]+(v.z-z+h/2)/h*(r[3]-r[1]))
        o['solid']=False
    def plate(key,center):
        spec=SIGNS[key];w,h=spec['w']*INCH,spec['h']*INCH;r=spec['radius']*INCH
        if spec['shape']=='diamond':
            side=w;w=h=side*math.sqrt(2);pts=G.fillet_polygon([(0,-h/2),(w/2,0),(0,h/2),(-w/2,0)],r,3)
        elif spec['shape']=='yield':pts=G.fillet_polygon([(-w/2,h/2),(0,-h/2),(w/2,h/2)],r,4)
        elif spec['shape']=='school':pts=G.fillet_polygon([(-w/2,-h/2),(w/2,-h/2),(w/2,0),(0,h/2),(-w/2,0)],r,3)
        else:pts=G.rounded_rectangle(w,h,r,3)
        x,y,z=center;t=.080*INCH
        ob=G.profile(key+' .080 aluminum blank',pts,y-t/2,y+t/2,mat,axis='Y');ob.location=(x,0,z)
        # Bolt holes go through the actual sheet, rather than an overlaid print.
        holes=[z-h/2+.065,z+h/2-.065]
        if spec['shape']=='yield':holes=[z-h*.22,z+h*.30]
        for zh in holes:
            cut=G.cylinder('Punch 3/8 inch',(x,y-.015,zh-z),(x,y+.015,zh-z),.0047625,mat,10);cut.location.z+=z
            # Cutter coordinates are world-authored, same datum as the blank.
            G.boolean(ob,cut)
        own(ob);uv=ob.data.uv_layers.active;rr=layout[key];mr=layout['metal']
        ob.data.materials.append(engineering if len(roots)%2 else prismatic)
        ys=[v.co.y for v in ob.data.vertices];gauge=max(ys)-min(ys)
        bores=[]
        for zh in holes:
            vertices=[v.co for v in ob.data.vertices if abs(math.hypot(v.co.x,v.co.z+z-zh)-.0047625)<2e-5]
            assert len(vertices)>=20,(key,zh,len(vertices))
            measured=[sum(v[k] for v in vertices)/len(vertices) for k in (0,2)]
            bores.append(dict(center_xz_m=[measured[0],measured[1]+z],vertices=len(vertices),radial_error_m=max(abs(math.hypot(v.x,v.z+z-zh)-.0047625) for v in vertices)))
        assert abs(gauge-.002032)<1e-6
        construction.setdefault(current.name,[]).append(dict(face=key,measured_gauge_m=gauge,actual_bore_measurements=bores))
        for poly in ob.data.polygons:
            front=poly.normal.y<-.9;poly.material_index=1 if front else 0
            for li in poly.loop_indices:
                v=ob.data.vertices[ob.data.loops[li].vertex_index].co
                uv.data[li].uv=(rr[0]+(v.x+w/2)/w*(rr[2]-rr[0]),rr[1]+(v.z+h/2)/h*(rr[3]-rr[1])) if front else (mr[0]+(v.x+w/2)/w*(mr[2]-mr[0]),mr[1]+(v.z+h/2)/h*(mr[3]-mr[1]))
        for zh in holes:
            box('Back mounting spacer',(0,y+.009,zh),(.030,.016,.025));bolt('1/4-20 sign fastener',0,y-t/2,zh)
        sticker(w*.25,y+t/2+.00015,z-h*.25)
        ob['sign_code']=spec['code'];ob['gauge_m']=t;ob['layout_page']=spec['page'];ob['sheeting_type']='ASTM I engineering grade' if len(roots)%2 else 'ASTM III high intensity prismatic'
        return w,h
    records={}
    for index,spec in enumerate(ASSEMBLIES):
        current=G.pivot('RoadSign_'+spec['name'],(0,0,0));current['static_root']=True;current['module_kind']='RoadSign';current['post_type']=spec['post'];current['socket_grid_m']=.1524;current['front']='-Y'
        roots.append(current);bottom=2.1336
        heights=[]
        for key in spec['faces']:
            face_spec=SIGNS[key];h=face_spec['h']*INCH*(math.sqrt(2) if face_spec['shape']=='diamond' else 1)
            heights.append((key,bottom+h/2));bottom+=h+.0508
        top=bottom-.0508;posth=max(z+SIGNS[k]['h']*INCH*.34 for k,z in heights)
        kind=spec['post']
        if kind=='round':
            # 2-3/8 in OD support, explicit hollow rim and cap.
            own(G.lathe('Round galvanized post',[(0,.03016), (posth,.03016),(posth,.0274),(0,.0274)],mat,12,closed=True))
        elif kind=='square':
            for width,wall,H in ((.0508,.002,posth),(.05715,.002,.0762)):
                pts=[(-width/2,-width/2),(width/2,-width/2),(width/2,width/2),(-width/2,width/2)]
                ip=[(-width/2+wall,-width/2+wall),(width/2-wall,-width/2+wall),(width/2-wall,width/2-wall),(-width/2+wall,width/2-wall)]
                own(G.ring_loft('Telescoping square tube / open gauge', [[(x,y,z) for x,y in sec] for z,sec in [(0,pts),(H,pts),(H,ip),(0,ip)]],mat))
            cyl('Anchor sleeve cross bolt',(-.037,0,.0381),(.037,0,.0381),.004,6)
        else:
            # Rolled hat section, 2 lb/ft nominal; the 3 lb profile has heavier walls.
            half=.0396875
            def section(t):return [(-half,.018),(-.013,.018),(-.007,-.014),(.007,-.014),(.013,.018),(half,.018),(half,.018+t),(.013-t*.83,.018+t),(.007-t*.83,-.014+t),(-.007+t*.83,-.014+t),(-.013+t*.83,.018+t),(-half,.018+t)]
            def area(pts):return abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(pts,pts[1:]+pts[:1])))/2
            target=(2 if kind=='u2' else 3)*.45359237/.3048/7850
            lo,hi=.001,.008
            for _ in range(40):
                t=(lo+hi)/2
                if area(section(t))<target:lo=t
                else:hi=t
            sec=section((lo+hi)/2);current['estimated_section_mass_lb_ft']=area(sec)*7850*.3048/.45359237
            if current.name=='RoadSign_speed25':
                own(G.loft('Impact-bent rolled U channel',[[(x,y,z) for x,y in sec] for z in (0,.35,posth)],mat))
                current['impact_bend_degrees']=3.0;current['impact_bend_height_m']=.35
            else:own(G.profile('Rolled '+kind+' channel',sec,0,posth,mat,axis='Z'))
        # Stamped perforation indication for form review only. Six-millimeter
        # mounting hardware remains geometry; all holes become baked normals later.
        dark=layout.get('onewayR');rr=(dark[0]+.002,(dark[1]+dark[3])/2)
        if kind!='round':
            vs=[];fs=[]
            for j in range(4,round(posth/.0254)):
                z=j*.0254;y=-.026 if kind=='square' else -.015
                start=len(vs);vs += [(-.0047625,y,z-.0047625),(.0047625,y,z-.0047625),(.0047625,y,z+.0047625),(-.0047625,y,z+.0047625)];fs.append(tuple(start+k for k in range(4)))
            o=own(G.mesh('Perforation indication 3/8in at 1in pitch',vs,fs,mat));o['solid']=False
            for v in o.data.uv_layers.active.data:v.uv=rr
        y=-.035 if kind=='round' else -.031
        for key,z in heights:plate(key,(0,y,z))
        # Banded pole mounting option is an independent reusable bracket module.
        current.location=(index%8*1.8,index//8*2.3,0)
        current['lowest_plate_m']=2.1336;current['face_keys']=spec['faces'];current['installation_offset_m']=.6096
    current=G.pivot('RoadSign_PoleBandBracket',(14.4,4.6,0));current['static_root']=True;roots.append(current)
    for z in (.15,.55):
        # Closed 1mm strip; independent short chords would sink into a host
        # cylinder and appear as disconnected tabs. Inner clearance also
        # accounts for the polygonal chord, not just vertex radii.
        own(G.lathe('19mm continuous stainless band',[(z-.0095,.161),(z+.0095,.161),(z+.0095,.162),(z-.0095,.162)],mat,32,closed=True))
        box('Band sign rail',(0,-.169,z),(.070,.018,.060));bolt('Band tension screw',.028,-.180,z)
    for rt in roots:
        obs=[o for o in rt.children_recursive if o.type=='MESH']
        for o in obs:G.apply(o)
        bpy.ops.object.select_all(action='DESELECT')
        for o in obs:o.select_set(True)
        bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();merged=obs[0];merged.name=rt.name+'_Mesh'
        tr=merged.modifiers.new('Triangle delivery','TRIANGULATE');G.apply(merged);merged.data.calc_loop_triangles()
        if rt.get('impact_bend_degrees'):
            # Joining retains the active child's origin. Deform in the module
            # footprint frame, not that arbitrary carriage-head/label frame.
            bpy.context.view_layer.update()
            to_root=rt.matrix_world.inverted()@merged.matrix_world;from_root=to_root.inverted()
            hinge=Vector((0,0,.35));rotation=Matrix.Rotation(math.radians(rt['impact_bend_degrees']),3,'Y')
            displacements=[]
            for v in merged.data.vertices:
                point=to_root@v.co
                if point.z>.35:
                    bent=hinge+rotation@(point-hinge);v.co=from_root@bent
                    displacements.append((to_root@v.co-point).length)
            rt['measured_max_bend_displacement_m']=max(displacements)
            assert .12<max(displacements)<.15,displacements
            merged.data.update()
        bpy.context.view_layer.update();points=[rt.matrix_world.inverted()@merged.matrix_world@v.co for v in merged.data.vertices]
        records[rt.name]=dict(triangles=len(merged.data.loop_triangles),bounds_m=[[min(p[k] for p in points) for k in range(3)],[max(p[k] for p in points) for k in range(3)]],post=rt.get('post_type','band'),faces=list(rt.get('face_keys',[])))
        records[rt.name]['construction']=construction.get(rt.name,[])
        # Reusable ground-centered origins, even in inspection arrangement.
        rt['footprint_m']=[max(p.x for p in points)-min(p.x for p in points),max(p.y for p in points)-min(p.y for p in points)]
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
    export=folder/'export/set/RoadSigns.gltf';export.parent.mkdir(parents=True,exist_ok=True)
    # Each glTF uses external images in its own canonical set directory.
    bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLTF_SEPARATE',export_texture_dir='textures',export_extras=True,export_animations=False,export_tangents=True)
    for rt in roots:
        bpy.ops.object.select_all(action='DESELECT')
        for ob in [rt,*rt.children_recursive]:ob.select_set(True)
        old=rt.location.copy();rt.location=(0,0,0)
        bpy.ops.export_scene.gltf(filepath=str(export.with_name(rt.name+'.gltf')),use_selection=True,export_format='GLTF_SEPARATE',export_texture_dir='textures',export_extras=True,export_animations=False,export_tangents=True)
        rt.location=old
    (work/'manifest.json').write_text(json.dumps(dict(stage='Final stock glTF / shared sheeting and metal chart',pieces=records,sheet_size=[2048,2048],font='DejaVu Sans Condensed / Book fitted to SHS cap heights and line widths'),indent=2))
    print('SIGN SET',len(records),'assemblies',sum(r['triangles'] for r in records.values()),'triangles')
if __name__=='__main__':main()
