"""Independent parking counts, occupied-lot routes and reversible park maneuver.

Sweeps rectangular bodies on sampled circular arcs, not vehicle dynamics.
The passenger-car park/back-out and pickup circulation have distinct envelopes.
"""
import json
import math
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from strip_plan import generate,PROOF_SEEDS,FT,GRID,required_accessible
from check_plan import rect,separation


def line(a,b,yaw,spacing=.18):
    n=max(1,math.ceil(math.dist(a,b)/spacing))
    return [(a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n,yaw) for i in range(n+1)]


def crossing(p,y):
    left,right=p['side_drive_centers'];R=4.8;D=p['lot'][1]
    if p.get('cross_aisle') and abs(y-p['aisle_centers'][0])<.001:
        result=line((left,-D/2-3.3),(left,y-R),0)
        def arc(start,a,b):
            radius=R if b>a else -R;n=round(abs(b-a));t0=math.radians(a)
            for i in range(n+1):
                angle=a+(b-a)*i/n;t=math.radians(angle)
                result.append((start[0]+radius*(math.cos(t)-math.cos(t0)),start[1]+radius*(math.sin(t)-math.sin(t0)),angle))
            return result[-1][:2]
        end=arc((left,y-R),0,-90);cx=p['cross_aisle']['center_x'];lower=p['aisle_centers'][1]
        result+=line(end,(cx-R,y),-90);end=arc((cx-R,y),-90,-180)
        result+=line(end,(cx,lower+R),-180);end=arc((cx,lower+R),-180,-90)
        result+=line(end,(right-R,lower),-90);end=arc((right-R,lower),-90,-180)
        result+=line(end,(right,-D/2-3.3),180)
        return result
    result=line((left,-D/2-3.3),(left,y-R),0)
    for a in range(91):
        t=math.radians(a);result.append((left+R*(1-math.cos(t)),y-R+R*math.sin(t),-a))
    result+=line((left+R,y),(right-R,y),-90)
    for a in range(91):
        t=math.radians(a);result.append((right-R+R*math.sin(t),y-R+R*math.cos(t),-90-a))
    result+=line((right,y-R),(right,-D/2-3.3),180)
    return result


def obstacles(p,omit=None):
    out=[]
    for i,s in enumerate(p['stalls']):
        if i==omit:continue
        out.append((f'occupied stall {i}',rect(((s['x0']+s['x1'])/2,(s['y0']+s['y1'])/2),1.85,4.70,0)))
    for i,isl in enumerate(p['islands']):
        a,b,c,d=isl['bounds'];out.append((f'island {i}',rect(((a+b)/2,(c+d)/2),b-a,d-c,0)))
    for m in p['modules']:
        # Module-local front is transformed independently to a footprint.
        from strip_plan import transform
        center=transform((0,m['depth']/2),m['origin'],m['yaw'])
        out.append((m['id'],rect(center,m['width'],m['depth'],m['yaw'])))
    b=p['building'];rowwidth=sum(m['width'] for m in p['modules'] if not m['wing'])
    out.append(('front covered walk',rect((b['left']+rowwidth/2,b['front']-p['walk']/2),rowwidth,p['walk'],0)))
    if p['elbow']:
        a,b,c,d=p['elbow']['bounds'];out.append(('elbow',rect(((a+b)/2,(c+d)/2),b-a,d-c,0)))
        wing_length=sum(m['width'] for m in p['modules'] if m['wing'])
        out.append(('wing covered walk',rect((a-p['walk']/2,c-wing_length/2),p['walk'],wing_length,0)))
    b=p['building'];out.append(('dumpster yard',rect((b['left']-2.75,b['rear']-3.1),4.5,3.6,0)))
    out.append(('pylon footing',rect(p['sign_center'],4.0,1.02,0)))
    return out


def sweep(p,poses,width,length,omit=None):
    obs=obstacles(p,omit);bounds=[(name,poly,(min(x for x,y in poly),max(x for x,y in poly),min(y for x,y in poly),max(y for x,y in poly))) for name,poly in obs]
    smallest=100.;closest=None;violations=[];W,D=p['lot']
    for i,(x,y,yaw) in enumerate(poses):
        car=rect((x,y),width,length,yaw)
        for name,poly,(a,b,c,d) in bounds:
            if x<a-6 or x>b+6 or y<c-6 or y>d+6:continue
            gap=separation(car,poly)
            if gap<smallest:smallest=gap;closest=name
            if gap<-.0001:violations.append(dict(sample=i,object=name,penetration_sat_m=-gap))
        for xx,yy in car:
            if abs(xx)>W/2-4*FT or yy>D/2-4*FT:violations.append(dict(sample=i,object='property landscaping'))
            if yy<-D/2 and not any(abs(xx-v)<12*FT-.02 for v in p['side_drive_centers']):violations.append(dict(sample=i,object='street opening'))
    return dict(passed=not violations,samples=len(poses),minimum_separating_gap_m=smallest,nearest_obstacle=closest,violations=violations[:12])


