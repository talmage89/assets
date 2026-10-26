from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'fences/src')]
from library_review import main
if __name__=='__main__':main(Path(__file__).resolve().parents[1],'WhitePicket','PicketAssembly')
