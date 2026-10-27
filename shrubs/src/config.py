"""One stock glTF library, two independent rooted specimens, one image set."""
BUDGETS={'Boxwood':6000,'Hydrangea':6000}
ATLAS_SETS=tuple(BUDGETS)
BOUNDS={'Boxwood':dict(size=(1.0,1.0,.9),tolerance=(.15,.15,.12)), 'Hydrangea':dict(size=(1.4,1.4,1.2),tolerance=(.22,.22,.15))}
EXPORT_COLOR_DATA={'Wind':'_WIND'}
TILED_MESHES={
 'Boxwood leaf cards':dict(rect=(0,0,1,.5),alpha_cutoff=.45,double_sided=True,preserve_normals=True,density_min=3000,density_max=5500),
 'Hydrangea leaf and flower cards':dict(rect=(.25,.5,1,1),alpha_cutoff=.45,double_sided=True,preserve_normals=True,density_min=900,density_max=8000),
}
UV_ATLAS_RECT=(.012,.565,.238,.988)
UV_MIN_COVERAGE=.025
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=100,median_min=300,median_max=3000,p95_max=6000)
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Boxwood','Hydrangea'],cage_m=.0007,ray_distance_m=.003,ao_distance_m=.015)
MATERIAL_OVERRIDES={'':dict(specular=.12)}
MAX_MATERIALS=2
SHOTS={}
MOTIONS=[]

UV_UNWRAP_METHOD="ANGLE_BASED"
UV_USE_TARGET_ASPECT=True
UV_NORMALIZE_ISLAND_SCALE=True
