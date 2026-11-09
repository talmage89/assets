"""Audit the factory-color contract in an immutable car and an LOD trial.

This checks exported data routing, independently of Atlantic-only renders.
Run with ordinary Python from the family folder; the output is diagnostic.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from kit.lod_io import Document, digest


def inspect(path):
    doc = Document(path)
    paints = []
    for material in doc.data.get('materials', []):
        extras = material.get('extras', {})
        if extras.get('paint_decode') == 'reference_plus_coverage_delta':
            paints.append(dict(name=material.get('name'), extras=extras,
                               base=material['pbrMetallicRoughness']['baseColorTexture']))
    return dict(path=str(path), sha256=digest(path), paints=paints,
                stats=doc.stats())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--candidate', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    source, candidate = inspect(args.source), inspect(args.candidate)
    errors = []
    if not source['paints']:
        errors.append('Source has no documented factory decoder')
    if source['paints'] and not candidate['paints']:
        errors.append('Candidate has no factory decoder or paint-only material binding')
    report = dict(source=source, candidate=candidate, errors=errors,
                  passed=not errors,
                  scope='Exported factory metadata/binding check; not a rendered color proof')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=report['passed'], errors=errors)))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
