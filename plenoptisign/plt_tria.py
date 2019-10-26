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

    def plt_tria(self, ax, plane_th=.9, ray_th=.75, fontsize=12):
        ''' This method draws the triangulation distance in 2-D space calculated from :func:`tria()`.

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

        # run tria method in advance
        self.tria()

        # set maximum plot distance
        z_max = self.Z if self.Z > 0 and self.Z != float('Inf') else 5000 # either furthest plane or 5m
        z_max *= 1.05   # add 5% space to max distance

        # set vertical plot limits
        y_min = min(self.sd[0]/2, self._Uij[0], self.D/2)
        ax.set_ylim([-y_min*1.2, y_min*1.2])

        ax.set_title('Cross-sectional triangulation plot', pad=10)
        ax.set_xlabel('$z$ [mm]'), ax.set_ylabel('$y$ [mm]')

        # optical axis
        ax.plot((0, z_max), (0, 0), linestyle='--', linewidth=plane_th, color='k')

        # main lens principal planes
        H2 = self.fs + self.hh + self.bU
        H1 = self.fs + self.hh + self.bU + self.HH
        ax.plot((H2, H2), (y_min*.85, -y_min*.85), linestyle='--', linewidth=plane_th, color='k')
        ax.plot((H1, H1), (y_min*.85, -y_min*.85), linestyle='--', linewidth=plane_th, color='k')
        ax.text(H2 + 2, y_min*.9, r'$H_{2U}$', fontsize=fontsize, horizontalalignment='center')
        ax.text(H1 + 2, y_min*.9, r'$H_{1U}$', fontsize=fontsize, horizontalalignment='center')

        # main lens focal point
        ax.plot((H1 + self.fU, H1 + self.fU), (y_min/50, -y_min/50), 'k-', linewidth=plane_th)
        ax.text(H1 + self.fU, -y_min*.15, r'$F_U$', fontsize=fontsize)

        # micro lens grid
        lens_y = np.arange(-self.sd[0]/2+self.pm/2, self.sd[0]/2+self.pm/2, self.pm)
        lens_f = np.arange(-self.sd[0]/2, self.sd[0]/2, self.pm)
        lens_x = (self.fs + self.hh) * np.ones(len(lens_y))
        ax.plot(lens_x, lens_y, linestyle='', marker='+', linewidth=plane_th, color='k')  # micro lens borders
        ax.plot(lens_x, lens_f, linestyle='', marker='.', linewidth=plane_th, color='k')  # micro optical axis
        ax.plot((self.fs, self.fs), (self.sd[0]/2, -self.sd[0]/2), 'k-', linewidth=plane_th)
        ax.plot((self.fs + self.hh, self.fs + self.hh), (self.sd[0]/2, -self.sd[0]/2), 'k-', linewidth=plane_th)

        # sensor plane
        ax.plot((0, 0), (self.sd[0]/2, -self.sd[0]/2), linestyle='-', linewidth=plane_th, color='k')

        # exit and entrance pupil plane
        ax.plot((self.dA, self.dA), (y_min*.85, -y_min*.85), linestyle='--', linewidth=plane_th, color='k')
        ax.plot((self._ent_pup_pos, self._ent_pup_pos), (y_min*.85, -y_min*.85), 'k--', linewidth=plane_th)
        ax.text(self.dA*1.05, -y_min, r"$d_{A'}$", fontsize=fontsize, horizontalalignment='center')
        ax.text(self._ent_pup_pos*.8, -y_min, r"$d_{A''}$", fontsize=fontsize, horizontalalignment='center')

        # intersection planes
        ax.plot((self.Z, self.Z), (y_min*.95, -y_min), linestyle='-', linewidth=plane_th, color='r')
        ax.text(self.Z, y_min, r'$\Delta x='+str(self.dx)+'$', color='r', fontsize=fontsize, horizontalalignment='right')

        # ray plots

        # virtual camera 1
        ax.plot((H1, self._ent_pup_pos), (self._Uij[0], self.B), 'r--', linewidth=ray_th)
        ax.plot((H1, self.Z), (self._Uij[0], self._qij[0]*(self.Z + self._intersect) + self._Uij[0]), 'r--',linewidth=ray_th)
        ax.plot((self._ent_pup_pos), (self.B), 'o', color='r', linewidth=.2)

        #virtual camera 2
        Uij_y = ((self.pm / self.dA) * H2 - self.pm)
        ax.plot((self.fs + self.hh, H2), (-self.pm, Uij_y), linestyle='-', linewidth=ray_th, color='y')
        ax.plot((H2, H1), (Uij_y, Uij_y), linestyle='--', linewidth=ray_th, color='y')
        ax.plot((H1, self.Z), (Uij_y, self._qij[0] * (self.Z + self._intersect) + self._Uij[0]), 'y-', linewidth=ray_th)
        ax.plot((H1, self._ent_pup_pos), (Uij_y, 0), linestyle='-', linewidth=ray_th, color='y')
        ax.plot((self._ent_pup_pos), (0), 'o', color='r', linewidth=.2)
        ax.plot((self._ent_pup_pos, self.Z), (0, 0), linestyle='--', linewidth=ray_th, color='r')

        # baseline
        ax.text(self._ent_pup_pos*1.1, self.B*.5, r"$B_{"+str(self.G)+"}$",
                color='r', fontsize=fontsize, horizontalalignment='right')
        ax.plot((self._ent_pup_pos, self._ent_pup_pos), (0, self.B), linestyle='-', linewidth=ray_th*2, color='r')

        z_min = min(0, self._ent_pup_pos*5)
        ax.set_xlim([z_min, z_max])

        # swap coordinates for current cursor position
        self._ax = ax
        ax.format_coord = self.format_coord_2d

        return ax
