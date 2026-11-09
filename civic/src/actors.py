"""Native vehicle factory uniforms; same three baked images, no new car mesh."""
import json
import bpy
CACHE={}


def finish(rt,preset='Atlantic',police=False):
    for ob in rt.children_recursive:
        if ob.type!='MESH':continue
        # Object-level slots allow linked geometry and different factory colors.
        for slot in ob.material_slots:
            original=slot.material
            if not original or not original.use_nodes:continue
            if original.get('lamp_strength'):
                bs=next(n for n in original.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
                bs.inputs['Emission Strength'].default_value=0
                continue
            if original.get('paint_decode')!='reference_plus_coverage_delta':continue
            key=(original.name,preset)
            if key not in CACHE:
                ma=original.copy();ma.name=original.name+' / Civic '+preset
                nt=ma.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
                tx=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
                colors=json.loads(ma['paint_colors']);color=colors[preset];ref=list(ma['paint_reference_color'])
                delta=nt.nodes.new('ShaderNodeVectorMath');delta.operation='SCALE';delta.inputs[0].default_value=tuple(a-b for a,b in zip(color,ref));nt.links.new(tx.outputs['Alpha'],delta.inputs['Scale'])
                add=nt.nodes.new('ShaderNodeVectorMath');add.operation='ADD';nt.links.new(tx.outputs['Color'],add.inputs[0]);nt.links.new(delta.outputs[0],add.inputs[1]);nt.links.new(add.outputs[0],bs.inputs['Base Color'])
                CACHE[key]=ma
            slot.link='OBJECT';slot.material=CACHE[key]
    rt['factory_paint']=preset;rt['police_presentation']=police
    if police:
        # Fictional municipal fleet upfit, separate from the native sedan.
        from geo import Assembly,text
        a=Assembly(rt.name+'_FleetUpfit');a.root.parent=rt
        m=a.mesh('RoofBeaconBar',kind='PatrolLightbar',trim_strip=2)
        m.box((0,-.10,1.52),(1.05,.26,.10),'Trim',(.055,.060,.052))
        for s,c in [(-1,(.36,.012,.008)),(1,(.008,.035,.30))]:m.box((s*.28,-.10,1.60),(.43,.23,.075),'Trim',c)
        for x in (-.4,.4):m.box((x,-.10,1.44),(.045,.18,.12),'Trim',(.055,.060,.052))
        m.finish()
