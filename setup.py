import subprocess
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex

        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


def git_version():
    try:
        version = subprocess.check_output(
            'git describe --dirty --always'.split()
        ).replace('-dirty', '.dev0').strip().decode()
    except subprocess.CalledProcessError:
        version = '0.0.0'

    return version


if __name__ == '__main__':
    setup(
        name='cinderblock',
        version=git_version(),
        description='Continous Integration with multiple github projects on CircleCI!',
        url='https://github.com/paperg/cinderblock',
        packages=['cinderblock'],
        entry_points={
            'console_scripts': [
                'cinderblock = cinderblock.integrate:main',
                'commitstatus = cinderblock.commitstatus:main',
            ]
        },
        install_requires=[
            'circleclient',
            'requests'
        ]
    )