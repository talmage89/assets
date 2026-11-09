# Church form and construction review

## Preliminary export inspection — pass 1

Color/value first: the shared brick has readable fired variation, but the
sky fill in `renders/pass1/101/hero.png` lifts the stone, the door is pale oak,
and the roof goes too blue. This initial assembly diagnostic has no ground;
it is not an acceptable site hero. Compare the later contextual views before
accepting its overall exposure. Reduced procedural sky contribution from .19
to .06 without raising exposure; darkened door timber and mineral trim.

Inspected all four exported-glTF images in `renders/pass1/`: both heroes and
both oblique overheads. The modern gable's repeated diagonal waves expose a
UV mapping error: each narrow panel stretched the whole art-glass height.
Replaced that with a single meter-related chart across the complete gable.
The historic storm sheet reflects almost white at this camera and needs a
close view; the rose's color is also too difficult to read. Both now preserve
two-sided art-glass faces through export. This needs render confirmation.

Form/construction: the historic door is too small in its blank gable wall;
it needs an articulated portal and a tympanum, rather than only square jambs.
The 1996 ramp has no real side aperture yet. The modern A bents need visible
steel shoes and end connections; their roof interface needs inspection.
The modern roof and hall need drainage and HVAC construction appropriate to
their low eaves, rather than the tall historic rainwater spacing.

Reference inspection: HABS IL-1223 sheets 3/5/9/11/14 were opened, individually
or on `build/habs-contact.jpg`. Sheet 11's deep arched entry and sheet 14's
layered window construction make the missing portal/recess depth clear.
The Chapel for the Children nomination's photos 2–8 were opened at full size.
Their neutral concrete walk is the white-balance reference, not the warm red
brick. The roof is dark neutral gray, the glass largely dark in shade and the
timber end/fascia has real gauge and sheltered shadow. Its curved tent roof is
a different subtype: our straight A-frame is not a reconstruction of it.

This is a preliminary diagnostic, not one of the three photographic review
passes required for acceptance. The pairs, source/ship comparisons and their
measured camera residuals still have to be completed.

## Construction and street inspection — pass 2

Color/value first: inspected all eight `pass2` images and all ten `pass3`
images. The overfilled blue roof and pale wood improved with lower sky fill
and the dark door. The next lighting pass uses a fixed daylight exposure .15,
4.5-strength warm sun and .06 sky; it must retain front stone detail and dark
recesses. The church should read as a maintained old building, not pale clay.
No wear approval is claimed at this form gate. The reference's unmarked gray
arrival drive supplies the modern neutral; the HABS references are monochrome.

The tower/entry is now articulated, but the side lancets were too broad for
their height compared with the storm-covered window in HABS TN-145-5.
Changed them to 1.4m wide, 3.1m stem and a 1.212m pointed head. The standing
entrance human remains a separate 1.8m presentation figure, with feet moved
off the stairs. The heroes were in neighboring backyards; moved both onto
clear across-street sight lines and moved the tower close-up out of foliage.

Construction tests rejected the original door and bell assemblies. Rebuilt
the hinges with 9mm sleeve bores, 7.5mm pins, 2mm axial knuckle gaps and a
55mm leaf datum above the threshold. Set the closers' outward stops at 90°.
Moved the rear condenser out of the exit sweep. Shifted the bell wheel outside
the bearing planes and raised the campanile crossbeam above its spokes. The
fresh-import sweeps now pass at 15° samples with no contact exceptions:
doors 0..90° outward; bells ±30°. Sampled maximum penetration is under 0.1mm,
below the 1mm tolerance. This is sampled surface testing, not a continuous
engineering clearance guarantee.

The original straight glulam bars did not actually follow the roof underside.
Rebuilt them as 620 × 240mm rafters on outboard concrete shoes, with their
outer face at the roof's underside and miters at the ridge. Moved the rear
hall beyond the last bent rather than intersecting its feet. The range now
includes a white clapboard chapel using the native house siding maps.

Slate courses were stretched over an entire roof panel. Their shared chart
now repeats at 406mm width and 196mm visible gauge, with physical tile cuts.
The sign atlas's W/M glyphs spilled outside their cells; refit each cell and
kept the same 1024×512 allocation. Both fixes need the next exported renders.

## Photographic form review A — first three calibrated pairs

