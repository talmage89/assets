"""Use the kit's image/PDF-only fetcher with a named research user agent."""
import sys
import urllib.request
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fetch_refs import fetch

original=urllib.request.urlopen


def named(request,*args,**kwargs):
    if isinstance(request,urllib.request.Request):
        request.add_header('User-Agent','RiverAssetReferenceStudy/1.0 (image and PDF reference research)')
    return original(request,*args,**kwargs)


if __name__=='__main__':
    urllib.request.urlopen=named
    fetch('refs')
