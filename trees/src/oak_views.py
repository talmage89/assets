"""Pin oak structure review cameras; full views at 1.7 m eye height."""
SHOTS={
 'daylight':dict(location=(20,-33,1.7),target=(0,0,8.2),lens=51,aspect=1),
 'crown_up':dict(location=(2.1,2.8,1.7),target=(-1,-1,9.0),lens=21,aspect=1),
 'silhouette':dict(location=(-20,-33,1.7),target=(0,0,8.2),lens=51,aspect=1,silhouette=True),
 'scale':dict(location=(20,-33,1.7),target=(0,0,8.2),lens=51,aspect=1,human=True),
 'structure':dict(location=(20,-33,1.7),target=(0,0,8.2),lens=51,aspect=1,hide_leaves=True),
 'lower_pins':dict(location=(2.4,-3.6,1.7),target=(0,0,3.2),lens=38,aspect=1,hide_leaves=True),
 'bark':dict(location=(-1.1,-1.65,1.7),target=(0,0,1.35),lens=44,aspect=1.2),
 'family':dict(location=(16,-44,1.7),target=(0,0,8.0),lens=45,aspect=1.6,family=True,human=True),
}

SHOTS.update(
 hero=dict(location=(16,-27,1.7),target=(0,0,8.1),lens=60,aspect=1),
 front=dict(location=(0,-38,1.7),target=(0,0,8.2),lens=51,aspect=1),
 side=dict(location=(38,0,1.7),target=(0,0,8.2),lens=51,aspect=1),
 back=dict(location=(0,38,1.7),target=(0,0,8.2),lens=51,aspect=1),
 top=dict(location=(0,0,33),target=(0,0,8),lens=50,aspect=1),
 branchlet=dict(location=(3.3,-4.6,3.3),target=(2.9,-3.7,3.9),lens=48,aspect=1.2,leaf_cluster=True),
 root_flare=dict(location=(1.2,-1.8,.65),target=(0,0,.27),lens=44,aspect=1.2),
)

SHOTS['cluster_3m']=dict(SHOTS['branchlet'],cluster_distance_m=3.0)
SHOTS['bark_raking']=dict(location=(-.67,-1.0,1.59),target=(0,0,1.35),lens=38,aspect=1.2,lighting=dict(sun_elevation=22,sun_azimuth=140,sun_energy=7,sky_strength=.22,exposure=.5))
