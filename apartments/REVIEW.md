# Form and look review

The form-only record below is retained from the accepted checkpoint at
`46c0207`. The current material and presentation review starts at **Look gate,
pass 1**; later observations supersede these historical limits.

That original gate stopped before look-dev. The assets are original type studies; photo
fits compare construction and rhythm, rather than claim a replica or a survey.
No reference pixels enter the meshes, colors, diagnostic image or future maps.

## Photographs, cameras and value controls

The three fitted views use the 2004 used garden-apartment photograph, a c.1978
DAHP mansard/gallery photograph, and a 2006 garage-row photograph. Crops,
authors and rights are in `refs/SOURCES.md`; DAHP's original page/crop register
is generated locally. Source and exported pairs are separate outputs.

Color review starts with assumed-neutral balancing, preserving average linear
exposure. `build/neutral-reference.json` records the exact ROIs and RGB gains:
white replacement sash (.884, 1.134, 1.013), light painted roof edge
(.910, .982, 1.133), and white garage panel (1.047, .968, .989). These are
assumptions about paint, not gray-card measurements. The photos have different
light and white balance; their JPEG values are not recovered albedos. The
shared procedural daylight stage uses AgX Medium High Contrast at −.45 EV.
The camera solver’s generic light/exposure defaults are retained in its data
but are not lighting recovery or applied stage settings.

The original form-only measured-landmark fits gave 9.59 / 9.91 / 11.95 px RMS at
25.00 / 44.78 / 54.73 mm, respectively (`build/matched-cameras.json`).
The used-garden fit reaches its lower lens bound; these corner fits do not
establish equivalent plans, fenestration or a recovered photographic camera.
The garage photo has 38 mm-equivalent EXIF; its longer fitted lens is a
consequence of comparing an original plan. Independent Blender projection
checks disagree by at most .00085 px, below the kit's .05 pixel limit.
Residual overlays remain available beside each pair.

## Pass 1 — room modules, scale and blocked openings

Witnesses: `renders/pass1/Building-301/`, `renders/pass1/Building-304/`,
`renders/pass1/Complex-301/` and `renders/pass1/matches/`. Historical pairs were
rendered retrospectively from retained procedural checkpoint scenes; they are
not substituted for current exported evidence.

**Value first:** the first exported brick building was white, despite colored
source vertices. The exporter did not recognize the first color multiply
node. Replaced it with the same supported stock texture/vertex-color node
arrangement used by the houses. White walls/rails from that rejected export
are not a color target. The two-story pair was too cold and its continuous
dark apron obscured upper gallery entrances; do not try to cure this by
brightening the light.

**Form critique:** the central-core mass and nine-foot floor rhythm read as a
small walk-up. Its broad gable is plausible for the deep double-loaded plan,
but every floor looked too diagrammatic. The gallery needed a continuous
protected route, separated end stairs and usable landing openings. Rails
initially continued across those openings. Mansard openings were cut for
windows while some doors remained behind the apron. Those are construction
failures, not material deficiencies.

**Changes:** cut real wall/roof openings, clear gallery guards at stair entries,
provide closed-riser pans/stringers/landings, reserve a side bypass in the
central hall and connect both front/rear unit pairs to it. Use front living
sliders, smaller bedroom/kitchen openings, end windows and shallow tenant
backings. Schematic unit rooms now reserve circulation and wet cores rather
than calling four exterior bays a finished interior plan.

## Pass 2 — roof intersections, approaches and site assembly

Witnesses: `renders/pass2/Complex-301/`, `renders/pass2/Row-403/`,
`renders/pass2/matches/` and `renders/pass3/Row-403/`. The second archival
source comparison was repeated after repairing its relocated relative image
paths; the magenta missing-image output was rejected.

**Value first:** dark steel and roof values now retain cavity shadow; green
foliage initially became a black silhouette because its active chart selected
an empty bark UV layer. Normalize botanical charts before joining, preserve
the original leaf mask, and strip unused wind color from this static context.
Do not raise foliage albedo to disguise an invalid chart. The blue-gray
apartment quick palette also did not support the 1970s gallery reference;
use a restrained landlord green for that profile.

