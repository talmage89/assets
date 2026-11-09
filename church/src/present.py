"""Finish the local checkpoint receipts and contacts after its serial capture."""
import subprocess,sys
from pathlib import Path
import comparisons,resources,review,presentation_check


def main():
    tool=Path(__file__).resolve().parents[2]/'kit/photo_match.py'
    for folder in ('matches','source-matches'):
        subprocess.run([sys.executable,str(tool),'compose','--calibration','build/matched-cameras.json',
            '--renders',f'renders/{folder}','--out',f'renders/{folder}'],check=True)
    previous=Path('renders/before-look/checkpoint/101/hero.png').exists()
    if previous:comparisons.main('renders/final')
    else:print('Cold build: previous-revision captures are unavailable; current exports are audited')
    resources.main();review.main();presentation_check.main(require_before=previous)
    from last_evidence import main as evidence
    evidence()


if __name__=='__main__':main()
