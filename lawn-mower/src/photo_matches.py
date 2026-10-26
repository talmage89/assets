"""Measured photographic landmarks. Only camera fitting; no traced geometry."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=-.41655
def a(p,pix):return dict(world=(p[0]-.0044,p[1]+D,p[2]),pixel=pix)
MATCHES={
'match_product':dict(title='21 inch class / construction and proportions',photo=str(R/'refs/product0.jpg'),crop=(20,10,730,720),location=(-1.8,-2.6,1.7),target=(0,0,.5),lens=65,background='transparent',landmarks=[
a((-.269,-.270,.0889),(418,619)),a((.269,-.270,.0889),(664,566)),a((-.269,.260,.1016),(265,531)),
a((-.239,1.160,1.008),(68,66)),a((.239,1.160,1.008),(236,50)),
a((0,-.052,.460),(431,401)),a((-.198,.825,.647),(175,255)),a((.198,.825,.647),(317,246))]),
# Used in-service fabric-bag mower. Different rear wheel size and styling;
# fit the two visible wheel axes, engine and grip, and retain measured residuals.
'match_used':dict(title='In-service mower / fabric and cause-driven wear',photo=str(R/'refs/used.jpg'),crop=(0,250,3200,2200),location=(1.5,-1,1.8),target=(0,0,.5),lens=50,background='transparent',studio_yaw=90,landmarks=[
a((.269,-.270,.0889),(298,1649)),a((.269,.260,.1016),(1144,1896)),a((0,-.052,.460),(859,1206)),a((.216,1.176,1.023),(2997,850)),a((-.216,1.176,1.023),(2953,547))])}

# Current owner correction requests one used-mower comparison only.
MATCHES={'match_used':MATCHES['match_used']}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--credit-dir',required=True);d=Path(p.parse_args().credit_dir);d.mkdir(parents=True,exist_ok=True)
    (d/'REFERENCE-CREDIT.txt').write_text(
        'Right-hand photographic panels are reference images only.\n'
        'TB120B product photograph: Troy-Bilt, copyright reserved, local comparison.\n'
        'https://www.troybilt.com/en_US/push-mowers/tb120b-push-lawn-mower/11A-A2T2066.html\n'
        'Used mower: Famartin, 27 May 2015, CC BY-SA 4.0.\n'
        'https://commons.wikimedia.org/wiki/File:2015-05-27_12_41_21_A_lawn_mower_on_Tranquility_Court_in_the_Franklin_Farm_section_of_Oak_Hill,_Fairfax_County,_Virginia.jpg\n'
        'https://creativecommons.org/licenses/by-sa/4.0/\n'
        'Changes: crop, resize and comparison captions. Used-photo composite is CC BY-SA 4.0.\n'
        'No reference pixels are present in the 3D model, textures or final docs.\n')
