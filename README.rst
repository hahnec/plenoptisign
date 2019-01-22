===================
|logo| Plenoptisign
===================

Light field geometry estimator for a Standard Plenoptic Camera (SPC)

This software treats a pair of lightfield rays as a system of linear functions whose solution yields ray intersections indicating distances to refocused object planes or virtual camera positions for perspective views captured by an SPC.

|release| |license| |code| |repo| |downloads|


Installation
============

* **executable**:
    1. download as an app_ (for macOS_ and Windows_ only)
    2. extract the archive to obtain the executable

* **command-line**:
    1. download the source_, e.g. using ``$ git clone https://github.com/hahnec/plenoptisign.git``
    2. install with ``$ python setup.py install`` from the source_ directory

* **CGI server**:
    1. download the source_
    2. place the extracted ``plenoptisign-master`` folder on the ftp next to your ``*.html`` that you want to embed it in
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

Usage
=====

* **executable**:
    run extracted app_ (for macOS_ and Windows_ only)

* **command-line**:
    run ``$ plenoptisign`` from the command line with optional arguments

    * -g, --gui: open graphical user interface
    * -p, --plot: plot paraxial rays
    * -r, --refo: refocusing results only
    * -t, --tria: triangulation results only
    * -h, --help: print help message


    unit testing: ``$ python plenoptisign/tests/plenoptisign_unittest.py -v``

* **CGI server**:
    website demo: http://www.plenoptic.info/pages/coding.html

Tested on macOS 10.14.2 and Windows 10 w/ Python 2.7 & Python 3.6

Further information
-------------------

* visit `plenoptic.info <http://www.plenoptic.info>`__ for technical details, animated figures and theoretical background

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

.. Image substitutions

.. |release| image:: https://img.shields.io/github/release/hahnec/plenoptisign.svg?style=flat-square
    :target: https://github.com/hahnec/plenoptisign/archive/v1.0.0-beta.zip
    :alt: release

.. |license| image:: https://img.shields.io/badge/License-GPL%20v3.0-orange.svg?style=flat-square
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License

.. |code| image:: https://img.shields.io/github/languages/code-size/hahnec/plenoptisign.svg?style=flat-square
    :target: https://github.com/hahnec/plenoptisign/archive/v1.0.0-beta.zip
    :alt: Code size

.. |repo| image:: https://img.shields.io/github/repo-size/hahnec/plenoptisign.svg?style=flat-square
    :target: https://github.com/hahnec/plenoptisign/archive/v1.0.0-beta.zip
    :alt: Repo size

.. |downloads| image:: https://img.shields.io/github/downloads/hahnec/plenoptisign/total.svg?style=flat-square
    :target: https://github.com/hahnec/plenoptisign/archive/v1.0.0-beta.zip
    :alt: Downloads

.. |logo| image:: https://github.com/hahnec/plenoptisign/blob/master/plenoptisign/gui/misc/circlecompass_1055093_24x24.png
    :alt: Logo

.. Hyperlink aliases

.. _source: https://github.com/hahnec/plenoptisign/archive/master.zip
.. _app: https://github.com/hahnec/plenoptisign/releases/tag/v1.0.0-beta
.. _macOS: https://github.com/hahnec/plenoptisign/releases/download/v1.0.0-beta/plenoptisign_1.0.0_macOS.zip
.. _Windows: https://github.com/hahnec/plenoptisign/releases/download/v1.0.0-beta/plenoptisign_1.0.0_windows.zip