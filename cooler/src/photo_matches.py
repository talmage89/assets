"""Manufacturer outdoor photograph: original shape/palette, measured-scale framing."""
MATCHES={'outdoor':dict(photo='refs/outdoor.jpg',crop=(285,90,765,455),title='Outdoor rotomolded cooler / original C48 / photographic comparison',location=(-.4,-2,.85),target=(0,0,.20),lens=65,exposure=-.45,
landmarks=[
 dict(world=(-.315,-.2095,.399),pixel=(316,216)),dict(world=(.315,-.2095,.399),pixel=(700,137)),
 dict(world=(-.285,-.18,.032),pixel=(369,429)),dict(world=(.285,-.18,.032),pixel=(743,350)),
 dict(world=(-.285,-.2095,.4191),pixel=(333,192)),dict(world=(.285,-.2095,.4191),pixel=(685,116))])}

# Actual used seller photograph, unknown age; original shape and palette retained.
MATCHES['used_full']=dict(photo='refs/used-full.jpg',crop=(120,340,755,835),
 title='Actually used rotomolded cooler / corner abrasion / original C48',
 location=(-1,-1.6,1),target=(0,0,.20),lens=65,exposure=-.25,
 landmarks=[
  dict(world=(-.3184,.1914,.4191),pixel=(170,423)),
  dict(world=(.3184,.1914,.4191),pixel=(520,375)),
  dict(world=(.3184,-.1914,.4191),pixel=(693,406)),
  dict(world=(-.3184,-.1914,.4191),pixel=(292,482)),
  dict(world=(-.285,-.159,.020),pixel=(315,795)),
  dict(world=(.285,-.159,.020),pixel=(672,665))])
