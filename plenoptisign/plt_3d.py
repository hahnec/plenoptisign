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

# external libs
from numpy import array, meshgrid, ones, arange

# local python files
from . import PlenoptisignError

class Mixin:

    def plt_3d_init(self, plt3d):
        ''' set initial parameters for 3D plot '''

        # perspective view init
        plt3d.view_init(elev=30, azim=-120)

        # start plotting axis matter
        plt3d.set_xlabel('z [mm]')
        plt3d.set_ylabel('x [mm]')
        plt3d.set_zlabel('y [mm]')

        return True

    def plt_3d(self, plt3d, amin, sen_dims=array([24.048, 36.072]), dep_type=False):
        ''' draw depth planes for Axes3D class instance based on respective provided method (refo or tria) '''

        x, y, z = ([] for _ in range(3))
        iter_range = [amin, amin+5]
        planes = arange(iter_range[0], iter_range[1], 1)[::-1]

        try:
            for el in planes:
                # compute distances depending on depth types
                if dep_type:
                    self.dx = el
                    self.tria()
                    z.append(float(self.Z))
                else:
                    self.a = el
                    self.refo()
                    z.append(float(self.d))

                # compute field of view
                yy, xx = sen_dims/self.bU*z[-1]
                x.append(xx)
                y.append(yy)

        except TypeError as e:
            raise PlenoptisignError(e)

        # determine maximum plot distance
        z_max = max(z) if max(z) != float('inf') else self.non_inf_max(z)
        max_dist = z_max*1.1

        plt3d.set_title('3-D ' + ('refo', 'tria')[dep_type] + ' plot')

        # plot camera axis and sensor
        plt3d.scatter(0, 0, 0, s=20, color='k')
        plt3d.plot([0, max_dist], [0, 0], [0, 0], 'k--')
        yy, xx = meshgrid((-sen_dims[0]/2, sen_dims[0]/2), (-sen_dims[1]/2, sen_dims[1]/2))
        plt3d.plot_surface(-self.bU*ones(xx.shape), xx, yy, color='k', alpha=.8)

        # plot the depth planes
        for i in range(len(z)):
            if z[i] != float('inf'):
                yy, xx = meshgrid((-y[i]/2, y[i]/2), (-x[i]/2, x[i]/2))
                zz = z[i]*ones(xx.shape)
                plt3d.plot_surface(zz, xx, yy, color='r', alpha=.5) # depth plane
                plt3d.scatter([z[i]], [0], [0], s=20, color='r') # plane-axis intersection

                # plot marker
                num_str = str(round(planes[i],1))
                label_str = "$d_{"+num_str+"}$" if dep_type else "$Z_{("+str(self.G)+', '+num_str+")}$"
                plt3d.text(z[i], x[i]/2, y[i]/2, s=label_str, fontsize=18, family='sans-serif')

        # plot field of view lines
        x_hw = self.non_inf_max(x)/2
        y_hw = self.non_inf_max(y)/2
        plt3d.plot([-self.bU, z_max], [-sen_dims[1]/2, x_hw], [-sen_dims[0]/2, y_hw], 'k-.', alpha=.8, linewidth=.5)
        plt3d.plot([-self.bU, z_max], [-sen_dims[1]/2, x_hw], [sen_dims[0]/2, -y_hw], 'k-.', alpha=.8, linewidth=.5)
        plt3d.plot([-self.bU, z_max], [sen_dims[1]/2, -x_hw], [-sen_dims[0]/2, y_hw], 'k-.', alpha=.8, linewidth=.5)
        plt3d.plot([-self.bU, z_max], [sen_dims[1]/2, -x_hw], [sen_dims[0]/2, -y_hw], 'k-.', alpha=.8, linewidth=.5)

        return plt3d

    @staticmethod
    def non_inf_max(input):
        ''' get maximum value in input list without consideration of infinity '''

        try:
            max_val = max([x for x in input if x != float('inf')])
        except TypeError:
            max_val = input if isinstance(input, (int, float)) else float('nan')

        return max_val