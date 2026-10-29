"""Round-four form bake: inspection constants, preserved named diagnostics.

The normal bake judges the exported form; finish/checkering/wear remain held.
Named rigid parts remain at this review gate for independent surface tests.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
UV_SMART_ANGLE=30
UV_PACK_SHAPE='AABB'
UV_MIN_COVERAGE=.20
UV_PRIORITY={'Action_Body':1.4,'Trigger_Plate':1.4,'Top_Lever':1.25,
 'Stock_Walnut':1.1,'Forend_Walnut':1.2,'Barrel_':.8,
 'Live':.5,'Hull':.5,'Insert':.5}
# Base contact-AO policy. bake_form.py derives an isolated projection root
# for every actual named part, independent of the animation's rigid owners.
BAKE_POLICY=dict(isolate_rigid_bones=True,consolidate_attribute_sources=True,
 cage_m=.0007,ray_distance_m=.003,ao_distance_m=.008)
