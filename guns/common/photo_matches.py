"""Shared measured-landmark units and calibrated camera/pose configuration.

Each gun owns its photographic landmarks and action selection. Photographs
are read only by the comparison pipeline, never by geometry or material code.
"""
import json
from pathlib import Path

def L(world_mm,pixel,weight=1):
 return dict(world=tuple(x*.001 for x in world_mm),pixel=pixel,weight=weight)

def camera_shots(path):
 return {name:dict(row['shot'],background='transparent',
         aspect=(row['crop'][2]-row['crop'][0])/(row['crop'][3]-row['crop'][1]))
         for name,row in json.loads(Path(path).read_text()).items()}
