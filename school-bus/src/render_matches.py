"""Refresh calibrated source/export comparisons in one GPU turn."""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from render import render

BASE = HERE.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=1400)
    parser.add_argument('--samples', type=int, default=48)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    for source, folder in [('export/C75-101.gltf', 'matches'),
                           ('build/bus-101.blend', 'source-matches')]:
        render(argparse.Namespace(
            source=str(BASE / source), out=str(BASE / 'renders' / folder),
            width=args.width, samples=args.samples, shots='all', school=None,
            calibration=str(BASE / 'build/calibration.json'), engine='CYCLES'))


if __name__ == '__main__':
    main()
