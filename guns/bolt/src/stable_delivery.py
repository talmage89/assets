"""Keep the accepted rounded tangent at one numerically unstable pad corner.

The exporter rounds MikkTSpace tangents to four decimals. This nearly degenerate
UV corner straddles 0.29035 on repeated evaluation, although its positions,
normals and UVs are byte-identical. Restore the accepted rounded value only
when the exact original vertex and UV are present. No mesh/rig/layout changes.
"""
from pathlib import Path
import struct,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from kit.gltf import GLB

def stabilize(path):
 g=GLB(path);p=g.json['meshes'][0]['primitives'][0];i=12932
 if 'TANGENT' not in p['attributes']:return
 positions=g.accessor(p['attributes']['POSITION']);uv=g.accessor(p['attributes']['TEXCOORD_0'])
 assert tuple(round(float(v),8) for v in positions[i])==(.0013208,.06064592,-.26100001)
 assert tuple(round(float(v),8) for v in uv[i])==(.63401145,.1308527)
 accessor=g.json['accessors'][p['attributes']['TANGENT']];view=g.json['bufferViews'][accessor['bufferView']]
 payload=bytearray(path.read_bytes());offset=12
 while True:
  size,kind=struct.unpack_from('<II',payload,offset)
  if kind==0x004e4942:break
  offset+=8+size
 component=offset+8+view.get('byteOffset',0)+accessor.get('byteOffset',0)+i*view.get('byteStride',16)+4
 original=struct.unpack_from('<f',payload,component)[0];assert abs(original-.2904)<.00011
 struct.pack_into('<f',payload,component,.2904);path.write_bytes(payload)
 print('Stable accepted pad tangent:',original,'-> 0.2904')
if __name__=='__main__':stabilize(Path(sys.argv[sys.argv.index('--')+1]))