**Form critique:** intersecting front-gable solids left abrupt roof ends. The
row's raised floors lacked foundation fill and its flat drives missed garage
thresholds. An entry camera looked at a truck instead of the door. Rear slabs,
carts and stoops needed ground-level placement despite stepped unit floors.
The reference's mansard end fins flank an open gallery: a continuous low strip
across the door faces is the wrong construction. The courtyard was too much
unbroken grass and wide unaccounted parking depth.

**Changes:** use the houses' analytic roof-plane clipping for the cross gables;
fill exposed foundations; vary stoop riser count with actual floor elevation;
slope garage drives and parked vehicles together; correct entry framing.
Open the gallery canopy between mansard fins. Split shared balcony posts at
each slab, give chairs four feet, and fit the bicycle/grill to their patio
surfaces. Add actual AC sleeves and one pad per split-system unit, with meter
count independent from HVAC type. Condensers sit along end-wall service runs,
outside occupied patios. Pool coping is an open ring, with an actual water
opening. Clip native turf around slabs/walks and add curbed islands and a drive.

**Assembly/optimization critique:** joining independently placed copies that
shared mutable mesh data multiplied context geometry. Consolidate each native
module once before instancing; independently count every raw glTF node's
triangles. Preserve separate moving architectural parts. Apply scaled terrain
placements into copied mesh data and leave exported frames at unit scale.

## Pass 3 — physical checks and current exported judgment

Current witnesses: all 52 images in `renders/checkpoint/`, three pairs in
`renders/matches/`, and three independent source pairs in
`renders/source-matches/`. `renders/review/` gathers the full set, plans and
heroes. Historical source images above do not certify the current export.

**Checks that changed the model:** sampled door surfaces caught threshold
penetration at rest and hinge binding at 100°. Raise the leaf bottom clear of
the threshold and put the offset hinge behind the casing return. Curved-guide
checks caught adjacent rectangular garage sections binding; tapered end noses
now clear while rigid section chords retain their length. The measured minimum
garage ceiling gap is 140.20 mm. Poses are sampled, not a continuous collision
proof. These checks cover leaves/casings and garage sections/guides/ceiling;
they are not a whole-site collision or egress certificate.

Wall-grid coordinates that differed only by floating arithmetic generated
zero-area slivers. Merge grid lines at a micrometer and reject zero spans.
Temporary text and constant-color source context also carried empty charts;
replace those with finite metric charts while retaining actual leaf-mask UVs.
The gate rejects zero-area geometry and UVs. This cleanup does not masquerade
as final atlas packing, density calibration or baked normal detail.

Building roots are centered on their actual wall-footprint bounds. Their
footprint polygons/corners, module walk sockets and townhouse party-wall
centers/endpoints remain explicit. Recentered site placement preserves the
designed world layout. Color and numbering vary by unit while belonging to
the same architectural module on both faces.

The additional passage/site pass below follows the close-up inspection.

## Pass 4 — service access, amenity routes and final frame review

**Value first:** flat quick colors remain visibly synthetic against the balanced
photographs. The green gallery profile now belongs to the period; it still
needs the reference’s material breakup and worn lower concrete at look-dev.
Shadowed rear patios and the core retain dark recesses. The first dark meter
views concealed the construction, so service/core inspection frames now use a
120 W temporary area fill, disclosed in camera provenance. That fill is absent
from the heroes and photo comparisons.

**Construction critique and corrections:** the linked wings’ original five-foot
wall gap was not five feet of working space. A neighboring balcony or condenser
consumed it, and canopy posts crowded the meters. Widen the walls to ten feet
and bear the low canopy on wall ledgers/cross beams. Actual opposing mesh bounds
now leave at least 1.295 m in the L and 1.564 m in the offset building through
2.1 m height, exceeding the authored 1.2192 m reservation. This does not certify
an electrical installation. Broad site views also cropped the amenity corner;
pull back those cameras. Connect pool/playground walks to the main path and
open the pool’s north fence with a separately hinged, outward-opening gate.

**Slider correction:** the first nine-position sash sweep failed at rest: the
outer moving extrusion intersected the fixed center stile, and the handle
belonged to the fixed window. Move the moving track 35 mm farther outward
and put the handle on that sash. The revised sweep tests actual fixed/moving
surfaces, separate from pivot serialization and the door-leaf tests. No
triangles were added by transferring that handle.

