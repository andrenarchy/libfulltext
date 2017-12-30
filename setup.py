"""Setup for libfulltext"""

# Use setuptools for these commands (they don't work well or at all
# with distutils).  For normal builds use distutils.
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='libfulltext',
      packages=['libfulltext'],
      version='1.0.0-alpha.1',
      description='Tools for downloading fulltexts of open access articles',
      url='https://github.com/andrenarchy/libfulltext',
      install_requires=['PyYAML (>=3)', 'requests (>=2)', "click (=>5)"],
      classifiers=[],
 )
