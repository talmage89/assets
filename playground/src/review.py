"""Ignored checkpoint contact sheets and measured budget table; never docs/."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact
from kit.fonts import find_font

def main():
    out=Path('renders/checkpoint')
    if (out/'pieces.json').exists():
        im=Image.open(out/'pieces.png').convert('RGB');d=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('Noto Sans'),19)
        for row in json.loads((out/'pieces.json').read_text()).get('piece_labels',[]):
            x,y=row['pixel'];label=row['name'];w=d.textlength(label,font=font)
            d.rectangle((x-w/2-4,y-2,x+w/2+4,y+25),fill=(238,239,235));d.text((x-w/2,y),label,font=font,fill=(22,32,27))
        im.save(out/'pieces-labeled.jpg',quality=95)
    paths=sorted(out.glob('[123]*/hero.png'))+sorted(out.glob('[123]*/above.png'))+sorted(out.glob('*.png'))
    years={str(s['seed']):s['year'] for s in json.loads(Path('build/manifest.json').read_text())['sites']}
    captions={str(p):str(years[p.parent.name])+' / seed '+p.parent.name+' / '+p.stem for p in paths if p.parent.name in years}
    contact(paths,out/'contact.jpg',width=2000,title='Playground / form and construction checkpoint / exported glTF',captions=captions)
    pairs=sorted((out/'matches').glob('*-pair.jpg'))
    if pairs:contact(pairs,out/'matched-contact.jpg',width=2000,title='Period photographs / construction comparisons / camera fit residuals retained')
    # Technical sections are derived only from the fresh-import check data.
    import os
    os.environ['MPLCONFIGDIR']=str(Path('build/matplotlib').resolve())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.font_manager import FontProperties
    data=json.loads(Path('build/check.json').read_text());font=FontProperties(fname=find_font('Noto Sans'))
    fig,axes=plt.subplots(2,3,figsize=(12,6),layout='constrained')
    for j,name in enumerate(('SlideWave72','SlideTube48')):
        for i,row in enumerate(data['pieces'][name]['imported_molded_sections']):
            ax=axes[j,i];ax.add_collection(LineCollection(row['segments_m'],colors='#154a40',linewidths=1.2));ax.autoscale();ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('transverse meters',fontproperties=font);ax.set_ylabel('section meters',fontproperties=font);ax.set_title(name+' / station '+str(row['station']),fontproperties=font,fontsize=10)
    fig.suptitle('Actual exported molded surfaces / three perpendicular sections / meters',fontproperties=font)
    fig.savefig(out/'molded-cross-sections.jpg',dpi=140);plt.close(fig)
    # Numerical value audit is descriptive; no exposure tricks or look acceptance.
    values={}
    for p in out.glob('*/hero.png'):
        a=__import__('numpy').asarray(Image.open(p).convert('RGB'))/255;lum=.2126*a[:,:,0]+.7152*a[:,:,1]+.0722*a[:,:,2]
        values[p.parent.name]=dict(p1=float(__import__('numpy').percentile(lum,1)),p50=float(__import__('numpy').percentile(lum,50)),p99=float(__import__('numpy').percentile(lum,99)),clipped_pixels_fraction=float((a.max(axis=2)>.995).mean()),scope='whole-frame display luminance; quick materials, not albedo calibration')
    Path('build/hero-values.json').write_text(json.dumps(values,indent=2));print('CONTACT',out/'contact.jpg')

if __name__=='__main__':main()
