"""Reuse the accepted garden July albedo recipe without changing Ground."""
import importlib.util
from pathlib import Path


def maps():
    root=Path(__file__).resolve().parents[2]
    spec=importlib.util.spec_from_file_location('_garden_turf_recipe',root/'community-garden/src/groundcover.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    source=root if (root/'ground/textures/ship/T_Lawn_BaseColor.png').is_file() else root/'trailer-park/build/library'
    module.maps(source,'textures/ship')


if __name__=='__main__':maps()
