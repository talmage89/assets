"""Whole-park photographic comparisons; kept as the public Make entry point."""
import sys
from park_matches import solve,compose

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='compose':compose(sys.argv[2])
    else:solve()
