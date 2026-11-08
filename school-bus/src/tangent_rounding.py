"""Three asset-owned MikkTSpace boundaries, with exact surface signatures.

The exporter rounds tangents to four decimals. These corners straddled one
rounding step in independent builds with identical positions, normals and UVs.
The kit rejects any changed signature or drift above a single rounding step.
"""
ANCHORS=[dict(mesh=7,primitive=1,vertices={101:72086,102:72078,103:72078},
    position=[.5205061435699463,1.9980708360671997,3.3194446563720703],
    normal=[.3096006214618683,-.8870018124580383,-.34260067343711853],
    uv=[.9352506399154663,.6424344778060913],
    tangent=[-.9445000290870667,-.24539999663829803,-.21819999814033508,1.]),
 dict(mesh=7,primitive=0,vertices={101:5048,102:5032,103:5032},
    position=[-.5400000214576721,1.8409167528152466,4.265833854675293],
    normal=[-.06869783997535706,.978969156742096,.19209395349025726],
    uv=[.6279965043067932,.7148125171661377],
    tangent=[-.9976000189781189,-.06750000268220901,-.013000000268220901,1.]),
 dict(mesh=7,primitive=0,vertices={101:5715,102:5699,103:5699},
    position=[-.41750001907348633,1.8829878568649292,4.051167011260986],
    normal=[-.01729963719844818,.9877792596817017,.15489675104618073],
    uv=[.621228039264679,.726926863193512],
    tangent=[-.9998000264167786,-.01679999940097332,-.004000000189989805,1.])]

def for_seed(seed):
    # Variant lettering changes deduplication before this same physical corner.
    return [{**{k:v for k,v in a.items() if k!='vertices'},'vertex':a['vertices'][seed]} for a in ANCHORS]
