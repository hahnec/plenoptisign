#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2017 Christopher Hahne <inbox@christopherhahne.de>

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
from .version import __version__

class SpcLfGeo(object):
    def __init__(self, data=[]):
        # input variables from data dictionary (set default values to prevent errors)
        self._pp = float(data["pp"]) if "pp" in data else .009        # pixel pitch
        self._fs = float(data["fs"]) if "fs" in data else 2.75        # focal length of micro lens
        self._hh = float(data["hh"]) if "hh" in data else .396        # principal plane separation of micro lens
        self._pm = float(data["pm"]) if "pm" in data else .125        # micro lens pitch
        self._dA = float(data["dA"]) if "dA" in data else 111.0324    # exit pupil distance
        self._fU = float(data["fU"]) if "fU" in data else 193.2935    # focal length of objective lens
        self._HH = float(data["HH"]) if "HH" in data else -65.5563    # principal plane spacing in objective lens
        self._df = float(data["df"]) if "df" in data else float('inf')# object distance
        self._D = self._fU/float(data["f_num"]) if "f_num" in data else self._fU/2.6846  # entrance pupil diameter of main lens
        self._a = float(data["a"]) if "a" in data else 1.0            # iterative refocusing parameter
        self._M = float(data["M"]) if "M" in data else 13             # 1-D micro image diameter
        self._i = float(data["i"]) if "i" in data else -6             # viewpoint position
        self._dx = float(data["dx"]) if "dx" in data else 1           # disparity value

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

        # output variables
        self.d = 0                # refocusing distance
        self.d_p = 0              # far depth of field border in refocusing
        self.d_m = 0              # near depth of field border in refocusing
        self.dof = 0              # depth of field
        self.B = 0                # baseline at entrance pupil of the main lens
        self.phi = 0              # tilt angle of virtual camera
        self.Z = 0                # triangulation distance

        # variables used for plot functions
        self._sc = 0              #
        self._uc = np.zeros(2)    # micro image centers (MICs)
        self._u = np.zeros(2)     # micro image ray positions
        self._s = np.zeros(2)     # micro lens positions
        self._Uij = np.zeros(2)
        self._Fij = np.zeros(2)
        self._uU = np.zeros(2)
        self._uL = np.zeros(2)
        self._sU = np.zeros(2)
        self._sL = np.zeros(2)
        self._UijU = np.zeros(2)
        self._UijL = np.zeros(2)

        self.console_msg = []

    def refo(self):

        # local variable initialization
        j = np.zeros(2); i = np.zeros(2)
        mc = np.zeros(2)
        mij = np.zeros(2); qij = np.zeros(2)
        mU = np.zeros(2); mL = np.zeros(2)
        mijU = np.zeros(2); mijL = np.zeros(2)
        FijU = np.zeros(2); FijL = np.zeros(2)
        qijU = np.zeros(2); qijL = np.zeros(2)

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

        # function to solve linear system set via pseudo inverse
        pseudo_inv = lambda X: np.dot(np.transpose(X), np.linalg.inv(np.dot(X, np.transpose(X))))

        # ray intersections behind image sensor
        b_new = self._bU - np.dot(pseudo_inv(np.array([[-mij[0], 1], [-mij[1], 1]])), np.array([self._s[0], self._s[1]]))[0]
        b_new_m = self._bU - np.dot(pseudo_inv(np.array([[-mijL[0], 1], [-mijU[1], 1]])), np.array([self._sL[0], self._sU[1]]))[0]
        b_new_p = self._bU - np.dot(pseudo_inv(np.array([[-mijU[0], 1], [-mijL[1], 1]])), np.array([self._sU[0], self._sL[1]]))[0]

        # check if refocused object plane not at infinity
        if (self._fU <= self._bU and self._a >= 0) and b_new > self._fU:
            # get distances from refocused image side planes
            d_new = (1/self._fU-1/b_new)**-1 + self._bU + self._HH
            d_new_p = (1/self._fU-1/b_new_p)**-1 + self._bU + self._HH
            d_new_m = (1/self._fU-1/b_new_m)**-1 + self._bU + self._HH

            # solve for ray intersections in object space to obtain distances and DoF
            self.d = np.dot(pseudo_inv(np.array([[-qij[0], 1], [-qij[1], 1]])), np.array([self._Uij[0], self._Uij[1]]))[0] + self._bU + self._HH
            self.d_p = np.dot(pseudo_inv(np.array([[-qijU[0], 1], [-qijL[1], 1]])), np.array([self._UijU[0], self._UijL[1]]))[0] + self._bU + self._HH
            self.d_m = np.dot(pseudo_inv(np.array([[-qijL[0], 1], [-qijU[1], 1]])), np.array([self._UijL[0], self._UijU[1]]))[0] + self._bU + self._HH
            self.dof = self.d_p - self.d_m

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
                #d_new_m = float('Inf')
                self.dof = float('Inf')
            else:
                self.d_m = np.dot(pseudo_inv(np.array([[-qijL[0], 1], [-qijU[1], 1]])),
                                  np.array([self._UijL[0], self._UijU[1]]))[0] + self._bU + self._HH
                d_new_m = (1 / self._fU - 1 / b_new_m) ** -1 + self._bU + self._HH
                self.dof = self.d_p - self.d_m
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
                self.d_m = np.dot(pseudo_inv(np.array([[-qijL[0], 1], [-qijU[1], 1]])),
                                  np.array([self._UijL[0], self._UijU[1]]))[0] + self._bU + self._HH
                d_new_m = (1/self._fU - 1/b_new_m) ** -1 + self._bU + self._HH
                self.dof = self.d_p - self.d_m
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
                self.d_p = np.dot(pseudo_inv(np.array([[-qijU[0], 1], [-qijL[1], 1]])),
                                  np.array([self._UijU[0], self._UijL[1]]))[0] + self._bU + self._HH
                d_new_p = (1 / self._fU - 1 / b_new_p) ** -1 + self._bU + self._HH

        # comparison of image and object side approach (for debug purposes)
        if not (np.equal(np.round(d_new), np.round(self.d)) or np.equal(np.round(d_new_p), np.round(self.d_p)) or \
               np.equal(np.round(d_new_m), np.round(self.d_m))):
            raise AssertionError('Results for object and image side intersections are different.')

        return True

    def plt_refo(self, plane_th=.5, ray_th=.5):

        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError('matplotlib not available')

        # ensure refo method runs in advance
        self.refo()

        plot_lim = 5000  # set 50 meter as maximum plot distance
        if self.d_p > 0 and self.d_p != float('Inf'):
            large_val = self.d_p
        elif self.d_m > 0 and self.d_m < plot_lim:
            large_val = self.d_m
        else:
            large_val = plot_lim

        xmax = np.round(large_val+large_val/10)

        ax = plt.figure().add_subplot(111)
        plt.xlabel('$z_U$ [mm]'), plt.ylabel('$(u,s)$ [mm]')

        # optical axis
        plt.plot((0, xmax), (0, 0), linestyle='--', linewidth=plane_th, color='k')

        # main lens principal planes
        plt.plot((self._fs+self._hh+self._bU, self._fs+self._hh+self._bU), (-self._D/10, self._D/10), linestyle='--', linewidth=plane_th, color='k')
        plt.plot((self._fs+self._hh+self._bU+self._HH, self._fs+self._hh+self._bU+self._HH), (-self._D/10, self._D/10), linestyle='--', linewidth=plane_th, color='k')
        ax.text(self._fs+self._hh+self._bU+2, self._D/12+1, r'$H_{2U}$', fontsize=10)
        ax.text(self._fs+self._hh+self._bU+self._HH+2, self._D/12+1, r'$H_{1U}$', fontsize=10)

        # main lens focal point
        plt.plot((self._fs+self._hh+self._bU+self._HH+self._fU, self._fs+self._hh+self._bU+self._HH+self._fU), (-self._D/100, self._D/100), linestyle='-', linewidth=plane_th, color='k')
        ax.text(self._fs+self._hh+self._bU+self._HH+self._fU, -self._D/50, r'$F_U$', fontsize=10)

        # micro lens grid
        lens_y = np.arange(-self._sc*self._pm+self._pm/2, self._sc*self._pm+self._pm/2, self._pm)
        lens_f = np.arange(-self._sc*self._pm, self._sc*self._pm, self._pm)
        lens_x = (self._fs+self._hh) * np.ones(len(lens_y))
        plt.plot(lens_x, lens_y, linestyle='', marker='+', linewidth=plane_th, color='k') # micro lens borders
        plt.plot(lens_x, lens_f, linestyle='', marker='.', linewidth=plane_th, color='k') # micro optical axis
        plt.plot((self._fs, self._fs), (self._sc*self._pm, -self._sc*self._pm), linestyle='-', linewidth=plane_th, color='k')
        plt.plot((self._fs+self._hh, self._fs+self._hh), (self._sc*self._pm, -self._sc*self._pm), linestyle='-', linewidth=plane_th, color='k')

        # sensor plane
        plt.plot((0, 0), (self._sc*self._pm, -self._sc*self._pm), linestyle='-', linewidth=plane_th, color='k')
        pixel_y0 = np.arange(self._uc[0]-self._pp/2-np.ceil(self._pm/self._pp)/2*self._pp,
                             self._uc[0]+self._pp/2+np.ceil(self._pm/self._pp)/2*self._pp, self._pp)
        pixel_y2 = np.arange(self._uc[1]-self._pp/2-np.ceil(self._pm/self._pp)/2*self._pp,
                             self._uc[1]+self._pp/2+np.ceil(self._pm/self._pp)/2*self._pp, self._pp)
        pixel_x = np.zeros(len(pixel_y0))
        plt.plot(pixel_x, pixel_y0, linestyle='', marker='+', color='k')  # pixel borders 1
        plt.plot(pixel_x, pixel_y2, linestyle='', marker='+', color='k')  # pixel borders 2

        # intersection planes
        plt.plot((self.d, self.d), (self._D/10, -self._D/10), linestyle='-', linewidth=plane_th, color='c')
        plt.plot((self.d_p, self.d_p), (self._D/10, -self._D/10), linestyle='-', linewidth=plane_th, color='k')
        plt.plot((self.d_m, self.d_m), (self._D/10, -self._D/10), linestyle='-', linewidth=plane_th, color='r')

        # ray plots
        # chief rays connceting micro and main lens centres
        plt.plot((0, self._dA), (self._uc[0], 0), linestyle='-', linewidth=ray_th, color='y')
        plt.plot((0, self._dA), (self._uc[1], 0), linestyle='-', linewidth=ray_th, color='y')

        # micro lens image side ray
        plt.plot((0, self._fs), (self._u[0], self._s[0]), linestyle='-', linewidth=ray_th, color='b')
        plt.plot((0, self._fs), (self._u[1], self._s[1]), linestyle='-', linewidth=ray_th, color='g')

        # micro lens aux ray
        plt.plot((self._fs, self._fs+self._hh), (self._s[0], self._s[0]), linestyle='--', linewidth=ray_th, color='b')
        plt.plot((self._fs, self._fs+self._hh), (self._s[1], self._s[1]), linestyle='--', linewidth=ray_th, color='g')

        # main lens image side ray
        plt.plot((self._fs+self._hh, self._fs+self._hh+self._bU), (self._s[0], self._Uij[0]), linestyle='-', linewidth=ray_th, color='b')
        plt.plot((self._fs+self._hh, self._fs+self._hh+self._bU), (self._s[1], self._Uij[1]), linestyle='-', linewidth=ray_th, color='g')

        # principal plane aux ray
        plt.plot((self._fs+self._hh+self._bU, self._fs+self._hh+self._bU+self._HH), (self._Uij[0], self._Uij[0]), linestyle='--', linewidth=ray_th, color='b')
        plt.plot((self._fs+self._hh+self._bU, self._fs+self._hh+self._bU+self._HH), (self._Uij[1], self._Uij[1]), linestyle='--', linewidth=ray_th, color='g')

        # focal aux ray
        plt.plot((self._fs+self._hh+self._bU+self._HH, self._fs+self._hh+self._bU+self._HH+self._fU), (0, self._Fij[0]), linestyle='--', linewidth=ray_th, color='b')
        plt.plot((self._fs+self._hh+self._bU+self._HH, self._fs+self._hh+self._bU+self._HH+self._fU), (0, self._Fij[1]), linestyle='--', linewidth=ray_th, color='g')

        # object space ray
        ray_length = self.d # xmax
        plt.plot((self._fs+self._hh+self._bU+self._HH, ray_length), (self._Uij[0], 0), linestyle='-', linewidth=ray_th, color='b')
        plt.plot((self._fs+self._hh+self._bU+self._HH, ray_length), (self._Uij[1], 0), linestyle='-', linewidth=ray_th, color='g')

        # DoF rays
        # micro lens image side ray
        plt.plot((0, self._fs), (self._uU[0], self._sU[0]), linestyle='-', linewidth=ray_th, color='k')
        plt.plot((0, self._fs), (self._uL[0], self._sL[0]), linestyle='-', linewidth=ray_th, color='r')
        plt.plot((0, self._fs), (self._uU[1], self._sU[1]), linestyle='-', linewidth=ray_th, color='r')
        plt.plot((0, self._fs), (self._uL[1], self._sL[1]), linestyle='-', linewidth=ray_th, color='k')

        # micro lens aux ray
        plt.plot((self._fs, self._fs+self._hh), (self._sU[0], self._sU[0]), linestyle='--', linewidth=ray_th, color='k')
        plt.plot((self._fs, self._fs+self._hh), (self._sL[0], self._sL[0]), linestyle='--', linewidth=ray_th, color='r')
        plt.plot((self._fs, self._fs+self._hh), (self._sU[1], self._sU[1]), linestyle='--', linewidth=ray_th, color='r')
        plt.plot((self._fs, self._fs+self._hh), (self._sL[1], self._sL[1]), linestyle='--', linewidth=ray_th, color='k')

        # DoF main lens image side rays
        plt.plot((self._fs+self._hh, self._fs+self._hh+self._bU), (self._sU[0], self._UijU[0]), linestyle='-', linewidth=ray_th, color='k') #mij0U*self._bU+self._s[0]+self._pm-m0U*self._fs-mij0U*self._hh
        plt.plot((self._fs+self._hh, self._fs+self._hh+self._bU), (self._sL[0], self._UijL[0]), linestyle='-', linewidth=ray_th, color='r')
        plt.plot((self._fs+self._hh, self._fs+self._hh+self._bU), (self._sU[1], self._UijU[1]), linestyle='-', linewidth=ray_th, color='r')
        plt.plot((self._fs+self._hh, self._fs+self._hh+self._bU), (self._sL[1], self._UijL[1]), linestyle='-', linewidth=ray_th, color='k')

        # DoF principal plane aux ray
        plt.plot((self._fs+self._hh+self._bU, self._fs+self._hh+self._bU+self._HH), (self._UijU[0], self._UijU[0]), linestyle='--', linewidth=ray_th, color='k')
        plt.plot((self._fs+self._hh+self._bU, self._fs+self._hh+self._bU+self._HH), (self._UijL[0], self._UijL[0]), linestyle='--', linewidth=ray_th, color='r')
        plt.plot((self._fs+self._hh+self._bU, self._fs+self._hh+self._bU+self._HH), (self._UijU[1], self._UijU[1]), linestyle='--', linewidth=ray_th, color='r')
        plt.plot((self._fs+self._hh+self._bU, self._fs+self._hh+self._bU+self._HH), (self._UijL[1], self._UijL[1]), linestyle='--', linewidth=ray_th, color='k')

        # DoF main object side rays
        plt.plot((self._fs+self._hh+self._bU+self._HH, self.d_p), (self._UijU[0], 0), linestyle='-', linewidth=ray_th, color='k')
        plt.plot((self._fs+self._hh+self._bU+self._HH, self.d_m), (self._UijL[0], 0), linestyle='-', linewidth=ray_th, color='r')
        plt.plot((self._fs+self._hh+self._bU+self._HH, self.d_m), (self._UijU[1], 0), linestyle='-', linewidth=ray_th, color='r')
        plt.plot((self._fs+self._hh+self._bU+self._HH, self.d_p), (self._UijL[1], 0), linestyle='-', linewidth=ray_th, color='k')

        plt.show()

        return True


    def tria(self):

        # local variable initialisation
        mij = np.zeros(2)
        Uij = np.zeros(2)
        qij = np.zeros(2)

        # ray geometry calculation
        j = 1
        s = j * self._pm
        mc = -(s / self._dA)
        uc = -mc * self._fs + s
        self._u[0] = uc + self._pp * self._i
        mij[0] = -self._pp * self._i / self._fs
        mij[1] = (s - self._u[0]) / self._fs
        Uij[0] = mij[0] * self._bU
        Uij[1] = mij[1] * self._bU + s
        qij[0] = (mij[0] * self._fU - Uij[0]) / self._fU
        qij[1] = (mij[1] * self._fU - Uij[1]) / self._fU

        # function to solve linear system set via pseudo inverse
        pseudo_inv = lambda X: np.dot(np.transpose(X), np.linalg.inv(np.dot(X, np.transpose(X))))

        # locate object side related virtual camera position
        x_int, self.B = np.dot(pseudo_inv(np.array([[-qij[1], 1], [-qij[0], 1]])), np.array([Uij[1], Uij[0]]))
        self.phi = np.degrees(np.arctan(qij[0]))
        ent_pup_pos = self._bU + self._HH + x_int # longitudinal entrance pupil position

        # estimate baseline at entrance pupil
        self.B = qij[0] * x_int + Uij[0]
        bNew = self._bU
        self._ppNew = (-qij[1] * bNew + self.B) - (-qij[0] * bNew + self.B)

        # triangulation
        dxNew = np.transpose(self._dx) * self._ppNew # crashes if dx=0  and i=0
        self.Z = self.B * bNew / (dxNew + bNew * -np.tan(np.radians(self.phi)))
        #self.Z = self.Z + ent_pup_pos

        return True