def traffic(p):
    # Both double-loaded aisles and the rear service drive connect to both
    # street openings. The L's front route uses the reserved cross aisle.
    routes={}
    for name,y in (('front_aisle',p['aisle_centers'][0]),('street_aisle',p['aisle_centers'][1]),('rear_drive',sum(p['rear_drive'])/2)):
        path=crossing(p,y);routes[name]=sweep(p,path,2.14,5.70)
    R=4.8;ay=p['aisle_centers'][0];park=None
    # Find a representative ordinary stall with a comfortable demonstrated
    # approach, keeping every other space occupied. This does not certify
    # every parking maneuver at every individual stall.
    for chosen,s in enumerate(p['stalls']):
        if s['row']!=0 or s['accessible']:continue
        x=(s['x0']+s['x1'])/2;y=(s['y0']+s['y1'])/2;path=[]
        for a in range(91):
            t=math.radians(a);path.append((x-R+R*math.sin(t),ay+R*(1-math.cos(t)),-90+a))
        path+=line((x,ay+R),(x,y),0)
        poses=path+list(reversed(path));park=sweep(p,poses,1.85,4.70,chosen)
        if park['passed'] and park['minimum_separating_gap_m']>.30:break
    assert park and park['passed'] and park['minimum_separating_gap_m']>.30,'No representative parking approach'
    park.update(stall=chosen,center=(x,y),radius_m=R,forward_samples=len(path),reverse_samples=len(path),body_m=(1.85,4.70))
    return dict(passed=all(r['passed'] for r in routes.values()) and park['passed'],pickup_routes=routes,passenger_car_parking=park,
                scope='Actual plan polygons and occupied 1.85 x 4.70m cars; pickup 2.14 x 5.70m through routes, 4.8m center arcs, <=.18m straights / 1 degree turns. Park/back-out is reversible kinematic geometry, not a tire/suspension/traffic-capacity certification.')


def plan_check(p):
    stalls=p['stalls'];aisles=p['access']
    for i,s in enumerate(stalls):
        for t in stalls[i+1:]:
            dx=min(s['x1'],t['x1'])-max(s['x0'],t['x0']);dy=min(s['y1'],t['y1'])-max(s['y0'],t['y0'])
            assert min(dx,dy)<1e-6,'Overlapping painted spaces'
        for t in aisles:
            dx=min(s['x1'],t['x1'])-max(s['x0'],t['x0']);dy=min(s['y1'],t['y1'])-max(s['y0'],t['y0'])
            assert min(dx,dy)<1e-6,'Parking in an access aisle'
    for a,b in ((p['rows'][1],p['rows'][0]),(p['rows'][3],p['rows'][2])):assert abs(b['y0']-a['y1']-24*FT)<1e-6
    for d in p['driveways']:assert abs(d['center'][0]/GRID-round(d['center'][0]/GRID))<1e-6
    assert sum(s['accessible'] for s in stalls)>=required_accessible(len(stalls))
    return True


def diagram(p,path):
    from PIL import Image,ImageDraw,ImageFont
    from kit.fonts import find_font
    im=Image.new('RGB',(1450,1100),'#edece6');dr=ImageDraw.Draw(im);W,D=p['lot'];scale=min(1320/W,930/D)
    def xy(x,y):return (725+x*scale,570-y*scale)
    def box(bounds,color,outline='#6a6a61'):
        a,b,c,d=bounds;dr.rectangle((*xy(a,d),*xy(b,c)),fill=color,outline=outline,width=1)
    box((-W/2,W/2,-D/2,D/2),'#55585a')
    for m in p['modules']:
        from strip_plan import transform
        poly=[transform(v,m['origin'],m['yaw']) for v in ((-m['width']/2,0),(m['width']/2,0),(m['width']/2,m['depth']),(-m['width']/2,m['depth']))]
        dr.polygon([xy(x,y) for x,y in poly],fill='#b6a994',outline='black')
    if p['elbow']:box(p['elbow']['bounds'],'#b6a994')
    for s in p['stalls']:box((s['x0'],s['x1'],s['y0'],s['y1']),'#325b71' if s['accessible'] else '#696b6c','#c6c4b5')
    for a in p['access']:box((a['x0'],a['x1'],a['y0'],a['y1']),'#a3a691')
    for i in p['islands']:box(i['bounds'],'#536b3c')
    for index,y in enumerate((p['aisle_centers'][1],sum(p['rear_drive'])/2)):
        poses=crossing(p,y);dr.line([xy(x,y) for x,y,a in poses],fill=('#e7ba68','#72bfba')[index],width=4)
        for x,y,a in poses[::35]:dr.polygon([xy(xx,yy) for xx,yy in rect((x,y),2.14,5.70,a)],outline=('#e7ba68','#72bfba')[index],width=2)
    font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),22)
    dr.text((40,25),f"Seed {p['seed']}  |  {W/FT:.0f} x {D/FT:.0f} ft  |  {p['stall_count']} stalls  |  {p['parking_ratio']:.2f} / 1,000 sq ft",font=font,fill='#232a28')
    dr.text((40,1060),'9 x 18 ft stalls; 24 ft aisles / side / rear drive. Gold: pickup street-aisle loop. Teal: rear service loop.',font=font,fill='#232a28')
    im.save(path,quality=92)


def main():
    out=Path('build/strip');out.mkdir(parents=True,exist_ok=True)
    for seed in range(1000):plan_check(generate(seed))
    negative=[dict(style='glass_box'),dict(lot_ft=(190,200)),dict(depth_ft=40),dict(wall='vinyl'),dict(bay_ft=12),dict(shape='U'),dict(bays=25)]
    for control in negative:
        try:generate(201,control)
        except (AssertionError,ValueError):continue
        raise AssertionError('Invalid control accepted '+str(control))
    rows={}
    for seed in PROOF_SEEDS:
        p=generate(seed);rows[str(seed)]=traffic(p);diagram(p,out/f'plan-{seed}.jpg')
        print(seed,json.dumps(rows[str(seed)]))
    report=dict(passed=all(r['passed'] for r in rows.values()),plan_sweep=1000,negative_controls=len(negative),traffic=rows)
    (out/'plan-check.json').write_text(json.dumps(report,indent=2)+'\n');assert report['passed'],'See plan-check.json'
    print('STRIP PLANS: 1000 nonoverlapping parking plans; 7 invalid controls rejected; four occupied-lot traffic proofs passed')


if __name__=='__main__':main()
