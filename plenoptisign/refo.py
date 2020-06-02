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
from plenoptisign.constants import PlenoptisignError, DEC_P


class Mixin:

    def refo(self):
        ''' This method computes the distance :math:`d_a` and depth of field limits :math:`d_{a\\pm }`
        of a plane that is computationally focused based on a standard plenoptic camera. The instance variables that
        are mutated are as follows

        :param d: refocusing distance
        :param d_p: far depth of field border in refocusing
        :param d_m: near depth of field border in refocusing
        :param dof: depth of field
        :type d: float
        :type d_p: float
        :type d_m: float
        :type dof: float

        :return: **True**
        :rtype: bool

        '''

        # local variable initialization
        j, i, mc, mij, qij, mU, mL, mijU, mijL, FijL, FijU, qijU, qijL, d_n, d_p_n, d_m_n = [np.zeros(2) for _ in range(16)]

        # compute main lens image distance
        self.compute_img_dist()

        # (s,u) coordinates for the intersecting rays
        smax = 2*self.M+1
        self._sc = (smax-1)/2

        # warnings
        if self.fU > self.bU:
            self.console_msg = 'Image distance is smaller than focal length'
        elif self.a >= (smax-1)/2:
            self.console_msg = 'Refocusing slice a %0.1f is out of range' % self.a

        # align intersection to be as paraxial as possible
        c = (self.M-1)/2
        j[0] = -np.round(self.a*(self.M-1)/2, DEC_P)
        j[1] = self.a*(self.M-1)+j[0]

        # set starting positions for micro lens s and pixel u
        for k in range(2):
            # for pixel centres
            self._s[k] = j[k]*self.pm
            mc[k] = -self._s[k]/self.dA
            self._uc[k] = -mc[k]*self.fs+self._s[k]
            i[k] = c if k == 0 else -c
            self._u[k] = self._uc[k]+i[k]*self.pp
            mij[k] = (self._s[k]-self._u[k])/self.fs
            self._Uij[k] = mij[k]*self.bU+self._s[k]
            self._Fij[k] = mij[k]*self.fU
            qij[k] = (self._Fij[k]-self._Uij[k])/self.fU

            # for pixel borders (DoF rays)
            self._uU[k] = self._u[k]+self.pp/2
            self._uL[k] = self._u[k]-self.pp/2
            self._sU[k] = self._s[k]+self.pm/2
            self._sL[k] = self._s[k]-self.pm/2
            mU[k] = (self._sU[k]-self._uU[k])/self.fs
            mL[k] = (self._sL[k]-self._uL[k])/self.fs
            mijU[k] = (self._s[k]-self._uU[k])/self.fs
            mijL[k] = (self._s[k]-self._uL[k])/self.fs
            self._UijU[k] = mijU[k]*self.bU+self._sU[k]
            self._UijL[k] = mijL[k]*self.bU+self._sL[k]
            FijU[k] = mijU[k]*self.fU
            FijL[k] = mijL[k]*self.fU
            qijU[k] = (FijU[k]-self._UijU[k])/self.fU
            qijL[k] = (FijL[k]-self._UijL[k])/self.fU

        # ray intersections behind image sensor
        b_new = self.bU-solve_sle(np.array([[-mij[0], 1], [-mij[1], 1]]), np.array([self._s[0], self._s[1]]))[0]
        b_new_m = self.bU-solve_sle(np.array([[-mijL[0], 1], [-mijU[1], 1]]), np.array([self._sL[0], self._sU[1]]))[0]
        b_new_p = self.bU-solve_sle(np.array([[-mijU[0], 1], [-mijL[1], 1]]), np.array([self._sU[0], self._sL[1]]))[0]

        # is refocused object plane not at infinity?
        if self.bU >= self.fU and b_new > self.fU:
            # get distances from refocused image side planes
            d_n = (1/self.fU-1/b_new)**-1+self.bU+self.HH
            d_p_n = (1/self.fU-1/b_new_p)**-1+self.bU+self.HH
            d_m_n = (1/self.fU-1/b_new_m)**-1+self.bU+self.HH

            # solve for ray intersections in object space to obtain distances and DoF
            self.d = solve_sle(np.array([[-qij[0], 1], [-qij[1], 1]]), np.array([self._Uij[0], self._Uij[1]]))[0]\
                                + self.bU+self.HH
            self.d_p = solve_sle(np.array([[-qijU[0], 1], [-qijL[1], 1]]), np.array([self._UijU[0], self._UijL[1]]))[0]\
                                + self.bU+self.HH
            self.d_m = solve_sle(np.array([[-qijL[0], 1], [-qijU[1], 1]]), np.array([self._UijL[0], self._UijU[1]]))[0]\
                                + self.bU+self.HH
            self.dof = self.d_p-self.d_m

            # is far depth of field border at infinity?
            if self.fU >= b_new_p:
                self.d_p = float('Inf')
                self.dof = float('Inf')

        # is refocused object plane at infinity?
        elif b_new is self.fU or (self.fU is self.bU and self.a is 0):
            self.console_msg = 'Refocused object plane a=%0.1f at infinity' % self.a
            self.d = float('Inf')
            d_n = float('Inf')
            self.d_p = float('Inf')
            d_p_n = float('Inf')
            # check if narrow depth of field border at infinity
            if b_new_m <= self.fU:
                self.d_m = float('Inf')
                d_m_n = float('Inf')
                self.dof = float('Inf')
            else:
                self.d_m = solve_sle(np.array([[-qijL[0], 1], [-qijU[1], 1]]),
                                     np.array([self._UijL[0], self._UijU[1]]))[0]+self.bU+self.HH
                d_m_n = (1/self.fU-1/b_new_m)**-1+self.bU+self.HH
                self.dof = self.d_p-self.d_m
        # is refocused object plane beyond infinity?
        elif b_new < self.fU or (self.bU <= self.fU and self.a <= 0):
            self.console_msg = 'Refocused object plane a=%0.1f out of range' % self.a
            self.d = float('Inf')
            d_n = float('Inf')
            # is narrow depth of field border at infinity?
            if b_new_m < self.fU:
                self.d_m = float('Inf')
                d_m_n = float('Inf')
                self.dof = float('Inf')
            elif self.fU is b_new_m:
                self.d_m = float('Inf')
                d_m_n = float('Inf')
                self.dof = float('Inf')
            else:
                self.d_m = solve_sle(np.array([[-qijL[0], 1], [-qijU[1], 1]]),
                                     np.array([self._UijL[0], self._UijU[1]]))[0]+self.bU+self.HH
                d_m_n = (1/self.fU-1/b_new_m)**-1+self.bU+self.HH
                self.dof = self.d_p-self.d_m
            # is farther depth of field border at infinity? (redundant since central plane already at infinity)
            if b_new_p < self.fU:
                self.d_p = float('Inf')
                d_p_n = float('Inf')
                self.dof = float('Inf')
            elif b_new_p is self.fU:
                self.d_m = float('Inf')
                d_m_n = float('Inf')
                self.dof = float('Inf')
            else:
                self.d_p = solve_sle(np.array([[-qijU[0], 1], [-qijL[1], 1]]),
                                     np.array([self._UijU[0], self._UijL[1]]))[0]+self.bU+self.HH
                d_p_n = (1/self.fU-1/b_new_p)**-1+self.bU+self.HH

        # comparison of image and object side approach (for debugging purposes)
        if not (np.equal(round(d_n, DEC_P), round(self.d, DEC_P)) or
                np.equal(round(d_p_n, DEC_P), round(self.d_p, DEC_P)) or
                np.equal(round(d_m_n, DEC_P), round(self.d_m, DEC_P))):
            raise PlenoptisignError('Results for object and image side intersections are different')

        return True
