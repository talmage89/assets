"""Structural grammar checks and negative controls, independent of Blender.

These prove constraints on authored plans and analytic roof partitions. The
separate mesh audit casts rays into built surfaces and checks the actual GLB.
Neither is a structural engineering calculation or a full code review.
"""
import argparse
import json
import math
from pathlib import Path
from plan import generate,openings,wall_frame,roof_blocks,roof_faces,roof_junctions,serialize


def check(plan):
    windows=openings(plan);main,garage=plan['blocks'];roof=[plan['roof_envelope']] if plan.get('roof_envelope') else roof_blocks(plan['blocks'])
    faces=roof_faces(roof);junctions=roof_junctions(roof)
    errors=[]
    for o in windows:
        b=next(b for b in plan['blocks'] if b.name==o['block'])
        origin,t,n,l=wall_frame(b,o['face'])
        margin=o['w'] if o['shutters'] else o['w']/2+.12
        if o['u']-margin<.03 or o['u']+margin>l-.03:errors.append(o['id']+' trim crosses corner')
        stair=o['role']=='stairwell landing'
        floor=b.upper_floor if o['z']>3.0 else b.floor
        plate=b.plate if o['z']>3.0 else b.first_plate
        if not stair and (o['z']<floor-.001 or o['z']+o['h']+.18>plate):errors.append(o['id']+' floor/header clearance')
        if stair and not o['z']<b.upper_floor<o['z']+o['h']:errors.append('Stairwell window must show its intermediate level')
        for s in (-1,1):
            x=origin[0]+t[0]*(o['u']+s*o['w']/2);y=origin[1]+t[1]*(o['u']+s*o['w']/2)
            if o['z']+o['h']+.13>b.height(x,y)-.14:errors.append(o['id']+' hits roof')
    for i,a in enumerate(windows):
        for c in windows[i+1:]:
            if (a['block'],a['face'])!=(c['block'],c['face']):continue
            hw=lambda o:o['w']+(.11 if o['shutters'] else .12) if o['shutters'] else o['w']/2+.12
            overlaps_x=abs(a['u']-c['u'])<hw(a)+hw(c)
            overlaps_z=min(a['z']+a['h']+.10,c['z']+c['h']+.10)>max(a['z']-.08,c['z']-.08)
            if overlaps_x and overlaps_z:errors.append(a['id']+' trim overlaps '+c['id'])
    # Actual polygons: no centroid may be lower than a neighboring roof.
    samples=0
    for row in faces:
        p=row['plane'];poly=row['polygon'];cx=sum(v[0] for v in poly)/len(poly);cy=sum(v[1] for v in poly)/len(poly)
        for vx,vy in poly:
            x=.8*cx+.2*vx;y=.8*cy+.2*vy;z=p[0]*x+p[1]*y+p[2]
            expected=max(b.height(x,y) for b in roof if b.contains(x,y,b.overhang+1e-6))
            if abs(z-expected)>1e-5:errors.append('Buried roof face')
            samples+=1
    slopes=[]
    for row in junctions:
        if row['kind']!='valley':continue
        a,c=row['points'];slope=abs(a[2]-c[2])/math.dist(a[:2],c[:2]);slopes.append(slope)
        if slope<.019:errors.append('Valley without positive drainage')
    # Landing/steps and porch-vs-entry are constrained by their actual plan.
    porch=plan['porch'];riser=porch.floor/3
    if riser>.19685 or .3048<.254:errors.append('Stair sanity limits')
    if porch.depth<.9144:errors.append('Entry landing too shallow')
    if plan['spec']['type']=='ranch':
        if plan['spec']['garage']['kind']=='carport' and any(o['block']=='Garage' for o in windows):errors.append('Closed carport opening')
        if not any(o.get('style')=='picture' for o in windows):errors.append('Missing picture window')
        for o in windows:
            if o['block']=='Main' and o['face']=='front' and o['kind']=='window':
                soffit=main.eave-main.pitch*main.overhang-.204
                if o['z']+o['h']+.065>soffit:errors.append('Front casing crosses low soffit')
                for post in (porch.x0+.14,porch.x1-.14):
                    if abs((main.x0+o['u'])-post)<o['w']/2+.13:errors.append('Entry post overlaps front window')
        if errors:raise AssertionError(f"seed {plan['seed']}: "+'; '.join(sorted(set(errors))))
        return dict(seed=plan['seed'],type='ranch',openings=len(windows),roof_faces=len(faces),roof_samples=samples,valley_min_fall=min(slopes) if slopes else None)
    # The garage room is three shallow interior steps below the main upper
    # floor. Its connection is reserved in the overlap, without interior mesh.
    if (main.upper_floor-garage.upper_floor)/3>.19685 or plan['spec']['garage']['overlap']<3*.254:
        errors.append('Upper floor connection cannot fit three steps')
    pmax=max(porch.height(x,y) for x,y in porch.domain())
    # For this portico the ridge point is interior, evaluate that too.
    pmax=max(pmax,porch.height(porch.cx,porch.cy))
    for o in windows:
        if o['block']=='Main' and o['face']=='front' and o['z']>3 and abs(o['u']-main.width/2)<1.8:
            if pmax+.15>o['z']:errors.append('Porch roof crosses upper casing')
    if errors:raise AssertionError(f"seed {plan['seed']}: "+'; '.join(sorted(set(errors))))
    return dict(seed=plan['seed'],openings=len(windows),roof_faces=len(faces),roof_samples=samples,
                valley_min_fall=min(slopes) if slopes else None,crickets=sum(b.roof=='cricket' for b in roof))


def main():
    p=argparse.ArgumentParser();p.add_argument('--count',type=int,default=1000);p.add_argument('--out',type=Path,default=Path('build/plan-sweep.json'));a=p.parse_args()
    rows=[check(generate(seed)) for seed in range(a.count)]
    ranch_rows=[check(generate(seed,house_type='ranch')) for seed in range(a.count)]
    # Wrong dimensions and unsupported stories must be rejected, not clamped.
    negative=[]
    for override in (dict(main=dict(width=8.0)),dict(garage=dict(stories=1)),dict(main=dict(pitch=.9)),dict(garage=dict(side='rear')),
                     dict(cladding=dict(Main=dict(front='unsupported'))),dict(colors=dict(trim=[1,1,1]))):
        try:generate(27,override)
        except AssertionError:negative.append(override)
        else:raise AssertionError('Invalid plan accepted')
    ranch_negative=[]
    for override in (dict(main=dict(stories=2)),dict(main=dict(pitch=.5)),dict(main=dict(overhang=.2)),dict(main=dict(width=25)),
                     dict(garage=dict(cars=0)),dict(garage=dict(kind='floating')),dict(garage=dict(entry='rear')),
                     dict(floor=.9),dict(wall_mix='stucco'),dict(window_update='glass_block'),dict(chimney='unsupported'),dict(colors=dict(door=[1,1,1]))):
        try:generate(12,override,house_type='ranch')
        except AssertionError:ranch_negative.append(override)
        else:raise AssertionError('Invalid ranch plan accepted: '+str(override))
    assert serialize(generate(27))==serialize(generate(27)), 'Plan repeatability'
    out=dict(passed=True,seeds=a.count,ranch_rows=ranch_rows,rows=rows,rejected_negative_controls=negative,ranch_rejected_negative_controls=ranch_negative,
             scope='Plan grammar and analytic partitions only; separate actual-surface checks required')
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2))
    print('PLAN_SWEEP',a.count,'passed; negative controls',len(negative))


if __name__=='__main__':main()