**Architectural judgment:** the central-core block has a legible nine-foot
floor rhythm, deep roof and paired unit/balcony bays. The open-core offset
version belongs to a later landlord-built phase. The two gallery variants
read as economy walk-ups with separated end flights and usable upper access;
they should not acquire a continuous mansard apron across their doors. The
six-unit mansard and brick/gable rows differ convincingly in period; the
four-unit green row is a smaller related place. The garage row’s clipped
cross-gables, filled raised foundations and sloped approaches resolve its
previous construction failures. Rear patios remain too repetitive and bare,
and the site’s sparse trees and identical pickups expose the staging. Those
are explicit next-gate weaknesses, not evidence of photographic realism.

The two final heroes’ encoded display-luma percentiles (whole frame, including
sky/ground) are .002805 / .310426 / .842056 and .069755 / .558953 / .845144
for p1 / median / p99, respectively. Neither has any channel above .99.
These are exposure/clipping checks, not linear photometry, surface albedos or
a substitute for matching materials to photographs. `tonal-range.json` records
the complete figures. The current physical gate passes 2,530 hinged leaf
poses, 1,998 sliding-sash poses and 504 garage-section poses. Complex point
correspondence is explicitly unmeasured; its counts and pivot/socket frames
are checked, while the building forms are compared as standalone exports.

**Final pair judgment and gate evidence:** opened all 52 current exported
views, all three exported photo pairs and all three independent source pairs.
The green economy gallery differs substantially from the used 2004 building’s
brick skin, recessed private balconies and continuous mansard. It is a
comparison of related period types, not a replica. Against 1978, the open
access rhythm and fin profile read correctly, while this authored version’s
stair flights project farther forward and its kitchen windows are taller.
The garage row has the period’s repeated private entries and front gables,
but fewer facade projections and no arched stair windows. Those choices and
the explicitly simple room backings limit the comparisons; low corner-fit
residuals do not erase them. Source/export pairs show the same form and quick
material response. No bake-loss conclusion is possible before look-dev.

`make WIDTH=1200 SAMPLES=32` completed with exit 0 after the staged rebuild;
`make check` also passed. The final repository check has 1,672 tracked/staged
source files and zero errors. `renders/review/evidence-audit.json` verifies
all 58 current frame hashes, Cycles provenance and the hero/ground eye/lens
settings. All twelve exports pass, with zero degenerate geometry or metric
UV triangles, and 197 pre-existing delivery/docs hashes unchanged. Images
remain local rebuildable evidence; no checkpoint JPEG is committed as final
documentation. The work stops at this gate, before look-dev.
The staging lawn also exposes native patch boundaries under raking light;
continuous ground treatment belongs with the site material pass.

## Limits deliberately retained for the look-dev gate

- Brick, wood, shingles, stone and steel are flat quick-color reservations.
  Surface manufacture, meaningful shared trim mapping, causal fading/rust/dirt,
  roughness variation and final maps are absent. These are not product photos.
- Repeated window backings remain simple; unit room reservations are schematic.
  Full interiors, fire-resistance assemblies and local accessibility/egress
  certification are not delivered.
- The original plan differs from each photograph. In particular the economy
  gallery has a continuous access route rather than the 2004 photograph's
  recessed private balcony rhythm; the garage row lacks its arched stair bays.
  The comparison exposes those differences instead of treating a low fit error
  as proof of architectural equivalence.
- Context uses original library source geometry and simplified materials. Parked
  pickups repeat; a final complex should use several accepted car types and the
  canonical landscape/ground maps. Landscape density and tenant dressing are
  still sparse. No claim of a finished photorealistic site is made.
- Linked wings provide L/offset assemblies. Arbitrary continuous L-roof plans,
  sunken-floor circulation, final collision/navigation, LODs and dusk window
  emission remain future work.

No kit or accepted family delivery was changed. This checkpoint's extra rigor
went into openings, construction, circulation, mechanics and independent
serialization checks; it did not add a new material atlas.

## Look gate, pass 1 — exported brick and the exposed construction edges

