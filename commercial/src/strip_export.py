"""Delivery-only consolidation; editable module source remains untouched."""
import bpy
from mathutils import Matrix
from geometry import root

BUILDING=('Bay_','EndCap_','Tower_','Elbow','RoofLadder','MeterBank')


def consolidate(world):
    groups={'BuildingStatic':[],'SiteSurfaceStatic':[]}
    for ob in sorted(bpy.context.scene.objects,key=lambda o:o.name):
        if ob.type!='MESH' or ob.name.startswith('StripBoxwood_'):continue
        owner=ob.parent;moving=False;building=False;surface=False
        while owner and owner!=world:
            moving|=bool(owner.get('pivot_axis'));building|=owner.name.startswith(BUILDING);surface|=owner.name.startswith(('SitePaving','ServiceWear'));owner=owner.parent
        if not moving and (building or surface):groups['BuildingStatic' if building else 'SiteSurfaceStatic'].append(ob)
    for name,obs in groups.items():
        if not obs:continue
        parent=root(name,kind=name,parent=world)
        bpy.context.view_layer.update()
        for ob in obs:
            xf=parent.matrix_world.inverted()@ob.matrix_world;ob.data.transform(xf);ob.parent=parent;ob.matrix_basis=Matrix.Identity(4);ob.matrix_parent_inverse=Matrix.Identity(4)
        bpy.ops.object.select_all(action='DESELECT')
        for ob in obs:ob.select_set(True)
        bpy.context.view_layer.objects.active=obs[0]
        bpy.ops.object.join();ob=bpy.context.object;ob.name=name+'__Mesh'
        # One slot per actual material, including slots inherited by joins.
        slots=[];mapping={}
        for i,ma in enumerate(ob.data.materials):
            if ma not in slots:slots.append(ma)
            mapping[i]=slots.index(ma)
        indices=[mapping[f.material_index] for f in ob.data.polygons]
        ob.data.materials.clear()
        for ma in slots:ob.data.materials.append(ma)
        for f,i in zip(ob.data.polygons,indices):f.material_index=i
