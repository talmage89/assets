"""Fetch only listed image/PDF reference files. Never executes remote content."""
import sys,urllib.request
from pathlib import Path

def fetch(folder):
    folder=Path(folder)
    for line in (folder/'SOURCES.md').read_text().splitlines():
        cells=[s.strip() for s in line.split('|')]
        if len(cells)<4 or not cells[2].startswith('https://'):continue
        name,url=cells[1:3];path=folder/name
        if path.name!=name or path.suffix.lower() not in {'.pdf','.jpg','.jpeg','.png'}:raise ValueError(name)
        if path.exists():continue
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:
            mime=r.headers.get('Content-Type','')
            if 'pdf' not in mime and not mime.startswith('image/'):raise ValueError('Reference is not image/PDF: '+url)
            data=r.read()
        path.write_bytes(data);print('Fetched',name,len(data))

if __name__=='__main__':fetch(sys.argv[1])
