"""Source detail checkpoint budget. UV, atlas and GLB checks are later gates."""
BUDGETS={'SUV':65000}
# The added antenna, rather than the accepted roof or rails, sets total height.
# Rotated support barrels inflate kit.audit's transformed local AABBs in Y.
# suv_detail_check.py independently measures the actual vertex envelope at 8 mm.
BOUNDS={'SUV':dict(size=(2.117,4.600,1.735),tolerance=(.010,.050,.005))}
