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

import numpy as np
from .solver import solve_sle
from . import PlenoptisignError, DEC_P

class Mixin:

    def tria(self):
        ''' computes depth plane distance, virtual camera orientation and baseline of a standard plenoptic camera '''

        # compute main lens image distance
        self.compute_img_dist()

        # ray geometry calculation
        j = 1
        s = j * self.pm
        mc = -(s / self.dA)
        uc = -mc * self.fs + s
        self._u[0] = uc + self.pp * self.G
        self._mij[0] = -self.pp * self.G / self.fs
        self._mij[1] = (s - self._u[0]) / self.fs
        for k in range(2):
            self._Uij[k] = self._mij[k] * self.bU + s*k
            self._qij[k] = (self._mij[k] * self.fU - self._Uij[k]) / self.fU

        # locate object side related virtual camera position
        self._intersect, self.B = solve_sle(np.array([[-self._qij[0], 1], [-self._qij[1], 1]]),
                                            np.array([self._Uij[0], self._Uij[1]]))
        # orientation of virtual camera
        self.phi = np.degrees(np.arctan(self._qij[0]))

        # longitudinal entrance pupil position
        self._ent_pup_pos = self.bU + self.HH + self._intersect

        # validate baseline approach (for debug purposes)
        B_alt = self._qij[0] * self._intersect + self._Uij[0]
        if not (np.equal(round(self.B, DEC_P), round(B_alt, DEC_P))):
            raise PlenoptisignError('Baseline validation failed')

        # triangulation
        b_new = self.bU
        self._pp_new = (-self._qij[1] * b_new + self.B) - (-self._qij[0] * b_new + self.B)
        dx_new = np.transpose(self.dx) * self._pp_new

        # is depth plane at infinity?
        if self.bU <= self.fU and self.dx <= 0:
            self.Z = float('inf')
        elif self.bU >= self.fU:
            self.Z = self.B * b_new / (dx_new + b_new * -np.tan(np.radians(self.phi)))

        return True