**Color and value first.** Opened `renders/look-pass1/Building-301/hero.png`
at native 1200 px, alongside the three neutral-balanced reference photographs.
Running bond and pale mortar now read at this distance; the roof and steel
retain dark values. White room backings were too bright in daylight. Reduced
the shared emission circuit and reserved its stronger setting for dusk.
The source white-balance assumptions remain the replacement sash, painted
roof edge and garage panel documented above; these are display comparisons,
not recovered reflectance measurements.

The formerly unexplained pale bands are **interior floor edges and wall ends
coplanar with the exterior veneer**, not veneer control joints or a belt
course. Texturing exposed them more clearly. Retracted floor plates and the
ends of core fire separations behind the exterior shell. Added the real
foundation outline under the stepped facades. The new stair-bay roof break
also exposed an open gable end; closed that end with its framed gable wall.
Both corrections require the next export/render as their visual proof.

Shared cedar, rather than asphalt, is the material basis for the full-story
mansards. Their gallery fronts retain the inner walking strip under the
slope: the upper edge projects over that strip rather than pinching it down
at each shingled pier. The additional brick/mansard seed 305 has recessed
balcony wells and will replace the unrelated teal gallery in the 2004 pair.
No photographic pixels are texture inputs.

## Look gate, pass 2 — closure, six-role delivery, and remaining orderliness

**Color and value first.** Opened `renders/look-pass2/Building-301/hero.png`
at native 1200 px. Dark roofs and steel hold their values and the lit-room
backings no longer turn whole panes white. The brick still looks too uniformly
red/orange; use the houses' fired red/tan/buff ranch variants for the respective
period profiles. The same three balanced photographs were opened again at
native size, including the cedar fins and the garage row's projecting bays.
Their material response must be judged in the next fitted comparisons.

The wide pale floor/wall bands are gone in the actual export; the roof end is
closed. The independent raw/fresh-import check of this intermediate export
passes at 78,125 triangles, six materials, zero collapsed geometry/UV0
triangles, and measured area-weighted UV density p5/p50/p95 of
168/420/469 px/m. Those are this intermediate's counts, not the final family.

Remaining tells: the brick's short repeat, the excessively orderly window
backings, broad clean ground and the absence of the town in this isolated
construction view. Added mapped soldier/rowlock courses, refined real-width
blind blades, upper-balcony grills/bicycles and distinct painted replacement
parts. Ground wear is an absorbed vertex field under engine positions and
a narrow walking desire line; no glossy film or rectangular oil stickers.
The full scene and matched-light pairs remain the next visual witnesses.

## Look gate, pass 3 — fitted exported color pairs expose roof/body collisions

**Color and value first.** Opened all three native 1400 px renders and their
pairs in `renders/look-pass3/`. The old sky contribution makes concrete,
white paint and steel blue; it is not matched neutral overcast in the 1978
pair. The cedar reads as an extremely contrasting silver checker, and the
garage row is blue-gray against beige siding. These comparisons are rejected
as final color evidence. Reduced clear-sky fill, warmed the procedural sun,
and mixed a neutral procedural cloud field for the overcast photograph.
Changed the garage profile to faded beige. Existing reference neutral
balances remain unchanged and do not come from fitting a rendered color.

The accepted Cape cedar's exposed-wood color range does not serve these dark,
maintained mansards. `derive_surfaces.py` applies an authored semi-solid brown
stain to that family's **4K baked color**, then filters in linear light to
512 × 256. It preserves dark key gaps, and retains the exact canonical cedar
normal and roughness bytes. One new color image costs 1/6 MiB with assumed
8-bpp compression and full mips. No source photograph enters this operation.

**Construction failure visible only in the pairs:** the sloping mansard
entered the unreduced upper wall box, so siding obscured its upper third.
Recessed the upper body 450 mm behind the front/rear slope and 350 mm at the
ends; retained window/dormer and balcony locations with actual wells. The
mansard now needs to be judged around the whole upper story, rather than
accepting a lower apron with a siding band above. Garage roof steps also
exposed previously omitted interior gable closures; added plain framed
closures without unnecessary outer-end vents and rake ornament.

