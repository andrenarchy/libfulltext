# -*- coding: utf-8 -*-
import os
import codecs

# Use setuptools for these commands (they don't work well or at all
# with distutils).  For normal builds use distutils.
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# shamelessly copied from VoroPy
def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
            ).read()
    except Exception:
        content = ''
    return content


setup(name='libfulltext',
      packages=['libfulltext'],
      version='1.0.0-alpha.1',
      description='Tools for downloading fulltexts of open access articles',
      url='https://github.com/andrenarchy/libfulltext',
      install_requires=['requests (>=2)'],
      classifiers=[],
      )
