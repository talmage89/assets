# Parking garage form review

This log separates preparatory construction review from rendered critique.
Only the exported glTF is allowed to supply the checkpoint geometry. No final
look-dev, manufactured concrete bake or service-age pass is claimed here.

## Preparatory construction review

Color/value first: choose neutral mineral form albedos rather than a white clay
override. Concrete is .34/.325/.29 linear, deck .27/.265/.245, with deep cavities
and a fixed low sun; exposure is not used to make the concrete match a photo.
The final form views still need direct visual review before acceptance.

The PCI reading rejected flange-height light placement: hanging straps now
put the diffusers near the tee-stem underside. The first PT framing attempt
ran its beams along the wrong axis; real transverse 60ft beams now support the
slab between 36ft stations. Ramp girders break at their grade transitions.

The first end decks were thick solid covers. The municipal landings now use
the same tee soffits as the parking bays. Roof ramp columns stop at the last
actual deck; internal and terminal guards protect differences in elevation.
The highest route ends on the flat aisle instead of entering a nonexistent
next ramp. End bays grew to 36ft for tangent turn arcs and lane offsets.

Accessible reservations initially consumed less row width than their shared
aisles needed. The generator now removes the correct full block of ordinary
stalls. The larger garage reserves eight spaces/two vans and the smaller
four/one. Hatching follows the actual 1% plane rather than sinking below it.

Tower doors originally faced opposite directions, and a nominal front stair
door opened under a half landing. Both upper-floor functions now face the
garage landing, with genuine apertures. A separate side exit meets the lower
stair landing at grade. Ticket screens face the driver's side and cabinets
and gearboxes sit on actual concrete control islands. The FULL display has a
back plate and bracket rather than floating beside the entry.

Native context is original library geometry: continuing Main Street rows,
commercial shops, proper alpha-card trees, native luminaires and three car
body types. Cars occupy the per-level stall reservations rather than a single
token car on the street. Nothing in another family is edited.

Three photographic comparisons use recorded neutral patches before fitting.
The Z22 pale sign border, Pleasant Hill shaded enclosure and Harmon sunlit
spandrel are approximate neutrals, not gray cards. Interior fitting uses four
column face anchors and the approximate 33mm EXIF equivalent; the corbel's
outline remains an independent visual comparison. Larger buildings and
different camera processing limit exact claims. The Alewife atrium/roof are
secondary references, not forced matches to a different architecture.

## Pass 1 — six exported Eevee form views

Opened both heroes, both overheads and both aisles in renders/pass1-eevee/. These
images precede the final construction corrections; their views.json records
source hashes. Color/value first: the frame is pale and blue, and the aisle
has almost no contact shadow. The log reports an overflowing Eevee shadow
pool, so these views cannot establish concrete value or cavity darkness.
The next set uses Cycles, with unchanged scalar material albedos and an
explicit clear procedural sky. No weathering is added at this checkpoint.

The municipal hero cuts off the near tower and its roof pole. Move the eye
farther across the intersection while keeping 1.65m height and 35mm lens.
The commercial overhead exposes an unfilled rear portion of its larger
parcel. Add continuous owned parcel ground and a rear landscape strip;
existing library streets continue beyond it. This is a site-construction
error, not an acceptable background crop.

The context hatch/SUV glass and tires also exported as white fallback factors;
this is separate from the shadow failure. Explicit stock quick finishes now
replace their unsupported procedural graph at site assembly, keeping every
original vertex. The sedan retains its native baked PBR.

The 60ft precast span reads in the aisle and its twin-stem rhythm is visible.
The compact garage has transverse downstand beams rather than disguised
tees. Parking density reads as a weekday. The next views must resolve car
contact, end-turn barriers, bearing seats, doorway swings and the stair's
waist construction under real shadows. The first pass is rejected for
presentation and remains a diagnostic, not a deliverable gallery.
