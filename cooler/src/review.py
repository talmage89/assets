from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.delivery_docs import main
if __name__=='__main__':main(ROOT/'cooler')
