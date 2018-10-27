===============
Plenoptisign
===============

Light field geometry estimator for a Standard Plenoptic Camera (SPC).

With this python module, a pair of lightfield rays is treated as a system of linear functions whose solution yields ray intersections indicating distances to refocused object planes or virtual camera positions that project perspective views captured by an SPC.

Usage instructions
===================

Use the package from the command line tool by

* downlading the source using ``$ git clone https://github.com/hahnec/plenoptisign.git``

* installing with ``$ sudo python setup.py install``

* running the program ``$ plenoptisign``

* unit testing (optional) ``$ python plenoptisign/tests/plenoptisign_unittest.py -v``

Further information
===================

* visit `plenoptic.info <http://www.plenoptic.info>`__ for technical details, animated figures and theoretical background

* Demo: http://www.plenoptic.info/pages/coding.html

Tested on macOS 10.13.3 /w Python 2.7 & Python 3.6

Credits
=======

Contributors
------------
* `Christopher Hahne <http://www.christopherhahne.de/>`__

Sponsors
--------
* `IRAC at University of Bedfordshire <https://www.beds.ac.uk/research-ref/irac/about>`__
* `7th Framework Programme under Grant EU-FP7 ICT-2010-248420 <https://cordis.europa.eu/project/rcn/94148_en.html>`__

Citation
--------
If you find this work helpful, please cite the following publications:

* `Refocusing distance of a standard plenoptic camera <https://doi.org/10.1364/OE.24.021521>`__, *OpticsExpress*, `[BibTeX] <http://www.plenoptic.info/bibtex/HAHNE-OPEX.2016.bib>`__

* `Baseline and triangulation geometry in a standard plenoptic camera <https://www.plenoptic.info/IJCV_Hahne17_final.pdf>`__, *Int. J. of Comp. Vis.*, `[BibTeX] <http://plenoptic.info/bibtex/HAHNE-IJCV.2017.bib>`__
