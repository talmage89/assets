"""Thirty-Hz feed audit for every action, insertion and partial rack."""
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from guns.common.feed_strips import main
import interface
if __name__=='__main__':main(BASE,interface)
