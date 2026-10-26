"""Real 60-inch retailer photograph; original relief, no printed pattern copied."""
MATCHES={'basin':dict(photo='refs/sixty.jpg',crop=(0,100,900,800),title='60-inch molded pool / original unprinted relief / photographic comparison',location=(.6,-2.9,2.1),target=(0,0,.14),lens=60,exposure=-.35,hide_assemblies=['Water'],landmarks=[
 dict(world=(-.7438,-.1581,.3003),pixel=(10,433)),dict(world=(.7438,-.1581,.3003),pixel=(893,433)),
 dict(world=(0,-.762,.2973),pixel=(467,655)),dict(world=(0,.762,.3028),pixel=(464,154)),
 dict(world=(-.518556,-.346488,0),pixel=(156,637)),dict(world=(.518556,-.346488,0),pixel=(749,635))])}
# Front round pool from an estate sale, not a new-product catalog. Only rim
# correspondences are reliable; its exact diameter, depth and age are unknown.
MATCHES['used_estate']=dict(photo='refs/estate-used.jpg',crop=(35,395,755,930),title='Actually used estate pool / fade and deposits / original design',location=(.1,-2.3,2.9),target=(0,0,.15),lens=65,exposure=-.5,hide_assemblies=['Water'],landmarks=[
 dict(world=(-.7438,-.1581,.3003),pixel=(59,650)),dict(world=(.7438,-.1581,.3003),pixel=(731,657)),
 dict(world=(0,-.762,.2973),pixel=(404,883)),dict(world=(0,.762,.3028),pixel=(384,405))])
