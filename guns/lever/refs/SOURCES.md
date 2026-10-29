# Bracken L20 reference register

Viewed 2026-10-28. Images and PDFs are comparison/measurement references only.
No photograph enters a material, bake, mesh generator or committed image.
The make fetcher downloads only the image/PDF URLs in this table.

Round-two measurement annotations use the same registered photographs.
`src/reference_measurements.py` records native endpoints, estimated camera-plane
lengths and the pivot/belly/throat measurements of the open lever. These are
comparison-only estimates, never mesh inputs. The open photograph recovers an
approximately 105 × 32 mm opening and 2.1 mm side depth; the closed oblique
photograph recovers a smaller opening. The photos do not establish an
identical lever, and their underdetermined perspective prevents treating them
as a single manufacturing drawing. The
open view controls the longer original loop; the closed discrepancy remains
explicit in REVIEW.md. The final form pass keeps that opening and measures the
closed photo's bar against its opening: approximately 3.3 mm at the lower loop
and 13 mm at the bow after normalization. Earlier 2.1 mm estimates document the
thin bar rejected at checkpoint two, rather than the delivered bar.
Transverse 8.2 mm bar width and 1.0 mm hammer checkering
are authored class estimates, not published manufacturer measurements.

| Local file | Direct image or PDF URL | Author / license | Use and limitation |
| --- | --- | --- | --- |
| right.jpg | https://upload.wikimedia.org/wikipedia/commons/4/48/Winchester_Mod_1894.jpg | Hmaag; CC0 | Lower 20-inch carbine, right-side proportions, straight grip, band layout. Upper long rifle excluded from calibration. |
| left.jpg | https://upload.wikimedia.org/wikipedia/commons/b/b3/Winchester_94XTR%2C_caliber_.375_Win.jpg | Cjp24; CC BY-SA 4.0 | Sharp left action/forend construction; different .375 variant, no cartridge measurements. |
| profile.jpg | https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Winchester_94XTR%2C_.375_Win_caliber.jpg/1280px-Winchester_94XTR%2C_.375_Win_caliber.jpg | Cjp24; CC BY-SA 4.0 | Clean left whole-gun comparison. Checkered .375 variant has a heavier receiver and different stock; original uncheckered .30-30 contours retained. |
| left-full.jpg | https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Winchester_94XTR_-_caliber_.375_Win.jpg/1280px-Winchester_94XTR_-_caliber_.375_Win.jpg | Cjp24; CC BY-SA 4.0 | Evaluated only: upside-down wall display, excluded from pairs. Never mirrored. |
| receiver.jpg | https://upload.wikimedia.org/wikipedia/commons/b/bb/Winch_M_94_receiver.JPG | Hmaag; CC0 | Sharp left action with lever fully open; lower link, trigger curvature and screws. Main open-action and sharp trigger comparison. |
| open.jpg | https://upload.wikimedia.org/wikipedia/commons/f/f5/Winch_M_94_Verschluss.JPG | Hmaag; CC0 | Despite the cache filename, this is a closed-action oblique view: hammer, tang and trigger. |
| open2.jpg | https://upload.wikimedia.org/wikipedia/commons/6/6b/Winch94_Verschluss.JPG | Hmaag; CC0 | Right/top closed bolt, loading gate and rear sight construction. |
| left2.jpg | https://upload.wikimedia.org/wikipedia/commons/e/e4/Winchester-94-32spl.jpg | Picanox / Waltherppx; CC BY-SA 4.0 | Independent used .32 Special right silhouette and wood/steel structure; not a finish target. |
| cheek.jpg | https://upload.wikimedia.org/wikipedia/commons/3/3c/Henry_rifle_operation_06_aiming_and_firing.jpg | US National Park Service, Stones River National Battlefield; US government public domain | Shouldered lever-action cheek weld only. Different long-barrel class; no claim that it publishes an eye-distance dimension. |
| ammo.jpg | https://upload.wikimedia.org/wikipedia/commons/f/fe/30-30.jpg | Boris Barowski; public domain dedication | Center cartridge only: rim, long neck and jacket/lead construction. Rounded soft point differs from our required flat nose; no color/material inference before neutral adaptation. |
| cartridge-spec.pdf | https://bobp.cip-bobp.org/uploads/tdcc/tab-ii/tabiical-en-page70.pdf | C.I.P.; published standard, no redistribution license stated | Table II .30-30 exterior envelope: 51.80 mm case, 64.77 mm overall, 12.85 mm rim, 10.71 mm body, 8.38 mm mouth. Visual exterior only. |
| parts.pdf | https://www.winchesterguns.com/content/dam/winchester-repeating-arms/support/parts-and-service/parts/2025/Winchester-Model-94-Parts-List.pdf | Winchester Repeating Arms; copyrighted manufacturer document | Named parts and visible construction. Modern angle-eject/rebound details are distinguished from the older top-ejecting class. No real manufacturing internals are reproduced. |
| manual.pdf | https://www.1895gunner.com/winchestermanuals/21-WRA-061_Model_94_OM_WEB.pdf | Winchester Repeating Arms; copyrighted primary manual, hosted by an independent archive | External anatomy, sight leaf/elevator, loading cover and illustrated lever/hammer states. Our older half-cock/top-eject visual binding is not the modern manual's rebound/angle-eject binding. |

