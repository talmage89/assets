"""Two-dimensional evidence from the shipped hero and a measured photo strip.

Photographs are read here for critique only, never by the asset generator.
Both images are sampled onto the same millimeter grid before thresholding.
Connected regions retain their area, two bounding dimensions and boundary
censoring. No 1-D run length is used as an acceptance measure.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from finish_review import camera, layout
from kit.photo_match import project
from kit.fonts import find_font
LUMA=np.array((.2126,.7152,.0722))
PPM=2.0
# Approximate photographic scale: the full receiver envelope is 1090 px/230 mm.
PHOTO_CORNERS=np.array(((1900,284),(2638,271),(2638,332),(1900,350)),float)
PHOTO_LENGTH=738/(1090/230)
LENGTH=round(PHOTO_LENGTH*PPM)/PPM
# Front photo edge: 66 px / (1090 px / 230 mm) = 13.93 mm.
# Use 14 mm within scale uncertainty; rectify the receding 61-px aft edge.
HEIGHT=14.0
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),13)

def sample(image,xy):
    a=np.asarray(image.convert('RGB'),float)
    x=np.clip(xy[...,0]-.5,0,image.width-1);y=np.clip(xy[...,1]-.5,0,image.height-1)
    ix=np.floor(x).astype(int);iy=np.floor(y).astype(int)
    jx=np.minimum(ix+1,image.width-1);jy=np.minimum(iy+1,image.height-1)
    tx=(x-ix)[...,None];ty=(y-iy)[...,None]
    return ((a[iy,ix]*(1-tx)+a[iy,jx]*tx)*(1-ty)
            +(a[jy,ix]*(1-tx)+a[jy,jx]*tx)*ty)

def surface(yy,zz):
    """Actual outer receiver triangle intersection along -X, not a box proxy."""
    d=np.load(BASE/'build/value-surfaces.npz');names=d['names'].tolist()
    triangles=d['triangles'][d['parts']==names.index('Receiver_Shell')]
    xx=np.full(yy.shape,np.inf)
    for tri in triangles:
        (ax,ay),(bx,by),(cx,cy)=tri[:,1:]
        den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(den)<1e-12:continue
        a=((by-cy)*(yy-cx)+(cx-bx)*(zz-cy))/den
        b=((cy-ay)*(yy-cx)+(ax-cx)*(zz-cy))/den;c=1-a-b
        x=a*tri[0,0]+b*tri[1,0]+c*tri[2,0]
        hit=(a>=-1e-7)&(b>=-1e-7)&(c>=-1e-7)&(x<xx)
        xx[hit]=x[hit]
    assert np.isfinite(xx).all(),'Strip grid missed actual receiver'
    return np.stack((xx,yy,zz),axis=-1)

def components(mask,diagonals=True):
    """Flood-fill native 2-D cells; preserve all regions, including clipped ones."""
    h,w=mask.shape;seen=np.zeros(mask.shape,bool);rows=[];labels=np.zeros(mask.shape,np.int32)
    steps=[(-1,0),(1,0),(0,-1),(0,1)]
    if diagonals:steps += [(-1,-1),(-1,1),(1,-1),(1,1)]
    for y,x in zip(*np.where(mask)):
        if seen[y,x]:continue
        todo=[(y,x)];seen[y,x]=True;points=[]
        while todo:
            qy,qx=todo.pop();points.append((qy,qx))
            for dy,dx in steps:
                ny,nx=qy+dy,qx+dx
                if 0<=ny<h and 0<=nx<w and mask[ny,nx] and not seen[ny,nx]:
                    seen[ny,nx]=True;todo.append((ny,nx))
        p=np.array(points);lo=p.min(0);hi=p.max(0)+1;n=len(p)
        label=len(rows)+1;labels[p[:,0],p[:,1]]=label
        boundaries=[name for flag,name in zip((lo[0]==0,hi[0]==h,lo[1]==0,hi[1]==w),('top','bottom','forward','aft')) if flag]
        rows.append(dict(label=label,cells=n,area_mm2=n/PPM**2,
            equivalent_diameter_mm=math.sqrt(4*n/math.pi)/PPM,
            length_mm=float((hi[1]-lo[1])/PPM),height_mm=float((hi[0]-lo[0])/PPM),
            bbox_cells=[int(lo[1]),int(lo[0]),int(hi[1]),int(hi[0])],
            touches=boundaries,complete=not boundaries))
    return sorted(rows,key=lambda r:-r['cells']),labels

def summary(rows,total):
    complete=[r for r in rows if r['complete']]
    areas=np.array([r['area_mm2'] for r in rows])
    bins=[0,.5,1,2,5,20,100,float('inf')]
    return dict(count=len(rows),complete_count=len(complete),
        area_bin_edges_mm2=[0,.5,1,2,5,20,100,'infinity'],
        area_bin_counts=np.histogram(areas,bins)[0].tolist(),
        largest_share_of_phase=rows[0]['cells']/max(total,1) if rows else 0,
        largest=rows[:8],complete_length_mm=[r['length_mm'] for r in complete],
        complete_area_mm2=[r['area_mm2'] for r in complete],
        all_regions=rows)

def metrics(rgb,threshold=65):
    worn=rgb@LUMA>threshold;wr,_=components(worn);pr,_=components(~worn,False)
    return worn,dict(worn_share=float(worn.mean()),
        observed_worn_median_rgb=np.median(rgb[worn],axis=0).tolist() if worn.any() else None,
        observed_worn_median_luma=float(np.median((rgb@LUMA)[worn])) if worn.any() else None,
        observed_bright_share=float(((rgb@LUMA>=180)&worn).sum()/max(worn.sum(),1)),
        length_profile=worn.mean(0).tolist(),height_profile=worn.mean(1).tolist(),
        thirds_forward_middle_aft=[float(a.mean()) for a in np.array_split(worn,3,axis=1)],
        quarters_top_to_bottom=[float(a.mean()) for a in np.array_split(worn,4,axis=0)],
        worn_regions=summary(wr,int(worn.sum())),paint_islands=summary(pr,int((~worn).sum())))

def color_components(mask,diagonals=True):
    rows,labels=components(mask,diagonals);result=np.zeros((*mask.shape,3),np.uint8)
    for r in rows:
        if r['cells']<2:color=(160,160,160)
        else:color=(50+r['label']*73%190,50+r['label']*107%190,50+r['label']*41%190)
        result[labels==r['label']]=color
    return Image.fromarray(result)

def plot(draw,box,curves,xlabel,ylabel):
    x,y,w,h=box
    for v in (0,.25,.5,.75,1):
        q=y+h*(1-v);draw.line((x,q,x+w,q),fill=(195,198,194))
        draw.text((x-37,q-8),f'{v:.0%}',font=SMALL,fill=(30,35,30))
    for i,(values,color) in enumerate(curves):
        pts=[(x+j*w/max(len(values)-1,1),y+h*(1-v)) for j,v in enumerate(values)]
        draw.line(pts,fill=color,width=3)
    draw.text((x,y+h+7),xlabel,font=SMALL,fill=(30,35,30))
    draw.text((x,y-24),ylabel,font=SMALL,fill=(30,35,30))

def build(beauty=None,out=None):
    layout()
    beauty=Path(beauty) if beauty else BASE/'renders/final/beauty'
    out=Path(out) if out else BASE/'renders/final/pairs';out.mkdir(parents=True,exist_ok=True)
    hero=Image.open(beauty/'hero.png');meta=json.loads((beauty/'shots.json').read_text())['hero']
    assert meta['sha256']==hashlib.sha256(Path(meta['source']).read_bytes()).hexdigest(),'Stale hero'
    w=round(LENGTH*PPM);h=round(HEIGHT*PPM)
    u,v=np.meshgrid((np.arange(w)+.5)/w,(np.arange(h)+.5)/h)
    yy=.140-u*(LENGTH/1000);zz=.1245-v*(HEIGHT/1000)
    points=surface(yy,zz)
    xy=project(camera(meta),points.reshape(-1,3),hero.width,hero.height)[0].reshape(h,w,2)
    reference=Image.open(BASE/'build/white-balanced/navy2.png')
    # A planar photograph requires projective rectification, rather than
    # stretching each vertical sample column by bilinear quad interpolation.
    unit=np.array(((0,0),(1,0),(1,1),(0,1)),float)
    matrix=[];target=[]
    for (pu,pv),(px,py) in zip(unit,PHOTO_CORNERS):
        matrix.extend(((pu,pv,1,0,0,0,-px*pu,-px*pv),
                       (0,0,0,pu,pv,1,-py*pu,-py*pv)))
        target.extend((px,py))
    transform=np.r_[np.linalg.solve(matrix,target),1].reshape(3,3)
    def warp(qu,qv):
        pts=np.stack((qu,qv,np.ones_like(qu)),axis=-1)@transform.T
        return pts[...,:2]/pts[...,2:]
    assert np.max(abs(warp(unit[:,0],unit[:,1])-PHOTO_CORNERS))<1e-8
    photo_xy=warp(u,v)
    images={'shipping':sample(hero,xy),'photo':sample(reference,photo_xy)}
    results={};masks={}
    for name,rgb in images.items():
        masks[name],results[name]=metrics(rgb)
        grain=(rgb@LUMA)[8:19,6:44]
        results[name]['forward_coating_grain']=dict(rectangle_cells=[6,8,44,19],
            median_luma=float(np.median(grain)),standard_deviation_luma=float(np.std(grain)),
            horizontal_adjacent_pixel_median_absolute_difference=float(np.median(abs(np.diff(grain,axis=1)))),
            scope='Fixed continuous forward worn-field patch on the common grid; texture grain diagnostic, not a wear-pattern acceptance profile.')
        results[name]['threshold_sensitivity']={str(t):{k:val for k,val in metrics(rgb,t)[1].items() if k in ('worn_share','thirds_forward_middle_aft','quarters_top_to_bottom')} for t in (55,60,70,75)}
        Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(out/f'wear-2d-{name}-color.png')
        Image.fromarray(masks[name].astype('uint8')*255).save(out/f'wear-2d-{name}-mask.png')
    # A separate full-height context proves that lower broad flats stay black.
    ch=round((124.5-75)*PPM)
    cu,cv=np.meshgrid((np.arange(w)+.5)/w,(np.arange(ch)+.5)/ch)
    cy=.140-cu*(LENGTH/1000);cz=.1245-cv*.0495
    context_points=surface(cy,cz)
    context_xy=project(camera(meta),context_points.reshape(-1,3),hero.width,hero.height)[0].reshape(ch,w,2)
    context_rgb=sample(hero,context_xy);context_worn=context_rgb@LUMA>65
    lower=cz<.109
    results['receiver_height_context']=dict(z_top_bottom_mm=[124.5,75],
        lower_flank_below_z_mm=109,lower_flank_worn_share=float(context_worn[lower].mean()),
        z_row_centers_mm=(cz[:,0]*1000).tolist(),height_profile=context_worn.mean(1).tolist(),
        method='Same exported hero, projected actual outer receiver triangles over the full visible flank; luma >65.')
    context=Image.new('RGB',(1500,500),(231,233,228));cd=ImageDraw.Draw(context)
    cd.text((20,15),'EXPORTED HERO / full receiver height / Z124.5 to Z75 mm / forward at left',font=FONT,fill=(20,30,25))
    for i,panel in enumerate((Image.fromarray(np.uint8(context_rgb)),Image.fromarray(context_worn.astype('uint8')*255))):
        context.paste(panel.resize((w*2,ch*2),Image.Resampling.NEAREST),(20+i*750,50))
    plot(cd,(65,315,1370,115),[(context_worn.mean(1), (25,100,190))],
        'Top -> bottom / full receiver height 49.5 mm','Worn share across full receiver height')
    cd.text((20,470),f"Below Z109 mm: {results['receiver_height_context']['lower_flank_worn_share']:.1%} visible worn area; only thin crest nicks remain.",font=FONT,fill=(20,30,25))
    context.save(out/'wear-2d-height-context.jpg',quality=96)
    # Sample a continuous rubbed patch at native reference resolution after WB.
    patch=np.asarray(reference.crop((1910,290,1990,323)),float).reshape(-1,3)
    patch=patch[patch@LUMA>65];median=np.median(patch,axis=0)
    results['reference_worn_field_color']=dict(rectangle=[1910,290,1990,323],threshold=65,
        rgb_median=median.tolist(),rgb_ratios_g1=(median/median[1]).tolist(),
        luma_median=float(np.median(patch@LUMA)))
    results['method']=dict(source='Exported GLB hero pixels sampled at projections of actual immutable receiver triangles; reference sampled independently.',
        glb_sha256=meta['sha256'],hero_size=list(hero.size),common_pixels_per_mm=PPM,
        grid_size=[w,h],span_mm=[LENGTH,HEIGHT],photo_corners=PHOTO_CORNERS.tolist(),
        photo_rectification='Projective homography; 14-mm depth estimated from the front 66-pixel edge, correcting the receding 61-pixel aft edge.',
        photo_front_edge_measured_depth_mm=66/(1090/230),
        hero_y_forward_aft_mm=[140,140-LENGTH],hero_z_top_bottom_mm=[124.5,110.5],
        neutral='Upper gun white selector legend, brightest 15% of rectangle (2270,535)-(2330,565).',
        neutral_linear_gains=json.loads((BASE/'build/white-balanced/corrections.json').read_text())['navy2.jpg']['linear_rgb_gains'],
        threshold_luma_255=65,filter='Bilinear color sampling to a common 0.5-mm cell, then binary tone classification. No morphological filling or speck removal.',
        connectivity='Worn: 8 neighbors; paint: 4 neighbors. Boundary-touching regions reported as censored, not silently discarded.',
        uncertainty='Photo 1090px/230mm scale is approximate. Photo depth is estimated from the front 66px edge (13.93mm, rounded to 14mm); a homography rectifies its 61px receding aft edge. This assumes a planar rectangular land. Different lighting, curvature, and finite hero/atlas resolution affect tone classification and connectivity. Threshold sensitivity is reported.')
    canvas=Image.new('RGB',(1500,1210),(231,233,228));draw=ImageDraw.Draw(canvas)
    draw.text((24,12),'RECEIVER / 2-D worn fields and paint islands / same 0.5-mm grid / forward at left',font=FONT,fill=(20,30,25))
    for col,name in enumerate(('shipping','photo')):
        x=25+750*col;row=results[name]
        draw.text((x,45),'EXPORTED GLB HERO' if name=='shipping' else 'WHITE-BALANCED PHOTO',font=FONT,fill=(20,30,25))
        panels=[Image.fromarray(np.uint8(images[name])),Image.fromarray(masks[name].astype('uint8')*255),color_components(masks[name]),color_components(~masks[name],False)]
        for i,(label,panel) in enumerate(zip(('Observed color','Binary worn area (white = worn)','Connected worn regions (8 neighbors)','Paint regions (4 neighbors)'),panels)):
            y=78+i*100;draw.text((x,y),label,font=SMALL,fill=(20,30,25))
            canvas.paste(panel.resize((w*2,h*2),Image.Resampling.NEAREST),(x,y+22))
        wr=row['worn_regions'];pr=row['paint_islands']
        lines=[f"Worn area {row['worn_share']:.1%}; forward/middle/aft: "+' / '.join(f'{v:.0%}' for v in row['thirds_forward_middle_aft']),
               f"Worn regions: {wr['count']}; largest contains {wr['largest_share_of_phase']:.1%} of wear",
               f"Paint regions: {pr['count']}; {pr['complete_count']} enclosed islands",
               'Largest worn regions, area mm2 / bounding length x height mm:']
        for r in wr['largest'][:3]:lines.append(f"  {r['area_mm2']:.1f} / {r['length_mm']:.1f} x {r['height_mm']:.1f}"+('  [boundary clipped]' if r['touches'] else ''))
        lines.append('Largest paint regions, area / bounding length x height mm:')
        for r in pr['largest'][:3]:lines.append(f"  {r['area_mm2']:.1f} / {r['length_mm']:.1f} x {r['height_mm']:.1f}"+('  [boundary clipped]' if r['touches'] else ''))
        grain=row['forward_coating_grain']
        lines.append(f"Forward coating grain: adjacent-pixel luma MAD {grain['horizontal_adjacent_pixel_median_absolute_difference']:.1f}; std {grain['standard_deviation_luma']:.1f}")
        for i,line in enumerate(lines):draw.text((x,485+i*21),line,font=SMALL,fill=(20,30,25))
    blue=(25,100,190);red=(190,75,35)
    plot(draw,(65,805,625,220),[(results[k]['length_profile'],c) for k,c in (('shipping',blue),('photo',red))],f'Forward -> aft / {LENGTH:.1f} mm','Worn share along length (all rows)')
    plot(draw,(815,805,625,220),[(results[k]['height_profile'],c) for k,c in (('shipping',blue),('photo',red))],'Top -> rib / 14 mm','Worn share across height (all columns)')
    draw.text((25,1075),'BLUE: exported hero     ORANGE: photo     Every cell contributes to both profiles.',font=FONT,fill=(20,30,25))
    draw.text((25,1105),'Components use actual 2-D area and two bounding dimensions. Clipped regions remain labeled; full lists and threshold sensitivity are in JSON.',font=SMALL,fill=(20,30,25))
    draw.text((25,1130),'Reference neutral: white selector legend. Photo scale and lighting are approximate; this is observed wear, not recovered coating chemistry.',font=SMALL,fill=(20,30,25))
    draw.text((25,1155),'No photo data enters the source mask or material. Binary masks are measured from the rendered delivery and the independent photograph.',font=SMALL,fill=(20,30,25))
    canvas.save(out/'wear-2d-pair.jpg',quality=96);canvas.save(out/'wear-2d-pair.png')
    (out/'wear-2d-values.json').write_text(json.dumps(results,indent=2))
    return results

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--beauty');p.add_argument('--out');a=p.parse_args()
    r=build(a.beauty,a.out)
    print(json.dumps({k:{x:r[k][x] for x in ('worn_share','thirds_forward_middle_aft','quarters_top_to_bottom')} for k in ('shipping','photo')},indent=2))
