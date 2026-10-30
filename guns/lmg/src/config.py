"""Canonical one-set PBR bake; individual projection owners retain thin walls."""
BAKE_BASECOLOR_ALPHA_CHANNEL='specular_factor'
BAKE_POLICY=dict(isolate_rigid_bones=True,consolidate_attribute_sources=True,
                 isolate_moving=True,moving_roots=['Handguard_Sculpt','HeatShield',
                  *['Handguard_MoldRib_'+str(s)+'_'+str(z) for s in (-1,1) for z in (52,66,80)]],
                 cage_m=.0007,ray_distance_m=.004,ao_distance_m=.008,
                 material_ao_channel='micro_ao')
