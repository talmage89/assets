"""Original two-dimensional paint fractures in the receiver's rest frame.

No reference files are read. Noise wavelengths, contact zones and statistical
coverage are authored in millimeters. These intermediate masks are baked into
the existing atlas; they are never shipped as additional textures.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image

BASE=Path(__file__).resolve().parents[1]
W,H=4096,1172
Y0,Y1=-.042,.192
Z0,Z1=.070,.137
CRESTS=(.0757,.0861,.0891,.1027,.1059)

def smooth(value,a,b):
    t=np.clip((value-a)/(b-a),0,1)
    return t*t*(3-2*t)

def field(seed,y,z,dy,dz):
    """Continuous quintic value noise, sampled in millimeters before thresholding.

    Domain warping prevents the underlying lattice from defining chip outlines.
    The fine, low-amplitude boundary layer spans about 1.6 shipping texels;
    the dominant chip layer is larger and continuous before rasterization.
    """
    u=(y-Y0)/dy+4;v=(Z1-z)/dz+4
    ix=np.floor(u).astype(np.int32);iz=np.floor(v).astype(np.int32)
    tx=u-ix;tz=v-iz
    tx=tx**3*(tx*(tx*6-15)+10);tz=tz**3*(tz*(tz*6-15)+10)
    rng=np.random.default_rng(seed)
    grid=rng.random((int(iz.max())+2,int(ix.max())+2),dtype=np.float32)
    a=grid[iz,ix]*(1-tx)+grid[iz,ix+1]*tx
    b=grid[iz+1,ix]*(1-tx)+grid[iz+1,ix+1]*tx
    return (a*(1-tz)+b*tz).astype(np.float32)

def fracture(seed,y,z):
    wy=y+(field(seed+30,y,z,.0047,.0037)-.5)*.0023
    wz=z+(field(seed+31,y,z,.0038,.0049)-.5)*.0020
    return (.65*field(seed,wy,wz,.00110,.0015)
            +.20*field(seed+1,wy,wz,.0045,.0045)
            +0.23*field(seed+2,wy,wz,.00065,.00065))

def antialias(score):
    # Integrate a crisp contour over its own pixel footprint using the local
    # gradient. This is coverage AA, not an arbitrary blurred chip boundary.
    gy,gx=np.gradient(score)
    footprint=np.maximum(np.abs(gx)+np.abs(gy),1e-5)
    return np.clip(score/footprint+.5,0,1)

def generate(side):
    """One upper contact land; sparse submillimeter nicks on lower crests.

    The well/support-hand contact is strongest forward (Y +110..145 mm).
    Aft, rubbing enters from the top crest. Coarse paint islands survive a
    multi-scale fracture threshold; fine noise only frays their margins.
    No longitudinal run statistic controls this two-dimensional field.
    """
    yy=np.linspace(Y0,Y1,W,endpoint=False,dtype=np.float32)[None,:]+(Y1-Y0)/(2*W)
    zz=np.linspace(Z1,Z0,H,endpoint=False,dtype=np.float32)[:,None]-(Z1-Z0)/(2*H)
    seed=15119+side*293
    wy=yy+(field(seed+30,yy,zz,.013,.009)-.5)*.009
    wz=zz+(field(seed+31,yy,zz,.010,.011)-.5)*.004
    wy=wy+(field(seed+32,yy,zz,.0034,.0030)-.5)*.0023
    wz=wz+(field(seed+33,yy,zz,.0028,.0037)-.5)*.0020
    islands=(0.3*field(seed,wy,wz,.017,.010)
             +0.34*field(seed+1,wy,wz,.0028,.0050)
             +0.23*field(seed+2,wy,wz,.00085,.0014)
             +0.13*field(seed+3,wy,wz,.00045,.00045))
    forward=smooth(yy,.080,.132)
    depth=(.1245-zz)/.0145
    # Distance to top/rib crests plus pressure falling away from the well.
    # High pressure crosses the percolation threshold into a connected field;
    # low pressure leaves edge-connected bites around large paint islands.
    hand=np.exp(-((yy-.095)/.045)**2)
    density=.51+.53*forward+.17*hand-.61*depth
    # Elongated fractures let low-pressure abrasion bite down from the
    # upper margin, enclosing large intact paint lobes between the bites.
    # This is another warped continuous field, not authored scratch paths.
    lace=(.65*field(seed+19,wy,wz,.0022,.0048)
          +.35*field(seed+20,wy,wz,.001,.0020))
    score=np.maximum(density-islands,.28+.20*hand-.22*depth-lace)
    # Coarse intact-paint lobes occasionally span the low-pressure land.
    # They interrupt thin gray bridges instead of leaving one continuous
    # upper ribbon; forward hand pressure still merges the rubbed field.
    separation=(.80*field(seed+41,wy,wz,.011,.018)
                +.20*field(seed+42,wy,wz,.002,.005))
    score=np.minimum(score,.75+.60*forward-separation)
    margin=field(seed+17,wy,wz,.0023,.0018)-.5
    score=np.minimum(score,(yy+.020)/.003+margin*.5)
    score=np.minimum(score,(.151-yy)/.005+margin*.6-(.3+.9*depth**2))
    score=np.minimum(score,(.1245-zz)/.001+margin*.65)
    score=np.minimum(score,(zz-.110)/.001+margin*.65)
    land=antialias(score)
    ends=np.minimum(abs(yy+.0396),abs(yy-.1896))
    pressure=np.maximum(smooth(ends,.047,.007),smooth(abs(yy-.116),.058,.018))
    layers=[]
    for i,h in enumerate(CRESTS):
        edge_seed=5119+side*293+i*61
        noise=fracture(edge_seed,yy,zz)
        center=h+(field(edge_seed+9,yy,zz,.008,.006)-.5)*.0002
        distance=np.abs(zz-center)/(.00022+pressure*.00013)
        layers.append(noise-.58+.08*pressure-.35*distance**1.25)
    nicks=antialias(np.maximum.reduce(layers))
    mask=np.maximum(land,nicks)
    sharp=np.maximum.reduce([smooth(abs(zz-h),.00055,.00025) for h in (*CRESTS,.1245)])
    eligible=mask*sharp*smooth(pressure,.3,.7)
    core=eligible*antialias(fracture(9301+side*173,yy,zz)-.70)
    result=np.stack((mask,core,np.zeros_like(mask)),axis=-1)
    return np.uint8(np.clip(result,0,1)*255),dict(seed_family=side,
        upper_land_y_mm=[-20,151],upper_land_z_mm=[110,124.5],
        coarse_island_wavelength_mm=[17,10],
        cause='Well/support-hand forward pressure; distance below upper crest aft; thin nicks only below the side rib.',
        acceptance='2-D connected regions and paint islands measured from the exported hero, never 1-D chip runs.')

def main():
    out=BASE/'build/markings';out.mkdir(parents=True,exist_ok=True);report={}
    for side,name in enumerate(('left','right')):
        array,row=generate(side);Image.fromarray(array).save(out/('receiver_wear_'+name+'.png'))
        report[name]=row
    (out/'receiver-wear-design.json').write_text(json.dumps(report,indent=2))
    print('Receiver fields: one upper contact land; thin lower crest nicks.')

if __name__=='__main__':main()
