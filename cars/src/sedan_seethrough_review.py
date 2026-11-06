"""Count resolved magenta pixels in an independently manufactured silhouette.

The continuous die is recorded before panel reveals, glazing and optical cuts;
its actual wheel arches remain exterior negative space. Spoke holes and the air
around a mirror stalk therefore never become fictitious body holes. This is not
a mask made from the tested export's coverage. Before/after share the exact
intersection of their independently generated silhouettes. Its exterior is
refined against actual coverage after closing 1–2 pixel reveal ribbons and
filling enclosed holes, then guarded by two pixels for sampling ambiguity.
This retains internal gaps while respecting a recessed lens at the silhouette.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
VIEWS=['front','side','rear','top','front_three_quarter','rear_three_quarter']


def filled_silhouette(coverage):
    """Fill enclosed voids after closing 1–2 pixel reveal ribbons.

    Run-length components retain the actual exterior contour; this corrects
    the uncut die where a recessed optical cover defines the final silhouette.
    It never derives the interior test mask from the export's unfilled holes.
    """
    closed=np.array(Image.fromarray(coverage.astype('uint8')*255).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)))>0
    empty=~closed;h,w=empty.shape;parent=[];external=[];rows=[];previous=[]
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for y,row in enumerate(empty):
        cuts=np.flatnonzero(np.diff(np.r_[False,row,False]));current=[];j=0
        for a,b in zip(cuts[::2],cuts[1::2]):
            k=len(parent);parent.append(k);external.append(y==0 or y==h-1 or a==0 or b==w);current.append((a,b,k))
            while j<len(previous) and previous[j][1]<=a:j+=1
            for c,d,q in previous[j:]:
                if c>=b:break
                u,v=root(k),root(q)
                if u!=v:parent[v]=u;external[u]=external[u] or external[v]
        rows.append(current);previous=current
    inside=closed.copy()
    for y,row in enumerate(rows):
        for a,b,k in row:
            if not external[root(k)]:inside[y,a:b]=True
    return np.array(Image.fromarray(inside.astype('uint8')*255).filter(ImageFilter.MinFilter(5)))>0


def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--before');p.add_argument('--out',required=True);p.add_argument('--diagnose',action='store_true');a=p.parse_args()
    folder=Path(a.renders);before=Path(a.before) if a.before else None;out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    metadata=json.loads((folder/'shots.json').read_text());old=json.loads((before/'shots.json').read_text()) if before else None
    report=dict(method=__doc__.strip(),samples_per_pixel=16,external_contour_guard_pixels=2,narrow_reveal_closing_radius_pixels=1,threshold='R/B >= 240, G <= 12 in a Standard/sRGB emission render of a (1,0,1) world; actual glazing white; adjacent gaps remain tested',views={})
    for name in VIEWS:
        envelope=np.array(Image.open(folder/(name+'-envelope.png')).convert('RGBA'))[:,:,3]>=128
        if before:
            for key in ['location','target','ortho','lens','width','height','samples']:
                if metadata[name].get(key)!=old[name].get(key):raise ValueError('Comparison cameras differ: '+name+' '+key)
            envelope&=np.array(Image.open(before/(name+'-envelope.png')).convert('RGBA'))[:,:,3]>=128
        reference=np.array(Image.open(folder/(name+'.png')).convert('RGB'))
        direct=(reference[:,:,0]>=240)&(reference[:,:,1]<=12)&(reference[:,:,2]>=240)
        mask=(np.array(Image.fromarray(envelope.astype('uint8')*255).filter(ImageFilter.MinFilter(3)))>0)&filled_silhouette(~direct)
        Image.fromarray(mask.astype('uint8')*255).save(out/(name+'-silhouette-mask.png'))
        rows={}
        for label,root,meta in [('before',before,old),('after',folder,metadata)]:
            if root is None:continue
            path=root/(name+'.png');pixels=np.array(Image.open(path).convert('RGB'))
            magenta=(pixels[:,:,0]>=240)&(pixels[:,:,1]<=12)&(pixels[:,:,2]>=240)
            leak=magenta&mask;ys,xs=np.where(leak)
            rows[label]=dict(magenta_pixels=int(leak.sum()),source_sha256=meta[name]['source_sha256'],render_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),envelope_sha256=meta[name]['envelope_sha256'],first_leak_pixels_xy=[[int(x),int(y)] for x,y in zip(xs[:30],ys[:30])])
            display=pixels.copy();display[leak]=(255,255,0);Image.fromarray(display).save(out/(name+'-'+label+'-leaks.png'))
        report['views'][name]=dict(tested_pixels=int(mask.sum()),**rows)
        print('SEE_THROUGH',name,rows.get('before',{}).get('magenta_pixels','—'),'->',rows['after']['magenta_pixels'],flush=True)
    report['passed']=all(row['after']['magenta_pixels']==0 for row in report['views'].values())
    (out/'counts.json').write_text(json.dumps(report,indent=2))
    if not report['passed'] and not a.diagnose:raise SystemExit('Direct background visible through the body; see '+str(out/'counts.json'))
if __name__=='__main__':main()
