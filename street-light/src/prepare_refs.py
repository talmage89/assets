"""Reference-only alpha compositing of the publisher's photograph, never a texture."""
from pathlib import Path
from PIL import Image
p=Path('refs');im=Image.open(p/'photo-009.jpg').convert('RGBA');im.putalpha(Image.open(p/'photo-010.jpg').convert('L'));bg=Image.new('RGBA',im.size,(238,239,236,255));bg.alpha_composite(im);bg.convert('RGB').save(p/'product.png')
