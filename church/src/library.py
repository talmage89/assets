"""Read-only native deliveries; instance meshes and retain alpha/PBR maps."""
from pathlib import Path
import bpy
import geometry as G
CACHE={}


def instance(path,name,point,yaw=0,scale=1,kind=None,actor='town'):
    path=Path(path).resolve();key=(str(path),kind)
    if key not in CACHE:
        before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path));obs=set(bpy.context.scene.objects)-before
        roots=[o for o in obs if o.parent not in obs]
        if kind:
            selected=[o for o in obs if o.name==kind or o.name.startswith(kind+'.')]
            if len(selected)!=1:raise ValueError((path,kind,[o.name for o in roots]))
            chosen=set([selected[0],*selected[0].children_recursive])
            for ob in reversed(list(obs-chosen)):bpy.data.objects.remove(ob,do_unlink=True)
            roots=[selected[0]]
            selected[0].location=(0,0,0);selected[0].rotation_euler=(0,0,0)
        if actor=='town':
            # Distant town only: simplify local copies, never library payloads.
            for ob in obs:
                if ob.name not in bpy.data.objects or ob.type!='MESH':continue
                if len(ob.data.polygons)<400:continue
                modifier=ob.modifiers.new('Church distant context reduction','DECIMATE');modifier.ratio=.13
                bpy.context.view_layer.objects.active=ob
                bpy.ops.object.modifier_apply(modifier=modifier.name)
        rt=G.root('Template_'+name)
        for ob in roots:ob.parent=rt
        CACHE[key]=rt
    rt=G.clone(CACHE[key],name,point,yaw);rt.scale=(scale,)*3;rt['actor_kind']=actor
    return rt


def clear():
    for rt in CACHE.values():
        for ob in reversed([rt,*rt.children_recursive]):bpy.data.objects.remove(ob,do_unlink=True)
    CACHE.clear()


def car(i,point,yaw=0):
    key=('AlderH120','AlderC150','AlderX220')[i%3]
    rt=instance(G.ROOT/f'cars/export/{key}.glb','Parked_'+str(i),point,yaw,actor='car')
    colors=((.30,.31,.30),(.06,.075,.080),(.19,.024,.016),(.015,.055,.075),(.47,.43,.34),(.48,.48,.43))
    for ob in rt.children_recursive:
        if ob.type!='MESH':continue
        for slot in ob.material_slots:
            ma=slot.material
            if not ma or not ma.use_nodes:continue
            bs=ma.node_tree.nodes.get('Principled BSDF')
            if not bs:continue
            if 'lamp' in ma.name.lower():bs.inputs['Emission Strength'].default_value=0
            if 'paint' in ma.name.lower():
                name='SundayPaint_'+key+'_'+str(i%6);cp=bpy.data.materials.get(name)
                if cp is None:
                    cp=ma.copy();cp.name=name;p=cp.node_tree.nodes.get('Principled BSDF')
                    for link in list(p.inputs['Base Color'].links):cp.node_tree.links.remove(link)
                    p.inputs['Base Color'].default_value=(*colors[i%6],1)
                slot.link='OBJECT';slot.material=cp
    return rt
