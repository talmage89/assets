"""Mixed-site repeat CLI, keeping native-car tolerance out of garage nodes."""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from context_embedded import check


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pairs',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);rows=[]
    for before,after in json.loads(a.pairs.read_text()):rows.append(dict(source=before,repeated=after,**check(Path(before),Path(after))))
    a.out.write_text(json.dumps(dict(passed=True,files=rows),indent=2)+'\n')
    print('EMBEDDED CAR TOLERANCE / EXACT NONCAR PASS',len(rows),flush=True)


if __name__=='__main__':main()
