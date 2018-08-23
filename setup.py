#!/usr/bin/env python

from setuptools import setup
from plenoptisign import __version__

setup(name='plenoptisign',
      version=__version__,
      description='Light field geometry estimator for a Standard Plenoptic Camera (SPC)',
      url='http://github.com/hahnec/plenoptisign',
      author='Christopher Hahne',
      author_email='inbox@christopherhahne.de',
      license='GNU GPL V3.0',
      scripts=['plenoptisign/bin/cmd_script.py'],
      entry_points = {
          'console_scripts': ['plenoptisign=plenoptisign.bin.cmd_script:main'],
      },
      packages=['plenoptisign'],
      install_requires=['numpy', 'matplotlib', 'ddt', 'datetime'],
      include_package_data=True,
      zip_safe=False)