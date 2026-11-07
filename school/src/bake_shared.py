"""Selective reuse of the houses' original buff-brick bake, no new artwork."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from kit.flat_bake import bake
rows=json.loads(Path('build/ranch/delivery/fields.json').read_text())
for name in ('RanchBrick_buff','RanchBrick_tan'):
    if all((Path('textures/ranch-bake')/f'T_{name}_{channel}.png').exists() for channel in ('BaseColor','Normal','ORM')):continue
    row=rows[name]
    bake(Path('build/ranch/delivery/procedural'),Path('textures/ranch-bake'),name,row['coverage_m'][0],4096,8,row['height_distance_m'])
