"""Compare unaffected visual geometry and control channels with a local baseline.

Optional review proof, not a dependency on another checkout or accepted binary.
"""
import argparse,json,sys
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit import weapon as W

def capture(path):
    bpy.ops.wm.open_mainfile(filepath=str(Path(path).resolve()));arm=bpy.data.objects['B24Armature'];W.pose(arm,None,0)
    meshes={o.name:(np.array([v.co[:] for v in o.data.vertices]),[tuple(f.vertices) for f in o.data.polygons])
            for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o}
    controls={}
    for track in arm.animation_data.nla_tracks:
        act=track.strips[0].action
        for tick in range(int(act.frame_range[1])*2+1):
            f=tick*.5;W.pose(arm,track.name,f)
            controls[(track.name,f)]={b.name:np.array(b.matrix_basis) for b in arm.pose.bones}
    return meshes,controls

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);old,old_controls=capture(a.before);new,new_controls=capture(a.after)
    changed_prefixes=('Magazine_','ChamberRound_','CycleCase_','Bolt_Extractor','Bolt_Ejector')
    changed={'Stock_Mold','Receiver','Barrel','Bolt_Body','Bolt_Lug','Bolt_Lug.001','Bottom_Metal','Action_Screw.001','Feed_Ramp'}
    preserved=[]
    for name,(positions,faces) in old.items():
        if name in changed or name.startswith(changed_prefixes):continue
        assert name in new and np.array_equal(positions,new[name][0]) and faces==new[name][1],name
        preserved.append(name)
    count=0;maximum=0.
    for (clip,f),bones in old_controls.items():
        for name,m in bones.items():
            if clip in ('Fire','FireLast','ReloadEmpty') and name in ('TopRound','ReserveRound','Follower','ChamberRound'):continue
            error=float(abs(m-new_controls[(clip,f)][name]).max());maximum=max(maximum,error)
            assert error<1e-7,(clip,f,name,error);count+=1
    report=dict(passed=True,unchanged_meshes=preserved,unchanged_mesh_count=len(preserved),
                unchanged_control_pose_comparisons=count,maximum_basis_delta=maximum,
                scope='source positions/topology and local control channels; changed parts explicitly excluded')
    Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print('PRESERVATION',len(preserved),'meshes;',count,'control poses;',maximum)
