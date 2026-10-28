# Compact pistol references

All retrieved 2026-10-27. Photos are for inspection, measurement and local comparison only;
no photo pixels enter geometry, material nodes, textures or committed images. Markings on
photographs belong to their manufacturers; the asset has original fictional markings.

| Local file | Direct image/PDF URL | Author / license | Use |
| --- | --- | --- | --- |
| daylight-side.jpg | https://upload.wikimedia.org/wikipedia/commons/0/09/Glock_19_%289mm%29%2C_Generation_3.jpg | Agazoo; public domain, [description](https://commons.wikimedia.org/wiki/File:Glock_19_(9mm),_Generation_3.jpg) | Used black pistol side silhouette, separate steel/polymer values, grip and guard proportions |
| daylight-quarter.JPG | https://upload.wikimedia.org/wikipedia/commons/4/45/Glock_19_Gen_4_photo.JPG | Martin1998cz; CC BY-SA 3.0, [description](https://commons.wikimedia.org/wiki/File:Glock_19_Gen_4_photo.JPG) | Three-quarter proportions, slide shoulders, port, muzzle and grip volume |
| used-detail.jpg | https://upload.wikimedia.org/wikipedia/commons/b/bd/Glock19-5.jpg | Klewitz-Shotgun; CC BY-SA 3.0 / GFDL, [description](https://commons.wikimedia.org/wiki/File:Glock19-5.jpg) | Carried finish, edge highlights and construction detail; later look-dev comparison |

Additional published specification pages (read online, not redistributed):

- [G19 manufacturer specification](https://eu.glock.com/en/products/pistols/g19):
  187 mm overall, 128 mm including magazine, 32 mm overall width, 102 mm barrel,
  15 rounds; slide 174 mm long and 25.5 mm wide.
- [Manufacturer 2020 buyer guide](https://us.glock.com/-/media/global/us/old/us-site/83-downloadable-materials/glock_buyersguide2020_lowres.pdf?la=en):
  compact Gen5 185 × 128 × 34 mm. Our fictional compact selects a 185 mm length and
  the narrower 32 mm envelope, rather than representing one manufacturer's generation.
- [HK compact class comparison, p. 8](https://hk-usa.com/wp-content/uploads/2025/09/VP9A1-Operators-Manual-8.27.25.pdf):
  VP9K A1 186 × 130 × 33 mm, 104 mm barrel, 15-round capacity. Confirms the class envelope.

Internal geometry and animated motion are visual approximations for a game asset,
not manufacturing drawings, functioning mechanisms, or measured mechanical tolerances.

| Local file | Direct image/PDF URL | Author / license | Use |
| --- | --- | --- | --- |
| round2-right.jpg | https://upload.wikimedia.org/wikipedia/commons/9/9d/Glock19-1.jpg | Klewitz-Shotgun (Shotgun); CC BY-SA 3.0 / GFDL, [description](https://commons.wikimedia.org/wiki/File:Glock19-1.jpg) | Opposite side, rounded mold transitions, guard, low sight installation |
| round2-open.jpg | https://upload.wikimedia.org/wikipedia/commons/a/a7/Glock19-2.jpg | Klewitz-Shotgun (Shotgun); CC BY-SA 3.0 / GFDL, [description](https://commons.wikimedia.org/wiki/File:Glock19-2.jpg) | Locked action, barrel projection and hood drop; individually estimated motion values |

The manufacturer also lists steel sight radius **152 mm** (polymer 153 mm) and
trigger distance **71.2 mm**. These are the round-two internal proportion baseline.
[C.I.P. 9 mm Luger sheet](https://bobp.cip-bobp.org/uploads/tdcc/tab-iv/tabivcal-en-page28.pdf)
lists case length 19.15 mm maximum, rim diameter 9.96 mm maximum, cartridge OAL
29.69 mm maximum. The repeated case keeps its accepted dimensions; no stretch
was made to compensate for the foreshortened presentation.

Round-three comparison additions:

| Local file | Direct image/PDF URL | Author / license | Use |
| --- | --- | --- | --- |
| magazine-loaded.jpg | https://upload.wikimedia.org/wikipedia/commons/9/94/Glock_9mm_Handgun_Magazine_-_Loaded.jpg | Tony Webster; CC BY-SA 2.0, [description](https://commons.wikimedia.org/wiki/File:Glock_9mm_Handgun_Magazine_-_Loaded.jpg) | Curled steel lip appearance and body/front/rear height; visual comparison only |

The left-side comparison uses `daylight-side.jpg`, rotated clockwise 30° on a
local comparison canvas by `src/photo_matches.py` so the kit's bounded roll fit
can frame it. The derivative stays in ignored `build/left-leveled.jpg`. No
reference pixels enter mesh, shader or texture construction. Its original
source/author/license are the first row above; the local comparison is not a
committed asset image. Right/open calibrations retain their earlier landmarks.

The final carry correction also uses the original daylight-side photograph for
finish calibration: narrow gray muzzle corners, a thin upper shoulder line and
lighter serration crests against retained dark steel. The broad smooth web
highlight is used to judge palm polish as sheen following the molding. These
are visual estimates of contact, not recovered physical albedos or wear widths.

## Trigger direction correction — 2026-10-28

| Local file | Direct image/PDF URL | Author / license | Use |
| --- | --- | --- | --- |
| trigger-right.JPG | https://thumb.wikimedia.org/wikipedia/commons/thumb/4/43/Glock_19_Gen_4_II.JPG/1920px-Glock_19_Gen_4_II.JPG | Martin1998cz, CC BY-SA 3.0; [description](https://commons.wikimedia.org/wiki/File:Glock_19_Gen_4_II.JPG) | Sharp right side: muzzle-facing concavity, forward toe, broad molded shoe and blade safety. Original contour remains fictional. |
| trigger-left.JPG | https://upload.wikimedia.org/wikipedia/commons/4/44/Glock_19_Gen_4_Pistol_made_in_Austria.JPG | Martin1998cz, CC BY-SA 3.0; [description](https://commons.wikimedia.org/wiki/File:Glock_19_Gen_4_Pistol_made_in_Austria.JPG) | Supplemental full-resolution side close-up: side thickness, edge radii and forward curl. |

The three-quarter trigger pair uses `daylight-quarter.JPG` above (Martin1998cz,
CC BY-SA 3.0), cropped to the guard. The white backdrop is the neutral check;
the right-side foam is approximately neutral gray but the flash is much harder.
No photo contour or pixel enters geometry or materials. Camera landmarks use
frame/guard features, leaving the trigger an independent shape comparison.

Exploratory photographs inspected, then discarded in favor of the sharper
paired views above (no contribution to the model):

- [Gen4 side photograph](https://thumb.wikimedia.org/wikipedia/commons/thumb/1/17/Glock_19_Gen_4.JPG/3840px-Glock_19_Gen_4.JPG), Martin1998cz, CC BY-SA 3.0.
- [Gen4 front-side photograph](https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a3/Glock_19_Gen_4_front.JPG/3840px-Glock_19_Gen_4_front.JPG), TacticalGuy, CC BY-SA 4.0.
- [Earlier quarter photograph](https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fa/Glock_19_01.jpg/1920px-Glock_19_01.jpg), Spike78, CC BY-SA 4.0 (also offered under earlier CC BY-SA versions/GFDL).
