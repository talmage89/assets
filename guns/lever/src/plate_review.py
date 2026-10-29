"""Whole-plate display distributions and highlights, comparison only.

Native photo observations stay here, outside modeling/look-dev. No reference
image, pixel, mask or histogram is read by the asset generator or the baker.
Use the whole flat (including protected bluing), excluding separate hardware.
"""
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(BASE.parents[1]), str(BASE/'src')]
from value_review import projection
from final_review import panel, sheet
from kit.fonts import find_font

FONT = ImageFont.truetype(find_font('Noto Sans', 'Regular'), 19)
# Inset from the bare fillet: this is the entire oxide flat, not a selected
# favorable rectangular patch. Actual side contours and hardware differ.
PLATE = [(y, z) for y, z in [(.069,.012),(.074,.052),(.188,.052),
         (.194,.018),(.181,.006),(.130,.003),(.115,.007)]]
SCREWS = [(.074,.015,.0034),(.092,.038,.0028),(.148,.040,.0029),(.185,.016,.00275)]
PHOTO = [(357,219),(377,210),(686,214),(677,256),(647,267),(420,275),(357,275)]
PHOTO_HOLES = [[(518,242),(607,236),(621,244),(615,254),(526,262),(515,254)],
               [(371,266),(377,262),(381,267),(376,273)],
               [(431,255),(438,252),(442,257),(438,261)]]

def region(im, poly, holes):
    mask = Image.new('L', im.size)
    draw = ImageDraw.Draw(mask)
    draw.polygon([tuple(p) for p in poly], fill=255)
    for hole in holes: draw.polygon([tuple(p) for p in hole], fill=0)
    return np.asarray(im.convert('RGB'), dtype=float)[np.asarray(mask)>0], mask

def render_region(im, shot):
    def xy(points):
        return projection(shot, [(.01575,y,z) for y,z in points], im.size).tolist()
    holes = [xy([(cy+np.cos(a)*r,cz+np.sin(a)*r) for a in np.linspace(0,np.pi*2,32)])
             for cy,cz,r in SCREWS]
    holes += [xy([(.122,.012),(.173,.012),(.179,.020),(.172,.028),(.122,.028)])]
    poly = xy(PLATE)
    rgb, mask = region(im, poly, holes)
    return rgb, mask, poly, holes

def describe(rgb):
    u = np.uint8(rgb).reshape(-1,1,3)
    hsv = np.asarray(Image.fromarray(u).convert('HSV')).reshape(-1,3).astype(float)/255
    hsv[:,0] *= 360
    luma = rgb @ np.array((.2126,.7152,.0722))
    high = rgb[luma>=np.percentile(luma,90)]
    saturation = (high.max(1)-high.min(1))/np.maximum(high.max(1),1)
    return dict(pixels=len(rgb), median_rgb=np.median(rgb,axis=0).tolist(),
        luma_p10_p50_p90=np.percentile(luma,[10,50,90]).tolist(),
        hsv_p10_p50_p90=np.percentile(hsv,[10,50,90],axis=0).tolist(),
        histograms={k:np.histogram(hsv[:,i],bins=36,range=(0,360 if i==0 else 1))[0].tolist()
                    for i,k in enumerate(('hue','saturation','value'))},
        brightest_decile=dict(median_rgb=np.median(high,axis=0).tolist(),
            median_saturation=float(np.median(saturation)),
            saturation_definition='Median of per-pixel (max(RGB)-min(RGB))/max(RGB); differs slightly from saturation of the channel-wise median RGB.',
            scope='Brightest 10% of whole oxide flat by display luma; not an isolated specular lobe.'),
        hue_scope='Hue is unreliable for near-neutral pixels; include all samples, do not select a favorable hue.')

def annotate(im,poly,holes):
    im=im.convert('RGB').copy(); d=ImageDraw.Draw(im)
    d.polygon([tuple(p) for p in poly],outline=(240,105,35),width=2)
    for h in holes:d.polygon([tuple(p) for p in h],outline=(240,105,35),width=1)
    return im