Inspected the three full-size pairs from the first complete export set, not
only their contact sheet. Archived evidence is in the worktree's ignored
`build/church-review-evidence/before/`. These are three different photographs.
Color/value first: HABS MD-1298-1 and TN-145-5 are monochrome, so they support
value and construction comparison, not a brick hue match. The modern photo
was balanced on its unmarked gray arrival drive; median RGB .557/.565/.545,
channel gains .998/.984/1.019. Its abandoned 2024 condition is form evidence
only. The rendered brick is warmer and cleaner than the gray stone reference
by design. Recesses stay dark; the smooth, even trim still looks new.

The street pair exposes the largest style difference: our rectangular brick
tower is plainer than the reference's stone tower, open timber stage and
splayed spire. Those are distinct construction choices, not missing replica
parts. Our recessed portal, stepped buttresses and measured arched apertures
are legible. The front wall remains visually spare. Preserve this as an
unresolved architectural refinement for the look-dev gate, not proof of a
photographic match. The fit has 30.6px RMS at 705px source width.

The modern pair now has a credible roof/bent/low-wall relationship and a
different garden/wing plan. The source's A roof is slightly curved and has
separate outboard supports. Ours is straight, on mitered glulam bents and
steel shoes. The previous whole-gable glass chart produced absurdly broad
leading and giant medallions; the replacement divides the art glass into
physical panels with fine leading. The gable remains more colorful and
regular than the photograph. Fit RMS 24.3px at 878px, with lens at 28mm bound.

The window pair failed as an inspection image: the required obliqueness put
a neighboring buttress in front of the lancet. Keep the actual buttress;
compare the isolated exported WallBay module against this flat-wall photo
instead. The photograph's narrow perspective is not evidence to shrink the
whole window again. Also found and corrected the ramp's lower landing in
the hall footprint, shrubs inside the modern education wing, unsupported
rear meters, and the 100mm gap below the spire cross. Added surface checks
for the cross seat and route centerlines. Reframe the obstructed wing view.

## Photographic form review B — unobstructed module and both parcels

Opened all three regenerated pairs and all 18 street/detail/site views.
Evidence is archived in `build/church-review-evidence/pass-b/` at the worktree
root. Color/value first: the same arrival-drive neutral and gains are used;
the HABS images remain monochrome. Hero display-luma percentiles (1/50/99)
are 0.8/125.2/194.1 for 101 and 4.1/110.4/188.7 for 202 on 0–255 output.
Clipping is below .002% of pixels in each hero. These whole-image readings
include sky and do not prove albedo accuracy. Dark cavities are retained.

The isolated WallBay comparison now reveals the complete aperture, frame,
storm bars and recess; RMS is 9.4px on a 170px-wide reference. Perspective
remains more oblique than the photo, and the 100mm lens bound is active.
This is a construction comparison of two different wall types, not a
reconstruction accuracy claim. The day/dusk pairs show a muted historic
window becoming emissive. The modern glass now has millimeter-scale lead,
but its repeated diamonds still look too regular across a full gable.
Its age and pattern need the later look-dev, not more silhouette triangles.

The street views show real parcel differences and the Sunday lot's full
occupancy. They also expose plain clipped lawns and coarse reduced house
roofs in the distance. The new stone/wood trim is still too uniformly clean;
the portal rebates help depth but do not supply decades of maintenance.
The 2009 Perris photo, now inspected locally, has darker glazing, jointed
surfaces and localized sheltered discoloration. Its neutral concrete steps
are the color reference; its elaborate ornament is not our style target.

Construction corrections prompted by this pass: seat the gutters at the
actual sloping eave, fill the upper ramp to grade, thicken raised paving
down into the ground, bring printed sign letters within 4mm of their face
to remove doubled shadows, and extend the canopy across the drive while
keeping its posts outside the vehicle path. Move the modern lot behind the
public sidewalk, enlarge it for 31 stalls, and put both depressed driveway
curbs on the parcel side of the street. Add an imported-surface curb check.
The earlier routes tested church obstructions only; they did not prove
street access. Reframe the wing views to include their lots and light the
historic rear inspection from that side. These changes await the final set.

The relit rear view then exposed an elevated rear leaf without steps. Added
a filled 1.8m-deep landing, measured-rise treads and iron rails at the historic
rear exit, a matching low modern rear landing, a walk to the rear lot and a
small hall entrance landing. Fresh door sweeps still pass, and all 39 own
geometry/map repeat payloads agree exactly. This is a construction correction,
not an aging iteration. A final clean rebuild follows these changes.

