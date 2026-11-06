# 2009-period regulatory and warning additions

The base assembly is described in REFERENCE.md and is unchanged. These
additions use **2009 MUTCD with 2012 Revisions 1/2**, **2004 Standard Highway
Signs**, and the **2012 SHS Supplement**. FHWA states that the latter two
documents are the companion design book for the 2009 manual. Primary source
URLs and cached PDF names are in [refs/SOURCES.md](refs/SOURCES.md).

| Code / legend | Nominal inches W × H | Border / corner, inches | SHS anchor |
| --- | --- | --- | --- |
| R2-1 SPEED LIMIT 20 / 25 / 30 / 35 / 45 | 24 × 30 | .375 border, .375 edge, 1.5 radius | 2012 revised R2-1, 4E caps / 10E digits; SPEED 18.806 in and LIMIT 14.642 in line widths |
| R2-1 SPEED LIMIT 30 / 45, larger | 30 × 36 | .5 border, .5 edge, 1.875 radius | Same revised sheet: 5E caps / 12E digits; SPEED 23.508 in, LIMIT 18.302 in |
| R1-2 YIELD | 36 nominal equilateral side, 31.177 height | .75 white margin; red band to 5 in inner edge; 2 radius | 1-2: 3C caps, 9.063 in fitted line width; rounded physical corners lie inside the virtual triangle |
| R6-1 ONE WAY, left / right | 36 × 12 | Black field / white arrow, 2 radius | 1-86: 4D letters, black legend within white arrow |
| R6-2 ONE WAY, right | 24 × 30 | .625 border, .375 edge, 1.5 radius | 1-87: 6D caps and separate black arrow |
| R5-1 DO NOT ENTER | 30 × 30 | No black border, 1.5 blank radius | 1-73: red disc, white bar/background/4D legend |
| R7-1 NO PARKING ANY TIME, left / right / both | 12 × 18 | .375 border / edge, 1.5 radius | 1-90: red 3C/3B and 2C legend, .75 arrow shaft; three independent directional variants |
| R7-2 NO PARKING, 8:30 AM TO 5:30 PM | 12 × 18 | .375 border / edge, 1.5 radius | 1-90: period-standard integral time panel; not a separate invented federal plaque code |
| Local R7 two-blank timed assembly | 12 × 12 NO PARKING / 12 × 6 time/day plaque | .375 border / edge, 1.5 radius | Agency adaptation of the R7 layout system: red legend, right arrow, 8 AM TO 6 PM / MON–FRI. Authored split across two blanks; not a standardized federal plaque designation. |
| R10-11 NO / TURN / ON RED, red disc | 24 × 30 | .625 border, .375 edge, 1.5 radius | 1-139: 5E NO, 4D TURN/ON RED, 6 in signal disc |
| S4-3 SCHOOL over R2-1 20, with S4-1 time | 24 × 8 / 24 × 30 / 24 × 10 | .625 border, 1.5 radius | 5-5 / revised R2-1 / 5-3. SCHOOL is FYG; speed/time panels white; local school-day times authored. |
| W1-2 right curve | 30 × 30 side; 42.426 diagonal envelope | .5 border / edge, 1.875 radius | 2-3/4; black curved arrow, yellow field |
| W3-1 stop ahead | Same 30 in diamond | Same | 2-20; black straight arrow, red/white octagon, yellow field |
| W11-2 pedestrian | Same 30 in diamond | Same | 2-92 and symbol 6-10; FYG option plus older yellow alternative |
| S1-1 school crossing | 36 × 36 pentagon | .625 border / edge, 2.25 radius | 5-1 / symbol 6-58; roof sides 45°, FYG required by 2009 §7B.07 |
| W16-7P left diagonal arrow | 24 × 12 | .625 border, .375 edge, 1.5 radius | 2-126; 30° arrow, matched FYG or yellow field |

The alphabet is **installed open DejaVu Sans Condensed / Book**. The scripts
fit the published cap heights and principal line widths to approximate Series
C/D/E proportions. It is not the exact federal alphabet, a downloaded highway
font or a traced drawing. Pictograms are independently authored grid-measured primitives and cubic
curves checked against Appendix 6-10 and 6-58; the school child is on the left
and adult on the right. No PDF vector or raster is used as artwork input.
White, black, red, yellow and FYG are explicit original sRGB palette values;
the final stock-PBR material differentiates satin engineering-grade and
smoother prismatic daylight sheen, without claiming headlight retroreflection.

