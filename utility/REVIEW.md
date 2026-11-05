# Utility construction review

This is a form checkpoint, not a final look-development sign-off. The user
asked for at least two form passes and then a stop. Photos are local inspection
only. The final reconstruction renders the exported quick-material GLBs.

## Pass 1 — first Cycles hero, transformer and house service

Color/value first: the provisional pole is too smooth and dark to reproduce
silvered treated timber in the residential photographs. Steel/can paint is
uniform and cold; the tree source and quick context are also darker than the
photographs. No wood/rust/chalk look-dev is claimed. The photographs' sidewalk
cement is the assumed neutral for the later balance measurement; no gray card
or inverse albedo claim is available.

The 40-ft pole height against one/two-story houses reads correctly, and the
native six-foot planting allowance gives sensible curb/walk placement. The
first hero clipped the top and made the line hierarchy harder to read.
The first transformer frame exposed an arrester consisting of floating sheds,
deadend eyes floating at tangent-pin height, a wrong-direction light bracket,
and insufficient support above the low house eave. Those are construction
errors, not material problems.

Fixed: add the arrester core and supported mounting bars; put deadend eyes on
the arm/pole bearing datum; face the bracket into the road and mount the
library head; roof-guy the mast at actual roof hits. Pull back to a 35 mm,
sidewalk-height hero. The three-can rack initially exceeded 11k triangles;
lower radial/cable resolution on that rare bank recovered its budget while
retaining the same can/fixture construction. Keep fixed parts consolidated.

## Pass 2 — all four streets, hardware, base and distance

Color/value first: cavity and under-hardware shadow are deep and legible.
There is no pale white clipping problem. The pole still lacks the photograph's
gray/brown fiber variation; the yellow guard is too uniformly manufactured.
These are documented next-stage surfaces. The quick label planes are useful
construction tags, not final burned/embossed graphics.

The full set exposed important errors that the hero alone concealed. The
house yaw convention faced the rows away from the street. Roof-ray checks
caught drops crossing those roofs, prompting the yaw correction rather than
relaxing the geometry test. A front-wall mast outside the overhang replaces
the first side-eave guess. Its lower elbow enters the wall; a second meter is
removed. A roof-guy query measures source roof triangles for every attachment.

Other rejected details: the anchor frame cropped away the actual ground eye;
the base frame did not show the base; a distance frame exposed the presentation
road's artificial end. Reframe the first two and extend the native roadway
well behind the viewing positions. Secondary spools originally had their axes
along the wire and the socket inside the porcelain. Reorient the spools,
give them a real vertical rack and put the neutral on its outer bearing line.
The ground-wire molding now follows the measured taper.

The three-can assembly now has separate primary phases, a supported steel rack
and three **independent** secondary circuits. Its outer hots must not terminate
on the central circuit. Three-phase risers now carry three sealed terminations
and tails rather than a single phase's cable. These were construction fixes.

The distant exported four-sided tubes show intermittent breakup, especially
against bright sky. A camera-facing .85-pixel ribbon with compensated coverage
preserves their integrated darkness better. Use that as the runtime direction,
retain true tubes near the player, and keep the comparison explicitly labeled.
An opaque width floor would make the remote wires visibly too heavy.

## Pass 3 — physical gates and final checkpoint replay

Color/value first: neutral balance is based on a bare sidewalk ROI in the NC
photo and concrete driveway/sidewalk in the MD photo. `build/reference-balance.json`
records native rectangles, linear medians and gains; balanced inspection copies
stay in build/. Photo pairs retain original colors, not baked replacement pixels.
The source wood is still deliberately flat. The exported hero's lower-image
Y′ percentiles and clipping fraction are recorded in `build/hero-tones.json`;
that region includes context and is not a utility-only albedo mask.

The mathematical tests verify unequal endpoint heights, sag definition,
catenary differential identity, tension conversion, polyline error and
coverage compensation; invalid inputs are rejected. The independent raw GLB
gate caught degenerate check-tip faces; those tips are now actual triangles
with single end vertices. Every final raw mesh has zero degenerate triangles
and unit normals. Fresh import verifies the real socket transforms and counts.

