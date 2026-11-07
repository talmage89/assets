"""Run the independent audits serially in one factory-startup process."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import check,audit_delivery,measure_layout,check_external,check_gate
check.main()
audit_delivery.main()
measure_layout.main()
check_external.check(Path('export/final'))

check_gate.check(202)
