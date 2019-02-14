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


class MainClass(plt_3d.Mixin, plt_tria.Mixin, plt_refo.Mixin, tria.Mixin, refo.Mixin):

    def __init__(self, data=None):
        # input variables from data dictionary (set default values to avoid errors)
        self.pp = float(data['pp']) if 'pp' in data else .009           # pixel pitch
        self.fs = float(data['fs']) if 'fs' in data else 2.75           # focal length of micro lens
        self.hh = float(data['hh']) if 'hh' in data else .396           # principal plane separation of micro lens
        self.pm = float(data['pm']) if 'pm' in data else .125           # micro lens pitch
        self.dA = float(data['dA']) if 'dA' in data else 111.0324       # exit pupil distance
        self.fU = float(data['fU']) if 'fU' in data else 193.2935       # focal length of objective lens
        self.HH = float(data['HH']) if 'HH' in data else -65.5563       # principal plane spacing in objective lens
        self.df = float(data['df']) if 'df' in data else float('inf')   # object distance
        self.D = self.fU/float(data['f_num']) if 'f_num' in data else self.fU/16.   # main lens entrance pupil diameter
        self.a = float(data['a']) if 'a' in data else 1.0               # iterative refocusing parameter
        self.M = float(data['M']) if 'M' in data else 13.               # 1-D micro image diameter
        self.G = float(data['G']) if 'G' in data else -6                # viewpoint gap
        self.dx = float(data['dx']) if 'dx' in data else 1              # disparity value

        # output variables
        self.d = 0      # refocusing distance
        self.d_p = 0    # far depth of field border in refocusing
        self.d_m = 0    # near depth of field border in refocusing
        self.dof = 0    # depth of field
        self.B = 0      # baseline at entrance pupil of the main lens
        self.phi = 0    # tilt angle of virtual camera
        self.Z = 0      # triangulation distance
        self.bU = None

        # variables used for plot functions
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

    def get_results(self):
        ''' get list of results '''

        return list([self.d, self.d_p, self.d_m, self.dof, self.B, self.phi, self.Z])

    def compute_img_dist(self):
        ''' compute main lens image distance self.bU based on focal length self.fU and focus distance self.df '''

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
        ''' estimate micro image size '''

        self.M = (self.D*self.fs)/(self.fU*self.pp)

        return True