The earlier uniform-height version passed the 20/18/15½-ft geometric screens. Minimum sampled
neutral/comm surface gap is 1.205 m, above 1.016 m; the nominal 1.32 m pole gap
alone was not used as proof. Ground clearances are measured on imported wire
vertices. Roof rays sample the actual placed house roof surfaces under the
service curves. A 100 mm mast increase recovers the conservative eight-foot
roof screen for the low communication drop near a porch. Minimum sampled
roof clearance is 2.493 m; higher masts remain supported by roof guys.

The photo fits keep their errors visible. NC uses several pole heights and
run positions; MD is a weaker type comparison, with the two space landmarks
held out because they differ from our selected utility layout. Lens estimates
are not EXIF. The MD image was made in 2015, after the modeled equipment period.
Both comparisons judge existing residential infrastructure, not an attempt to
copy a real neighborhood. Full residuals live beside the paired images.

No final look-dev, atlas, UV, bake, engine shader compilation or game
performance result is implied by these form checks.

## Pass 4 — reject repetitive antenna-like service masts

Color/value first: the replay's lower-image Y′ range has deep cavity/context
shadow and rolled highlights without clipped white. Its flat wood and guard
still cannot reproduce the aged-photo surfaces; this remains an explicit
look-dev stop, not a material approval.

The replay made the uniform 6.6 m masts conspicuous over the one-story roofs.
Applying a road-height criterion to the entire yard was visually and
constructionally unhelpful. Review WPS Section 7's actual distinctions:
the general Type-A service criterion is 16 ft, with a conditional lower
residential-driveway exception that this family does not use.

Move supports to solid corner jambs outside porch roofs. Measure roof anchors
again and size the mast to those anchors and its own service/communication
crossing. The current 5.2–7.435 m attachments follow one/two-story roof heights.
The 5.2 m ranch masts replace the old 6.6 m version. Keep a conservative 18-ft
service screen over the road and 16 ft over all private land; comm drops use
15½ ft over the road and an authored 12-ft private-yard screen.

The independent audit clips imported triangles at the curb-back planes, so
a crossing minimum between centerline stations cannot escape the test.
Current measured minima: service private 5.193 m / road 5.975 m; comm private
4.397 m / road 4.866 m. Sampled roof rays now find no overflights. The previous
2.493 m porch separation is a superseded layout measurement, not a current claim.
The guy guard is also a real hollow 2.5 mm wall with open end rings, exposing
the wire/anchor rather than passing it through a solid yellow cap.

## Pass 5 — reject the misleading imported context pose

Color/value first: the quick-material limitation remains unchanged. This
pass addresses a construction presentation error that the source-space roof
checks could not establish.

Imported house roots use quaternion rotation. Writing their Euler yaw left
the visible houses unrotated, even though the layout, source roof queries
and service mast transforms faced the street. The resulting pictures showed
apparently floating masts. This was a renderer bug and invalidated those
pictures as evidence of a working assembly.

Compose the instance's world matrix explicitly, preserving the imported glTF
axis conversion. Add a second check against the actual posed visible GLB
house triangles: every roof-guy endpoint must meet that house within 0.2 mm.
Run it for all 48 house instances, and include its measured errors in each
render receipt. All 96 anchors pass; the maximum measured surface miss is
0.00811 mm. The service camera now follows the house's front frame.
Regenerate every street, detail, distance frame and photographic pair from
the corrected presentation. Current-source recipe hashes reject stale images.

## Remaining work, deliberately outside this checkpoint

- Prove real aged wood, silvering/check depth, wet ground-line absorption,
  bolt rust/runoff, transformer chalking, hand contact and faded guards against
  used photographs, first in source and then on the baked export.
- Put fine triplex strand lay, long-span fiber lashing, conductor strands,
  threads, manufacturing texture and scars into the shared normal/color maps.
  Current service constituent tubes are smooth, not a geometric helix.
- Complete the shared 2048 atlas and at-most-three-material delivery; current
  diagnostic material/label counts are temporary. Run final UV/density/bake gates.
- Validate the supplied original ribbon shader in a real engine, moving the
  camera under its AA modes and testing transitions, culling and performance.
- Town staging is intentionally sparse and repeats one source seed per house
  type, with quick ground/pickup materials. It demonstrates utility scale and
  connections rather than a finished town environment. House internal meter
  routing and a three-phase secondary bank connection are not modeled.

No shared kit file or neighboring asset source is modified. Existing generated
deliveries were absent from this worktree; context generation writes only
utility/build. Their absence is stated rather than claimed as a comparison of
hundreds of delivered files that were not present.
