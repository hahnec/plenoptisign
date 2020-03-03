#!/usr/bin/env python

from setuptools import setup, find_packages
from plenoptisign import __version__
from sys import platform
from docutils import core

APP = ['plenoptisign/gui/gui_app.py']
DATA_FILES = [
        # ('subdir' , ['file_path'])
        ('misc', ['plenoptisign/gui/misc/circlecompass_1055093.ico'])
]

OPTIONS = {
    "argv_emulation": True,
    "compressed": True,
    "optimize": 2,
    "iconfile": 'plenoptisign/gui/misc/circlecompass_1055093.icns',
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
     data_files=DATA_FILES,
 )
else:
 extra_options = dict(
     # Normally unix-like platforms will use "setup.py install"
     # and install the main script as such
     setup_requires=[],
 )

# parse description section text
with open("README.rst", "r") as f:
 data = f.read()
 readme_nodes = list(core.publish_doctree(data))
 for node in readme_nodes:
     if node.astext().startswith('Description'):
         long_description = node.astext().rsplit('\n\n')[1]

setup(
      name='plenoptisign',
      version=__version__,
      description='Light field geometry estimator for a Standard Plenoptic Camera (SPC)',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='http://github.com/hahnec/plenoptisign',
      author='Christopher Hahne',
      copyright='Christopher Hahne',
      author_email='inbox@christopherhahne.de',
      license='GNU GPL V3.0',
      keywords='plenoptic camera optics design software',
      scripts=['plenoptisign/bin/cli_script.py'],
      entry_points={'console_scripts': ['plenoptisign=plenoptisign.bin.cli_script:main'],},
      packages=find_packages(),
      install_requires=['numpy', 'matplotlib', 'ddt', 'nose'],
      include_package_data=True,
      zip_safe=False,
      **extra_options
      )
