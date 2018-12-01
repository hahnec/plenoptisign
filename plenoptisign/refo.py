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

    def refo(self):
        ''' computes the distance and depth of field of a plane that is computationally focused based on a standard plenoptic camera '''

        # image distance handling
        if self._df == 'Inf':
            self._bU = self._fU  # image distance at focal plane
        elif self._df <= self._fU:
            self._bU = float('Inf')  # image distance at infinity
        elif self._df > self._fU:
            self._bU = self._fU
            self._aU = self._df-self._fU-self._HH
            while self._bU != (1/self._fU-1/self._aU)**-1:
                self._bU = (1/self._fU-1/self._aU)**-1  # calculate paraxial image distance
                self._aU = self._df-self._bU-self._HH

        # output variables
        self.d = 0  # refocusing distance
        self.d_p = 0  # far depth of field border in refocusing
        self.d_m = 0  # near depth of field border in refocusing
        self.dof = 0  # depth of field
        self.B = 0  # baseline at entrance pupil of the main lens
        self.phi = 0  # tilt angle of virtual camera
        self.Z = 0  # triangulation distance

        # variables used for plot functions
        self._sc = 0
        self._uc = np.zeros(2)  # micro image centers (MICs)
        self._u = np.zeros(2)  # micro image ray positions
        self._s = np.zeros(2)  # micro lens positions
        self._Uij = np.zeros(2)  # intersections at the main lens
        self._Fij = np.zeros(2)  # intersections at the main lens' focal plane
        self._uU = np.zeros(2)
        self._uL = np.zeros(2)
        self._sU = np.zeros(2)
        self._sL = np.zeros(2)
        self._UijU = np.zeros(2)
        self._UijL = np.zeros(2)

        self.console_msg = []

        # local variable initialization
        j = np.zeros(2);
        i = np.zeros(2)
        mc = np.zeros(2)
        mij = np.zeros(2);
        qij = np.zeros(2)
        mU = np.zeros(2);
        mL = np.zeros(2)
        mijU = np.zeros(2);
        mijL = np.zeros(2)
        FijU = np.zeros(2);
        FijL = np.zeros(2)
        qijU = np.zeros(2);
        qijL = np.zeros(2)

        # (s,u) coordinates for the intersecting rays
        smax = 2*self._M+1
        self._sc = (smax-1)/2

        # warnings
        if self._fU > self._bU:
            self.console_msg.append('Image distance is smaller than focal length (fU>bU).')
        elif self._a >= (smax-1)/2:
            self.console_msg.append('Refocusing slice is out of range.')

        # align intersection to be as paraxial as possible
        c = (self._M-1)/2
        j[0] = -round(self._a*(self._M-1)/2)
        j[1] = self._a*(self._M-1)+j[0]

        # set starting positions for micro lens s and pixel u
        for k in range(2):
            # for pixel centres
            self._s[k] = j[k]*self._pm
            mc[k] = -self._s[k]/self._dA
            self._uc[k] = -mc[k]*self._fs+self._s[k]
            i[k] = c if k == 0 else -c
            self._u[k] = self._uc[k]+i[k]*self._pp
            mij[k] = (self._s[k]-self._u[k])/self._fs
            self._Uij[k] = mij[k]*self._bU+self._s[k]
            self._Fij[k] = mij[k]*self._fU
            qij[k] = (self._Fij[k]-self._Uij[k])/self._fU

            # for pixel borders (DoF rays)
            self._uU[k] = self._u[k]+self._pp/2
            self._uL[k] = self._u[k]-self._pp/2
            self._sU[k] = self._s[k]+self._pm/2
            self._sL[k] = self._s[k]-self._pm/2
            mU[k] = (self._sU[k]-self._uU[k])/self._fs
            mL[k] = (self._sL[k]-self._uL[k])/self._fs
            mijU[k] = (self._s[k]-self._uU[k])/self._fs
            mijL[k] = (self._s[k]-self._uL[k])/self._fs
            self._UijU[k] = mijU[k]*self._bU+self._sU[k]
            self._UijL[k] = mijL[k]*self._bU+self._sL[k]
            FijU[k] = mijU[k]*self._fU
            FijL[k] = mijL[k]*self._fU
            qijU[k] = (FijU[k]-self._UijU[k])/self._fU
            qijL[k] = (FijL[k]-self._UijL[k])/self._fU

        # function solver for system of linear equations
        intersect_fun = lambda A, b: np.dot(np.linalg.inv(A), b)

        # ray intersections behind image sensor
        b_new = self._bU-intersect_fun(np.array([[-mij[0], 1], [-mij[1], 1]]), np.array([self._s[0], self._s[1]]))[0]
        b_new_m = self._bU-intersect_fun(np.array([[-mijL[0], 1], [-mijU[1], 1]]), np.array([self._sL[0], self._sU[1]]))[0]
        b_new_p = self._bU-intersect_fun(np.array([[-mijU[0], 1], [-mijL[1], 1]]), np.array([self._sU[0], self._sL[1]]))[0]

        # check if refocused object plane not at infinity
        if (self._fU <= self._bU and self._a >= 0) and b_new > self._fU:
            # get distances from refocused image side planes
            d_new = (1/self._fU-1/b_new)**-1+self._bU+self._HH
            d_new_p = (1/self._fU-1/b_new_p)**-1+self._bU+self._HH
            d_new_m = (1/self._fU-1/b_new_m)**-1+self._bU+self._HH

            # solve for ray intersections in object space to obtain distances and DoF
            self.d = intersect_fun(np.array([[-qij[0], 1], [-qij[1], 1]]), np.array([self._Uij[0], self._Uij[1]]))[
                         0]+self._bU+self._HH
            self.d_p = intersect_fun(np.array([[-qijU[0], 1], [-qijL[1], 1]]), np.array([self._UijU[0], self._UijL[1]]))[
                           0]+self._bU+self._HH
            self.d_m = intersect_fun(np.array([[-qijL[0], 1], [-qijU[1], 1]]), np.array([self._UijL[0], self._UijU[1]]))[
                           0]+self._bU+self._HH
            self.dof = self.d_p-self.d_m

            # check if far depth of field border at infinity
            if self._fU >= b_new_p:
                self.d_p = float('Inf')
                self.dof = float('Inf')
        # check if refocused object plane at infinity
        elif (self._fU is self._bU and self._a is 0) or b_new is self._fU:
            self.console_msg.append('Refocused object plane at infinity.')
            self.d = float('Inf')
            d_new = float('Inf')
            self.d_p = float('Inf')
            d_new_p = float('Inf')
            # check if narrow depth of field border at infinity
            if self._fU >= b_new_m:
                self.d_m = float('Inf')
                # d_new_m = float('Inf')
                self.dof = float('Inf')
            else:
                self.d_m = intersect_fun(np.array([[-qijL[0], 1], [-qijU[1], 1]]),
                                         np.array([self._UijL[0], self._UijU[1]]))[0]+self._bU+self._HH
                d_new_m = (1/self._fU-1/b_new_m)**-1+self._bU+self._HH
                self.dof = self.d_p-self.d_m
        # check if refocused object plane exists
        elif (self._fU >= self._bU and self._a <= 0) or b_new < self._fU:
            self.console_msg.append('Refocused object plane out of range.')
            self.d = float('Inf')
            d_new = float('Inf')
            # check if narrow depth of field border at infinity (distinction redundant?)
            if self._fU > b_new_m:
                self.d_m = float('Inf')
                d_new_m = float('Inf')
                self.dof = float('Inf')
            elif self._fU is b_new_m:
                self.d_m = float('Inf')
                d_new_m = float('Inf')
                self.dof = float('Inf')
            else:
                self.d_m = intersect_fun(np.array([[-qijL[0], 1], [-qijU[1], 1]]),
                                         np.array([self._UijL[0], self._UijU[1]]))[0]+self._bU+self._HH
                d_new_m = (1/self._fU-1/b_new_m)**-1+self._bU+self._HH
                self.dof = self.d_p-self.d_m
            # check if farther depth of field border at infinity
            if self._fU > b_new_p:
                self.d_p = float('Inf')
                d_new_p = float('Inf')
                self.dof = float('Inf')
            elif self._fU is b_new_p:
                self.d_m = float('Inf')
                d_new_m = float('Inf')
                self.dof = float('Inf')
            else:
                self.d_p = intersect_fun(np.array([[-qijU[0], 1], [-qijL[1], 1]]),
                                         np.array([self._UijU[0], self._UijL[1]]))[0]+self._bU+self._HH
                d_new_p = (1/self._fU-1/b_new_p)**-1+self._bU+self._HH

        # comparison of image and object side approach (for debug purposes)
        if not (np.equal(np.round(d_new), np.round(self.d)) or np.equal(np.round(d_new_p), np.round(self.d_p)) or \
                np.equal(np.round(d_new_m), np.round(self.d_m))):
            raise AssertionError('Results for object and image side intersections are different.')

        return True