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

class Mixin:

    def plt_refo(self, ax, plane_th=.9, ray_th=.75, fontsize=12):
        ''' This method draws the refocusing distance and depth of field limits in 2-D space based on :func:`refo()`.

        :param ax: instance of matplotlib's Axes
        :param plane_th: line thickness of depth plane
        :param ray_th: line thickness of rays
        :param fontsize: font size of scientific notations
        :type ax: :class:`~matplotlib:matplotlib.axes.Axes`
        :type plane_th: float
        :type ray_th: float
        :type fontsize: float

        :return: **ax**

        '''

        # run refo method in advance
        self.refo()

        # set maximum plot distance
        z_max = self.d_p if self.d_m > 0 and self.d_p != float('Inf') else 5000     # either furthest plane or 5m
        z_max += z_max/10 # add 10% space to max distance

        # set vertical plot limits
        y_min = min(self.sd[0]/2, self._UijU[0], self.D/2)
        ax.set_ylim([-y_min*1.2, y_min*1.2])

        ax.set_title('Cross-sectional refocusing plot', pad=10)
        ax.set_xlabel('$z$ [mm]'), ax.set_ylabel('$y$ [mm]')

        # optical axis
        ax.plot((0, z_max), (0, 0), linestyle='--', linewidth=plane_th, color='k')

        # main lens principal planes
        ax.plot((self.fs+self.hh+self.bU, self.fs+self.hh+self.bU), (self._UijU[0], -self._UijU[0]), 'k--', linewidth=plane_th)
        ax.plot((self.fs+self.hh+self.bU+self.HH, self.fs+self.hh+self.bU+self.HH), (self._UijU[0], -self._UijU[0]), 'k--', linewidth=plane_th)
        ax.text(self.fs+self.hh+self.bU+2, self._UijU[0]*.5, r'$H_{2U}$', fontsize=fontsize)
        ax.text(self.fs+self.hh+self.bU+self.HH+2, self._UijU[0]*.5, r'$H_{1U}$', fontsize=fontsize)

        # main lens focal point
        ax.plot((self.fs+self.hh+self.bU+self.HH+self.fU, self.fs+self.hh+self.bU+self.HH+self.fU), (y_min/50, -y_min/50), 'k-', linewidth=plane_th)
        ax.text(self.fs+self.hh+self.bU+self.HH+self.fU, -y_min*.12, r'$F_U$', fontsize=fontsize)

        # micro lens grid
        lens_y = np.arange(-self.sd[0]/2+self.pm/2, self.sd[0]/2+self.pm/2, self.pm)
        lens_f = np.arange(-self.sd[0]/2, self.sd[0]/2, self.pm)
        lens_x = (self.fs+self.hh) * np.ones(len(lens_y))
        ax.plot(lens_x, lens_y, linestyle='', marker='+', linewidth=plane_th, color='k')    # micro lens borders
        ax.plot(lens_x, lens_f, linestyle='', marker='.', linewidth=plane_th, color='k')    # micro optical axis
        ax.plot((self.fs, self.fs), (self.sd[0]/2, -self.sd[0]/2), 'k-', linewidth=plane_th)
        ax.plot((self.fs+self.hh, self.fs+self.hh), (self.sd[0]/2, -self.sd[0]/2), 'k-', linewidth=plane_th)

        # sensor plane
        ax.plot((0, 0), (self.sd[0]/2, -self.sd[0]/2), 'k-', linewidth=plane_th)
        pixel_y0 = np.arange(self._uc[0]-self.pp/2-np.ceil(self.pm/self.pp)/2*self.pp,
                             self._uc[0]+self.pp/2+np.ceil(self.pm/self.pp)/2*self.pp, self.pp)
        pixel_y2 = np.arange(self._uc[1]-self.pp/2-np.ceil(self.pm/self.pp)/2*self.pp,
                             self._uc[1]+self.pp/2+np.ceil(self.pm/self.pp)/2*self.pp, self.pp)
        pixel_x0 = np.zeros(len(pixel_y0))
        pixel_x2 = np.zeros(len(pixel_y2))
        ax.plot(pixel_x0, pixel_y0, linestyle='', marker='+', color='k')  # pixel borders 1
        ax.plot(pixel_x2, pixel_y2, linestyle='', marker='+', color='k')  # pixel borders 2

        # intersection planes
        ax.plot((self.d, self.d), (y_min*.85, -y_min), 'c-', linewidth=plane_th)
        ax.plot((self.d_p, self.d_p), (y_min*.85, -y_min), 'k-', linewidth=plane_th)
        ax.plot((self.d_m, self.d_m), (y_min*.85, -y_min), 'r-', linewidth=plane_th)
        ax.text(self.d, y_min, r'$d_a$', fontsize=fontsize, color='c', horizontalalignment='center', verticalalignment='top')
        ax.text(self.d_p, y_min, r'$d_{a+}$', fontsize=fontsize, color='k', horizontalalignment='center', verticalalignment='top')
        ax.text(self.d_m, y_min, r'$d_{a-}$', fontsize=fontsize, color='r', horizontalalignment='center', verticalalignment='top')

        # ray plots
        # chief rays connecting micro and main lens centres
        ax.plot((self.fs + self.hh, self.dA), (self._s[0], 0), linestyle='-', linewidth=ray_th, color='y')
        ax.plot((self.fs + self.hh, self.dA), (self._s[1], 0), linestyle='-', linewidth=ray_th, color='y')

        # micro lens image side ray
        ax.plot((0, self.fs), (self._u[0], self._s[0]), linestyle='-', linewidth=ray_th, color='b')
        ax.plot((0, self.fs), (self._u[1], self._s[1]), linestyle='-', linewidth=ray_th, color='g')

        # micro lens aux ray
        ax.plot((self.fs, self.fs+self.hh), (self._s[0], self._s[0]), linestyle='--', linewidth=ray_th, color='b')
        ax.plot((self.fs, self.fs+self.hh), (self._s[1], self._s[1]), linestyle='--', linewidth=ray_th, color='g')

        # main lens image side ray
        ax.plot((self.fs+self.hh, self.fs+self.hh+self.bU), (self._s[0], self._Uij[0]), 'b-', linewidth=ray_th)
        ax.plot((self.fs+self.hh, self.fs+self.hh+self.bU), (self._s[1], self._Uij[1]), 'g-', linewidth=ray_th)

        # principal plane aux ray
        ax.plot((self.fs+self.hh+self.bU, self.fs+self.hh+self.bU+self.HH), (self._Uij[0], self._Uij[0]), 'b--', linewidth=ray_th)
        ax.plot((self.fs+self.hh+self.bU, self.fs+self.hh+self.bU+self.HH), (self._Uij[1], self._Uij[1]), 'g--', linewidth=ray_th)

        # focal aux ray
        ax.plot((self.fs+self.hh+self.bU+self.HH, self.fs+self.hh+self.bU+self.HH+self.fU), (0, self._Fij[0]), 'b--', linewidth=ray_th)
        ax.plot((self.fs+self.hh+self.bU+self.HH, self.fs+self.hh+self.bU+self.HH+self.fU), (0, self._Fij[1]), 'g--', linewidth=ray_th)

        # object space ray
        ray_length = self.d
        ax.plot((self.fs+self.hh+self.bU+self.HH, ray_length), (self._Uij[0], 0), 'b-', linewidth=ray_th)
        ax.plot((self.fs+self.hh+self.bU+self.HH, ray_length), (self._Uij[1], 0), 'g-', linewidth=ray_th)

        # DoF rays
        # micro lens image side ray
        ax.plot((0, self.fs), (self._uU[0], self._sU[0]), 'k-', linewidth=ray_th)
        ax.plot((0, self.fs), (self._uL[0], self._sL[0]), 'r-', linewidth=ray_th)
        ax.plot((0, self.fs), (self._uU[1], self._sU[1]), 'r-', linewidth=ray_th)
        ax.plot((0, self.fs), (self._uL[1], self._sL[1]), 'k-', linewidth=ray_th)

        # micro lens aux ray
        ax.plot((self.fs, self.fs+self.hh), (self._sU[0], self._sU[0]), 'k--', linewidth=ray_th)
        ax.plot((self.fs, self.fs+self.hh), (self._sL[0], self._sL[0]), 'r--', linewidth=ray_th)
        ax.plot((self.fs, self.fs+self.hh), (self._sU[1], self._sU[1]), 'r--', linewidth=ray_th)
        ax.plot((self.fs, self.fs+self.hh), (self._sL[1], self._sL[1]), 'k--', linewidth=ray_th)

        # DoF main lens image side rays
        ax.plot((self.fs+self.hh, self.fs+self.hh+self.bU), (self._sU[0], self._UijU[0]), 'k-', linewidth=ray_th)
        ax.plot((self.fs+self.hh, self.fs+self.hh+self.bU), (self._sL[0], self._UijL[0]), 'r-', linewidth=ray_th)
        ax.plot((self.fs+self.hh, self.fs+self.hh+self.bU), (self._sU[1], self._UijU[1]), 'r-', linewidth=ray_th)
        ax.plot((self.fs+self.hh, self.fs+self.hh+self.bU), (self._sL[1], self._UijL[1]), 'k-', linewidth=ray_th)

        # DoF principal plane aux ray
        ax.plot((self.fs+self.hh+self.bU, self.fs+self.hh+self.bU+self.HH), (self._UijU[0], self._UijU[0]), 'k--', linewidth=ray_th)
        ax.plot((self.fs+self.hh+self.bU, self.fs+self.hh+self.bU+self.HH), (self._UijL[0], self._UijL[0]), 'r--', linewidth=ray_th)
        ax.plot((self.fs+self.hh+self.bU, self.fs+self.hh+self.bU+self.HH), (self._UijU[1], self._UijU[1]), 'r--', linewidth=ray_th)
        ax.plot((self.fs+self.hh+self.bU, self.fs+self.hh+self.bU+self.HH), (self._UijL[1], self._UijL[1]), 'k--', linewidth=ray_th)

        # DoF main object side rays
        ax.plot((self.fs+self.hh+self.bU+self.HH, self.d_p), (self._UijU[0], 0), 'k-', linewidth=ray_th)
        ax.plot((self.fs+self.hh+self.bU+self.HH, self.d_m), (self._UijL[0], 0), 'r-', linewidth=ray_th)
        ax.plot((self.fs+self.hh+self.bU+self.HH, self.d_m), (self._UijU[1], 0), 'r-', linewidth=ray_th)
        ax.plot((self.fs+self.hh+self.bU+self.HH, self.d_p), (self._UijL[1], 0), 'k-', linewidth=ray_th)

        # swap coordinates for current cursor position
        self._ax = ax
        ax.format_coord = self._format_coord_2d

        return ax
