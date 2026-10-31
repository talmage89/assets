"""Covey atlas, isolated field-finish projection and accepted named rig parts."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
UV_SMART_ANGLE=55
UV_PACK_SHAPE='AABB'
UV_MIN_COVERAGE=.20
UV_PRIORITY={'Action_Body':1.4,'Trigger_Plate':1.4,'Top_Lever':2.1,'Front_Trigger':2.2,'Rear_Trigger':2.2,'Tang_Safety':9.0,
 'Stock_Walnut':1.1,'Forend_Walnut':3.5,'Barrel_':.8,
 'Live':2.0,'Hull':2.0,'Insert':2.0}
# Base contact-AO policy. bake_form.py derives an isolated projection root
# for every actual named part, independent of the animation's rigid owners.
BAKE_POLICY=dict(isolate_rigid_bones=True,consolidate_attribute_sources=True,
 cage_m=.0007,ray_distance_m=.003,ao_distance_m=.008,material_ao_channel="micro_ao")

MATERIAL_OVERRIDES={"":dict(specular=.45)}
OPAQUE_SPECULAR_FROM_BASECOLOR_ALPHA=True