The new wall shell topology removed hidden grid faces. Thin folded curtains
replace solid curtain boxes; shutter louvers use the houses' existing normal
strip instead of hundreds of tiny boxes. These recover triangles for the
requested articulation. Extended gallery floors to recessed thresholds and
added actual downward surface probes at those entries. These changes await
the next complete rebuild/check and exported images; the earlier passing
serialization check did not prove these construction relationships.

## Look gate, pass 4 — full-size town heroes and night routing

**Color and value first.** Opened the three native 1400 px images in
`renders/look-pass4/` and the complex hero/dusk plus row hero in
`renders/look-town/`. The mansard is now a full brown story, without the
exposed upper siding band or silver checker. Beige siding and warmer daylight
better support the garage photograph. The gallery's neutral overcast is too
dark, so its sky illumination is raised while retaining neutral cloud light;
that correction must still be checked. Dark stained cedar is reduced slightly
in reflectance. These are material/light corrections, not a new photo balance.

The first town hero is rejected: a courtyard canopy and near pickup hide most
of the accepted building. Move the canopy to the flank and leave the camera's
nearest stalls vacant, retaining mixed occupied stalls beyond them. The row's
street still ends against empty green at the right of its frame; add adjacent
houses and trees along that visible frontage, with continuous PBR turf at grade.
Presentation continues to use the canonical car, house, shrub, tree, utility
and light exports, never altering their files.

The first dusk is also rejected. A broad color-range test accidentally routes
cream door casing through the lamp mask. Replace it with the exact authored
lens-color test, and give room backings a dimmer mask region than fixtures.
Use the street light's actual `LightEmitter` socket and local -Z spot axis;
the former fallback point was inside the shaft and could not illuminate the
lot correctly. Raise blue-hour sky fill, and keep light bases outside the
accepted walking routes. Night uses a documented emission multiplier, not a
changed delivered texture.

Mineral UVs on length-scaled native roads/curbs are rephased in metric world
coordinates; trim artwork retains its atlas cells. Native private-aisle
asphalt shares the apartment lot's dry response and value, and native curb
concrete uses the same small concrete set as the walks. This does not modify
Ground's canonical materials or images. The row's public street is now
presentation-only native Ground, with turf clipped out of its crowned road
instead of a flat private road plate overlapping it. The next focus batch
checks these corrections before the full cold delivery rebuild.


## Look gate, pass 5 — readable town, restrained dusk, physical reveal correction

**Color and value first.** Opened all six 1400 px focus frames, the three
composed pairs, and all three balanced source photographs at native resolution.
Brick holds a medium fired value, asphalt is dark, balcony cavities stay deep
and the garage siding is beige rather than slate blue. The used 2004 pair still
has direct-sun shadows and darker pavement than its softly lit photograph;
changed only that comparison's procedural illumination to a largely neutral
cloud sky with a weak broad sun. Corrected its left front ground/top landmark
identification; photo residuals remain original-type differences, not survey
accuracy. The 1978 gallery still has more regular fins/planting than its photo;
this remains a declared type comparison.

The complex now reads through the gap in mature trees, with factory-colored
hatchback/pickup, neighboring houses and grounded curbs. The row's far right is
filled by adjacent houses and mature canopies. The repeated low shrub forms,
shallow room backings and very tidy site remain CG tells. Dusk now has dim warm
rooms behind curtains, neutral door casings, and pools on actual pavement;
there is no clipped white casing sheet. Night interior depth is still limited.

The cold build exposed a real final-pose failure in the new deep mansard jamb:
a rectangular return intersects the accepted door leaf at 100 degrees. Splayed
the return and widened the concealed upper rough opening. The leaf, its hinge
and its authored range stay unchanged. This correction is subject to the same
sampled surface test, rather than a visual claim of clearance.

Pre-clean iteration frames and logs for passes 1–5 are retained outside the
family's clean outputs at `build/apartments-preclean/`; paths in those earlier
passes are relative to its archived `renders/`. Current evidence will be in
`apartments/renders/`. No image from these passes is committed to `docs/`.


