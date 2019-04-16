#!/usr/bin/env python

from setuptools import setup, find_packages
from plenoptisign import __version__
from sys import platform

APP = ['plenoptisign/gui/gui_app.py']
DATA_FILES = [
        # ('subdir' , ['file_path'])
        ('cfg', ['plenoptisign/gui/cfg/cfg.json']),
        ('misc', ['plenoptisign/gui/misc/circlecompass_1055093.ico']),
        ('docs/build/html', ['docs/build/html/'])   # this comes last to exclude it for pyinstaller crashes
]

OPTIONS = {
    "argv_emulation": True,
    "compressed": True,
    "optimize": 2,
    "iconfile":'plenoptisign/gui/misc/circlecompass_1055093.icns',
    "excludes": ['pillow', 'Image'],
    "plist": dict(NSHumanReadableCopyright='2019 Christopher Hahne')
}

if platform == 'darwin':
 extra_options = dict(
     setup_requires=['py2app'],
     app=APP,
     data_files=DATA_FILES,
     # Cross-platform applications generally expect sys.argv to be used for opening files.
     options=dict(py2app=OPTIONS),
 )
elif platform == 'win32':
 extra_options = dict(
     setup_requires=[],
     app=[],
     data_files=DATA_FILES[:2],
 )
else:
 extra_options = dict(
     # Normally unix-like platforms will use "setup.py install"
     # and install the main script as such
     setup_requires=[],
     scripts=APP,
 )

setup(
      name='plenoptisign',
      version=__version__,
      description='Light field geometry estimator for a Standard Plenoptic Camera (SPC)',
      url='http://github.com/hahnec/plenoptisign',
      author='Christopher Hahne',
      copyright='Christopher Hahne',
      author_email='inbox@christopherhahne.de',
      license='GNU GPL V3.0',
      scripts=['plenoptisign/bin/cli_script.py'],
      entry_points={'console_scripts': ['plenoptisign=plenoptisign.bin.cli_script:main'],},
      packages=find_packages(),
      install_requires=['numpy', 'matplotlib'],
      include_package_data=True,
      zip_safe=False,
      **extra_options
      )