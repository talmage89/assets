"""Registered image/PDF inputs only; never executes anything retrieved.

Use the kit fetcher first. curl is a system TLS/CDN fallback for servers that
reject urllib. Validate the bytes in memory before writing a reference file.
"""
import io,subprocess,sys,urllib.error
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fetch_refs import fetch
count=0
for folder in (Path('refs'),ROOT/'street-signs/refs'):
    for line in (folder/'SOURCES.md').read_text().splitlines():
        cells=[s.strip() for s in line.split('|')]
        if len(cells)<4 or not cells[2].startswith('https://'):continue
        name,url=cells[1:3];path=folder/name
        assert path.name==name and path.suffix.lower() in ('.pdf','.jpg','.jpeg','.png','.webp')
        if not path.exists():
            try:fetch(folder,[name])
            except (urllib.error.URLError,TimeoutError):
                data=subprocess.check_output(['curl','--fail','--location','--retry','2','--max-time','90',url])
                if path.suffix.lower()=='.pdf':assert data.startswith(b'%PDF-'),name
                else:Image.open(io.BytesIO(data)).verify()
                path.write_bytes(data);print('FETCHED',name,len(data))
        if path.suffix.lower()=='.pdf':assert path.read_bytes().startswith(b'%PDF-'),name
        else:
            with Image.open(path) as image:image.verify()
        count+=1
print('REGISTERED REFERENCES',count,'ready; all URLs/authors/licenses in SOURCES.md')
