"""Independent raw glTF UV, shared-map and preservation audit; pure Python."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image
from surfaces import rect,NAMES,PALETTE

TYPES={5126:np.dtype('<f4'),5123:np.dtype('<u2'),5125:np.dtype('<u4'),5121:np.dtype('u1')}
WIDTHS={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}

def audit():
    report={};texture_identity={}
    for seed in (117,229,341):
        path=Path(f'export/checkpoint/Garden_{seed}.gltf');d=json.loads(path.read_text());binary=(path.parent/d['buffers'][0]['uri']).read_bytes()
        def read(i):
            a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];dt=TYPES[a['componentType']];n=WIDTHS[a['type']];offset=v.get('byteOffset',0)+a.get('byteOffset',0)
            return np.ndarray((a['count'],n),dtype=dt,buffer=binary,offset=offset,strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize)).copy()
        density={};degenerate=[];outside=0;triangles=0
        for mesh in d['meshes']:
          for p in mesh['primitives']:
            xyz=read(p['attributes']['POSITION']);uv=read(p['attributes']['TEXCOORD_0']);ids=read(p['indices']).ravel().reshape(-1,3);mat=d['materials'][p['material']]['name']
            assert np.isfinite(uv).all();triangles+=len(ids)
            a,b,c=xyz[ids[:,0]],xyz[ids[:,1]],xyz[ids[:,2]];area3=np.linalg.norm(np.cross(b-a,c-a),axis=1)*.5
            a,b,c=uv[ids[:,0]],uv[ids[:,1]],uv[ids[:,2]];area2=abs((b[:,0]-a[:,0])*(c[:,1]-a[:,1])-(b[:,1]-a[:,1])*(c[:,0]-a[:,0]))*.5
            # Real visible triangles require nonzero tangent charts. Repeated
            # swatches/cards intentionally overlap, not unique atlas islands.
            bad=(area2<1e-14)&(area3>1e-12)
            if bad.any():degenerate.append(dict(mesh=mesh['name'],material=mat,count=int(bad.sum())))
            if mat=='GardenSurfaces':
                inside=np.zeros(len(uv),bool)
                for u0,v0,u1,v1 in map(rect,[*NAMES,*PALETTE]):
                    # glTF stores V down, Blender authored V up.
                    inside|=(uv[:,0]>=u0-1e-5)&(uv[:,0]<=u1+1e-5)&(uv[:,1]>=1-v1-1e-5)&(uv[:,1]<=1-v0+1e-5)
                outside+=int((~inside).sum())
            size=2048 if mat in ('GardenSurfaces','Lawn') else 1024
            density.setdefault(mat,[]).extend((size*np.sqrt(area2[area3>1e-12]/area3[area3>1e-12])).tolist())
        images=[]
        for im in d['images']:
            p=path.parent/im['uri'];w,h=Image.open(p).size;sha=hashlib.sha256(p.read_bytes()).hexdigest()
            if im['uri'] in texture_identity:assert texture_identity[im['uri']]==sha
            texture_identity[im['uri']]=sha;images.append(dict(uri=im['uri'],size=[w,h],bytes=p.stat().st_size,sha256=sha))
        row=dict(materials=len(d['materials']),unique_mesh_triangles=triangles,images=images,texture_mib=sum(x['size'][0]*x['size'][1]*4/3 for x in images)/2**20,
            uv_degenerate=degenerate,uv_outside_reserved_swatches=outside,uv_density_px_m={k:np.quantile(v,[.05,.5,.95]).tolist() for k,v in density.items()},
            scope='raw exported charts; deliberately shared swatches/alpha cards, no unique-island overlap claim; density per unscaled mesh primitive')
        assert outside==0,(seed,'UV escaped swatch',outside)
        assert not degenerate,(seed,'Collapsed UVs',degenerate)
        assert row['materials']<=4
        report[str(seed)]=row
    old=Path('build/lookdev-before/existing-deliveries.json')
    if old.exists():
        baseline=json.loads(old.read_text());root=Path.cwd().parent;changed=[p for p,h in baseline.items() if not (root/p).exists() or hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
        assert not changed,('Existing delivery changed',changed)
        report['preserved_delivery_files']=len(baseline)
    plant=np.asarray(Image.open('textures/checkpoint/T_GardenPlants_BaseColor.png'))
    net=plant[:plant.shape[0]//4,:plant.shape[1]//4,3]
    retained=float((net>.45*255).mean());assert .01<retained<.7,('Bird net disappeared or became solid',retained)
    report['net_retained_alpha_fraction']=retained
    report['passed']=True;Path('build/look-audit.json').write_text(json.dumps(report,indent=2));print('LOOK AUDIT PASSED')

if __name__=='__main__':audit()
