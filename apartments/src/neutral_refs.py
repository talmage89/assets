"""Disclosed assumed-neutral white balance for reference comparisons only."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
rows={
 'garden-2004':dict(file='garden-2004.jpg',roi=(408,155,420,164),neutral='sunlit white replacement window sash'),
 'mansard-1978':dict(file='mansard-1978.jpg',roi=(381,72,437,78),neutral='light painted flat roof edge, assumed neutral'),
 'townhouses':dict(file='townhouses.jpg',roi=(679,774,704,799),neutral='white garage door panel')}
def linear(c):return np.where(c<=.04045,c/12.92,((c+.055)/1.055)**2.4)
def srgb(c):return np.where(c<=.0031308,c*12.92,1.055*np.maximum(c,0)**(1/2.4)-.055)
for k,row in rows.items():
 p=Path('refs')/row['file'];rgb=np.array(Image.open(p).convert('RGB'))/255
 a,b,c,d=row['roi'];neutral=linear(rgb[b:d,a:c]).mean((0,1));gain=neutral.mean()/neutral
 # Assumed neutrals preserve average linear exposure; no shadow lifting.
 Image.fromarray(np.round(np.clip(srgb(linear(rgb)*gain),0,1)*255).astype('uint8')).save(Path('refs')/(k+'-balanced.jpg'),quality=97)
 row['linear_gain']=gain.tolist();row['linear_neutral_mean']=neutral.tolist()
Path('build/neutral-reference.json').write_text(json.dumps(rows,indent=2))
