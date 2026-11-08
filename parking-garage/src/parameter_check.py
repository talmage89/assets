"""Pure manifest checks across the supported bay/level envelope.

These verify the grammar and reservations, not unbuilt geometry. Actual surface
and moving-clearance checks separately import the two proof deliveries.
"""
import json
import math
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from plan import garage


def main():
    valid=[];rejected=0
    for system in ('precast','pt'):
        for levels in range(3,6):
            for count in range(12,25):
                try:p=garage(77,system,levels,count)
                except ValueError as error:
                    assert 'slope' in str(error) or 'ramp' in str(error),error
                    rejected+=1;continue
                spaces=p['stalls'];accessible=[s for s in spaces if s['accessible']]
                vans=[s for s in accessible if s.get('van')]
                required=next(n for limit,n in ((25,1),(50,2),(75,3),(100,4),(150,5),(200,6),(300,7),(400,8),(500,9)) if len(spaces)<=limit)
                assert len(accessible)>=required and len(vans)>=math.ceil(len(accessible)/6)
                for level in range(levels):
                    labels=[s['paint_number'] for s in spaces if s['level']==level]
                    assert len(labels)==len(set(labels)) and all(1<=int(n)<=120 for n in labels)
                assert all(abs(s['x'])+s['width']/2<p['length']/2 for s in spaces)
                assert all(abs(s['y'])+s['depth']/2<=p['width']/2+1e-8 for s in spaces)
                for i,a in enumerate(spaces):
                    for b in spaces[i+1:]:
                        if (a['level'],a['ramp'])!=(b['level'],b['ramp']):continue
                        assert abs(a['x']-b['x'])>=(a['width']+b['width'])/2-1e-8 or abs(a['y']-b['y'])>=(a['depth']+b['depth'])/2-1e-8,(system,levels,count,a['id'],b['id'])
                valid.append(dict(system=system,levels=levels,tee_count=count,capacity=len(spaces),accessible=len(accessible),vans=len(vans)))
    invalid=[dict(levels=0),dict(tee_count=0),dict(occupancy=-.01),dict(occupancy=1.01)]
    for kwargs in invalid:
        try:garage(**kwargs)
        except ValueError:continue
        raise AssertionError(('Invalid parameter accepted',kwargs))
    for system in ('precast','pt'):
        empty=garage(77,system=system,occupancy=0)
        full=garage(77,system=system,occupancy=1)
        assert not any(s['occupied'] for s in empty['stalls'])
        assert all(s['occupied'] for s in full['stalls'] if not s['accessible'])
        assert not any(s['occupied'] for s in full['stalls'] if s['accessible'])
    first,second=garage(101),garage(202)
    assert (first['length'],first['width'],first['levels'],first['system'])!=(second['length'],second['width'],second['levels'],second['system'])
    report=dict(scope='Manifest grammar/reservations only; actual imported geometry checked separately for seeds 101/202',valid_configurations=valid,rejected_short_ramps=rejected,invalid_parameters_rejected=len(invalid),occupancy_extremes_passed=True,passed=True)
    Path('build').mkdir(exist_ok=True)
    Path('build/parameter-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PARAMETER PASS',len(valid),'valid;',rejected,'short ramps rejected;',len(invalid),'invalid parameters rejected',flush=True)


if __name__=='__main__':main()
