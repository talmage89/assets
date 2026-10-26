"""Create a minimal asset folder without replacing any existing files.

python3 kit/new_asset.py <folder-name> --name <PascalCaseName>
New assets start in checkpoint mode; opt into FINAL_PIPELINE after look-dev review.
"""
import argparse,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('--name',required=True);a=p.parse_args()
if not re.fullmatch('[a-z][a-z0-9-]*',a.folder) or not re.fullmatch('[A-Z][A-Za-z0-9]*',a.name):p.error('Use a folder-name and PascalCase asset name')
root=Path(__file__).resolve().parents[1];dest=root/a.folder
if dest.exists():p.error('Folder already exists')
for d in ('src','refs','docs'):(dest/d).mkdir(parents=True,exist_ok=True)
(dest/'Makefile').write_text(f'ASSET := {a.name}\ninclude ../kit/rules.mk\n')
(dest/'README.md').write_text(f'# {a.name}\n\nModeling checkpoint in progress. Research and cite real dimensions before modeling.\n')
(dest/'refs/SOURCES.md').write_text('# Reference sources\n\n| Local file | URL | Author / license | Used for |\n| --- | --- | --- | --- |\n')
(dest/'src/markings.py').write_text('"""No generated markings required yet."""\n')
(dest/'src/config.py').write_text("BUDGETS={'Main':5000}\nBOUNDS={'Main':{'size':(1,1,1),'tolerance':(.01,.01,.01)}}\nSHOTS={}  # Add measured framing for this asset.\n")
(dest/'src/build.py').write_text('"""Implement a measured, original parametric asset here."""\nraise RuntimeError("Research and implement this asset before building")\n')
print('Created',dest)
