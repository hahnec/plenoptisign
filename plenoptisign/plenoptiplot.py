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

def plt_refo(self, plane_th=.5, ray_th=.5, fontsize=11):
    ''' plots the distance and depth of field to a plane computationally focused based on a standard plenoptic camera '''

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError('Please install matplotlib package.')

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
    ax.text(self._fs+self._hh+self._bU+2, self._D/12+1, r'$H_{2U}$', fontsize=fontsize)
    ax.text(self._fs+self._hh+self._bU+self._HH+2, self._D/12+1, r'$H_{1U}$', fontsize=fontsize)

    # main lens focal point
    plt.plot((self._fs+self._hh+self._bU+self._HH+self._fU, self._fs+self._hh+self._bU+self._HH+self._fU), (-self._D/100, self._D/100), linestyle='-', linewidth=plane_th, color='k')
    ax.text(self._fs+self._hh+self._bU+self._HH+self._fU, -self._D/50, r'$F_U$', fontsize=fontsize)

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
    plt.plot((self._fs + self._hh, self._dA), (self._s[0], 0), linestyle='-', linewidth=ray_th, color='y')
    plt.plot((self._fs + self._hh, self._dA), (self._s[1], 0), linestyle='-', linewidth=ray_th, color='y')

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

def plt_tria(self, plane_th=.5, ray_th=.5, fontsize=11):
    ''' plots the distance from disparity just as baseline and virtual camera orientation in a standard plenoptic camera '''

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError('Please install matplotlib package.')

    # ensure refo method runs in advance
    self.tria()

    plot_lim = 5000  # set 50 meter as maximum plot distance
    if self.Z > 0 and self.Z != float('Inf'):
        large_val = self.Z
    else:
        large_val = plot_lim

    xmax = np.round(large_val + large_val / 10) # add 10% of the depth plane distance

    ax = plt.figure().add_subplot(111)
    plt.xlabel('$z_U$ [mm]'), plt.ylabel('$(u,s)$ [mm]')

    # optical axis
    plt.plot((0, xmax), (0, 0), linestyle='--', linewidth=plane_th, color='k')

    # main lens principal planes
    H2 = self._fs + self._hh + self._bU
    H1 = self._fs + self._hh + self._bU + self._HH
    plt.plot((H2, H2), (-self._D / 10, self._D / 10), linestyle='--', linewidth=plane_th, color='k')
    plt.plot((H1, H1), (-self._D / 10, self._D / 10), linestyle='--', linewidth=plane_th, color='k')
    ax.text(H2 + 2, self._D / 12 + 1, r'$H_{2U}$', fontsize=fontsize)
    ax.text(H1 + 2, self._D / 12 + 1, r'$H_{1U}$', fontsize=fontsize)

    # main lens focal point
    plt.plot((H1 + self._fU, H1 + self._fU), (-self._D/100, self._D/100), linestyle='-', linewidth=plane_th, color='k')
    ax.text(H1 + self._fU, -self._D / 50, r'$F_U$', fontsize=fontsize)

    # micro lens grid
    lens_y = np.arange(-self._sc * self._pm + self._pm / 2, self._sc * self._pm + self._pm / 2, self._pm)
    lens_f = np.arange(-self._sc * self._pm, self._sc * self._pm, self._pm)
    lens_x = (self._fs + self._hh) * np.ones(len(lens_y))
    plt.plot(lens_x, lens_y, linestyle='', marker='+', linewidth=plane_th, color='k')  # micro lens borders
    plt.plot(lens_x, lens_f, linestyle='', marker='.', linewidth=plane_th, color='k')  # micro optical axis
    plt.plot((self._fs, self._fs), (self._sc * self._pm, -self._sc * self._pm), linestyle='-',
             linewidth=plane_th, color='k')
    plt.plot((self._fs + self._hh, self._fs + self._hh), (self._sc * self._pm, -self._sc * self._pm),
             linestyle='-', linewidth=plane_th, color='k')

    # sensor plane
    plt.plot((0, 0), (self._sc * self._pm, -self._sc * self._pm), linestyle='-', linewidth=plane_th, color='k')

    # exit and entrance pupil plane
    plt.plot((self._dA, self._dA), (-self._D / 10, self._D / 10), linestyle='--', linewidth=plane_th, color='k')
    plt.plot((self._ent_pup_pos, self._ent_pup_pos), (-self._D / 10, self._D / 10), linestyle='--', linewidth=plane_th, color='k')
    ax.text(self._dA + 2, self._D / 12 + 1, r"$d_{A'}$", fontsize=fontsize)
    ax.text(self._ent_pup_pos + 2, self._D / 12 + 1, r"$d_{A''}$", fontsize=fontsize)

    # intersection planes
    plt.plot((self.Z, self.Z), (self._D / 10, -self._D / 10), linestyle='-', linewidth=plane_th, color='r')
    ax.text(self.Z + self.Z/100, self._D / 12 + 1, r"$\Delta x="+str(self._dx)+"$", color='r', fontsize=fontsize)

    # ray plots

    # virtual camera 1
    plt.plot((self._fs + self._hh, H2), (0, self._Uij[0]), linestyle='-', linewidth=ray_th, color='b')
    plt.plot((self._fs + self._hh, H2), (self._pm, self._Uij[1]), linestyle='-', linewidth=ray_th, color='b')

    plt.plot((H2, H1), (self._Uij[0], self._Uij[0]), linestyle='--', linewidth=ray_th, color='b')
    plt.plot((H2, H1), (self._Uij[1], self._Uij[1]), linestyle='--', linewidth=ray_th, color='b')

    plt.plot((H1, self._ent_pup_pos), (self._Uij[1], self._qij[1] * self._intersect + self._Uij[1]), linestyle='-', linewidth=ray_th, color='b')
    plt.plot((H1, self._ent_pup_pos), (self._Uij[0], self._qij[0] * self._intersect + self._Uij[0]), linestyle='--', linewidth=ray_th, color='r')

    plt.plot((H1, self.Z), (self._Uij[1], self._qij[1] * (self.Z + self._intersect) + self._Uij[1]), linestyle='-', linewidth=ray_th, color='b')
    plt.plot((H1, self.Z), (self._Uij[0], self._qij[0] * (self.Z + self._intersect) + self._Uij[0]), linestyle='--',linewidth=ray_th, color='r')
    plt.plot((self._ent_pup_pos), (self._qij[0] * self._intersect + self._Uij[0]), 'o', color='r', linewidth=.2)

    #virtual camera 2
    Uij_y = ((self._pm / self._dA) * H2 - self._pm)
    plt.plot((self._fs + self._hh, H2), (-self._pm, Uij_y), linestyle='-', linewidth=ray_th, color='y')

    plt.plot((H2, H1), (Uij_y, Uij_y), linestyle='--', linewidth=ray_th, color='y')
    plt.plot((H1, self.Z), (Uij_y, self._qij[0] * (self.Z + self._intersect) + self._Uij[0]), linestyle='-', linewidth=ray_th, color='y')
    plt.plot((H1, self._ent_pup_pos), (Uij_y, 0), linestyle='-', linewidth=ray_th, color='y')
    plt.plot((self._ent_pup_pos), (0), 'o', color='r', linewidth=.2)
    plt.plot((self._ent_pup_pos, self.Z), (0, 0), linestyle='--', linewidth=ray_th, color='r')

    # baseline
    ax.text(self._ent_pup_pos-100, self._Uij[0]+self._Uij[0]/10, r"$B_{"+str(self._G)+"}$", color='r', fontsize=fontsize)

    plt.show()

    return True
