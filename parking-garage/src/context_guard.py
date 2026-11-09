"""CLI for the owner's 0.1% triangle / 1 mm native-car cache ruling."""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from context_geometry import capture,compare,digest


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--record',action='store_true')
    ap.add_argument('--out',type=Path);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.record:
        assert not a.baseline.exists(),'Never replace an accepted surface baseline'
        a.baseline.write_text(json.dumps(capture(a.source),separators=(',',':'))+'\n')
        print('RECORDED ACCEPTED CAR',a.source,a.baseline.stat().st_size,flush=True);return
    reference=json.loads(a.baseline.read_text())
    try:report=compare(reference,a.source,enforce=False)
    except (AssertionError,ValueError) as error:
        report=dict(passed=False,reference_sha256=reference['sha256'],actual_sha256=digest(a.source),error=str(error))
    if a.out:a.out.write_text(json.dumps(report,indent=2)+'\n')
    print('NATIVE SURFACE TOLERANCE', 'PASS' if report['passed'] else 'REJECT',report,flush=True)
    assert report['passed'],report


if __name__=='__main__':main()
