"""Contact sheets and image-range receipts, never committed docs."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import review_sheet
from kit.image_io import srgb_to_linear


def verify_receipt(r):
    digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    assert digest(r['output'])==r['sha256']
    path=Path(r['source']);assert digest(path)==r['source_sha256']
    for uri,value in {**r.get('source_buffer_sha256',{}),**r.get('images',{})}.items():assert digest(path.parent/uri)==value
    for uri,value in r.get('source_finish_images',{}).items():assert digest(uri)==value
    if 'calibration_sha256' in r:assert digest('build/lookdev/matches/calibration.json')==r['calibration_sha256']


def main():
    a=argparse.ArgumentParser();a.add_argument('--pass-name',default='lookdev-checkpoint');args=a.parse_args();folder=Path('renders')/args.pass_name
    receipts=json.loads((folder/'views.json').read_text());rows=[];ranges=[]
    for seed in (101,202):
        selected=[r for r in receipts if r['seed']==seed]
        for r in selected:
            verify_receipt(r);path=Path(r['output'])
            arr=np.asarray(Image.open(path).convert('RGB'))/255;Y=srgb_to_linear(arr)@np.array([.2126,.7152,.0722])
            ranges.append(dict(seed=seed,name=r['name'],display_luma_percentiles=np.percentile(arr@np.array([.2126,.7152,.0722]),[1,5,50,95,99]).tolist(),
                linear_Y_percentiles=np.percentile(Y,[1,5,50,95,99]).tolist(),clipped_rgb_fraction=float(np.mean(np.any(arr>=1,axis=2))),black_rgb_fraction=float(np.mean(np.all(arr<.008,axis=2)))))
        paths=[Path(r['output']) for r in selected];rows.extend([paths[i:i+3] for i in range(0,len(paths),3)])
    for suffix in ('-matches','-source-matches'):
        pairfolder=Path('renders')/(args.pass_name+suffix)
        if pairfolder.exists():
            for r in json.loads((pairfolder/'views.json').read_text()):verify_receipt(r)
            rows.extend([[p] for p in sorted(pairfolder.glob('*-pair.jpg'))])
    review_sheet(rows,folder/'contact.jpg',width=2400,title='Parking garages / exported baked checkpoint / no docs')
    out=Path('build/lookdev')/(args.pass_name+'-image-values.json');out.write_text(json.dumps(ranges,indent=2)+'\n')
    # Within-photo value comparison, balanced on bare column concrete. These
    # are displayed image values under unequal lighting, not measured albedos.
    rois={'column':[1210,1800,1280,1900],'soffit':[2600,280,2950,430],'floor':[2120,2180,2340,2320]}
    pairfolder=Path('renders')/(args.pass_name+'-matches');render=pairfolder/'precast.png'
    if render.exists():
        photo=Image.open('build/lookdev/matches/precast-balanced.jpg').convert('RGB');im=Image.open(render).convert('RGB');report={}
        for name,roi in rois.items():
            x0,y0,x1,y1=roi;scaled=[round(x0*im.width/photo.width),round(y0*im.height/photo.height),round(x1*im.width/photo.width),round(y1*im.height/photo.height)]
            def stats(image,rect):
                a=np.asarray(image.crop(rect))/255;linear=srgb_to_linear(a);return dict(median_srgb=np.median(a.reshape(-1,3),axis=0).tolist(),median_linear_Y=float(np.median(linear@np.array([.2126,.7152,.0722]))))
            report[name]=dict(photo=stats(photo,roi),render=stats(im,scaled),native_photo_roi=roi)
        (folder/'precast-values.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
