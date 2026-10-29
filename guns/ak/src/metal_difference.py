"""Native-hero controlled metal-abrasion evidence from two exported GLBs.

The independent control bake sets only metal abrasion to zero. Wood, carbon,
manufacturing, geometry, camera, lighting, exposure and render settings stay.
Pixel regions are actual z-buffered imported triangles and changed shipping
texels, subdivided by physical site. No morphology filtering or added sites.
"""
from pathlib import Path
import json,sys,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.fonts import find_font
from image_masks import raster,bilinear
from texture_preservation import signature,geometry_equal
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),15)
LUMA=np.array([.2126,.7152,.0722])

def main():
    out=BASE/'renders/final';control=BASE/'build/metal-control'
    shipped=BASE/'export/ak.glb';counter=control/'export/ak.glb'
    assert geometry_equal(signature(shipped),signature(counter)),'Control changed geometry or animation'
    records=[json.loads((out/d/'shots.json').read_text())['hero'] for d in ('beauty','metal-control')]
    for r,p in zip(records,(shipped,counter)):
        assert r['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(),'Stale hero'
    exclude={'source','sha256','stage'}
    assert {k:v for k,v in records[0].items() if k not in exclude}=={k:v for k,v in records[1].items() if k not in exclude}
    rgba=[np.asarray(Image.open(out/d/'hero.png').convert('RGBA')).astype(float) for d in ('beauty','metal-control')]
    assert rgba[0].shape==rgba[1].shape and np.array_equal(rgba[0][:,:,3],rgba[1][:,:,3])
    used,clean=[a[:,:,:3] for a in rgba];h,w=used.shape[:2]
    geometry=np.load(BASE/'build/value-geometry.npz');geo={k:geometry[k] for k in geometry.files}
    ids,uv=raster(geo,records[0],w,h)
    _,yz=raster(dict(geo,uv=geo['xyz'][:,:,1:]),records[0],w,h);y,z=yz[:,:,0],yz[:,:,1]
    texcoords=np.stack([uv[:,:,0].ravel()*2047,(1-uv[:,:,1].ravel())*2047],axis=1).astype(float)
    maps=[]
    for folder in (BASE/'textures',control/'textures'):
        channels=[]
        for key in ('BaseColor','ORM'):
            image=np.asarray(Image.open(folder/('T_Rill39_'+key+'.png')).convert('RGBA' if key=='BaseColor' else 'RGB')).astype(float)
            channels.append(bilinear(image,texcoords).reshape(h,w,-1))
        maps.append(np.concatenate(channels,axis=2))
    support=(np.max(np.abs(maps[0]-maps[1]),axis=2)>4)&(ids>0)
    names=geo['names'];part=lambda *prefix:np.isin(ids,[i+1 for i,n in enumerate(names) if str(n).startswith(prefix)])
    # Inverse the same accepted curved sweep, for reporting rib station only.
    a=np.full((h,w),-.04);b=np.full((h,w),.24)
    for _ in range(24):
        s=(a+b)/2;center=.132+1.65*s*s+3*s*s*s;slope=3.3*s+9*s*s
        error=z-.070+.87*s-(y-center)*slope
        b=np.where(error>0,s,b);a=np.where(error>0,a,s)
    s=(a+b)/2;center=.132+1.65*s*s+3*s*s*s
    v=(y-center)*np.sqrt(1+(3.3*s+9*s*s)**2)
    cover=part('TopCover_Pressed');receiver=part('Receiver_Sheet');mag=part('Magazine_Sheet')
    # Mutually exclusive physical partitions; only changed baked texels in
    # each partition count. Rear-rim/crest priority resolves overlap at joins.
    sites=[('Receiver lower front corners',receiver&(y>=.145)),
           ('Receiver magazine-entry edge',receiver&(y<.145)),
           ('Lower-front rivet crown',part('Receiver_Rivet')),
           ('Cover rear rim',cover&(y<-.026)|part('TopCover_RearCap')),
           ('Cover rear side bead',cover&(y>=-.026)&(z<.102)),
           ('Cover rear roof crest',cover&(y>=-.026)&(y<.035)&(z>=.102)),
           ('Cover middle roof crest',cover&(y>=.035)&(z>=.102)),
           ('Trigger guard bottom',part('TriggerGuard_Stamping')),
           ('Magazine rear raised rib',mag&(v<-.011)),
           ('Magazine middle raised rib',mag&(v>=-.011)&(v<.011)),
           ('Magazine forward raised rib',mag&(v>=.011)),
           ('Magazine folded spines',part('Magazine_FoldSpine')),
           ('Magazine floorplate corners',part('Magazine_Floorplate')),
           ('Magazine feed lips',part('Magazine_FeedLip')),
           ('Selector forward edge and fold',part('Selector_Lever','Selector_ThumbFold')),
           ('Charging handle and carrier rails',part('ChargingHandle','Carrier_VisualRail','Carrier_PortCheek')),
           ('Gas block collar edges',part('GasBlock_Neck')),
           ('Gas tube seat and muzzle rim',part('GasBlock_TubeSeat','Muzzle_SlantBrake')),
           ('Hood notch and slider peaks',part('Sight_FrontHood','Sight_RearNotch','Sight_SliderButton')),
           ('Buttplate and front cap side edges',part('Buttplate','Handguard_Retainer363'))]
    diff=used-clean;delta=diff@LUMA;absolute=np.abs(diff)
    Image.fromarray(np.uint8(np.clip(absolute,0,255))).save(out/'metal-wear-difference.png')
    Image.fromarray(np.uint8(np.clip(absolute*4,0,255))).save(out/'metal-wear-difference-x4.png')
    labels=Image.fromarray(np.uint8(used)).convert('RGB');d=ImageDraw.Draw(labels);rows=[];assigned=np.zeros((h,w),bool)
    for number,(name,region) in enumerate(sites,1):
        mask=support&region;assert not (assigned&mask).any(),name;assigned|=mask
        area=int(mask.sum());row=dict(site=name,area_pixels=area)
        if area:
            jj,ii=np.where(mask);box=[int(ii.min()),int(jj.min()),int(ii.max()+1),int(jj.max()+1)]
            u=(used@LUMA)[mask];c=(clean@LUMA)[mask];dv=delta[mask]
            row.update(region_xyxy=box,shipped_mean_luma=float(u.mean()),control_mean_luma=float(c.mean()),
                       mean_delta_luma=float(dv.mean()),median_delta_luma=float(np.median(dv)),mean_absolute_delta_luma=float(np.abs(dv).mean()),
                       absolute_delta_p90=float(np.percentile(np.abs(dv),90)),pixels_absolute_delta_ge8=int((np.abs(dv)>=8).sum()))
            d.rectangle(box,outline=(231,149,47),width=1);d.text((box[0],max(0,box[1]-18)),str(number),font=SMALL,fill=(244,163,51))
        else:row.update(region_xyxy=None,mean_delta_luma=None,pixels_absolute_delta_ge8=0)
        rows.append(row)
    labels.save(out/'metal-wear-regions.png')
    # Diagnostic purity: wood and grip shipping texels should not change.
    nonmetal=part('Stock_Sculpt','LowerHandguard_Sculpt','UpperHandguard_Sculpt','PistolGrip_Sculpt')
    nonmetal_map_delta=np.abs(maps[0]-maps[1])[nonmetal]
    assert nonmetal_map_delta.max()<2,'Metal-only control altered wood/grip maps'
    unassigned=int((support&~assigned&~nonmetal).sum())
    # The accepted atlas projection crosses a few touching Front_Insert
    # texels at the receiver's lower-front joint. Keep those pixels visible
    # in the raw difference, but exclude them from every wear-site area.
    # This is a measured projection qualification, not a new abrasion site.
    extra=support&~assigned&~nonmetal
    joint=part('Front_Insert')&(y>=.174)&(y<=.221)&(z>=.048)&(z<=.055)
    assert not (extra&~joint).any(),('Changed metal texels outside accepted sites/contact join',int((extra&~joint).sum()))
    joint_row=None
    if extra.any():
        jj,ii=np.where(extra)
        joint_row=dict(part='Front_Insert',area_pixels=int(extra.sum()),region_xyxy=[int(ii.min()),int(jj.min()),int(ii.max()+1),int(jj.max()+1)],
                       mean_delta_luma=float(delta[extra].mean()),excluded_from_all_site_counts=True,
                       scope='Touching receiver lower-front joint; existing projection picks up neighboring receiver abrasion. Not an independently authored site.')
    report=dict(passed=True,method=__doc__,resolution=[w,h],rows=rows,shipped_sha256=records[0]['sha256'],control_sha256=records[1]['sha256'],
                support_definition='Visible imported surface whose sampled BaseColor RGBA or ORM differs by >4/255 between independently baked atlases. No dilation/filtering. Integer pixel-center areas; fractional antialias coverage is not counted.',
                value_definition='8-bit display-referred Rec.709 luma. Signed shipped minus control; absolute contrast >=8 listed separately. Noise/global light-transport differences outside direct wear remain in the full difference image.',
                control_nonmetal_max_map_delta=float(nonmetal_map_delta.max()),unassigned_changed_metal_pixels=unassigned,
                contact_projection=joint_row,
                scope='Control is comparison-only: original enamel/oxide/bluing everywhere abrasion was removed. Carbon, manufacturing and wood stay. Hidden sites report zero honestly; area is visible support, not total authored wear.')
    (out/'metal-wear-values.json').write_text(json.dumps(report,indent=2))
    lines=['| Site | Hero region xyxy | Area px | Mean ΔY /255 | Pixels abs ΔY ≥8 |','| --- | --- | ---: | ---: | ---: |']
    for row in rows:
        value='hidden' if row['mean_delta_luma'] is None else f"{row['mean_delta_luma']:+.2f}"
        lines.append(f"| {row['site']} | {row['region_xyxy'] or 'occluded'} | {row['area_pixels']} | {value} | {row['pixels_absolute_delta_ge8']} |")
    if joint_row:lines.extend(['',f"Projection qualification: {joint_row['area_pixels']} Front_Insert pixels at {joint_row['region_xyxy']} change by mean {joint_row['mean_delta_luma']:+.2f}/255 at the touching lower-front receiver joint. Excluded from every site count; retained in the unmasked difference."])
    (out/'metal-wear-table.md').write_text('\n'.join(lines)+'\n')
    canvas=Image.new('RGB',(1600,800*4+440),'#ebede9');draw=ImageDraw.Draw(canvas)
    for i,(title,path) in enumerate([('Shipped GLB / 1600 native pixels',out/'beauty/hero.png'),('Independent GLB / metal abrasion masked out',out/'metal-control/hero.png'),('Absolute RGB difference / unamplified',out/'metal-wear-difference.png'),('Native site regions / pixel areas and luma changes below',out/'metal-wear-regions.png')]):
        im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(108,111,114,255));bg.alpha_composite(im);canvas.paste(bg.convert('RGB'),(0,i*800));draw.text((12,i*800+8),title,font=FONT,fill='white' if i==2 else '#efc783')
    for i,row in enumerate(rows):
        x=12+(i//10)*800;yy=3210+(i%10)*38
        val='occluded' if row['mean_delta_luma'] is None else f"{row['area_pixels']} px; mean change {row['mean_delta_luma']:+.1f}/255"
        draw.text((x,yy),f"{i+1}. {row['site']}: {val}",font=SMALL,fill='black')
    canvas.save(out/'metal-wear-proof.jpg',quality=94)
    print('\n'.join(lines),flush=True)
if __name__=='__main__':main()
