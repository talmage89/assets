"""Reference footprint masks and independent exported-layout measurements.

Masks measure published drawings only. They are not generator geometry inputs.
Color masks and manually read blueprint outlines carry explicit uncertainty.
"""
import sys,json,math,argparse,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))

def reference_measurements():
    folder=Path('renders/research');folder.mkdir(parents=True,exist_ok=True);out={}
    for name,page,width in [('columbia',10,2000),('los-altos',2,2200),('ann-arbor',18,2400)]:
        target=Path('build')/(name+'-plan')
        subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to',str(width),'-png','-singlefile','refs/'+name+'.pdf',str(target)],check=True,stdout=subprocess.DEVNULL)
        im=Image.open(target.with_suffix('.png')).convert('RGB');w,h=im.size
        frac=(.36,.32,.72,.68) if name=='columbia' else (.11,.09,.51,.47) if name=='los-altos' else (.215,.075,.51,.52)
        holes=[]
        im=im.crop(tuple(int(v*(w if k%2==0 else h)) for k,v in enumerate(frac)));a=np.asarray(im)/255
        if name=='columbia':
            boundary=[(53,150),(173,150),(173,138),(270,138),(270,174),(382,174),(390,210),(423,210),(423,175),(462,175),(462,150),(506,150),(506,265),(469,279),(469,321),(506,345),(505,461),(482,532),(442,578),(396,595),(365,562),(336,584),(305,605),(241,638),(179,632),(121,609),(76,573),(53,541)]
            feature=((a[:,:,2]>a[:,:,1]*1.1)|(a[:,:,0]>a[:,:,1]*1.1)|((a[:,:,0]>.65)&(a[:,:,1]>.65)&(a[:,:,2]<.4)))
            # 1in=60ft on an 11in-tall page rendered at 2000px.
            px_m=(2000/11)/(60*.3048)
            gaps=[((241,350),(253,402),'pyramid toe to funbox toe'),((156,383),(172,442),'funbox to flybox'),((169,539),(185,473),'transition inside toe to flybox')]
            uncertainty=5
        elif name=='los-altos':
            boundary=[(40,258),(269,103),(375,100),(476,112),(598,69),(792,89),(784,211),(736,306),(661,368),(628,420),(509,459),(424,477),(397,501),(342,501),(325,458),(282,435),(242,447),(203,429),(176,449),(156,447),(144,412),(72,421),(38,365)]
            # Program envelopes: raised horseshoe, huevo bump, crescent bank.
            regions=[[(272,294),(290,227),(324,178),(393,161),(486,175),(494,208),(472,242),(428,261),(431,284),(475,286),(512,315),(511,350),(470,386),(406,405),(337,391),(297,357)],
                     [(558+43*math.cos(t),233+43*math.sin(t)) for t in np.linspace(0,math.tau,80)],
                     [(584,145),(623,128),(662,141),(693,177),(702,223),(689,255),(661,266),(636,257),(647,230),(652,202),(628,179),(595,175)]]
            mask=Image.new('1',im.size);d=ImageDraw.Draw(mask)
            for region in regions:d.polygon(region,fill=1)
            feature=np.asarray(mask,dtype=bool).copy()
            # 1in=10ft, on a 36in-wide record sheet rendered 2200px wide.
            px_m=(2200/36)/(10*.3048)
            gaps=[((492,285),(521,253),'horseshoe toe to huevo'),((600,231),(646,220),'huevo to crescent inside toe')]
            uncertainty=6
        else:
            boundary=[(57,495),(67,431),(74,311),(100,239),(156,171),(242,121),(301,83),(328,34),(373,0),(469,0),(491,43),(510,89),(551,103),(611,117),(641,163),(653,226),(649,253),(685,279),(707,315),(700,408),(704,493),(240,614),(141,628),(59,652),(29,596),(33,543)]
            regions=[[(308,153),(332,126),(345,89),(349,57),(370,34),(401,30),(436,42),(457,69),(463,103),(463,144),(453,180),(430,215),(395,237),(354,246),(326,235),(307,212),(298,183)],
                     [(483,179),(485,148),(499,124),(524,118),(549,122),(563,141),(573,160),(594,169),(621,184),(637,212),(637,235),(619,256),(591,261),(569,275),(548,291),(512,302),(480,299),(452,283),(439,259),(442,230),(460,210),(480,200)],
                     [(572,320),(593,305),(600,286),(618,279),(645,282),(661,299),(669,325),(664,346),(668,367),(668,393),(652,415),(626,424),(615,448),(618,469),(608,488),(586,496),(565,492),(549,477),(548,452),(548,425),(535,414),(534,390),(547,370),(573,359),(583,346)],
                     [(298,317),(302,290),(322,274),(350,275),(373,298),(394,299),(416,307),(435,330),(437,357),(425,373),(427,391),(444,404),(455,424),(458,448),(467,472),(445,484),(430,454),(426,429),(406,415),(373,402),(351,380),(343,353),(325,342),(310,338)],
                     [(113,413),(139,406),(159,430),(175,434),(182,460),(222,481),(233,510),(233,537),(213,544),(201,516),(182,508),(152,486),(144,458),(128,457),(122,481),(119,517),(134,546),(176,550),(194,577),(190,591),(153,599),(119,570),(105,531),(106,488),(111,448)],
                     [(193,288),(267,326),(254,354),(179,316)]]
            holes=[[(198,343),(236,355),(250,394),(278,435),(312,449),(324,478),(276,490),(239,475),(206,456),(184,417)],[(148,511),(176,500),(199,512),(209,540),(195,557),(165,565),(146,553),(139,533)],[(443,308),(505,309),(516,345),(482,357),(459,344)],[(122,230),(169,186),(213,158),(192,223),(167,285),(138,344),(112,398),(95,410),(102,300)]]
            mask=Image.new('1',im.size);d=ImageDraw.Draw(mask)
            for region in regions:d.polygon(region,fill=1)
            feature=np.asarray(mask,dtype=bool).copy();px_m=(2400/36)/(20*.3048)
            gaps=[((463,144),(485,148),'kidney coping to clover coping'),((601,261),(618,279),'clover to amoeba deck gap'),((269,326),(300,313),'hubba landing to snake-run lip')]
            uncertainty=7
        active=Image.new('1',im.size);ImageDraw.Draw(active).polygon(boundary,fill=1)
        for hole in holes:ImageDraw.Draw(active).polygon(hole,fill=0)
        active=np.asarray(active,dtype=bool)
        feature &= active
        annotated=im.copy();overlay=np.asarray(annotated).copy();overlay[feature]=(overlay[feature]*.55+np.array((240,130,35))*.45).astype('uint8');annotated=Image.fromarray(overlay);d=ImageDraw.Draw(annotated);d.line(boundary+[boundary[0]],fill=(220,30,30),width=2)
        for hole in holes:d.line(hole+[hole[0]],fill=(40,135,30),width=2)
        rows=[]
        for start,end,label in gaps:
            distance=math.dist(start,end)/px_m;rows.append(dict(description=label,pixels=[start,end],clear_gap_m=distance,reading_uncertainty_m=.4))
            d.line([start,end],fill=(20,170,240),width=3);d.text(start,f'{distance:.1f}m',fill=(10,10,10))
        annotated.save(folder/(name+'-measured.png'))
        out[name]=dict(pdf_page=page,coverage_percent=100*float(feature.sum()/active.sum()),coverage_uncertainty_percentage_points=uncertainty,
                       definition=('Northern bowl/street program only; major feature envelopes with their local platforms; planted/retention holes and surrounding circulation excluded' if name=='ann-arbor' else 'Major feature envelopes with local platforms; surrounding circulation not classified by grade and excluded'),
                       paved_outline_area_m2=float(active.sum()/px_m**2),feature_envelope_area_m2=float(feature.sum()/px_m**2),pixels_per_m=px_m,gaps=rows,
                       limits='Raster drawing read, not a CAD takeoff; line weights, crop and boundaries limit precision. Original park geometry is not replicated.')
    return out

