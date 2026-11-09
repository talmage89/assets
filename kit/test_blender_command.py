"""Thread overrides must leave wrappers, other flags and script argv intact."""
from pathlib import Path
import unittest
from unittest.mock import patch
from kit.blender_command import main, with_threads


class BlenderCommandTests(unittest.TestCase):
    def test_override_before_script_arguments(self):
        command = ['blender', '-t', '4', '-b', '--threads', '8',
                   '--python', 'build.py', '--', '--threads', '12', '-t', '3']
        self.assertEqual(with_threads(command, 1),
                         ['blender', '-b', '--python', 'build.py', '-t', '1',
                          '--', '--threads', '12', '-t', '3'])
        self.assertEqual(command[2], '4')

    def test_wrapped_launch_and_paths(self):
        self.assertEqual(with_threads([Path('with_gpu.sh'), 'blender', '-b'], 1),
                         ['with_gpu.sh', 'blender', '-b', '-t', '1'])

    def test_cli_executes_without_a_shell(self):
        with patch('kit.blender_command.os.execvp') as execute:
            main(['--threads', '1', '--', 'blender', '-b', '-t', '4', '--', 'a b'])
        execute.assert_called_once_with('blender', ['blender', '-b', '-t', '1', '--', 'a b'])

    def test_invalid_launch(self):
        for command, count in [([], 1), (['blender'], 0), (['blender'], True),
                               (['blender', '-t'], 1), (['blender', '-t', '--'], 1)]:
            with self.subTest(command=command, count=count), self.assertRaises(ValueError):
                with_threads(command, count)


if __name__ == '__main__':
    unittest.main()
