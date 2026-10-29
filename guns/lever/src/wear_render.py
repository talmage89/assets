"""Export-only close views of both band rims, using the common final studio."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from guns.common.render import main
import final_shots,interface
from shots import shot
final_shots.SHOTS={**final_shots.SHOTS,
 'forend_band':shot((.15,.51,.105),(0,.432,.027),75,1.5,
                    action='Idle',frame=0,exposure=-.15,background='transparent'),
 'muzzle_band':shot((.14,.73,.09),(0,.667,.035),85,1.5,
                    action='Idle',frame=0,exposure=-.15,background='transparent')}
final_shots.DEFAULT_SHOTS='forend_band,muzzle_band'
if __name__=='__main__':main(final_shots,interface)
