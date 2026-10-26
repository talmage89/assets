"""Extract original product photographs locally; never feed them into Blender."""
from pathlib import Path
import subprocess
from PIL import Image
root=Path(__file__).resolve().parents[1];folder=root/'refs'
subprocess.run(['pdfimages','-f','2','-l','2','-j',str(folder/'foxhill.pdf'),str(folder/'foxhill-photo')],check=True)
Image.open(folder/'foxhill-photo-012.ppm').save(folder/'chaise-reference.jpg')