def reflection_regions(im, shot):
    # Independent physical sites, selected by the key/camera geometry. Keep
    # the central shoulder away from both explicitly bare corner patches.
    # Angle is measured around the actual R2.2 forging roll, in meters.
    points=[]
    for y,a in ((.105,28),(.170,28),(.170,48),(.105,48)):
        t=np.radians(a)
        points.append((.01355+.0022*np.cos(t),y,.0538+.0022*np.sin(t)))
    regions={'key_on_oxide_shoulder':points,
      'upper_flat':[(.01575,y,z) for y,z in ((.108,.045),(.170,.045),(.170,.050),(.108,.050))],
      'front_ring':[(.01565,y,z) for y,z in ((.197,.034),(.201,.034),(.201,.046),(.197,.046))]}
    rows={}
    for name,points in regions.items():
        poly=projection(shot,points,im.size).tolist()
        rgb,_=region(im,poly,[])
        rows[name]=dict(describe(rgb),polygon=poly,surface_points_m=points)
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--beauty',default=str(BASE/'renders/final/beauty'))
    p.add_argument('--photos',default=str(BASE/'renders/final/photos'))
    p.add_argument('--out',default=str(BASE/'renders/final/look-review'))
    p.add_argument('--shotgun-renders',type=Path)
    a=p.parse_args();beauty=Path(a.beauty);photos=Path(a.photos);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    wb=BASE/'build/white-balanced/open2.png';photo=Image.open(wb).convert('RGB')
    prgb,pmask=region(photo,PHOTO,PHOTO_HOLES)
    rows={'white_balanced_photo':describe(prgb)};samples={'white_balanced_photo':prgb};marked={}
    paths={'white_balanced_photo':wb}
    for name,folder,shot_name in [('hero',beauty,'hero'),('receiver',beauty,'receiver'),('used_photo_view',photos,'used_photo')]:
        path=folder/(shot_name+'.png');im=Image.open(path)
        meta=json.loads((folder/'shots.json').read_text())[shot_name]
        rgb,mask,poly,holes=render_region(im,meta)
        rows[name]=describe(rgb);samples[name]=rgb;paths[name]=path
        marked[name]=annotate(im,poly,holes)
        rows[name].update(polygon=poly,excluded_hardware=holes,render_source_sha256=meta['sha256'])
        rows[name]['reflection_sites']=reflection_regions(im,meta)
        # The brightest flat pixels can be lit brown diffuse, rather than a
        # specular reflection. Report a separate physical rolled-shoulder
        # highlight, without calling its width an albedo/roughness target.
        shoulder=projection(meta,[(.01515,y,z) for y,z in
            [(.085,.05465),(.175,.05465),(.175,.05535),(.085,.05535)]],im.size).tolist()
        hrgb,_=region(im,shoulder,[])
        rows[name]['rolled_shoulder_reflection']=describe(hrgb)
        rows[name]['rolled_shoulder_reflection']['polygon']=shoulder
    rows['white_balanced_photo'].update(polygon=PHOTO,excluded_hardware=PHOTO_HOLES)
    poly=[(388,194),(661,195),(661,200),(388,199)]
    hrgb,_=region(photo,poly,[])
    rows['white_balanced_photo']['rolled_shoulder_reflection']=describe(hrgb)
    rows['white_balanced_photo']['rolled_shoulder_reflection']['polygon']=poly
    result=dict(scope='Observed entire oxide-flat distributions under different light/view; no albedo inversion.',
        neutral='Broad bare bolt flat, native (470,166)-(570,177), linear neutral adaptation; reflective estimate, not a gray card.',
        percentile_order=[10,50,90],rows=rows,
        input_sha256={k:hashlib.sha256(v.read_bytes()).hexdigest() for k,v in paths.items()})
    target=rows['white_balanced_photo']['brightest_decile']['median_saturation']
    result['bright_decile_comparison']=dict(photo_saturation=target,
        rendered={k:dict(saturation=rows[k]['brightest_decile']['median_saturation'],
          at_or_below_photo=rows[k]['brightest_decile']['median_saturation']<=target)
          for k in ('hero','receiver','used_photo_view')})
    (out/'plate-distributions.json').write_text(json.dumps(result,indent=2))
    # A standalone reproducible plot, suitable for native-resolution review.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,3,figsize=(16,8),dpi=100)
    colors={'hero':'#a95424','used_photo_view':'#506f8d','white_balanced_photo':'#303332'}
    for j,(key,label) in enumerate([('hue','Hue / degrees'),('saturation','Saturation / fraction'),('value','Value / fraction')]):
        for name in colors:
            h=np.asarray(rows[name]['histograms'][key],float)
            x=(np.arange(36)+.5)*(10 if j==0 else 1/36)
            axes[0,j].plot(x,h/h.sum(),label=name.replace('_',' '),color=colors[name])
        axes[0,j].set(xlabel=label,ylabel='Fraction of entire plate',title=label.split(' /')[0])
        axes[0,j].grid(alpha=.2)
    axes[0,0].legend(fontsize=8)
    for ax,key in zip(axes[1],('hero','used_photo_view','white_balanced_photo')):
        ax.imshow(marked[key] if key in marked else annotate(photo,PHOTO,PHOTO_HOLES))
        ax.set_title(key.replace('_',' '));ax.axis('off')
    fig.suptitle('Whole receiver oxide flat: native masks, HSV distributions and display highlights')
    fig.text(.04,.02,'Orange outlines exclude hardware. Photo neutral: exposed bolt flat. Lighting differs; these are display distributions, not recovered albedos.',fontsize=10)
    fig.tight_layout(rect=(0,.05,1,.95));fig.savefig(out/'receiver-histograms.jpg',pil_kwargs={'quality':94});plt.close(fig)
    # Keep the full macro beside the photograph, rather than cropping down
    # to the previously favorable single rectangle.
    image=Image.new('RGB',(1800,870),(230,230,225));d=ImageDraw.Draw(image)
    d.text((15,10),'Exported receiver / whole white-balanced used action',font=FONT,fill='black')
    for j,im in enumerate((Image.open(beauty/'receiver.png'),photo.crop((338,170,712,288)))):
        im=im.copy()
        if j==1:im=im.resize((880,round(im.height*880/im.width)),Image.Resampling.LANCZOS)
        im.thumbnail((880,600),Image.Resampling.LANCZOS)
        bg=Image.new('RGBA',(880,600),(65,67,70,255));bg.alpha_composite(im.convert('RGBA'),((880-im.width)//2,(600-im.height)//2))
        image.paste(bg.convert('RGB'),(10+j*900,50))
    for j,key in enumerate(('receiver','white_balanced_photo')):
        r=rows[key];d.text((15+j*900,668),'Whole flat median RGB '+str(r['median_rgb']),font=FONT,fill='black')
        d.text((15+j*900,702),'Brightest flat decile RGB '+str(r['brightest_decile']['median_rgb']),font=FONT,fill='black')
        d.text((15+j*900,738),'Rolled shoulder RGB '+str(r['rolled_shoulder_reflection']['median_rgb']),font=FONT,fill='black')
        d.text((15+j*900,772),'Bright-decile saturation %.3f'%r['brightest_decile']['median_saturation'],font=FONT,fill='black')
    d.text((15,825),'Photo cropped and enlarged for inspection; all measurements use original native pixels. Macro angles and illumination differ.',font=FONT,fill='black')
    image.save(out/'receiver-used-closeup.jpg',quality=94,optimize=True)
    sites=[('Continuous oxide / narrow screw seats / sparse palm and scabbard marks',beauty/'receiver.png'),
           ('Inner finger rail / rear bar / rubbed trigger face',beauty/'receiver_left.png'),
           ('Graded hand oil / satin upper tang / finished mortise',beauty/'wrist_raking.png'),
           ('Forend / local wood edge dings',beauty/'forend.png'),
           ('Muzzle rim / dark bore',beauty/'muzzle.png'),
           ('Toe and heel: compressed fibers and broken finish',beauty/'stock.png')]
    bands=beauty.parent/'wear-details'
    if (bands/'forend_band.png').exists() and (bands/'muzzle_band.png').exists():
        sites += [('Forend band / blue sleeve and satin rim rubs',bands/'forend_band.png'),
                  ('Forward band / blue sleeve and satin rim rubs',bands/'muzzle_band.png')]
    if all(file.exists() for _,file in sites):
        sheet(sites,out/'wear-sites.jpg',columns=2,width=1800,height=580)
    # Native macro with named physical wear/contact sites and a separate
    # sampled oxide highlight. The labels never feed a generated texture.
    macro=Image.open(beauty/'receiver.png').convert('RGBA')
    meta=json.loads((beauty/'shots.json').read_text())['receiver']
    marked=panel(beauty/'receiver.png',macro.size);d=ImageDraw.Draw(marked)
    named=[('1  Continuous shoulder oxide',(.0151,.128,.05535)),
      ('2  Front ring: continuous oxide',(.01565,.200,.041)),
      ('3  Screw seat: surviving blue',(.01575,.092,.0410)),
      ('4  Loading recess: surviving blue',(.01575,.154,.0275)),
      ('5  Wood/tang joint: narrow blue',(.0154,.0668,.032)),
      ('6  Sparse carrying-palm tracks',(.01575,.121,.033)),
      ('7  Sparse lower scabbard tracks',(.01575,.139,.007)),
      ('8  Cupped lower-fillet satin steel',(.0151,.151,.0021)),
      ('9  Front-corner satin rub',(.0154,.204,.020))]
    for i,(label,point) in enumerate(named):
        xy=projection(meta,[point],macro.size)[0]
        tx=18 if i%2==0 else macro.width-495
        ty=20+(i//2)*42
        d.line([(tx+12,ty+22),tuple(xy)],fill=(210,182,94),width=1)
        d.ellipse((xy[0]-3,xy[1]-3,xy[0]+3,xy[1]+3),fill=(242,204,91))
        d.rectangle((tx-4,ty-1,tx+475,ty+28),fill=(40,42,45))
        d.text((tx,ty),label,font=FONT,fill=(245,239,220))
    marked.save(out/'receiver-sites.jpg',quality=94,optimize=True)
    rows['receiver']['named_sites']=[dict(name=n,point_m=p) for n,p in named]
    reflections=Image.new('RGB',(1800,860),(230,230,225));d=ImageDraw.Draw(reflections)
    for j,key in enumerate(('hero','receiver')):
        path=paths[key];im=Image.open(path);overlay=panel(path,im.size)
        draw=ImageDraw.Draw(overlay)
        for r in rows[key]['reflection_sites'].values():
            draw.polygon([tuple(p) for p in r['polygon']],outline=(230,196,80),width=2)
        overlay.thumbnail((880,590),Image.Resampling.LANCZOS)
        reflections.paste(overlay,(j*900+(900-overlay.width)//2,45+(590-overlay.height)//2))
        d.text((j*900+15,10),key+' / physical reflection samples',font=FONT,fill='black')
        for i,(name,r) in enumerate(rows[key]['reflection_sites'].items()):
            d.text((j*900+15,655+i*38),name.replace('_',' ')+': '+str(r['median_rgb']),font=FONT,fill='black')
        d.text((j*900+15,780),'Key reflection bright decile '+str(rows[key]['reflection_sites']['key_on_oxide_shoulder']['brightest_decile']['median_rgb']),font=FONT,fill='black')
    d.text((15,825),'Fixed surface sites, independent of pixel color. Shoulder excludes bare corner rubs. RGB values use native renders.',font=FONT,fill='black')
    reflections.save(out/'reflection-samples.jpg',quality=94,optimize=True)
    # Save after adding the exact physical annotation sites as well.
    (out/'plate-distributions.json').write_text(json.dumps(result,indent=2))
    if a.shotgun_renders:
        sheet([('Bracken L20 / current exported GLB',beauty/'hero.png'),
               ('Hearth 12 / main exported GLB',a.shotgun_renders/'hero.png')],
              out/'hero-shotgun.jpg',columns=1,width=1600,height=480)
        sheet([('Bracken receiver',beauty/'receiver.png'),('Hearth receiver / same lighting',a.shotgun_renders/'receiver.png')],
              out/'steel-shotgun.jpg',columns=2,width=1800,height=650)
    print('WHOLE PLATE',[(n,r['median_rgb'],r['brightest_decile']['median_rgb']) for n,r in rows.items()],flush=True)

if __name__=='__main__':main()
