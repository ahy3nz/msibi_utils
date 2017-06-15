from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(['msibi_utils/tests/test_parse_logfile.py'])
        sys.exit(errcode)

requirements = [line.strip() for line in open('requirements.txt').readlines()]
setup(name='msibi_utils',
      version='0.1',
      description='',
      url='http://github.com/tcmoore3/msibi_utils',
      author='Timothy C. Moore',
      author_email='timothy.c.moore@vanderbilt.edu',
      license='MIT',
      packages=['msibi_utils'],
      install_requires=requirements,
      cmdclass={'test': PyTest},
      extras_require={'utils': ['pytest']},
      zip_safe=False)
