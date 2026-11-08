"""Image/PDF-only curl fetch, with a verified signature before accepting bytes."""
import subprocess
from pathlib import Path
from PIL import Image


def main():
    folder=Path('refs')
    for line in (folder/'SOURCES.md').read_text().splitlines():
        cells=[c.strip() for c in line.split('|')]
        if len(cells)<4 or not cells[2].startswith('https://'):continue
        name,url=cells[1:3];dest=folder/name
        if name!=dest.name or dest.suffix.lower() not in ('.jpg','.png','.pdf'):raise ValueError(name)
        if dest.exists():continue
        subprocess.run(['curl','-fL','--retry','2','--max-time','60','-A','Mozilla/5.0',url,'-o',str(dest)],check=True)
        if dest.suffix=='.pdf':
            if not dest.read_bytes().startswith(b'%PDF-'):dest.unlink();raise ValueError('Not PDF: '+name)
        else:
            with Image.open(dest) as im:im.verify()
        print('REFERENCE',name,dest.stat().st_size)


if __name__=='__main__':main()
