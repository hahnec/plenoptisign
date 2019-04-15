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

    def plt_tria(self, ax, plane_th=.5, ray_th=.5, fontsize=11):
        ''' plot distance based on disparity, baseline and virtual camera orientation in a standard plenoptic camera '''

        # ensure refo method runs in advance
        self.tria()

        # set maximum plot distance
        z_max = self.Z if self.Z > 0 and self.Z != float('Inf') else 5000 # either furthest plane or 5m
        z_max += z_max/10 # add 10% space to max distance

        ax.set_title('Cross-sectional triangulation plot')
        ax.set_xlabel('$z_U$ [mm]'), ax.set_ylabel('$(u,s)$ [mm]')

        # optical axis
        ax.plot((0, z_max), (0, 0), linestyle='--', linewidth=plane_th, color='k')

        # main lens principal planes
        H2 = self.fs + self.hh + self.bU
        H1 = self.fs + self.hh + self.bU + self.HH
        ax.plot((H2, H2), (self._Uij[0], -self._Uij[0]), linestyle='--', linewidth=plane_th, color='k')
        ax.plot((H1, H1), (self._Uij[0], -self._Uij[0]), linestyle='--', linewidth=plane_th, color='k')
        ax.text(H2 + 2, self.D / 12 + 1, r'$H_{2U}$', fontsize=fontsize)
        ax.text(H1 + 2, self.D / 12 + 1, r'$H_{1U}$', fontsize=fontsize)

        # main lens focal point
        ax.plot((H1 + self.fU, H1 + self.fU), (self._Uij[0]/50, -self._Uij[0]/50), 'k-', linewidth=plane_th)
        ax.text(H1 + self.fU, self._UijU[0]*.15, r'$F_U$', fontsize=fontsize)

        # micro lens grid
        lens_y = np.arange(-self._sc * self.pm + self.pm / 2, self._sc * self.pm + self.pm / 2, self.pm)
        lens_f = np.arange(-self._sc * self.pm, self._sc * self.pm, self.pm)
        lens_x = (self.fs + self.hh) * np.ones(len(lens_y))
        ax.plot(lens_x, lens_y, linestyle='', marker='+', linewidth=plane_th, color='k')  # micro lens borders
        ax.plot(lens_x, lens_f, linestyle='', marker='.', linewidth=plane_th, color='k')  # micro optical axis
        ax.plot((self.fs, self.fs), (self._sc * self.pm, -self._sc * self.pm), 'k-', linewidth=plane_th)
        ax.plot((self.fs + self.hh, self.fs + self.hh), (self._sc * self.pm, -self._sc * self.pm), 'k-', linewidth=plane_th)

        # sensor plane
        ax.plot((0, 0), (self._sc * self.pm, -self._sc * self.pm), linestyle='-', linewidth=plane_th, color='k')

        # exit and entrance pupil plane
        ax.plot((self.dA, self.dA), (self._Uij[0], -self._Uij[0]), linestyle='--', linewidth=plane_th, color='k')
        ax.plot((self._ent_pup_pos, self._ent_pup_pos), (self._Uij[0], -self._Uij[0]), 'k--', linewidth=plane_th)
        ax.text(self.dA*1.1, -self.D / 3, r"$d_{A'}$", fontsize=fontsize)
        ax.text(self._ent_pup_pos*1.1, -self.D / 3, r"$d_{A''}$", fontsize=fontsize)

        # intersection planes
        ax.plot((self.Z, self.Z), (self._Uij[0], -self._Uij[0]), linestyle='-', linewidth=plane_th, color='r')
        ax.text(self.Z + self.Z/100, self._Uij[0]*.8, r"$\Delta x="+str(self.dx)+"$", color='r', fontsize=fontsize)

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
        ax.text(self._ent_pup_pos*.8, self.B*.5, r"$B_{"+str(self.G)+"}$", color='r', fontsize=fontsize)
        ax.plot((self._ent_pup_pos, self._ent_pup_pos), (0, self.B), linestyle='-', linewidth=ray_th*2, color='r')

        return ax