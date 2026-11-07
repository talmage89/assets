"""Fresh source / bytecode processes share reduction caches; edits invalidate them."""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class LODCacheTests(unittest.TestCase):
    def test_source_pyc_and_implementation_change(self):
        (ROOT/'build').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='lod-cache-test-',dir=ROOT/'build') as temp:
            folder=Path(temp);modules=folder/'source';modules.mkdir()
            for name in ('lod_shared.py','lod_mesh.py','lod_constraints.py'):
                shutil.copyfile(ROOT/'kit'/name,modules/name)
            script=folder/'probe.py'
            script.write_text('''import sys,importlib.util,json,hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0,sys.argv[sys.argv.index('--')+1])
folder=Path(__file__).parent;source=folder/'source/lod_shared.py'
spec=importlib.util.spec_from_file_location('cache_fixture',source)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
x,y=np.meshgrid(np.arange(6),np.arange(6));p=np.column_stack([x.ravel(),y.ravel(),np.zeros(36)]).astype(np.float32)
a=dict(POSITION=p,NORMAL=np.tile([0,0,1.],(36,1)).astype(np.float32),TEXCOORD_0=p[:,:2]/5)
f=[]
for j in range(5):
 for i in range(5):
  k=j*6+i;f.extend([[k,k+1,k+7],[k,k+7,k+6]])
out,tri,row=m.reduce(a,np.array(f,np.uint32),.4,.05,dict(TEXCOORD_0=.001))
h=hashlib.sha256()
for k,v in sorted({**out,'indices':tri}.items()):h.update(k.encode());h.update(v.tobytes())
files=sorted(str(p.relative_to(folder)) for p in (folder/'build/lod-shared-cache').rglob('*.npz'))
(folder/'result.json').write_text(json.dumps(dict(files=files,arrays=h.hexdigest(),triangles=len(tri))))
''')
            def run(label):
                command=['blender','-b','--factory-startup','--threads','2','--python-exit-code','1','--python',str(script),'--',str(ROOT)]
                with (folder/(label+'.log')).open('w') as log:
                    result=subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,
                                          env={**os.environ,'TMPDIR':str(folder)})
                self.assertEqual(result.returncode,0,(folder/(label+'.log')).read_text())
                return json.loads((folder/'result.json').read_text())
            first=run('source')
            self.assertTrue(list((modules/'__pycache__').glob('lod_shared*.pyc')))
            second=run('bytecode')
            self.assertLess(first['triangles'],50)
            self.assertEqual(first,second,'Bytecode reload missed the existing content cache')
            source=modules/'lod_shared.py';source.write_text(source.read_text()+'\n# Changed implementation receipt.\n')
            third=run('changed')
            self.assertEqual(first['arrays'],third['arrays'])
            self.assertGreater(len(third['files']),len(first['files']),'Changed source incorrectly reused the old implementation cache')


if __name__=='__main__':unittest.main()
