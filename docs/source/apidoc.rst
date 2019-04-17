.. Plenoptisign documentation master file, created by
   sphinx-quickstart on Sat Mar 16 18:50:44 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================
API documentation
=================

.. toctree::
   :maxdepth: 3
   :caption: Contents:

Architecture
------------

A schematic overview of Plenoptisign's architecture is seen in the diagram below:

.. image:: ../../docs/img/plenoptisign_arch.png

As the mainclass.py and the solver.py will be of primary interest for future extensions, both are documented hereafter.

MainClass
---------

.. automodule:: plenoptisign
.. autoclass:: MainClass
	:inherited-members:
	
.. autofunction:: plenoptisign.solve_sle

.. Indices and tables
.. ==================
.. 
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
