#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2019 Christopher Hahne <inbox@christopherhahne.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from . import refo
from . import tria
from . import plt_refo
from . import plt_tria
from . import plt_3d

import numpy as np


class MainClass(plt_3d.Mixin, plt_tria.Mixin, plt_refo.Mixin, tria.Mixin, refo.Mixin, object):
    """ The MainClass stores optical parameters and performs numerical light field geometry calculations.

    It is made of five Mixin classes which are laid off in separate files containing methods for distance retrieval.
    The main methods to compute the plenoptic geometry are :func:`refo()` and :func:`tria()`.
    The Mixin classes share the optical parameters which are initialized as seen in :func:`__init__()` below.

    Usage example::

        >> import plenoptisign
        >> obj = plenoptisign.MainClass()
        >> obj.refo()
        >> results = obj.get_results()
        >> print(results)

    """

    def __init__(self, data=None):
        """ Initialize plenoptic camera parameters with following instance variables:

            :param data: dictionary containing input parameters (see full description below)
            :param d: refocusing distance
            :param d_p: far depth of field border in refocusing
            :param d_m: near depth of field border in refocusing
            :param dof: depth of field
            :param B: baseline at entrance pupil of the main lens
            :param phi: tilt angle of virtual camera
            :param Z: triangulation distance
            :param bU: main lens image distance
            :param console_msg: text for console output

            :type data: dict
            :type d: float
            :type d_p: float
            :type d_m: float
            :type dof: float
            :type B: float
            :type phi: float
            :type Z: float
            :type bU: float
            :type console_msg: str

            .. note::
                Insightful description of the parameter terminology can be found in the author's publications:

                * `Refocusing distance of a standard plenoptic camera <https://doi.org/10.1364/OE.24.021521>`__, Hahne et al., *OpticsExpress*, `[BibTeX] <http://www.plenoptic.info/bibtex/HAHNE-OPEX.2016.bib>`__

                * `Baseline and triangulation geometry in a standard plenoptic camera <https://www.plenoptic.info/IJCV_Hahne17_final.pdf>`__, Hahne et al., *Int. J. of Comp. Vis.*, `[BibTeX] <http://plenoptic.info/bibtex/HAHNE-IJCV.2017.bib>`__

                If you find this work helpful for your research, please cite as appropriate.



        """

        # convert input data dictionary to class variables
        self.data = data if data is not None else dict()

        # initialize output variables
        self.d = 0      # refocusing distance:instance variable
        self.d_p = 0    # far depth of field border in refocusing
        self.d_m = 0    # near depth of field border in refocusing
        self.dof = 0    # depth of field
        self.B = 0      # baseline at entrance pupil of the main lens
        self.phi = 0    # tilt angle of virtual camera
        self.Z = 0      # triangulation distance
        self.bU = None  # main lens image distance

        # initialize private variables
        self._sc = 0
        self._uc = np.zeros(2)   # micro image centers (MICs)
        self._u = np.zeros(2)    # micro image ray positions
        self._s = np.zeros(2)    # micro lens positions
        self._mij = np.zeros(2)  # image side ray slopes
        self._Uij = np.zeros(2)  # intersections at the main lens
        self._Fij = np.zeros(2)  # intersections at the main lens' focal plane
        self._qij = np.zeros(2)  # object side ray slopes
        self._uU = np.zeros(2)
        self._uL = np.zeros(2)
        self._sU = np.zeros(2)
        self._sL = np.zeros(2)
        self._UijU = np.zeros(2)
        self._UijL = np.zeros(2)

        # console message initialization
        self.console_msg = ""

    @property
    def data(self):
        '''
            Instance variable of type dict containing input parameters with following keys

            :keyword data['pp']: pixel pitch
            :keyword data['fs']: focal length of micro lens
            :keyword data['hh']: principal plane separation of micro lens
            :keyword data['pm']: micro lens pitch
            :keyword data['dA']: exit pupil distance
            :keyword data['fU']: focal length of objective lens
            :keyword data['HH']: principal plane spacing in objective lens
            :keyword data['df']: object distance
            :keyword data['f_num']: main lens entrance pupil diameter
            :keyword data['a']: iterative refocusing parameter
            :keyword data['M']: 1-D micro image diameter
            :keyword data['G']: viewpoint gap
            :keyword data['dx']: disparity value

        '''

        return self.data

    @data.setter
    def data(self, data=None):
        ''' put data dictionary to class variables while setting default values to avoid errors '''

        data = data if data is not None else dict()

        self.pp = float(data['pp']) if 'pp' in data else .009           # pixel pitch
        self.fs = float(data['fs']) if 'fs' in data else 2.75           # focal length of micro lens
        self.hh = float(data['hh']) if 'hh' in data else .396           # principal plane separation of micro lens
        self.pm = float(data['pm']) if 'pm' in data else .125           # micro lens pitch
        self.dA = float(data['dA']) if 'dA' in data else 111.0324       # exit pupil distance
        self.fU = float(data['fU']) if 'fU' in data else 193.2935       # focal length of objective lens
        self.HH = float(data['HH']) if 'HH' in data else -65.5563       # principal plane spacing in objective lens
        self.df = float(data['df']) if 'df' in data else float('inf')   # object distance
        self.D = self.fU/float(data['f_num']) if 'f_num' in data else self.fU/16.   # main lens pupil diameter
        self.a = float(data['a']) if 'a' in data else 1.0               # iterative refocusing parameter
        self.M = float(data['M']) if 'M' in data else 13.9523           # 1-D micro image diameter
        self.G = float(data['G']) if 'G' in data else -6                # viewpoint gap
        self.dx = float(data['dx']) if 'dx' in data else 1              # disparity value
        self.sd = tuple(data['sd']) if 'sd' in data else (24.048,36.072)# sensor dimensions
        self.refo_opt = float(data['refo']) if 'refo' in data else True # refo bool option
        self.tria_opt = float(data['tria']) if 'tria' in data else True # tria bool option

    def get_results(self):
        ''' This is the getter function for output parameters. See :func:`__init__()` for more details on the parameters.

            :returns: list(**d**, **d_p**, **d_m**, **dof**, **B**, **phi**, **Z**)
            :rtype: list
        '''

        return list([self.d, self.d_p, self.d_m, self.dof, self.B, self.phi, self.Z])

    def compute_img_dist(self):
        ''' This method iteratively computes the main lens image distance :math:`b_U` via
        :math:`b_U = (\\frac{1}{f_U}-\\frac{1}{a_U})^{-1}` until both sides match. The initial value is :math:`b_U=f_U`.

        :return: **True**
        :rtype: bool

        '''

        # is image distance at focal plane?
        if self.df == float('inf'):
            self.bU = self.fU
        # is image distance between infinity and focal plane?
        elif self.df > self.fU:
            # set initial values for iteration
            self.bU = self.fU
            self.aU = self.df - self.fU - self.HH
            # calculate paraxial image and object distance iteratively
            while self.bU != (1/self.fU-1/self.aU)**-1:
                self.bU = (1/self.fU-1/self.aU)**-1
                self.aU = self.df-self.bU-self.HH
                # is object distance smaller than image distance?
                if self.aU < 0:
                    self.bU = (1/self.fU-1/self.aU)**-1
                    self.console_msg = 'Object distance smaller than image distance'
                    break
        # is image distance at infinity?
        elif self.df <= self.fU:
            self.bU = float('inf')

        return True

    def compute_mic_img_size(self):
        ''' This method mutates the micro image size :math:`M` according to
            :math:`M = \\frac{D \\times f_s}{f_U \\times p_p}`.

            :return: **True**
            :rtype: bool

        '''

        self.M = (self.D*self.fs)/(self.fU*self.pp)

        return True

    def compute_pupil_size(self):
        ''' This method estimates the pupil size :math:`D` of the main lens via
            :math:`D = \\frac{M \\times f_U \\times p_p}{f_s}.`

            :return: **True**
            :rtype: bool

        '''

        self.D = (self.M*self.fU*self.pp)/self.fs

        return True

    def _format_coord_2d(self, x, y):
        """ wrapper function used to swap on hover coordinates fox x and z axes in plot window """

        # swap coordinates for current cursor position
        xs = self._ax.format_xdata(x)
        ys = self._ax.format_ydata(y)

        return 'z=%s, y=%s' % (xs, ys)
