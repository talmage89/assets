"""Source-controlled lens/countdown membership in additional shared-map levels."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from kit.lod import configuration
from kit.lod_io import Document,digest

def run(config):
    cfg,family,source,out=configuration(config)
    manifest=json.loads((out/'manifest.json').read_text())
    base=Document(source)
    fields=('signal_lens','signal_kind','powered','flashing_yellow_arrow','digit','segment')
    wanted={n['name']:(i,n) for i,n in enumerate(base.data['nodes']) if 'mesh' in n and
            (n.get('extras',{}).get('signal_lens') or n.get('extras',{}).get('signal_kind')=='countdown')}
    def materials(doc,node):
        return sorted(doc.data['materials'][p.get('material',0)]['name']
                      for p in doc.data['meshes'][node['mesh']]['primitives'])
    levels=[]
    for row in manifest['levels'][1:]:
        doc=Document(out/row['path']);nodes={n['name']:(i,n) for i,n in enumerate(doc.data['nodes'])}
        checks=[]
        for name,(si,original) in wanted.items():
            assert name in nodes,(name,'missing state node')
            ni,node=nodes[name]
            assert 'mesh' in node,(name,'state node lost its geometry')
            expected={k:original.get('extras',{}).get(k) for k in fields}
            actual={k:node.get('extras',{}).get(k) for k in fields}
            assert expected==actual,(name,'state flags changed')
            before,after=materials(base,original),materials(doc,node)
            assert before==after,(name,'lit/off material routing changed')
            error=float(np.max(np.abs(base.world(si)-doc.world(ni))))
            assert error<=2e-5,(name,'state frame changed',error)
            checks.append(dict(node=name,state=actual,materials=after,max_world_matrix_error=error))
        levels.append(dict(level=row['level'],state_nodes=len(checks),checks=checks))
    report=dict(passed=True,source_sha256=digest(source),manifest_sha256=digest(out/'manifest.json'),
        levels=levels,scope='Named exported state geometry, current material membership and canonical frames; not phase timing or flexible cable simulation')
    (family/'build'/('lod-'+cfg.get('readme_key','default')+'-state.json')).write_text(json.dumps(report,indent=2)+'\n')
    print('LOD STATE ROUTING',[(r['level'],r['state_nodes']) for r in levels])

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',required=True)
    args=parser.parse_args()
    run(Path(args.config))