One final construction audit identified the annex roof crossing the lower
three right-side lancets. Closed those lower openings and retained their
original arch heads with higher glazed sills. The other side's tall windows
are unchanged. Added a fresh-import measurement of the lowest affected glass
against the actual highest annex vertex; do not accept a configured roof
height as evidence of clearance.

## Eevee culling rejection and correction

The first final Eevee frame failed: portions of the gable, roof and spire
vanished. Cycles had hidden the problem by drawing back faces. I should have
checked this earlier. Unit normals and matching re-import counts had not
proved outward face winding. The culprit was recalculating normals after
UV splitting, when every polygon had become a disconnected island.

Normalize prism winding against its extrusion direction before UV splitting,
preserve the primitive winding through triangulation, and interpolate smooth
loop normals across coincident curved-surface UV seams. Do not mask the fault
with double-sided masonry. Added imported geometric-normal checks on the
front gable and both roof skins. Re-render Eevee first, then the full set.
The same review identified coarse bell shading and procedural bronze bands;
the smooth-normal correction addresses the former, while the bronze's
surface pattern remains look-dev work. The range and isolated modules now
use neutral studio backgrounds; the shoe is framed at detail scale, and
rear steps are viewed from their tread side.

## Photographic form review C — corrected export and source, final gate

Opened all 56 final PNGs, including every module, all 18 site views, the
four-church range and Eevee. Reopened all three exported/photo pairs and
their three source/photo counterparts. Color/value first: the modern photo
still uses the gray arrival-drive neutral (.557/.565/.545 RGB, gains
.998/.984/1.019); the two monochrome HABS photographs cannot calibrate hue.
Final hero display-luma percentiles (1/50/99) are .8/125.2/194.1 for 101
and 3.8/123.2/188.6 for 202. Clipped channels affect 0% and .00023% of pixels.
The actual surfaces retain dark recesses and highlight detail. These whole
frame statistics do not certify material albedos or photographic realism.

Form: the street pair reads as a town church at the right human scale, with
a deep portal, slender lancets, substantial buttresses and an assembled bell
stage. The reference's stone front and timber belfry are richer and less
regular than our deliberately simpler brick design. The broad front wall,
minimal rose tracery and square trim still advertise a procedural asset at
close range. This is an original design, not a claim that those differences
have disappeared. The HABS details support reveal depth and layered frames;
the image-fit residuals remain 30.6/24.3/9.4 source pixels, not survey error.

Construction: the later hall now leaves .420m from its highest vertex to
the lowest affected art glass. The raised lights preserve the original arch
heads. The rear exit has a supported landing, rails, steps and a lot walk.
The A-frame's bent ends meet shoes, its ridge is mitered under the covering,
and the drop-off roof covers the drive on seated posts. Fresh imports verify
1,708 historic and 56 modern outward-facing gable/roof triangles, in addition
to the measured ramp, curb and motion checks. The corrected Eevee image no
longer loses opaque faces. Its glazing uses the library's raytrace/6mm slab
setup; screen reflections still differ from Cycles and need engine testing.

Glass: daylight on the historic storm sheet is dark and hazy, and the dusk
view reveals the lead and muted color. The close matched module shows the
stand-off, bars, sill and reveal without the old buttress occlusion. The
protective glazing still needs more credible yellowing and detailed breathing
slot verification. Modern repeated diamonds look too regular across a whole
gable. The bell is smoothly shaded now, but its wavy bronze pattern is
plainly synthetic. Correct its patina from exposure/handling in look-dev.

Place: Sunday has 17 occupied stalls and four street cars; the weekday site
has seven cars in 31 stalls. The wider modern overhead shows the whole lot,
walks, canopy and arterial; the rear views reveal actual churchyard access.
The corner's commercial row and the arterial's houses distinguish the sites.
Parcel lawns are still planar, distant roofs are coarsely reduced, the wider
district is sparse, and maintenance history is too weak. They are substantial
remaining look-dev/place work. No age or photographic-finish approval follows
from successful checks. No final docs images are committed.

The input-hash audit passes all 56 renders. Source/export matched images
have mean absolute RGB differences of approximately .09/.13/.04 on a 0–255
scale, showing that export preserves this source appearance; that does not
prove the source itself looks real. Stop here at the requested form and
construction gate, with the weaknesses above exposed for lead review.

## Place and age review D — first revised export set

