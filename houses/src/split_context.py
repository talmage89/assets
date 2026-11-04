"""Read-only accepted type context, with source fallback on a cold clone."""
from pathlib import Path
import bpy
from build import build,save
from plan import generate


def ensure(force_source=False):
    paths={}
    for kind,seed,stem in [('cape',36,'HearthfieldCape'),('ranch',12,'HearthfieldRanch'),('builder_colonial',27,'Hearthfield')]:
        exported=Path(f'export/{stem}-{seed}.gltf')
        if exported.exists() and not force_source:paths[kind]=exported;continue
        folder=Path('build/split/context');folder.mkdir(parents=True,exist_ok=True)
        form=folder/f'{kind}-form.blend';source=folder/f'{kind}.blend'
        if not source.exists():
            bpy.ops.wm.read_factory_settings(use_empty=True);save(build(generate(seed,house_type=kind)),form,export=False)
            if kind=='cape':from cape_lookdev import prepare
            elif kind=='ranch':from ranch_lookdev import prepare
            else:from lookdev import prepare
            prepare(form,source)
        paths[kind]=source
    return paths