The family render exposed two additional checks in pass 5: the camera's
first downward hit was a mature canopy, so the eye-height ray now continues
through overhead geometry to the first upward walking surface below 0.5 m.
This still measures the actual surface rather than substituting nominal grade.
The overview of seed 305 showed a legacy grill beyond the newly recessed slab;
the grill and rear bicycle placements now follow their actual respective
patio centers in core/gallery and recessed/hung variants. Their geometry is
unchanged. A second `make clean` removed all four generated apartment output
folders before the corrected cold build; read-only references/library caches
and original handoff witnesses were retained.


## Look gate, pass 6 — complete family review and rejected inspection views

**Color and value first.** Opened the complete 59-view family set at native
1400 px, all three exported native comparisons and their composed pairs.
The softened used-building comparison now has neutral gray paving and buff
masonry rather than the earlier blue/dark direct-sun stage. Beige siding,
brown mansards and black steel retain their hues. Still, the flat roof tops
reflect a broad pale sheen in rear views, and rear patios are too dark/blue
to inspect. The flat membrane now uses the existing rough trim region and
a darker vertex value, with no new image or material. Rear/patio inspection
frames get the raking sun from their own side, recorded in provenance; hero
and matched-light stages are unchanged. Stair-hall inspection fill is raised
locally, without raising the hero's shadow exposure.

The main heroes, articulated fronts, continuous mansards and garage bays read
clearly. The rear complex cameras are rejected: mature canopies fill their
foreground. Move those stations inside the perimeter; omit only presentation
trees within ten meters of each inspection camera and list their objects in
that image's provenance. Add the own-house library beyond side lawns so the
remaining sideways horizon is occupied as well as the opposite frontage.
Native roads/curbs/slabs now repeat at their original lengths: the former
stretched expansion joints are gone. Scene dressing stays outside delivery.

The garage-row fanlight is modeled but partly hidden by the eave. Lower its
unchanged 1.22 × 1.32 m stair sash and the curved fanlight 270 mm, moving its
rough opening with it. This preserves the accepted sash form while giving
the half-round head physical space below the eave. New raw checks pass at
63,012 triangles for that row (55,634 architecture), within its allowance.

The independent source-pair import failed on a Blender 5.2 settings interface:
the source tiling's minimal `glTF Material Output` AO group shadows the
importer's full group, which expects iridescence inputs. Applied the same
source-group rename already used by the houses' renderers, only in the
in-memory presentation importer. Source materials, files and deliveries are
unchanged. Rejected native frames/pairs are retained under
`build/apartments-pass6-rejected/`; the next complete batch supersedes them.

Remaining visual weaknesses are repetitive shrub and tenant-prop shapes,
very tidy lots, simple meter faces, shallow window rooms and non-identical
photo fenestration/proportions. Low numerical camera residuals do not remove
those differences and are not used as proof of photographic equivalence.


The allocation audit also rejects the unnecessary 2048² colonial roof maps
on the garden gables. The existing 1024² `RanchRoof` set supplies the correct
asphalt-shingle manufacture over the same 4.8768 m coverage, reducing each
gable building's compressed cold load by 12 MiB, with no new images. Its
210 px/m density exceeds the principal hero's sampling rate. The complete
export/render/check cycle is repeated with that actual shipped selection;
the material reduction is not a paper-only estimate.


## Look gate, pass 7 — final shipped maps, native inspection and repeat

**Color and value first.** Opened all 66 final native 1400 px frames: 59
exported family views, three exported comparisons, three independent source
comparisons, and the Eevee hero. Also opened all five 1200-pixel-per-side
before/after plates and the contact sheet. The 1024² ranch shingles hold a
credible gray granular response; brick stays fired red/tan/buff, cedar stays
brown, and the steel stays dark. The rough flat tops no longer turn into
bright sheets. The rear/patio inspection sun now reveals the actual siding,
concrete, curtains and fences without lifting the principal heroes.

The two principal Cycles heroes' encoded display-luma p10 / median / p99 are
.062 / .227 / .704 (complex) and .105 / .357 / .742 (garage row).
Only two / three pixels exceed .99 in every display channel. These are
whole-frame display statistics, including sky and paving, not recovered
albedo measurements or a silhouette mask. Cavity shadows remain deep and
highlights roll off; the scenes do not read pale overall.

