"""Construction checkpoint only. Delivery textures remain intentionally gated."""
TITLE='Hearthfield / seeded builder colonial'
import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plan import load
p=load(int(os.environ.get('HOUSE_SEED','27')),Path(os.environ['HOUSE_PLAN']) if os.environ.get('HOUSE_PLAN') else None)
service=[0,100] if p['spec']['garage']['side']=='right' else [-100,0]
MOTIONS=[dict(node='FrontDoor',axis='Z',range=[0,105],step=3,tolerance_m=.0005),
    dict(node='ServiceDoor',axis='Z',range=service,step=5,tolerance_m=.0005),
    dict(node='PatioDoor',axis='X',kind='translation',range=[0,.8382],step=.04,tolerance_m=.0005)]
