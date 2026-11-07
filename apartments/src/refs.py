"""Reproducible reference crops, inspection only, never material inputs."""
import json
import subprocess
from pathlib import Path
from PIL import Image
refs=Path('refs')
subprocess.run(['pdftoppm','-f','113','-singlefile','-scale-to','1800','-jpeg',str(refs/'mansard.pdf'),str(refs/'mansard-page')],check=True)
Image.open(refs/'mansard-page.jpg').crop((46,312,936,677)).save(refs/'mansard-1978.jpg',quality=95)
Image.open(refs/'mansard-page.jpg').crop((46,773,765,1258)).save(refs/'gallery-1972.jpg',quality=95)
(refs/'crop-metadata.json').write_text(json.dumps(dict(source='mansard.pdf',page_one_based=113,raster_long_side=1800,crops={'mansard-1978.jpg':[46,312,936,677],'gallery-1972.jpg':[46,773,765,1258]}),indent=2))
