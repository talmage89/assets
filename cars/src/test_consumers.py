"""Car launches use one thread; cache reuse and other generators stay scoped."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


class ConsumerThreads(unittest.TestCase):
    def setUp(self):
        (ROOT/'build/tmp').mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'build/tmp')
        self.addCleanup(self.temp.cleanup);self.folder=Path(self.temp.name)

    def test_school_replaces_old_cache_then_reuses_one_thread_cache(self):
        deps=load('school_deps','school/src/dependencies.py')
        target=self.folder/'car.blend';target.write_bytes(b'old')
        def run(command,**kwargs):
            self.assertEqual(command[command.index('-t')+1],'1')
            target.write_bytes(b'new')
        with patch.object(deps.subprocess,'run',side_effect=run) as launch:
            deps.car_cache('hatchback',target,self.folder/'car.log')
            deps.car_cache('hatchback',target,self.folder/'car.log')
        self.assertEqual(launch.call_count,1)
        self.assertEqual(target.with_suffix('.threads').read_text(),'1\n')

    def test_downtown_changes_only_car_launches_and_invalidates_recipe(self):
        context=load('town_context','downtown/src/context.py')
        context.CASES=(context.CASES[0],context.CASES[3]);commands=[]
        def run(command,**kwargs):
            commands.append(command)
            Path(command[command.index('--out')+1]).write_bytes(b'new')
        previous=Path.cwd();os.chdir(self.folder)
        try:
            with patch.object(context.subprocess,'run',side_effect=run):
                context.ensure();context.ensure()
        finally:os.chdir(previous)
        self.assertEqual(len(commands),2)
        self.assertEqual(commands[0][commands[0].index('-t')+1],'1')
        self.assertNotIn('-t',commands[1])

    def test_utility_keeps_other_builds_at_four_threads(self):
        context=load('utility_context','utility/src/context.py')
        for source,count in [('cars/src/build.py','1'),('trees/src/build.py','4')]:
            command=context.build_command(source,ROOT/source,['--quality','game'])
            self.assertEqual(command[command.index('-t')+1],count)
            self.assertEqual(command[command.index('--')+1:],['--quality','game'])

    def test_garage_rebuilds_old_cache_and_retains_guard(self):
        deps=load('garage_deps','parking-garage/src/dependencies.py');commands=[]
        (self.folder/'hatchback.glb').write_bytes(b'old')
        def run(command,**kwargs):
            commands.append(command);output=Path(command[command.index('--out')+1])
            if 'src/context_guard.py' in command:
                output.write_text(json.dumps(dict(passed=True,actual_sha256='fixture')))
            else:
                self.assertEqual(command[command.index('-t')+1],'1');output.write_bytes(b'new')
            return subprocess.CompletedProcess(command,0)
        with patch.object(deps.subprocess,'run',side_effect=run):
            deps.build_context('hatchback',self.folder)
            deps.build_context('hatchback',self.folder)
        self.assertEqual(len(commands),3)
        self.assertEqual(commands[-1][commands[-1].index('-t')+1],'2')

    def test_apartment_make_changes_only_car_rule(self):
        def dry(target):
            return subprocess.check_output(['make','-C',str(ROOT/'apartments'),'-n',
                '-W','src/context_build.py',target],text=True)
        self.assertIn('blender_command.py --threads 1 --',dry('build/context/car/source.blend'))
        tree=dry('build/context/tree/source.blend')
        self.assertNotIn('blender_command.py --threads',tree)
        self.assertIn('-t 4',tree)


if __name__=='__main__':unittest.main()
