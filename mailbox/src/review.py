import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.delivery_docs import main
main(Path(__file__).resolve().parents[1])
