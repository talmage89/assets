"""Asset policy shared by modeling, graphics, studio and verification; meters."""
ASSET_SET='Grill'
HINGE=(0,.294,.912)
WHEEL_CENTERS=(-.290,.290)
KNOB_RANGE=(-140,0)
KNOB_GRAPHICS={'off':0,'high':-25,'low':-140,'tick_step':15}
RIG_POSE={'angles':[55,28,0,-28,-55,-70],'lateral':-.08,'twist_step':24,'initial_z':(0,-1,0)}
COMBUSTION_GEOMETRY={
 'burner_x':(-.205,0,.205),'lane_width':.020,'lane_softness':.035,
 'hood_spread_min':.060,'hood_spread_growth':.075,'hood_spread_height':(0,.22),'hood_thermal_height':(-.01,.09),'hood_oil':(.015,.014,.018),
 'bowl_under_height':(.80,.73),'drain_center':(0,-.024),'drain_radii':(.12,.15),'drain_height':(.76,.70),
 'bowl_drips':[(-.19,.887,.009,.19),(.07,.887,.006,.19),(.24,.887,.004,.19)],
 'channel_apex':(.841,.0015,.006),'channel_streak_y':(-.125,-.045,.062,.157),'channel_oil_height':(.808,.819),
}
BURNER_GEOMETRY={'burner_z':.770,'port_z':.772,'pitch':.0118,'start':-.209,'end':.218,'port_radius':.00075,'soot_radius':.0018,'thermal_offset':.003,'thermal_width':.006,'thermal_softness':.004}
