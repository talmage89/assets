"""Five compact final JPGs, after exported-image provenance and review gates."""
import io,json,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import review_sheet
OUT=Path('renders/final');DOCS=Path('docs');stage=OUT/'docs-staging';stage.mkdir(parents=True,exist_ok=True)
assert Path('renders/fixes/crops.json').is_file()
assert len(json.loads((OUT/'provenance.json').read_text()))==31
for state in ('new','season','beat'):
    for name in ('construction','high-check','verify'):
        assert json.loads(Path(f'build/{state}/{name}.json').read_text())['passed'],(state,name)
# The committed review is the human image critique. Numbers alone do not
# certify appearance; these entries document the actual full-size audit.
review=Path('REVIEW.md').read_text()
assert all(f'Delivery pass {i}' in review for i in (1,2,3)),'Full-size delivery critiques are required'
review_sheet([[OUT/s/(k+'.png') for s in ('new','season','beat')] for k in ('hero','hero_bottom')],stage/'ages.jpg',width=1600,title='New / season / beat — baked exported GLBs')
review_sheet([[OUT/'season/grip_macro.png',OUT/'season/grip_edge.png'],[OUT/'season/truck.png',OUT/'season/wheel_bearing.png'],[OUT/'season/tail_plies.png',OUT/'beat/wheel_profile.png']],stage/'details.jpg',width=1600,title='Carbide / filed trim / ground alloy / old urethane / maple')
review_sheet([[OUT/'season/top.png',OUT/'season/bottom.png'],[OUT/'season/side.png',OUT/'season/front.png'],[OUT/'season/scale.png',OUT/'eevee/hero.png']],stage/'inspection.jpg',width=1600,title='Top / bottom / side / front / 1.8 m scale / Eevee')
DOCS.mkdir(exist_ok=True);report={}
for name,source in [('hero',OUT/'season/hero.png'),('ages',stage/'ages.jpg'),('details',stage/'details.jpg'),('inspection',stage/'inspection.jpg'),('graphics',OUT/'graphics-sheet.jpg')]:
    im=Image.open(source).convert('RGB');im.thumbnail((1600,6000),Image.Resampling.LANCZOS)
    for quality in range(94,34,-1):
        data=io.BytesIO();im.save(data,format='JPEG',quality=quality,optimize=True,subsampling=0)
        if len(data.getvalue())<=200000:break
    assert len(data.getvalue())<=200000,name
    target=DOCS/(name+'.jpg');target.write_bytes(data.getvalue())
    report[name]=dict(bytes=target.stat().st_size,size=im.size,quality=quality)
(OUT/'docs.json').write_text(json.dumps(report,indent=2));print('Final docs',report)