Description pages and licenses:

- [Right, Hmaag](https://commons.wikimedia.org/wiki/File:Winchester_Mod_1894.jpg),
  [open left action, Hmaag](https://commons.wikimedia.org/wiki/File:Winch_M_94_receiver.JPG),
  [closed oblique, Hmaag](https://commons.wikimedia.org/wiki/File:Winch_M_94_Verschluss.JPG),
  [right/top, Hmaag](https://commons.wikimedia.org/wiki/File:Winch94_Verschluss.JPG).
  [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
- [Cjp24 left profile](https://commons.wikimedia.org/wiki/File:Winchester_94XTR,_.375_Win_caliber.jpg),
  [Cjp24 close left](https://commons.wikimedia.org/wiki/File:Winchester_94XTR,_caliber_.375_Win.jpg),
  [Cjp24 display](https://commons.wikimedia.org/wiki/File:Winchester_94XTR_-_caliber_.375_Win.jpg).
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- [Picanox independent right](https://commons.wikimedia.org/wiki/File:Winchester-94-32spl.jpg),
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- [NPS cheek weld](https://commons.wikimedia.org/wiki/File:Henry_rifle_operation_06_aiming_and_firing.jpg).

Published external specifications and manuals, read as pages:

- [Manufacturer 2015 catalog, printed p.30](https://www.winchesterguns.com/content/dam/winchester-repeating-arms/support/print-catalogs/2015/2015-winchester-repeating-arms-catalog.pdf):
  indexed primary table, 20-inch barrel / 38-inch OAL / 13.5-inch pull;
  6.5 lb carbine and 6.75 lb short/takedown class, six/seven capacity listings.
  The live PDF URL returned 404 when fetched; it is not a make dependency.
- [Smithsonian measured carbine](https://americanhistory.si.edu/collections/object/nmah_418211):
  independent 38-inch external length. No museum image downloaded.
- [Manufacturer pre-1992 manual](https://www.winchesterguns.com/support/owners-manuals/model-94-pre-1992.html):
  spring loading cover, lever and sight-elevator illustrations. This page covers
  a later rebound/angle-eject variant; it is not mis-cited as an early half-cock manual.
- [Manufacturer current manual](https://www.winchesterguns.com/support/owners-manuals/model-94.html):
  distinguishes original dropped/half-cock positions from modern rebound;
  describes the dropping lower link and tube-compatible blunt bullet class.

White balance, native neutral patches and estimated gains are recorded by
`src/white_balance.py` in `build/white-balanced/corrections.json`. Reflected
silver and unclipped paper are estimated neutrals, not a color chart. These
form comparisons do not establish final bluing/walnut albedo. Only the locally
generated scripts and this register are tracked; references and pairs are ignored.

- [Boris Barowski cartridge comparison](https://commons.wikimedia.org/wiki/File:30-30.jpg): public domain dedication; center .30-30 only.

## Final form / finish additions

| Local file | Direct image or PDF URL | Author / license | Use and limitation |
| --- | --- | --- | --- |
| rear-blade.jpg | https://homesteadparts.com/shop/images/st207b.jpg | Homestead Parts; copyrighted product photograph, comparison only | Front-facing semi-buckhorn steel sheet beside inch ruler. Native ruler scale and ear/notch measurements in `build/final-form-measurements.json`. Different two-screw insert; no reproduction of its screw pattern. |
| rear-sheet.jpg | https://homesteadparts.com/shop/images/73rearsight.jpg | Homestead Parts; copyrighted product photograph, comparison only | Oblique leaf/elevator construction and coin-gauge blade. No reliable dimensional scale in this image. |

The [seller's measured insert description](https://homesteadparts.com/shop/sight-rear-winchester-vnotch-element-for-semibuckhorn-post64-winchester-94-p-3925.html)
gives 0.355-inch overall height and 0.270-inch notch height; different mounting
construction is explicitly distinguished. Downloaded 2026-10-28. No reference
pixel enters the asset. Product markings are not reproduced.
