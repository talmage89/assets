from pathlib import Path
P=Path(__file__).resolve().parents[1];y=-1.760;z=7.7722
# Drawing dimensions set the envelope. Pixel anchors are measured on the photo;
# the authored reflector layout and bolts intentionally differ.
MATCHES={'fixture':dict(photo=str(P/'refs/product.png'),crop=(0,0,987,503),title='Compact cobra / casting, optics and control comparison',location=(1.1,-2.1,7.73),target=(0,-2.01,7.84),lens=70,emission_scale=0,background='transparent',isolate=['Die-cast','Driver','Folded','LED','Tempered','Cast heat','Photocell','Tray','Slipfitter'],landmarks=[dict(world=w,pixel=p) for w,p in [((.06078,y-.489,z+.007),(27,436)),((.0455,y,z+.007),(981,435)),((.0455,y,z+.095),(935,226)),((.061,y-.18,z+.108),(556,199)),((.07602,y-.465,z+.051),(71,307))]])}
