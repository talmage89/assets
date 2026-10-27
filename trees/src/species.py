"""Explicit species namespaces. No process-global species switching."""
from types import SimpleNamespace
import maple

def namespace(module):
    return SimpleNamespace(**{k:v for k,v in vars(module).items() if k.isupper()})

MAPLE=namespace(maple)

def get(name="maple"):
    if name=="maple":return MAPLE
    if name=="oak":
        import oak
        return namespace(oak)
    raise ValueError("Unknown tree species: "+name)