Color/value first: opened all eight full-size `renders/look-a/101,202/`
views and the three composed pairs. The new Gothic reference is the MDAH
April 2009 color photograph, prepared at 1000×960, balanced on the concrete
entry steps (360,925..420,934). The modern pair retains its arrival-drive
neutral. Brick is still too even in value and repairs are too hard to see
at hero distance. Buff trim is improved but needs grime specifically below
projecting moldings. The lawns have their own yellow-green rather than the
old dark felt; their broad patches still look interpolated from a coarse grid.

The street context is substantially closer: distinct native storefronts,
an alley, Sunday street parking, varied houses and yard trees. The modern
overhead still exposes an empty eastern half-block. Add the adjoining local
street and two lots there, rather than filling the land with isolated props.
The tree beside the downtown sign hides its letters; move it along the same
parkway. Smaller parking-island trees will reveal the education-wing roof.

Historic glass now has a pale field and one symbol panel. Its colored border
is clipped by the old UV range and does not follow the arch. Correct the
border chart and UVs. Modern clear glazing reflects the sky and town against
a dim nave, but the faceted cross stretches its atlas differently in its
vertical and horizontal arms. Give its facets one physical scale and reduce
the relief. The 20-sample clear-glass specular noise needs a higher-sample test.

The Gothic color fit is 17.72 px RMS; the modern is 24.32 px. The provisional
13.90 px window fit is REJECTED: on opening the composed pair I saw that the
selected small tower lancet was infilled with brick, not protective glass.
That was my reference-selection error. It supplies no glass evidence. Replace
it with the NPS NCPTT photograph explicitly captioned as yellowed plastic
protective glazing on a brick church, and retain the rejected pair only in
the ignored iteration evidence. No accepted result relies on that fit.

## Place and age review E — corrected glazing pair and density

Color/value first: opened all eight `renders/look-b/` street/site/window PNGs
and all three complete pairs. The concrete-step balance is now explicitly
RGB .667/.627/.584, gains .939/.998/1.072. The same clear gable-brick patch
(674,575..695,595 in the prepared street frame) measures 143/99/95 in the
balanced photograph and 151/105/80 in the export. These display RGB medians
are lighting-dependent, not measured physical albedo. They still expose an
orange bias. Correct the brick tint toward red-brown before finer wear.

The replacement window is definitively protective glazing: Jason Church's
NCPTT photograph is captioned as clouded/yellowed plastic over stained glass
on a brick church. Compare its left light, with its shared tracery visible at
the crop edge, against the original exported lancet. It is not a replica of
that multi-light window. Balance on the white-painted exterior bar, RGB
.741/.749/.710, gains .989/.979/1.033. The fit is 4.43 px RMS on the native
240×570 crop; the 150mm lens limit is active. The brick hue target remains
the red-brick street photograph, not this buff-brick window surround.

The daylight export is dark olive behind the protective reflection, with a
visible but subdued memorial field. Dusk now shows a continuous blue/amber
border following the pointed crown, pale cathedral glass and a central cross
panel. The modern cross now has one physical facet scale; clear glass shows
the reflected town and the dim nave. It still has specular grain at 40 samples,
and the simple geometric composition is less rich than historical craft.

The additional two eastern lots close the modern block instead of leaving
its east side as a field. The island trees are smaller, the wing roof reads,
wheel stops sit at real stall heads and the seven weekday cars are spread
between both rows. The front lot row needs another .6m of depth to preserve
the intended aisle width after adding the grass buffer; measure that on the
fresh import. Sunday curbs are lined with cars. Native distant roofs remain
coarsely reduced; that is a context weakness, not a church-triangle excuse.

Front repairs now read at the tower base, but the age is still too weak on
large lit walls. Add splash-zone color samples only to the front gable,
tower shaft and modern low walls; retain the accepted WallBay count. Darken
runoff below actual tower courses, and make the corner-cut traffic line
continuous rather than relying on a two-meter lawn grid to find it. The next
export pass must judge those changes at hero size before the complete set.

## Place and age review F — color correction on the exports

Color/value first: inspected all eight `renders/look-c/` PNGs and all three
composed pairs. The same concrete-balanced front-gable brick patch now reads
145/101/93 against the photograph's 143/99/95. The low sun still makes the
hero warmer; the old orange hue is corrected without raising exposure or
flattening cavities. The two storm-window images retain dark daylight and
a pale, luminous dusk field, rather than saturated primary quarries.

