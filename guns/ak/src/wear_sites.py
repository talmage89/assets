"""Read-only 2D wear evidence on shipped UVs, at a common physical grid.

The image thresholds are stated, not treated as inverse material estimates.
Photographs and substrate masks have different scratch histories and lighting.
No image or mask produced here is an input to the asset.
"""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.fonts import find_font
from image_masks import raster,projection,bilinear
from look_review import component_sizes,polygon_mask,REGIONS,LUMA
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),16)

def homography(world,pixels):
    rows=[];rhs=[]
    for (x,y),(u,v) in zip(world,pixels):
        rows.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]])
        rhs.extend([u,v])
    return np.r_[np.linalg.solve(np.array(rows),np.array(rhs)),1].reshape(3,3)

def main():
    out=BASE/'renders/final/look-review';folder=BASE/'renders/final/photos'
    metadata=json.loads((folder/'shots.json').read_text())
    geometry=np.load(BASE/'build/value-geometry.npz')
    maps={key:np.asarray(Image.open(BASE/'textures'/('T_Rill39_'+key+'.png')).convert('RGB')).astype(float) for key in ('BaseColor','ORM')}
    # Independent receiver corner observations in the used side photograph.
    H=homography([[-.035,.086],[-.035,.050],[.220,.086],[.220,.050]],
                 [[612,246],[612,352],[1270,228],[1270,323]])
    photo=np.asarray(Image.open(BASE/'build/white-balanced/early.jpg').convert('RGB')).astype(float)
    im=np.asarray(Image.open(folder/'used_photo.png').convert('RGB')).astype(float)
    h,w=im.shape[:2];ids,uv=raster(geometry,metadata['used_photo'],w,h)
    # All bounds are meters. X is a projection plane, not a claimed surface.
    sites=[('Cover bead and ribs',(-.035,.180,.085,.119),('TopCover_',),'cover'),
           ('Selector and receiver edges',(-.035,.220,.050,.100),('Selector_','Receiver_Sheet','Receiver_Rivet'),'steel'),
           ('Lower handguard pressure',(.220,.366,.045,.093),('LowerHandguard_Sculpt',),'wood'),
           ('Upper handguard pressure',(.245,.350,.090,.124),('UpperHandguard_Sculpt',),'wood'),
           ('Wrist, stock toe and heel',(-.282,-.035,-.008,.091),('Stock_Sculpt',),'wood'),
           ('Magazine ribs and spines',(.096,.264,-.118,.057),('Magazine_',),'magazine')]
    evidence=[]
    for title,(y0,y1,z0,z1),prefixes,role in sites:
        yy,zz=np.meshgrid(np.arange(y0,y1,.0005),np.arange(z0,z1,.0005))
        points=np.stack([np.full_like(yy,.0175),yy,zz],axis=2).reshape(-1,3)
        xy,_=projection(points,metadata['used_photo'],w,h)
        ii=np.clip(xy[:,0].astype(int),0,w-1);jj=np.clip(xy[:,1].astype(int),0,h-1)
        valid=np.isin(ids[jj,ii],[i+1 for i,n in enumerate(geometry['names']) if str(n).startswith(prefixes)]).reshape(yy.shape)
        coords=bilinear(uv,xy);samples={}
        for key,a in maps.items():
            samples[key]=bilinear(a,np.stack([coords[:,0]*(a.shape[1]-1),(1-coords[:,1])*(a.shape[0]-1)],axis=1)).reshape(*yy.shape,3)
        rough=samples['ORM'][:,:,1];metal=samples['ORM'][:,:,2];color=samples['BaseColor']@LUMA
        if role=='wood':
            # Shared threshold above every intact film, including the duller
            # upper. This reads actual shipping roughness, not source masks.
            threshold=157
            worn=(rough>threshold)&valid
            definition=f'GLB: roughness >{threshold}/255 (exposed fibers/dings); photo: luma >78, R/B <3.1'
        else:
            worn=(((rough>160)&(metal<100))|(color>76))&valid
            definition='GLB: matte substrate or base luma >76; photo: bright gray, luma >80, saturation <.30'
        q=np.stack([yy.ravel(),zz.ravel(),np.ones(yy.size)],axis=1)@H.T
        q=q[:,:2]/q[:,2:];reference=bilinear(photo,q).reshape(*yy.shape,3)
        observed=bilinear(im,xy).reshape(*yy.shape,3)
        mx=reference.max(axis=2);sat=(mx-reference.min(axis=2))/np.maximum(mx,1)
        if role=='wood':
            region=polygon_mask((photo.shape[1],photo.shape[0]),REGIONS['wood'][1])
            refmask=(reference@LUMA>78)&(reference[:,:,0]/np.maximum(reference[:,:,2],1)<3.1)
        else:
            polys=REGIONS['magazine'][1] if role=='magazine' else [[(580,140),(1250,130),(1255,355),(580,370)]]
            region=polygon_mask((photo.shape[1],photo.shape[0]),polys)
            refmask=(reference@LUMA>80)&(sat<.30)
        photo_valid=bilinear(region.astype(float),q).reshape(yy.shape)>.5
        refmask &= photo_valid
        measurements=dict(title=title,pitch_mm=.5,world_yz_bounds_m=[y0,y1,z0,z1],
                          definitions=definition,render_area_share=float(worn[valid].mean()),
                          photo_area_share=float(refmask[photo_valid].mean()) if photo_valid.any() else 0,
                          render_components_mm2=component_sizes(worn),photo_components_mm2=component_sizes(refmask),
                          limits='Planar side rectification uses receiver corners; wood/magazine depth and photographic lighting limit correspondence. Photo classification is not an authored wear channel.')
        evidence.append(measurements)
        canvas=Image.new('RGB',(1800,790),'#ebede9');d=ImageDraw.Draw(canvas)
        d.text((25,12),title+' / two-dimensional evidence, 0.5 mm per grid cell',font=FONT,fill='black')
        scale=min(850/yy.shape[1],260/yy.shape[0]);size=(round(yy.shape[1]*scale),round(yy.shape[0]*scale))
        for k,(rgb,mask,label) in enumerate([(observed,worn,'Exported GLB / actual shipping maps'),(reference,refmask,'Locally white-balanced used photo')]):
            x=25+k*900;d.text((x,55),label,font=SMALL,fill='black')
            pic=Image.fromarray(np.uint8(np.clip(np.flipud(rgb),0,255))).resize(size)
            binary=Image.fromarray(np.uint8(np.flipud(mask))*255).resize(size,Image.Resampling.NEAREST)
            canvas.paste(pic,(x,85));canvas.paste(binary.convert('RGB'),(x,365))
            areas=measurements['render_components_mm2' if k==0 else 'photo_components_mm2']
            d.text((x,650),'Largest connected areas mm²: '+str(np.round(areas[:6],1).tolist()),font=SMALL,fill='black')
        d.text((25,690),definition,font=SMALL,fill='black')
        d.text((25,725),'Planar scale estimate from receiver corners. Lighting/thresholds differ; masks preserve topology without morphology filtering.',font=SMALL,fill='black')
        d.text((25,758),'The broad flats and sheltered returns must remain protected. Original scratch histories are intentionally different.',font=SMALL,fill='black')
        canvas.save(out/(title.lower().replace(',','').replace(' ','-')+'-wear-2d.jpg'),quality=94)
    (out/'site-wear-values.json').write_text(json.dumps(evidence,indent=2))
    print('SITE WEAR',len(evidence),'independent 2D comparisons')

if __name__=='__main__':main()
