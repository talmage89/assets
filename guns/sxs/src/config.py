"""Covey atlas, isolated field-finish projection and accepted named rig parts."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
UV_SMART_ANGLE=30
UV_PACK_SHAPE='AABB'
UV_MIN_COVERAGE=.20
UV_PRIORITY={'Action_Body':1.4,'Trigger_Plate':1.4,'Top_Lever':1.6,'Tang_Safety':3.0,
 'Stock_Walnut':1.1,'Forend_Walnut':2.1,'Barrel_':.8,
 'Live':1.2,'Hull':1.2,'Insert':1.2}
# Base contact-AO policy. bake_form.py derives an isolated projection root
# for every actual named part, independent of the animation's rigid owners.
BAKE_POLICY=dict(isolate_rigid_bones=True,consolidate_attribute_sources=True,
 cage_m=.0007,ray_distance_m=.003,ao_distance_m=.008,material_ao_channel="micro_ao")

MATERIAL_OVERRIDES={"":dict(specular=.33)}