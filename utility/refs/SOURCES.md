# Utility reference register

Downloaded images/PDFs are local inspection only. No pixels enter geometry,
materials or markings. URLs below retrieve only images or PDFs. Publication
rights stay with their authors; no source image is redistributed in Git.

| Local file | Direct URL | Author / rights | Used for |
| --- | --- | --- | --- |
| wps-poles.pdf | https://www.wisconsinpublicservice.com/joint-use-management/ju-standards/pole-info.pdf | Wisconsin Public Service / We Energies; published utility standards, copyright retained | P25 embedment, P30 ANSI class circumferences, P5 brand/tag locations, P15–20 bolt/gain construction |
| wps-joint.pdf | https://www.wisconsinpublicservice.com/joint-use-management/ju-standards/joint-use.pdf | WPS / We Energies; copyright retained | JU10: NESC 238E safety space, 232-1 ground clearance, pole versus span clearances and equipment rules |
| wps-services.pdf | https://www.wisconsinpublicservice.com/partners/builders/manual/section7.pdf | WPS; copyright retained | Section 7 Type-A cabled services: general 16-ft service clearance versus limited residential-driveway 12-ft exception; roof and road/yard distinctions |
| wps-3phase.pdf | https://www.wisconsinpublicservice.com/joint-use-management/ju-standards/three-phase-framing.pdf | WPS / We Energies; copyright retained | C01 wood arm/pin/braces, C20/C40 armless, construction differences at angle/deadend |
| wps-transformer.pdf | https://www.wisconsinpublicservice.com/joint-use-management/ju-standards/transformer-framing.pdf | WPS / We Energies; copyright retained | Can hangers, cutout/arrester placement, grounded-wye leads, three-can support hardware |
| wps-guy.pdf | https://www.wisconsinpublicservice.com/joint-use-management/ju-standards/guying-and-anchoring.pdf | WPS / We Energies; copyright retained | G series: load-side guying, anchor rod, strain and guy markers |
| pse-joint.pdf | https://www.pse.com/-/media/Feature/PSE/Construction-Service/Technical-Resource-Documents/Electric-Service-CommercialIndustrial-and-Multifamily-Permanent-and-Temporary-Service/Attachment-and-Clearance-Standards-2017-Update.pdf?modified=20220621214006 | Puget Sound Energy; copyright retained | 0700.8000: 40-inch ungrounded supply separation, 30-inch grounded equipment allowance; compared with WPS |
| pole-tables.pdf | https://www.sfasilviculture.com/documents/fieldsilv/pole_classification_2017.pdf | Association of Southern Forestry Clubs; copyright retained | Published ANSI O5.1-2008 southern pine table cross-check |
| nreca-staking.pdf | https://www.cooperative.com/programs-services/bts/Documents/Reports/SimplifiedStakingManual.pdf | NRECA / Cooperative Research Network; published technical manual, copyright retained | RUS/REA assembly cross-reference, NESC-derived Table 2.1, staking, tension and sag, guy anchor directions |
| mps-transformer.pdf | https://metapowersolutions.com/wp-content/uploads/2023/05/SPECS_Single-Phase-Pole-Mounted-Distribution-Transformers.pdf | Meta Power Solutions; manufacturer, copyright retained | 50 kVA: 42-inch overall height, 20-inch tank, 26-inch width and 29-inch depth envelope |
| hubbell-ties.pdf | https://hubbellcdn.com/salesdrawings/LDIC_CC-26966.pdf | Hubbell Power Systems; manufacturer, copyright retained | ANSI 55-2/55-3 tie and neck connection construction |
| residential-a.jpg | https://www.opendurham.org/sites/default/files/styles/full_width_image/public/images/2009_5/CrestSt_W_041209.jpg?itok=5-cSfwBL | Gary Kueber / Open Durham, 12 April 2009; copyright retained, local comparison only | Residential NC street: three-phase vertical framing, spacing, line silhouette, planting strip and service age |
| residential-b.jpg | https://upload.wikimedia.org/wikipedia/commons/e/ed/Houses_in_Oxon_Hill.jpg | Ser Amantio di Nicolao, 13 June 2015; CC BY-SA 4.0 | Residential Maryland street: maintained older distribution equipment, transformer, sag, communication hierarchy; photographed after the modeled installation period |
| street-a.jpg | https://upload.wikimedia.org/wikipedia/commons/2/2a/North_Bennington%2C_Vermont.jpg | Mark Barry, 21 April 2007; CC BY 2.0 | Supplemental period crossarm and street hardware; commercial edge, not one of the two residential fits |
| street-b.jpg | https://upload.wikimedia.org/wikipedia/commons/8/8f/Phone_Pole_Valley_%284977085933%29.jpg | Superior National Forest, 10 September 2010; CC BY 2.0 | Supplemental wood silvering and long-span sag; not a residential comparison |
| hardware.jpg | https://upload.wikimedia.org/wikipedia/commons/d/dd/Southeastern_United_States_Utility_Pole.jpg | AdventureStoryFanGamer, 30 May 2024; CC BY 4.0 | Supplemental maintained hardware construction; not period dating evidence |
| telephone-cables.pdf | https://www.caledonian-cables.co.uk/DdFls/Telephone%20Cables.pdf | Caledonian Cables; manufacturer, copyright retained | GR-421 air-core 200-pair .63 mm: 37 mm jacket, 1.771 kg/m. Geometric cable envelope, not a claimed US vendor installation |

