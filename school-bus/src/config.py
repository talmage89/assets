"""Checkpoint atlas and construction policy; not a final look-dev acceptance."""
BUDGETS={'SchoolBus':90000}
BOUNDS={'SchoolBus':dict(size=(3.35,12.3005,3.330),tolerance=(.002,.003,.002))}
MAX_MATERIALS=4
SHIP_SIZE=2048
UV_SMART_ASPECT=False
UV_USE_TARGET_ASPECT=True
UV_MIN_COVERAGE=.20
UV_DEFAULT_PRIORITY=.65
UV_PRIORITY={'District lettering':3,'Fleet number':2,'Front school':3,'Rear school':3,'Stop legend':3,
             'Rear emergency label':3,'Side exit label':3,
             'Front fictional':2,'Rear fictional':2,'Glass':.75,'Truck rim':1.1,'Tire':1.0,
             'Lower folded':1.4,'Formed roof':1.1,'Compound hood':1.8,'Front nose':1.5,'Bench':.55}
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=5,median_min=50,median_max=500,p95_max=1800)
DELIVERY_SURFACES={
 'Paint':dict(principled={'Coat Weight':.25,'Coat Roughness':.22},factors={'Metallic':0},normal_strength=.45),
 'Opaque':dict(normal_strength=1),
 'Glass':dict(principled={'Transmission Weight':1,'IOR':1.52},normal_strength=0),
 'Lamps':dict(normal_strength=0,extras={'lamp_lit_strength':12}),
}
SOURCE_MATERIAL_SURFACES={
    **{f'Bus {s}':'Opaque' for s in ['black','frame','aluminum','wheel','vinyl','floor','ceiling','dash','white','red','mirror','tire']},
    'Bus yellow':'Paint','Bus glass':'Glass','Bus windshield':'Glass',
    'Bus tape':'Opaque',
    **{f'Bus {s}':'Lamps' for s in ['amber','warning_red','headlight','dome','strobe']},
    **{f'Bus print {s}':'Opaque' for s in ['school','emergency','maker','stop']+[f'{kind}-{seed}' for seed in [101,102,103] for kind in ['district','fleet','plate']]},
}
EXPORT_VARIANT=101
