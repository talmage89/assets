"""In-service cloth comparison; frame class assumed, no photographic tracing."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
MATCHES={'match_used':dict(title='In-service trampoline / sewn padding and hanging enclosure',photo=str(R/'refs/enclosure.jpg'),crop=(80,50,910,820),location=(0,-7.6,5.6),target=(0,0,1.2),lens=50,background='transparent',landmarks=[
 dict(world=(0,-2.14,.93),pixel=(520,734)),dict(world=(0,2.14,.93),pixel=(512,307)),
 dict(world=(-2.14,0,.93),pixel=(184,520)),dict(world=(2.14,0,.93),pixel=(854,513)),
 dict(world=(0,1.919,2.64),pixel=(509,95)),
])}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--credit-dir',required=True);d=Path(p.parse_args().credit_dir);d.mkdir(parents=True,exist_ok=True)
 (d/'REFERENCE-CREDIT.txt').write_text('Reference photo: Nayand, Trampoline with enclosure, 19 October 2011.\nhttps://commons.wikimedia.org/wiki/File:Trampoline_with_enclosure.jpg\nCC BY-SA 3.0, https://creativecommons.org/licenses/by-sa/3.0/\nChanges: crop, resize and comparison captions. Photographic composites retain CC BY-SA 3.0.\nNo reference pixels enter the model, maps or committed docs.\n')
