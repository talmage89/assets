"""Override a Blender launch's thread count without changing script arguments."""
import argparse
import os
import sys


def with_threads(command, count):
    """Return a new argv; retain wrappers and everything after Blender's ``--``.

    The executable may be Blender itself or a wrapper such as with_gpu.sh.
    Callers opt in per build, so unrelated generators retain their own policy.
    """
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise ValueError('Thread count must be a positive integer')
    command = list(map(os.fspath, command))
    if not command:
        raise ValueError('Missing Blender command')
    result = [command[0]]
    index = 1
    while index < len(command):
        arg = command[index]
        if arg == '--':
            break
        if arg in ('-t', '--threads'):
            if index + 1 == len(command) or command[index + 1] == '--':
                raise ValueError('Missing thread count')
            index += 2
        else:
            result.append(arg)
            index += 1
    return result + ['-t', str(count)] + command[index:]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--threads', type=int, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command
    if command[:1] == ['--']:
        command = command[1:]
    command = with_threads(command, args.threads)
    os.execvp(command[0], command)


if __name__ == '__main__':
    main()
