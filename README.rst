===================
|logo| PlenoptiSign
===================

Description
-----------

*PlenoptiSign* is an open-source app_ for geometry estimation of a light field captured by a Standard Plenoptic Camera (SPC).
This software treats a pair of light field rays as a system of linear functions whose solution yields ray intersections indicating distances to refocused object planes or virtual camera positions of perspective views (so-called sub-aperture images).

|release| |license| |downloads| |pypi|

|paper| |zenodo|


GUI-based executable
====================

* **Installation**:
    1. download as an app_ (macOS_, Windows_ and Linux_)
    2. extract the archive to obtain the executable

* **Usage**:
    run extracted app_ (macOS_, Windows_ and Linux_)

|gui|

.. note::
    Insightful description of the parameter terminology and experimental validation can be found in the author's publications:

    * `Refocusing distance of a standard plenoptic camera`_, Hahne et al., *OpticsExpress*, `[BibTeX] <http://www.plenoptic.info/bibtex/HAHNE-OPEX.2016.bib>`__

    * `Baseline and triangulation geometry in a standard plenoptic camera`_, Hahne et al., *Int. J. of Comp. Vis.*, `[BibTeX] <http://plenoptic.info/bibtex/HAHNE-IJCV.2017.bib>`__

    * `PlenoptiSign paper`_, Hahne and Aggoun, *SoftwareX*, Volume 10, 2019

    If you find this work helpful for your research, please cite as appropriate.


Command-line interface
======================

* **Installation**:
    For ease of use, you can install with pip:

    * ``$ pip install plenoptisign``

    Alternatively, installation is possible from source via:

    1. download the source_ using ``$ git clone https://github.com/hahnec/plenoptisign.git``
    2. go to the root directory ``$ cd plenoptisign``
    3. install with ``$ python setup.py install`` from the root directory


* **Usage**:
    Run ``$ plenoptisign`` from the command line with optional arguments:

    * -g, --gui: open graphical user interface
    * -p, --plot: plot paraxial rays
    * -r, --refo: refocusing results only
    * -t, --tria: triangulation results only
    * -h, --help: print help message


    Unit testing is done with ``$ python plenoptisign/tests/plenoptisign_unittest.py -v``

CGI server
==========

* **Installation**:
    1. download the source_
    2. place extracted ``plenoptisign-master`` folder on the ftp next to your ``*.html`` that you want to embed it in
    3. rename ``plenoptisign-master`` to ``plenoptisign``
    4. include ``cgi.html`` into your ``*.html`` with ``includeCGI`` as the ``id`` of the desired ``div`` container

        .. code-block:: html

            <script>
                $(function(){
                    $("#includeCGI").load("plenoptisign/plenoptisign/bin/cgi.html");
                });
            </script>
            .
            .
            .
            <div id="includeCGI"></div>


    5. give sufficient permission (chmod 750) to the file ``plenoptisign/plenoptisign/bin/cgi_script.py``

* **Usage**:

    website demo: http://www.plenoptic.info/pages/software.html

Tested on macOS 10.14.2 and Windows 10 w/ Python 2.7 & Python 3.6

Credits
-------

Citation
========

