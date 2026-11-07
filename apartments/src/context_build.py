"""Build repository-owned context into apartments/build only.

No canonical export, texture or source is modified. Each invocation is a fresh
Blender process so family-local module names cannot leak between generators.
"""
import argparse
import runpy
import importlib.util
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
p=argparse.ArgumentParser();p.add_argument('kind',choices=('car','tree','shrub','fence','ground'));args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
folder=Path('build/context')/args.kind;folder.mkdir(parents=True,exist_ok=True)
case={'car':'cars','tree':'trees','shrub':'shrubs','fence':'fences','ground':'ground'}[args.kind]
sys.path.insert(0,str(ROOT/case/'src'))
if args.kind=='shrub':
    from atlas import generate
    generate(folder/'shrubs/textures/analytic',1024)
    spec=importlib.util.spec_from_file_location('_apartments_context_source',ROOT/case/'src/build.py');module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module);ns=module.__dict__
    ns['main'].__globals__['ROOT']=folder.resolve()
    sys.argv=['build.py','--','--quality','game','--out',str(folder/'source.blend')];ns['main']()
elif args.kind=='ground':
    # Quick diagnostic maps stand in for the accepted ground tiles, whose
    # dimensions/geometry are still used unchanged from the original generator.
    from PIL import Image
    for name,c in (('Asphalt',(48,49,47)),('Concrete',(145,142,131)),('Lawn',(62,86,36)),('GroundTrim',(130,128,115))):
        for channel,col in (('BaseColor',c),('Normal',(128,128,255)),('ORM',(255,220,0))):Image.new('RGB',(8,8),col).save(folder/f'T_{name}_{channel}.png')
    spec=importlib.util.spec_from_file_location('_apartments_context_source',ROOT/case/'src/build.py');module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module);ns=module.__dict__
    sys.argv=['build.py','--','--textures',str(folder),'--out',str(folder/'source.glb')];ns['main']()
else:
    spec=importlib.util.spec_from_file_location('_apartments_context_source',ROOT/case/'src/build.py');module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module);ns=module.__dict__
    argv=['build.py','--','--quality','game','--out',str(folder/'source.blend')]
    if args.kind=='car':
        # Retained form path predates later material keys. Local diagnostic
        # aliases preserve the original generator's vertices without look-dev.
        from collections import defaultdict
        original=ns['Build'].__init__
        def quick_init(self,*a,**kw):
            original(self,*a,**kw);self.m=defaultdict(lambda:self.m['bumper'],self.m)
            for k in ('plastic','interior','frame','rear_glass'):self.m[k]=self.m['rubber']
            self.m['chrome']=self.m['wheel']
        ns['Build'].__init__=quick_init;argv+=['--form-only']
    sys.argv=argv;ns['main']()
