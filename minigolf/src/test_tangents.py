"""Regression for the actual long-bevel export precision failure."""
import json,struct,tempfile,unittest
from pathlib import Path
import numpy as np
from tangents import repair

class BevelTangentTest(unittest.TestCase):
 def fixture(self,directory,packed=False,collapsed=False,valid=False):
  arrays=[np.array([[-3.4,0,0],[3.4,0,0],[3.4,.002,0]],'<f4'),np.tile([0,0,1],(3,1)).astype('<f4'),np.array([[0,0],[1,0],[1,1]],'<f4'),np.tile([1,0,0,1],(3,1)).astype('<f4'),np.array([0,1,2],'<u4')]
  if collapsed:arrays[2][:]=0
  if not valid:arrays[3][0,:3]=0
  binary=bytearray();views=[];accessors=[]
  for a,kind in zip(arrays,('VEC3','VEC3','VEC2','VEC4','SCALAR')):
   views.append(dict(buffer=0,byteOffset=len(binary),byteLength=a.nbytes));binary.extend(a.tobytes());accessors.append(dict(bufferView=len(views)-1,componentType=5125 if kind=='SCALAR' else 5126,count=len(a),type=kind))
  doc=dict(asset=dict(version='2.0'),buffers=[dict(byteLength=len(binary))],bufferViews=views,accessors=accessors,materials=[dict(name='Paint')],meshes=[dict(name='Acute bevel',primitives=[dict(attributes=dict(POSITION=0,NORMAL=1,TEXCOORD_0=2,TANGENT=3),indices=4,material=0)])])
  path=Path(directory)/('test.glb' if packed else 'test.gltf')
  if packed:
   j=json.dumps(doc).encode();j+=b' '*((-len(j))%4);raw=struct.pack('<4sII',b'glTF',2,28+len(j)+len(binary))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(binary),b'BIN\x00')+binary;path.write_bytes(raw)
  else:
   doc['buffers'][0]['uri']='test.bin';path.write_text(json.dumps(doc));path.with_suffix('.bin').write_bytes(binary)
  return path,views[3]['byteOffset']

 def test_acute_corner_both_containers(self):
  for packed in (False,True):
   with tempfile.TemporaryDirectory(dir='build') as directory:
    path,offset=self.fixture(directory,packed);rows=repair(path);self.assertEqual(rows[0]['repaired_vertices'],1)
    raw=path.read_bytes() if packed else path.with_suffix('.bin').read_bytes()
    if packed:offset+=28+struct.unpack_from('<I',raw,12)[0]
    np.testing.assert_allclose(np.frombuffer(raw,dtype='<f4',count=4,offset=offset),[1,0,0,1],atol=1e-7)
    self.assertEqual(repair(path),[])

 def test_collapsed_uv_rejected(self):
  with tempfile.TemporaryDirectory(dir='build') as directory:
   path,_=self.fixture(directory,collapsed=True)
   with self.assertRaises(AssertionError):repair(path)

 def test_valid_delivery_unchanged(self):
  with tempfile.TemporaryDirectory(dir='build') as directory:
   path,_=self.fixture(directory,packed=True,valid=True);before=path.read_bytes();self.assertEqual(repair(path),[]);self.assertEqual(before,path.read_bytes())

if __name__=='__main__':unittest.main()
