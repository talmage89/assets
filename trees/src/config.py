"""Summer maple source and baked-GLB delivery policy."""
BUDGETS={'RedMaple':25000}
BOUNDS={'RedMaple':dict(size=(10.0,9.2,12.4),tolerance=(.35,.55,.4))}
TILED_MESHES={'Summer leaf cards':dict(rect=(0,0,1,.5),alpha_cutoff=.45,double_sided=True,preserve_normals=True,density_min=650,density_max=900)}
SHOTS={}
MOTIONS=[]

EXPORT_COLOR_DATA={'Wind':'_WIND'}
DELIVERY_BOUNDS=BOUNDS['RedMaple']
UV_ATLAS_RECT=(.01,.51,.99,.99)
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=50,median_min=100,median_max=500,p95_max=950)
UV_MIN_COVERAGE=.22
BAKE_POLICY=dict(cage_m=.003,ray_distance_m=.025,ao_distance_m=.035,material_ao_channel='micro_ao')
MATERIAL_OVERRIDES={'Trunk and branches':dict(ior=1.45,specular=.12)}

UV_UNWRAP_METHOD='ANGLE_BASED'
UV_PACK_SHAPE='CONCAVE'
UV_USE_TARGET_ASPECT=True

UV_NORMALIZE_ISLAND_SCALE=True
UV_PRIORITY_ATTRIBUTE='BarkUVPriority'
