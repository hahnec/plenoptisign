===================
|logo| Plenoptisign
===================

Light field geometry estimator for a Standard Plenoptic Camera (SPC)

This software treats a pair of lightfield rays as a system of linear functions whose solution yields ray intersections indicating distances to refocused object planes or virtual camera positions for perspective views captured by an SPC.

Check out Plenoptisign's partner project Plenopticam_ capable of rendering light field images from scratch.

|release| |license| |code| |repo| |downloads|

Installation
============

GUI-based executable
--------------------

* **Installation**:
    1. download as an app_ (for macOS_ and Windows_ only)
    2. extract the archive to obtain the executable

* **Usage**:
    run extracted app_ (for macOS_ and Windows_ only)

|gui|

.. note::
    Insightful description of the parameter terminology can be found in the author's publications:

    * `Refocusing distance of a standard plenoptic camera`_, Hahne et al., *OpticsExpress*, `[BibTeX] <http://www.plenoptic.info/bibtex/HAHNE-OPEX.2016.bib>`__

    * `Baseline and triangulation geometry in a standard plenoptic camera`_, Hahne et al., *Int. J. of Comp. Vis.*, `[BibTeX] <http://plenoptic.info/bibtex/HAHNE-IJCV.2017.bib>`__

    If you find this work helpful for your research, please cite as appropriate.


Command-line interface
----------------------

* **Installation**:
    1. download the source_ using ``$ git clone https://github.com/hahnec/plenoptisign.git``
    2. go to the root directory ``$ cd plenoptisign``
    3. install with ``$ python setup.py install`` from the root directory


* **Usage**:
    run ``$ plenoptisign`` from the command line with optional arguments

    * -g, --gui: open graphical user interface
    * -p, --plot: plot paraxial rays
    * -r, --refo: refocusing results only
    * -t, --tria: triangulation results only
    * -h, --help: print help message


    unit testing: ``$ python plenoptisign/tests/plenoptisign_unittest.py -v``

CGI server
----------

* **Installation**:
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

* **Usage**:

    website demo: http://www.plenoptic.info/pages/coding.html

Tested on macOS 10.14.2 and Windows 10 w/ Python 2.7 & Python 3.6

User Guide
==========

Once Plenoptisign is ready for use (whether from source_, as an app_ or `CGI demo`_), you will be provided with a default parameter set.
You can start off varying these parameters as you like to see their impact on the light field geometry.
As of version 1.1.0, the input and output parameters are defined as shown in the following.

Optical parameters
------------------

|

.. list-table:: Input Parameters
   :widths: 4 15
   :header-rows: 1

   * - Notation
     - Description
   * - :math:`p_p`
     - pixel pitch
   * - :math:`f_s`
     - micro lens focal length
   * - :math:`H_{1s}H_{2s}`
     - micro lens principal plane spacing
   * - :math:`p_m`
     - micro lens pitch
   * - :math:`d_{A'}`
     - exit pupil distance
   * - :math:`f_U`
     - main lens focal length
   * - :math:`H_{1U}H_{2U}`
     - main lens principal plane spacing
   * - :math:`d_f`
     - main lens focusing distance
   * - :math:`F\#`
     - F-number
   * - :math:`a`
     - refocusing shift parameter
   * - :math:`M`
     - micro image resolution
   * - :math:`G`
     - virtual camera gap
   * - :math:`\Delta x`
     - disparity

|

.. list-table:: Geometry Results
   :widths: 4 15
   :header-rows: 1

   * - Notation
     - Description
   * - :math:`d_a`
     - refocusing distance
   * - :math:`DoF`
     - depth of field
   * - :math:`d_{a-}`
     - narrow DoF border
   * - :math:`d_{a+}`
     - narrow DoF border
   * - :math:`B_G`
     - baseline
   * - :math:`\Phi_G`
     - tilt angle
   * - :math:`Z_{(G, \Delta x)}`
     - triangulation distance

Design trends
-------------
Generally, it can be stated that the refocusing distance :math:`d_a` and triangulation distance :math:`Z_{(G, \Delta x)}`  drop with

    * ascending shift parameter :math:`a` or ascending disparity :math:`\Delta x`
    * enlarging micro lens focal length :math:`f_s`
    * reducing objective lens focal length :math:`f_U`

and vice versa. Similarly, the baseline :math:`B_G`, a substantial triangulation parameter, grows with

    * larger main lens focal length :math:`f_U`
    * shorter micro lens focal length :math:`f_s`
    * decreasing focusing distance :math:`d_f`
    * increasing absolute virtual camera spacing :math:`|G|`

In case of the app_ version, graphical plots will be displayed supporting you in the decision making.

Credits
=======

Contributors
------------
* `Christopher Hahne <http://www.christopherhahne.de/>`__

Sponsors
--------
* `IRAC at University of Bedfordshire <https://www.beds.ac.uk/research-ref/irac/about>`__
* `7th Framework Programme under Grant EU-FP7 ICT-2010-248420 <https://cordis.europa.eu/project/rcn/94148_en.html>`__

Further information
-------------------

* visit `plenoptic.info <http://www.plenoptic.info>`__ for technical details, animated figures and theoretical background

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

.. |logo| image:: https://raw.githubusercontent.com/hahnec/plenoptisign/master/plenoptisign/gui/misc/circlecompass_1055093_24x24.png

.. |gui| image:: https://raw.githubusercontent.com/hahnec/plenoptisign/develop/docs/img/screenshot_2d_refo.png

.. Hyperlink aliases

.. _source: https://github.com/hahnec/plenoptisign/archive/master.zip
.. _app: https://github.com/hahnec/plenoptisign/releases/tag/v1.0.0-beta
.. _macOS: https://github.com/hahnec/plenoptisign/releases/download/v1.0.0-beta/plenoptisign_1.0.0_macOS.zip
.. _Windows: https://github.com/hahnec/plenoptisign/releases/download/v1.0.0-beta/plenoptisign_1.0.0_windows.zip
.. _Plenopticam: https://github.com/hahnec/plenopticam/
.. _CGI demo: http://www.plenoptic.info/pages/coding.html

.. _Optics, Eugene Hecht:  https://www.pearson.com/us/higher-education/program/Hecht-Optics-5th-Edition/PGM45350.html
.. _Refocusing distance of a standard plenoptic camera: https://doi.org/10.1364/OE.24.021521
.. _Baseline and triangulation geometry in a standard plenoptic camera: https://www.plenoptic.info/IJCV_Hahne17_final.pdf