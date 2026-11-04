"""Audit this branch's source history without retaining private identifiers."""
import json
import re
import subprocess
from pathlib import Path


def audit():
    # These listing CDNs use property/listing numbers in their image paths.
    forbidden = re.compile(r'https://[^\s|]*(?:cdn-redfin\.com|rdcpix\.com)[^\s|]*')
    revision = '965da63..HEAD'
    patch = subprocess.check_output(['git', 'log', '-p', revision], text=True)
    assert not forbidden.search(patch), 'Listing identifier remains in branch patches'
    commits = subprocess.check_output(['git', 'rev-list', revision], text=True).splitlines()
    for commit in commits:
        tree = subprocess.check_output(['git', 'show', commit + ':houses/refs/SOURCES.md'], text=True)
        assert not forbidden.search(tree), 'Listing identifier remains in a historical source table'
    result = dict(passed=True, revision=revision, commits=len(commits),
                  removed_sources=['split-builder-used-pa.jpg', 'split-builder-used-oh.jpg',
                                   'split-oh-side-b.jpg', 'split-used-bay.jpg',
                                   'split-foyer-used-pa.webp'],
                  scope='Every branch patch and every historical source table; source CDN URLs carrying listing identifiers')
    out = Path('build/split/delivery/privacy.json');out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('SPLIT_PRIVACY', len(commits), 'branch commits, no identifying listing URLs')
    return result


if __name__ == '__main__':
    audit()
