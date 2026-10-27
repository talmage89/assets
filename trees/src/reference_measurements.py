"""Manually inspected photo landmarks, not photo-derived model geometry.

Coordinates refer to original upright images. The crown base is the lowest
continuous leafy mass; isolated peripheral leaf tips vary by roughly 10–15 px.
Metric values are illustrative normalization to 12.4 m, not surveys.
"""
MEASUREMENTS={
 'psu':dict(photo='psu-form.jpg',crop=(90,0,835,675),crown=(126,32,817,582),ground_y=659,
            widest_y=442,widest_uncertainty_px=30,uncertainty_px=12,credit='Jodi Sulpizio / Penn State Extension'),
 'osu':dict(photo='osu-form.jpg',crop=(704,0,1425,898),crown=(748,24,1414,718),ground_y=841,
            widest_y=465,widest_uncertainty_px=30,uncertainty_px=15,credit='Oregon State University Landscape Plants'),
}


def values(row):
    x0,y0,x1,y1=row['crown'];height=y1-y0;tree=row['ground_y']-y0
    return dict(crown_width_px=x1-x0,crown_height_px=height,crown_width_height=(x1-x0)/height,
                base_fraction_of_tree=(row['ground_y']-y1)/tree,
                crown_base_at_12_4m=(row['ground_y']-y1)/tree*12.4,
                widest_height_fraction_of_crown=(y1-row['widest_y'])/height,
                widest_height_fraction_of_tree=(row['ground_y']-row['widest_y'])/tree,
                widest_height_at_12_4m=(row['ground_y']-row['widest_y'])/tree*12.4,
                widest_y_px=row['widest_y'],widest_uncertainty_px=row['widest_uncertainty_px'],uncertainty_px=row['uncertainty_px'])

if __name__=='__main__':
    from pathlib import Path
    import sys,json
    import numpy as np
    from PIL import Image,ImageDraw,ImageFont
    ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
    from kit.fonts import find_font
    out=ROOT/'trees/renders/round3-measurements';out.mkdir(parents=True,exist_ok=True)
    (ROOT/'trees/build').mkdir(parents=True,exist_ok=True)
    report={};font=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
    for name,row in MEASUREMENTS.items():
        im=Image.open(ROOT/'trees/refs'/row['photo']).convert('RGB');a=np.asarray(im)/255
        x0,y0,x1,y1=row['crown'];crop=a[y0:y1,x0:x1]
        mask=(crop[:,:,1]>crop[:,:,0]*1.10)&(crop[:,:,1]>crop[:,:,2]*1.08)
        lum=crop[mask]@np.array([.2126,.7152,.0722])
        v=values(row);v['near_black_green_fraction']=float(np.mean(lum<.02));v['green_display_luminance_p5_p50_p95']=np.percentile(lum,[5,50,95]).tolist();report[name]=v
        d=ImageDraw.Draw(im);d.rectangle(row['crown'],outline=(255,210,40),width=3)
        d.line((x0,row['ground_y'],x1,row['ground_y']),fill=(255,90,50),width=3)
        d.line((x0,row['widest_y'],x1,row['widest_y']),fill=(230,85,240),width=3)
        for y,label in [(row['widest_y'],'widest band ±30 px'),(y0,'crown top'),(y1,'crown base'),(row['ground_y'],'grade')]:
            d.text((x0+8,y-22),label,font=font,fill=(255,255,230),stroke_width=2,stroke_fill=(0,0,0))
        im=im.crop(row['crop']);canvas=Image.new('RGB',(im.width,im.height+125),(235,235,230));canvas.paste(im,(0,0));d=ImageDraw.Draw(canvas)
        d.text((10,im.height+7),f"{name.upper()} crown W/H {v['crown_width_height']:.3f}; base {100*v['base_fraction_of_tree']:.1f}% of tree height",font=font,fill=(20,35,25))
        d.text((10,im.height+34),f"Base {v['crown_base_at_12_4m']:.2f} m IF total height is 12.4 m; ±{row['uncertainty_px']} px landmarks",font=font,fill=(20,35,25))
        d.text((10,im.height+61),f"Widest band {100*v['widest_height_fraction_of_crown']:.1f}% above crown base; {v['widest_height_at_12_4m']:.2f} m IF 12.4 m tree",font=font,fill=(20,35,25))
        d.text((10,im.height+91),row['credit']+' / local study only',font=font,fill=(20,35,25))
        canvas.save(out/(name+'-measurements.jpg'),quality=94)
    (ROOT/'trees/build/reference-measurements.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
