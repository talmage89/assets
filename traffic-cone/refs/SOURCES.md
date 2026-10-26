# Traffic cone sources

| Local file | URL | Author / license | Used for |
| --- | --- | --- | --- |
| dimensions.pdf | https://orangegearsafety.com/images/products/cones/specs/DataSheet-OG2810SO64B.pdf | OrangeGear; copyrighted, local research only | 28 × 14 × 14 in, 7.5 in cone base, 6/4 in bands, 0.1 in wall, open grip dimensions |
| product.png | https://orangegearsafety.com/images/com_hikashop/upload/orange-top-cone.png | OrangeGear; copyrighted icon, looked at and rejected as a photo | Not used in modeling or comparison |

`sheet-*.jpg` are locally extracted images from the cited PDF, same author/rights. `sheet-004.jpg` is its actual 182 × 435 product photograph and is used only for source/exported-GLB comparisons. Regenerate with `make photo` (installed Poppler pdfimages).

| used-roadside.jpg | https://images.unsplash.com/photo-1633580886553-e5c26e0348f2?w=1200&q=85&fm=jpg | June Heredia / Unsplash license https://unsplash.com/license | Installed worn cone: rubber transfer, dirty collar, road grime; https://unsplash.com/photos/9AFU18FL24k |

Additional images inspected and rejected for the wear calibration (not fetched
by `make refs`):

- `used-road.jpg`: [Broadmoor3425Cones9Jan.jpg](https://upload.wikimedia.org/wikipedia/commons/7/7d/Broadmoor3425Cones9Jan.jpg),
  Infrogmation, CC BY 2.5. The cones are too distant and lack the required collars.
- `used-parking.jpg`: [Free Parking Cone](https://upload.wikimedia.org/wikipedia/commons/7/78/Free_Parking_Cone_%28886973341%29.jpg),
  David Blaikie, CC BY 2.0. The cone is horizontal, partially occluded and too small
  for useful wear calibration. Both were used only to select a better photograph.

| used-campus.jpg | https://upload.wikimedia.org/wikipedia/commons/6/61/Bright_orange_cone_on_the_campus_of_George_Washington_University.jpg | Ser Amantio di Nicolao / CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/ | Installed road-used cone, 22 July 2024: moderate vertical sleeve abrasion, low rubber transfer and scuffed black base. Photographed duct tape/markings are not reproduced; dimensions and collar proportions differ. Source page: https://commons.wikimedia.org/wiki/File:Bright_orange_cone_on_the_campus_of_George_Washington_University.jpg |

The campus photograph was opened as a secondary qualitative reference for
ordinary sleeve abrasion and base scuffs. Its unknown tall-cone dimensions,
double foot and taped neck give a poor 141.58 px full-envelope fit at 1200 px
width, so that full fit was rejected rather than changing the specified 28-inch
geometry. A separate four-landmark fit uses only the common body envelope,
excluding the different foot and taped neck. The `used_campus` pair calibrates
moderate sleeve abrasion and base scuffs; the `used_roadside` pair supplies
the much heavier sleeve-failure upper limit. The unknown sizes do not establish
our dimensions. Neither photo enters a material.
