"""Hash a stock external glTF bundle without Blender or optional libraries."""
import hashlib
import json
from pathlib import Path


def dependencies(path):
    d=json.loads(path.read_text())
    return [path]+[path.parent/b['uri'] for b in d['buffers']]+[path.parent/i['uri'] for i in d['images']]


def bundle_hash(path):
    h=hashlib.sha256()
    for p in dependencies(path):h.update(p.name.encode());h.update(p.read_bytes())
    return h.hexdigest()

