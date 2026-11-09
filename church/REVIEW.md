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