def mesh_groups(path):
    from kit.gltf import GLB
    g=GLB(path);groups={}
    for ni,node in enumerate(g.json['nodes']):
        if 'mesh' not in node:continue
        root=ni
        while root in g.parents:root=g.parents[root]
        owner=g.json['nodes'][root];name=owner['name']
        if owner.get('extras',{}).get('module_kind')!='skating':continue
        T=g.world(ni)
        for prim in g.json['meshes'][node['mesh']]['primitives']:
            v=g.accessor(prim['attributes']['POSITION']);v=np.c_[v,np.ones(len(v))]@T.T;v=v[:,:3][:,[0,2,1]];v[:,1]*=-1
            ids=g.accessor(prim['indices']).reshape(-1,3);mat=g.json['materials'][prim['material']]['name']
            groups.setdefault(name,[]).append((v,ids,mat))
    return groups

def layout_measurement(seed,folder):
    info=json.loads(Path('build/park-'+str(seed)+'.json').read_text());p=info['plan'];W,D=p['skating'];scale=40
    groups=mesh_groups(folder/f'Park_{seed}.glb');size=(round(W*scale)+1,round(D*scale)+1)
    active=Image.new('1',size,1);d=ImageDraw.Draw(active)
    def pixel(x,y):return ((x+W/2)*scale,(D/2-y)*scale)
    for x0,x1,y0,y1 in p.get('landscape_cuts',[]):d.rectangle((*pixel(x0,y1),*pixel(x1,y0)),fill=0)
    mask=Image.new('1',size);draw=ImageDraw.Draw(mask);features=Image.new('1',size);fd=ImageDraw.Draw(features)
    for name,rows in groups.items():
        if name=='SkatingFlatwork':continue  # Flat asphalt underside is not a riding feature.
        for points,indices,material in rows:
            for tri in points[indices]:
                if abs(tri[:,2].mean())<.03:continue
                area=abs((tri[1,0]-tri[0,0])*(tri[2,1]-tri[0,1])-(tri[1,1]-tri[0,1])*(tri[2,0]-tri[0,0]))*.5
                if area<1e-8:continue
                draw.polygon([pixel(x,y) for x,y,z in tri],fill=1)
                circulation=name in ('UpperStreetPlaza','NorthDeckConnection') or (name.startswith('Connected_') and np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))>0 and abs(np.cross(tri[1]-tri[0],tri[2]-tri[0])[2])/np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))>.999)
                if not circulation:fd.polygon([pixel(x,y) for x,y,z in tri],fill=1)
    a=np.asarray(active,dtype=bool);m=np.asarray(mask,dtype=bool)&a
    im=Image.new('RGB',size,(204,207,201));arr=np.asarray(im).copy();arr[~a]=(75,96,56);arr[m]=(186,123,67);Image.fromarray(arr).save(Path('renders/research')/f'{seed}-terrain-coverage.png')
    def vertices(name,concrete=True):
        return np.concatenate([v for v,i,mat in groups[name] if not concrete or 'Concrete' in mat],axis=0)
    gaps=[]
    if p['type']=='poured':
        stair=next((name for name in groups if name.startswith('Stairs_')),None);ledge=min((name for name in groups if name.startswith('Ledge_18in')),key=lambda name:vertices(name)[:,1].mean())
        a0=vertices(stair);b0=vertices(ledge)
        near=float(a0[np.abs(a0[:,2])<1e-4,1].min());far=float(b0[:,1].max())
        gaps.append(dict(line='stair toe to ledge upper end',clear_gap_m=near-far,actual_surface_Y_m=[near,far]))
        bank=next(name for name in groups if name.startswith('Bank_3ft'))
        c0=vertices(bank);bt=float(c0[np.abs(c0[:,2])<1e-4,1].max());le=float(b0[:,1].min())
        gaps.append(dict(line='ledge lower end to south bank toe',clear_gap_m=le-bt,actual_surface_Y_m=[le,bt]))
        bowl=[]
        for name,rows in groups.items():
            if 'Bowl_Sector' not in name:continue
            for v,ids,mat in rows:
                if 'Concrete' not in mat:bowl.extend(v.tolist())
        bowl=np.asarray(bowl);top=bowl[:,2].max();rim=bowl[np.abs(bowl[:,2]-top)<.0001]
        for name in groups:
            if not name.startswith('Quarter_') or not name.endswith(tuple('_'+str(i) for i in p['transition_runs'][1]['indices'])):continue
            q=vertices(name);toe=q[np.abs(q[:,2])<1e-4]
            if not len(toe):continue
            x=(toe[:,0].min()+toe[:,0].max())/2;close=rim[np.abs(rim[:,0]-x)<.12]
            if not len(close):continue
            start=float(toe[:,1].min());end=float(close[:,1].max())
            gaps.append(dict(line=name+' toe to bowl lip on its approach line',clear_gap_m=start-end,actual_surface_Y_m=[start,end],line_X_m=x))
    else:
        quarter=next(name for name in groups if name.startswith('Prefab_Quarter_0'))
        q=vertices(quarter,False);toe=float(q[q[:,2]<.01,1].min());f=vertices(next(name for name in groups if name.startswith('Prefab_Funbox')),False);end=float(f[:,1].max())
        gaps.append(dict(line='north quarter toe to funbox approach',clear_gap_m=toe-end,actual_surface_Y_m=[toe,end]))
    f=np.asarray(features,dtype=bool)&a
    return dict(seed=seed,active_paved_area_m2=float(a.sum()/scale**2),nonflat_program_footprint_m2=float(m.sum()/scale**2),coverage_percent=float(m.sum()/a.sum()*100),major_feature_envelope_percent=float(f.sum()/a.sum()*100),major_feature_envelope_area_m2=float(f.sum()/scale**2),raster_pixels_per_m=scale,
                definition='Actual exported skating triangle footprint above/below grade, including raised decks, excluding landscape cutouts; raster boundary uncertainty approximately 0.5 percentage point',gaps=gaps)

def main():
    p=argparse.ArgumentParser();p.add_argument('--refs-only',action='store_true');p.add_argument('--folder',type=Path,default=Path('export/lookdev'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    result=dict(references=reference_measurements())
    if not a.refs_only:result['parks']={str(seed):layout_measurement(seed,a.folder) for seed in (101,202,303)}
    Path('build/plan-measurements.json').write_text(json.dumps(result,indent=2));print('PLAN MEASUREMENTS',json.dumps(result))

if __name__=='__main__':main()