Supplemental inspection, excluded from the automatic fetch list: `howard.pdf`,
[Howard Industries conventional pole-mounted transformers](https://howard-ind.com/Power/Product/DisplayDocument/14),
Howard Industries, copyright retained. Used for conventional versus CSP can
construction, the single HV bushing and accessories, not dimensions. The
endpoint's TLS chain fails in this environment; it is not a required rebuild input.

Read-only online references (no executable or asset downloads):

- [USDA RUS bulletin index](https://www.rd.usda.gov/resources/regulations/bulletins),
  and [1728F-804, 2005](https://www.rd.usda.gov/media/file/download/uep-bulletin-1728f-804.pdf).
  USDA's PDF endpoint returned HTTP 403 here. The available NRECA manual provides
  the published REA/RUS cross-reference and reproduced construction examples.
  The implemented drawing baseline is WPS, not an assertion of exact RUS unit compliance.
- [WPS joint-use document index](https://www.wisconsinpublicservice.com/joint-use-management/).
  WPS permits 30 inches at an effectively grounded neutral under its stated
  conditions; PSE uses 40 inches at a secondary/neutral. This family keeps
  40 inches to every supply conductor and at least 30 inches to grounded hardware.
- [ANSI ASC O5 standards](https://asco5.org/standards/), publisher; wood-pole
  class specification, not an installation-depth standard. Period dimensions
  are available in WPS P30 and the 2008 table above. No paywalled standard is
  claimed to have been downloaded/read.
- [Hubbell ANSI 55-3 pin insulator](https://www.hubbell.com/hubbell/en/products/porcelain-pin-type-insulator-ansi-55-3/p/15841797):
  4.75-inch shed diameter, 3.75-inch height, one-inch pin hole; copyright retained.
- [Southwire ACSR specification 80100](https://cabletechsupport.southwire.com/cablespec/download_spec/?country=US&spec=80100):
  Raven 1/0 6/1, .398-inch OD; Sparrow #2 6/1, .316-inch OD; copyright retained.
- [Southwire triplex service drop](https://www.southwire.com/wire-cable/600-volt-secondary-distribution/al-xlp-triplex-service-drop/p/AL600V66):
  two insulated aluminum hots and neutral messenger. Construction reference only; the selected dimensions below come from the
  Classic Wire table, without a claim of an ampacity design.
- [Classic Wire #4 triplex service drop](https://www.classicwire.com/products/triplex-service-drop-aluminum-conductor-acsr-neutral-messenger/),
  manufacturer, copyright retained: Periwinkle .303-inch insulated hots,
  #4 6/1 .250-inch messenger, .653-inch total bundle and 153 lb/1,000 ft
  (**.227692 kg/m**, not .153 kg/m). This look
  round replaces the provisional 8.5/6.2 mm constituents with 7.6962/6.35 mm.
- [Belden outdoor loose-tube dimensional table](https://www.belden.com/products/cable/fiber-optic-cable/multi-loose-tube-fiber-cable/fs1l144ng),
  manufacturer, copyright retained: 144-fiber .621-inch / 15.8 mm
  jacket envelope. The authored aerial route is a maintained pair of black PE
  cables lashed together to 6.35 mm strand; no exact Belden product installation
  or period introduction is claimed. Two real jackets total 31.6 mm wide.
  The retained fourth copper route uses the Caledonian GR-421 100-pair .63 mm
  table's 28 mm jacket. Its 1.135 kg/m authored supported mass includes strand;
  4,256.25 N is an authored horizontal tension case, not a utility stringing chart.
- [NVIDIA GPU Gems 2, chapter 22](https://developer.nvidia.com/gpugems/gpugems2/part-iii-high-quality-rendering/chapter-22-fast-prefiltered-lines),
  Eric Chan and Frédo Durand; copyright retained: prefiltered screen-space lines.
- [Pixar RenderMan curves](https://renderman.atlassian.net/wiki/spaces/REN23/pages/19039125),
  Pixar; minimum pixel width with reduced presence. Informed the original
  .85-pixel coverage compensation, not copied shader code.
- [Godot spatial shader reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html),
  Godot contributors, CC BY 3.0: vertex view transform and alpha rendering interface.

Fictional marks: RILL TIMBER / RILL ELECTRIC / RV numbers, using installed
DejaVu Sans (Bitstream Vera/DejaVu open font license), resolved by kit/fonts.py.
Only direct image URLs identify residential photographs; no home address,
license plate, listing identifier or homeowner is recorded in tracked files.

The manufacturer's former QR860 JCA PDF URL now returns HTTP 404. It is
excluded from automatic fetching; the manufacturer's [current QR860 page](https://www.commscope.com/product-type/cables/coaxial-cables/hardline-cables/item5501302/) and [coaxial construction guide](https://www.commscope.com/globalassets/digizuite/3447-broadband-app-const-manual-ii-106549-en.pdf) supply the jacket/strand construction and bend radius.

Additional local inspection candidates (not used in the asset or final pairs):
`residential-straight.jpg`, direct image
https://upload.wikimedia.org/wikipedia/commons/0/01/Revloc_Historic_District_625_Highland.jpg
(Wikimedia Commons contributor; rights not verified here; rejected because
its road slopes and curves). `straight-in.jpg`, direct image
https://www.rxrsignals.com/Indiana/L-Q/Michigan_City/CSSM/Elston/10.JPG
(Tommy McGowan, 5 December 2015; copyright retained; straight-street/light
inspection, rejected as the replacement because its parallel double-arm
feeder is different). No pixels from either enter generated content.
