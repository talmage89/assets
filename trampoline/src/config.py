from pathlib import Path
import runpy
v=runpy.run_path(str(Path(__file__).with_name('views.py')));SHOTS=v['SHOTS'];STUDIO=v['STUDIO'];TITLE=v['TITLE'];EXTRA_SHOTS=v['EXTRA_SHOTS']
BUDGETS={'Trampoline':8000}
BOUNDS={'Trampoline':dict(size=(4.3612,4.2912,2.69),tolerance=(.005,.005,.002))}
DELIVERY_BOUNDS=BOUNDS['Trampoline']
TILED_MESHES={
 'Enclosure net alpha':dict(rect=(16/1024,16/1024,272/1024,272/1024),alpha_cutoff=.4,alpha_mode='BLEND',double_sided=True,density_min=870,density_max=1150),
 'Jump mat alpha':dict(rect=(288/1024,16/1024,544/1024,272/1024),alpha_cutoff=.4,alpha_mode='BLEND',double_sided=True,density_min=980,density_max=1020),
 'Spring coil alpha':dict(rect=(560/1024,16/1024,816/1024,80/1024),alpha_cutoff=.4,alpha_mode='BLEND',double_sided=True,density_min=1500,density_max=1800),
}
TILED_MESHES['FabricAssembly']=dict(rect=(16/1024,16/1024,816/1024,272/1024),alpha_mode='BLEND',alpha_cutoff=.4,double_sided=True,density_min=980,density_max=1800)
UV_ATLAS_RECT=(.01,.32,.99,.99)
UV_DENSITY_BANDS=dict(reference_size=1024,p5_min=65,median_min=150,median_max=500,p95_max=900)
UV_SMART_ASPECT=False
UV_SMART_ANGLE=66
UV_PRIORITY={'Sewn safety pad':1.6,'W leg':.60,'Leg extension':.70,'Enclosure pole':.65,'Pole foam':.9,'Twelve section':.8,'Net ': .4,'Entry zipper':1.6,'Pad radial':.4,'Pad underside':.5,'Sewn mat perimeter':.6}
# Unique geometry plus explicitly occupied repeating tiles fill ~38% of the map.
UV_MIN_COVERAGE=.23
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['ZipSlider'],cage_m=.0006,ray_distance_m=.004,ao_distance_m=.03)
REQUIRED_NODES=('ZipSlider',)
MOTIONS=[dict(node='ZipSlider',axis='Z',kind='translation',range=[-1.28,0],step=.04,tolerance_m=.0003,allow=[dict(moving='Zipper slider',fixed='Entry zipper teeth',reason='Slider embraces the toothed track')])]
CONTACTS=[('Leg socket 0 -1','Leg extension 0 L',.0002),('Twelve section galvanized hoop 10','Leg socket 0 -1',.0002),('Enclosure pole 0','Pole clamp 0',.0002),('Net pole top attachment 0','Pole upper cap 0',.004)]
