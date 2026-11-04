"""Compare historical house GLBs without mistaking exporter labels for mesh edits."""
import hashlib,json,struct
from glb_budget import read

def provenance_normalized_hash(path):
    # Compare the complete payload after normalizing only the exporter label
    # to the fixture's version. No geometry, material or node bytes are changed.
    doc,binary=read(path);generator=doc['asset']['generator'];doc['asset']['generator']='Khronos glTF Blender I/O v5.2.40'
    j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*(-len(j)%4)
    payload=struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(binary),0x004e4942)+binary
    return hashlib.sha256(struct.pack('<III',0x46546c67,2,len(payload)+12)+payload).hexdigest(),generator