.. code-block:: BibTeX

    @article{Hahne_2019,
       title={PlenoptiSign: An optical design tool for plenoptic imaging},
       volume={10},
       ISSN={2352-7110},
       url={http://dx.doi.org/10.1016/j.softx.2019.100259},
       DOI={10.1016/j.softx.2019.100259},
       journal={SoftwareX},
       publisher={Elsevier BV},
       author={Hahne, Christopher and Aggoun, Amar},
       year={2019},
       month={Jul},
       pages={100259}
    }

Contributors
============

|Hahne|

`Christopher Hahne <http://www.christopherhahne.de/>`__

Sponsors
========
|

.. list-table::
   :widths: 8 8

   * - |EUFramework|
     - |UoB|
   * - `under Grant EU-FP7 ICT-2010-248420 <https://cordis.europa.eu/project/rcn/94148_en.html>`__
     - `Institute for Research in Applicable Computing (IRAC) <https://www.beds.ac.uk/research-ref/irac/about>`__

Further information
-------------------

* check out PlenoptiSign's partner project PlenoptiCam_ capable of rendering light field images from scratch.
* visit `plenoptic.info <http://www.plenoptic.info>`__ for technical details, animated figures and theoretical background

.. Image substitutions

.. |release| image:: https://img.shields.io/github/release/hahnec/plenoptisign.svg?style=flat-square
    :target: https://github.com/hahnec/plenoptisign/releases
    :alt: release

.. |license| image:: https://img.shields.io/badge/License-GPL%20v3.0-orange.svg?style=flat-square
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License

.. |code| image:: https://img.shields.io/github/languages/code-size/hahnec/plenoptisign.svg?style=flat-square
    :target: https://github.com/hahnec/plenoptisign/archive/v1.1.3.zip
    :alt: Code size

.. |repo| image:: https://img.shields.io/github/repo-size/hahnec/plenoptisign.svg?style=flat-square
    :target: https://github.com/hahnec/plenoptisign/archive/v1.1.3.zip
    :alt: Repo size

.. |downloads| image:: https://img.shields.io/github/downloads/hahnec/plenoptisign/total.svg?label=Release%20downloads&style=flat-square
    :target: https://github.com/hahnec/plenoptisign/archive/v1.1.3.zip
    :alt: Downloads

.. |pypi_total| image:: https://pepy.tech/badge/plenoptisign?label=PyPI%20total&style=flat-square
    :target: https://pepy.tech/project/plenoptisign
    :alt: PyPi Dl2

.. |pypi| image:: https://img.shields.io/pypi/dm/plenoptisign?label=PyPI%20downloads&style=flat-square
    :target: https://pypi.org/project/plenoptisign/
    :alt: PyPI Downloads

.. |zenodo| image:: https://zenodo.org/badge/126895033.svg?style=flat-square
    :target: https://zenodo.org/badge/latestdoi/126895033
    :alt: zenodo link

.. |paper| image:: http://img.shields.io/badge/paper-arxiv.2006.01015-red.svg?style=flat-square
    :target: https://arxiv.org/pdf/2006.01015.pdf
    :alt: arXiv link

.. |logo| image:: https://raw.githubusercontent.com/hahnec/plenoptisign/master/plenoptisign/gui/misc/circlecompass_1055093_24x24.png

.. |gui| image:: https://raw.githubusercontent.com/hahnec/plenoptisign/develop/docs/img/screenshot_2d_refo.png

.. |UoB| raw:: html

    <img src="https://3tkh0x1zl0mb1ta92c2mrvv2-wpengine.netdna-ssl.com/wp-content/uploads/2015/12/LO_KukriGB_Universities_Bedfordshire.png" width="70px">

.. |EUFramework| raw:: html

    <img src="http://www.gsa.europa.eu/sites/default/files/Seventh_Framework_Programme_logo.png" width="100px">

.. |Hahne| raw:: html

    <img src="http://www.christopherhahne.de/images/about_alt.jpg" width="100px">

.. Hyperlink aliases

.. _source: https://github.com/hahnec/plenoptisign/archive/master.zip
.. _app: https://github.com/hahnec/plenoptisign/releases/
.. _macOS: https://github.com/hahnec/plenoptisign/releases/download/v1.1.3/plenoptisign_1.1.3_macOS.zip
.. _Windows: https://github.com/hahnec/plenoptisign/releases/download/v1.1.3/plenoptisign_1.1.3_win.zip
.. _Linux: https://github.com/hahnec/plenoptisign/releases/download/v1.1.3/plenoptisign_1.1.3_linux.zip
.. _PlenoptiCam: https://github.com/hahnec/plenopticam/
.. _CGI demo: http://www.plenoptic.info/pages/software.html

.. _Optics, Eugene Hecht:  https://www.pearson.com/us/higher-education/program/Hecht-Optics-5th-Edition/PGM45350.html
.. _Refocusing distance of a standard plenoptic camera: https://doi.org/10.1364/OE.24.021521
.. _Baseline and triangulation geometry in a standard plenoptic camera: http://www.plenoptic.info/files/IJCV_Hahne17_final.pdf
.. _PlenoptiSign paper: https://doi.org/10.1016/j.softx.2019.100259