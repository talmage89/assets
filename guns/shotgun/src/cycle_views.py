"""Close action presentation; exported geometry and textures only."""
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from guns.common.feed_views import main
import interface,final_shots
if __name__=='__main__':
    main(BASE,interface,final_shots,
         dict(location=(.46,.12,.19),target=(0,.20,.032),lens=60,aspect=1.8,exposure=-.15),
         ['Receiver','Magazine_Tube','Barrel','Bolt_Body','Bolt_Face','Bolt_PortCheek','Forend_Wood','Forend_Sleeve'])