The refined front/tower base now carries interrupted damp and salt deposits;
repairs are visible at the tower foot. Fixed course joints feed short runoff
paths. These remain maintenance cues on red masonry rather than a gray wash.
The front gable remains plainer and more even than the old church photograph;
some of that difference is the accepted original architecture. Keep it honest
as an appearance limitation rather than claiming a product-photo match.

The continuous lawn ribbon failed this review: from above it read as an orange
line drawn across the grass. Reduce both chroma and contrast and vary its
intensity along the route, retaining compressed grass instead of rust-colored
bare earth. Reframe the modern wing view outside the new island tree canopy.
Capture dedicated beam/step and north-roof views in the full set so moss and
end-grain wear are actually inspected, rather than inferred from shader code.

The native houses now supply lot widths, driveways, fences and yard trees.
Their roofs remain visibly coarse at aerial distance and the district beyond
these blocks is sparse. The new faceted cross is confined to about five
percent of the gable glass; it no longer turns the entire sanctuary front into
a repeating colored mosaic. The NCPTT pair is valid glass evidence at 4.43px,
not the rejected brick infill. Fresh-import tests pass wheel-stop placement,
7.3136m modern aisle, the clear/colored area ratio and a measured .0200m lower
air slot. These measure the imported surfaces, not renderer serialization.

## Place and age review G — full-size failures, then targeted inspection

Color/value first: inspected the revised 1400px downtown hero, overhead,
door, glass, tower, sign, scale/entry and north-roof views. The lawn's orange
shortcut is gone; its grass stays yellow-green with interrupted compression.
The low sun retains dark belfry cavities and sidewall shade. The stone entry
and door panels remain too even, despite the warmer stone and lower-base
maintenance. Do not call that photographic finish.

The first full capture exposed the parish-hall camera inside the new tree.
Stopped the owned render process, released its lock and moved only that
inspection camera. In all six `renders/look-g/` exports the new wing camera
clears the tree; the modern wing/lot view also clears its island canopy.
Both still show their imported context. The original hero/overhead/glass
cameras stay unchanged for native-size before/after comparison.

Runoff previously used GroundTrim's very faint deposit alpha (median 1/255,
99th percentile 52/255), so much of the modeled age disappeared. Repurposed
the unused ChurchGlass quarter for deposits, adding no texture allocation.
This removes GroundTrim from the standalone historic building's resident
union. The stronger roof test then failed honestly: all 24 thin drips in
each patch looked like rectangular barcodes, especially on the A-frame.
Do not ship `look-g` as the north-roof appearance. Divide that spare quarter
into a vertical runoff chart and a separate broken, wavering growth chart
following damp slate/tread joints. The next export inspection must prove it.

The day glass is subdued; the modern clear field reflects houses over the
dark nave. Specular grain is visible in the close door view at 32 samples.
The existing unbatched module hierarchy and coarse neighboring roofs remain
performance/context weaknesses. These observations come from the images,
not passing triangle counts or source/export equivalence.

## Place and age review H — complete exported checkpoint

Color/value first: inspected all 61 current checkpoint PNGs, their contact
sheets, all three final color/form pairs and the eight 1400px-per-panel
before/after JPGs. The street photo remains balanced on concrete steps, the
modern on its gray arrival drive and the NCPTT glass on its white-painted
storm bar. The same brick sample stays 145/101/93 against 143/99/95. The hero
99th-percentile display luminance is 190.8/203.4 of 255; clipped fractions
are .00000153/0. The dark belfry and nave remain dark, while broad highlights
stay below clipping. These frame/display observations are not albedo readings.

The final overheads prove the place changes: the historic church has six
different nearby storefront hosts, parsonage/house neighbors, a rear alley,
a Sunday rear lot and occupied curbs. The modern church has individually
placed houses at 23–25m lot widths, local streets, drives, fences and yard
trees. Its 27-stall lot has six weekday cars, islands, poles and stops at the
heads, not along the street. No accepted church massing or generator range
was redesigned. Native reduced house roofs still look torn/coarse from above,
and the larger district beyond these blocks remains sparse.

