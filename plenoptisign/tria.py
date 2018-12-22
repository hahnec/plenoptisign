#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2018 Christopher Hahne <inbox@christopherhahne.de>

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

import numpy as np

class Mixin:

    def tria(self):
        ''' computes the distance from disparity just as baseline and virtual camera orientation of a standard plenoptic camera '''

        # image distance handling
        if self._df == 'Inf':
            self._bU = self._fU                       # image distance at focal plane
        elif self._df <= self._fU:
            self._bU = float('Inf')                   # image distance at infinity
        elif self._df > self._fU:
            self._bU = self._fU
            self._aU = self._df - self._fU - self._HH
            while self._bU != (1/self._fU-1/self._aU)**-1:
                self._bU = (1/self._fU-1/self._aU)**-1    # calculate paraxial image distance
                self._aU = self._df - self._bU - self._HH

        # variable initialization
        self._u, self._mij, self._Uij, self._qij = [np.zeros(2) for _ in range(4)]

        # ray geometry calculation
        j = 1
        s = j * self._pm
        mc = -(s / self._dA)
        uc = -mc * self._fs + s
        self._u[0] = uc + self._pp * self._G
        self._mij[0] = -self._pp * self._G / self._fs
        self._mij[1] = (s - self._u[0]) / self._fs
        self._Uij[0] = self._mij[0] * self._bU
        self._Uij[1] = self._mij[1] * self._bU + s
        self._qij[0] = (self._mij[0] * self._fU - self._Uij[0]) / self._fU
        self._qij[1] = (self._mij[1] * self._fU - self._Uij[1]) / self._fU

        # function solver for system of linear equations
        intersect_fun = lambda A, b: np.dot(np.linalg.inv(A), b)

        # locate object side related virtual camera position
        self._intersect, self.B = intersect_fun(np.array([[-self._qij[1], 1], [-self._qij[0], 1]]),
                                                np.array([self._Uij[1], self._Uij[0]]))
        self.phi = np.degrees(np.arctan(self._qij[0]))
        self._ent_pup_pos = self._bU + self._HH + self._intersect # longitudinal entrance pupil position

        # estimate baseline at entrance pupil
        self.B = self._qij[0] * self._intersect + self._Uij[0]
        b_new = self._bU
        self._pp_new = (-self._qij[1] * b_new + self.B) - (-self._qij[0] * b_new + self.B)

        # triangulation
        dx_new = np.transpose(self._dx) * self._pp_new
        self.Z = self.B * b_new / (dx_new + b_new * -np.tan(np.radians(self.phi))) if self._dx != 0 or self.phi != 0 else float('inf')

        return True