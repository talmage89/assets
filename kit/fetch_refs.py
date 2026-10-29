"""Fetch only listed image/PDF reference files. Never executes remote content."""
import sys,urllib.request
from pathlib import Path

def fetch(folder,names=None):
    folder=Path(folder)
    entries=[]
    for line in (folder/'SOURCES.md').read_text().splitlines():
        cells=[s.strip() for s in line.split('|')]
        if len(cells)<4 or not cells[2].startswith('https://'):continue
        entries.append(cells[1:3])
    requested=set(names) if names is not None else None
    if requested is not None:
        unknown=requested-{name for name,url in entries}
        if unknown:raise ValueError('Unregistered references: '+', '.join(sorted(unknown)))
    for name,url in entries:
        if requested is not None and name not in requested:continue
        path=folder/name
        if path.name!=name or path.suffix.lower() not in {'.pdf','.jpg','.jpeg','.png','.webp'}:raise ValueError(name)
        if path.exists():continue
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:
            mime=r.headers.get('Content-Type','')
            if 'pdf' not in mime and not mime.startswith('image/'):raise ValueError('Reference is not image/PDF: '+url)
            data=r.read()
        path.write_bytes(data);print('Fetched',name,len(data))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('--only',nargs='+')
    a=p.parse_args();fetch(a.folder,a.only)