The old random primary quarries are gone. Historic dusk shows a cream/sage
field, blue/amber border and cross panel; day shows a dark field behind the
yellowed reflective protective sheet. The modern gable is mostly clear over
a dim nave, with one physically scaled faceted cross. Its glazing still has
specular grain at 48 samples and its composition remains simple. The NCPTT
comparison has much cloudier plastic and white painted shared tracery; our
original window is less opaque. Buff versus red surrounding brick is not
treated as a hue match. The complete color street/window fits are 17.72px
at 1000px and 4.44px at the native 240px crop; modern stays 24.32px at 878px.
All lens bounds are active. These are framing comparisons, not reconstructions.

The new joint-growth mask removes the rectangular drip-barcode test. Growth
is still flat and a little brush-like close up. Front/tower repairs, base
moisture and course runoff are visible, and the lawn stays its own summer
yellow-green with mulch under the shrubs and fine clipped edges. Entry stone,
door panels and steps remain too uniform. Surviving fascia paint looks like
coarse patches close up; beam ends remain too warm. Cross rust, ledge/bird
deposits, roof-repair and flat-roof ponding history under-read. These are
remaining appearance tasks, not concealed by successful resource checks.
Eevee preserves the form but differs in glass/reflections and thin paint
patch visibility. The module hierarchy still needs static batching.

The render batch received two SIGTERM interruptions, with no Blender traceback;
the cause was not established. Both processes exited. Recovery reused only
captures with matching package, renderer, camera, engine, dimensions and
PNG-recorded sample counts, then completed the missing frames under the lock.
The 61-image audit passes. Source/export mean absolute RGB differences are
.254/.079/.260 on a 0–255 scale: this proves preservation, not realism.
The independent rebuild reproduces 42 own BIN/new-and-lawn PNG payloads,
62,053,256 bytes exactly. Other deliveries' 1,080 recorded files are unchanged.
No kit change, docs images or README gallery is included. Stop at this review
checkpoint; final delivery remains the next round.

## Final round I — the ten exported correction views

Color and value first: opened both 1400px heroes, both obliques, both age
macros, both north roofs and both entries in the last-pass1 capture. The
photographic neutrals remain the concrete steps in the MDAH street photo,
the unmarked arrival drive in the Connecticut view and the white-painted
storm bar in the NCPTT photograph. The accepted red-brown brick hue is kept;
the new change is wall value and caused dampness. These are display-domain
comparisons, not a physical albedo measurement. The downtown composition,
sun, neighbors, curb parking and window composition are unchanged.

The A-frame's opposite-side 16-degree sun puts light on the wing's brick,
casts beam/mullion shadows across the clear front and removes the ambiguous
large shadow from the foreground road. Its .045 sky strength is deeper than
the former .09. This is the strongest landed fix. The sanctuary backing is
still plainly simplified in the close entry, and 32-sample glazing has grain.

The downtown tower now shows runoff from actual courses at hero distance,
but the close view reveals a repeated narrow-track pattern. The slate's
first increased value range also looks checker-like on the spire. Before
the final rebuild, reduce that range and replace 24 narrow runoff tracks
with seven broader, softer washes. The north asphalt now uses only the
three-tab half of RanchRoof, at its actual 143mm exposure, rather than
alternating both atlas styles. Its first long algae layers look like barcode
columns. Reduce them from seven regular stations to four irregular areas,
starting at the ridge, with lower contrast and the broader runoff chart.
Do not call the first north-roof test a successful age treatment.

Larger moss colonies are visible instead of dots but remain flat, brush-like
stamps. Roof replacement packets read more clearly, although their rectangle
boundaries are regular. The new wall/base values are subtler from the hero
than the tower runoff; front cars hide useful lower-wall evidence. Upper
walls and long buff trims still read too fresh beside the used photograph.

The lawns are darker yellow-green with low-frequency drought patches and
walk-edge wear. Obliques expose their coarse interpolation and planar base;
mulch is a dark strip, not a rich bed. The stone treads now have real 14mm
center hollows, darker footfall zones and small nosing losses, but the close
view exposes faceted rectangular color bands. Door touch wear under-reads;
rail-foot oxidation looks like a simplified orange collar. The beam ends
are grayer, yet the fascia still has thick, rectangular surviving-paint
pieces and lacks convincing checks. These are partial fixes, retained as
known flaws rather than grounds for another open-ended look round.

All ten frames were inspected before gallery creation. The last-pass1
evidence is retained under the worktree's ignored build/church-handoff
archive; final correction crops compare directly with the c655bb4 handoff.
Proceed to clean export, all finals and delivery checks. No more form or
place redesign is authorized by this critique.
