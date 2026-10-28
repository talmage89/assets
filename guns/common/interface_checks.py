"""Guns Interface 1.0.0 manifest and scene-frame checks, independent of gun form."""
STATIC_SOCKETS=('Socket_Muzzle','Socket_Foregrip','Socket_Butt','Socket_Eye','Socket_Ejection','Socket_MagWell')

def manifest(binding):
 assert binding.VERSION=='1.0.0' and binding.FPS==60
 assert {'Idle','Fire','FireLast'}<=set(binding.CLIPS)
 for name,spec in binding.CLIPS.items():
  assert spec['start'] in binding.STATES and spec['end'] in binding.STATES,name
  assert spec['frames']>0 and isinstance(spec['required'],bool),name
  assert all(0<=v<=spec['frames'] for v in spec['events'].values()),name
 return dict(version=binding.VERSION,clips=len(binding.CLIPS))

def scene_frame(arm,clip,frame):
 import bpy
 root=arm.pose.bones['Root'];delta=root.matrix@root.bone.matrix_local.inverted()
 assert max(abs(delta[i][j]-(1 if i==j else 0)) for i in range(4) for j in range(4))<2e-6
 for name in STATIC_SOCKETS:
  assert bpy.data.objects[name].matrix_world.to_quaternion().angle<2e-6,(clip,frame,name)
