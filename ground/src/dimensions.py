"""Meters; municipal section plus original repeatable plan choices."""
GRID = .1524                       # 6 in construction subgrid
PANEL = 10*GRID                     # 5 ft
BAY = 20*GRID                       # 10 ft curb / two sidewalk panels
LENGTH = 40*GRID                    # 20 ft road module
ASPHALT_HALF = 24*GRID               # 12 ft from crown to asphalt edge
GUTTER = 3*GRID                      # 18 in exposed pan
CURB = GRID                         # 6 in total back thickness
FACE = ASPHALT_HALF+GUTTER           # 13.5 ft from center to curb flow line
BACK = FACE+CURB                     # 14 ft back of curb
RADIUS = 30*GRID                     # 15 ft curb return at nominal face
CORE = FACE+RADIUS                   # 28.5 ft intersection half envelope
STRIP = 12*GRID                      # 6 ft future planting allowance
WALK_IN = BACK+STRIP                 # 20 ft sidewalk front edge
WALK_OUT = WALK_IN+PANEL              # 25 ft back edge
CURB_HEIGHT = GRID                   # 6 in from flow line
ROAD_EDGE = .00635                   # 1/4 in gutter/asphalt lip rise
CROWN_SLOPE = 1/48                   # municipal 1/4 in per foot
WALK_SLOPE = .01                     # 1%, toward gutter
ASPHALT_TILE = LENGTH                # 6.096 m
CONCRETE_TILE = BAY                  # 3.048 m
LAWN_TILE = BAY                      # 3.048 m, 1.49 mm delivered texels
YARD_GRADE = CURB_HEIGHT+PANEL*WALK_SLOPE
MANHOLE_COVER = .6096                # 24 in lid diameter
MANHOLE_FRAME = .635                 # 25 in upper frame diameter
MANHOLE_PATCH = 1.12                 # authored resurfacing cut diameter
DECAL_OFFSET = .002                  # 2 mm above evaluated surface

def road_z(x):
    return ROAD_EDGE + (ASPHALT_HALF-abs(x))*CROWN_SLOPE


def transition_stations(length,width):
    """Identical curb/wing stations, including both ends of the clear opening."""
    return sorted(set([-length/2+(length-width)/2*i/8 for i in range(9)]+
                      [width/2+(length-width)/2*i/8 for i in range(9)]))
