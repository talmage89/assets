"""Run the independent construction/import, look and external-image gates serially."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[2])]
import check,check_look,check_external
check.check();check_look.main();check_external.main()