The three photo neutrals remain the white replacement sash, painted flat-roof
edge and white garage panel documented above. Current camera RMS residuals
are 18.57 / 11.19 / 11.79 px, with lenses 25.00 / 24.00 / 38.36 mm. The first
two reach their lower lens bounds. Those are original-type fits; the exact
end projection, window rhythm and roof proportions differ from the photos.
The new used-building comparison is brick/mansard with recessed balconies,
rather than the unrelated gallery type. Procedural illumination is soft and
largely neutral for the first two photographs, direct for the garage row.
Mean absolute source/export display RGB differences are .000745 / .000248 /
.001561; that is evidence of retained render response after export, not proof
of a correct photographic match.

Eevee initially rendered white panes without refracted rooms. It now uses the
houses' existing ray-tracing/refraction integration pattern, with a 12 mm
slab gauge matching these modeled panes, instead of estimating thickness from
the whole joined building. Opened the corrected Eevee image: white panes are
gone and the window backings transmit, though its glass and bounce response
still differs from Cycles. This is an in-memory renderer setting, not a
modified canonical house material or a new shipped map.

**Rebuild evidence.** `make clean` removed this family's build, export,
textures and renders; the original handoff and 197-file preservation witness
were restored as comparison inputs. `make WIDTH=1400 SAMPLES=32` regenerated
all thirteen packages, checks and the full Cycles/exported-comparison set.
That invocation was interrupted during a subsequent GPU-lock wait. Resumed
with `make -o src/render.py WIDTH=1400 SAMPLES=32` to finish the independent
source pairs, Eevee and review, without rerendering unaffected Cycles frames
after the Eevee-only integration edit. It passed. Plain `make check repeat
check-repo` then passed. `make repeat` independently regenerated geometry and
compared all **61** glTF/BIN/referenced-image files: zero changed bytes. It
retains the independent sources and restores reviewed witnesses/timestamps,
so provenance remains valid. Accepted shared bakes are cached repeat inputs.
Logs are in the repository's ignored `build/apartments-verified-clean-build.log`
and `build/apartments-finish-{0,1}.log`.

Raw checks report zero collapsed triangles/metric UV0 triangles in all 13
assets, at most six building materials, measured density p5–p95 spanning
86.6–671.9 px/m across the family, maximum bidirectional source/import point
error 3.932 micrometers, and maximum normal-length error 1.19e-7. Physical
stairs, 0–100° sampled leaf/casing sweeps, sliders, garage guide/section poses,
gallery entry surfaces and meter passages pass separately. Existing 197
delivery/docs hashes and 110 dependency export/map hashes remain unchanged.
`kit/repo_check.py` reports 1,679 source files and zero errors. No kit or
other family source changed, and no docs image is committed.

The final unique image inventory is 35 files, 63,166,694 encoded bytes and
91.6875 MiB at assumed 8-bpp compression/full mips. New apartment maps add
1.1875 MiB; painted steel reuses the house trim. Complete geometry plus shared
images is 312,133,336 bytes. Per-building, complex and row figures are in the
README and generated `build/check.json`/`build/delivery-summary.json`.
`build/native-inspection.json` records hashes/dimensions of the 66 opened
frames. All five form plates retain 1200 native pixels on each side.

**Remaining CG tells.** Plantings and tenant furnishings still repeat, the
lots and flat membrane tops are unusually tidy, meter faces are simplified,
and room backings have shallow, repetitive depth. Some shared siding/brick
repeats are visible in close-ups. The reference pairs establish the same
construction types and a disclosed color/light comparison; they do not make
these original buildings photographic replicas. No new tool or approval is
needed from the lead. A future general kit helper could centralize the AO
settings-group accommodation and thin-glass Eevee setup already used by both
this family and the houses; this round makes no kit change.

## Delivery pass 8 — first fix crops, rejected planting balance

**Color and value first.** Opened the inherited heroes, all three pairs, the
native recessed-type plate and dusk before changing anything, then all six
1400 px frames in `renders/delivery-pass1/`. The native afternoon lot foreground
rose from about .19 to .32 encoded display luma; it no longer reads as fresh
black sealcoat. The 2004 photograph's asphalt is .68–.80 in the tested patches,
with a very bright photographic exposure. Use the direct-sun 2006 townhouse
photograph as the primary weathered-lot value control: its assumed neutral is
the same white garage panel already recorded above. Three native pavement
patches measure .369 / .393 / .435. These are exposed display values, not
reflectance measurements, and the brighter 2004 comparison is retained.

