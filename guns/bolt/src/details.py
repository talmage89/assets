"""Supplemental final GLB views of engraving and the bag-contact paint."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
from guns.common.render import main
import final_shots as shots,interface
shots.SHOTS={**shots.SHOTS,
 'receiver_markings':dict(location=(-.30,.10,.14),target=(0,.125,.068),lens=80,aspect=1.8,action='Idle',frame=0,exposure=-.15),
 'forend_wear':dict(location=(.30,.42,-.18),target=(0,.33,.025),lens=72,aspect=1.6,action='Idle',frame=0,exposure=-.15,under_light=True)}
if __name__=='__main__':main(shots,interface)
