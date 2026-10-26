"""Measure the finalized geometry and the retained spring pixels, not constants."""
import argparse,json,math,sys
from pathlib import Path
import bpy,numpy as np
from PIL import Image
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--tile',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
def points(prefix):return [o.matrix_world@v.co for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(prefix) for v in o.data.vertices]
legs=points('W leg ');floor=min(v.z for v in legs)
outer=max(math.hypot(v.x,v.y) for v in points('Twelve section galvanized hoop'))
spring_z=sum(v.z for v in points('Spring coil alpha')[:4])/4
frame_mid=[v for v in points('Twelve section galvanized hoop') if abs(v.z-spring_z)<1e-5]
frame_inner=min(math.hypot(v.x,v.y) for v in frame_mid)
mat_edge=max(math.hypot(v.x,v.y) for v in points('Sewn mat perimeter webbing'))
o=bpy.data.objects['Spring coil alpha'];vs=[o.matrix_world@v.co for v in o.data.vertices[:4]]
start=(vs[0]+vs[3])/2;end=(vs[1]+vs[2])/2;start_r=math.hypot(start.x,start.y);length=(end-start).length
image=np.asarray(Image.open(a.tile).convert('RGBA'));alpha=image[1024-80:1024-16,560:816,3];xx=np.where((alpha>=128).any(axis=0))[0]
retained=(start_r+(xx[0]+.5)/256*length,start_r+(xx[-1]+.5)/256*length)
errors=[]
if abs(floor)>1e-6:errors.append('W brace does not meet ground')
if abs(2*outer-4.2672)>1e-5:errors.append('Frame outside 14 ft diameter')
if retained[0]>mat_edge:errors.append('Retained mat hook pixels do not reach webbing')
if retained[1]<frame_inner:errors.append('Retained outer hook pixels do not reach frame')
report=dict(passed=not errors,ground_min_z_m=floor,measured_frame_diameter_m=2*outer,mat_webbing_outer_radius_m=mat_edge,frame_inner_radius_at_spring_height_m=frame_inner,retained_spring_alpha_radius_m=retained,mat_ring_overlap_m=mat_edge-retained[0],outer_hook_overlap_m=retained[1]-frame_inner,method='world-space finalized vertices plus retained alpha pixel-center spans; contact sampled for the radial card at angle zero',errors=errors)
Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report));assert not errors,errors
