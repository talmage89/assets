"""Assemble only imported game modules; world-rephase UVs for stock glTF."""
import argparse,hashlib,json,math,sys,random
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from kit.tiling import world_uv,export
from dimensions import *
from build import terrain_tint,curb_project,ramp_project,joint_floor_uv,inlet_return_uv


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=Path('export/Ground.glb'));p.add_argument('--out',type=Path,default=Path('export/GroundStreet.glb'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.source.resolve()))
    library={ob.name:ob for ob in bpy.context.scene.objects if ob.parent is None}
    original=list(bpy.context.scene.objects);placements=[];rng=random.Random(5317)
    def place(kind,name,loc=(0,0,0),yaw=0):
        source=library[kind];copies={}
        for ob in [source]+list(source.children_recursive):
            cp=ob.copy()
            if cp.type=='MESH':cp.data=ob.data.copy()
            bpy.context.collection.objects.link(cp);copies[ob]=cp
        for ob,cp in copies.items():
            cp.parent=copies.get(ob.parent);cp.matrix_basis=ob.matrix_basis.copy();cp.name=name if ob==source else name+'__'+ob.name
        rt=copies[source];rt.location=loc;rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,math.radians(yaw))
        placements.append(dict(module=kind,name=name,location=list(loc),yaw=yaw))
        return rt
    place('Road_Intersection','Junction')
    for k in range(4):
        angle=k*90;theta=math.radians(angle);c,s=math.cos(theta),math.sin(theta)
        def xy(x,y):return (c*x-s*y,s*x+c*y,0)
        place('Curb_Corner',f'Corner_{k}',xy(CORE,CORE),angle)
        place('Sidewalk_Corner',f'WalkCorner_{k}',xy(CORE,CORE),angle)
    for arm in range(4):
        yaw=arm*90;theta=math.radians(yaw);c,s=math.cos(theta),math.sin(theta)
        def xy(x,y):return (c*x-s*y,s*x+c*y,0)
        count=6 if arm in (0,2) else 3
        for i in range(count):
            cy=CORE+(i+.5)*LENGTH
            # Repairs are rare events, not a repeating wear package per bay.
            variant='C' if (arm,i)==(0,4) else 'B' if (arm,i)==(3,1) else 'A'
            manhole=(arm,i)==(2,1)
            place('Road_Straight_Manhole' if manhole else 'Road_Straight_'+variant,f'Arm{arm}_Road{i}',xy(0,cy),yaw)
            if manhole:
                # Rotate the casting with its crowned road; its local 1:48
                # plane and polygonal patch edge match the replacement skin.
                p=xy(1.1,cy);place('Manhole','Street_manhole',(p[0],p[1],road_z(1.1)),yaw)
            for side in (-1,1):
                syaw=yaw+(180 if side<0 else 0)
                for j in range(2):
                    yy=CORE+i*LENGTH+(j+.5)*BAY
                    kind='Curb_Ramp' if i==0 and j==0 else 'Curb_Straight'
                    # A 10 ft depressed drive opening in the third main-road bay.
                    drive=i==2 and (arm,side) in ((0,1),(2,-1))
                    if drive:
                        if j:continue
                        kind='Curb_DrivewayCut';yy=CORE+(i+.5)*LENGTH
                    if (arm,side,i,j)==(2,-1,0,1):kind='Curb_StormInlet'
                    place(kind,f'Arm{arm}_Curb{side}_{i}_{j}',xy(side*FACE,yy),syaw)
                    if drive:
                        place('Driveway_Apron',f'Arm{arm}_Drive_apron',xy(side*BACK,yy),syaw)
                        place('Lawn_DriveWings',f'Arm{arm}_Drive_wings',xy(side*BACK,yy),syaw)
                        for slab in range(2):
                            p=xy(side*(WALK_OUT+slab*BAY),yy)
                            place('Driveway_Slab',f'Arm{arm}_Drive_slab{slab}',(p[0],p[1],.004*slab*BAY),syaw)
                    elif kind!='Curb_Ramp':
                        place('Lawn_Strip',f'Arm{arm}_Strip{side}_{i}_{j}',xy(side*BACK,yy),syaw)
                if i==0:
                    place('Sidewalk_Ramp',f'Arm{arm}_Ramp{side}',xy(side*BACK,CORE+PANEL),syaw)
                for j in range(4):
                    if i==0 and j<2:continue
                    yy=CORE+i*LENGTH+(j+.5)*PANEL
                    variant='Sidewalk_B' if rng.random()<.06 else 'Sidewalk_A'
                    # Mirrored sidewalk root lies on its outside edge for a 180° placement.
                    x=side*WALK_IN
                    place(variant,f'Arm{arm}_Walk{side}_{i}_{j}',xy(x,yy),syaw)
        # Crossing root itself includes correctly crowned 18 in bars and 12 in stop line.
        place('Markings_Crossing',f'Crossing{arm}',xy(0,CORE+PANEL),yaw)
    # Four curved planting strips and yard corners complete the existing
    # tangencies. North/south yard bays fill the lots; short east/west fillers
    # stop at those bays instead of stacking coplanar lawn rectangles.
    for k in range(4):
        theta=k*math.pi/2;c,s=math.cos(theta),math.sin(theta)
        p=(c*CORE-s*CORE,s*CORE+c*CORE,0)
        place('Lawn_CornerStrip',f'Corner_turf{k}',p,k*90)
        place('Lawn_CornerYard',f'Corner_yard{k}',p,k*90)
    for sx in (-1,1):
        for sy in (-1,1):
            for row in range(6):
                cy=sy*(CORE+(row+.5)*LENGTH)
                for col in range(4):
                    narrow=col==3
                    kind='Lawn_FieldNarrow' if narrow else 'Lawn_Yard' if col==0 else 'Lawn_Field'
                    if sx==1 and row==2 and col==0:
                        for sign,label in ((-1,'S'),(1,'N')):
                            place('Lawn_DriveSide_'+label,f'Lot_drive_{sy}_{label}',(WALK_OUT,cy+sign*(BAY/2+PANEL/2),0))
                        continue
                    place(kind,f'Lot_{sx}_{sy}_{row}_{col}',(sx*(WALK_OUT+col*LENGTH),cy,.004*col*LENGTH),0 if sx>0 else 180)
            for row in range(3):
                cx=sx*(CORE+(row+.5)*LENGTH)
                place('Lawn_YardNarrow',f'EastWest_lot_{sx}_{sy}_{row}',(cx,sy*WALK_OUT,0),90 if sy>0 else -90)
    # The cast cap replaces the curb skin right up to its back edge. Exclude
    # only overhanging fringe cards at this inlet: turf skin/other strips stay
    # untouched, and no grass is allowed to sprout through the iron cap.
    inlet_root=next(o for o in bpy.context.scene.objects if o.name=='Arm2_Curb-1_0_1')
    bpy.context.view_layer.update()
    inverse=inlet_root.matrix_world.inverted()
    import bmesh
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or ob in original or not any(m.name=='GroundFoliage' for m in ob.data.materials):continue
        bm=bmesh.new();bm.from_mesh(ob.data);remove=[]
        for face in bm.faces:
            if ob.data.materials[face.material_index].name!='GroundFoliage':continue
            points=[inverse@ob.matrix_world@v.co for v in face.verts]
            if min(p.x for p in points)<CURB+.025 and max(p.x for p in points)>-.02 and min(p.y for p in points)<.48 and max(p.y for p in points)>-.48:remove.append(face)
        if remove:
            bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(ob.data)
        bm.free()
    for ob in original:bpy.data.objects.remove(ob,do_unlink=True)
    bpy.context.view_layer.update()
    # Blend the short east/west yard fillers into the north/south lots. Their
    # distant edge must meet the actual lot grade, not restart at walk height.
    # Hermite terms preserve the 0.4% walk-edge tangent and flatten at the lot.
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ob.parent or not ob.parent.name.startswith('EastWest_lot'):continue
        if not ob.data.materials or ob.data.materials[0].name!='Lawn':continue
        depth=RADIUS-CURB-STRIP-PANEL;normals=[]
        base={i for p in ob.data.polygons if ob.data.materials[p.material_index].name=='Lawn' for i in p.vertices}
        original_normals=[n.vector.copy() for n in ob.data.vertex_normals]
        for v in ob.data.vertices:
            p=ob.matrix_world@v.co;t=max(0,min(1,v.co.x/depth));h=t*t*(3-2*t)
            correction=.004*(abs(p.x)-WALK_OUT-depth)
            target=YARD_GRADE-.005+.004*depth*(t+t*t-t*t*t)+h*correction
            if v.index not in base:
                v.co.z+=target-(YARD_GRADE-.005+.004*v.co.x)
                normals.append(original_normals[v.index]);continue
            v.co.z=target
            dx=.004*(1+2*t-3*t*t)+6*t*(1-t)/depth*correction
            dy=h*.004*math.copysign(1,p.x)*ob.matrix_world.to_3x3()[0][1]
            normals.append(Vector((-dx,-dy,1)).normalized())
        for poly in ob.data.polygons:poly.use_smooth=True
        ob.data.normals_split_custom_set_from_vertices(normals)
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ob.parent or ob.parent.get('module')!='Lawn_CornerYard':continue
        depth=RADIUS-CURB-STRIP-PANEL;normals=[]
        inverse=ob.matrix_world.to_3x3().inverted()
        base={i for p in ob.data.polygons if ob.data.materials[p.material_index].name=='Lawn' for i in p.vertices}
        original_normals=[n.vector.copy() for n in ob.data.vertex_normals]
        for v in ob.data.vertices:
            p=ob.matrix_world@v.co
            # Only the lawn skin participates; authored foliage UVs are kept.
            corner_fraction=(CORE-abs(p.x))/depth;t=(abs(p.y)-WALK_OUT)/depth
            h=t*t*(3-2*t);g=t+t*t-t*t*t
            target=YARD_GRADE-.005+.004*depth*(g-corner_fraction*h)
            if v.index not in base:
                old_a=-v.co.x/depth;old_t=1+v.co.y/depth
                old_h=old_t*old_t*(3-2*old_t);old_g=old_t+old_t*old_t-old_t**3
                v.co.z+=target-(YARD_GRADE-.005+.004*depth*(old_g-old_a*old_h))
                normals.append(original_normals[v.index]);continue
            v.co.z=target
            dx=.004*h*math.copysign(1,p.x)
            dy=.004*((1+2*t-3*t*t)-corner_fraction*6*t*(1-t))*math.copysign(1,p.y)
            normals.append((inverse@Vector((-dx,-dy,1))).normalized())
        for poly in ob.data.polygons:poly.use_smooth=True
        ob.data.normals_split_custom_set_from_vertices(normals)
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        kind=ob.get('surface_kind','')
        if kind in ('Asphalt','Concrete','Lawn'):
            world_uv(ob,{'Asphalt':ASPHALT_TILE,'Concrete':CONCRETE_TILE,'Lawn':LAWN_TILE}[kind],project=curb_project if ob.get('curb_chart') else ramp_project if ob.get('ramp_chart') else None,material_filter=lambda m:m.name in ('Asphalt','Concrete','Lawn'))
            inlet_return_uv(ob)
            # glTF's importer names COLOR_0 "Color" and stores triangle colors
            # on corners. Recreate its referenced layer as float point data so
            # world-field evaluation is continuous and never indexed as loops.
            colors=ob.data.color_attributes.active_color
            if colors:
                name=colors.name;ob.data.color_attributes.remove(colors)
                colors=ob.data.color_attributes.new(name=name,type='FLOAT_COLOR',domain='POINT')
                for v in ob.data.vertices:
                    p=ob.matrix_world@v.co
                    tint=list(terrain_tint(p,kind));scale=ob.get('tint_scale',1.)
                    if kind=='Concrete' and 'Inlet_depressed_gutter' in ob.name and v.co.z<-.25:
                        # This floor is visible through the slots. Wet settled
                        # sediment absorbs light even where the sun reaches it;
                        # its local tint survives joining the concrete body.
                        scale*=.12
                    if kind=='Concrete' and 'Inlet_depressed_gutter' in ob.name and v.co.z>-.25:
                        # Water accelerates into the lip; damp/silt darken the
                        # inlet shoulders and wash out toward normal gutter.
                        distance=max(0,abs(v.co.y)-.45)
                        low=math.exp(-((v.co.x+.12)/.22)**2)
                        deposition=math.exp(-distance/.24)*low
                        scale*=1-.48*deposition
                    if kind=='Concrete' and '_Walk' in ob.name:
                        # Different pours vary quietly in value. Soil and
                        # joint edges darken; centers remain foot-polished.
                        local=v.co
                        batch=.970+.025*(.5+.5*math.sin(math.floor((p.y+.762)/PANEL)*91.7+math.floor((p.x+.762)/PANEL)*17.1))
                        edge=math.exp(-max(0,min(local.x,PANEL-local.x))/.075)
                        joint=math.exp(-abs(local.y)/.045)
                        scale*=batch*(1-.045*edge-.035*joint)
                    for j in range(3):tint[j]*=scale
                    colors.data[v.index].color=tint
    # Causal trim layers are fitted onto imported actual triangles, not assumed heights.
    from weather import apply_weather
    weather=apply_weather()
    weather_meshes=[ob for ob in bpy.context.scene.objects if ob.type=='MESH' and ob.get('decal_cause')]
    if weather_meshes:
        bpy.ops.object.select_all(action='DESELECT')
        for ob in weather_meshes:ob.select_set(True)
        bpy.context.view_layer.objects.active=weather_meshes[0];bpy.ops.object.join()
        bpy.context.object.name='Localized_weather';bpy.context.object['decal_cause']='flow sediment, tire scuffs and planter damp'
    export(a.out)
    tile_boards=[]
    for kind,x,coverage in [('Asphalt',-24,ASPHALT_TILE),('Concrete',0,CONCRETE_TILE),('Lawn',24,LAWN_TILE)]:
        bpy.ops.mesh.primitive_plane_add(size=coverage*3,location=(x,0,0));ob=bpy.context.object;ob.name='TileBoard_'+kind
        ob.data.materials.append(next(m for m in bpy.data.materials if m.name==kind))
        world_uv(ob,coverage,offset=(-x/coverage+1.5,1.5))
        attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        for i in range(4):attr.data[i].color=(1,1,1,1)
        tile_boards.append(ob)
    export(Path('export/GroundTiles.glb'),objects=tile_boards)
    for ob in tile_boards:bpy.data.objects.remove(ob,do_unlink=True)
    # Save a true pre-bake comparison scene: original 4K color/ORM/height
    # fields replace baked maps on the identical assembled source geometry.
    for mat in bpy.data.materials:
        if mat.name not in ('Asphalt','Concrete','Lawn','GroundTrim','GroundFoliage','GroundIron'):continue
        nt=mat.node_tree
        for node in nt.nodes:
            if node.type=='TEX_IMAGE' and node.image:
                channel=next((c for c in ('BaseColor','Normal','ORM') if c in node.image.name),None)
                if channel is None:continue
                trim=mat.name in ('GroundTrim','GroundFoliage','GroundIron')
                if not trim and channel=='Normal':continue
                base=Path('textures/bake') if trim else Path('build/procedural')
                im=bpy.data.images.load(str((base/f'T_{"GroundTrim" if trim else mat.name}_{channel}.png').resolve()),check_existing=True)
                im.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color';node.image=im
        if mat.name not in ('GroundTrim','GroundFoliage','GroundIron'):
            src=nt.nodes.new('ShaderNodeTexImage');src.image=bpy.data.images.load(str((Path('build/procedural')/f'T_{mat.name}_Height.png').resolve()),check_existing=True);src.image.colorspace_settings.name='Non-Color';src.extension='REPEAT'
            bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.004
            nt.links.new(src.outputs['Color'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED').inputs['Normal'])
    bpy.context.scene['ground_source_stage']='original periodic fields before flat baking'
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/lookdev-assembly.blend').resolve()))
    report=dict(source=str(a.source),source_sha256=hashlib.sha256(a.source.read_bytes()).hexdigest(),placements=placements,weather=weather)
    Path('build/assembly.json').write_text(json.dumps(report,indent=2))
    print('ASSEMBLED',len(placements),'modules',len(weather),'placed weather treatments')

if __name__=='__main__':main()
