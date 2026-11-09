"""Fresh-import measurements for this round's parking and glazing changes."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy


def points(ob,material=None):
    out=[]
    for face in ob.data.polygons:
        if material and material not in ob.data.materials[face.material_index].name:continue
        out.extend(ob.matrix_world@ob.data.vertices[i].co for i in face.vertices)
    return out


def area(ob,material):
    total=0
    for face in ob.data.polygons:
        if material not in ob.data.materials[face.material_index].name:continue
        pp=[ob.matrix_world@ob.data.vertices[i].co for i in face.vertices]
        total+=(pp[1]-pp[0]).cross(pp[2]-pp[0]).length/2
    return total


def main():
    report={}
    for seed in (101,202):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(Path(f'export/ChurchSite-{seed}.gltf').resolve()))
        bpy.context.view_layer.update()
        stops=next(o for o in bpy.context.scene.objects if o.name.startswith('Parking stripes wheel stops'))
        concrete=points(stops,'concrete');stalls=[o for o in bpy.context.scene.objects if o.get('socket_kind')=='parked_car']
        measurements=[]
        for stall in stalls:
            x,y,z=stall.matrix_world.translation;row=int(stall.name.split('_')[1])
            local=[q for q in concrete if abs(q.x-x)<.9 and 1.8<abs(q.y-y)<2.3]
            assert local,('Missing wheel stop',seed,stall.name)
            xx=(min(q.x for q in local)+max(q.x for q in local))/2
            yy=(min(q.y for q in local)+max(q.y for q in local))/2
            assert abs(xx-x)<.001 and abs(abs(yy-y)-2.1)<.001
            assert (yy-y)*(1 if row else -1)>0,('Stop is at aisle end',stall.name)
            measurements.append(dict(stall=stall.name,center_offset_m=[xx-x,yy-y],stop_height_m=max(q.z for q in local)-min(q.z for q in local)))
        depths=[float(o['stall_depth']) for o in stalls]
        south=[o.matrix_world.translation.y for o in stalls if o.name.startswith('Stall_0_')]
        north=[o.matrix_world.translation.y for o in stalls if o.name.startswith('Stall_1_')]
        aisle=min(north)-max(south)-max(depths)
        assert aisle>=7.31,(seed,aisle)
        result=dict(wheel_stops=measurements,clear_aisle_between_stall_envelopes_m=aisle,stalls=len(stalls),occupied=sum(bool(o['occupied']) for o in stalls))
        if seed==202:
            gable=next(o for o in bpy.context.scene.objects if o.name.startswith('Glazed entry gable'))
            glazing=sum(area(o,'Church_glass') for o in gable.children_recursive if o.type=='MESH')
            facets=sum(area(o,'stained_faceted') for o in gable.children_recursive if o.type=='MESH')
            assert glazing>facets*10,(glazing,facets)
            result['gable']=dict(clear_glass_area_m2=glazing,faceted_cross_area_m2=facets,colored_fraction_of_combined_face_area=facets/(facets+glazing),method='Triangle areas on freshly imported glass and faceted-cross primitives, not configured dimensions')
        report[str(seed)]=result
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(Path('export/modules/WallBay.gltf').resolve()))
    pane=next(o for o in bpy.context.scene.objects if '1990s protective glazing' in o.name)
    bars=next(o for o in bpy.context.scene.objects if 'Storm bars vents' in o.name)
    bottom=min(q.z for q in points(pane));below=[q.z for q in points(bars) if q.z<bottom]
    gap=bottom-max(below);assert .0199<gap<.0201,gap
    report['protective_glazing_lower_air_slot_m']=gap
    Path('build/site-check.json').write_text(json.dumps(dict(passed=True,measurements=report),indent=2))
    print('PASS wheel-stop head offsets, measured parking aisles, clear/faceted glass area and 20mm protective-glazing air slot')


if __name__=='__main__':main()