Blanks are **.080 in / 2.032 mm**, a normal supplier procurement choice;
MUTCD does not mandate that gauge. Rounded corners, 3/8 in punches and 1/4 in
fasteners are geometry. Each punch is independently measured on the generated
sheet vertices, rather than reporting its requested radius as a measurement.
The back is plain gray aluminum with an ALDERVALE inspection/date label.

Supports: **60.32 mm round hollow pipe**, **50.8 mm square × 2 mm wall with
57.15 mm anchor sleeve**, and rolled **2 / 3 lb-ft U-channel**, 79.375 mm
overall width. The channel wall outline is authored; its measured polygon
area is sized for the weight class using 7850 kg/m³ steel, not presented as
a certified structural section. Indicated post holes are 9.525 mm at 25.4 mm
pitch; normal/color detail is planned at delivery. The 25 mph U-post has an
authored 3° impact bend at .350 m. The fresh import measures 2.9996° by a fit to the exposed post perforations; its damaged lower sheet edge consequently dips below nominal. A separate pair of 19 mm steel bands grips
a nominal .320 m host pole; the host pole is not included.

2009 §2A.18 requires 7 ft in these pedestrian/commercial locations, measured
from curb/sidewalk grade. Every straight assembly's lowest plate starts at **2.1336 m**;
the related lower plaque is not lowered into a pedestrian path. §2A.19 allows
reduced urban offsets, including 1 ft where width is limited. The example
uses a .650 m post-center curb offset (not a universal minimum), leaving
more than .3048 m to the actual support. §2A.20 controls facing the approaching
lane; the hero demonstrates one sign turned 8°. Only related school-speed
and crossing-arrow panels share a post. No legal placement certification is
claimed for the illustrative street.

One **2048² face sheet** carries all added legends, backs and hardware, with
guarded cells. At 1920 horizontal pixels and a 40 mm / 36 mm-sensor camera,
the conventional R2-1's 4 in caps project to **21.7 px at 10 m / 7.2 px at
30 m**, and its 10 in numerals to **54.2 / 18.1 px**, front-on. Its atlas
cell supplies about 42 cap pixels / 106 numeral pixels before mipmapping.
The number should read at both distances; the small words become marginal
at 30 m, particularly oblique. These are projection estimates, not a game
camera/antialiasing guarantee. A full mip chain at 8-bpp compression costs
**5⅓ MiB**, shared once for the entire addition; the old 4 MiB atlas remains
its own unchanged allocation.


## Checkpoint export budgets

All counts below include the support, blank(s) and mounting fasteners. One
quick shared material and one external 2048² image per module. The bracket
is the reusable band fitting alone. Counts are measured on fresh imports.

| Module | Triangles | Materials |
| --- | ---: | ---: |
| speed20 | 446 | 1 |
| speed25 | 628 | 1 |
| speed30 | 648 | 1 |
| speed35 | 446 | 1 |
| speed45 | 604 | 1 |
| speed30large | 658 | 1 |
| speed45large | 446 | 1 |
| yield | 614 | 1 |
| onewayR | 618 | 1 |
| onewayL | 446 | 1 |
| onewayVertical | 604 | 1 |
| doNotEnter | 648 | 1 |
| noParkingL | 446 | 1 |
| noParkingR | 584 | 1 |
| noParkingBoth | 628 | 1 |
| parkingTime | 446 | 1 |
| noTurnRed | 446 | 1 |
| curve | 446 | 1 |
| stopAhead | 616 | 1 |
| schoolSpeed | 1,400 | 1 |
| parkingWithTimePlate | 796 | 1 |
| pedestrian | 994 | 1 |
| pedestrianYellow | 796 | 1 |
| schoolCrossing | 1,000 | 1 |
| PoleBandBracket | 712 | 1 |

The inspection library contains 16,116 triangles. Individual modules range
from 446 to 1,400, within the 1,500 ceiling. Its library glTF/BIN are
52,746 / 1,210,272 bytes and its shared PNG is 506,267 bytes at this checkpoint.
Individual glTFs sit beside `RoadSigns.gltf`, reuse its external image URI,
and have their support-foot origin at zero. Disk bytes are not GPU memory.