The initial tint correction exceeded 1 in COLOR_0 on a few asphalt vertices.
Clamp the delivered factors to the ordinary glTF color range before final
judgment; do not count on engine-specific out-of-range color behavior. Existing
baked images, lighting and exposure remain the accepted inputs. Narrow dark
routed seals, discrete darker utility patches, oils beneath engine positions
and broken paint runs now differentiate a maintained old wearing course.

The rightmost upper sash now fills its actual roof opening; it formerly
followed the stepped wall behind an opaque cheek. Its deep return connects
back to that wall. The dusk shows broad warm pavement pools and the entry's
wall/walk pool, instead of only glowing lenses. Actual fixture sockets replace
name-derived door offsets; stair-hall bulkheads use the same existing circuit.
These changes still require geometric checks as well as visual judgment.

**Remaining CG tells and correction.** The first planting mix still presents
five small boxwoods together in the principal hero: the hydrangea drift fell
outside that short bed. Reject that distribution, force a short flowering
drift within each border, widen the size range and retain a few empty mulch
stations. The first row photo pair still used legacy shrub markers; route it
through the same new beds and restore its public-street foreground. The new
corner maple is plausible but hides part of a balcony, as real planting does.
Shallow rooms, repeated props and very regular brick manufacture remain
visible. No docs are created at this pass.

## Delivery pass 9 — all four fixes visible at native size

**Color and value first.** Opened all six second-pass frames and the four
native before/after plates in `renders/delivery-fixes/`, plus both outlined
value-control images. The first proposed .369 photo patch included a mulch
edge and flowers; reject it after looking at the marked photograph. Move
that patch entirely onto the wearing course. The final three native sunlit
photo-patch medians are **.385 / .393 / .435**. The unchanged-camera exported
hero's two pavement rectangles are **.186 → .318** (private aisle) and
**.198 → .330** (stall apron). The result is deliberately on the darker side,
.055–.067 below the darkest reference patch, without raising the accepted
building exposure or editing a canonical Ground image. Five actual surface
rays hit asphalt and five sunward rays are unblocked. Different photographic
exposure and sealcoat histories still limit exact value equality. The 2004
photo remains much brighter; it is not silently rebalanced to fit our lot.

The four plates contain 1400 / 900 / 1050 / 1400 native pixels per side for
asphalt / dormer / planting / dusk; no resampling. Camera position, target,
focal length and aspect are independently compared for the hero and dusk.
The apron has finer mineral breakup than the near-black before, with worn
paint and dark routed sealing visible in the full frame. Oils remain absorbed
under selected engine stations; patches and tar do not act as shiny films.

The rightmost mansard aperture now has its sash, glazed pane, curtains and
room backing. Nine actual source rays through that aperture hit its window;
the rightmost room joins the existing selected-room dusk circuit. The new
mixed border visibly breaks the old row of cloned balls: taller/lower clipped
boxwoods, flowering hydrangea groups, empty stations, bark mulch, low edging
and a young corner maple. It uses the family's original 419 / 815 specimens,
with seeded placement, yaw and bounded nonuniform size changes. It does not
claim additional botanical species or newly baked shrub variants.

The unchanged dusk camera now shows pole-light pools across the aisle and
stalls, and an entry pool on the wall and approach. All entry/hall fixtures
have their own engine sockets; nearest actual lens-to-socket distances are
at most **94.51 mm**. New stair bulkheads and existing gallery entry fixtures
will be judged in the extended final night views. Light energies are Blender
presentation settings, not measured illuminance or a luminaire specification.

**What still reads as CG.** The narrow tar zigzag is more regular than a real
repair; the existing Ground grain repeats, plant specimens remain two shared
meshes, the brick/curtain rhythm is tidy, and the window rooms have shallow
backs. The photo fits still compare original plans rather than replicas.
The four requested changes are visible in their plates, so the family can
proceed to the final export views and documentation. No docs image exists yet.
