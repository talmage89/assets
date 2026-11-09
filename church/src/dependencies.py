"""Validate read-only library inputs and build our private Downtown host."""
import hashlib,json,os,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


def main():
    required=['ground/export/Ground.glb','trees/export/RedMaple.glb','trees/export/PinOak.glb','shrubs/export/Shrubs.glb','houses/export/HearthfieldRanch-11.gltf','houses/export/HearthfieldCape-34.gltf','cars/export/AlderH120.glb','cars/export/AlderC150.glb','cars/export/AlderX220.glb','street-light/export/StreetLight.glb','street-signs/export/StreetSigns.glb']
    required += [f'houses/export/{name}.gltf' for name in ('Hearthfield-2','Hearthfield-6','HearthfieldRanch-14','HearthfieldCape-32')]
    required += ['fences/export/WoodPrivacy.glb']
    missing=[s for s in required if not (ROOT/s).exists()]
    if missing:raise SystemExit('Build these native library dependencies first: '+', '.join(missing))
    host=Path('build/hosts/downtown-opposite.glb');host.parent.mkdir(parents=True,exist_ok=True)
    if not host.exists():
        cached=ROOT/'coffee-shop/build/hosts/downtown-opposite.glb'
        if cached.exists():shutil.copyfile(cached,host)
        else:subprocess.run(['blender','-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(ROOT/'coffee-shop/src/hosts.py'),'--','--kind','downtown-opposite','--out',str(host.resolve())],check=True)
    rows={s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in required}
    recipe=ROOT/'church/src/context_hosts.py'
    if any(not Path(f'build/hosts/town-{i}.glb').exists() or Path(f'build/hosts/town-{i}.glb').stat().st_mtime<recipe.stat().st_mtime for i in range(6)):
        subprocess.run(['blender','-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(ROOT/'church/src/context_hosts.py'),'--','--out',str(host.parent.resolve())],check=True)
    Path('build/dependencies.json').write_text(json.dumps(rows,indent=2))


if __name__=='__main__':main()
