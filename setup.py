# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Setup for libfulltext"""

# Use setuptools for these commands (they don't work well or at all
# with distutils).  For normal builds use distutils.
try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup

    def find_packages(*args, **kwargs):
        return ['libfulltext.doi']


setup(name='libfulltext',
      packages=find_packages(),
      version='1.0.0-alpha.1',
      description='Tools for downloading fulltexts of open access articles',
      url='https://github.com/andrenarchy/libfulltext',
      install_requires=['PyYAML (>=3)', 'requests (>=2)', "click (>=5)"],
      scripts=['bin/get_fulltext.py'],
      classifiers=[],
      )
