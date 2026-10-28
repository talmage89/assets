"""Close trigger inspection without changing the accepted final cameras."""
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
import final_shots as shots,interface
from guns.common.render import main
shots.SHOTS.update({
 'trigger_right':dict(location=(.40,.026,.005),target=(0,.026,.005),ortho=.062,aspect=1.25,background='transparent',exposure=-.15,action='Idle',frame=0),
 'trigger_quarter':dict(location=(.30,.18,.075),target=(0,.026,.005),lens=100,aspect=1.25,background='transparent',exposure=-.15,action='Idle',frame=0),
 'trigger_pulled':dict(location=(.40,.026,.005),target=(0,.026,.005),ortho=.062,aspect=1.25,background='transparent',exposure=-.15,action='Fire',frame=3),
})
if __name__=='__main__':main(shots,interface)
