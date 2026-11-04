"""Disposable evaluated original parent for detail sampling; never exported."""
import bpy
from hatch_body import master
from hatch_fairness import smooth_parent_field
_parent=None
_field=None


def field():
    global _parent,_field
    if _field is None:
        _parent,_=master(1)
        _field=smooth_parent_field(_parent)
    return _field


def cleanup():
    global _parent,_field
    if _parent is not None:bpy.data.objects.remove(_parent,do_unlink=True)
    _parent=None;_field=None
