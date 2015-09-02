from setuptools import setup


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
      zip_safe=False)
